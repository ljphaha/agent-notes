# AI Agent 课程笔记

自学 AI Agent 工程的课程笔记，用 LaTeX（ElegantBook 模板）编写。

课程从一次 LLM 调用开始，逐步搭出能检索、调用工具、管理上下文、接受用户审批的 Agent，再学习用运行轨迹和验证器判断它是否真正完成了任务。

## 学习材料

- **主教材**：李博杰《深入理解 AI Agent：设计原理与工程实践》（[在线版](https://bojieli.github.io/ai-agent-book/) · [配套代码](https://github.com/bojieli/ai-agent-book)）
- **辅助材料**：Stanford CS329Z *Engineering AI Agents*（Fall 2026）的课件与阅读清单（[课程主页](https://cs329z.stanford.edu/)）
- **作业**：CS329Z 原版 [HW1 Building an Agentic Harness](https://github.com/cs329z/assignment1-harness)、[HW2 Building an Evaluation Task](https://github.com/cs329z/assignment2-harness)
- 论文按单元选读，作为补充

## 笔记目录

| 讲 | 主题 | PDF |
|---|---|---|
| 1 | Agent、工作流与 Harness：谁决定下一步、工具调用怎么发生、Harness 五要素、上下文的组成与 ReAct 轨迹 | [ai-agent-note-1.pdf](ai-agent-note-1.pdf) |
| 2 | 固定流水线、BM25 与多跳检索：把一次调用写成规格说明、防御式解析、多次调用的分工、RAG 与 BM25、倒排索引与检索评价、多跳检索 | [ai-agent-note-2.pdf](ai-agent-note-2.pdf) |
| 3 | 工具协议与 Agent 循环 | 待更新 |
| 4 | 文档工具、终端与上下文管理 | 待更新 |
| 5 | 跨会话记忆、用户审批与防注入 | 待更新 |
| 6 | 用模拟用户评测完整 Agent | 待更新 |
| 7 | 运行公开 Benchmark 并读懂轨迹 | 待更新 |
| 8 | 设计评测任务和验证器 | 待更新 |

每讲完成后上传一份 PDF，文件名为 `ai-agent-note-N.pdf`。

## 实验记录

跟着主教材的[配套代码](https://github.com/bojieli/ai-agent-book)动手做的实验，每个实验一个文件夹，内含实验报告（`README.md`）和我自己跑出的结果文件。

| 编号 | 实验 | 核心结论 | 模型 | 报告 |
|---|---|---|---|---|
| 1-1 | 上下文消融：依次拿掉历史、推理、工具定义、工具结果，比较 Agent 行为 | 模型无状态，上下文就是程序每轮重组的消息列表；`completed` ≠ 答对 ≠ 数字有依据，交出看似可信的编造数字是最危险的失败 | deepseek-v4-flash | [experiments/chapter1/1-1](experiments/chapter1/1-1/) |
| 1-2 | Web 搜索 Agent：离线演示读懂 ReAct 轨迹，再用 Moonshot 服务端 `web_search` 真实联网问答 | ReAct 的"想→做→看"就是消息列表循环；服务端工具的观察结果是加密的，程序无法做 grounding 检查，答案只能靠外部独立核实 | kimi-k3 | [experiments/chapter1/1-2](experiments/chapter1/1-2/) |
| 1-3 | 搜索 + 代码执行 | 待更新 | | |
| 1-4 | 图像生成：工作流 vs 原生 | 待更新 | | |

## 目录结构

```
preamble.tex          各讲共用的版式设置（字体、配色、代码样式）
ai-agent-note-N.tex   第 N 讲的主文件：引入 preamble 和对应的一章，单独编译出一份 PDF
chapters/             各章正文，每讲一个 .tex 文件
elegantbook.cls       ElegantBook v4.7 模板类文件
LATEX-CHEATSHEET.md   本模板的 LaTeX 语法速查
ai-agent-note-N.pdf   每讲编译好的笔记
experiments/          动手实验：按 chapterN/编号 分文件夹，每个含报告 README.md 和 results/
```

## 自己编译

需要 XeLaTeX（TeX Live 或 MiKTeX，带 ctex 中文支持）。在仓库根目录运行：

```sh
xelatex -no-shell-escape -interaction=nonstopmode -halt-on-error ai-agent-note-2.tex
```

把文件名里的数字换成要编译的那一讲。每讲单独编译，生成同名的 PDF。新增章节、引用或目录后，再运行一次以更新页码和链接。模板里各种环境和命令的写法见 [LATEX-CHEATSHEET.md](LATEX-CHEATSHEET.md)。

## 致谢与许可

版式来自 [ElegantBook v4.7](https://github.com/ElegantLaTeX/ElegantBook/releases/tag/v4.7)，模板的许可证见 [License](License)。笔记内容是个人学习总结，书和课程的原始内容版权归各自作者所有。
