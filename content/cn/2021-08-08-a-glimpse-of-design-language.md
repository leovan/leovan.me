---
title: 设计语言初探 (A Glimpse of Design Language)
author: 范叶亮
date: '2021-08-08'
slug: a-glimpse-of-design-language
show_toc: true
toc_depth: 3
categories:
  - 产品
  - 设计
tags:
  - Design Language
  - 设计语言
  - Design Language System
  - 设计语言系统
  - Apple Human Interface Guidelines
  - 苹果人机界面设计指南
  - Google Material Design
  - 谷歌材料设计
  - Microsoft Fluent Design
  - 微软流畅设计
  - Ant Design
  - 蚂蚁金服设计
  - 语法
  - 设计价值观
  - 设计原则
  - 语素
  - 色彩
  - 布局
  - 字体
  - 图标
  - 语句
  - 语义
  - 语境
  - 语气
  - 语素
  - 响度
images:
  - /images/cn/2021-08-08-a-glimpse-of-design-language/qq-music.png
  - /images/cn/2021-08-08-a-glimpse-of-design-language/futu-nn.png
---

设计语言（Design Language）或设计语言系统（Design Language System, DLS）是一套用于指导产品设计的整体风格方案 [^design-language-wikipedia]。设计语言把设计作为一种“沟通的方式”，用于在特定的场景内，做适当的表达，进行特定的信息传递。设计语言在建筑、工业设计和数字产品等领域都有广泛的应用，本文仅围绕数字产品进行初探。

## 为什么构建设计语言？

### 统一

通过设计语言可以在整个平台中统一颜色、字体、组件、动效等各种规范，避免由于设计师的个人特点导致产品风格不一致。

### 体验

优秀的设计语言符合大众审美，可以提高产品的可用性和易用性。设计语言可以使用户能够与具备一致性的应用进行交互，让用户在使用过程中获得愉悦，提升用户体验。

### 效率

优秀的设计语言使得设计和开发团队能够快速、经济、高效地进行开发、重构和迭代产品。通过不断更新和完善的文档库，可以改善团队之间的协作，提高生产力。

### 品牌

设计语言的构建可以传达一个统一的公司品牌形象。设计语言让产品具有自己的身份，使其在市场上的众多产品中更容易被识别出来，加深用户对品牌的印象。

## 设计语言构建

在此我们借助语言学的角度来讨论数字化产品的构建 [^design-language-uisdc]。在语言应用中，我们通常会涉及语法、语素、语句、语义、语境、语气、语素和响度等维度，通过不同的组合达成应景的表达和适时的沟通。

### 语法

设计语言中的语法即设计价值观和设计原则，这是构建设计语言系统的起点，用于传达品牌主张或设计理念，它将指引业务设计执行的方向。

制定设计原则时，首先研究用户特性，聚焦产品核心价值，然后通过脑暴等形式选择有特点的维度，结合用户体验与品牌属性将其视觉化，最后用简要的语言归纳出来。

#### Ant Design 设计价值观 [^ant-design-values]

<table>
  <tr>
    <td width="50%"><img src="https://gw.alipayobjects.com/mdn/rms_08e378/afts/img/A*zx7LTI_ECSAAAAAAAAAAAABkARQnAQ"/></td>
    <td>
      <p><b>自然</b></p>
      <p>数字世界的光速迭代使得产品日益复杂，而人类意识和注意力资源有限。面对这种设计矛盾，追求「自然」交互将是 Ant Design 持之以恒的方向。</p>
    </td>
  </tr>
  <tr>
    <td width="50%"><img src="https://gw.alipayobjects.com/mdn/rms_08e378/afts/img/A*yHjSQKAhF5kAAAAAAAAAAABkARQnAQ"/></td>
    <td>
      <p><b>确定性</b></p>
      <p>界面是用户与系统交互的媒介，是手段而非目的。在追求「自然」交互基础上，通过 Ant Design 创造的产品界面应是高确定性、低合作熵的状态。</p>
    </td>
  </tr>
  <tr>
    <td width="50%"><img src="https://gw.alipayobjects.com/mdn/rms_08e378/afts/img/A*xOYlR4e8ihIAAAAAAAAAAABkARQnAQ"/></td>
    <td>
      <p><b>意义感</b></p>
      <p>一个产品或功能被设计者创造出来不只是用户的需要，而更多是承载用户的某个工作使命。产品设计应充分站在工作视角，促成用户使命的达成；同时，在「自然」、「确定」之上，兼顾用户的人性需求，为工作过程创造富有意义感的人机交互。</p>
    </td>
  </tr>
  <tr>
    <td width="50%"><img src="https://gw.alipayobjects.com/mdn/rms_08e378/afts/img/A*pKz3TabovrEAAAAAAAAAAABkARQnAQ"/></td>
    <td>
      <p><b>生长性</b></p>
      <p>企业级产品功能的增长与用户系统角色的演变相生相伴。设计者应为自己创造的产品负责，提升功能、价值的可发现性。用发展的眼光做设计，充分考虑人、机两端的共同生长。</p>
    </td>
  </tr>
</table>

#### Ant Design 设计原则 [^ant-design-principle]

##### 亲密性

如果信息之间关联性越高，它们之间的距离就应该越接近，也越像一个视觉单元；反之，则它们的距离就应该越远，也越像多个视觉单元。亲密性的根本目的是实现组织性，让用户对页面结构和信息层次一目了然。

##### 对齐

正如「格式塔学派」中的连续律（Law of Continuity）所描述的，在知觉过程中人们往往倾向于使知觉对象的直线继续成为直线，使曲线继续成为曲线。在界面设计中，将元素进行对齐，既符合用户的认知特性，也能引导视觉流向，让用户更流畅地接收信息。

##### 对比

对比是增加视觉效果最有效方法之一，同时也能在不同元素之间建立一种有组织的层次结构，让用户快速识别关键信息。

##### 重复

相同的元素在整个界面中不断重复，不仅可以有效降低用户的学习成本，也可以帮助用户识别出这些元素之间的关联性。

##### 直截了当

正如 Alan Cooper 所言：「需要在哪里输出，就要允许在哪里输入」。这就是直接操作的原理。eg：不要为了编辑内容而打开另一个页面，应该直接在上下文中实现编辑。

##### 足不出户

能在这个页面解决的问题，就不要去其它页面解决，因为任何页面刷新和跳转都会引起变化盲视（Change Blindness），导致用户心流（Flow）被打断。频繁的页面刷新和跳转，就像在看戏时，演员说完一行台词就安排一次谢幕一样。

##### 简化交互

根据费茨法则（Fitts's Law）所描述的，如果用户鼠标移动距离越少、对象相对目标越大，那么用户越容易操作。通过运用上下文工具（即：放在内容中的操作工具），使内容和操作融合，从而简化交互。

##### 提供邀请

很多富交互模式（eg：「拖放」、「行内编辑」、「上下文工具」）都有一个共同问题，就是缺少易发现性。所以「提供邀请」是成功完成人机交互的关键所在。

邀请就是引导用户进入下一个交互层次的提醒和暗示，通常包括意符（eg：实时的提示信息）和可供性，以表明在下一个界面可以做什么。当可供性中可感知的部分（Perceived Affordance）表现为意符时，人机交互的过程往往更加自然、顺畅。

##### 巧用过渡

人脑灰质（Gray Matter）会对动态的事物（eg：移动、形变、色变等）保持敏感。在界面中，适当的加入一些过渡效果，能让界面保持生动，同时也能增强用户和界面的沟通。

##### 即时反应

「提供邀请」的强大体现在 交互之前 给出反馈，解决易发现性问题；「巧用过渡」的有用体现在它能够在 交互期间 为用户提供视觉反馈；「即时反应」的重要性体现在 交互之后 立即给出反馈。

就像「牛顿第三定律」所描述作用力和反作用一样，用户进行了操作或者内部数据发生了变化，系统就应该立即有一个对应的反馈，同时输入量级越大、重要性越高，那么反馈量级越大、重要性越高。

虽然反馈太多（准确的说，错误的反馈太多）是一个问题，但是反馈太少甚至没有反馈的系统，则让人感觉迟钝和笨拙，用户体验更差。

#### Alibaba Fusion 设计价值观 [^fusion-design-values]

![](https://fusion.alicdn.com/images/2o1CnXRJI4a_-ilKT92bcI0fs.png)

##### 化繁为简的交互模式

面对互联网产品高迭代节奏和复杂的中后台场景，将复杂的业务组件抽象为用户标准认知层的交互方式，这套组件库来自于阿里巴巴上百个中后台场景的抽象结果，试图建立中后台 web 设计标准。

##### 驾驭技术

你用的所有设计资料，小到 sketch 样式工具中的颜色、字体、字号、投影、边框、尺寸；再到组件，大到一套完整的中后台产品系统，均能找到其对应的代码，完整的释放整个团队的前端生产力。

##### 追求新鲜，潮流

设计风格每年都会更新换代，由于 Alibaba Fusion  设计系统中的颜色、字体、字号、投影等样式均可通过线上配置修改，这也决定了它可以快速（甚至 15 分钟内）完成整套设计系统的样式迭代。

##### 聚变/裂变

通过在 Alibaba Fusion 设计系统原则下，变换样式、多维度定制组件交互形式，可瞬间获取属于自己业务属性的设计系统；我们期待有无数业务线能够通过 Alibaba Fusion 的设计系统原则聚变出符合各类业务场景的 Fusion 生态系统。

##### 效率

Alibaba Fusion Design 希望构建一套提升设计与开发之间 UI 构建效率的工作方式，让 UED 的工作能够尽可能多的投入在 UE（User Experience）的用户调研、用户体验、商业思考，而在 D（Design）的过程中更多的投入与创意而非日复一日的重复绘图。

#### 腾讯 Q 语言理念 [^q-design-concept]

<table>
  <tr>
    <td width="30%"><img src="https://qzonestyle.gtimg.cn/qzone/qzact/act/external/qdesign/Design/QLanguage/DesignConcept/tongyi.png"/></td>
    <td>
      <p><b>统一体验</b></p>
      <p>QQ 作为一个社交平台，会容纳多样性的功能与体验，为了降低用户在不同场景功能下的学习成本，并提升易用性，统一体验是提升平台易用性的关键基础。同时有助于提升各角色间的协作效率。</p>
    </td>
  </tr>
  <tr>
    <td width="30%"><img src="https://qzonestyle.gtimg.cn/qzone/qzact/act/external/qdesign/Design/QLanguage/DesignConcept/jiyin.png"/></td>
    <td>
      <p><b>基因体现</b></p>
      <p>当今同质化的社交应用越来越多，QQ 作为横跨多时期多平台的社交应用，一方面需紧贴时代趋势，在众多应用中脱颖而出，另一方面有足够的历史底蕴，应强化自身基因特征，提升整体品牌认知。</p>
    </td>
  </tr>
  <tr>
    <td width="30%"><img src="https://qzonestyle.gtimg.cn/qzone/qzact/act/external/qdesign/Design/QLanguage/DesignConcept/xiangshan.png"/></td>
    <td>
      <p><b>社交向善</b></p>
      <p>社交应用会融入琳琅满目的娱乐化规则与玩法，但吸引年轻人的不应只是单纯娱乐消费，需要考虑社交娱乐的本质初心，QQ 更倡导用户在一个积极健康，安全贴心，触动情感的环境进行社交，并最终导人向善。</p>
    </td>
  </tr>
  <tr>
    <td width="30%"><img src="https://qzonestyle.gtimg.cn/qzone/qzact/act/external/qdesign/Design/QLanguage/DesignConcept/gaoxiao.png"/></td>
    <td>
      <p><b>高效娱乐</b></p>
      <p>伴随信息传播便利性提升，用户需要更高浓度的信息和更快的娱乐方式。用户时间愈加宝贵，偏向消费耗时较短的短视频、信息流等内容，希望更快找到喜欢的内容，以及更高浓度的内容。</p>
    </td>
  </tr>
  <tr>
    <td width="30%"><img src="https://qzonestyle.gtimg.cn/qzone/qzact/act/external/qdesign/Design/QLanguage/DesignConcept/xingqu.png"/></td>
    <td>
      <p><b>兴趣细分</b></p>
      <p>互联网使用场景更细分，兴趣爱好更加细分深入。各种兴趣圈、游戏圈、粉丝圈等年轻用户基于互联网衍生出来的圈子，需要有更细分深入的功能场景去承载。线上和线下联动是细分圈子持续活跃的关键。</p>
    </td>
  </tr>
  <tr>
    <td width="30%"><img src="https://qzonestyle.gtimg.cn/qzone/qzact/act/external/qdesign/Design/QLanguage/DesignConcept/yali.png"/></td>
    <td>
      <p><b>社交压力</b></p>
      <p>互联网信息传播的扩散效应，以及社会的复杂性给用户带来更多社交压力，原创越来越少。可以通过丰富的形象建立和维护体系增强用户的社交动力，引导产生更多原创内容和互动。</p>
    </td>
  </tr>
</table>

#### 腾讯 Q 语言原则 [^q-design-principles]

<table>
  <tr>
    <td width="80%"><img src="https://qzonestyle.gtimg.cn/qzone/qzact/act/external/qdesign/Design/QLanguage/DesignPrinciples/yuanze-004.gif"/></td>
    <td>
      <p><b>活力灵动</b></p>
      <p>对年轻人有吸引力，传递积极乐观情感，有怦然心动的感觉。</p>
    </td>
  </tr>
  <tr>
    <td width="80%"><img src="https://qzonestyle.gtimg.cn/qzone/qzact/act/external/qdesign/Design/QLanguage/DesignPrinciples/yuanze005.gif"/></td>
    <td>
      <p><b>亲和自然</b></p>
      <p>体验过程犹如与朋友打交道，亲和自然，懂我所想。</p>
    </td>
  </tr>
  <tr>
    <td width="80%"><img src="https://qzonestyle.gtimg.cn/qzone/qzact/act/external/qdesign/Design/QLanguage/DesignPrinciples/yuanze006.gif"/></td>
    <td>
      <p><b>自我有范</b></p>
      <p>用户能无压力表达自我，满足不同人群个性诉求。</p>
    </td>
  </tr>
</table>

### 语素

视觉基础是构成设计语言的最小单位，就像语素是语言中最小的音义结合体。在原子设计理论中，它属于最小粒度的元素，通常包括：色彩、布局、字体、图标等。

#### 色彩

无论 UI 还是平面，颜色是视觉传达的最核心也是最基本的语言，不同的主色，会给人不同的视觉感受，同样的主色不同的配色，视觉感受也会不同。通常一款产品的色彩体系包含：品牌色、功能色、中立色三个部分：

**品牌色**：代表品牌形象及 VI 识别的色彩，品牌色的数量可以一个也可以多个，用于主按钮、主 icon 等需要突出品牌特征的地方。

![](https://gw.alipayobjects.com/mdn/rms_08e378/afts/img/A*1c74TKxuEW4AAAAAAAAAAABkARQnAQ)

**功能色**：代表明确的信息以及状态，如成功、出错、失败、提醒等。功能色的选取需要遵守用户对色彩的基本认知，如绿色代表成功，红色代表警示或失败。

![](https://gw.alipayobjects.com/mdn/rms_08e378/afts/img/A*QY4JRa92gHQAAAAAAAAAAABkARQnAQ)

**中立色**：灰或饱和度低的颜色，用于界面设计中的字体、背景、边框、分割线等，中立色通常是按照透明度的方式实现。

![](https://gw.alipayobjects.com/zos/antfincdn/8yMmB1lcD%24/colors.jpg)

#### 布局

空间布局是体系化视觉设计的起点，和传统的平面设计的不同之处在于，UI 界面的布局空间要基于「动态、体系化」的角度出发展开。在中后台视觉体系中定义布局系统，可以从 5 个方面出发：统一的画板尺寸、适配方案、网格单位、栅格、常用模度。

**统一画板**：为了尽可能减少沟通与理解的成本，有必要在组织内部统一设计板的尺寸。

**适配**：在设计过程中还需要建立适配的概念，根据具体情况判断系统是否需要进行适配，以及哪些区块需要考虑动态布局。

左右布局的适配方案：常被用于左右布局的设计方案中，常见的做法是将左边的导航栏固定，对右边的工作区域进行动态缩放。

![](https://gw.alipayobjects.com/zos/rmsportal/vSqMhPolCtINKLvVVdLt.png)

上下布局的适配方案：常被用于上下布局的设计方案中，做法是对两边留白区域进行最小值的定义，当留白区域到达限定值之后再对中间的主内容区域进行动态缩放。

![](https://gw.alipayobjects.com/zos/rmsportal/VQEiJqtZfvvdyZSKcEsE.png)

**网格单位**：通过网格体系可以实现视觉体系的秩序。网格的基数为 8，不仅符合偶数的思路同时能够匹配多数主流的显示设备。通过建立网格的思考方式，还能帮助设计者快速实现布局空间的设计决策同时也能简化设计到开发的沟通损耗。

**栅格**：以上下布局的结构为例，对内容区域进行 24 栅格的划分设置，如下图所示。页面中栅格的 Gutter 设定了定值，即浏览器在一定范围扩大或缩小，栅格的 Column 宽度会随之扩大或缩小，但 Gutter 的宽度值固定不变。

![](https://gw.alipayobjects.com/zos/rmsportal/YPUZpPCzFgQHVxXCIAzq.png)

**模度**：模度是为了帮助不同设计能力的设计者们在界面布局上的一致性和韵律感，统一设计到开发的布局语言，减少还原损耗。

![](https://gw.alipayobjects.com/zos/rmsportal/ZBeDQMLMHLRfmUlUaaII.png)

#### 字体

字体是界面设计中最基本的构成之一。通过定义字体在设计上的使用规则，从而在阅读的舒适性上达到平衡。确定字体主要从下面四个方面出发：字体家族、主字体、字阶与行高、字重。

**字体家族**：优秀的字体系统首先是要选择合适的字体家族。提供一套利于屏显的备用字体库，来维护在不同平台以及浏览器的显示下，字体始终保持良好的易读性和可读性，体现了友好、稳定和专业的特性。在中后台系统中，数字经常需要进行纵向对比展示，将数字的字体 `font-variant-numeric` 设置为 `tabular-nums`，使其为等宽字体。

**主字体**：基于电脑显示器阅读距离（50 cm）以及最佳阅读角度（0.3），将自私设置为 14，以保证在多数常用显示器上的用户阅读效率最佳。

![](https://gw.alipayobjects.com/zos/rmsportal/yriUFbqOPtVniYYiikfb.png)

**字阶与行高**：字阶和行高决定着一套字体系统的动态与秩序之美。字阶是指一系列有规律的不同尺寸的字体。行高可以理解为一个包裹在字体外面的无形的盒子。

![](https://gw.alipayobjects.com/zos/rmsportal/xpykKKFJQorFJltdXkie.png)

**字重**：字重的选择同样基于秩序、稳定、克制的原则。多数情况下，只出现 regular 以及 medium 的两种字体重量，分别对应代码中的 400 和 500。在英文字体加粗的情况下会采用 semibold 的字体重量，对应代码中的 600。

| ![](https://gw.alipayobjects.com/zos/rmsportal/orIVrEOZIpjMbqZGiXEi.png) | ![](https://gw.alipayobjects.com/zos/rmsportal/sasWhUzTGjlZKftukraH.png) | ![](https://gw.alipayobjects.com/zos/rmsportal/QqxifAZlISrSUwnlonyx.png) |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |

#### 图标

图标是 UI 设计中必不可少的组成。通常我们理解图标设计的含义，是将某个概念转换成清晰易读的图形，从而降低用户的理解成本，提升界面的美观度。在我们的企业级应用设计范围中，图标在界面设计的诸多元素中往往只占了很小的比重，在调用时也会被缩到比设计稿小很多倍的尺寸，加上在图形素材极度丰富并且便于获取的今天，在产品设计体系中实现一套美观、一致、易用、便于延展的图标体系往往会被不小心忽略掉。

### 语句

组件就像由若干个语素组成的语句，比如一个基础按钮，通常就是由颜色、字体、边距等元素组成。而我们平时所说的组件库，其实就是一部词典，其中包含了设计系统中所需的基础组件与用法，在界面设计中也具有较高的通用性。

![](https://gw.alipayobjects.com/mdn/rms_08e378/afts/img/A*wsXrT7yQH2MAAAAAAAAAAABkARQnAQ)

### 语义

符号是语言的载体，但符号本身没有意义，只有被赋予含义的符号才能够被使用，这时候语言就转化为信息，而语言的含义就是语义。在视觉传达设计中也一样，使用的图标或图形，需具备正确的语义属性。如果商场导视设计中非要使用「裙子」图标来代表「男厕」入口，如此混淆语义挑战公众认知，那就等着被投诉吧。

### 语境

语境包含 3 个维度：一是流程意义上的上下文，二是产品属性中的语境，三是用户当下所处的环境。

当设计需要对上下文进行特别处理时，有可能对话的层级次序是受限于屏幕稀缺性，通常可采用 z-depth 叠加（Material Design 属性）、步骤条、元素关联转场动效等方式。举个常见的例子，当用户发起一个删除数据的请求时，界面会弹出一个二次确认的模态会话，用户点击确认之后才会执行删除操作。

针对用户当下所处的环境来适配界面语境，常见通过界面换肤的手法来实现，比如微信读书等阅读应用为用户提供白天模式或黑夜模式的选择。用户所处的外部环境因素可以很大程度上决定界面语言的应用，就好像在菜市场买东西要靠吼，在图书馆借书仅需要用肢体语言便能达成。

![](https://image.uisdc.com/wp-content/uploads/2019/06/uisdc-yy-20190624-8.jpg)

### 语气

交互界面通常需要使用说明或提示文案来指导用户完成操作，大多数情况下都是使用第二人称，就像在与用户对话，从以用户为中心的角度上讲，建议保持谦逊、友善的语气，尽可能避免使用晦涩的专业术语，谨慎使用带有强烈情感属性的感叹号，或过于口语化的语言。另外，语气的拿捏也将直接影响到与用户的距离感，以及当下的应景度。

{{% blockquote %}}
正确示例：使用检索可以快速搜索任务。
{{% /blockquote %}}

{{% blockquote type="error" %}}
不良示例：你一定会爱上方便快捷的检索功能！
{{% /blockquote %}}

### 语速

语速在这里指的是界面的信息密度，在不同的场合对语速的控制能够提升接受者的体验，视觉设计也同样需要注意把握间距与留白，网格系统在这里可以起到「节拍器」的作用，借助节拍器可以让设计更具节奏感。而交互意义上的语速，更多体现在操作路径的长度，以及动效的速率。

下图分别展示了 QQ 音乐和富途牛牛两种不同场景的「语速」：

![](/images/cn/2021-08-08-a-glimpse-of-design-language/qq-music.png)

![](/images/cn/2021-08-08-a-glimpse-of-design-language/futu-nn.png)

### 响度

其实就好像我们说话可以通过音量大小来控制信息的可感知程度，希望接受者听清楚的就说大声一点。汤姆奥斯本（Tom Osborne）的视觉响度指南（Visual Loudness Guide）是一个如何系统地处理按钮和链接的例子，它们不是单独列出，而是作为一个套件呈现，并且根据每个元素的视觉冲击力会相应的拥有一个「响度」值。我们在构建设计语言系统时，也同样需要设置梯级「响度」的按钮、字重等组件来满足不同场景的表达需求。

![](/images/cn/2021-08-08-a-glimpse-of-design-language/visual-loudness.png)

## 设计语言列表

| 企业      | 设计语言                                                     |
| ---------- | ------------------------------------------------------------ |
| <i class="icon icon-apple">Apple</i>      | [Human Interface Guidelines](https://developer.apple.com/design/) |
| <i class="icon icon-google">Google</i> | [Material Design](https://material.io/design)                |
| <i class="icon icon-microsoft">Microsoft</i> | [Fluent Design](https://www.microsoft.com/design/fluent)     |
| <i class="icon icon-facebook">Facebook</i>   | [Facebook Design](https://design.facebook.com/)              |
| <i class="icon icon-adobe">Adobe</i>      | [Spectrum](https://spectrum.adobe.com/)                      |
| <i class="icon icon-firefox">Firefox</i>    | [Photon Design](https://design.firefox.com/photon)           |
| <i class="icon icon-ibm">IBM</i>        | [Carbon Design System](https://www.carbondesignsystem.com/)  |
| <i class="icon icon-airbnb">Airbnb</i>     | [Lottie](https://airbnb.design/lottie/)                      |
| <i class="icon icon-salesforce">Salesforce</i> | [Lightning Design System](https://www.lightningdesignsystem.com/) |
| <i class="icon icon-ant-group">蚂蚁金服</i>   | [Ant Design](https://ant.design/)                            |
| <i class="icon icon-alibaba">阿里巴巴</i>   | [Fusion Design](https://alibaba.fusion.design/)              |
| <i class="icon icon-wechat">腾讯</i>       | [WeUI](https://weui.io/)                                     |
| <i class="icon icon-qq">腾讯</i>       | [Q Design](https://qq.design/)                               |

[^design-language-wikipedia]: https://en.wikipedia.org/wiki/Design_language

[^design-language-uisdc]: https://www.uisdc.com/design-language

[^ant-design-principle]: https://ant.design/docs/spec/overview-cn

[^fusion-design-values]: https://fusion.design/pc/doc/design/设计概览/12

[^q-design-concept]: https://qq.design/design/QLanguage/Concept/

[^q-design-principles]: https://qq.design/design/QLanguage/Principles/
