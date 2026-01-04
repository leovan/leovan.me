---
title: '使用 Invoke 创作你的第一张图片'
subtitle: 'Invoke AI 101 教程'
author: 范叶亮
date: '2025-06-01'
slug: invoke-101-creating-your-first-image-in-invoke
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
  - SD1.X
  - SDXL
  - Flux
  - Juggernaut XL
---

{{% admonition type="tip" %}}
本节将展示如何使用 Invoke 创作你的第一张图片。
{{% /admonition %}}

{{< tab id="video" labels-position="center" >}}

{{% tab-item label="<i class='icon icon-bilibili'></i> Bilibili" %}}
{{< bilibili bvid="BV16AuczkEAk" >}}
{{% /tab-item %}}

{{% tab-item label="<i class='icon icon-youtube'></i> YouTube" %}}
{{< youtube id="efBFZ3S8sWc" >}}
{{% /tab-item %}}

{{< /tab >}}

## 安装 Invoke

从 [Invoke 官网](https://www.invoke.com/downloads)下载对应系统的安装包，根据如下步骤完成安装。

1. 运行 Invoke 社区版本，单击 <button>Install</button> 开始安装。
2. 选择安装位置，单击 <button>Next</button> 进行下一步。
3. 选择安装版本，单击 <button>Next</button> 进行下一步。
4. 确认 GPU 情况，单击 <button>Next</button> 进行下一步。
5. 确认安装选项，单击 <button>Install</button> 开始安装。
6. 安装完成，单击 <button>Finish</button> 关闭安装向导。
7. 安装完成后，单击 <button>Launch</button> 启动 Invoke。

{{< swiper data="/data/cn/2025-06-01-invoke-101-creating-your-first-image-in-invoke/installation.json" max-width="800px" >}}

## 用户界面

Invoke 启动后会打开主界面，从启动器的日志不难看出，Invoke 在后台启动了一个 HTTP 服务，用浏览器打开 `http://127.0.0.1:9090` 可以得到相同的界面：

{{< swiper data="/data/cn/2025-06-01-invoke-101-creating-your-first-image-in-invoke/main-window.json" max-width="1080px" >}}

主界面包含三个区域，分别是：

1. 左侧：用于输入提示词、模型选择和参数设置等。
2. 中间：用于显示生成的图片。
3. 右侧：用于显示生成图片的所需的图层和历史生成的图片等。

### 左侧

#### 提示词

{{< flex align-items="flex-start" >}}

{{% flex-item flex-grow="1" flex-basis="50%" %}}
{{< figure src="/images/cn/2025-06-01-invoke-101-creating-your-first-image-in-invoke/ui-left-propmt.avif" title="提示词" >}}
{{% /flex-item %}}

{{% flex-item flex-grow="1" flex-basis="50%" %}}
提示词区域用于输入生成图片提示词。

1. 在下拉菜单中可以选择预设的提示词模板。
2. 在 `Prompt` 中输入正向提示词，在 [`Negative Prompt`](https://getimg.ai/guides/guide-to-negative-prompts-in-stable-diffusion) 中输入负向提示词。
3. 也可以将自定义的提示词添加为模板以方便后续使用。
{{% /flex-item %}}

{{< /flex >}}

#### 图像

{{< flex align-items="flex-start" >}}

{{% flex-item flex-grow="1" flex-basis="50%" %}}
{{< figure src="/images/cn/2025-06-01-invoke-101-creating-your-first-image-in-invoke/ui-left-image.avif" title="图像" >}}
{{% /flex-item %}}

{{% flex-item flex-grow="1" flex-basis="50%" %}}
图像区域用于控制生成图片的比例和大小。

1. `Aspect` 用于设置生成图片的宽高比，`Width` 和 `Height` 用于设置生成图片的宽高。
2. [`Seed`](https://getimg.ai/guides/guide-to-seed-parameter-in-stable-diffusion) 用于设置生成图片的随机数种子，设置相同的随机数种子将在相同的条件下得到一致的图片，这在微调的时候会派上用场。
{{% /flex-item %}}

{{< /flex >}}

#### 生成

{{< flex align-items="flex-start" >}}

{{% flex-item flex-grow="1" flex-basis="50%" %}}
{{< figure src="/images/cn/2025-06-01-invoke-101-creating-your-first-image-in-invoke/ui-left-generation.avif" title="生成" >}}
{{% /flex-item %}}

{{% flex-item flex-grow="1" flex-basis="50%" %}}
生成区域用于设置模型和相关参数。

1. `Model` 用于选择生成图片的模型。
2. `Concepts` 用于选择进行微调的 LoRA 模型。
3. 高级选项中可以设置图片生成使用的调度器（[`Scheduler`](https://getimg.ai/guides/guide-to-stable-diffusion-samplers)）。调度器负责数据采样，包括采样的步骤数（[`Steps`](https://getimg.ai/guides/interactive-guide-to-stable-diffusion-steps-parameter)）和提示词相关性（[`CFG Scale`](https://getimg.ai/guides/interactive-guide-to-stable-diffusion-guidance-scale-parameter)）等。
{{% /flex-item %}}

{{< /flex >}}

### 中间

{{< flex align-items="flex-start" >}}

{{% flex-item flex-grow="1" flex-basis="50%" %}}
{{< figure src="/images/cn/2025-06-01-invoke-101-creating-your-first-image-in-invoke/ui-middle.avif" title="中间区域" >}}
{{% /flex-item %}}

{{% flex-item flex-grow="1" flex-basis="50%" %}}
中间区域用于查看和调整生成的图片。在后续教程中将会深度介绍如何使用该区域来优化生成的图片。

在上方选项卡中单击 `Canvas` 可以打开画布，单击 `Image Viewer` 可打开图片浏览器。
{{% /flex-item %}}

{{< /flex >}}

### 右侧

#### 图板和图片库

{{< flex align-items="flex-start" >}}

{{% flex-item flex-grow="1" flex-basis="50%" %}}
{{< figure src="/images/cn/2025-06-01-invoke-101-creating-your-first-image-in-invoke/ui-right-boards-gallery.avif" title="图板和图片库" >}}
{{% /flex-item %}}

{{% flex-item flex-grow="1" flex-basis="50%" %}}
图板用于组织和管理用户生成的图像，它提供了一种结构化的方式来高效地分类和访问这些图像。

在图片库中，你可以将图片拖拽到画布中来使用。此外，你还可以在图库中共享、下载和删除图片。
{{% /flex-item %}}

{{< /flex >}}

#### 图层

{{< flex align-items="flex-start" >}}

{{% flex-item flex-grow="1" flex-basis="50%" %}}
{{< figure src="/images/cn/2025-06-01-invoke-101-creating-your-first-image-in-invoke/ui-right-layers.avif" title="图层" >}}
{{% /flex-item %}}

{{% flex-item flex-grow="1" flex-basis="50%" %}}
图层区域显示了工作区中用于修改图像的所有活动图层。单击右上角的 `+` 图标即可添加新图层。你可以创建多个图层并对其进行操作和变换，在生成图像之前进行组合使用。
{{% /flex-item %}}

{{< /flex >}}

## 模型

单击左侧面板的 <span style="vertical-align: middle;"><svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 256 256" aria-hidden="true" height="1em" widht="1em" xmlns="http://www.w3.org/2000/svg"><path d="M225.6,62.64l-88-48.17a19.91,19.91,0,0,0-19.2,0l-88,48.17A20,20,0,0,0,20,80.19v95.62a20,20,0,0,0,10.4,17.55l88,48.17a19.89,19.89,0,0,0,19.2,0l88-48.17A20,20,0,0,0,236,175.81V80.19A20,20,0,0,0,225.6,62.64ZM128,36.57,200,76,128,115.4,56,76ZM44,96.79l72,39.4v76.67L44,173.44Zm96,116.07V136.19l72-39.4v76.65Z"></path></svg></span> 图标打开模型页面。针对新手用户 Invoke 提供了新手模型包，单击 `Starter Models` 选项卡，可以看到系统提供了 `Stable Diffusion 1.5`、`SDXL` 和 `FLUX` 三款模型包。根据官方[系统环境要求](https://invoke-ai.github.io/InvokeAI/installation/quick_start/#step-1-system-requirements)和自己的设备性能选择合适的模型包。

{{< tab id="system-requirements" >}}

{{% tab-item label="Stable Diffusion 1.5" %}}
- GPU：Nvidia 10xx 或更新，4GB+ 显存
- 内存：至少 8GB
- 磁盘：至少 30GB
{{% /tab-item %}}

{{% tab-item label="SDXL" %}}
- GPU：Nvidia 20xx 或更新，8GB+ 显存
- 内存：至少 18GB
- 磁盘：至少 100GB
{{% /tab-item %}}

{{% tab-item label="FLUX" %}}
- GPU：Nvidia 20xx 或更新，10GB+ 显存
- 内存：至少 32GB
- 磁盘：至少 200GB
{{% /tab-item %}}

{{< /tab >}}

在下载模型前，需在 HuggingFace 的[设置页面](https://huggingface.co/settings/tokens)创建 Token，并将其保存在 Invoke 模型页面的 HuggingFace 选项卡中。本教程选择 `SDXL` 作为模型包，单击模型包启动下载。模型下载完毕后可以在 `Model Manager` 中查看已下载的模型。

![模型](/images/cn/2025-06-01-invoke-101-creating-your-first-image-in-invoke/ui-models.avif)

## 创作图片

在提示词模板中选择 `Environment Art`，在 `Prompt` 中输入如下提示词：

```txt
futuristic urban park, neon lighting, raised highways, green spaces, modern architecture
```

单击模板中的 <button><span style="vertical-align: middle;"><svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 256 256" aria-hidden="true" focusable="false" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M251,123.13c-.37-.81-9.13-20.26-28.48-39.61C196.63,57.67,164,44,128,44S59.37,57.67,33.51,83.52C14.16,102.87,5.4,122.32,5,123.13a12.08,12.08,0,0,0,0,9.75c.37.82,9.13,20.26,28.49,39.61C59.37,198.34,92,212,128,212s68.63-13.66,94.48-39.51c19.36-19.35,28.12-38.79,28.49-39.61A12.08,12.08,0,0,0,251,123.13Zm-46.06,33C183.47,177.27,157.59,188,128,188s-55.47-10.73-76.91-31.88A130.36,130.36,0,0,1,29.52,128,130.45,130.45,0,0,1,51.09,99.89C72.54,78.73,98.41,68,128,68s55.46,10.73,76.91,31.89A130.36,130.36,0,0,1,226.48,128,130.45,130.45,0,0,1,204.91,156.12ZM128,84a44,44,0,1,0,44,44A44.05,44.05,0,0,0,128,84Zm0,64a20,20,0,1,1,20-20A20,20,0,0,1,128,148Z"></path></svg></span></button> 按钮会开启应用模板后的提示词预览，如下图所示：

{{< figure src="/images/cn/2025-06-01-invoke-101-creating-your-first-image-in-invoke/prompt-demo-environment-art.avif" title="模板提示词预览"  large-max-width="50%" middle-max-width="50%" >}}

可以看到，提示词模板在用户输入的提示词基础上添加了更多的正向和负向提示词。在 `Generation` 中选择 `Juggernaut XL v9` 作为生成模型。

在左上角 <span style="vertical-align: middle;">![](/images/cn/2025-06-01-invoke-101-creating-your-first-image-in-invoke/iteration-and-generation.avif)</span> 中输入生成图片的数量，单击 <button>Invoke</button> 开始生成图片。单击左侧面板的 <span style="vertical-align: middle;"><svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 256 256" aria-hidden="true" focusable="false" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M28,64A12,12,0,0,1,40,52H216a12,12,0,0,1,0,24H40A12,12,0,0,1,28,64Zm104,52H40a12,12,0,0,0,0,24h92a12,12,0,0,0,0-24Zm0,64H40a12,12,0,0,0,0,24h92a12,12,0,0,0,0-24Zm120-20a12,12,0,0,1-5.64,10.18l-64,40A12,12,0,0,1,164,200V120a12,12,0,0,1,18.36-10.18l64,40A12,12,0,0,1,252,160Zm-34.64,0L188,141.65v36.7Z"></path></svg></span> 图标打开队列页面，等待中、执行中和已完成的所有任务都将显示在该页面中：

![队列](/images/cn/2025-06-01-invoke-101-creating-your-first-image-in-invoke/ui-queue.avif)

生成的 3 张图片如下所示：

{{< flex >}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-06-01-invoke-101-creating-your-first-image-in-invoke/futuristic-urban-park-en-01.avif" title="第 1 张" >}}
{{% /flex-item %}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-06-01-invoke-101-creating-your-first-image-in-invoke/futuristic-urban-park-en-02.avif" title="第 2 张" >}}
{{% /flex-item %}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-06-01-invoke-101-creating-your-first-image-in-invoke/futuristic-urban-park-en-03.avif" title="第 3 张" >}}
{{% /flex-item %}}

{{< /flex >}}

## 中文测试

为了验证 `Juggernaut XL v9` 模型对于中文提示词的兼容性，对上述示例和 `Environment Art` 提示词模板中的提示词整理中英文对照版本如下：

<table>
    <thead>
        <tr>
            <th width="20%">提示词</th>
            <th width="40%">英文</th>
            <th width="40%">中文</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>用户 - 正向</td>
            <td>futuristic urban park, neon lighting, raised highways, green spaces, modern architecture</td>
            <td>未来城市公园, 霓虹灯, 高架公路, 绿色空间, 现代建筑</td>
        </tr>
        <tr>
            <td>模板 - 正向</td>
            <td>environment artwork, hyper-realistic digital painting style with cinematic composition, atmospheric, depth and detail, voluminous. textured dry brush 2d media</td>
            <td>环境艺术作品, 具有电影构图的超现实数字绘画风格, 大气, 深度和细节, 丰满, 纹理干笔画 2D 媒体</td>
        </tr>
        <tr>
            <td>模板 - 负向</td>
            <td>photo, distorted, blurry, out of focus. sketch.</td>
            <td>照片, 扭曲, 模糊, 失焦, 草图</td>
        </tr>
    </tbody>
</table>

用户的正向提示词使用中文，选择 `Environment Art` 提示词模板（即提示词模板使用英文），生成的图片如下：

{{< flex >}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-06-01-invoke-101-creating-your-first-image-in-invoke/futuristic-urban-park-mix-01.avif" title="第 1 张" >}}
{{% /flex-item %}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-06-01-invoke-101-creating-your-first-image-in-invoke/futuristic-urban-park-mix-02.avif" title="第 2 张" >}}
{{% /flex-item %}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-06-01-invoke-101-creating-your-first-image-in-invoke/futuristic-urban-park-mix-03.avif" title="第 3 张" >}}
{{% /flex-item %}}

{{< /flex >}}

用户的正向提示词使用中文，不选择提示词模板，将 `Environment Art` 提示词模板的中文提示词补充到用户的正向和负向提示词后，生成的图片如下：

{{< flex >}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-06-01-invoke-101-creating-your-first-image-in-invoke/futuristic-urban-park-zh-01.avif" title="第 1 张" >}}
{{% /flex-item %}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-06-01-invoke-101-creating-your-first-image-in-invoke/futuristic-urban-park-zh-02.avif" title="第 2 张" >}}
{{% /flex-item %}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-06-01-invoke-101-creating-your-first-image-in-invoke/futuristic-urban-park-zh-03.avif" title="第 3 张" >}}
{{% /flex-item %}}

{{< /flex >}}

不难看出虽然图片生成的画质不错，但其并未遵循提示词的指令生成（看起来是将中文提示词作为了画风），因此可以判断 `Juggernaut XL v9` 模型不具备直接使用中文提示词的能力。
