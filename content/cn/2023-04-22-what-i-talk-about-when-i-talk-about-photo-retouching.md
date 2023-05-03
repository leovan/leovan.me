---
title: 当我谈修图时，我谈些什么
subtitle: 色彩篇 Part 1
author: 范叶亮
date: '2023-04-22'
slug: what-i-talk-about-when-i-talk-about-photo-retouching-colors-part-1
categories:
  - 科普
  - 当我谈
  - 生活
tags:
  - 修图
  - 色彩空间
  - 色彩模型
  - RGB
  - 加法混色模型
  - CMYK
  - 减法混色模型
  - HSV
  - HSL
  - 色相
  - 饱和度
  - 明度
  - 亮度
  - 直方图
  - 色温
  - 色调
images:
  - /images/cn/2023-04-22-what-i-talk-about-when-i-talk-about-photo-retouching/demo-color-temperature-warm.jpg
  - /images/cn/2023-04-22-what-i-talk-about-when-i-talk-about-photo-retouching/demo-color-temperature-cold.jpg
  - /images/cn/2023-04-22-what-i-talk-about-when-i-talk-about-photo-retouching/demo-color-tint-negative.jpg
  - /images/cn/2023-04-22-what-i-talk-about-when-i-talk-about-photo-retouching/demo-color-tint-positive.jpg
---

> 文本是「当我谈」系列的第一篇博客，后续「当我谈」系列会从程序员的视角一起科普认知未曾触及的其他领域。

# 色彩空间

**色彩空间**是对色彩的组织方式，借助色彩空间和针对物理设备的测试，可以得到色彩的固定模拟和数字表示。**色彩模型**是一种抽象数学模型，通过一组数字来描述颜色。由于“色彩空间”有着固定的色彩模型和映射函数组合，非正式场合下，这一词汇也被用来指代色彩模型。

## RGB

红绿蓝（RGB）色彩模型，是一种**加法混色模型**，将<b style="color: #FF0000;">红（Red）</b>、<b style="color: #00FF00;">绿（Green）</b>、<b style="color: #0000FF;">蓝（Blue）</b>三原色的色光以不同的比例相加，以合成产生各种色彩光。三原色的原理不是出于物理原因，而是由于生理原因造成的。

RGB 色彩模型可以映射到一个立方体上，如下图所示：

![](/images/cn/2023-04-22-what-i-talk-about-when-i-talk-about-photo-retouching/rgb.png)

红绿蓝的三原色光显示技术广泛用于电视和计算机的显示器，利用红、绿、蓝三原色作为子像素组成的真色彩像素，透过眼睛及大脑的模糊化，“人类看到”不存在于显示器上的感知色彩。

## CMYK

印刷四分色模式（CMYK）是彩色印刷中采用的一种**减法混色模型**，利用色料的三原色混色原理，加上黑色油墨，共计四种颜色混合叠加，形成所谓的“全彩印刷”。四种标准颜色分别是：

- <b style="color: #00FFFF;">Cyan</b>：青色或“水蓝”
- <b style="color: #FF00FF;">Magenta</b>：洋红色或“紫色”
- <b style="color: #FFFF00;">Yellow</b>：黄色
- <b style="color: #000000;">Key plate</b>：因实务上多使用黑色，所以也可以简单视为 **blacK**

CMY 叠色的示意图如下所示：

![](/images/cn/2023-04-22-what-i-talk-about-when-i-talk-about-photo-retouching/cmyk.png)

利用 $0$ 到 $1$ 的浮点数表示 $R, G, B$ 和 $C, M, Y, K$，从四分色向三原光转换公式如下：

`$$
\begin{aligned}
R &= \left(1 - C\right) \left(1 - K\right) \\
G &= \left(1 - M\right) \left(1 - K\right) \\
B &= \left(1 - Y\right) \left(1 - K\right)
\end{aligned}
$$`

从三原光向四分色转换公式如下：

`$$
\begin{aligned}
C &= 1 - \dfrac{R}{\max \left(R, G, B\right)} \\
M &= 1 - \dfrac{G}{\max \left(R, G, B\right)} \\
Y &= 1 - \dfrac{B}{\max \left(R, G, B\right)} \\
K &= 1 - \max \left(R, G, B\right) \\
\end{aligned}
$$`

## HSL 和 HSV

HSL 和 HSV 都是一种将 RGB 色彩模型中的点在圆柱坐标系中的表示法。这两种表示法试图做到比基于笛卡尔坐标系的几何结构 RGB 更加直观。HSL 即色相、饱和度、亮度（Hue，Saturation，Lightness），HSV 即色相、饱和度、明度（Hue，Saturation，Value），又称 HSB，其中 B 为 Brightness。另种色彩空间定义如下图所示：

{{% figure src="/images/cn/2023-04-22-what-i-talk-about-when-i-talk-about-photo-retouching/hsl-hsv.png" title="HSL 和 HSV 色彩空间" %}}

### 色相

色相（Hue）指的是色彩的外相，是在不同波长的光照射下，人眼所感觉到的不同的颜色。在 HSL 和 HSV 色彩空间中，色相是以<b style="color: #FF0000">红色</b>为 0 度（360 度）、<b style="color: #FFFF00">黄色</b>为 60 度、<b style="color: #00FF00">绿色</b>为 120 度、<b style="color: #00FFFF">青色</b>为 180 度、<b style="color: #0000FF">蓝色</b>为 240 度、<b style="color: #FF00FF">洋红色</b>为 300 度。如下图所示：

![](/images/cn/2023-04-22-what-i-talk-about-when-i-talk-about-photo-retouching/hue-scale.png)

### 饱和度

饱和度（Saturation）指的是色彩的纯度，饱和度由光强度和它在不同波长的光谱中分布的程度共同决定。下图为红色从最小饱和度到最大饱和度的示例：

![](/images/cn/2023-04-22-what-i-talk-about-when-i-talk-about-photo-retouching/red-saturations.png)

### 亮度和明度

明度值是与同样亮的白色物体相比，某物的亮的程度。如果我们拍摄一张图像，提取图像色相、饱和度和明度值，然后将它们与不同色彩空间的明度值进行比较，可以迅速地从视觉上得出差异。如下图所示，HSV 色彩空间中的 V 值和 HSL 色彩空间中的 L 值与感知明度值明显不同：

{{% flex %}}

{{% flex-item %}}
{{% figure src="/images/cn/2023-04-22-what-i-talk-about-when-i-talk-about-photo-retouching/fire-breather.jpg" title="原始图片" %}}
{{% /flex-item %}}

{{% flex-item %}}
{{% figure src="/images/cn/2023-04-22-what-i-talk-about-when-i-talk-about-photo-retouching/fire-breather-hsl-l.jpg" title="HSL 中的 L" %}}
{{% /flex-item %}}

{{% flex-item %}}
{{% figure src="/images/cn/2023-04-22-what-i-talk-about-when-i-talk-about-photo-retouching/fire-breather-hsv-v.jpg" title="HSV 中的 V" %}}
{{% /flex-item %}}

{{% /flex %}}

### 差异

HSV 和 HSL 两者对于色相（H）的定义一致，但对于饱和度（S）和亮度与明度（L 与 B）的定义并不一致。

在 HSL 中，饱和度独立于亮度存在，也就是说非常浅的颜色和非常深的颜色都可以在 HSL 中非常饱和。而在 HSV 中，接近于白色的颜色都具有较低的饱和度。

- HSV 中的 S 控制纯色中混入白色的量，值越大，混入的白色越少，颜色越纯。
- HSV 中的 V 控制纯色中混入黑色的量，值越大，混入的黑色越少，明度越高。
- HSL 中的 S 和黑白没有关系，饱和度不控制颜色中混入白色和黑色的多少。
- HSL 中的 L 控制纯色中混入白色和黑色的多少。

以 Photoshop 和 Afiinity Photo 两款软件的拾色器为例：

{{% flex justify-content="space-around" %}}

{{% flex-item %}}
{{% figure src="/images/cn/2023-04-22-what-i-talk-about-when-i-talk-about-photo-retouching/color-picker-photoshop.png" title="Photoshop 拾色器（HSV）" %}}
{{% /flex-item %}}

{{% flex-item %}}
{{% figure src="/images/cn/2023-04-22-what-i-talk-about-when-i-talk-about-photo-retouching/color-picker-affinityphoto.png" title="Afiinity Photo 拾色器（HSL）" %}}
{{% /flex-item %}}

{{% /flex %}}

两个软件分别采用 HSV 和 HSL 色彩空间，其横轴为饱和度（S），纵轴分别为明度（V）和亮度（L）。不难看出，在 Photoshop 拾色器中，越往上混入的黑色越少，明度越高；越往右混入的白色越少，纯度越高。在 Afiinity Photo 拾色器中，下部为纯黑色，亮度最小，从下往上，混入的黑色逐渐减少，直到 50\% 位置处完全没有黑色混入，继续往上走，混入的白色逐渐增加，直到 100\% 位置处完全变为纯白色，亮度最高。

# 直方图

图像直方图是反映图像**色彩亮度**的直方图，其中 $x$ 轴表示亮度值，$y$ 轴表示图像中该亮度值像素点的个数。以 $8$ 位图像为例，亮度的取值范围为 $\left[0, 2^8-1\right]$，即 $\left[0, 255\right]$。以如下图片为例（原始图片：[链接](/images/cn/2023-04-22-what-i-talk-about-when-i-talk-about-photo-retouching/demo.jpg)）：

{{% figure src="/images/cn/2023-04-22-what-i-talk-about-when-i-talk-about-photo-retouching/demo-small.jpg" title="原始图片" %}}

在 Lightroom 中直方图如下所示：

{{% figure src="/images/cn/2023-04-22-what-i-talk-about-when-i-talk-about-photo-retouching/demo-lightroom-image-histgram.png" title="原始图片 Lightroom 直方图" %}}

利用 Python 绘制的直方图如下所示：

{{% details-summary summary="直方图代码" %}}
{{< include-code file="/static/codes/cn/2023-04-22-what-i-talk-about-when-i-talk-about-photo-retouching/demo-histgram.py" language="python" >}}
{{% /details-summary %}}

{{% figure src="/images/cn/2023-04-22-what-i-talk-about-when-i-talk-about-photo-retouching/demo-image-histgram.png" title="原始图片直方图" %}}

直方图以 $28, 85, 170, 227$ 为分界线可以划分为**黑色**、**阴影**、**曝光**、**高光**、**白色**共 5 个区域。其中曝光区域以适中的亮度保留了图片最多的细节，阴影和高光对应了照片中较暗和较亮的区域，黑色和白色两个部分则几乎没有任何细节。当整个直方图**过于偏左**时表示**欠曝**，**过于偏右**时则表示**过曝**。

# 色温

色温（Temperature）是指照片中光源发出相似的光的黑体辐射体所具有的开尔文温度。开尔文温度越**低**光越**暖**，开尔文温度越**高**光越**冷**，如下图所示：

![](/images/cn/2023-04-22-what-i-talk-about-when-i-talk-about-photo-retouching/color-temperature.png)

针对图片分别应用 5000K 和 10000K 色温的对比结果如下图所示：

{{% details-summary summary="色温代码" %}}
{{< include-code file="/static/codes/cn/2023-04-22-what-i-talk-about-when-i-talk-about-photo-retouching/demo-temperature.py" language="python" >}}
{{% /details-summary %}}

{{< image-compare show-labels=true label-before="暖色" label-after="冷色" image-before="/images/cn/2023-04-22-what-i-talk-about-when-i-talk-about-photo-retouching/demo-color-temperature-warm.jpg" image-after="/images/cn/2023-04-22-what-i-talk-about-when-i-talk-about-photo-retouching/demo-color-temperature-cold.jpg" >}}

# 色调

色调（Tint）允许我们为了实现中和色偏或增加色偏的目的，而将色偏向绿色或洋红色转变。针对图片分别应用 -30 和 +30 色调的对比结果如下图所示：

{{% details-summary summary="色调代码" %}}
{{< include-code file="/static/codes/cn/2023-04-22-what-i-talk-about-when-i-talk-about-photo-retouching/demo-tint.py" language="python" >}}
{{% /details-summary %}}

{{< image-compare show-labels=true label-before="洋红" label-after="绿色" image-before="/images/cn/2023-04-22-what-i-talk-about-when-i-talk-about-photo-retouching/demo-color-tint-negative.jpg" image-after="/images/cn/2023-04-22-what-i-talk-about-when-i-talk-about-photo-retouching/demo-color-tint-positive.jpg" >}}
