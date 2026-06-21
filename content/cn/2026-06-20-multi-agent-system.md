---
title: 多智能体系统
enTitle: Multi-Agent System
date: 2026-06-20
slug: multi-agent-system
categories:
  - AI
tags:
  - 人工智能
  - AI
  - 单智能体
  - Single Agent
  - ReAct
  - 多智能体
  - Multi Agent
  - 分布式智能体
  - Distributed Agent
---

## 单智能体

在单智能体中，ReAct 框架 [^yao2022react] 作为当前智能体的一个核心设计模式，其通过 Reasoning（推理）和 Acting（行动）两个模块实现了大语言模型推理能力与外部环境交互能力的深度协同。ReAct 框架的整体执行过程如下图所示：

{{< figure src="/images/cn/2026-06-20-multi-agent-system/react.avif" large-max-width="300px" middle-max-width="300px" >}}

[^yao2022react]: Yao, Shunyu, et al. "React: Synergizing reasoning and acting in language models." _The eleventh international conference on learning representations._ 2022.

在之前的[博客](/cn/2026/04/agent-role-orientation-and-identity-evolution)中有介绍 ReAct 框架的主要特点，在上图中可以将流程划分为三个阶段：

### 初始化

该步骤会创建一个上下文，其中除了包含用户的输入以外还会包含系统提示词、可用的工具列表等其他信息。

### 循环迭代

循环迭代是 ReAct 框架的核心步骤，该步骤实现了在真实世界中人类解决问题的行为模式。

1. **推理**：用于分析任务目标，根据历史反馈和当前状态确定下一步动作。
2. **行动**：将模型推理的结果转化为可执行的工具指令（Tool Calling 或 Function Calling）。
3. **观测**：将工具执行结果返回给 LLM 用于确定下一步动作。

### 终止输出

当模型判断已获得最终答案后，会停止循环迭代并将结果输出给用户。除此之外也会存在异常输出的情况，例如：循环迭代达到最大限制次数，工具调用超时或返回错误等等。

我们以 [Hotpot QA](https://hotpotqa.github.io/) 数据集中的一个问题为例，对比其他方法展示 ReAct 框架是如何解决问题的。

{{< figure src="/images/cn/2026-06-20-multi-agent-system/comparison-of-4-prompting-methods.avif" >}}

## 多智能体

当单智能体配置的工具过多导致难以正确决策，或任务需要庞大的专业领域知识，抑或需要施加特定的顺序约束时，单智能体往往力不从心，此时多智能体架构成为更优的选择 [^langchain-blog-architecture]。归纳来看，引入多智能体主要是为了获得以下三方面能力：

1. **上下文管理（Context Management）**：单一提示词难以容纳所有能力所需的专业知识，需要按需将相关信息呈现给模型，避免上下文窗口被无关内容占满。
2. **分布式开发（Distributed Development）**：不同团队可以在清晰的边界内独立开发和维护各自的能力，再将其组合成更大的系统，而非维护一个庞大且难以协作的单体提示词。
3. **并行化（Parallelization）**：为不同子任务派发专门的智能体并发执行，从而获得更快的响应。

多智能体并非银弹。Anthropic 的研究 [^anthropic-multi-agent] 表明，以 Claude Opus 4 作为主智能体、Claude Sonnet 4 作为子智能体的多智能体系统，在其内部研究类评测中比单体 Claude Opus 4 高出 **90.2%**，关键在于多个子智能体各自拥有独立的上下文窗口，从而实现了单智能体难以企及的并行推理。但同时也应注意，单智能体更易于构建、推理和调试，应当优先从单智能体加良好的提示词与工具设计开始，只有在确实触及瓶颈时再引入多智能体。

### LangGraph 定义

根据 LangGraph v0.x 版本文档（已过时）[^langgraph-v0-doc]，其将多智能体模型划分为：**网络模式（Network）**、**监督模式（Supervisor）**、**工具化监督模式（Supervisor as Tools）**、**层级模式（Hierarchical）**和**自定义模式（Custom Workflow）**。

{{< figure src="/images/cn/2026-06-20-multi-agent-system/multi-agent-langgraph-v0.avif" large-max-width="640px" middle-max-width="640px" >}}

不同类型的多智能体模型的特点和差异如下：

| 类型 | 架构 | 优点 | 缺点 | 适用场景 |
| :--: | ---- | ---- | ---- | -------- |
| 单智能体 | 基础形态，一个 LLM 配置多个工具。 | 1. 结构简单，逻辑集中。<br/>2. 易于开发，调试方便。 | 1. 难以应对复杂任务。<br/>2. 可维护性和可拓展性差。 | 1. MVP 开发。<br/>2. 小型智能体开发。 |
| 网络模式 | 多个智能体之间相互连接，无明显的上下级关系，组成点对点的网络。 | 1. 去中心化，任意智能体之间均可通信。<br/>2. 灵活性高，容易激发群体涌现能力。 | 1. 任务流程可控性低。<br/>2. 容易出现循环调用。 | 1. 开放式问题求解。<br/>2. 探索性对话系统。|
| 监督模式 | 由主智能体负责调度指挥下面的子智能体，指令由主智能体分发，子智能体之间不直接通信。 | 1. 中心化决策，易于发现问题。<br/>2. 流程清晰，易于控制。 | 1. 主智能体容易产生瓶颈。 | 1. 结构化流程系统。 |
| 监督模式<br/>（工具化） | 同单智能体类似，区别在于调用的不一定是工具，也可能是其他智能体。 | 1. 复杂性封装。<br/>2. 标准化调用。 | 1. 主智能体难以干预子智能体。 | 1. 标准化子任务执行。 |
| 层级模式 | 监督模式的演化，子智能体之下还有子智能体，整体形成树状结构。 | 1. 模块化高，扩展性强。<br/>2. 层级管理，多级协调。 | 1. 系统复杂度高，响应速度慢。<br/>2. 信息在多层传递中可能失真。 | 1. 多领域任务调度。<br/>2. 企业级 AI 应用。 |
| 自定义模式 | 智能体之间的连接方式是根据业务逻辑自定义的。 | 1. 特定场景效率高。<br/>2. 路由可配置。 | 1. 灵活性差，开发成本高。 | 1. 结构化流程系统。 |
{width="10%,20%,25%,25%,20%"}

整体而言，没有最好的模式只有最适合的模式。在搭建多智能体系统时，需要根据实际的业务场景选择最合适的多智能体模式。

### LangChain 定义

根据 LangChain v1.x 版本文档 [^langchain-v1-doc]，其将多智能体模型划分为：**子智能体模式（Subagents）**、**传递模式（Handoffs）**、**技能模式（Skills）**、**路由模式（Router）**和**自定义模式（Custom Workflow）**。

#### 子智能体模式

{{< figure src="/images/cn/2026-06-20-multi-agent-system/multi-agent-langgraph-v1-subagents.avif" large-max-width="360px" middle-max-width="360px" >}}

类似上文中的监督模式。主智能体以工具方式调用子智能体对其进行协调，主智能体决定调用哪个子智能体、提供什么输入以及如何组合结果。子智能体是无状态的，所有记忆由主智能体维护。该模式的主要特点如下：

1. 中心化控制：所有路由都经由主智能体。
2. 无用户直接交互：子智能体将结果返回给主智能体而非用户。
3. 工具调用：子智能体作为工具被调用。
4. 并行执行：主智能体可以在单轮对话中调用多个子智能体。

当存在多个独立的场景（例如：日程、电子邮件、数据库等）时，子智能体无须同用户直接交互或者你希望通过统一流程进行控制，适合使用该模式。

#### 技能模式

{{< figure src="/images/cn/2026-06-20-multi-agent-system/multi-agent-langgraph-v1-skills.avif" large-max-width="360px" middle-max-width="360px" >}}

该模式下专业能力被打包成可调用的“技能”（Skill），用于增强智能体的行为能力。技能由专业化的提示词构成，智能体可以按需调用。该模式的主要特点如下：

1. 提示词驱动：技能由特定的专业化提示词定义。
2. 渐进式呈现：技能根据上下文或用户需求变为可用。
3. 团队分布式：不同团队可以独立开发和维护技能。
4. 轻量级组合：技能相比完整的子智能体更简单。
5. 引用感知：技能可以引用脚本、模板和其他资源。

当你希望单个智能体具有多种专业化，无须在技能之间施加强制约束，或者不同团队需要独立开发能力时，适合使用该模式。

{{% admonition type="warning" title="注意" %}}
技能模式在技术上仍然只使用单个智能体，LangChain 官方将其称为“准多智能体架构”。它通过让单个智能体动态切换专业化人格，获得了与多智能体类似的分布式开发与细粒度上下文控制能力，但采用的是更轻量的、提示词驱动的方式，而非真正管理多个智能体实例。
{{% /admonition %}}

#### 路由模式

{{< figure src="/images/cn/2026-06-20-multi-agent-system/multi-agent-langgraph-v1-router.avif" large-max-width="600px" middle-max-width="600px" >}}

该模式下，路由会对输入进行分类，并将其重定向至专门的智能体。该模式的主要特点如下：

1. 路由会对输入进行拆解。
2. 并行调用多个智能体。
3. 将结果整合成一个统一的响应。

当你拥有多个垂直领域（每个领域需要独立的智能体），需要并行查询多个数据源，同时希望将结果汇总成一个统一的响应时，适合使用该模式。

{{% admonition type="tip" title="路由模式 v.s. 子智能体模式" %}}
子智能体模式中的主智能体是一个完整的智能体，用来维护对话的上下文，并动态地决定在多轮中调用哪些子智能体。路由模式中的路由只是一个分类步骤，它将任务分派给各个智能体，其并不维护持续的对话状态。不过路由也可以被包装成一个工具，嵌入到一个有状态的会话智能体中，从而在保留分类与并行分发能力的同时，弥补其不维护对话历史的不足。
{{% /admonition %}}

#### 传递模式

{{< figure src="/images/cn/2026-06-20-multi-agent-system/multi-agent-langgraph-v1-handoffs.avif" large-max-width="420px" middle-max-width="420px" >}}

类似上文中的网络模式。该模式下，行为会根据状态动态变化。其核心机制是工具更新一个可跨多轮的状态变量，系统通过该状态变量来调整行为（例如：应用不同的提示词和工具，或将用户路由到不同的智能体）。该模式的主要特点如下：

1. 状态驱动行为：行为基于状态变量发生变化。
2. 基于工具的转换：工具更新状态变量以在不同状态之间切换。
3. 用户直接交互：每个状态配置均可以直接处理用户消息。
4. 状态持久化：状态可以贯穿多轮对话。

当你希望依据强制约束进行执行，智能体需要跨不同状态同用户直接沟通，或者构建多阶段对话流程时，适合使用该模式。该模式在客户支持场景中尤其适用，因为在该场景下需要根据特定顺序收集信息，例如在发起退款之前收集订单 ID。

{{% admonition type="warning" title="注意" %}}
传递模式只能顺序执行，无法并行处理。在需要同时咨询多个领域的场景下，它无法利用并行工具调用，往往需要更多的模型调用次数，效率较低。
{{% /admonition %}}

#### 自定义模式

{{< figure src="/images/cn/2026-06-20-multi-agent-system/multi-agent-langgraph-v1-custom-workflow.avif" large-max-width="460px" middle-max-width="460px" >}}

类似上文中的自定义模式。该模式下，你可以自定义执行流程，包括顺序执行、条件分支、循环和并行执行等。该模式的主要特点如下：

1. 完全的流程控制。
2. 将确定性逻辑和智能体行为相结合。
3. 支持顺序执行、条件分支、循环和并行执行。
4. 将其他模式作为节点融入到工作流中。

当上述模式无法满足需求，需要将确定性逻辑与智能体行为相结合，或者场景需要复杂的路由或多阶段处理时，适合使用该模式。

#### 模式能力对比

从分布式开发、并行化、多跳调用（Multi-hop，即串行调用多个子智能体）以及用户直接交互四个维度来看，不同模式各有侧重：

| 模式 | 分布式开发 | 并行化 | 多跳调用 | 用户直接交互 |
| -----| :--------: | :----: | :------: | :----------: |
| 子智能体模式 | <i class="icon-mask icon-star-filled"></i><i class="icon-mask icon-star-filled"></i><i class="icon-mask icon-star-filled"></i><i class="icon-mask icon-star-filled"></i><i class="icon-mask icon-star-filled"></i> | <i class="icon-mask icon-star-filled"></i><i class="icon-mask icon-star-filled"></i><i class="icon-mask icon-star-filled"></i><i class="icon-mask icon-star-filled"></i><i class="icon-mask icon-star-filled"></i> | <i class="icon-mask icon-star-filled"></i><i class="icon-mask icon-star-filled"></i><i class="icon-mask icon-star-filled"></i><i class="icon-mask icon-star-filled"></i><i class="icon-mask icon-star-filled"></i> | <i class="icon-mask icon-star-filled"></i> |
| 传递模式 | - | - | <i class="icon-mask icon-star-filled"></i><i class="icon-mask icon-star-filled"></i><i class="icon-mask icon-star-filled"></i><i class="icon-mask icon-star-filled"></i><i class="icon-mask icon-star-filled"></i> | <i class="icon-mask icon-star-filled"></i><i class="icon-mask icon-star-filled"></i><i class="icon-mask icon-star-filled"></i><i class="icon-mask icon-star-filled"></i><i class="icon-mask icon-star-filled"></i> |
| 技能模式 | <i class="icon-mask icon-star-filled"></i><i class="icon-mask icon-star-filled"></i><i class="icon-mask icon-star-filled"></i><i class="icon-mask icon-star-filled"></i><i class="icon-mask icon-star-filled"></i> | <i class="icon-mask icon-star-filled"></i><i class="icon-mask icon-star-filled"></i><i class="icon-mask icon-star-filled"></i> | <i class="icon-mask icon-star-filled"></i><i class="icon-mask icon-star-filled"></i><i class="icon-mask icon-star-filled"></i><i class="icon-mask icon-star-filled"></i><i class="icon-mask icon-star-filled"></i> | <i class="icon-mask icon-star-filled"></i><i class="icon-mask icon-star-filled"></i><i class="icon-mask icon-star-filled"></i><i class="icon-mask icon-star-filled"></i><i class="icon-mask icon-star-filled"></i> |
| 路由模式 | <i class="icon-mask icon-star-filled"></i><i class="icon-mask icon-star-filled"></i><i class="icon-mask icon-star-filled"></i> | <i class="icon-mask icon-star-filled"></i><i class="icon-mask icon-star-filled"></i><i class="icon-mask icon-star-filled"></i><i class="icon-mask icon-star-filled"></i><i class="icon-mask icon-star-filled"></i> | - | <i class="icon-mask icon-star-filled"></i><i class="icon-mask icon-star-filled"></i><i class="icon-mask icon-star-filled"></i> |

#### 模式性能对比

不同模式在模型调用次数和 token 消耗上存在明显差异。以下以三个典型场景为例：

| 模式 | 单次请求 | 重复请求 | 多领域查询 |
| ---- | :------: | :------: | :--------: |
| 子智能体模式 | 4 次 | 8 次（4+4） | 5 次 / 9K tokens |
| 传递模式 | 3 次 | 5 次（3+2） | 7+ 次 / 14K+ tokens |
| 技能模式 | 3 次 | 5 次（3+2） | 3 次 / 15K tokens |
| 路由模式 | 3 次 | 6 次（3+3） | 5 次 / 9K tokens |

从中可以总结出几点规律：

1. **子智能体模式**因子任务结果需经主智能体回流，每次子任务返回时会多出一次模型调用，但换来了最强的上下文隔离。
2. **有状态的模式**（传递模式、技能模式）在重复请求时可复用已有状态或已加载的技能，相比无状态模式节省约 40%~50% 的调用。
3. **多领域并行场景**下，支持并行执行的子智能体模式与路由模式最省 token；技能模式虽然调用次数少，但由于上下文不断累积，token 消耗反而最高；传递模式因只能顺序执行而效率最低。

最后需要强调的是，上述模式并非互斥，而是可以相互组合的。例如子智能体模式内部可以调用路由模式或自定义模式，子智能体本身也可以借助技能模式按需加载上下文。更多智能体架构的对比讨论和选择请参考 [LangChain 官方博客](https://www.langchain.com/blog/choosing-the-right-multi-agent-architecture)。

[^langchain-blog-architecture]: <https://www.langchain.com/blog/choosing-the-right-multi-agent-architecture>

[^anthropic-multi-agent]: <https://www.anthropic.com/engineering/multi-agent-research-system>

[^langgraph-v0-doc]: <https://web.archive.org/web/20241205065611/https://langchain-ai.github.io/langgraph/concepts/multi_agent/>

[^langchain-v1-doc]: <https://docs.langchain.com/oss/python/langchain/multi-agent>

### 系统实现

#### OpenClaw

OpenClaw 采用的是子智能体模式 [^openclaw-docs-multi-agent] [^openclaw-docs-subagents]，在 OpenClaw 中“一个智能体”拥有自己的：

1. 工作区（文件，`AGENTS.md`、`SOUL.md`、`USER.md`、本地笔记、人格规则）。
2. 状态目录（`agentDir`），用于凭证配置、模型注册和按智能体划分的配置。
3. 会话存储（聊天历史 + 路由状态），位于 `~/.openclaw/agents/<agentId>/sessions` 下。

凭证配置是按智能体划分的，每个智能体都会从自己的位置读取。子智能体是由一个现有的智能体派生出来的，其在独立的会话（`agent:<agentId>:subagent:<uuid>`）中运行。

[^openclaw-docs-multi-agent]: <https://docs.openclaw.ai/concepts/multi-agent>

[^openclaw-docs-subagents]: <https://docs.openclaw.ai/tools/subagents>

#### Hermes Agent

Hermes Agent 采用的是路由模式 [^hermes-agent-blog-multi-agent] [^hermes-docs-profiles]，在 Hermes Agent 中“一个智能体”定义为一个档案（Profile）。每个 Profile 拥有自己的目录，其中包含各自的 `config.yaml`、`.env`、`SOUL.md`、记忆、会话、技能、Cron 任务和状态数据库。

[^hermes-agent-blog-multi-agent]: <https://hermes-agent.ai/blog/hermes-agent-multi-agent>

[^hermes-docs-profiles]: <https://hermes-agent.nousresearch.com/docs/user-guide/profiles>

#### QwenPaw

QwenPaw 通过一个内置的 **多智能体协作（Multi-Agent Collaboration）** 技能实现智能体之间的通信和协作 [^qwenpaw-docs-multi-agent]，个人理解类似路由模式。每个智能体拥有自己的工作区，包括 `AGENTS.md`、`SOUL.md`、工具、技能、对话历史、定时任务等。

除了与不同工作区的其他智能体协作外，QwenPaw 还支持在当前项目内派发临时子任务。

| 模式 | 工作区 | 历史上下文 | 适用场景 |
| ---- | ------ | ---------- | -------- |
| `chat_with_agent` | 目标智能体独立工作区 | 无（只传消息） | 调用专长智能体（例如：QA、代码等） |
| `spawn_subagent(fork=False)` | 与当前智能体相同 | 无（空白会话） | 干净独立子任务 |
| `spawn_subagent(fork=True)` | 取决于环境 | 继承完整对话历史 | 需要背景的侧任务，且可能修改文件 |

通过 `spawn_subagent` 派发的子智能体不可恢复，子智能体使用相同的配置（例如：人格、工具等），只是在独立的会话中运行。

[^qwenpaw-docs-multi-agent]: <https://qwenpaw.agentscope.io/docs/multi-agent>

## 分布式智能体

以上讨论的都是在相同服务下的单智能体和多智能体实现，当我们需要让不同来源和实现的智能体之间进行协同时则需要构建一个分布式智能体系统。在分布式智能体中，每个智能体具备局部感知、自主规划与执行能力，并能跨节点交互，突破了单一系统在算力、扩展性和功能上的限制。分布式智能体具有如下特点：

1. **模块化与专业化**：将复杂任务拆解，交由不同专长的智能体处理（如：研究员、分析师、创作者等）。
2. **高鲁棒性与扩展性**：去中心化设计避免了单点故障。系统可根据需求跨多台机器、甚至跨多云环境进行水平扩展。
3. **异构协同**：允许运行在不同平台、不同框架的智能体通过标准化协议无缝互联。

在分布式智能体之间进行通信和协作需要统一的标准，A2A 协议 [^a2a-docs] 是由 Google 贡献，当前已加入 Linux 基金会的一个开放标准，它实现了智能体之间的无缝通信和协作。它为使用不同框架和由不同供应商构建的智能体提供了一种通用语言，从而促进了互操作性并打破了信息孤岛。不同于 MCP 协议解决的是智能体与工具、资源之间的协同问题，A2A 协议解决的是智能体与智能体之间的协同问题，两者之间的区别如下图所示：

{{< figure src="/images/cn/2026-06-20-multi-agent-system/a2a-and-mcp.avif" large-max-width="480px" middle-max-width="480px" >}}

虽然分布式智能体可以在横向扩展（更多实例，解决吞吐和并发问题）和纵向扩展（更多类型，解决合作和协同问题）上具有优势，但当前其仍面临诸多挑战 [^distributed-agent-zhihu-blog]，例如：

1. **任务状态一致性**：需要借助会话粘连（保证同一会话总是由同一实例处理）或状态持久化等手段，来实现状态同步，保证智能体任务状态和上下文在多个实例间的一致性。
2. **任务调度与容错**：需要有效的负载均衡和任务调度策略来优化资源利用，是简单的轮询还是根据实例响应时间或资源使用的动态分配等。此外，还需要考虑实例故障的容错，通常需要借助成熟的负载均衡与容器编排策略。
3. **消息传递效率**，**上下文共享**，**能力复用**等问题也会随着智能体复杂度提升而涌现。

[^a2a-docs]: <https://a2a-protocol.org/>

[^distributed-agent-zhihu-blog]: <https://zhuanlan.zhihu.com/p/1900870144567285384>
