---
title: '探索 AI 模型和概念适配器'
subtitle: 'Invoke AI 101 教程'
author: 范叶亮
date: '2025-06-20'
slug: invoke-101-exploring-ai-models-and-concept-adapters
categories:
  - Tech101
  - AI
  - 计算机视觉
tags:
  - Invoke
  - 图片生成
  - 概念适配器
  - Concept Adapter
  - LoRA
  - Low-Rank Adaptation
  - Animagine XL
  - Anim4gine
  - Stable Diffusion XL
  - SDXL
  - Pixel Art XL
---

{{% admonition type="tip" %}}
本节将介绍图片生成使用到的 AI 模型和概念适配器，我们将讨论提示词和模型的训练方式是如何最终决定提示词对生成图片的有效性。
{{% /admonition %}}

{{< tab id="video" labels-position="center" >}}

{{% tab-item label="<i class='icon icon-bilibili'></i> Bilibili" %}}
{{< bilibili bvid="BV1ii8ezDEQw" >}}
{{% /tab-item %}}

{{% tab-item label="<i class='icon icon-youtube'></i> YouTube" %}}
{{< youtube id="3slNNrfeWBs" >}}
{{% /tab-item %}}

{{< /tab >}}

在图片生成过程中你需要认识到提示词并非在任何时候都是有效的。相同的提示词在一个模型上可以获得很好的生成效果，但在另一个模型上可能无法生成所需的图片。这是由于模型训练所使用的图片和图片的标注文本不同所导致的，因此模型的提示词指南会格外重要。这也是为什么训练自己的模型会更好，因为你完全清楚在训练模型时所使用的标注文本。

在本节教程中我们不会讨论如何训练模型，我们将重点介绍不同模型之间的差异，展示它们如何影响图片生成的过程。除此之外我们还会讨论概念适配器（通常也称为 LoRA），来帮助你更好的理解相关工具。

# 模型比较

进入模型管理页面，在添加模型选项卡处选择 `HuggingFace`，输入 `cagliostrolab/animagine-xl-4.0` 下载 Animagine XL 4.0 模型。Animagine XL 模型与其他的通用模型有很大的不同，Animagine XL 模型是一个动漫主题的 SDXL 微调模型。Animagine XL 4.0 基于 Stable Diffusion XL 1.0 进行重新训练所得，它使用了 840 万张不同来源不同动漫风格的图片进行微调。

Animagine XL 模型使用了一套自有的数据标注方法进行训练，提示词指南如下图所示：

{{< figure src="/images/cn/2025-06-20-invoke-101-exploring-ai-models-and-concept-adapters/animagine-prompting-guide.avif" title="Animagine 提示词指南" >}}

整个提示词包含 6 个部分：

1. 性别。例如：`1girl/1boy/1other`。
2. 角色。例如：`remilia scarlet`。
3. 来源作品。例如：`touhou`。
4. 分级。例如：`safe, sensitive, nsfw, explicit`。
5. 一般标签。
6. 质量标签。例如：`masterpiece, high score, great score, absurdres`。

建议的负向提示词如下：

```plain
lowres, bad anatomy, bad hands, text, error, missing finger, extra digits, fewer digits, cropped, worst quality, low quality, low score, bad score, average score, signature, watermark, username, blurry
```

Animagine XL 模型支持一些特殊的标签用于控制图片生成。质量标签直接影响生成图像的整体质量和细节水平。可用的质量标签有：`masterpiece，best quality，low quality，worst quality`。

{{< flex justify-content="space-evenly" >}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-06-20-invoke-101-exploring-ai-models-and-concept-adapters/animagine-xl-quality-tags-1.avif" title="`masterpiece, best quality`" large-max-width="256px" middle-max-width="256px" small-max-width="256px" >}}
{{% /flex-item %}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-06-20-invoke-101-exploring-ai-models-and-concept-adapters/animagine-xl-quality-tags-2.avif" title="`low quality, worst quality`" large-max-width="256px" middle-max-width="256px" small-max-width="256px" >}}
{{% /flex-item %}}

{{< /flex >}}

与质量标签相比，分数标签可以对图像质量进行更细致的控制。在 Animagine XL 模型中，它们对输出质量的影响更大。可用的分数标签有：`high score，great score，good score，average score，bad score，low score`。

{{< flex justify-content="space-evenly" >}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-06-20-invoke-101-exploring-ai-models-and-concept-adapters/animagine-xl-score-tags-1.avif" title="`high score, great score`" large-max-width="256px" middle-max-width="256px" small-max-width="256px">}}
{{% /flex-item %}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-06-20-invoke-101-exploring-ai-models-and-concept-adapters/animagine-xl-score-tags-2.avif" title="`bad score, low score`" large-max-width="256px" middle-max-width="256px" small-max-width="256px" >}}
{{% /flex-item %}}

{{< /flex >}}

时间标签允许根据特定时间段或年份来控制生成图片的艺术风格。这对于生成具有特定时代艺术特征的图像非常有用。支持的年份标签有：`year 2005，year {n}，year 2025`。

{{< flex justify-content="space-evenly" >}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-06-20-invoke-101-exploring-ai-models-and-concept-adapters/animagine-xl-temporal-tags-1.avif" title="`year 2007`" large-max-width="256px" middle-max-width="256px" small-max-width="256px" >}}
{{% /flex-item %}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-06-20-invoke-101-exploring-ai-models-and-concept-adapters/animagine-xl-temporal-tags-2.avif" title="`year 2023`" large-max-width="256px" middle-max-width="256px" small-max-width="256px" >}}
{{% /flex-item %}}

{{< /flex >}}

利用如下正向和负向提示词分别使用 Animagine XL 4.0 模型和 Juggernaut XL v9 模型生成图片。

{{< highlight title="正向提示词" >}}
1boy, black hoodie, white spiky punk hair, nose piercing, standing against a brick wall, masterpiece, best quality, high score, great score
{{< /highlight >}}

{{< highlight title="负向提示词" >}}
lowres, bad anatomy, bad hands, text, error, missing finger, extra digits, fewer digits, cropped, worst quality, low quality, low score, bad score, average score, signature, watermark, username, blurry
{{< /highlight >}}

同时，为了比较提示词在不同模型中对生成图片的影响，再利用如下正向和负向提示词分别使用 Animagine XL 4.0 模型和 Juggernaut XL v9 模型生成图片。

{{< highlight title="正向提示词" >}}
1boy, black hoodie, white spiky punk hair, nose piercing, standing against a brick wall
{{< /highlight >}}

{{< highlight title="负向提示词" >}}
lowres, bad anatomy, bad hands, text, error, missing finger, extra digits, fewer digits, cropped, signature, watermark, username, blurry
{{< /highlight >}}

为了确保可复现，手动将随机数种子固定设置为 `42`，生成的图片如下：

{{< flex justify-content="space-evenly" >}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-06-20-invoke-101-exploring-ai-models-and-concept-adapters/animagine-xl-4.0-demo.avif" title="Animagine XL 4.0" >}}
{{% /flex-item %}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-06-20-invoke-101-exploring-ai-models-and-concept-adapters/juggernaut-xl-v9-demo.avif" title="Juggernaut XL v9" >}}
{{% /flex-item %}}

{{< /flex >}}

{{< flex justify-content="space-evenly" >}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-06-20-invoke-101-exploring-ai-models-and-concept-adapters/animagine-xl-4.0-demo-less-prompt-keywords.avif" title="Animagine XL 4.0 (删除部分提示词)" >}}
{{% /flex-item %}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-06-20-invoke-101-exploring-ai-models-and-concept-adapters/juggernaut-xl-v9-demo-less-prompt-keywords.avif" title="Juggernaut XL v9 (删除部分提示词)" >}}
{{% /flex-item %}}

{{< /flex >}}

不难看出，从正向和负向提示词中删除关于图片质量的关键词后，Animagine XL 4.0 模型生成的图片有显著的画质降低，而 Juggernaut XL v9 模型生成的图片质量变化并不大。实验说明提示词在不同的模型中效果存在差异，你必须了解模型的训练过程才能更好的使用提示词生成所需的图片。

# 概念适配器

上述问题就导致了概念适配器的诞生，通过自己训练概念适配器，你可以完全掌握对于模型的修改。进入模型管理页面，在添加模型选项卡处选择 `HuggingFace`，输入 `nerijs/pixel-art-xl` 下载 Pixel Art XL 概念适配器。利用如下正向和负向提示词分别使用 Animagine XL 4.0 模型和 Juggernaut XL v9 模型生成图片。

{{< highlight title="正向提示词" >}}
1boy, black hoodie, white spiky punk hair, nose piercing, standing against a brick wall, masterpiece, best quality, high score, great score, pixel art style
{{< /highlight >}}

{{< highlight title="负向提示词" >}}
lowres, bad anatomy, bad hands, text, error, missing finger, extra digits, fewer digits, cropped, worst quality, low quality, low score, bad score, average score, signature, watermark, username, blurry
{{< /highlight >}}

在 `Generation` 中添加概念适配器 `pixel-art-xl` 并启用：

{{< figure src="/images/cn/2025-06-20-invoke-101-exploring-ai-models-and-concept-adapters/concepts-pixel-art-xl.avif" title="概念适配器" large-max-width="480px" middle-max-width="480px" small-max-width="480px" >}}

Pixel Art XL 概念适配器用于生成像素风格的图片，生成的图片如下：

{{< flex justify-content="space-evenly" >}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-06-20-invoke-101-exploring-ai-models-and-concept-adapters/animagine-xl-4.0-pixel-demo.avif" title="Animagine XL 4.0 (Pixel Art XL)" >}}
{{% /flex-item %}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-06-20-invoke-101-exploring-ai-models-and-concept-adapters/juggernaut-xl-v9-pixel-demo.avif" title="Juggernaut XL v9 (Pixel Art XL)" >}}
{{% /flex-item %}}

{{< /flex >}}

需要注意，LoRA 这类概念适配器与用于训练的原始模型之间存在关联。概念适配器可以理解为一个模型的上层封装，其扩展和增强了某些概念。将其放在另一个模型上，其仍可以将这个概念应用到新的模型上，但质量可能会有所下降。这是因为训练概念适配器的底层模型与当前应用的模型可能有着不同的架构和假设。也就是说 LoRA 这类模型并不是一个完全独立的模型，而是一个专门为某个基础模型构建的适配器，但如果两个模型本质上非常相似，则 LoRA 具有一定的可移植性。
