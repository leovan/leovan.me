---
title: CSS 布局和定位 (CSS Display & Position)
author: 范叶亮
date: '2023-05-03'
slug: css-display-and-position
show_toc: true
toc_depth: 3
categories:
  - 编程
  - 设计
tags:
  - CSS
  - 盒模型
  - box model
  - 块级盒子
  - block box
  - 内联盒子
  - inline box
  - 布局
  - display
  - 弹性布局
  - flex layout
  - 网格布局
  - grid layout
  - 定位
  - position
  - 静态定位
  - static
  - 相对定位
  - relative
  - 绝对定位
  - absolute
  - 固定定位
  - fixed
  - 粘性定位
  - sticky
images:
  - /images/cn/2023-05-03-css-display-and-position/css-box-model.png
---

CSS 中的布局 `display` 和定位 `position` 可以说是两个最基本的属性，其控制着元素在网页中的显示方式。之前对布局和定位可谓是一知半解，最终奏不奏效全凭一顿乱试😂，想了想还是应该细致地了解下，后面虽不妄想写起代码来事半功倍，但至少不会再暴力遍历破解了。

# 盒模型

在介绍布局和定位之前，首先回顾一下 CSS 的盒模型。CSS 盒模型从外到内由**外边距 `margin`**、**边框 `border`**、**内边距 `padding`** 和**内容 `content`** 共 4 部分组成，如下图所示：

{{< figure src="/images/cn/2023-05-03-css-display-and-position/css-box-model.png" title="CSS 盒模型" >}}

元素的宽度 `width` 为内容的宽度 + 左边框 + 有边框 + 左内边距 + 右内边距，上例中为 $360+10+10+10+10=400$；元素的的高度 `height` 为内容的高度 + 上边框 + 下边框 + 上内边距 + 下内边距，上例中为 $240+10+10+20+20=300$。在实际中，我们并不能直接设定内容的宽度和高度，只能设置元素的宽度和高度，而显示区域的宽度和高度则通过计算自动设定。

在 CSS 中广泛使用的有两种盒子模型：**块级盒子（block box）** 和 **内联盒子（inline box）**[^mdn-css-box-model]。

**块级盒子**有如下表现行为：

- 盒子会在内联方向上扩展并占据父容器在该方向上的所有可用空间，在绝大数情况下意味着盒子会和父容器一样宽。
- 每个盒子都会换行。
- `width` 和 `height` 属性可以发挥作用。
- 内边距、外边距和边框会将其他元素从当前盒子周围“推开”。

除非特殊指定，诸如标题 (`<h1>` 等) 和段落 (`<p>`) 默认情况下都是块级的盒子。

**内联盒子**有如下表现行为：

- 盒子不会产生换行。
- `width` 和 `height` 属性将不起作用。
- 垂直方向的内边距、外边距以及边框会被应用但是不会把其他处于 `inline` 状态的盒子推开。
- 水平方向的内边距、外边距以及边框会被应用且会把其他处于 `inline` 状态的盒子推开。

`<a>` 、`<span>`、`<em>` 以及 `<strong>` 都是默认处于 `inline` 状态的。

[^mdn-css-box-model]: https://developer.mozilla.org/zh-CN/docs/Learn/CSS/Building_blocks/The_box_model

# 布局

在 CSS 中使用 `display` 属性控制元素的布局方式，上文中的 `block` 和 `inline` 是最常用的两种布局方式。除此之外还有一种介于块级盒子和内联盒子之间的布局方式，即 `inline-block`，其具有如下表现行为：

- 盒子不会产生换行。
- `width` 和 `height` 属性可以发挥作用。
- 内边距、外边距和边框会将其他元素从当前盒子周围“推开”。

{{< flex >}}

{{< flex-item >}}
{{< include "/static/codes/cn/2023-05-03-css-display-and-position/inline-span.html" >}}
{{< /flex-item >}}

{{< flex-item >}}
{{< include "/static/codes/cn/2023-05-03-css-display-and-position/inline-block-span.html" >}}
{{< /flex-item >}}

{{< /flex >}}

上图分别展示了 `display: inline` 和 `display: inline-block` 两种布局 `span` 元素的显示差异。

## 弹性布局

{{% admonition %}}
本节内容主要参考自：[A Complete Guide to Flexbox](https://css-tricks.com/snippets/css/a-guide-to-flexbox/)
{{% /admonition %}}

**弹性布局（Flexbox Layout，Flexible Box Layout）** 旨在提供一种更加有效的方式来布局、对齐和分配容器中元素之间的空间，即使元素的大小是未知或动态的，这也就是称为“弹性”的原因。

弹性布局是一套完整的模块而非一个单一的属性，其中一些属性要设置在**父元素（flex container）** 上，一些属性要设置在**子元素（flex items）** 上。常规布局是基于块级元素和内联元素的的流向，而弹性布局是基于**弹性流向（flex-flow directions）**。下图展示了弹性布局的基本思想：

{{< figure src="/images/cn/2023-05-03-css-display-and-position/flexbox-basic-terminology.svg" title="Flexbox 基本思想" >}}

### 父元素属性

{{< figure src="/images/cn/2023-05-03-css-display-and-position/flexbox-container.svg" middle-max-width="60%">}}

#### display

该属性启用弹性容器，为其子元素开启弹性上下文。

```css
.container {
  display: flex; /* 或 inline-flex */
}
```

#### flex-direction

{{< figure src="/images/cn/2023-05-03-css-display-and-position/flexbox-flex-direction.svg">}}

该属性定义了弹性流向，即基本思想中的 `main-axis`。

```css
.container {
  flex-direction: row | row-reverse | column | column-reverse;
}
```

- `row`（默认）：`ltr` 时从左至右，`rtl` 时从右至左
- `row-reverse`：`ltr` 时从右至左，`rtl` 时从左至右
- `column`：从上至下
- `column-reverse`：从下至上

#### flex-wrap

{{< figure src="/images/cn/2023-05-03-css-display-and-position/flexbox-flex-wrap.svg" middle-max-width="60%">}}

默认情况下会将子元素放置在一行中，该属性用于设置换行模式。

```css
.container {
  flex-wrap: nowrap | wrap | wrap-reverse;
}
```

- `nowarp`（默认）：所有子元素放置在一行中。
- `wrap`：允许换行，从上至下。
- `wrap-reverse`：允许换行，从下至上。

#### flex-flow

该属性是 `flex-direction` 和 `flex-wrap` 两个属性的简写。

```css
.container {
  flex-flow: column wrap;
}
```

#### justify-content

{{< figure src="/images/cn/2023-05-03-css-display-and-position/flexbox-justify-content.svg" middle-max-width="60%">}}

该属性用于设置主轴（main axis）方向的对齐方式。

```css
.container {
  justify-content: flex-start | flex-end | center | space-between | space-around | space-evenly | start | end | left | right ... + safe | unsafe;
}
```

- `flex-start`（默认）：将子元素排列在 `flex-direction` 起始位置。
- `flex-end`：将子元素排列在 `flex-direction` 结束位置。
- `center`：将子元素沿着 `flex-direction` 方向居中排列。
- `space-between`：将子元素沿着 `flex-direction` 方向均匀排列，第一个子元素位于起始位置，最后一个子元素位于结束位置。
- `space-around`：将子元素沿着 `flex-direction` 方向均匀排列，每个子元素周围分配相同的空间。
- `space-evenly`：将子元素沿着 `flex-direction` 方向均匀排列，每个子元素之间的间隔相同。

#### align-items

{{< figure src="/images/cn/2023-05-03-css-display-and-position/flexbox-align-items.svg" middle-max-width="60%">}}

该属性用于设置交叉轴（cross axis）方向的对齐方式。

```css
.container {
  align-items: stretch | flex-start | flex-end | center | baseline | first baseline | last baseline | start | end | self-start | self-end + ... safe | unsafe;
}
```

- `stretch`（默认）：拉伸并填充容器（仍遵守 `min-width` 和 `max-width`）。
- `flex-start / start / self-start`：子元素被放置在交叉轴的起始位置。
- `flex-end / end / self-end`：子元素被放置在交叉轴的结束位置。
- `center`：子元素在交叉轴上居中对齐。
- `baseline`：子元素沿着他们的基线对齐。

#### align-content

{{< figure src="/images/cn/2023-05-03-css-display-and-position/flexbox-align-content.svg" middle-max-width="60%">}}

该属性用于设置当交叉轴上有额外的空间时容器多行的内部对齐方式，类似 `justify-content` 设置主轴上子元素的对齐方式。

{{% admonition title="" %}}
该属性仅对包含多行子元素的容器有效。
{{% /admonition %}}

```css
.container {
  align-content: flex-start | flex-end | center | space-between | space-around | space-evenly | stretch | start | end | baseline | first baseline | last baseline + ... safe | unsafe;
}
```

- `normal`（默认）：子元素被放置到容器的默认位置。
- `flex-start / start`：子元素被放置到容器的起始位置。
- `flex-end  / end`：子元素被放置到容器的结束位置。
- `center`：子元素被放置到容器的居中位置。
- `space-between`：子元素均匀分布，第一行在容器的起始位置，最后一行在容器的结束位置。
- `space-around`：子元素均匀分布，每行元素周围分配相同的空间。
- `space-evenly`：子元素均匀分布，每行元素之间的间隔相同。
- `stretch`：子元素拉伸占用剩余空间。

#### gap, row-gap, column-gap

{{< figure src="/images/cn/2023-05-03-css-display-and-position/flexbox-gap.svg" middle-max-width="60%">}}

该属性用于控制子元素之间的间距，其仅用于非边缘子元素之间的间距。

```css
.container {
  display: flex;
  ...
  gap: 10px;
  gap: 10px 20px; /* row-gap column gap */
  row-gap: 10px;
  column-gap: 20px;
}
```

该属性产生的行为可以认为是子元素之间的最小间距。

### 子元素属性

{{< figure src="/images/cn/2023-05-03-css-display-and-position/flexbox-items.svg" middle-max-width="60%">}}

#### order

{{< figure src="/images/cn/2023-05-03-css-display-and-position/flexbox-order.svg" middle-max-width="60%">}}

默认情况下，子元素按照代码顺序排列。该属性可以控制子元素在容器中的顺序。

```css
.item {
  order: 5; /* 默认为 0 */
}
```

#### flex-grow

{{< figure src="/images/cn/2023-05-03-css-display-and-position/flexbox-flex-grow.svg" middle-max-width="60%">}}

该属性定义了子元素在必要时的扩张能力，其接受一个整数比例值用于设定子元素占用容器的空间。如果所有子元素的 `flew-grow` 都设置为 1，则所有子元素将评分容器的剩余空间；如果一个子元素的 `flex-grow` 设置为 2，则该子元素将尝试占用其他子元素 2 倍大小的空间。

```css
.item {
  flex-grow: 4; /* 默认为 0 */
}
```

#### flex-shrink

该属性定义了子元素在必要时的收缩能力。

```css
.item {
  flex-shrink: 3; /* 默认为 1 */
}
```

#### flex-basis

该属性定义了分配剩余空间之前子元素的默认大小。其可以为例如 `20%`、`5rem` 之类的长度或一个关键字。

```css
.item {
  flex-basis:  | auto; /* 默认为 auto */
}
```

#### flex

该属性是 `flex-grow`、`flex-shrink` 和 `flex-basis` 三个属性的简写。

```css
.item {
  flex: none | [ <'flex-grow'> <'flex-shrink'>? || <'flex-basis'> ]
}
```

#### align-self

{{< figure src="/images/cn/2023-05-03-css-display-and-position/flexbox-align-self.svg" middle-max-width="60%">}}

该属性可以覆盖由 `align-items` 指定的对齐方式。

```css
.item {
  align-self: auto | flex-start | flex-end | center | baseline | stretch;
}
```

## 网格布局

{{% admonition %}}
本节内容主要参考自：[A Complete Guide to CSS Grid](https://css-tricks.com/snippets/css/complete-guide-grid/)
{{% /admonition %}}

**网格布局（Grid Layout）** 是一种基于网格的布局系统，相比于沿轴线 **一维布局** 的弹性布局，网格布局可以看做是一种 **二维布局**。

### 核心概念

#### 网格容器

网格容器即属性 `display` 为 `grid` 的元素，其为所有网格项目的直接父级。如下示例中，`container` 即为网格容器：

```html
<div class="container">
  <div class="item item-1"> </div>
  <div class="item item-2"> </div>
  <div class="item item-3"> </div>
</div>
```

#### 网格项目

网格项目为网格容器的直接后代。如下示例中，`item` 即为网格项目，但 `sub-item` 不是：

```html
<div class="container">
  <div class="item"> </div>
  <div class="item">
    <p class="sub-item"> </p>
  </div>
  <div class="item"> </div>
</div>
```

#### 网格线

网格线即构成网格结构的分界线。其可以是位于行或列任意一侧的垂直或水平线。如下示例中，黄色的线为一条列网格线：

{{< figure src="/images/cn/2023-05-03-css-display-and-position/grid-terms-grid-line.svg" middle-max-width="60%" large-max-width="40%">}}

#### 网格单元

网格单元即两个相邻行和两个相邻列之间的区域。如下示例中，黄色区域为行网格线 1 和 2 以及列网格线 2 和 3 之间的单元格：

{{< figure src="/images/cn/2023-05-03-css-display-and-position/grid-terms-grid-cell.svg" middle-max-width="60%" large-max-width="40%">}}

#### 网格轨道

网格轨道即 2 条相邻网格线之间的区域，可以将其视为网格的行或列。如下示例中，黄色区域为第 2 行和第 3 行网格线之间的网格轨道：

{{< figure src="/images/cn/2023-05-03-css-display-and-position/grid-terms-grid-track.svg" middle-max-width="60%" large-max-width="40%">}}

#### 网格区域

网格区域即 4 条网格线包围的区域，一个网格区域可以由任意数量的网格单元组成。如下示例中，黄色区域为行网格线 1 和 3 以及列网格线 1 和 3 之间的网格区域：

{{< figure src="/images/cn/2023-05-03-css-display-and-position/grid-terms-grid-area.svg" middle-max-width="60%" large-max-width="40%">}}

### 父元素属性

#### display

该属性启用网格容器，为其子元素开启网格上下文。

```css
.container {
  display: grid | inline-grid;
}
```

#### grid-template-columns, grid-template-rows

该属性通过空格分隔的值列表定义网格的列和行，值代表轨道的大小。值列表包括：

- `<track-size>`：轨道大小，可以为长度、百分比等。
- `<line-name>`：网格线名称，可以为任意值。

```css
.container {
  grid-template-columns: ...  ...;
  /* 例如：
      1fr 1fr
      minmax(10px, 1fr) 3fr
      repeat(5, 1fr)
      50px auto 100px 1fr
  */
  grid-template-rows: ... ...;
  /* 例如：
      min-content 1fr min-content
      100px 1fr max-content
  */
}
```

网格线默认将会被分为正整数（-1 作为最后一个的替代值）。

{{< figure src="/images/cn/2023-05-03-css-display-and-position/grid-template-columns-rows-01.svg" middle-max-width="60%" >}}

同时也可以明确指定这些线的名称，请注意括号命名语法：

```css
.container {
  grid-template-columns: [first] 40px [line2] 50px [line3] auto [col4-start] 50px [five] 40px [end];
  grid-template-rows: [row1-start] 25% [row1-end] 100px [third-line] auto [last-line];
}
```

{{< figure src="/images/cn/2023-05-03-css-display-and-position/grid-template-columns-rows-02.svg" middle-max-width="60%" >}}

请注意，一个行或列可以有多个名称：

```css
.container {
  grid-template-rows: [row1-start] 25% [row1-end row2-start] 25% [row2-end];
}
```

使用 `repeat()` 可以简化重复项：

```css
.container {
  grid-template-columns: repeat(3, 20px [col-start]);
}
```

上述代码等效于：

```css
.container {
  grid-template-columns: 20px [col-start] 20px [col-start] 20px [col-start];
}
```

如果多行或多列共享相同的名称，可以通过行名或列名和计数来引用它们：

```css
.item {
  grid-column-start: col-start 2;
}
```

`fr` 单位允许将轨道的大小设置为网格容器可用空间的一定比例。例如，如下示例将每个项目设置为容器宽度的三分之一：

```css
.container {
  grid-template-columns: 1fr 1fr 1fr;
}
```

可用空间是在所有非弹性项目之后计算得到。在上述示例中，`fr` 单位的可用空间总量不包括 `50px`：

```css
.container {
  grid-template-columns: 1fr 50px 1fr 1fr;
}
```

#### grid-template-areas

该属性通过引用网格区域的名称 `grid-area` 来定义网格。重复网格区域名称会导致内容跨越这些单元格。句点表示一个空单元格。语法本身提供了网格结构的可视化。

- `<grid-area-name>`：网格区域的名称。
- `.`：空网格单元。
- `none`：未定义的网格区域。

```css
.container {
  grid-template-areas: 
    "<grid-area-name> | . | none | ..."
    "...";
}
```

```css
.item-a {
  grid-area: header;
}
.item-b {
  grid-area: main;
}
.item-c {
  grid-area: sidebar;
}
.item-d {
  grid-area: footer;
}

.container {
  display: grid;
  grid-template-columns: 50px 50px 50px 50px;
  grid-template-rows: auto;
  grid-template-areas: 
    "header header header header"
    "main main . sidebar"
    "footer footer footer footer";
}
```

上述示例将创建一个 4 列 3 行的网格。整个顶部为 `header` 区域，中间一行由 `main` 和 `sidebar` 两个区域和一个空单元格组成，最后一行为 `footer`。

{{< figure src="/images/cn/2023-05-03-css-display-and-position/grid-template-areas.svg" middle-max-width="60%" >}}

声明中的每一行都需要有相同数量的单元格。可以使用任意数量的句点声明一个空单元格，只要句点之间没有空格，就代表一个单元格。

注意使用此语法仅可以命名区域，不可命名线。使用此语法时，区域两端的线会自动命名，如果网格区域名称为 `foo`，那么该区域的起始行线和起始列线名称为 `foo-start`，该区域的终止行线和终止列线名称为 `foo-end`。这意味着某些线可能有多个名称，上述示例中最左边的行线将有 3 个名称：`header-start`、`main-start` 和 `footer-start`。

#### grid-template

该属性是 `grid-template-rows`、`grid-template-columns` 和 `grid-template-areas` 三个属性的简写。

```css
.container {
  grid-template: none | <grid-template-rows> / <grid-template-columns>;
}
```

其接受更复杂但更方便的语法来指定这三个值，例如：

```css
.container {
  grid-template:
    [row1-start] "header header header" 25px [row1-end]
    [row2-start] "footer footer footer" 25px [row2-end]
    / auto 50px auto;
}
```

上述代码等效于：

```css
.container {
  grid-template-rows: [row1-start] 25px [row1-end row2-start] 25px [row2-end];
  grid-template-columns: auto 50px auto;
  grid-template-areas: 
    "header header header" 
    "footer footer footer";
}
```

由于 `grid-template` 并不会重置网格的隐含属性（`grid-auto-columns`、`grid-auto-rows` 和 `grid-auto-flow`）。因此，建议使用 `grid` 属性而非 `grid-template`。

#### column-gap, row-gap, grid-column-gap, grid-row-gap

该属性用于指定网格线的大小，你可以将其看做列和行之间的间距。

```css
.container {
  /* standard */
  column-gap: <line-size>;
  row-gap: <line-size>;

  /* old */
  grid-column-gap: <line-size>;
  grid-row-gap: <line-size>;
}
```

```css
.container {
  grid-template-columns: 100px 50px 100px;
  grid-template-rows: 80px auto 80px; 
  column-gap: 10px;
  row-gap: 15px;
}
```

{{< figure src="/images/cn/2023-05-03-css-display-and-position/grid-gap.svg" middle-max-width="60%" >}}

间距仅在列和行之间创建，不在边缘创建。注意，带有 `grid-` 前缀的属性将被废弃。

#### gap, grid-gap

该属性为 `row-gap` 和 `column-gap` 两个属性的简写。

```css
.container {
  /* standard */
  gap: <grid-row-gap> <grid-column-gap>;

  /* old */
  grid-gap: <grid-row-gap> <grid-column-gap>;
}
```

```css
.container {
  grid-template-columns: 100px 50px 100px;
  grid-template-rows: 80px auto 80px; 
  gap: 15px 10px;
}
```

如果未指定 `row-gap`，则它将被设置为与 `column-gap` 相同的值。注意，带有 `grid-` 前缀的属性将被废弃。

#### justify-items

沿 `inline`（行）轴对齐网格项（与沿 `block`（列）轴对齐 `align-items` 相反）。该属性将应用于容器内所有网格项。

- `stretch`（默认值）：将网格项填充至整个单元格宽度。
- `start`：将网格项与单元的起始边缘对齐。
- `end`：将网格项与单元的结束边缘对齐。
- `center`：将网格项与单元的中心对齐。

```css
.container {
  justify-items: stretch | start | end | center;
}
```

```css
.container {
  justify-items: stretch;
}
```

{{< figure src="/images/cn/2023-05-03-css-display-and-position/grid-justify-items-stretch.svg" middle-max-width="60%" large-max-width="40%" >}}

```css
.container {
  justify-items: start;
}
```

{{< figure src="/images/cn/2023-05-03-css-display-and-position/grid-justify-items-start.svg" middle-max-width="60%" large-max-width="40%" >}}

```css
.container {
  justify-items: end;
}
```

{{< figure src="/images/cn/2023-05-03-css-display-and-position/grid-justify-items-end.svg" middle-max-width="60%" large-max-width="40%" >}}

```css
.container {
  justify-items: center;
}
```

{{< figure src="/images/cn/2023-05-03-css-display-and-position/grid-justify-items-center.svg" middle-max-width="60%" large-max-width="40%" >}}

#### align-items

沿 `block`（列）轴对齐网格项（与沿 `inline`（行）轴对齐 `align-items` 相反）。该属性将应用于容器内所有网格项。

- `stretch`（默认值）：将网格项填充至整个单元格高度。
- `start`：将网格项与单元的起始边缘对齐。
- `end`：将网格项与单元的结束边缘对齐。
- `center`：将网格项与单元的中心对齐。
- `baseline`：将网格项沿文本基线对齐。

```css
.container {
  align-items: stretch | start | end | center;
}
```

```css
.container {
  align-items: stretch;
}
```

{{< figure src="/images/cn/2023-05-03-css-display-and-position/grid-align-items-stretch.svg" middle-max-width="60%" large-max-width="40%" >}}

```css
.container {
  align-items: start;
}
```

{{< figure src="/images/cn/2023-05-03-css-display-and-position/grid-align-items-start.svg" middle-max-width="60%" large-max-width="40%" >}}

```css
.container {
  align-items: end;
}
```

{{< figure src="/images/cn/2023-05-03-css-display-and-position/grid-align-items-end.svg" middle-max-width="60%" large-max-width="40%" >}}

```css
.container {
  align-items: center;
}
```

{{< figure src="/images/cn/2023-05-03-css-display-and-position/grid-align-items-center.svg" middle-max-width="60%" large-max-width="40%" >}}

通过 `align-self` 属性可以在单个网格项上覆盖由 `align-items` 指定的对齐方式。

#### place-items

该属性在单次声明中同时设置 `align-items` 和 `justify-items` 属性。

- `<align-items> / <justify-items>`：省略第二个值则将第一个值分配给两个属性。

```css
.center {
  display: grid;
  place-items: center;
}
```

#### justify-content

当所有网格项均使用非弹性的单位（例如 `px`）来确定大小，则网格的总大小可能小于网格容器的大小。在这种情况下，可以在网格容器内设置网格的对齐方式。该属性沿 `inline`（行）轴（与沿 `block`（列）轴对齐 `align-content` 相反）对齐网格。

- `start`：将网格与网格容器的起始边缘对齐。
- `end`：将网格与网格容器的结束边缘对齐。
- `center`：将网格与网格容器的中心对齐。
- `stretch `：调整网格项的大小使网格填充网格容器的整个宽度。
- `space-around`：每个网格项均匀分布，每个网格项周围分配相同的空间。
- `space-between`：每个网格项均匀分布，第一个网格项在起始位置，最后一个网格项在结束位置。
- `space-evenly`：每个网格项均匀分布，每个网格项之间的间隔相同。

```css
.container {
  justify-content: start | end | center | stretch | space-around | space-between | space-evenly;    
}
```

```css
.container {
  justify-content: start;
}
```

{{< figure src="/images/cn/2023-05-03-css-display-and-position/grid-justify-content-start.svg" middle-max-width="60%" large-max-width="40%" >}}

```css
.container {
  justify-content: end;
}
```

{{< figure src="/images/cn/2023-05-03-css-display-and-position/grid-justify-content-end.svg" middle-max-width="60%" large-max-width="40%" >}}

```css
.container {
  justify-content: center;
}
```

{{< figure src="/images/cn/2023-05-03-css-display-and-position/grid-justify-content-center.svg" middle-max-width="60%" large-max-width="40%" >}}

```css
.container {
  justify-content: stretch;
}
```

{{< figure src="/images/cn/2023-05-03-css-display-and-position/grid-justify-content-stretch.svg" middle-max-width="60%" large-max-width="40%" >}}

```css
.container {
  justify-content: space-around;
}
```

{{< figure src="/images/cn/2023-05-03-css-display-and-position/grid-justify-content-space-around.svg" middle-max-width="60%" large-max-width="40%" >}}

```css
.container {
  justify-content: space-between;
}
```

{{< figure src="/images/cn/2023-05-03-css-display-and-position/grid-justify-content-space-between.svg" middle-max-width="60%" large-max-width="40%" >}}

```css
.container {
  justify-content: space-evenly;
}
```

{{< figure src="/images/cn/2023-05-03-css-display-and-position/grid-justify-content-space-evenly.svg" middle-max-width="60%" large-max-width="40%" >}}

#### align-content

当所有网格项均使用非弹性的单位（例如 `px`）来确定大小，则网格的总大小可能小于网格容器的大小。在这种情况下，可以在网格容器内设置网格的对齐方式。该属性沿 `block`（列）轴（与沿 `inline`（行）轴对齐 `justify-content` 相反）对齐网格。

- `start`：将网格与网格容器的起始边缘对齐。
- `end`：将网格与网格容器的结束边缘对齐。
- `center`：将网格与网格容器的中心对齐。
- `stretch `：调整网格项的大小使网格填充网格容器的整个高度。
- `space-around`：每个网格项均匀分布，每个网格项周围分配相同的空间。
- `space-between`：每个网格项均匀分布，第一个网格项在起始位置，最后一个网格项在结束位置。
- `space-evenly`：每个网格项均匀分布，每个网格项之间的间隔相同。

```css
.container {
  align-content: start | end | center | stretch | space-around | space-between | space-evenly;    
}
```

```css
.container {
  align-content: start;    
}
```

{{< figure src="/images/cn/2023-05-03-css-display-and-position/grid-align-content-start.svg" middle-max-width="60%" large-max-width="40%" >}}

```css
.container {
  align-content: end;    
}
```

{{< figure src="/images/cn/2023-05-03-css-display-and-position/grid-align-content-end.svg" middle-max-width="60%" large-max-width="40%" >}}

```css
.container {
  align-content: center;    
}
```

{{< figure src="/images/cn/2023-05-03-css-display-and-position/grid-align-content-center.svg" middle-max-width="60%" large-max-width="40%" >}}

```css
.container {
  align-content: stretch;    
}
```

{{< figure src="/images/cn/2023-05-03-css-display-and-position/grid-align-content-stretch.svg" middle-max-width="60%" large-max-width="40%" >}}

```css
.container {
  align-content: space-around;    
}
```

{{< figure src="/images/cn/2023-05-03-css-display-and-position/grid-align-content-space-around.svg" middle-max-width="60%" large-max-width="40%" >}}

```css
.container {
  align-content: space-between;    
}
```

{{< figure src="/images/cn/2023-05-03-css-display-and-position/grid-align-content-space-between.svg" middle-max-width="60%" large-max-width="40%" >}}

```css
.container {
  align-content: space-evenly;    
}
```

{{< figure src="/images/cn/2023-05-03-css-display-and-position/grid-align-content-space-evenly.svg" middle-max-width="60%" large-max-width="40%" >}}

#### place-content

该属性在单次声明中同时设置 `align-content` 和 `justify-content` 属性。

- `<align-content> / <justify-content>`：省略第二个值则将第一个值分配给两个属性。

#### grid-auto-columns, grid-auto-rows

该属性指定自动生成的网格轨道（也称为隐式网格轨道）的大小。当网格项多于网格中的单元格或当网格项放置在显示网格之外时，将创建隐式网格轨道。

- `<track-size>`：可以为长度、百分比或可用空间的比例（使用 `fr` 单位）。

```css
.container {
  grid-auto-columns: <track-size> ...;
  grid-auto-rows: <track-size> ...;
}
```

```css
.container {
  grid-template-columns: 60px 60px;
  grid-template-rows: 90px 90px;
}
```

上述代码将生成一个 2x2 的网格：

{{< figure src="/images/cn/2023-05-03-css-display-and-position/grid-auto-columns-rows-01.svg" middle-max-width="60%" large-max-width="40%" >}}

使用 `grid-column` 和 `grid-row` 来定位网格项：

```css
.item-a {
  grid-column: 1 / 2;
  grid-row: 2 / 3;
}
.item-b {
  grid-column: 5 / 6;
  grid-row: 2 / 3;
}
```

{{< figure src="/images/cn/2023-05-03-css-display-and-position/grid-auto-columns-rows-02.svg" middle-max-width="60%" large-max-width="40%" >}}

`.item-b` 从第 5 列线开始到第 6 列线结束，但由于并未定义第 5 列线和第 6 列线，因此创建了宽度为 0 的隐式轨道用于填充间隙。使用 `grid-auto-columns` 和 `grid-auto-rows` 可以指定这些隐式轨道的宽度：

```css
.container {
  grid-auto-columns: 60px;
}
```

{{< figure src="/images/cn/2023-05-03-css-display-and-position/grid-auto-columns-rows-03.svg" middle-max-width="60%" large-max-width="40%" >}}

#### grid-auto-flow

如果有未明确放置在网格中的网格项目，自动放置算法会自动放置这些网格项目。此属性用于控制自动放置算法的工作方式。

- `row`（默认）：依次填充每一行，并根据需要添加新行。
- `column`：依次填充每一列，并根据需要添加新列。
- `dense`：将可能较晚出现的较小的网格项优先填充在网格中。

```css
.container {
  grid-auto-flow: row | column | row dense | column dense;
}
```

注意 `dense` 仅会改变网格项目的视觉顺序，这可能导致顺序混乱且不利于访问。

考虑如下示例：

```html
<section class="container">
  <div class="item-a">item-a</div>
  <div class="item-b">item-b</div>
  <div class="item-c">item-c</div>
  <div class="item-d">item-d</div>
  <div class="item-e">item-e</div>
</section>
```

定义一个包含 5 列和 2 行的网格，并将 `grid-auto-flow` 设置为 `row`：

```css
.container {
  display: grid;
  grid-template-columns: 60px 60px 60px 60px 60px;
  grid-template-rows: 30px 30px;
  grid-auto-flow: row;
}
```

将网格项目放置在网格中时，只需要为其中两个指定位置：

```css
.item-a {
  grid-column: 1;
  grid-row: 1 / 3;
}
.item-e {
  grid-column: 5;
  grid-row: 1 / 3;
}
```

因为将 `grid-auto-flow` 设置为了 `row`，未放置的三个网格项目（`item-b`、`item-c` 和 `item-d`）如下所示：

{{< figure src="/images/cn/2023-05-03-css-display-and-position/grid-auto-flow-01.svg" middle-max-width="60%" large-max-width="40%" >}}

```css
.container {
  display: grid;
  grid-template-columns: 60px 60px 60px 60px 60px;
  grid-template-rows: 30px 30px;
  grid-auto-flow: column;
}
```

如果将 `grid-auto-flow` 设置为 `column`，未放置的三个网格项目（`item-b`、`item-c` 和 `item-d`）如下所示：

{{< figure src="/images/cn/2023-05-03-css-display-and-position/grid-auto-flow-02.svg" middle-max-width="60%" large-max-width="40%" >}}

#### grid

该属性为 `grid-template-rows`、`grid-template-columns`、`grid-template-areas`、`grid-auto-rows`、`grid-auto-columns` 和 `grid-auto-flow` 属性的简写。

- `none`：将所有子属性设置为初始值。
- `<grid-template>`：同 `grid-template`。
- `<grid-template-rows> / [ auto-flow && dense? ] <grid-auto-columns>?`：设置 `grid-template-rows` 为指定值。如果使用 `auto-flow` 关键字，则设置 `grid-auto-flow` 为 `colomn`。如果额外使用 `dense` 关键字，则自动放置算法将使用 `dense` 算法。如果省略 `grid-auto-columns`，则其被设置为 `auto`。
- `[ auto-flow && dense? ] <grid-auto-rows>? / <grid-template-columns>`：设置 `grid-template-columns` 为指定值。如果使用 `auto-flow` 关键字，则设置 `grid-auto-flow` 为 `row`。如果额外使用 `dense` 关键字，则自动放置算法将使用 `dense` 算法。如果省略 `grid-auto-rows`，则其被设置为 `auto`。

如下示例中的代码是等效的：

```css
.container {
  grid: 100px 300px / 3fr 1fr;
}

.container {
  grid-template-rows: 100px 300px;
  grid-template-columns: 3fr 1fr;
}
```

```css
.container {
  grid: auto-flow / 200px 1fr;
}

.container {
  grid-auto-flow: row;
  grid-template-columns: 200px 1fr;
}
```

```css
.container {
  grid: auto-flow dense 100px / 1fr 2fr;
}

.container {
  grid-auto-flow: row dense;
  grid-auto-rows: 100px;
  grid-template-columns: 1fr 2fr;
}
```

```css
.container {
  grid: 100px 300px / auto-flow 200px;
}

.container {
  grid-template-rows: 100px 300px;
  grid-auto-flow: column;
  grid-auto-columns: 200px;
}
```

它还接受更复杂但更方便的语法来一次性设置所有内容。如下示例中的代码是等效的：

```css
.container {
  grid: [row1-start] "header header header" 1fr [row1-end]
        [row2-start] "footer footer footer" 25px [row2-end]
        / auto 50px auto;
}

.container {
  grid-template-areas: 
    "header header header"
    "footer footer footer";
  grid-template-rows: [row1-start] 1fr [row1-end row2-start] 25px [row2-end];
  grid-template-columns: auto 50px auto;    
}
```

### 子元素属性

#### grid-column-start, grid-column-end, grid-row-start, grid-row-end

该属性通过网格线来设置网格项在网格中的位置。`grid-column-start` 和 `grid-row-start` 为网格项起始的线，`grid-column-end` 和 `grid-row-end` 为网格项结束的线。

- `<line>`：指代网格线的数字编号或名称。
- `span <number>`：该网格项跨越的网格轨道数。
- `span <name>`：该网格项跨越直到它抵达该名称网格线的下一个网格线。
- `auto`：表示自动放置、自动跨度或一个默认跨度。

```css
.item {
  grid-column-start: <number> | <name> | span <number> | span <name> | auto;
  grid-column-end: <number> | <name> | span <number> | span <name> | auto;
  grid-row-start: <number> | <name> | span <number> | span <name> | auto;
  grid-row-end: <number> | <name> | span <number> | span <name> | auto;
}
```

```css
.item-a {
  grid-column-start: 2;
  grid-column-end: five;
  grid-row-start: row1-start;
  grid-row-end: 3;
}
```

{{< figure src="/images/cn/2023-05-03-css-display-and-position/grid-column-row-start-end-01.svg" middle-max-width="60%" large-max-width="40%" >}}

```css
.item-b {
  grid-column-start: 1;
  grid-column-end: span col4-start;
  grid-row-start: 2;
  grid-row-end: span 2;
}
```

{{< figure src="/images/cn/2023-05-03-css-display-and-position/grid-column-row-start-end-02.svg" middle-max-width="60%" large-max-width="40%" >}}

如果 `grid-column-end` 或 `grid-row-end` 未声明，则该网格项将默认跨越一个轨道。网格项目之间可以相互重叠，使用 `z-index` 可以控制它们的重叠次序。

#### grid-column, grid-row

分别是 `grid-column-start` + `grid-column-end` 和 `grid-row-start`+ `grid-row-end` 的简写。

- `<start-line> / <end-line>`：接受非简写版本相同的值，包括 `span`。

```css
.item {
  grid-column: <start-line> / <end-line> | <start-line> / span <value>;
  grid-row: <start-line> / <end-line> | <start-line> / span <value>;
}
```

```css
.item-c {
  grid-column: 3 / span 2;
  grid-row: third-line / 4;
}
```

{{< figure src="/images/cn/2023-05-03-css-display-and-position/grid-column-row.svg" middle-max-width="60%" large-max-width="40%" >}}

如果未设置结束线的值，则该网格项将默认跨越一个轨道。

#### grid-area

为一个网格项命名以便它可以使用 `grid-template-areas` 属性创建的模板引用。此属性可以作为 `grid-row-start` + `grid-column-start` + `grid-row-end` + `grid-column-end` 的简写。

- `<name>`：选用的名称。
- `<row-start> / <column-start> / <row-end> / <column-end>`：可以为数字编号或线名称。

用作为网格项分配名称：

```css
.item-d {
  grid-area: header;
}
```

用作 `grid-row-start` + `grid-column-start` + `grid-row-end` + `grid-column-end` 的简写：

```css
.item-d {
  grid-area: 1 / col4-start / last-line / 6;
}
```

{{< figure src="/images/cn/2023-05-03-css-display-and-position/grid-area.svg" middle-max-width="60%" large-max-width="40%" >}}

#### justify-self

沿 `inline`（行）轴对齐单元格内的网格项（与沿 `block`（列）轴对齐 `align-self` 相反）。该属性仅应用于单个单元格内的网格项。

- `stretch`（默认）：填充单元格的整个宽度。
- `start`：将网格项与单元格的起始边缘对齐。
- `end`：将网格项与单元格的结束边缘对齐。
- `center`：将网格项与单元格的中心对齐。

```css
.item {
  justify-self: stretch | start | end | center;
}
```

```css
.item-a {
  justify-self: stretch;
}
```

{{< figure src="/images/cn/2023-05-03-css-display-and-position/grid-justify-self-stretch.svg" middle-max-width="60%" large-max-width="40%" >}}

```css
.item-a {
  justify-self: start;
}
```

{{< figure src="/images/cn/2023-05-03-css-display-and-position/grid-justify-self-start.svg" middle-max-width="60%" large-max-width="40%" >}}

```css
.item-a {
  justify-self: end;
}
```

{{< figure src="/images/cn/2023-05-03-css-display-and-position/grid-justify-self-end.svg" middle-max-width="60%" large-max-width="40%" >}}

```css
.item-a {
  justify-self: center;
}
```

{{< figure src="/images/cn/2023-05-03-css-display-and-position/grid-justify-self-center.svg" middle-max-width="60%" large-max-width="40%" >}}

通过 `justify-items` 属性可以为容器中所有的网格项设置对齐方式。

#### align-self

沿 `block`（列）轴对齐单元格内的网格项（与沿 `inline`（行）轴对齐 `justify-self` 相反）。该属性将仅应用于单个单元格内的网格项。

- `stretch`（默认）：填充单元格的整个高度。
- `start`：将网格项与单元格的起始边缘对齐。
- `end`：将网格项与单元格的结束边缘对齐。
- `center`：将网格项与单元格的中心对齐。

```css
.item {
  align-self: stretch | start | end | center;
}
```

```css
.item-a {
  align-self: stretch;
}
```

{{< figure src="/images/cn/2023-05-03-css-display-and-position/grid-align-self-stretch.svg" middle-max-width="60%" large-max-width="40%" >}}

```css
.item-a {
  align-self: start;
}
```

{{< figure src="/images/cn/2023-05-03-css-display-and-position/grid-align-self-start.svg" middle-max-width="60%" large-max-width="40%" >}}

```css
.item-a {
  align-self: end;
}
```

{{< figure src="/images/cn/2023-05-03-css-display-and-position/grid-align-self-end.svg" middle-max-width="60%" large-max-width="40%" >}}

```css
.item-a {
  align-self: center;
}
```

{{< figure src="/images/cn/2023-05-03-css-display-and-position/grid-align-self-center.svg" middle-max-width="60%" large-max-width="40%" >}}

#### place-self

`place-self` 可以在单次声明中同时设置 `align-self` 和 `justify-self`。

- `auto`：默认对齐方式。
- `<align-self> / <justify-self>`：省略第二个值则将第一个值分配给两个属性。

```css
.item-a {
  place-self: center;
}
```

{{< figure src="/images/cn/2023-05-03-css-display-and-position/grid-place-self-center.svg" middle-max-width="60%" large-max-width="40%" >}}

```css
.item-a {
  place-self: center stretch;
}
```

{{< figure src="/images/cn/2023-05-03-css-display-and-position/grid-place-self-center-stretch.svg" middle-max-width="60%" large-max-width="40%" >}}

# 定位

{{% admonition %}}
本节内容主要参考自：[定位技术](https://developer.mozilla.org/zh-CN/docs/Learn/CSS/CSS_layout/Introduction#%E5%AE%9A%E4%BD%8D%E6%8A%80%E6%9C%AF)
{{% /admonition %}}

定位允许我们将一个元素放置在网页的指定位置上。定位并非是一种用来做主要布局的方式，而是一种用于微调布局的手段。通过 `position` 属性在特定的布局中修改元素的定位方式，该属性有 `static`、`relative`、`fixed`、`absolute` 和 `sticky` 共 5 种可选值。

为了展示不同 `position` 的效果，在此采用相同的 HTML 进行比较：

```html
<h1>XXX 定位</h1>

<p>这是一个基本块元素。</p>
<p class="position">这是一个基本块元素。</p>
<p>这是一个基本块元素。</p>
```

默认样式为：

```css
body {
  width: 400px;
  margin: 0 auto;
}

h1 {
  text-align: center;
}
  
p {
  margin: 10px;
  padding: 10px;
  background-color: #916cad;
  border: 2px #523874 solid;
  border-radius: 3px;
}
```

## 静态定位

**静态定位（`static`）** 是 `position` 属性的 **默认值**，它表示将元素放置在文档布局流的默认位置上。

静态定位样式为：

```css
.position {
  position: static;
}
```

渲染效果如下：

<iframe height="300" width="100%" style="background: #ffffff; border: 1px solid var(--code-border); border-radius: 3px;" src="/codes/cn/2023-05-03-css-display-and-position/static-position.html"></iframe>

## 相对定位

**相对定位（`relative`）** 表示相对于 **静态定位** 的默认位置进行偏移，其需要搭配 `top`、`bottom`、`left` 和 `right` 四个属性使用。

相对定位样式为：

```css
.position {
  position: relative;
  top: 30px;
  left: 30px;
  background-color: #c7fba5cc;
  border: 2px #adf182cc solid;
}
```

渲染效果如下：

<iframe height="300" width="100%" style="background: #ffffff; border: 1px solid var(--code-border); border-radius: 3px;" src="/codes/cn/2023-05-03-css-display-and-position/relative-position.html"></iframe>

## 绝对定位

**绝对定位（`absolute`）** 表示相对于 **上级元素** 的位置进行偏移，其需要搭配 `top`、`bottom`、`left` 和 `right` 四个属性使用。绝对定位的定位基点不能为 `static` 定位，否则定位基点将变成网页根元素 `html`。

绝对定位样式为：

```css
.position {
  position: absolute;
  top: 30px;
  left: 30px;
  background-color: #c7fba5cc;
  border: 2px #adf182cc solid;
}
```

渲染效果如下：

<iframe height="300" width="100%" style="background: #ffffff; border: 1px solid var(--code-border); border-radius: 3px;" src="/codes/cn/2023-05-03-css-display-and-position/absolute-position.html"></iframe>

## 固定定位

**固定定位（`fixed`）** 表示相对于 **视窗（viewport，即浏览器窗口）** 进行偏移，其需要搭配 `top`、`bottom`、`left` 和 `right` 四个属性使用。利用固定定位可以实现元素位置不随页面滚动而发生变化。

为了演示固定定位，修改 HTML 代码如下：

```html
<h1>固定定位</h1>

<p>这是一个基本块元素。</p>
<p class="position">固定</p>
<p>这是一个基本块元素。</p>
<p>这是一个基本块元素。</p>
<p>这是一个基本块元素。</p>
<p>这是一个基本块元素。</p>
<p>这是一个基本块元素。</p>
```

固定定位样式为：

```css
.position {
  position: fixed;
  top: 30px;
  left: 30px;
  background-color: #c7fba5cc;
  border: 2px #adf182cc solid;
}
```

渲染效果如下：

<iframe height="300" width="100%" style="background: #ffffff; border: 1px solid var(--code-border); border-radius: 3px;" src="/codes/cn/2023-05-03-css-display-and-position/fixed-position.html"></iframe>

## 粘性定位

**粘性定位（`sticky`）** 可以理解为 **静态定位（`static`）** 和 **固定定位（`fixed`）** 的 **混合**。当指定一个元素的 `position` 属性为 `sticky` 后，它会在正常布局流中滚动，直至它出现在设定的相对于容器的位置，此时它会停止滚动，表现为固定定位。

为了演示粘性定位，修改 HTML 代码如下：

```html
<h1>粘性定位</h1>

<p>这是一个基本块元素。</p>
<p class="position">这是一个粘性定位元素。</p>
<p>这是一个基本块元素。</p>
<p>这是一个基本块元素。</p>
<p>这是一个基本块元素。</p>
<p>这是一个基本块元素。</p>
<p>这是一个基本块元素。</p>
<p>这是一个基本块元素。</p>
<p>这是一个基本块元素。</p>
```

粘性定位样式为：

```css
.position {
  position: sticky;
  top: 30px;
  left: 30px;
  background-color: #c7fba5cc;
  border: 2px #adf182cc solid;
}
```

渲染效果如下：

<iframe height="300" width="100%" style="background: #ffffff; border: 1px solid var(--code-border); border-radius: 3px;" src="/codes/cn/2023-05-03-css-display-and-position/sticky-position.html"></iframe>
