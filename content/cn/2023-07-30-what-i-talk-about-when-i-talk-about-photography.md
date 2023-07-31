---
title: 当我谈摄影时，我谈些什么
subtitle: 色彩篇 Part 1
author: 范叶亮
date: '2023-07-30'
slug: what-i-talk-about-when-i-talk-about-photography-colors-part-1
categories:
  - 科普
  - 当我谈
  - 生活
tags:
  - 摄影
  - 色域
  - CIE 1931 色彩空间
  - 颜色匹配实验
  - 三刺激值曲线
  - 相对色度图
  - 明度
  - 色度
  - 色彩深度
  - 色深
  - FRC
  - 帧率控制
  - 像素抖动
  - Dither
  - 色度抽样
  - 动态范围
  - Dynamic Range
  - 高动态范围
  - High Dynamic Range
  - HDR
  - 标准动态范围
  - Standard Dynamic Range
  - SDR
  - 包围曝光
  - 曝光合成
  - Log 曲线
  - 曝光量
  - Photometric Exposure
  - 曝光值
  - Exposure Value
  - EV
images:
  - /images/cn/2023-07-30-what-i-talk-about-when-i-talk-about-photography-colors-part-1/color-matching-experiment.png
  - /images/cn/2023-07-30-what-i-talk-about-when-i-talk-about-photography-colors-part-1/cie-rgb-cie-xyz-color-matching-functions.png
  - /images/cn/2023-07-30-what-i-talk-about-when-i-talk-about-photography-colors-part-1/cie-1931-xy.png
  - /images/cn/2023-07-30-what-i-talk-about-when-i-talk-about-photography-colors-part-1/cie-1931-xy-comparison.png
  - /images/cn/2023-07-30-what-i-talk-about-when-i-talk-about-photography-colors-part-1/frc.png
  - /images/cn/2023-07-30-what-i-talk-about-when-i-talk-about-photography-colors-part-1/dither.png
  - /images/cn/2023-07-30-what-i-talk-about-when-i-talk-about-photography-colors-part-1/chroma-subsampling.png
  - /images/cn/2023-07-30-what-i-talk-about-when-i-talk-about-photography-colors-part-1/hdr-sdr.png
---

# 色域

在[当我谈修图时，我谈些什么 - 色彩篇 Part 1](/cn/2023/04/what-i-talk-about-when-i-talk-about-photo-retouching-colors-part-1) 中已经介绍过什么是[**色彩空间**](/cn/2023/04/what-i-talk-about-when-i-talk-about-photo-retouching-colors-part-1/#色彩空间)，在**显示领域**通常会使用 **RGB 色彩模型**，在**印刷领域**通常会使用 **CMYK 色彩模型**。而在**颜色感知领域**，[**CIE 1931 色彩空间**](https://zh.wikipedia.org/wiki/CIE_1931色彩空间) 则是在设计之初便要求包含普通人眼可见的所有颜色的标准色彩空间。

人类眼睛有对于短、中和长波的感光细胞，色彩空间在描述颜色时则可以通过定义三种刺激值，再利用值的叠加表示各种颜色。在 CIE 1931 色彩空间中，这三种刺激值并不是指对短、中和长波的反应，而是一组约略对应红色、绿色和蓝色的 X、Y 和 Z 的值。X、Y 和 Z 的值并不是真的看起来是红色、绿色和蓝色，而是使用 CIE XYZ 颜色匹配函数计算而来。

在**颜色匹配实验**中，如下图 [^image-source-color-matching-experiment] 所示：

![](/images/cn/2023-07-30-what-i-talk-about-when-i-talk-about-photography-colors-part-1/color-matching-experiment.png)

[^image-source-color-matching-experiment]: Verhoeven, G. (2016). Basics of photography for cultural heritage imaging. In E. Stylianidis & F. Remondino (Eds.), _3D recording, documentation and management of cultural heritage_ (pp. 127–251). Caithness: Whittles Publishing.

受试者通过观察单一光源的颜色和三原色光源的混合颜色是否相同，得到光谱**三刺激值曲线**如下图 [^image-source-color-matching-functions] 左所示。为了消除负值对数据处理带来的不便，通过转换得到了三个新的值 $X$、$Y$ 和 $Z$ 的曲线如下图 [^image-source-color-matching-functions] 右所示。

![](/images/cn/2023-07-30-what-i-talk-about-when-i-talk-about-photography-colors-part-1/cie-rgb-cie-xyz-color-matching-functions.png)

[^image-source-color-matching-functions]: Patrangenaru, V., & Deng, Y. (2020). Nonparametric data analysis on the space of perceived colors. _arXiv preprint arXiv:2004.03402._

在 CIE 1931 色彩空间中，所有可视颜色的完整绘图是三维的，$Y$ 可以表示颜色的明度 [^wikipedia-meaning-of-xyz]。$Y$ 表示明度的好处是在给定 $Y$ 值时，XZ 平面将包含此明度下的所有色度。通过规范化 $X$、$Y$ 和 $Z$ 的值：

`$$
\begin{aligned}
x &= \dfrac{X}{X + Y + Z} \\
y &= \dfrac{Y}{X + Y + Z} \\
z &= \dfrac{Z}{X + Y + Z} = 1 - x - y
\end{aligned}
$$`

色度可以使用 $x$ 和 $y$ 来表示。CIE 1931 的**相对色度图** [^image-source-cie-1931-xy] 如下所示：

![](/images/cn/2023-07-30-what-i-talk-about-when-i-talk-about-photography-colors-part-1/cie-1931-xy.png)

[^image-source-cie-1931-xy]: <https://commons.wikimedia.org/wiki/File:CIE1931xy_blank.svg>

外侧曲线边界是光谱轨迹，波长用纳米标记。不同色域（Color Gamut）标准之间的对比如下图 [^image-source-cie-1931-xy-comparison] 所示：

![](/images/cn/2023-07-30-what-i-talk-about-when-i-talk-about-photography-colors-part-1/cie-1931-xy-comparison.png)

[^image-source-cie-1931-xy-comparison]: <https://commons.wikimedia.org/wiki/File:CIE1931xy_gamut_comparison.svg>

对于一个显示设备来说，不可能产生超过其色域的颜色。通常情况下，讨论一台摄影设备的色域并没有意义，但使用什么样的色彩空间进行编码则需要重点关注。

[^wikipedia-meaning-of-xyz]: <https://en.wikipedia.org/wiki/CIE_1931_color_space#Meaning_of_X,_Y_and_Z>

# 色彩深度

**色彩深度**，简称**色深**（Color Depth），即存储一个像素的颜色所需要的位数。若色彩深度为 $n$ 位，则代表一共包含 $2^n$ 种颜色。例如我们常说的**真彩色**，即 24 位，对应 RGB 三个通道，每个通道 8 位（即 0-255），共可以表示 16,777,216 种颜色。

{{% flex justify-content="space-around" %}}

{{% flex-item %}}
{{% figure src="/images/cn/2023-07-30-what-i-talk-about-when-i-talk-about-photography-colors-part-1/color-depth-24-bit.png" title="24bit（98KB）" %}}
{{% /flex-item %}}

{{% flex-item %}}
{{% figure src="/images/cn/2023-07-30-what-i-talk-about-when-i-talk-about-photography-colors-part-1/color-depth-8-bit.png" title="8bit（37KB -62%）" %}}
{{% /flex-item %}}

{{% /flex %}}

{{% flex justify-content="space-around" %}}

{{% flex-item %}}
{{% figure src="/images/cn/2023-07-30-what-i-talk-about-when-i-talk-about-photography-colors-part-1/color-depth-2-bit.png" title="4bit（13KB -87%）" %}}
{{% /flex-item %}}

{{% flex-item %}}
{{% figure src="/images/cn/2023-07-30-what-i-talk-about-when-i-talk-about-photography-colors-part-1/color-depth-2-bit.png" title="2bit（6KB -94%）" %}}
{{% /flex-item %}}

{{% /flex %}}

从上述对比图 [^image-source-color-depth] 中不难看出，色深越大，图像的效果越好，图像内容之间的过度越自然，与此同时占用的存储也会越多。

[^image-source-color-depth]: <https://en.wikipedia.org/wiki/Color_depth>

在视频拍摄中，我们通常说的 8bit 和 10bit 指的是位深（Bit Depth），即每个通道的位数。设备在拍摄素材时，记录更大位数的信息会更有利于后期调色等处理。

在显示器的特性中，我们也经常会遇见 8bit 和 10bit，以及 8bit FRC 这个概念。**FRC** 是 **Frame Rate Control** 的缩写，即**帧率控制**，是一种时间维度的**像素抖动**算法。以灰度图像为例，如下图所示，当渲染一个图像包含多个帧时，可以让帧在明暗之间进行切换，从而产生中间灰度。

![](/images/cn/2023-07-30-what-i-talk-about-when-i-talk-about-photography-colors-part-1/frc.png)

相应的空间维度的像素抖动算法（**Dither**）如下图所示：

![](/images/cn/2023-07-30-what-i-talk-about-when-i-talk-about-photography-colors-part-1/dither.png)

所以，一块原生 10bit 屏幕优于 8bit FRC 10bit 的屏幕优于原生 8bit 的屏幕。

# 色度抽样

在拍摄视频时，除了 8bit 和 10bit 位深的区别外，我们还经常听到 4:2:2 和 4:2:0 等比值，这代表**色度抽样**。由于人眼对色度的敏感度不及对亮度的敏感度，图像的色度分量不需要有和亮度分量相同的清晰度，在色度上进行抽样可以在不明显降低画面质量的同时降低影像信号的总带宽。

抽样系统通常用一个三分比值表示：$J : a : b$，其中：

- $J$ 为水平抽样的宽度
- $a$ 为第一行 $J$ 个像素中色度的抽样数量
- $b$ 为第二行 $J$ 个像素中色度的抽样数量

不同的比值色度抽样对比图 [^image-source-chroma-subsampling] 如下所示：

![](/images/cn/2023-07-30-what-i-talk-about-when-i-talk-about-photography-colors-part-1/chroma-subsampling.png)

[^image-source-chroma-subsampling]: <https://en.wikipedia.org/wiki/Chroma_subsampling>

# 动态范围

**动态范围**（**Dynamic Range**）是可变信号（例如声音或光）最大值和最小值的比值。在相机中，设置不同的 ISO 会影响到动态范围在记录高光和暗部时的噪点表现。

**高动态范围**（**High Dynamic Range**，**HDR**）相比与**标准动态范围**（**Standard Dynamic Range**，**SDR**）具有更大的动态范围，简而言之 HDR 可以让画面中亮的地方足够亮暗的的地方足够暗。HDR 需要采集设备和显示设备同时支持才能够得以正常的显示，下图 [^image-source-what-is-hdr] 展示了 HDR 和 SDR 从场景采集到显示还原的过程：

![](/images/cn/2023-07-30-what-i-talk-about-when-i-talk-about-photography-colors-part-1/hdr-sdr.png)

[^image-source-what-is-hdr]: <https://www.benq.com/en-my/knowledge-center/knowledge/what-is-hdr.html>

最终 SDR 和 HDR 成像的区别如下图 [^image-source-hdr-sdr] 所示（模拟效果）：

{{< image-compare show-labels=true label-before="SDR" label-after="HDR" image-before="/images/cn/2023-07-30-what-i-talk-about-when-i-talk-about-photography-colors-part-1/sdr.png" image-after="/images/cn/2023-07-30-what-i-talk-about-when-i-talk-about-photography-colors-part-1/hdr.png" >}}

[^image-source-hdr-sdr]: <https://kmbcomm.com/demystifying-high-dynamic-range-hdr-wide-color-gamut-wcg/>

在摄影过程中，如下两种方式都可以得到不错的 HDR 照片：

1. 针对 RAW 格式照片，其存储的不同明暗数据已经足够多，针对高光降低一些曝光，暗部增加一些曝光即可获得 HDR 照片。
2. 前期进行**包围曝光**，即在拍摄时同时拍摄多张具有不同曝光补偿的照片，后期再利用**曝光合成**技术得到一张 HDR 照片。

在摄像过程中，上述的两种方案就变得不太可行了，如果对于视频的每一帧都保存 RAW 信息会导致视频素材体积过大。此时我们会采用一种名为 **Log 曲线**的方式对视频的每一帧图像进行处理。

首先我们需要了解一下什么是**曝光量**（**Photometric Exposure**）和**曝光值**（**Exposure Value**，**EV**）。**曝光量**是指进入镜头在感光介质上的光量，其由光圈、快门和感光度组合控制，定义为：

`$$
H = Et
$$`

其中，$E$ 为影像平面的照度，$t$ 为快门的曝光时间。影像平面照度与光圈孔径面积成正比，因此与光圈 $f$ 值的平方成反比，则有：

`$$
H \propto \dfrac{t}{N^2}
$$`

其中，$N$ 为光圈的 $f$ 值。$\dfrac{t}{N^2}$ 这个比例值可以用于表示多个等效的曝光时间和光圈 $f$ 值组合。此比值具有较大的分母，为了方便使用反转该比值并取以 $2$ 为底的对数则可以得到**曝光值**的定义：

`$$
EV = \log_2{\dfrac{N^2}{t}} = 2 \log_2{\left(N\right)} - \log_2{\left(t\right)}
$$`

在现实中，随着**光线强度**（类比曝光量）的**成倍**增加，人眼对于**光的感应**（类比曝光值）大约成**线性**增长。同时，摄像机器对于光线强度的记录是线性的，也就是说当光线强度翻倍时，转换后存储的数值也会翻倍。

以 8bit 为例，对于高光部分（7 - 8 档曝光值）会使用 128 位存储相关信息，而对于暗部（0 - 1 档曝光值）则仅使用 8 位存储相关信息，如下图左所示。此时由于高光部分看起来亮度变化并不大，使用的存储位数比暗部多得多，这种非均衡的的存储容易丢失图像的暗部细节。通过对曝光量进行 Log 处理，可以得到均衡的对应关系，如下图右所示。

{{% flex justify-content="space-around" %}}

{{% flex-item %}}
{{% figure src="/images/cn/2023-07-30-what-i-talk-about-when-i-talk-about-photography-colors-part-1/ev-linear-dv.png" title="EV 和曝光量关系" %}}
{{% /flex-item %}}

{{% flex-item %}}
{{% figure src="/images/cn/2023-07-30-what-i-talk-about-when-i-talk-about-photography-colors-part-1/ev-log-dv.png" title="EV 和曝光量 $\log$ 值关系" %}}
{{% /flex-item %}}

{{% /flex %}}

在真实场景中，各个相机厂商的所搭载的 Log 曲线并不完全相同，都会为了实现某种效果进行调整修改。但整体来说其目的还是为了让每一档曝光值之间存储的信息量大致相同。颜色矫正后和原始应用 Log 曲线的对比图像 [^image-source-normal-vs-logc] 如下所示：

![](/images/cn/2023-07-30-what-i-talk-about-when-i-talk-about-photography-colors-part-1/normal-vs-logc.jpg)

[^image-source-normal-vs-logc]: <https://postpace.io/blog/difference-between-raw-log-and-rec-709-camera-footage/>
