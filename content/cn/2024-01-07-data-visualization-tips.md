---
title: 数据可视化小贴士
subtitle: 面向动态文档生成，秉承规范、统一和实用的理念
author: 范叶亮
date: '2024-01-07'
slug: data-visualization-tips
categories:
  - 编程
  - 设计
tags:
  - 可视化
  - 一画胜千言
  - 设计规范
  - 可视化规范
  - Ant Vision
  - AntV
  - ECharts
  - Plotly
  - D3
  - Matplotlib
  - seaborn
  - plotnine
  - ggplot2
  - quarto
  - Jupyter Widgets
  - htmlwidgets
  - 布局
  - 色板
  - 字体
  - 尺寸
  - 响应式
images:
  - /images/cn/2024-01-07-data-visualization-tips/a-picture-is-worth-a-thousand-words.jpg
  - /images/cn/2024-01-07-data-visualization-tips/ant-vision-layout.png
  - /images/cn/2024-01-07-data-visualization-tips/ant-vision-color-palette.png
  - /images/cn/2024-01-07-data-visualization-tips/ant-vision-font.png
---

{{% admonition type="tip" %}}
文本主要面向不同格式文档（HTML、PDF、Word）的动态生成，秉承规范、统一和实用的理念总结数据可视化过程中的相关问题，不过度涉及数据可视化本身细节。
{{% /admonition %}}

一画胜千言（A picture is worth a thousand words）是我个人很推崇的一个指引，不过前提是这得是一张「好图」，否则容易过犹不及。

![一画胜千言](/images/cn/2024-01-07-data-visualization-tips/a-picture-is-worth-a-thousand-words.jpg)

数据可视化是一门复杂的学问，在动态文档生成中，秉承规范、统一和实用的理念，我认为是快速提高数据可视化质量的不错之选。

# 设计规范

在之前的文章[「设计语言初探」](/cn/2021/08/a-glimpse-of-design-language/)中探讨过产品的设计语言，在此针对各大企业的数据可视化规范并结合中文文档生成和个人偏好做简要分析。各大企业的数据可视化规范如下：

| 企业      | 数据可视化规范                                      |
| ---------- | ------------------------------------------------------------ |
| <i class="icon icon-apple">Apple</i>      | [Human Interface Guidelines - Charts](https://developer.apple.com/design/human-interface-guidelines/charts) |
| <i class="icon icon-google">Google</i> | [Material Design - Data Visualization](https://m2.material.io/design/communication/data-visualization.html)                |
| <i class="icon icon-microsoft">Microsoft</i> | [Data visualization style guidelines for Office Add-ins](https://learn.microsoft.com/en-us/office/dev/add-ins/design/data-visualization-guidelines)     |
| <i class="icon icon-adobe">Adobe</i>      | [Spectrum - Data Visualization](https://spectrum.adobe.com/page/data-visualization-fundamentals/)                      |
| <i class="icon icon-ibm">IBM</i>        | [Carbon Design System - Data Visualization](https://carbondesignsystem.com/data-visualization/getting-started/)  |
| <i class="icon icon-salesforce">Salesforce</i> | [Lightning Design System - Data Visualization](https://www.lightningdesignsystem.com/guidelines/data-visualization/charts/) |
| <i class="icon icon-ant-group">蚂蚁金服</i>  | [Ant Vision](https://antv.antgroup.com/specification/principles/basic)                            |

各家的设计理念有所不同，但我相信其目标是一致的，就是让用户可以更好更快地理解数据并从数据中获取洞见。上面的大多数数据可视化规范依旧是以面向产品设计为主，不过我认为大部分理念是可以迁移到文档中的可视化，尤其是 HTML 格式的动态文档。

Apple、Google、Microsoft 三大家的规范在自家系统的平台上针对**简单**的可视化场景可以说是最适用的，毕竟原生设计毫无违和感。但针对**复杂**的可视化场景，三家并没有给出更细的指引，不过也能理解针对商业数据可视化和科技绘图等复杂场景，确实更适合由上层（例如：库、应用等）去根据实际情况作出相应规范。

所以，站在**规范**和**统一**的视角，我个人更倾向于选择适合中国宝宝体质的 Ant Vision。给出些我认为靠谱的理由：

1. 设计体系基于具有更悠久历史的 Ant Design 衍生，具有完善的设计规范指引。
2. 针对简单场景（例如：统计图表等）和复杂场景（例如：地图、关系图表等）都有较好的覆盖。
3. 科学的色彩体系，在萝卜青菜各有所爱的配色之上给到了科学的指引。
4. 最后也是我认为最重要的特点，开源，且有丰富的中文文档。

从规范和统一的角度，可以说 Ant Vision 是最优选择，有关 Ant Vision 的更多资料除了[官网](https://antv.antgroup.com/)以外，还可以参见[语雀上的 AntV 文档](https://www.yuque.com/antv)。

# 工具选择

由于是面向动态文档生成为主，基于各种可视化工具的绘图很难嵌入自动化流水线中，因此本节主要讨论相关扩展包，不涉及专用的可视化工具（例如：Tableau，Power BI 等）。常用的可视化扩展包及其支持的语言和图类型，如下表所示：

| 扩展包                                              | JS/TS | Python                  | R             | 统计图 | 地图 | 关系图 |
| --------------------------------------------------- | ----- | ----------------------- | ------------- | ------ | ---- | ------ |
| [Ant Vision](https://github.com/antvis)             | ✅     | ❌                       | ⛔️[^g2r]       | ✅      | ✅    | ✅      |
| [ECharts](https://echarts.apache.org/zh/index.html) | ✅     | ☑️[^pyecharts]           | ☑️[^echarts4r] | ✅      | ✅    | ✅      |
| [Plotly](https://plotly.com/)                       | ✅     | ✅                       | ✅             | ✅      | ✅    | ✅      |
| [D3](https://d3js.org/)                             | ✅     | ☑️[^d3blocks] [^d3graph] | ☑️[^r2d3]      | ✅      | ✅    | ✅      |
| [Matplotlib](https://matplotlib.org/)               | ❌     | ✅                       | ❌             | ✅      | ✅    | ✅      |
| [seaborn](https://seaborn.pydata.org/)              | ❌     | ✅                       | ❌             | ✅      | ❌    | ❌      |
| [plotnine](https://plotnine.readthedocs.io/)        | ❌     | ✅                       | ❌             | ✅      | ✅    | ❌      |
| [ggplot2](https://ggplot2.tidyverse.org/)           | ❌     | ❌                       | ✅             | ✅      | ✅    | ✅      |

[^g2r]: 由第三方 [g2r](https://github.com/devOpifex/g2r) 提供 G2 部分支持，已停止更新。

[^pyecharts]: 由第三方 [pyecharts](https://pyecharts.org/) 提供支持。

[^echarts4r]: 由第三方 [echarts4r](https://echarts4r.john-coene.com/) 提供支持。

[^d3blocks]: 由第三方 [d3blocks](https://github.com/d3blocks/d3blocks) 提供支持。

[^d3graph]: 由第三方 [d3graph](https://github.com/erdogant/d3blocks) 提供关系图支持。

[^r2d3]: 由第三方 [r2d3](https://rstudio.github.io/r2d3/) 提供支持。

上述扩展包是我个人在实际项目中真实会使用到的，此时此刻就不难发现 Ant Vision 最大的问题就是对科学编程几乎 [^l7vp] 没有官方支持。

[^l7vp]: L7VP 提供了 Python 绑定。

用于可视化的扩展包远不止上述的这 8 种，但我们不可能去学习使用所有的扩展包，这样于自己需要投入大量的学习成本，于团队也不利于项目的维护。即便就这 8 种扩展包，其语法也大不相同。

我接触的第一门绘图语言应该是 [Logo](https://zh.wikipedia.org/wiki/Logo_(%E7%A8%8B%E5%BA%8F%E8%AF%AD%E8%A8%80))，不过 Logo 是一门教学语言，所以在科学编程中使用的最早的是 Matlab 的绘图功能，Matplotlib 从名称上就不难看出是源自 Matlab。不过个人而言不是很喜欢 Matplotlib 的 API 风格，或者说我认为其 API 更偏底层一些。谈到这里就不得不谈一下「The Grammar of Graphics」，这也是我个人认为绘图「最舒服」的 ggplot2 扩展包背后的理论。在上述扩展包中，ggplot2 算是先驱者，plotnine 是 ggplot2 的 Python 复刻，Plotly 的 R 绑定可以支持直接将 ggplot2 对象绘制成 plotly 绘图，Ant Vision 则在该核心理论的基础上做了更多探索。所以当掌握了图形语法的理论基础后，对这些包的学习就相对会简单不少。由于长尾需求还是会存在，所以掌握不同可视化包的使用就成了技多不压身，我认为上述 8 种扩展包覆盖 99% 的可视化需求应该不成问题。

上述 8 种可视化包中，前 4 种都是以 JS/TS 库为基础，部分由官方或三方实现了 Python 和 R 的绑定，所以前 4 种天然就支持可交互绘图。利用 Python 的 [Jupyter Widgets](https://jupyter.org/widgets) 和 R 的 [htmlwidgets](https://www.htmlwidgets.org/) 实现在网页和 Notebook 中的可交互绘图。D3 背后的 Observable JS 也被当下流行的动态文档生成工具 [quarto](https://quarto.org/) 所[支持](https://quarto.org/docs/interactive/ojs/)。后 4 种则只能创建不可交互的静态绘图，Matplotlib 作为 Python 绘图的重要可视化扩展包提供了丰富的绘图 API，seaborn 和 plotnine 均基于其开发，seaborn 简化了 API，plotnine 提供了 ggplot2 语法支持，而 ggplot2 则是 R 语言中数据可视化的不二之选。

讲了这么多并不是要在各个扩展包之间分个孰优孰劣，而是需要其特性和需求场景选择合适的扩展包。在此个人愚见如下：

1. 动态绘图：Plotly > ECharts > D3 > Ant Vision，理由：多语言支持优先。
2. 动态绘图（复杂场景，例如：地图、关系图等）：Ant Vision > D3 > ECharts > Plotly，理由：交互性能优先。
3. 静态绘图：ggplot2 = plotnine > seaborn > Matplotlib，理由：语法简单易于理解优先。
4. 静态绘图（长尾需求，例如：示意图等）Matplotlib，理由：较为底层的绘图 API，使用更为灵活。

# 实用建议

根据规范，为了保证利用不同的工具绘图的视觉效果一致，我们需要在布局、色板、字体等多个角度进行自定义配置。下表展示了扩展包在不用语言绑定中样式的可自定义特性：

| 扩展包                                              | JS/TS                                                        | Python                                                       | R                                                            |
| --------------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| [Ant Vision](https://github.com/antvis)             | ☑️[详情](https://g2.antv.antgroup.com/theme)                  | -                                                            | -                                                            |
| [ECharts](https://echarts.apache.org/zh/index.html) | ☑️[详情](https://echarts.apache.org/handbook/zh/concepts/style) | ☑️[详情](https://pyecharts.org/#/zh-cn/themes)                | ☑️[详情](https://echarts4r.john-coene.com/articles/themes)    |
| [Plotly](https://plotly.com/)                       | ☑️[详情](https://plotly.com/javascript/layout-template/)      | ✅[详情](https://plotly.com/python/templates/)                | ☑️[详情](https://plotly.com/r/styling-figures/)，✅复用 ggplot2 |
| [D3](https://d3js.org/)                             | ❌[详情](https://d3-graph-gallery.com/custom.html)            | ❌                                                            | ❌                                                            |
| [Matplotlib](https://matplotlib.org/)               | -                                                            | ✅[详情](https://matplotlib.org/stable/users/explain/customizing.html) | -                                                            |
| [seaborn](https://seaborn.pydata.org/)              | -                                                            | ✅复用 Matplotlib                                             | -                                                            |
| [plotnine](https://plotnine.readthedocs.io/)        | -                                                            | ✅[详情](https://plotnine.readthedocs.io/en/latest/api.html#theme-helper-functions-and-classes) | -                                                            |
| [ggplot2](https://ggplot2.tidyverse.org/)           | -                                                            | -                                                            | ✅[详情](https://ggplot2.tidyverse.org/reference/index.html#themes) |

其中，✅表示支持自定义样式，且支持修改全局默认样式；☑️表示支持自定义样式，不支持修改全局默认样式，但支持通过函数一次性设置自定义样式；❌表示支持自定义样式，但需要每次手动配置所有样式细节。

## 布局

在 Ant Vision 设计语言中一个图应该包含标题、轴、图形、标签、注解、提示信息、图例等信息，如下图所示：

![布局](/images/cn/2024-01-07-data-visualization-tips/ant-vision-layout.png)

大多数扩展包支持绝大多数元素，但对于一些相对特殊的元素（例如：注解，尤其是富文本的注解）支持较为有限。同时不同扩展包对于相同元素的样式控制也存在差异，这就导致很难将在不同扩展包之间做到完全统一，只能是尽可能相似。

## 色板

色板（配色）是影响统一的另一大重要因素，相比布局其更好做到不同扩展包之间的统一。根据 Ant Vision 的设计语言，色板分为：分类、顺序、发散、叠加、强调、语义共 6 大色板，如下图所示：

![色板](/images/cn/2024-01-07-data-visualization-tips/ant-vision-color-palette.png)

不同扩展包不一定能覆盖所有类型色板（视其绘图能力而定）。除了选择合适的统一色板之外，不同类型色板在使用时也有各自的[注意事项](https://antv.antgroup.com/specification/language/palette)，虽然这无关样式统一，但却会从很大程度上影响数据可视化的效果。

## 字体

根据 Ant Vision 的设计语言，数据可视化字体应当具备三个条件：数字等宽、识别度高、混排美观，如下图所示：

![字体](/images/cn/2024-01-07-data-visualization-tips/ant-vision-font.png)

针对文档生成，个人总结了能够覆盖大部分文档场景且商用免费的字体，如下表所示：

| 字体名称          | 字体分类    | 语言   | 版权              | 建议使用场景 |
| ----------------- | ----------- | ------ | ----------------- | ------------ |
| 思源黑体          | 无衬线黑体  | 中英文 | SIL开源，商用免费 | 网页正文     |
| 思源宋体          | 衬线宋体    | 中英文 | SIL开源，商用免费 | PDF&Word正文 |
| 方正仿宋          | 仿宋        | 中英文 | 商用免费          | 公文         |
| 方正楷体          | 楷体        | 中英文 | 商用免费          | 注释         |
| ETbb              | 衬线        | 英文   | MIT开源，商用免费 | PDF&Word正文 |
| Latin Modern Math | TeX数学字体 | 英文   | GFL开源，商用免费 | 数学公式     |
| 更纱黑体          | 等宽黑体    | 中英文 | SIL开源，商用免费 | 代码         |

为了满足 Ant Vision 对字体的要求，在 Word 和 PDF 格式文档中的静态绘图可以使用**更纱黑体**。针对 HTML 格式文档，由于不会内嵌字体，为了适配不同的操作系统同时考虑不同字体的可用性，可以将交互式绘图字体设置为多个值：

```css
{
  font-family: Iosevka, 'Iosevka Nerd', Consolas, 'Lucida Console', Menlo, Monaco, 'Andale Mono', 'Ubuntu Mono', 'Source Han Mono SC', 'Source Han Mono TC', 'Source Han Mono', 'Noto Sans Mono SC', 'Noto Sans Mono TC', 'Noto Sans Mono', monospace, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol' !important;
}
```

## 尺寸 & 响应式

错误的尺寸选择或不良的元素位置摆放都会导致可视化效果变差。PDF 和 Word 格式文档，以及 PC 端的 HTML 格式文档，通过限制页面宽度，可以相对统一的规范到标准的可读内容宽度。此时图片的最大宽度是已知的，可视化时仅需要考虑合适的宽高比即可。

针对移动端的 HTML 文档，由于可读内容宽度较小，绘图的尺寸则需要有针对性地进行调整。此时，使用交互式绘图则比静态绘图有更有优势，利用交互式绘图本身的[响应式能力](https://antv.antgroup.com/specification/language/media)，可以减少人工调整的工作量，也更容易实现一套绘图代码处处可用的效果。

在动态文档生成过程中，我们很难预估数据的真实场景，一些极端情况往往可能会导致可视化结果完全不可用。因此在编写绘图代码时应充分考虑到数据类别的数量、数据类别名称的长度、数据分布等多种因素，同时将绘图中的不同元素摆放在合适的位置。编写出适应性更好的绘图代码才能保证动态文档的高可用性，当然这个过程不是一蹴而就的，随着真实数据中极端情况的积累，绘图代码也会越来越完善越来越鲁棒。
