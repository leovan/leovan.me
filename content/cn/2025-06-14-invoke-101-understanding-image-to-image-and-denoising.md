---
title: '理解图像到图像和降噪过程'
subtitle: 'Invoke AI 101 教程'
author: 范叶亮
date: '2025-06-14'
slug: invoke-101-understanding-image-to-image-and-denoising
categories:
  - Tech101
  - AI
  - 计算机视觉
tags:
  - Invoke
  - 图片生成
  - 图像到图像
  - image to image
  - 文本到图像
  - text to image
  - 降噪
  - denoising
---

{{% admonition type="tip" %}}
本节将介绍「 [图像到图像](https://getimg.ai/guides/guide-to-image-to-image)」和「降噪」两个重要概念，帮助大家更好的理解 Invoke 中的画布是如何工作的，或者说生成式 AI 图片生成是如何工作的。
{{% /admonition %}}

{{< tab id="video" labels-position="center" >}}

{{% tab-item label="<i class='icon icon-bilibili'></i> Bilibili" %}}
{{< bilibili bvid="BV1s484zyE9S" >}}
{{% /tab-item %}}

{{% tab-item label="<i class='icon icon-youtube'></i> YouTube" %}}
{{< youtube id="BsIyJSqnGEc" >}}
{{% /tab-item %}}

{{< /tab >}}

在之前的图像生成示例中，单击 <button>Invoke</button> 按钮后，整个图像生成过程会从一张静态噪声图像开始，模型会将噪声逐步转化为最终图片，整个过程如下图所示：

{{< flex >}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-06-14-invoke-101-understanding-image-to-image-and-denoising/dog-1.avif" >}}
{{% /flex-item %}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-06-14-invoke-101-understanding-image-to-image-and-denoising/dog-2.avif" >}}
{{% /flex-item %}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-06-14-invoke-101-understanding-image-to-image-and-denoising/dog-3.avif" >}}
{{% /flex-item %}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-06-14-invoke-101-understanding-image-to-image-and-denoising/dog-4.avif" >}}
{{% /flex-item %}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-06-14-invoke-101-understanding-image-to-image-and-denoising/dog-5.avif" >}}
{{% /flex-item %}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-06-14-invoke-101-understanding-image-to-image-and-denoising/dog-6.avif" >}}
{{% /flex-item %}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-06-14-invoke-101-understanding-image-to-image-and-denoising/dog-7.avif" >}}
{{% /flex-item %}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-06-14-invoke-101-understanding-image-to-image-and-denoising/dog-8.avif" >}}
{{% /flex-item %}}

{{< /flex >}}

将噪声图像转化成最终图片的过程称之为降噪（Denoising）。

将示例图片拖拽至画布上，选择 New Raster Layer，示例图片如下 [^demo-image]：

{{< figure src="/images/cn/2025-06-14-invoke-101-understanding-image-to-image-and-denoising/cup.jpg" title="示例图片" large-max-width="50%" middle-max-width="50%" >}}

在图层中，可以找到 Denosing Strength 参数：

{{< figure src="/images/cn/2025-06-14-invoke-101-understanding-image-to-image-and-denoising/denoising-strength.avif" title="Denoising Strength" >}}

Denosing Strength 用于控制初始图片或 Raster Layer 在降噪过程中影响最终输出图片的程度。设置较高的值会使降噪过程从一个具有更多噪声数据的图片开始，此时模型会具有更高的自由度根据提示词生成新的内容。

图像到图像和文本到图像的最主要区别在于图像生成的起点。文本到图像时从纯噪声开始，并根据提示词逐步细化。图像到图像则会根据 Denosing Strength 跳过前面的一些步骤，使用提供的图像作为起点。

以 `a porcelain teacup on a table` 作为提示词，选择 `Photography (General)` 作为提示词模板，分别将 Denosing Strength 设置为 0.2 和 0.8，生成的图片和原始图片对比如下：

{{< flex >}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-06-14-invoke-101-understanding-image-to-image-and-denoising/cup.jpg" title="原始图片" >}}
{{% /flex-item %}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-06-14-invoke-101-understanding-image-to-image-and-denoising/denoising-strength-low.avif" title="低 Denosing Strength" >}}
{{% /flex-item %}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-06-14-invoke-101-understanding-image-to-image-and-denoising/denoising-strength-high.avif" title="高 Denosing Strength" >}}
{{% /flex-item %}}

{{< /flex >}}

可以看出，较高 Denosing Strength 值可以让模型具有更高的自由度生成图片，而设置较低的 Denosing Strength 值时生成的图片仅有少量的变化。除此之外，在控制层和参考图片上也可以设置 Denosing Strength 来取得不同的效果。

[^demo-image]: <https://pixabay.com/zh/photos/teacup-ceramic-table-room-curtain-2605474/>
