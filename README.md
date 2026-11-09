# AI Agent 课程笔记

打开 main.tex 编译，在 chapters/01-agent-basics.tex 里写正文。每增加一章，就在 chapters/ 新建 .tex 文件，并在 main.tex 加一行 \input{chapters/文件名}。需要目录时，取消 \tableofcontents 前的注释。

编译器选 XeLaTeX。在本目录运行以下命令。新增章节、引用或目录后，再运行一次以更新页码和链接。

~~~powershell
xelatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex
~~~

版式来自 [ElegantBook v4.7](https://github.com/ElegantLaTeX/ElegantBook/releases/tag/v4.7)。类文件取自该版本的 0ff65a8 提交，许可证见同目录的 License。

## LaTeX 语法速查

这些例子可以放进章节的 `.tex` 文件。正文直接写，空一行分段。`%` 后面是注释，选中带 `%` 的模板块，按 `Ctrl+/` 可切换注释。

| 想写什么 | 写法 |
|---|---|
| 章、小节、子小节 | `\chapter{章标题}`、`\section{小节标题}`、`\subsection{子小节标题}` |
| 加粗、强调、行内代码 | `\textbf{重点}`、`\emph{强调}`、`\texttt{tool\_call}` |
| 行内公式 | `\(x_i^2 + \frac{1}{n}\)` |
| 单独一行公式 | `\[\sum_{i=1}^{n} x_i\]` |
| 超链接 | `\href{https://example.com}{链接文字}` |
| 在正文显示特殊符号 | `\%`、`\_`、`\&`、`\#`、`\$` |

**列表**。无序列表用 `itemize`，编号列表用 `enumerate`。

~~~latex
\begin{itemize}
  \item 第一项
  \item 第二项
\end{itemize}
~~~

**定义框**。第二对花括号是标签，每个框用不同的标签。

~~~latex
\begin{definition}{术语}{term-1}
  在这里写定义。
\end{definition}
~~~

**举例**。用 `example` 环境，标题放在方括号里。省略方括号时只显示「例题」和自动编号。

~~~latex
\begin{example}[固定工作流]
程序按预设顺序换汇、求和，再让模型生成报告。
\end{example}
~~~

**Python 代码块**。块里的下划线和百分号可以直接写。

~~~latex
\begin{lstlisting}[style=agentpython]
tool_call = "search"
print(tool_call)
\end{lstlisting}
~~~

**实验记录**。`\item[...]` 中的文字是每项前面的标签。

~~~latex
\begin{description}
  \item[设置] 写输入和对照条件。
  \item[观察] 写实际输出。
  \item[解释] 写你如何理解结果。
\end{description}
~~~

### 流程、图表和引用

**流程箭头**。短流程用 `\rightarrow`，中文步骤包在 `\text{}` 里。

~~~latex
\[
  \text{用户请求} \rightarrow \text{模型选动作}
  \rightarrow \text{工具执行} \rightarrow \text{结果回传}
\]
~~~

**多行公式**。`align*` 里的 `&` 标记对齐位置，`\\` 换行。需要公式编号时用 `align`。

~~~latex
\begin{align*}
  \text{全年总额} &= q_1 + q_2 + q_3 + q_4,\\
  \text{季度均值} &= \frac{q_1 + q_2 + q_3 + q_4}{4}.
\end{align*}
~~~

**对比表格**。`{ll}` 表示两列都左对齐。列之间用 `&`，行末用 `\\`。

~~~latex
\begin{center}
\begin{tabular}{ll}
  \toprule
  写法 & 谁选择下一步 \\
  \midrule
  固定工作流 & 预先写好的程序逻辑 \\
  Agent & 根据当前上下文作决定的模型 \\
  \bottomrule
\end{tabular}
\end{center}
~~~

**插图**。把 `example-image` 换成自己的文件路径，例如 `figures/agent-loop.png`。图片路径从 `main.tex` 所在目录算起。

~~~latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.7\linewidth]{example-image}
  \caption{Agent 工具调用流程}
  \label{fig:agent-loop}
\end{figure}

如图~\ref{fig:agent-loop} 所示，工具结果会进入下一轮上下文。
~~~

**引用小节**。把 `\label` 放在小节标题后面。新增或改动引用后，编译两遍可更新编号。

~~~latex
\section{上下文}
\label{sec:context}

回顾第~\ref{sec:context}~节里的消息来源。
~~~

**行内代码与脚注**。正文中可以用 `\verb|tool_call_id|` 原样显示下划线。脚注写成 `术语\footnote{这里写补充说明。}`。

**嵌套列表**。把第二层列表放在对应的 `\item` 里面。

~~~latex
\begin{itemize}
  \item 工具调用
    \begin{itemize}
      \item 请求记录工具名称与参数。
      \item 结果记录工具实际返回的内容。
    \end{itemize}
  \item 最终回答
\end{itemize}
~~~

## 模板自带的全部环境和命令

下面的内容来自 `elegantbook.cls` 源码，按当前 `main.tex` 的设置（`mode=fancy`、`lang=cn`）写。改成 `mode=simple` 后，第一类彩色框会变成普通段落，写法也不同。

模板里的环境分三类：

| 类型 | 环境 | 样子 |
|---|---|---|
| 彩色框，自动编号 | `definition`、`theorem`、`lemma`、`corollary`、`axiom`、`postulate`、`proposition`，以及用 `\elegantnewtheorem` 自建的框 | 带标题条的彩色框，可以跨页 |
| 彩色标题段落 | `example`、`exercise`、`problem`、`note`、`remark`、`proof`、`solution`、`assumption`、`conclusion`、`property`、`custom` | 没有框，只有一个彩色粗体开头 |
| 章级结构 | `introduction`、`problemset`、`change` | 章首提要、章末习题、版本记录 |

### 一、彩色框

#### 七种内置框

| 环境 | 显示名 | 颜色 | 角标 | 引用前缀 |
|---|---|---|---|---|
| `definition` | 定义 | `main`（绿） | ♣ | `def:` |
| `theorem` | 定理 | `second`（橙） | ♥ | `thm:` |
| `lemma` | 引理 | `second` | ♥ | `lem:` |
| `corollary` | 推论 | `second` | ♥ | `cor:` |
| `axiom` | 公理 | `second` | ♥ | `axi:` |
| `postulate` | 公设 | `second` | ♥ | `pos:` |
| `proposition` | 命题 | `third`（浅蓝） | ♠ | `pro:` |

显示名是固定的。想要“实验”“要点”这类名字，用后面的 `\elegantnewtheorem` 自己建。

#### 四种写法

以 `definition` 为例，其他六种用法相同。

~~~latex
% 写法 1：标题 + 标签（最常用）。标签自动加前缀，引用时写 def:workflow
\begin{definition}{工作流}{workflow}
  控制流由代码写死，LLM 只在节点内部被调用。
\end{definition}

% 写法 2：标题放在方括号里，不需要引用时可以不写标签
\begin{definition}[Agent]
  控制流由 LLM 在运行时决定。
\end{definition}

% 写法 3：标题后紧跟 \label，标签原样使用，不加前缀
\begin{definition}{Harness}\label{harness}
  模型之外的运行与治理层。
\end{definition}

% 写法 4：带星号，不编号，也不能引用
\begin{definition*}{上下文}
  每次调用模型时送进去的全部消息。
\end{definition*}
~~~

- **显示效果**：标题条写成“定义 1.1 (工作流)”。编号格式是“章号.序号”，每种框各自计数，每章从 1 重新开始。
- **不要标题**：写成 `\begin{definition}{}{workflow}`，标题条只显示“定义 1.1”。
- **引用**：`见定义~\ref{def:workflow}` 显示“见定义 1.1”，点击可以跳转。写法 3 用 `\ref{harness}`。
- **框里的文字**默认是楷体，和正文区分开。
- **长内容**会自动跨页断开。

#### 自定义框：`\elegantnewtheorem`

**这条只能写在 `main.tex` 里**，放在 `\documentclass` 之后、`\begin{document}` 之前。

~~~latex
% 格式：\elegantnewtheorem{环境名}{显示名}{样式}{引用前缀}
\elegantnewtheorem{experiment}{实验}{prostyle}{exp}
\elegantnewtheorem{insight}{要点}{thmstyle}{ins}
\elegantnewtheorem{pitfall}{误区}{defstyle}{pit}
~~~

三种样式对应三种配色：

| 样式 | 颜色 | 角标 | 和谁一样 |
|---|---|---|---|
| `defstyle` | `main`（绿） | ♣ | 定义 |
| `thmstyle` | `second`（橙） | ♥ | 定理 |
| `prostyle` | `third`（浅蓝） | ♠ | 命题 |

建好之后，用法和内置框完全一样，也有带星号的不编号版本：

~~~latex
\begin{experiment}{1-1 上下文消融}{ctx-ablation}
  \begin{description}
    \item[设置] 去掉工具执行结果，其余保持不变。
    \item[观察] Agent 反复重试，直到用完迭代次数。
    \item[解释] 看不到执行结果，模型无法判断上一步是否成功。
  \end{description}
\end{experiment}

如实验~\ref{exp:ctx-ablation} 所示……

\begin{insight*}{一句话}
  判断工作流还是 Agent，只看控制流在谁手里。
\end{insight*}
~~~

- **想让两种框共用一个编号序列**：比如让“要点”和“定理”连着编号，在末尾加上要共用的环境名：`\elegantnewtheorem{insight}{要点}{thmstyle}{ins}[theorem]`。
- **想让所有框共用一个序列**：在 `\documentclass[...]` 的选项里加 `usesamecnt`。

### 二、彩色标题段落

这一类没有框，只在段首放一个彩色粗体标题，适合放在正文中间，不打断阅读。

#### 带编号的：`example`、`exercise`、`problem`

方括号里的内容原样接在编号后面，所以建议自己加括号：

~~~latex
\begin{example}[（订机票工作流）]\label{ex:flight}
  核实身份 → 搜索航班 → 付款 → 确认，顺序由代码写死。
\end{example}

\begin{exercise}[（判断类型）]
  路由器先调一次 LLM 分类，再走固定流程，算工作流还是 Agent？
\end{exercise}

\begin{problem}[（为什么需要停止条件）]
  如果 Agent 没有最大迭代次数，会发生什么？
\end{problem}

回看例题~\ref{ex:flight}……
~~~

| 环境 | 显示 | 特点 |
|---|---|---|
| `example` | 例题 1.1 | 绿色标题，每章重新编号 |
| `exercise` | 练习 1.1 | 绿色标题，左边距有一个红色铅笔图标 |
| `problem` | 问题 1.1 | 绿色标题 |

三者各自计数，`\label` 写在 `\begin{...}[...]` 后面就能引用。

#### 不带编号的

~~~latex
\begin{note}
  “调用了 LLM”不等于“是 Agent”。
\end{note}

\begin{remark}
  书里把“Model + Harness”当作观察视角，不是全书骨架。
\end{remark}

\begin{custom}{误区}
  Agent 一定比工作流高级。
\end{custom}

\begin{custom}{出处}
  教材第 1 章「编排模式」；CS329Z L01。
\end{custom}
~~~

| 环境 | 标题文字 | 颜色 | 正文字体 | 适合记什么 |
|---|---|---|---|---|
| `note` | 笔记 | `second`（橙），左边距有一个“危险弯道”警示图标 | 楷体 | 需要特别提醒的坑 |
| `remark` | 注 | `second` | 正文字体 | 补充说明 |
| `proof` | 证明 | `second` | 仿宋 | 推导过程 |
| `solution` | 解 | `main`（绿） | 楷体 | 练习的答案 |
| `assumption` | 假设 | `third`（浅蓝） | 楷体 | 前提条件 |
| `conclusion` | 结论 | `third` | 楷体 | 小结 |
| `property` | 性质 | `third` | 楷体 | 特点 |
| `custom{标题}` | 任意标题 | `third` | 楷体 | 误区、出处、对比、TODO 等 |

`custom` 最灵活，花括号里写什么就显示什么。

#### 一键隐藏答案

在 `\documentclass[...]` 的选项里加 `noanswer`，全书的 `solution` 和 `proof` 都会被隐藏，适合导出一份只有题目的版本来自测。去掉这个选项就恢复显示。

### 三、章级结构

#### 章首“内容提要”框：`introduction`

紧跟在 `\chapter{...}` 后面。框里的条目自动排成两栏，用 `\item`，不用再写 `itemize`。

~~~latex
\chapter{Agent、工作流和 Harness}

\begin{introduction}
  \item 工作流与 Agent
  \item 工具调用的四步
  \item 消息的四种角色
  \item Harness 五要素
\end{introduction}

% 自定义框标题
\begin{introduction}[本章要回答的问题]
  \item 谁决定下一步
  \item 结果怎么回到上下文
\end{introduction}
~~~

#### 章末习题：`problemset`

放在章节最后。会生成一个居中的花饰标题“第一章 练习”，并在目录里加一条。里面直接写 `\item`，自动编号。

~~~latex
\begin{problemset}
  \item 路由器模式算工作流还是 Agent？说明理由。
  \item 去掉工具执行结果后，Agent 会出现什么行为？
\end{problemset}

% 自定义标题
\begin{problemset}[第一章 思考题]
  \item ……
\end{problemset}
~~~

#### 版本记录：`\datechange` 和 `change`

用来记录笔记什么时候改过什么。

~~~latex
\datechange{2026-11-07}{完成 U1 第 1 节}
\begin{change}
  \item 新增工作流与 Agent 的对比表
  \item 修正 Harness 五要素的顺序
\end{change}
~~~

`change` 里的条目用圈号 ①②③ 编号。在 `main.tex` 的 `\begin{document}` 之后写 `\listofchanges`，会生成一页“版本更新历史”，汇总所有 `\datechange`。

### 四、小命令

| 想写什么 | 写法 | 效果 |
|---|---|---|
| 圈号 | `\circled{1}` | ① 样式，括号里可以是任意短文字 |
| 楷体提问段 | `\question{控制流由谁决定？}` | 单独成段，楷体，后面自动换行 |
| 引用图、表 | `\figref{fig:agent-loop}`、`\tabref{tab:compare}` | 显示“**图** 1.1”“**表** 1.1”，需要先给图表加 `\label` |
| 美元符号 | `\dollar` | \$ |
| 对勾、叉号 | `\ding{51}`、`\ding{55}` | ✓、✗ |
| 指示手 | `\HandRight` | 👉 样式的图标 |
| 中文字体 | `{\kaishu 楷体}`、`{\heiti 黑体}`、`{\songti 宋体}`、`{\fangsong 仿宋}` | 只改花括号里的字体 |
| 粗体向量 | `\(\bm{x}\)` | 数学模式下加粗 |
| 花体字母 | `\(\mathscr{L}\)` | 花体 L |

### 五、配色

模板定义了五个颜色名，可以用在任何地方：

| 颜色名 | 当前 `color=blue` 下 | 模板用在哪 |
|---|---|---|
| `structurecolor` | 蓝 | 标题、页眉、列表符号；`main.tex` 也把超链接设成了这个颜色 |
| `main` | 绿 | 定义框、例题、练习 |
| `second` | 橙 | 定理框、笔记、注 |
| `third` | 浅蓝 | 命题框、假设、结论、`custom` |
| `winered` | 暗红 | 写了 `\tableofcontents` 后，目录之后的超链接会变成这个颜色 |

~~~latex
\textcolor{second}{这句话是橙色}
{\color{main} 这一段都是绿色}
\colorbox{structurecolor!10}{浅蓝底色}      % !10 表示 10% 浓度
~~~

想换整套配色，把 `main.tex` 里的 `color=blue` 改成 `green`、`cyan`、`gray` 或 `black`。

### 六、列表

模板已经给列表改了样式：`itemize` 的前缀是彩色小球，`enumerate` 逐层编号为 `1.`、`(a).`、`I.`、`A.`。另外加载了 `enumitem`，可以在方括号里调格式：

~~~latex
\begin{enumerate}[label=(\roman*)]    % (i) (ii) (iii)
  \item 第一项
\end{enumerate}

\begin{enumerate}[start=3]            % 从 3 开始
  \item 接着上一个列表
\end{enumerate}

\begin{itemize}[noitemsep]            % 去掉条目之间的空隙
  \item 紧凑一点
\end{itemize}

% 行内列表：条目排在同一行
\begin{enumerate*}[label=(\alph*)]
  \item 声明工具 \item 模型决定调用 \item 结果追加 \item 模型回复
\end{enumerate*}
~~~

`label` 里可以用的编号：`\arabic*`（1）、`\alph*`（a）、`\Alph*`（A）、`\roman*`（i）、`\Roman*`（I）。

### 七、自由彩色框：`tcolorbox`

模板加载了完整的 `tcolorbox`。内置框不够用时，可以直接写：

~~~latex
\begin{tcolorbox}[colback=second!5, colframe=second, title=Harness 五要素]
  Context、Tools、Constrain、Verify、Correct
\end{tcolorbox}

% 左右分栏：\tcblower 把框分成两半
\begin{tcolorbox}[colback=main!5, colframe=main, sidebyside, title=工作流 vs Agent]
  代码决定下一步
  \tcblower
  模型决定下一步
\end{tcolorbox}

% 上下分栏：去掉 sidebyside
\begin{tcolorbox}[colback=third!5, colframe=third, title=问与答]
  控制流由谁决定？
  \tcblower
  工作流由代码决定，Agent 由模型决定。
\end{tcolorbox}

% 很长、需要跨页的框
\begin{tcolorbox}[breakable, colback=gray!5, colframe=gray]
  ……
\end{tcolorbox}
~~~

常用选项：`colback`（背景色）、`colframe`（边框色）、`title`（标题）、`fonttitle=\bfseries`（标题加粗）、`sharp corners`（直角）、`boxrule=0.5pt`（边框粗细）。

### 八、代码块

模板全局给 `lstlisting` 设了边框，默认语言是 LaTeX。所以写 JSON 或纯文本时，要加 `language={}` 关掉 LaTeX 高亮。

~~~latex
% Python：用 main.tex 里定义好的 agentpython 样式
\begin{lstlisting}[style=agentpython, caption={最小 Agent 循环}, label={lst:loop}]
while True:
    action = llm(context)
    if action.is_final:
        return action.answer
\end{lstlisting}

% JSON 或纯文本：关掉语言高亮
\begin{lstlisting}[language={}, caption={一条 tool 消息}]
{"role": "tool", "tool_call_id": "call_1", "content": "{\"temp\": 13}"}
\end{lstlisting}

% 行内代码，下划线不用转义
调用结果通过 \lstinline|tool_call_id| 和请求配对。
~~~

- 加了 `caption` 的代码块会有“Listing 1.1”式的标题。
- 加了 `label` 的可以用 `\ref{lst:loop}` 引用。
- 想给 JSON 定义固定样式，可以仿照 `main.tex` 里的 `agentpython`，再写一个 `\lstdefinestyle{agentjson}{...}`，把 `language=Python` 换成 `language={}`。

### 九、表格增强

除了 `booktabs` 的三线表，模板还加载了 `multirow`、`makecell` 和带 `table` 选项的 `xcolor`。

~~~latex
\begin{center}
\begin{tabular}{lll}
  \toprule
  \rowcolor{structurecolor!10}          % 给整行上底色
  写法 & 谁决定下一步 & 例子 \\
  \midrule
  \multirow{2}{*}{工作流}               % 竖向合并两行
    & 代码 & 订机票流水线 \\
    & 代码 & 文生图改写 \\
  Agent & 模型 & \makecell[l]{SWE-agent\\Claude Code} \\   % 单元格内换行
  \bottomrule
\end{tabular}
\end{center}
~~~

- `\multicolumn{2}{c}{内容}`：横向合并两列。
- `\cellcolor{second!10}`：只给一个单元格上色。

### 十、画流程图：TikZ

模板已经加载了 `tikz`，以及 `positioning`、`calc`、`fit`、`shadows`、`backgrounds` 这几个库，可以直接画 Agent 循环这类图。

~~~latex
\begin{figure}[htbp]
\centering
\begin{tikzpicture}[
    node distance=1.6cm,
    >=stealth,
    box/.style={draw=structurecolor, rounded corners, fill=structurecolor!8,
                minimum width=2.4cm, minimum height=0.9cm}
  ]
  \node[box] (llm)  {模型决定动作};
  \node[box, right=of llm]  (tool) {程序执行工具};
  \node[box, right=of tool] (ctx)  {结果追加上下文};
  \draw[->, thick] (llm) -- (tool);
  \draw[->, thick] (tool) -- (ctx);
  \draw[->, thick] (ctx.south) -- ++(0,-0.8) -| node[pos=0.25, below] {下一轮} (llm.south);
\end{tikzpicture}
\caption{ReAct 循环}
\label{fig:react-loop}
\end{figure}

如\figref{fig:react-loop} 所示……
~~~

要点：

- `right=of llm`：放在 `llm` 右边，间距由 `node distance` 决定。还可以用 `below=of`、`above right=of` 等。
- `-|`：先横着走再竖着走。`|-` 正好相反。
- `++(0,-0.8)`：从当前点往下移 0.8 厘米。

### 十一、插图路径

模板已经设好了图片搜索目录。只要把图片放进本目录下的 `figures/`、`figure/`、`images/`、`image/`、`pictures/` 或 `graphics/` 中的任一个，就可以只写文件名：

~~~latex
\includegraphics[width=0.7\linewidth]{agent-loop}   % 会自动去 figures/ 等目录找
~~~

### 十二、双栏

~~~latex
\begin{multicols}{2}
  左栏：工作流的优点……
  \columnbreak                 % 强制换到右栏
  右栏：Agent 的优点……
\end{multicols}
~~~

### 十三、参考文献（引用论文时用）

模板已经加载了 `biblatex`，后端是 `biber`。

1. 在本目录新建 `reference.bib`，写入条目：

~~~bibtex
@article{yao2022react,
  title   = {ReAct: Synergizing Reasoning and Acting in Language Models},
  author  = {Yao, Shunyu and Zhao, Jeffrey and Yu, Dian and others},
  journal = {arXiv preprint arXiv:2210.03629},
  year    = {2022}
}
~~~

2. 在 `main.tex` 的 `\begin{document}` 之前加 `\addbibresource{reference.bib}`。
3. 正文里写 `ReAct~\cite{yao2022react} 把推理和行动交替进行。`
4. 在 `\end{document}` 之前加 `\printbibliography[heading=bibintoc]`，最后会生成一页“参考文献”，并加入目录。
5. 编译顺序改成四步：

~~~powershell
xelatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex
biber main
xelatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex
xelatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex
~~~

论文的 BibTeX 条目可以在 arXiv 页面的“Export BibTeX Citation”或 Google Scholar 的“引用”里直接复制。

### 十四、全书结构命令

| 命令 | 作用 | 写在哪 |
|---|---|---|
| `\part{构建 Agent}` | 分“部分”，显示为“第一部分”，单独占一页 | `main.tex`，在一组 `\input` 前面 |
| `\appendix` | 之后的 `\chapter` 都变成“附录 A”“附录 B” | `main.tex`，在附录章节前面 |
| `\chapter*{前言}` | 不编号的章 | 任意位置 |
| `\section*{补充}` | 不编号的小节 | 任意位置 |
| `\tableofcontents` | 生成目录 | `main.tex`，已经在注释里 |

### 十五、封面

现在的 `main.tex` 没有封面。想加的话，在 `\begin{document}` 之前写这些信息，再在 `\begin{document}` 后面第一行写 `\maketitle`：

~~~latex
\title{AI Agent 课程笔记}
\subtitle{《深入理解 AI Agent》与 Stanford CS329Z}
\author{你的名字}
\date{2026 年秋}
\version{1.0}
\extrainfo{从一次 LLM 调用开始，搭出能用工具、管上下文的 Agent。}
\cover{cover.jpg}      % 封面顶部大图，放在 figures/ 里；不写会显示一张占位图
\logo{logo.png}        % 右下角小图，可以不写
~~~

### 十六、`\documentclass` 选项一览

都写在 `main.tex` 第一行的方括号里，用逗号隔开。

| 选项 | 可选值 | 作用 |
|---|---|---|
| `color` | `blue`（当前）、`green`、`cyan`、`gray`、`black` | 整套配色 |
| `mode` | `fancy`（当前）、`simple` | `simple` 去掉彩色框，定义、定理变成普通段落 |
| `titlestyle` | `hang`（默认）、`display` | `display` 让章标题的“第一章”单独占一行 |
| `toc` | `onecol`（默认）、`twocol` | 目录排成两栏 |
| `device` | `normal`（默认 A4）、`pad` | `pad` 用 7.5×10 英寸页面，适合在平板上看 |
| `marginpar` | `marginfalse`（默认）、`margintrue` | 右边留出 5 厘米宽的页边，正文里用 `\marginpar{旁注}` 写批注 |
| `thmcnt` | `chapter`（默认）、`section` | 框的编号按章（1.1）还是按节（1.1.1） |
| `usesamecnt` | 写上即生效 | 所有框共用一个编号序列 |
| `result` | `answer`（默认）、`noanswer` | `noanswer` 隐藏所有 `solution` 和 `proof` |
| `math` | `cm`（默认）、`newtx` | 数学字体 |

例：想在平板上看、并且带旁注栏：

~~~latex
\documentclass[lang=cn,scheme=chinese,color=blue,mode=fancy,oneside,11pt,device=pad]{elegantbook}
~~~

注意：`marginpar=margintrue` 只在 `device=normal` 下生效，和 `device=pad` 一起用时旁注栏不会出现。

### 十七、推荐用法：课程笔记里怎么分工

| 内容 | 用什么 |
|---|---|
| 术语的定义 | `definition` |
| 核心结论、判断标准 | 自建 `insight`（要点） |
| 书里或作业里的实验记录 | 自建 `experiment`，里面套 `description` 写“设置 / 观察 / 解释” |
| 具体例子 | `example` |
| 常见误区 | `custom{误区}`，或自建 `pitfall` |
| 资料出处 | `custom{出处}` |
| 需要警惕的坑 | `note` |
| 章首概览 | `introduction` |
| 章末思考题 | `problemset` |
| 代码 | `lstlisting` |
| 流程图 | TikZ 或 `\includegraphics` |
