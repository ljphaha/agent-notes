# 第一章实验
## 1-2 Web 搜索 Agent（ReAct 循环）

> 实验代码来自 [bojieli/ai-agent-book](https://github.com/bojieli/ai-agent-book) 的 `chapter1/web-search-agent/`，命令均在该目录下运行。
> 本文件夹只保存我的实验报告和运行结果：
>
> | 文件 | 对应报告章节 |
> |---|---|
> | `results/demo.json` | 1. 小规模观察（离线演示） |
> | `results/live.json` | 3. 联网运行（账号相关的 ID 已替换为 `<redacted>`） |

### 1. 小规模观察：离线演示

指令：
```bash
python main.py --provider offline-demo --output demo.json
```

运行条件：
- 日期：2026-11-10
- 提供商：`offline-demo`（不调用模型，不需要 API Key）
- 注意：离线演示回放的是**预先写好的示例轨迹**，搜索结果也是编写的（标有"示例结果"）。它只证明流程能展示出来，不代表真实搜索服务已经连通。

输出
```
============================================================
🧪 离线演示模式（示例轨迹，非真实搜索结果）
============================================================
问题: Moonshot AI 的 Context Caching 是什么技术？
------------------------------------------------------------
🔍 ReAct 轨迹（想 → 做 → 看）:

💭 [1] 思考: 用户想了解 Context Caching。这是 Moonshot 的特性，我需要先搜索官方说明，确认它的定义和作用。
🔧 [1] 行动: 调用工具 web_search  参数={"query": "Moonshot AI Context Caching 是什么"}
👀 [1] 观察: （示例结果）Context Caching 是一种上下文缓存机制：把重复使用的前缀（如长系统提示、文档）缓存在服务端，后续请求命中缓存即可复用，从而降低重复计算与费用。
💭 [2] 思考: 已知大致定义，但还缺少适用场景。再搜一次它的典型用途以便答得更完整。
🔧 [2] 行动: 调用工具 web_search  参数={"query": "Context Caching 适用场景 计费"}
👀 [2] 观察: （示例结果）常见于多轮对话、长文档反复问答、固定系统提示等场景；命中缓存的 token 通常按更低价格计费，并能显著降低首字延迟。
✅ [3] 最终答案: Context Caching（上下文缓存）是 Moonshot AI 提供的一种机制：……它特别适合长系统提示、长文档反复问答、多轮对话等场景。（本段来自离线示例轨迹，非真实搜索结果。）
============================================================
```

**轨迹结构**（来自 demo.json）

`demo.json` 包含三个字段：`question`（问题）、`trace`（轨迹）、`answer`（最终答案）。`trace` 中每一步的 `type` 是 `thought` / `action` / `observation` / `answer` 之一：

| 轮次 | thought（思考） | action（行动） | observation（观察） |
|---|---|---|---|
| 1 | 需要先搜官方说明，确认定义和作用 | `web_search("Moonshot AI Context Caching 是什么")` | 定义：把重复使用的前缀缓存在服务端，降低重复计算与费用 |
| 2 | 已知大致定义，还缺适用场景 | `web_search("Context Caching 适用场景 计费")` | 场景：多轮对话、长文档问答、固定系统提示；缓存 token 更便宜，首字延迟更低 |
| 3 | — | — | **answer**：综合两次观察给出最终答案 |

**观察**
- **为什么要搜第二次？** 第 2 轮的 thought 写明"已知大致定义，但还缺少适用场景"。模型判断信息还不够，所以继续搜。
- **第二次的搜索词是怎么来的？** action 2 是根据 thought 2 决定的；而 thought 2 之所以能说"已知定义"，是因为第 1 轮的 observation **还留在上下文里**。完整链条是：observation 1（查到定义）→ thought 2（定义有了，缺场景）→ action 2（搜适用场景）。
- **答案有依据**：答案里的每句话都能在两次 observation 中找到出处：
  - "缓存在服务端……降低重复计算、减少费用" → 第 1 轮 observation
  - "加快响应"、"适合长系统提示、长文档反复问答、多轮对话" → 第 2 轮 observation（"降低首字延迟"、"常见于多轮对话……"）

**理解：ReAct 轨迹和 1-1 的消息列表是同一个东西**

| ReAct 步骤（1-2） | 对应 1-1 消息列表里的什么 | 1-1 `full.json` 里的例子 |
|---|---|---|
| 💭 thought | assistant 消息的 `reasoning_content` | "The user wants me to calculate…" |
| 🔧 action | assistant 消息的 `tool_calls` | `calculate("(125 + 375) * 8")` |
| 👀 observation | `role: "tool"` 消息的 `content` | `{"result": 4000}` |
| ✅ answer | assistant 消息的 `content`，此时 `finish_reason = "stop"` | "FINAL ANSWER: 4000" |

- 容易混淆的地方：assistant 消息和 tool 消息**都有** `content` 字段。assistant 的 content 是模型**说的话**（最后一轮就是答案），tool 的 content 是工具**返回的结果**（也就是观察）。
- "想 → 做"在协议里是**同一条** assistant 消息的两个字段（`reasoning_content` + `tool_calls`），"看"是**另一条**单独的 tool 消息。
- ReAct 的每一轮都建立在上一轮的观察之上，观察必须留在上下文里，循环才能往前走。这和 1-1 中 `no_history` 组每轮重做第一步，是同一个道理的两面。

---

### 2. 读代码：离线演示是怎么生成的

顺着 `--provider offline-demo` 这个参数值往下追：

| 位置 | 作用 |
|---|---|
| `main.py` 第 151 行 | 定义参数：`--provider` 可选 `kimi` / `offline-demo`，默认 `kimi` |
| `main.py` 第 176 行 | `if args.provider == "offline-demo":` 走离线分支 |
| `main.py` 第 184 行 | 调用 `run_offline_demo(demo_question, ...)` |
| `agent.py` 第 553 行起 | `run_offline_demo` 的定义：`trace = [...]` 是一个**写死的列表** |

**观察**
- thought / action / observation / answer 全是代码里的**固定字符串**，函数里没有任何调用模型或搜索的代码。
- 验证：换个问题运行 `python main.py "今天北京天气怎么样" --provider offline-demo`，第一行打印的"问题"变了，但轨迹和答案**完全不变**，仍然在讲 Context Caching。原因是传入的 `question` 只用在最后的 `return {"question": question, ...}`，`trace` 根本没用到它。

**理解**

| | 离线演示 | 真实联网 |
|---|---|---|
| thought / action | 写死的字符串 | 模型根据问题和上一轮观察生成 |
| observation | 写死的"示例结果" | 搜索服务真实返回的内容 |
| 能说明什么 | 循环**长什么样** | 模型**怎么做决定** |

离线演示是一份"剧本"，ReAct 最关键的"根据看到的东西决定下一步"在剧本里看不到。

> 读代码小技巧：VS Code 里 `⌘+P` 输入 `agent.py:553` 可直接跳到指定行；`⌘+Shift+F` 全局搜索 `def 函数名` 可找到函数定义；装好 Python 扩展并选中 `.venv` 解释器后，按住 ⌘ 点击函数名即可跳转。

---

### 3. 联网运行

指令：
```bash
python main.py "2026年诺贝尔物理学奖获得者是谁？他们因什么成就获奖？" --output live.json
```

运行条件：
- 日期：2026-11-10
- 提供商 / 模型：Moonshot / kimi-k3（`reasoning_effort = max`，`temperature = 1`）
- 搜索：Moonshot Formula 服务端工具 `moonshot/web-search:latest`
- 最大迭代：5 轮（默认）
- 选题理由：2026 年诺贝尔奖 10 月才公布，模型训练数据里大概率没有，必须真的去搜

**轨迹**（来自 live.json）

| 轮次 | 类型 | 内容 |
|---|---|---|
| 1 | 💭 thought | "当前系统日期是 2026-08-07……诺贝尔奖 10 月才公布，可能尚未公布……搜索看看是否有相关信息" |
| 1 | 🔧 action | `web_search("2026 Nobel Prize in Physics announced laureates October 2026")` |
| 1 | 👀 observation | `----MOONSHOT ENCRYPTED BEGIN----……`（加密文本） |
| 2 | 💭 thought | "搜索结果显示 2026 年物理学奖授予 Francis Halzen……"（期间对当前日期有些混乱，还怀疑过"搜索结果会不会是编的"，最终选择相信工具结果） |
| 2 | ✅ answer | 弗朗西斯·哈尔岑（Francis Halzen）一人获奖；2026-10-06 公布；因对 IceCube 中微子天文台的决定性贡献及发现天体物理来源的高能中微子 |

只搜了 **1 次**，第 2 轮就作答。

**程序在一轮工具调用中做的事**（来自 live.json 的 api_turns）
```
GET  .../formulas/moonshot/web-search:latest/tools    ← 获取工具定义，交给模型
chat completion                                       ← 模型返回 tool_calls: web_search(...)
POST .../formulas/moonshot/web-search:latest/fibers   ← 把 tool_call 转交服务端执行，status = succeeded，拿回密文
chat completion                                       ← 把密文作为 tool 消息放回，模型给出答案
```
循环结构和 1-1 完全一样，只是"执行工具"这一步搬到了 Moonshot 服务器上。

**观察**
1. **观察结果是加密的**：tool 消息的内容是 `MOONSHOT ENCRYPTED` 密文，程序只负责原样转交，只有 Moonshot 那边的模型能读。
2. **模型的先验和搜索结果冲突**：thought 1 以为"现在是 8 月，奖还没公布"，但没有直接下结论，而是先去搜；最后选择相信工具结果。
3. **纠正了问题的前提**：问题问的是"他们"，模型回答"由一人获得"。

**验证：答案对不对？有没有依据？**
- 1-1 的 grounding（可依据性）检查，是拿答案去 tool 消息里找出处。这次 tool 消息是密文，**这个办法失效了**。单看 live.json，无法判断答案是出自搜索结果，还是模型碰巧知道。
- 可用的验证办法：

| 办法 | 能证明什么 | 局限 |
|---|---|---|
| ① 查执行状态（fiber `status = succeeded`） | 搜索确实执行了 | 证明不了答案和结果一致 |
| ② 要求模型附上来源链接 | 把检查变成核对链接 | 链接也可能是编的，要点进去看 |
| ③ 去权威来源独立核实 | 最可靠，不依赖模型 | 需要人工，难以自动化 |

- 用办法 ③ 核实（2026-11-10，诺贝尔奖官网及多家媒体）：

| 模型的说法 | 核实结果 |
|---|---|
| 获奖者 Francis Halzen | ✅ 一致 |
| 一人获奖 | ✅ 一致 |
| 2026-10-06 公布 | ✅ 一致 |
| 因 IceCube / 宇宙高能中微子获奖 | ✅ 主题一致（官方获奖理由原文未逐字核对） |

- 来源：[Nobel Prize in Physics 2026 – nobelprize.org](https://nobelprize.org/prizes/physics/2026/summary)、[Press release](https://www.nobelprize.org/prizes/physics/2026/press-release/)、[OPB](https://www.opb.org/article/2026/10/06/francis-halzen-wins-nobel-prize-in-physics-for-work-on-high-energy-neutrinos/)、[SCMP](https://scmp.com/news/world/europe/article/3369925/francis-halzen-wins-2026-nobel-prize-physics)

**理解**

| | 1-1（本地工具） | 1-2（服务端搜索） |
|---|---|---|
| 工具在哪执行 | 本地 Python 程序 | Moonshot 服务器 |
| 程序能读到结果吗 | ✅ 明文 | ❌ 密文 |
| 能自动做 grounding 检查吗 | ✅ 能 | ❌ 不能，只能外部核实 |

**服务端工具省去了自己实现搜索的麻烦，代价是看不见。控制权交出去了，检查能力也跟着交出去了。** 这次答案正确，是靠外部独立核实确认的，而不是从轨迹里看出来的。

---

### 4. 思考题：搜索结果互相矛盾怎么办？

README 的问题：如果搜索结果互相矛盾，循环应该继续搜索、向用户澄清，还是带着不确定性回答？

**我的回答**
- 第一反应：**再搜**。用更精确的条件（年份、官方网站）再找一个来源。很多"矛盾"其实是条件没限定清楚，比如把 2025 年和 2026 年的新闻混在一起。
- 但不能无限搜：Agent 有迭代上限（默认 5 轮）。1-1 里 `no_history` 和 `no_tool_results` 都是一直调工具，最后什么都没交出来。
- 如果到上限仍然矛盾：**把两种说法都列出来，说明来源有冲突、无法确定**。直接挑一个作答，选错了就是一个"看起来很确定"的错误答案，也就是 1-1 中最危险的那类失败；看得见的不确定，比看不见的错误安全。

**更完整的判断：看矛盾出在哪里**

| 矛盾出在哪 | 怎么做 | 例子 |
|---|---|---|
| 问题本身有歧义 | 问用户 | 没说哪一年、哪个奖项；1-1 报告第 2 节"三种货币求平均"也属于这类 |
| 来源之间有冲突 | 摆出冲突，说明不确定 | 两篇报道对同一件事说法不同 |
| 有一个来源明显更权威 | 采信权威来源，并说明理由 | 官网 vs 二手转载 |

---

### 总结

- ReAct 的"想 → 做 → 看"，就是 1-1 消息列表循环的另一种说法：thought = `reasoning_content`，action = `tool_calls`，observation = tool 消息，answer = 最后一条 assistant 消息的 `content`。
- 循环能往前走，靠的是上一轮的观察留在上下文里。
- 离线演示只能展示循环的形状；模型怎么做决定，要联网才看得到。
- 工具放到服务端以后，结果可能对程序不可见，答案的依据只能靠外部独立核实。
