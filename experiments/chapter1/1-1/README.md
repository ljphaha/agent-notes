# 第一章实验
## 1-1 上下文感知Agent

> 实验代码来自 [bojieli/ai-agent-book](https://github.com/bojieli/ai-agent-book) 的 `chapter1/context/`（Apache 2.0），命令均在该目录下运行。
> 本文件夹只保存我的实验报告和运行结果：
>
> | 文件 | 对应报告章节 |
> |---|---|
> | `results/full.json` | 1. 小规模观察 |
> | `results/sample.json` | 2. 运行样例任务 |
> | `results/ablation_results.json`、`ablation_study_report.md`、`ablation_study_results.png` | 3. 运行消融实验 |
> | `results/formal_run_20261109/evidence.json` | 4. 正式实验 |

### 1.小规模观察

#### 1.1 full（完整上下文）

指令：
``` bash
python main.py --mode single --provider deepseek --context-mode full --task "请调用计算器计算 (125 + 375) * 8，并给出结果。" --output full.json
```
> 注：README 原文示例用 `--provider dashscope`（百炼），这里实际用的是 DeepSeek，其余参数相同。

输出
```
2026-11-08 19:15:26,944 - INFO - Terminal text response (no tool calls); stopping after iteration 2

============================================================
TASK EXECUTION RESULT
============================================================
Context Mode: full
Terminal response completed: True
Iterations: 2
Tool Calls: 1

Final Answer:
----------------------------------------
4000
2026-11-08 19:15:26,946 - INFO - Detailed results saved to full.json
```

运行条件：
- 日期：2026-11-08
- 提供商 / 模型：deepseek / deepseek-v4-flash
- 上下文模式：full

**轨迹**（来自 full.json 的 api_turns）

| 轮次 | 发给模型的消息 | 模型返回 | finish_reason |
|---|---|---|---|
| 1 | system; user（另附 `tools`：4 个工具定义） | `content` 为空；`tool_calls` = `calculate("(125 + 375) * 8")`；`reasoning_content` = "The user wants me to calculate … using the calculator tool." | `tool_calls` |
| 2 | system; user; assistant（上一轮的 tool_calls，原样放回）; tool（`{"result": 4000}`） | `content` = "… FINAL ANSWER: 4000"；没有 tool_calls | `stop` |

**观察**
- 模型有没有调用计算器？**有。** 第 1 轮模型没有直接作答，而是返回了一个 `calculate` 调用请求。模型本身不执行计算，执行的是本地程序。
- 计算器的结果（4000）有没有进入下一轮消息？**有。** 它在第 2 轮请求中 `role: "tool"` 的那条消息里，模型读到这条消息后给出了 `FINAL ANSWER: 4000`。
- 第 2 轮的 prompt_tokens（854）比第 1 轮（751）多，因为整个消息列表被重新发送了一遍。

**理解**
- **模型为什么能"记得"上一轮？** 模型本身是无状态的，每次请求都从零开始。是程序（`agent.py`）每一轮把模型上一轮的回复（assistant 消息）和工具执行结果（tool 消息）追加到 messages 列表里，再把**整个列表**重新发给模型。所以，上下文 = 程序每轮组装并发出的 messages 列表（加上 tools 定义）。
- **四种消融分别动的是哪一部分？** 消融就是程序在组装这个列表时，故意少放某一类东西：

| 消融模式 | 少放了什么 |
|---|---|
| `no_history` | 之前的 assistant / tool 消息全部不放，只发 system + user |
| `no_reasoning` | assistant 消息里的 `reasoning_content` 被删掉 |
| `no_tool_calls` | 不发 `tools` 字段，模型不知道有工具可用 |
| `no_tool_results` | tool 消息还在，但 `content` 被清空 |

> 注：README 小规模观察的第 2 步（同一道计算题改用 `no_tool_results` 重跑）这里没有单独做，放到第 6 步消融实验中一并观察。

---

### 2. 运行样例任务（快速开始 · 第 5 步）

指令：
```bash
python main.py --mode single --provider deepseek --output sample.json
# 交互选择：题号 1
```

运行条件：
- 日期：2026-11-08
- 提供商 / 模型：deepseek / deepseek-v4-flash
- 上下文模式：full（默认）
- 任务：Convert $1000 USD to EUR, GBP, and JPY. Then calculate the average value across all three converted currencies.

结果概览：迭代 4 轮，completed = True，工具调用 7 次（6 次 `convert_currency` + 1 次 `calculate`）

**工具调用记录**（来自 sample.json 的 tool_calls）

| # | 工具 | 参数 | 汇率 | 结果 |
|---|---|---|---|---|
| 1 | convert_currency | 1000 USD → EUR | 0.92 | 920 |
| 2 | convert_currency | 1000 USD → GBP | 0.79 | 790 |
| 3 | convert_currency | 1000 USD → JPY | 149.5 | 149,500 |
| 4 | convert_currency | 920 EUR → USD | 1.087 | 1000 |
| 5 | convert_currency | 790 GBP → USD | 1.2658 | 1000 |
| 6 | convert_currency | 149,500 JPY → USD | 0.0067 | 1000 |
| 7 | calculate | (1000 + 1000 + 1000) / 3 | — | 1000 |

最终答案：$1000 = €920 / £790 / ¥149,500；平均值 $1,000.00

**轨迹：每轮发给模型的消息条数**

| 轮次 | 消息条数 | 本轮发出的工具调用数 | finish_reason |
|---|---|---|---|
| 1 | 2（system + user） | 3 | tool_calls |
| 2 | 6（+1 assistant +3 tool） | 3 | tool_calls |
| 3 | 10（+1 assistant +3 tool） | 1 | tool_calls |
| 4 | 12（+1 assistant +1 tool） | 0 | stop |

规律：一轮工具调用，下一轮的列表就多出 **1 条 assistant + N 条 tool**（N = 这一轮调用的工具数）。
- 同一轮的多个工具调用都装在**同一条** assistant 消息里，但每个结果**各自是一条** tool 消息。
- 每条 tool 消息带有 `tool_call_id`，和 assistant 消息里的某个 tool_call 一一对应，所以 assistant 消息必须排在这几条 tool 消息前面。

**观察**
- **答案有依据**：最终答案里的 €920、£790、¥149,500、$1,000 都能在 `role: "tool"` 消息的 `content` 里找到出处，没有一个数字是模型自己编的。
- **模型把钱又换回了美元**：€920、£790、¥149,500 单位不同，不能直接相加求平均，必须统一换算成同一种货币。模型这样做是合理的。
- 结论：**答案有依据，不等于答案有用。**

---

### 3. 运行消融实验（快速开始 · 第 6 步）

指令：
```bash
python main.py --mode ablation --provider deepseek
```

任务：默认的跨国预算题（`main.py` 第 130 行），5 个地区、5 种货币换算成美元，计算总额、平均值、各地区占比，以及削减 8% 后各地区的新支出。

运行条件：
- 日期：2026-11-08
- 提供商 / 模型：deepseek / deepseek-v4-flash
- 迭代上限：10 轮
- 输出文件：`ablation_results.json`（汇总，最终回答只保留前约 300 字，没有逐轮的 api_turns）、`ablation_study_report.md`、`ablation_study_results.png`

**结果**

| 组 | 迭代 | 工具调用 | completed | grounding_verdict | observation_count | 最终回答 |
|---|---:|---:|---|---|---:|---|
| `full` | 8 | 10 | ✅ | not_assessable | 79 | 说明 PDF 中没有金额数据，然后用工具完成了换算 |
| `no_history` | 10（触顶） | 53 | ❌ | no_answer | 0 | 无 |
| `no_reasoning` | 4 | 6 | ✅ | not_assessable | 67 | 正常完成了换算和计算 |
| `no_tool_calls` | 1 | 0 | ✅ | no_quantities | 0 | 一段用纯文本模仿出来的工具调用（`invoke name="bash"`） |
| `no_tool_results` | 5 | 9 | ✅ | **ungrounded** | 0 | 总额 **$11,984,000**，附带汇率 GBP 1.27 / JPY 0.0067 / EUR 1.08 / SGD 0.745 |

> `not_assessable`：这道默认题没有标准答案，框架只能检查数字有没有出处，判断不了对错。`full` 和 `no_reasoning` 都没有发现编造的数字。

**观察与分析**

1. **`no_history`：重复做第一轮的动作，直到触顶**
   - 不放历史时，每一轮发给模型的消息都只有 system + user，和第 1 轮一模一样。对模型来说，每一轮都像第一次见到这道题。
   - 53 次调用 ÷ 10 轮 ≈ 每轮 5 次，正好对应题目里的 5 个地区。也就是说，它每轮都把 5 个地区重新换一遍汇，结果随即被丢掉，下一轮再从头开始，所以永远走不到"汇总并作答"那一步。
   - 失败**看得见**：没有交卷，一眼就能发现。

2. **`no_tool_results`：交卷了，但数字是编的（最危险）**
   - 调用了 9 次工具，但收到的工具结果是 0 条（`observation_count = 0`）；题目原文里也没有给汇率。
   - 回答里的汇率只剩一个来源：**模型凭训练时的记忆自己补上的**。它们接近真实世界的汇率，但和工具汇率表不一致：

     | 货币 | 工具汇率表（sample.json） | 回答里写的 |
     |---|---|---|
     | GBP → USD | 1.2658 | 1.27 |
     | EUR → USD | 1.087 | 1.08 |
     | JPY → USD | 0.0067 | 0.0067（碰巧一致） |

   - grounding 检查发现了 14 个找不到出处的营收量级数字，判为 `ungrounded`。
   - 失败**看不见**：格式工整、有过程、有汇率，和正确答案长得一模一样，程序也报告 `completed: true`。只看总额的人根本发现不了。

3. **`no_tool_calls`：没有工具，就用文字假装调用**
   - 请求里没有任何工具定义，模型却在回答里用纯文本写出了一段工具调用的格式，调用的 `bash` 在这个实验里根本不存在。
   - 程序把这段文字当成了最终回答，所以这一组也算 `completed`。这说明 `completed` 什么都证明不了。

4. **`no_reasoning`：这次没有看出退化**
   - 4 轮、6 次调用就完成了，比 `full` 还少。和 README 及实验记录一致："去掉推理会退化"这个说法，在实测里并不能稳定复现。
   - 只跑了一次，不能据此说"推理没用"，只能说"这一次没有观察到差异"。

**结论**
- **`completed`（交卷了）≠ 答对了 ≠ 数字有依据。** 三者要分开检查。
- **看不见的失败比看得见的失败更危险**：`no_history` 没交卷，人能发现；`no_tool_results` 交出了看起来可信的错误答案，只有逐个检查数字出处才能发现。
- 每组只跑了一次，模型行为有随机性，以上都是**这一次的观察**，不是定律。

---

### 4. 正式实验（run_experiment_1_1.py）

指令：
```bash
python run_experiment_1_1.py --provider deepseek
```

运行条件：
- 日期：2026-11-09
- 提供商 / 模型：deepseek / deepseek-v4-flash
- 迭代上限：5 轮（脚本默认）
- 标准配置：`--task guarded`（带"不要自己估计汇率"的约束）、`--hidden-result empty`（静默隐藏工具结果）、五组齐全，即 `canonical_run = true`
- 验收：`experiment_execution_accepted = true`
- 输出：`validation/real_20261109T165058Z/evidence.json`（每一轮的请求和响应都保存了下来）
- 版本管理：这次运行覆盖了 `validation/latest.json`，已用 `git restore` 恢复成仓库原版；本次结果单独提交为 `db20672`

任务（标准答案：总额 **9,602,895.73**，平均 **2,400,723.93**）：
```
Q1: 2.5 million USD / Q2: 2.1 million EUR / Q3: 1.8 million GBP / Q4: 380 million JPY
换算成美元，计算全年总额和季度平均值，保留两位小数。
Do not estimate exchange rates yourself; use the tool observations.
```

**预测（跑之前）**
- `no_tool_calls` → `unsupported_numbers` ✅
- `no_tool_results` → `no_terminal_response` ✅

**结果**

| 组 | 迭代 | 工具调用 | observation_count | 最终回答 | outcome |
|---|---:|---:|---:|---|---|
| `full` | 3 | 5 | 20 | 总额 9,602,895.73；平均 2,400,723.93 | `correct` |
| `no_history` | 5（触顶） | 15（重复 9 次） | 0 | 无 | `no_terminal_response` |
| `no_reasoning` | 3 | 4 | 20 | 总额 9.60 million；平均 2.40 million | `incorrect` |
| `no_tool_calls` | 1 | 0 | 0 | 总额 $9.60 million；平均 $2.40 million | `unsupported_numbers` |
| `no_tool_results` | 5（触顶） | 7 | 0 | 无 | `no_terminal_response` |

**观察与分析**

1. **`no_history`：每轮重做第一轮**
   - 15 次调用 ÷ 5 轮 = 每轮 3 次，正好对应 Q2、Q3、Q4 三个非美元季度的换汇。
   - 和第 6 步的现象一致：每一轮看到的消息都和第 1 轮一样，所以每轮都从头开始换汇，永远走不到汇总那一步。

2. **`no_tool_results`：盲目执行，然后试探工具**
   - 前 3 次是正常的换汇调用；收不到结果以后，开始用奇怪的参数**试探**工具：`2.1 EUR→USD`、`1 USD→USD`、`calculate("2.5 + 2.1")`，最后甚至调用了 `code_interpreter("print('hello')")`。
   - 看起来像是在排查"工具为什么什么都不返回"，但它始终没有说出"我没有拿到结果"，一直试到 5 轮上限。这就是 README 所说的"盲目执行"。
   - 和第 6 步不同（那次它编出了 $11,984,000）：这次带了"不要自己估计汇率"的约束，迭代上限也更低，它没有交卷。

3. **`no_tool_calls`：题目明确禁止，模型还是自己估计了汇率**
   - 请求里没有工具定义，模型无法换汇，却直接给出了 $9.60 million / $2.40 million。
   - 这个数和标准答案只差约 0.03%，**很接近正确，但仍然判为 `unsupported_numbers`**：它一条工具结果都没收到，数字不可能是"读到"的。**可依据性和正确性是两条独立的轴。**
   - 对照 README 中作者用 Kimi K3 的运行（2026-08-25）：同样的任务、同样的约束，Kimi 这一组没有报出任何数字，而是说明无法换汇。**同一句提示词约束，不同模型的反应不同。** 提示词只能降低编造的概率，不能消除。

4. **`no_reasoning`：答案"不对"，但错在汇报格式**
   - 收到了 20 条工具结果，数字有出处；9.60 million 与 9,602,895.73 只差 0.03%。
   - 错在对"保留两位小数"的理解：它理解成了"以百万为单位保留两位"，丢掉了后面的 2,895.73 美元。评分脚本要找的是 `9602895.73`，于是判为 `incorrect`。
   - 脚本据此把 `without_reasoning_degraded` 标为 `true`，但它在 `claim_qualifications` 里也承认，这只是"根据答案不对推断出来的"。这次的错误更像是**理解偏差**，而不是推理能力退化。
   - 实验删掉的是**之前几轮**留下的推理，模型每一轮仍然会重新思考；而每一步该做什么已经由上一轮的工具结果决定。推理负责"为什么"，工具结果负责"拿到了什么"，后者还在时，前者丢掉往往影响不大。

**与仓库里已有的运行对比**

仓库原版的 `validation/latest.json` 也是用 deepseek-v4-flash 跑的（2026-09-01）。两次运行五组的 outcome **完全一致**：

| 组 | 仓库原版（2026-09-01） | 本次（2026-11-09） |
|---|---|---|
| `full` | `correct` | `correct` |
| `no_history` | `no_terminal_response` | `no_terminal_response` |
| `no_reasoning` | `incorrect`（9,600,000.00 / 9.60 million） | `incorrect`（9.60 million） |
| `no_tool_calls` | `unsupported_numbers`（9.60 million） | `unsupported_numbers`（9.60 million） |
| `no_tool_results` | `no_terminal_response` | `no_terminal_response` |

- `no_reasoning` 两次都写成了 9.60 million，而 `full` 两次都给出了精确值。这说明对 deepseek-v4-flash 来说，**去掉保留的推理以后更容易忽略格式要求**，这个倾向可能不完全是随机的。
- 但实验记录（EXPERIMENT_LEDGER）里也提到，有读者用 deepseek-v4-flash 复现时，`no_reasoning` 组答对了。所以目前是 2 次错、1 次对，样本仍然太少，只能算一个值得继续验证的**倾向**，不能下结论。

**结论**
- 正式实验有标准答案，可以用 `outcome` 把五种结局区分开，比只看 `completed` 清楚得多。
- **可依据性 ≠ 正确性**：`no_tool_calls` 的数字接近正确，但没有依据；`no_reasoning` 的数字有依据，但格式不对。
- **程序给出的结论标签（`true`/`false`），要和它背后的证据分开看。** 单次运行、单个标签说明不了因果；要讨论稳定的差异，需要多次重复运行。



