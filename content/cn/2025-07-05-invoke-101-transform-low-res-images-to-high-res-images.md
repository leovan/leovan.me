---
title: '提升图片分辨率和质量'
subtitle: 'Invoke AI 101 教程'
author: 范叶亮
date: '2025-07-05'
slug: invoke-101-transform-low-res-images-to-high-res-images
categories:
  - Tech101
  - AI
  - 计算机视觉
tags:
  - Invoke
  - 图片生成
  - 提升分辨率
  - 画质提升
  - Upscaling
  - SwinIR
  - 创意性
  - Creativity
  - 结构
  - Structure
---

{{% admonition type="tip" %}}
本节将介绍如何将一张低分辨率的图片转换成一张高分辨率高质量的图片。
{{% /admonition %}}

{{< tab id="video" labels-position="center" >}}

{{% tab-item label="<i class='icon icon-bilibili'></i> Bilibili" %}}
{{< bilibili bvid="BV1io8dz2EQW" >}}
{{% /tab-item %}}

{{% tab-item label="<i class='icon icon-youtube'></i> YouTube" %}}
{{< youtube id="5jRQh_fpLvM" >}}
{{% /tab-item %}}

{{< /tab >}}

为了对比提升分辨率后的图片质量，我们先下载一张原始的高清图片 [^image-source]，通过 ImageMagick 命令将其转换为一个低分辨率低质量的图片，未来基于这张转换后的图片进行分辨率和质量的提升，再与原始图片进行对比验证提升的效果。

```shell
magick toucan-raw.jpg -resize 512x -quality 10 toucan-low-res.jpg
```

{{< flex justify-content="space-evenly" >}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-07-05-invoke-101-transform-low-res-images-to-high-res-images/toucan-raw.jpg" title="原始图片" large-max-width="400px" middle-max-width="320px" small-max-width="320px" >}}
{{% /flex-item %}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-07-05-invoke-101-transform-low-res-images-to-high-res-images/toucan-low-res.jpg" title="低分辨率图片" large-max-width="400px" middle-max-width="320px" small-max-width="320px" >}}
{{% /flex-item %}}

{{< /flex >}}

[^image-source]: 图片来源：<https://pixabay.com/zh/photos/toucan-nature-bird-beak-costa-rica-9603854/>

## 基础操作

单击左侧 <span style="vertical-align: middle;"><svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 256 256" aria-hidden="true" focusable="false" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M140,88a12,12,0,0,1,12-12h32a12,12,0,0,1,12,12v32a12,12,0,0,1-24,0V100H152A12,12,0,0,1,140,88ZM72,180h32a12,12,0,0,0,0-24H84V136a12,12,0,0,0-24,0v32A12,12,0,0,0,72,180ZM236,56V200a20,20,0,0,1-20,20H40a20,20,0,0,1-20-20V56A20,20,0,0,1,40,36H216A20,20,0,0,1,236,56Zm-24,4H44V196H212Z"></path></svg></span> 按钮进入 Upscaling 界面，将上面生成的低分辨率图片拖入 Assets 中，之后再拖入到 Upscale 面板的图片区域。

{{< figure src="/images/cn/2025-07-05-invoke-101-transform-low-res-images-to-high-res-images/upscaling-basic-before-invoke.avif" title="基础操作" >}}

安装的 SDXL 模型包中包含一个 SwinIR 分辨率提升模型。选择该模型并添加如下的正向和负向提示词：

{{< highlight title="正向提示词" >}}
a vibrant bird, detailed, a high contrast, inviting warmth, sunlit elements, dynamic composition, 35mm lens, 1/2.8, environmental context, detailed har photography
{{< /highlight >}}

{{< highlight title="负向提示词" >}}
blurry, out of focus, over saturated, text+++
{{< /highlight >}}

将 `Creativity` 和 `Structure` 保持默认值 `0`，单击 <button>Invoke</button> 按钮生成图片。生成完毕后在 Assets 中的低分辨图片上右键，单击 <span style="vertical-align: middle;"><svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 256 256" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M160,88a16,16,0,1,1,16,16A16,16,0,0,1,160,88Zm76-32V160a20,20,0,0,1-20,20H204v20a20,20,0,0,1-20,20H40a20,20,0,0,1-20-20V88A20,20,0,0,1,40,68H60V56A20,20,0,0,1,80,36H216A20,20,0,0,1,236,56ZM180,180H80a20,20,0,0,1-20-20V92H44V196H180Zm-21.66-24L124,121.66,89.66,156ZM212,60H84v67.72l25.86-25.86a20,20,0,0,1,28.28,0L192.28,156H212Z"></path></svg></span> 按钮选择进行对比，单击 Images 选项卡回到新生成的图片页面查看对比效果。

{{< figure src="/images/cn/2025-07-05-invoke-101-transform-low-res-images-to-high-res-images/upscaling-basic-compare.avif" title="对比图片" >}}

从如下的对比中可以看出，生成的图片具有更多的细节，这样我们就可以在更高的分辨率下获得更加清晰锐利的图像。

{{< image-compare show-labels=true large-max-width="50%" middle-max-width="50%" small-max-width="100%" label-before="低分辨率" label-after="高分辨率" image-before="/images/cn/2025-07-05-invoke-101-transform-low-res-images-to-high-res-images/toucan-low-res.jpg" image-after="/images/cn/2025-07-05-invoke-101-transform-low-res-images-to-high-res-images/upscaling-basic.avif" >}}

单击画布上方的 `Exit Compare` 退出对比，在生成的图片上右键，单击 <span style="vertical-align: middle;"><svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 256 256" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M228,104a12,12,0,0,1-24,0V69l-59.51,59.51a12,12,0,0,1-17-17L187,52H152a12,12,0,0,1,0-24h64a12,12,0,0,1,12,12Zm-44,24a12,12,0,0,0-12,12v64H52V84h64a12,12,0,0,0,0-24H48A20,20,0,0,0,28,80V208a20,20,0,0,0,20,20H176a20,20,0,0,0,20-20V140A12,12,0,0,0,184,128Z"></path></svg></span> 按钮可以在新窗口中打开图片，之后则可以使用鼠标进行放大来观察图片细节。

## 进阶操作

除了基础的分辨率提升以外，还有一些高级选项可以用来控制分辨率提升后的图片与原始图片的相似程度以及在提升分辨率过程中的创意性。`Creativity` 参数用于设置提示词控制图像生成的创意性，从而控制与原始图像的差异程度，值越大表示越具有创意性。`Structure` 参数用于确保分辨率提升过程中图像中的元素与原始图像中的元素的形状和位置匹配，值越大表示越会严格遵守原始图片的结构。

{{< figure src="/images/cn/2025-07-05-invoke-101-transform-low-res-images-to-high-res-images/upscale-panel.avif" title="Upscale" large-max-width="366px" middle-max-width="366px" small-max-width="366px" >}}

同时也可以调整生成的模型及其相关参数，例如：`Scheduler` 和 `CFG Scale` 等。

## 风格调整

如果在提升分辨率的过程中还希望调整图片的风格，你可以尝试使用不同的提示词，例如下面是一个绘画风格的提示词：

```plain
a painting of a vibrant bird, oil painting, deep impasto, glazed brushstrokes
```

我们适当增加 `Creativity` 的值到 `8`，减少 `Structure` 的值到 `-4`，这样可以给到模型更多的自由度重新构思一些细节。最后我们来综合对比原始图片、低分辨率图片、提升分辨率后的图片以及调整风格的图片：

至此，我们 Invoke AI 101 系列的 6 节课程就全部结束了，希望大家能够通过这 6 节课程对 Invoke AI 的功能有一个基础的认知。也期待大家能够进一步探索 Invoke AI 的高级功能，去创造更多自己喜欢的图片。

{{< flex justify-content="space-evenly" >}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-07-05-invoke-101-transform-low-res-images-to-high-res-images/toucan-raw.jpg" title="原始图片" large-max-width="400px" middle-max-width="320px" small-max-width="320px" >}}
{{% /flex-item %}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-07-05-invoke-101-transform-low-res-images-to-high-res-images/toucan-low-res.jpg" title="低分辨率图片" large-max-width="400px" middle-max-width="320px" small-max-width="320px" >}}
{{% /flex-item %}}

{{< /flex >}}

{{< flex justify-content="space-evenly" >}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-07-05-invoke-101-transform-low-res-images-to-high-res-images/upscaling-basic.avif" title="提升分辨率图片" large-max-width="400px" middle-max-width="320px" small-max-width="320px" >}}
{{% /flex-item %}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-07-05-invoke-101-transform-low-res-images-to-high-res-images/upscaling-change-style.avif" title="提升分辨率图片（风格调整）" large-max-width="400px" middle-max-width="320px" small-max-width="320px" >}}
{{% /flex-item %}}

{{< /flex >}}
