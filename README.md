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
| 2 | 固定流水线、BM25 与多跳检索 | 待更新 |
| 3 | 工具协议与 Agent 循环 | 待更新 |
| 4 | 文档工具、终端与上下文管理 | 待更新 |
| 5 | 跨会话记忆、用户审批与防注入 | 待更新 |
| 6 | 用模拟用户评测完整 Agent | 待更新 |
| 7 | 运行公开 Benchmark 并读懂轨迹 | 待更新 |
| 8 | 设计评测任务和验证器 | 待更新 |

每讲完成后上传一份 PDF，文件名为 `ai-agent-note-N.pdf`。

## 目录结构

```
main.tex              主文件：版式设置，并用 \input 引入各章
chapters/             各章正文，每讲一个 .tex 文件
elegantbook.cls       ElegantBook v4.7 模板类文件
LATEX-CHEATSHEET.md   本模板的 LaTeX 语法速查
ai-agent-note-N.pdf   每讲编译好的笔记
```

## 自己编译

需要 XeLaTeX（TeX Live 或 MiKTeX，带 ctex 中文支持）。在仓库根目录运行：

```sh
xelatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex
```

新增章节、引用或目录后，再运行一次以更新页码和链接。模板里各种环境和命令的写法见 [LATEX-CHEATSHEET.md](LATEX-CHEATSHEET.md)。

## 致谢与许可

版式来自 [ElegantBook v4.7](https://github.com/ElegantLaTeX/ElegantBook/releases/tag/v4.7)，模板的许可证见 [License](License)。笔记内容是个人学习总结，书和课程的原始内容版权归各自作者所有。
