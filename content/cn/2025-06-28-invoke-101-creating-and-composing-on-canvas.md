---
title: '使用画布创建和组合生成新的图片'
subtitle: 'Invoke AI 101 教程'
author: 范叶亮
date: '2025-06-28'
slug: invoke-101-creating-and-composing-on-canvas
categories:
  - Tech101
  - AI
  - 计算机视觉
tags:
  - Invoke
  - 图片生成
  - 边界框
  - Bbox
  - 补全
  - out painting
  - infilling
  - 图像到图像
  - Image2Image
  - I2I
  - 修复蒙版
  - Inpaint Mask
---

{{% admonition type="tip" %}}
本节将介绍在使用画布进行创建和组合生成新的图片的过程中使用到的核心工具。
{{% /admonition %}}

{{< tab id="video" labels-position="center" >}}

{{% tab-item label="<i class='icon icon-bilibili'></i> Bilibili" %}}
{{< bilibili bvid="BV1pj8EzJE1q" >}}
{{% /tab-item %}}

{{% tab-item label="<i class='icon icon-youtube'></i> YouTube" %}}
{{< youtube id="w0wd35UUBIQ" >}}
{{% /tab-item %}}

{{< /tab >}}

首先，我们使用 Juggernaut XL v9 模型和如下提示词生成一张基础图片留作备用：

{{< flex align-items="flex-start" >}}

{{% flex-item flex-grow="1" %}}
{{< figure src="/images/cn/2025-06-28-invoke-101-creating-and-composing-on-canvas/base-image.png" title="基础图片" large-max-width="256px" middle-max-width="256px" >}}
{{% /flex-item %}}

{{% flex-item flex-grow="1" %}}

**提示词模板**：

Environment Art

**正向提示词**：

```plain
futuristic terraced structure built into a mountain at dusk, twilight hues, lush greenery illuminated by soft glowing lights, multiple levels, pathways, vast mountain range, distant winding roads, glowing city lights below, towering otherworldly rock formations
```

{{% /flex-item %}}

{{< /flex >}}

为了保证可复现性，在生成这张图片时可以将随机数种子 `Seed` 固定，此处设置为 `42`。

# 边界框

将生成的图片拖入画布并创建一个新的 Raster Layer。在画布上单击 <span style="vertical-align: middle;"><svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 256 256" aria-hidden="true" focusable="false" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M208,100a20,20,0,0,0,20-20V48a20,20,0,0,0-20-20H176a20,20,0,0,0-20,20v4H100V48A20,20,0,0,0,80,28H48A20,20,0,0,0,28,48V80a20,20,0,0,0,20,20h4v56H48a20,20,0,0,0-20,20v32a20,20,0,0,0,20,20H80a20,20,0,0,0,20-20v-4h56v4a20,20,0,0,0,20,20h32a20,20,0,0,0,20-20V176a20,20,0,0,0-20-20h-4V100ZM180,52h24V76H180ZM52,52H76V76H52ZM76,204H52V180H76Zm128,0H180V180h24Zm-24-48h-4a20,20,0,0,0-20,20v4H100v-4a20,20,0,0,0-20-20H76V100h4a20,20,0,0,0,20-20V76h56v4a20,20,0,0,0,20,20h4Z"></path></svg></span> Bbox 按钮，此时图片的周围将显示一个边界框，使用鼠标按住可以拖动边界框的位置，放在边界框的四角可以调整边界框的大小。

将边界框移动到画布的一个完全空白的区域，此时边界框中没有任何 Raster Layer 的内容，单击 <button>Invoke</button> 会生成一张新的图片。

{{< figure src="/images/cn/2025-06-28-invoke-101-creating-and-composing-on-canvas/new-bbox-before-invoke.avif" title="生成前" >}}

{{< figure src="/images/cn/2025-06-28-invoke-101-creating-and-composing-on-canvas/new-bbox-after-invoke.avif" title="生成后" >}}

将边界框移动到画布的一个包含部分 Raster Layer 内容的区域，单击 <button>Invoke</button> 会将空白的部分补全，通常称之为 Out Painting 或 Infilling。

{{< figure src="/images/cn/2025-06-28-invoke-101-creating-and-composing-on-canvas/overlap-bbox-before-invoke.avif" title="生成前" >}}

{{< figure src="/images/cn/2025-06-28-invoke-101-creating-and-composing-on-canvas/overlap-bbox-after-invoke.avif" title="生成后" >}}

如果边界框和 Raster Layer 完全重合，单击 <button>Invoke</button> 将会基于当前 Raster Layer 中的内容重新生成新的图片，通常称之为图像到图像（Image2Image）。

{{< image-compare show-labels=true label-before="生成前" label-after="生成后" image-before="/images/cn/2025-06-28-invoke-101-creating-and-composing-on-canvas/same-bbox-before-invoke.avif" image-after="/images/cn/2025-06-28-invoke-101-creating-and-composing-on-canvas/same-bbox-after-invoke.avif" >}}

# 修复蒙版

修复蒙版（Inpaint Mask）用于控制在边界框中哪些区域会被修改。在图层中单击 `+` 新建一个 Inpaint Mask 图层。单击画布上的 <span style="vertical-align: middle;"><svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 256 256" aria-hidden="true" focusable="false" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M236,32a12,12,0,0,0-12-12c-44.78,0-90,48.54-115.9,82a64,64,0,0,0-80,62c0,12-3.1,22.71-9.23,31.76A43,43,0,0,1,9.4,206.05a11.88,11.88,0,0,0-4.91,13.38A12.07,12.07,0,0,0,16.11,228h76A64,64,0,0,0,154,148C187.49,122.05,236,76.8,236,32ZM209.62,46.39c-4,12.92-13.15,27.49-26.92,42.91-3,3.39-6.16,6.7-9.35,9.89a104.31,104.31,0,0,0-16.5-16.51c3.19-3.19,6.49-6.32,9.88-9.35C182.15,59.55,196.71,50.43,209.62,46.39ZM92.07,204H42a80.17,80.17,0,0,0,10.14-40,40,40,0,1,1,40,40Zm38.18-91.32c3.12-3.93,6.55-8.09,10.23-12.35a80.52,80.52,0,0,1,15.23,15.24c-4.26,3.68-8.42,7.11-12.35,10.23A64.43,64.43,0,0,0,130.25,112.68Z"></path></svg></span> 按钮后，则可以在画布上绘制所需要修改的区域。

{{< figure src="/images/cn/2025-06-28-invoke-101-creating-and-composing-on-canvas/inpaint-mask.avif" title="修复蒙版" >}}

此时可以将边界框进行缩放并移动到关注的指定区域。从左侧的 Image 面板中可以看到边界框的大小为 `320x320`。

{{< figure src="/images/cn/2025-06-28-invoke-101-creating-and-composing-on-canvas/bbox-scaling.avif" title="边界框缩放" large-max-width="366px" middle-max-width="366px" small-max-width="366px" >}}

但在图片生成过程中，仍然会以 `1024x1024` 分辨率进行生成，再通过缩放填充到边界框中。由于先生成了分辨率更高的图片，再进行的缩放，此时生成的部分可以具有更多的细节。这使得我们可以在不牺牲图片质量的前提下，对于图片的复杂区域进行优化。

修复蒙版可以让我们很方便的在图片中添加、移除和改变元素。例如，我们希望在楼梯台阶上添加两个人，可以按照如下步骤进行操作：

1. 将边界框调整到一个合适的大小和位置。
2. 创建一个 Inpaint Mask 图层，使用画笔勾勒出需要修改的区域。
3. 返回 Raster Layer，选择一个颜色，使用画笔勾勒出两个人的大概位置。
4. 在提示词的前面添加 `two people`。
5. 选择一个合适的 Denoising Strength，此处设置为 `0.7`，单击 <button>Invoke</button> 按钮启动生成。

{{< figure src="/images/cn/2025-06-28-invoke-101-creating-and-composing-on-canvas/add-two-people-before-invoke.avif" title="生成前" >}}

{{< figure src="/images/cn/2025-06-28-invoke-101-creating-and-composing-on-canvas/add-two-people-after-invoke.avif" title="生成后" >}}

可以看出，在修复蒙版区域内，根据 Raster Layer 的修改和提示词的修改成功的在台阶上添加了两个人。
