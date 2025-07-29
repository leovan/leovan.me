---
title: '使用控制层和指示控制图片的生成'
subtitle: 'Invoke AI 101 教程'
author: 范叶亮
date: '2025-06-07'
slug: invoke-101-using-control-layers-and-reference-guides
show_toc: true
toc_depth: 3
categories:
  - Tech101
  - AI
  - 计算机视觉
tags:
  - Invoke
  - 图片生成
  - SD
  - Stable Diffusion
  - Flux
  - Juggernaut XL
  - 控制网络
  - ControlNet
  - Contour Detection
  - scribble
  - 深度图
  - Depth Map
  - Hard Edge Detection
  - canny
  - Pose Detection
  - openpose
  - Soft Edge Detection
  - softedge
  - Tile
  - 控制层
  - Control Layer
  - 参考图片
  - Reference Image
  - 局部指示
  - Regional Guidance
---

{{% admonition type="tip" %}}
本节将介绍如何使用控制层和指示来精确控制图片的生成。
{{% /admonition %}}

{{< tab id="video" labels-position="center" >}}

{{% tab-item label="<i class='icon icon-bilibili'></i> Bilibili" %}}
{{< bilibili bvid="BV1hjgtzrEeS" >}}
{{% /tab-item %}}

{{% tab-item label="<i class='icon icon-youtube'></i> YouTube" %}}
{{< youtube id="dtojbQayPUU" >}}
{{% /tab-item %}}

{{< /tab >}}

# 控制网络

控制层通常用作控制网络（[ControlNet](https://getimg.ai/guides/guide-to-controlnet)）在图片生成中以线或结构的形式来提供参考。在 SDXL 中，常用的预训练控制网络有 [^control-net]：

## Contour Detection (scribble)

Scribble 模型可以根据输入的图片生成线条画，处理后的图片作为原始图片的简化版本可以精准的捕捉图片的轮廓。

{{< flex >}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-06-07-invoke-101-using-control-layers-and-reference-guides/scribble-input.avif" title="输入" >}}
{{% /flex-item %}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-06-07-invoke-101-using-control-layers-and-reference-guides/scribble-analyzed.avif" title="分析" >}}
{{% /flex-item %}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-06-07-invoke-101-using-control-layers-and-reference-guides/scribble-generation.avif" title="生成" >}}
{{% /flex-item %}}

{{< /flex >}}

## Depth Map

Depth Map 可以生成图片的深度图，在图片生成中模拟深度效果，从而创建更加逼真的 3D 图片。

{{< flex >}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-06-07-invoke-101-using-control-layers-and-reference-guides/depth-map-input.avif" title="输入" >}}
{{% /flex-item %}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-06-07-invoke-101-using-control-layers-and-reference-guides/depth-map-analyzed.avif" title="分析" >}}
{{% /flex-item %}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-06-07-invoke-101-using-control-layers-and-reference-guides/depth-map-generation.avif" title="生成" >}}
{{% /flex-item %}}

{{< /flex >}}

## Hard Edge Detection (canny)

Canny 边缘检测的原理是通过寻找强度突变来识别图片中的边缘。它能够准确的检测边缘并减少噪声和伪边缘，通过降低阈值可以识别更多的信息。采用 Canny 模型时，将会生成与检测到的边缘匹配的图片。

{{< flex >}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-06-07-invoke-101-using-control-layers-and-reference-guides/canny-input.avif" title="输入" >}}
{{% /flex-item %}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-06-07-invoke-101-using-control-layers-and-reference-guides/canny-analyzed.avif" title="分析" >}}
{{% /flex-item %}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-06-07-invoke-101-using-control-layers-and-reference-guides/canny-generation.avif" title="生成" >}}
{{% /flex-item %}}

{{< /flex >}}

## Pose Detection (openpose)

Openpose 模型可以检测身体、手部、面部等多个部位的关键点，在生成图片时可以控制人体的姿态。

{{< flex >}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-06-07-invoke-101-using-control-layers-and-reference-guides/openpose-input.avif" title="输入" >}}
{{% /flex-item %}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-06-07-invoke-101-using-control-layers-and-reference-guides/openpose-analyzed.avif" title="分析" >}}
{{% /flex-item %}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-06-07-invoke-101-using-control-layers-and-reference-guides/openpose-generation.avif" title="生成" >}}
{{% /flex-item %}}

{{< /flex >}}

## Soft Edge Detection (softedge)

Softedge 模型与 Scribble 模型类似，处理后的图片作为原始图片的简化版本仅保留形状的柔和边缘和一些浅阴影。

## Tile

Tile 模型的主要功能可以归结为如下两点：

1. 可以重新解读图片中的特定细节，并创建全新的元素。
2. 当全局指令与图片的局部或特定部分存在差异时，可以忽略这些指令。在这种情况下，它可以使用局部上下文指示图片生成。

Tile 模型可以作为增强图片质量和细节的工具。如果在图片中存在一些不足的地方，例如调整图片大小导致的模糊，Tile 模型可以有效的消除此类问题从而获得更加清晰锐利的图片。此外 Tile 模型还可以添加更多细节，从而提升图片的整体质量。

# 控制层

在图层中单击 `+ Control Layer` 添加控制层，或者在图片库中将图片拖拽至画布上，选择 `New Control Layer`。

{{< figure src="/images/cn/2025-06-07-invoke-101-using-control-layers-and-reference-guides/invoke-drag-image-new-control-layer.avif" title="创建控制层" >}}

示例图片及其生成的提示词如下：

{{< flex align-items="flex-start" >}}

{{% flex-item flex-grow="1" %}}
{{< figure src="/images/cn/2025-06-07-invoke-101-using-control-layers-and-reference-guides/control-layer-input.png" title="示例图片" large-max-width="256px" middle-max-width="256px" >}}
{{% /flex-item %}}

{{% flex-item flex-grow="1" %}}

**正向提示词**：

```plain
futuristic terraced structure built into a mountain at dusk, twilight hues, lush greenery illuminated by soft glowing lights, multiple levels, pathways, vast mountain range, distant winding roads, glowing city lights below, towering otherworldly rock formations, dreamy sky with soft clouds
```

**负向提示词**：

```plain
painting, digital art, sketch, blurry
```

{{% /flex-item %}}

{{< /flex >}}

{{< figure src="/images/cn/2025-06-07-invoke-101-using-control-layers-and-reference-guides/invoke-control-layer.avif" title="控制层" >}}

本教程以 Hard Edge Detection (canny) 模型为例，单击 `Filter` 中的 `Advanced` 可以进行更多的调整：

{{< flex >}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-06-07-invoke-101-using-control-layers-and-reference-guides/control-layer-canny-filter-default.avif" title="Canny Filter - Default" >}}
{{% /flex-item %}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-06-07-invoke-101-using-control-layers-and-reference-guides/control-layer-canny-filter-advanced.avif" title="Canny Filter - Advanced" >}}
{{% /flex-item %}}

{{< /flex >}}

调整完毕各项参数后，单击 `Apply` 即可生成控制图片。

{{< figure src="/images/cn/2025-06-07-invoke-101-using-control-layers-and-reference-guides/invoke-control-layer-canny.avif" title="控制图片" >}}

控制图片提供的线条可以为图片生成提供参考。在画布中，可以使用 <span style="vertical-align: middle;"><svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 256 256" aria-hidden="true" focusable="false" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M236,32a12,12,0,0,0-12-12c-44.78,0-90,48.54-115.9,82a64,64,0,0,0-80,62c0,12-3.1,22.71-9.23,31.76A43,43,0,0,1,9.4,206.05a11.88,11.88,0,0,0-4.91,13.38A12.07,12.07,0,0,0,16.11,228h76A64,64,0,0,0,154,148C187.49,122.05,236,76.8,236,32ZM209.62,46.39c-4,12.92-13.15,27.49-26.92,42.91-3,3.39-6.16,6.7-9.35,9.89a104.31,104.31,0,0,0-16.5-16.51c3.19-3.19,6.49-6.32,9.88-9.35C182.15,59.55,196.71,50.43,209.62,46.39ZM92.07,204H42a80.17,80.17,0,0,0,10.14-40,40,40,0,1,1,40,40Zm38.18-91.32c3.12-3.93,6.55-8.09,10.23-12.35a80.52,80.52,0,0,1,15.23,15.24c-4.26,3.68-8.42,7.11-12.35,10.23A64.43,64.43,0,0,0,130.25,112.68Z"></path></svg></span>、<span style="vertical-align: middle;"><svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 256 256" aria-hidden="true" focusable="false" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M216,204H141l86.84-86.84a28,28,0,0,0,0-39.6L186.43,36.19a28,28,0,0,0-39.6,0L28.19,154.82a28,28,0,0,0,0,39.6l30.06,30.07A12,12,0,0,0,66.74,228H216a12,12,0,0,0,0-24ZM163.8,53.16a4,4,0,0,1,5.66,0l41.38,41.38a4,4,0,0,1,0,5.65L160,151l-47-47ZM71.71,204,45.16,177.45a4,4,0,0,1,0-5.65L96,121l47,47-36,36Z"></path></svg></span> 和 <span style="vertical-align: middle;"><svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 256 256" aria-hidden="true" focusable="false" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M216,36H40A20,20,0,0,0,20,56V200a20,20,0,0,0,20,20H216a20,20,0,0,0,20-20V56A20,20,0,0,0,216,36Zm-4,160H44V60H212Z"></path></svg></span> 等工具对控制图片进行添加或删除等微调操作。接下来对控制层进行设置：

1. `Weight`：用于设置控制图层在图片生成过程中的权重，值越大则图片生成时越会严格遵守控制线条。
2. `Begin/End %`：用于设置在图片生成过程中在何时使用控制图层，将其设置为 0% 至 100% 表示从图片生成开始至结束一直使用控制图层。调整开始和结束的百分比可以给到模型更多的灵活性，从而获得更好的生成图片。
3. `Control Mode`：包含多种控制模式用于调节控制层的相关性（[CFG scale](https://getimg.ai/guides/interactive-guide-to-stable-diffusion-guidance-scale-parameter)）：
    - `Balanced`：提示词和控制层同等重要。
    - `Prompt`：提示词更加重要。
    - `Control`：控制层更加重要。

不同的 `Control Mode` 的生成示例如下 [^control-mode-examples]：

{{< flex >}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-06-07-invoke-101-using-control-layers-and-reference-guides/control-mode-input.avif" title="输入" >}}
{{% /flex-item %}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-06-07-invoke-101-using-control-layers-and-reference-guides/control-mode-balanced.avif" title="Balanced" >}}
{{% /flex-item %}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-06-07-invoke-101-using-control-layers-and-reference-guides/control-mode-prompt.avif" title="Prompt" >}}
{{% /flex-item %}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-06-07-invoke-101-using-control-layers-and-reference-guides/control-mode-control.avif" title="Control" >}}
{{% /flex-item %}}

{{< /flex >}}

单击 <button>Invoke</button> 开始生成图片。此时可以看到模型在控制线条的指示下开始生成图片。

{{< figure src="/images/cn/2025-06-07-invoke-101-using-control-layers-and-reference-guides/invoke-control-layer-generation.avif" title="生成图片" >}}

由于将结束百分比设置为了 70%，生成的图片也具有一定的灵活创意。单击 <span style="vertical-align: middle;"><svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 256 256" aria-hidden="true" focusable="false" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M232.49,80.49l-128,128a12,12,0,0,1-17,0l-56-56a12,12,0,1,1,17-17L96,183,215.51,63.51a12,12,0,0,1,17,17Z"></path></svg></span> 会将生成的图片添加到 `Raster Layer`。单击 <span style="vertical-align: middle;"><svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 256 256" aria-hidden="true" focusable="false" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M222.14,69.17,186.83,33.86A19.86,19.86,0,0,0,172.69,28H48A20,20,0,0,0,28,48V208a20,20,0,0,0,20,20H208a20,20,0,0,0,20-20V83.31A19.86,19.86,0,0,0,222.14,69.17ZM164,204H92V160h72Zm40,0H188V156a20,20,0,0,0-20-20H88a20,20,0,0,0-20,20v48H52V52H171l33,33ZM164,84a12,12,0,0,1-12,12H96a12,12,0,0,1,0-24h56A12,12,0,0,1,164,84Z"></path></svg></span> 可以将画布保存到图片库中。新生成的图片和用于生成控制层的图片对比如下：

{{< flex >}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-06-07-invoke-101-using-control-layers-and-reference-guides/control-layer-generation.avif" title="新生成的图片" >}}
{{% /flex-item %}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-06-07-invoke-101-using-control-layers-and-reference-guides/control-layer-input.png" title="生成控制层的图片" >}}
{{% /flex-item %}}

{{< /flex >}}

# 参考图片

接下来我们将添加一个参考图片，也称为 [IP Adapter](https://getimg.ai/guides/guide-to-ip-adapters)。模型会根据参考图片的风格和结构来生成图片。首先将参考图片添加到图片库，本教程中使用的图片如下 [^reference-image]：

{{< figure src="/images/cn/2025-06-07-invoke-101-using-control-layers-and-reference-guides/reference-image.jpg" title="参考图片" >}}

将图片拖拽至左侧 `Reference Image` 上。

{{< figure src="/images/cn/2025-06-07-invoke-101-using-control-layers-and-reference-guides/invoke-drag-image-reference-image.avif" title="创建参考图片" >}}

在左侧将会创建一个 `Reference Image`，并可以对其进行相关设置。

{{< figure src="/images/cn/2025-06-07-invoke-101-using-control-layers-and-reference-guides/reference-image-1.avif" title="Global Reference Image" large-max-width="50%" middle-max-width="50%" >}}

1. 模型：在安装 SDXL 相关模型的情况下，选择 `Standard Reference (IP Adapter ViT-H)` 模型，这里可以选择 `ViT-H`、`ViT-G` 和 `ViT-L` 多种变种。
2. `Mode`：`Style and Composition` 表示参考样式和结构，`Style` 表示仅参考样式，`Composition` 表示仅参考结构。
3. `Weight`：类比控制层。
4. `Begin/End %`：类比控制层。

在本教程中，将参考图片的 `Weight` 设置为 0.7，将结束百分比设置为 70%，从而给到模型更多的自由度。删除之前生成的 `Raster Layer`，单击 <button>Invoke</button> 开始生成图片。应用参考图片生成的图片和之前生成的图片对比如下：

{{< flex >}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-06-07-invoke-101-using-control-layers-and-reference-guides/reference-image-generation.avif" title="应用参考图片生成的图片" >}}
{{% /flex-item %}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-06-07-invoke-101-using-control-layers-and-reference-guides/control-layer-generation.avif" title="之前生成的图片" >}}
{{% /flex-item %}}

{{< /flex >}}

可以看出新生成的图片在遵循控制层的前提下同时应用了参考图片的白色风格。

# 局部指示

在新生成的图片中，可以看到左侧背景中的山峰也被应用了参考图片中的建筑风格。为了实现更精确的控制，可以选择局部参考图片，将图片拖拽至画布上，选择 `New Regional Reference Image`。

{{< figure src="/images/cn/2025-06-07-invoke-101-using-control-layers-and-reference-guides/invoke-drag-image-new-regional-reference-image.avif" title="创建局部参考图片" >}}

在画布上选择 <span style="vertical-align: middle;"><svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 256 256" aria-hidden="true" focusable="false" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M236,32a12,12,0,0,0-12-12c-44.78,0-90,48.54-115.9,82a64,64,0,0,0-80,62c0,12-3.1,22.71-9.23,31.76A43,43,0,0,1,9.4,206.05a11.88,11.88,0,0,0-4.91,13.38A12.07,12.07,0,0,0,16.11,228h76A64,64,0,0,0,154,148C187.49,122.05,236,76.8,236,32ZM209.62,46.39c-4,12.92-13.15,27.49-26.92,42.91-3,3.39-6.16,6.7-9.35,9.89a104.31,104.31,0,0,0-16.5-16.51c3.19-3.19,6.49-6.32,9.88-9.35C182.15,59.55,196.71,50.43,209.62,46.39ZM92.07,204H42a80.17,80.17,0,0,0,10.14-40,40,40,0,1,1,40,40Zm38.18-91.32c3.12-3.93,6.55-8.09,10.23-12.35a80.52,80.52,0,0,1,15.23,15.24c-4.26,3.68-8.42,7.11-12.35,10.23A64.43,64.43,0,0,0,130.25,112.68Z"></path></svg></span>，设置合适的笔刷宽度，在画布上勾勒出需要应用参考的区域，这里我们仅勾勒出建筑所在的区域。

{{< figure src="/images/cn/2025-06-07-invoke-101-using-control-layers-and-reference-guides/invoke-regional-reference-image-region.avif" title="勾勒需要应用参考的区域" >}}

单击 <button>Invoke</button> 开始生成图片。应用局部参考图片生成的图片和应用参考图片生成的图片对比如下：

{{< flex >}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-06-07-invoke-101-using-control-layers-and-reference-guides/regional-reference-image-generation.avif" title="应用局部参考图片生成的图片" >}}
{{% /flex-item %}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-06-07-invoke-101-using-control-layers-and-reference-guides/global-reference-image-generation.avif" title="应用参考图片生成的图片" >}}
{{% /flex-item %}}

{{< /flex >}}

可以看出新生成的图片仅在勾勒的区域内与参考图片的白色风格保持了一致，背后的山峰仍根据提示词生成相应的风格。

# 基于文本的指示

除了基于图片的指示以外，还可以创建基于文本的局部指示。在图层中单击 `+`，选择 `Reginal Guidance` 创建局部指示。在画布上选择 <span style="vertical-align: middle;"><svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 256 256" aria-hidden="true" focusable="false" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M236,32a12,12,0,0,0-12-12c-44.78,0-90,48.54-115.9,82a64,64,0,0,0-80,62c0,12-3.1,22.71-9.23,31.76A43,43,0,0,1,9.4,206.05a11.88,11.88,0,0,0-4.91,13.38A12.07,12.07,0,0,0,16.11,228h76A64,64,0,0,0,154,148C187.49,122.05,236,76.8,236,32ZM209.62,46.39c-4,12.92-13.15,27.49-26.92,42.91-3,3.39-6.16,6.7-9.35,9.89a104.31,104.31,0,0,0-16.5-16.51c3.19-3.19,6.49-6.32,9.88-9.35C182.15,59.55,196.71,50.43,209.62,46.39ZM92.07,204H42a80.17,80.17,0,0,0,10.14-40,40,40,0,1,1,40,40Zm38.18-91.32c3.12-3.93,6.55-8.09,10.23-12.35a80.52,80.52,0,0,1,15.23,15.24c-4.26,3.68-8.42,7.11-12.35,10.23A64.43,64.43,0,0,0,130.25,112.68Z"></path></svg></span>，设置合适的笔刷宽度，在画布上勾勒出需要应用参考的区域，这里我们勾勒出建筑后面的一座山峰。在 `Reginal Guidance` 中选择 `+ Prompt` 并添加 `lush greenery` 提示词。

{{< figure src="/images/cn/2025-06-07-invoke-101-using-control-layers-and-reference-guides/invoke-regional-guidance-text-prompt.avif" title="创建局部文本指示" >}}

单击 <button>Invoke</button> 开始生成图片。应用局部基于文本的指示的图片和应用局部参考图片生成的图片对比如下：

{{< flex >}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-06-07-invoke-101-using-control-layers-and-reference-guides/regional-guidance-text-prompt-generation.avif" title="应用局部基于文本的指示的图片" >}}
{{% /flex-item %}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-06-07-invoke-101-using-control-layers-and-reference-guides/regional-reference-image-generation.avif" title="应用局部参考图片生成的图片" >}}
{{% /flex-item %}}

{{< /flex >}}

可以看出新生成的图片在勾勒的山峰区域增加了郁郁葱葱的树木。

[^control-net]: <https://support.invoke.ai/support/solutions/articles/151000105880-control-layers>

[^control-mode-examples]: <https://github.com/Mikubill/sd-webui-controlnet>

[^reference-image]: <https://pixabay.com/zh/photos/modern-building-business-district-4428919/>
