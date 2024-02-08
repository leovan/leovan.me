---
title: 我们需要多少种编程语言 (How Many Programming Languages do We Need)
author: 范叶亮
date: '2024-02-09'
slug: how-many-programming-languages-do-we-need
categories:
  - 编程
tags:
  - 编程语言
  - 通用编程语言
  - GPL
  - 领域特定语言
  - DSL
  - 标记语言
---

编程语言「只是」达成目标的工具，这是我一直推崇的说法，因为我认为达成目标更重要的在于个人思考，编程语言不过是个「工具」，选哪个并没有那么重要。现在我越来越认为这个「工具」的选择还是很重要的，因为编程语言之于目标实现的可能性和效率都制约了目标的最终达成。

以个人数据科学的工作背景，结合我的编程语言学习路径，尝试回答一下我们需要多少种编程语言这个问题。我的编程语言学习路径大致如下：

- 小学时代：[Logo](https://zh.wikipedia.org/wiki/Logo_(%E7%A8%8B%E5%BA%8F%E8%AF%AD%E8%A8%80))
- 初高中时代：[Basic](https://zh.wikipedia.org/wiki/BASIC)，[HTML](https://zh.wikipedia.org/zh-cn/HTML)，[CSS](https://zh.wikipedia.org/wiki/CSS)
- 本科时代：[C](https://zh.wikipedia.org/wiki/C%E8%AF%AD%E8%A8%80)，[C++](https://zh.wikipedia.org/wiki/C%2B%2B)
- 研究生时代：[Matlab](https://zh.wikipedia.org/wiki/MATLAB)，[R](https://zh.wikipedia.org/wiki/R%E8%AF%AD%E8%A8%80)，[Python](https://zh.wikipedia.org/wiki/Python)，[SQL](https://zh.wikipedia.org/wiki/SQL)
- 工作时代：[Markdown](https://zh.wikipedia.org/wiki/Markdown)，[Java](https://zh.wikipedia.org/wiki/Java)，[JavaScript](https://zh.wikipedia.org/wiki/JavaScript)，[TypeScript](https://zh-yue.wikipedia.org/wiki/TypeScript)，[Rust](https://zh.wikipedia.org/wiki/Rust)

# 语言分类

在我的编程语言学习路径中，各个编程语言之间还是存在很大差异的，以最早接触的 Logo 为例，其除了教学目的之外似乎就真的没有什么大用途了。这些编程语言可以大致划分为如下三种类型：

- **通用编程语言（General-purpose Programming Language，GPL）**：Basic，C，C++，Python，JavaScript，TypeScript，Java，Rust
- **领域特定语言（Domain-Specific Language，DSL）**：Logo，CSS，Matlab，R，SQL
- **标记语言（Markup Language）**：HTML，Markdown

领域特定语言和标记语言就不用多说了，其应用范围有限。通用编程语言虽然定义为通用，但各自也有擅长和不擅长的领域，需要针对实际场景进行选择。

# 领域偏好

领域偏好是指你所从事的领域内大家对编程语言的使用偏好，这对于语言的选择至关重要，因为靠一己之力改变领域内大多数人的选择还是相当有难度的，从众可以极大地充分利用前人的成果降低工作的成本。

## 数据科学

数据科学可选的编程语言有 Python、R 和 Matlab 等，从技多不压身的角度出发肯定是掌握的越多越好，但精力终归是有限的。Matlab 在版权、仿真等方面具有一定的特殊性，Python 和 R 在数据科学中的竞争可谓是旷日持久，相关对比也数不胜数 [^python-vs-r-jiqizhixin] [^python-vs-r-datacamp] [^python-vs-r-geeksforgeeks]。

[^python-vs-r-datacamp]: <https://www.datacamp.com/blog/python-vs-r-for-data-science-whats-the-difference>

[^python-vs-r-geeksforgeeks]: <https://www.geeksforgeeks.org/r-vs-python/>

[^python-vs-r-jiqizhixin]: <https://www.jiqizhixin.com/articles/2018-06-30-2>

如果非要二选一我现在会选择 **Python**，因为其作为通用编程语言在将数据科学和工程代码结合时会展现出更多的优势。但在一些特定领域，例如生物信息学，R 的采用率会更高。一些新起之秀例如 Julia 和 Mojo 仍需要进一步观测其发展，过早地大面积使用新语言可能会面临各种风险。

## 后端

企业级后端应用中 Java 应该是首选，对一些高性能场景 C/C++、Rust 可能更加适合。

在实际工作中，Python 依旧可以作为一个不错的后端语言选择。Python 在 HTTP 和 RPC 接口、高并发、开源组件 SDK 支持等方面都不错的表现。Python 作为一种解释型语言，时常被诟病运行慢，这确实是解释型语言的一个问题。不过现在很多流行扩展包都是基于 C/C++ 构建，并且从 3.13 版本开始已经可选去除全局解释锁，这些都会使 Python 的性能变得越来越好。个人认为 Python 运行慢的另一个原因是使用者对其理解仍不够深入，使用的技巧仍有待提升，《流畅的 Python》可以让你对 Python 有更深入的认识。

## 前端

前端是程序与用户进行交互的必经之路，HTML，CSS 和 JavaScript 可以算得上前端三剑客了，分别负责元素的定义、样式和交互。随着 Node.js 的发展，JavaScript 也可以作为后端语言使用。TypeScript 作为 JavaScript 的超集，扩展了 JavaScript 的功能和特性，同时随着 React 和 Vue 框架的出现，前端的发展可谓是盛况空前。

Python 此时就真的很难插入一脚了，不过话无绝对，基于 WebAssembly 技术 Python 也可以在前端运行。WebAssembly 设计的目的是为了提升前端代码的运行效率，而在这方面从实践上 [^antv-layout] 来看 [Rust](https://www.rust-lang.org/zh-CN/what/wasm) 更受青睐。

[^antv-layout]: <https://github.com/antvis/layout>

## 客户端

在 Apple 和 Google 两大移动阵营中，iOS（iPadOS 和 tvOS）系统的首选语言为 Swift，Android 系统的首选语言为 Kotlin。在 Apple 和 Microsoft 两大桌面阵营中，macOS 系统的首选语言为 Swift，Windows 系统的首选语言为 .Net。原生语言可以让应用更好的适配对应的系统，但引入的问题就是相同应用针对不同系统适配的成本增加。针对大公司的核心应用确实有这个必要，但是普通场景，「跨平台」则会更吸引人。

在之前的[博客](/cn/2018/05/cross-platform-gui-application-based-on-pyqt/)中有对桌面端的跨平台框架作简要分析，但结合当下移动端的市场占比，基于前端技术的跨平台解决方案会是一个不错的选择。

## 脚本

脚本可以说就只是程序员自己为了方便而产生的需求，不出意外它应该只会出现在命令行的黑框框中。在类 Unix 系统中，Shell 是一个通用且不需要额外安装扩展的不错之选。除此之外，什么 Python、Perl、Ruby、Lua 都在不同的场景中发光发热，相信我们将处于并将长期处于脚本语言的五代十国中。

## 嵌入式

早期的嵌入式我认为是一个相对专业垂直的领域，由于操作的对象更加底层，所以使用的语言也会更底层一些，例如 C/C++。随着硬件的不断发展，开发板、智能设备、机器人都在逐步走入更多程序员的视野，硬件性能的提升也使得 Python 等高级语言可以作为嵌入式开发的工具。

# 个人偏好

领域偏好是站在客观的角度指导我们如何选择语言，但谁还没有些小脾气呢？以自己为例，最早接触的数据分析语言是 Matlab，我的本科和研究生的论文都是用 Matlab 完成的，当时是由于实验室都在用它（领域偏好），但我个人并不很喜欢它。虽然上面我也承认在 Python 和 R 的大战中，如果非让我选一个我会选择 Python，但这也剥夺不了我对 R 的钟爱。R 的管道符 `|>` 用起来就是舒服，虽然 Python 第三方也提供了类似的扩展包 `siuba`，但模仿终归还是模仿。

在一定程度上坚持自己的个性还是可能会有些益处的。仍以自己为例，钟爱 R 的我在了解到 RMarkdown 之后让我喜欢上了可重复性研究（更多细节可参见之前的[博客](/cn/2023/03/literate-programming-and-reproducible-research/)）。再到之后的 Quarto，最终我将这些内容融入工作之中，开发工作中适用的产品。可以说如果仅是基于领域偏好彻底拥抱 Python 而抛弃 R，那么我会错过不少优秀的项目和工具。还有不得不提的 `ggplot2`，图形语法的最好践行者，Python 中 Matlab 的遗留瑰宝 `matplotlib` 我只能说很强大但我不喜欢用，至于 Python 第三方提供的类似扩展包 `plotnine`，模仿终归还是模仿。

# 真实需要

聊了这么多，到底我们需要多少种编程语言？这取决于你到底想要啥？

如果想作为一个安分守己的数据科学工作者，Python 能撑起你 90% 的需求，多花一些时间去了解业务可能比你多学一门编程语言的收益要大得多。

如果你不够安分，不想深藏于后端，甚至有技术变现的想法，那么前端交互自然不可缺失。此时 JavaScript/TypeScript 应该是个不错的选择，毕竟你不是要成为一个专业的前端或 APP 开发人员，跨平台才应该是我们应该偏好的重点，毕竟一套代码处处可用，变现的速度就可以杠杠的了。

当然我相信除了眼前的这些苟且，大家还是有更远大抱负的，那么在这条布满荆棘的路上你会遇到更复杂的问题。性能的提升我会选择 Rust，毕竟人家除了能提升后端还能提升前端，何乐而不为呢？

综上所述，作为数据科学工作的从业者，我将以并将长期以如下四句作为我编程语言选择的重要指导方针：

{{% admonition type="tip" %}}
人生苦短，我用 <i class="icon icon-python">Python</i>。

想要甜些，得上 <i class="icon icon-javascript">JavaScript</i> / <i class="icon icon-typescript">TypeScript</i>。

开心的话，就用 <i class="icon icon-r">R</i>。

再想更屌，恶补 <i class="icon icon-rust">Rust</i>。
{{% /admonition %}}
