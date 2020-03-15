---
title: 国际智慧温室种植挑战赛 (International Autonomous Greenhouse Challenge)
author: 范叶亮
date: '2019-09-21'
slug: international-autonomous-greenhouse-challenge
categories:
  - 智慧农业
tags:
  - 农业
  - Agriculture
  - 智慧农业
  - Intelligent Agriculture
  - 荷兰
  - Netherlands
  - 瓦赫宁根大学
  - Wageningen University
  - 瓦赫宁根大学研究中心
  - Wageningen University & Research
  - Wageningen UR
  - 国际智慧温室种植
  - International Autonomous Greenhouse Challenge
  - 物联网
  - IoT
  - 番茄
  - 西红柿
  - Tomatos
  - 植物生长模型
  - Plant Growth Model
  - 机器学习
  - Machine Learning
  - 深度学习
  - Deep Learning
  - 强化学习
  - Reinforcement Learning
  - 知识图谱
  - Knowledge Graph
images:
  - /images/cn/2019-09-21-international-autonomous-greenhouse-challenge/hacking.jpg
  - /images/cn/2019-09-21-international-autonomous-greenhouse-challenge/me.jpg
  - /images/cn/2019-09-21-international-autonomous-greenhouse-challenge/lunch.jpg
  - /images/cn/2019-09-21-international-autonomous-greenhouse-challenge/agc-2019-teams.png
---

[国际智慧温室种植挑战赛](http://www.autonomousgreenhouses.com) 是一个由 [瓦赫宁根大学研究中心 (Wageningen University & Research)](https://www.wur.nl) 主办的旨在利用自动化、信息技术和人工智能技术控制温室以实现增加产量、降低成本等目标的大赛。第一届赛事的种植作物为黄瓜，第二届赛事为樱桃西红柿。

{{< photoswipe-gallery caption-position="bottom" caption-effect="fade" >}}
{{< photoswipe-figure link="/images/cn/2019-09-21-international-autonomous-greenhouse-challenge/cucumber.jpg" caption="黄瓜" >}}
{{< photoswipe-figure link="/images/cn/2019-09-21-international-autonomous-greenhouse-challenge/greenhouse.png" caption="温室" >}}
{{< photoswipe-figure link="/images/cn/2019-09-21-international-autonomous-greenhouse-challenge/tomatos.jpg" caption="西红柿" >}}
{{< /photoswipe-gallery >}}

很幸运能够在晚些时候加入到 CPlant 队伍中一同参与到这次赛事，虽然加入到队伍中比较晚，但工作之余也参与了大部分赛事的准备工作。

{{< photoswipe-gallery caption-position="bottom" caption-effect="fade" >}}
{{< photoswipe-figure link="/images/cn/2019-09-21-international-autonomous-greenhouse-challenge/greenhouse-1.jpg" caption="温室" >}}
{{< photoswipe-figure link="/images/cn/2019-09-21-international-autonomous-greenhouse-challenge/greenhouse-2.jpg" caption="温室" >}}
{{< photoswipe-figure link="/images/cn/2019-09-21-international-autonomous-greenhouse-challenge/greenhouse-3.jpg" caption="温室" >}}
{{< /photoswipe-gallery >}}

整个赛事分为初赛和复赛两个部分，初赛采用 Hackathon 的形式通过仿真模拟进行，初赛晋级的队伍将会在后续 6 个月的时间内通过远程控制进行真实的作物种植比赛。本次赛事吸引了全球顶级的农业与 AI 领域的企业、大学和研究机构参与，组成来自 26 个国家的 21 支团队，超过 200 名专家与学生。

{{< photoswipe-gallery caption-position="bottom" caption-effect="fade" >}}
{{< photoswipe-figure link="/images/cn/2019-09-21-international-autonomous-greenhouse-challenge/hacking.jpg" caption="Hacking" >}}
{{< photoswipe-figure link="/images/cn/2019-09-21-international-autonomous-greenhouse-challenge/me.jpg" caption="我" >}}
{{< photoswipe-figure link="/images/cn/2019-09-21-international-autonomous-greenhouse-challenge/lunch.jpg" caption="午餐" >}}
{{< /photoswipe-gallery >}}

初赛黑客马拉松评分主要由三部分组成：团队构成 （20％)、人工智能方法（30％)，以及虚拟西红柿种植净利润（50％)。仿真部分，采用了 Venlo 类型的温室，模拟时间从 2017/12/15 日至 2018/06/01，荷兰本地的外部天气，整个模拟过程并未考虑病虫害问题 (主要受到湿度影响)。仿真模型包含三个子模型：

1. Kaspro 温室模型
2. Intkam 作物模型
3. 经济模型

**Kaspro 温室模型**：主要通过温室的控制器 (例如：通风口，加热管道，CO<sub>2</sub> 补充器，遮阳帘，灌溉系统等) 控制温室内的环境变量 (例如：光照，温度，湿度，CO<sub>2</sub> 浓度，水量，水 EC 值等)，进而控制作物生长。环境控制模型是相对复杂的一个模型，因为控制器和环境变量之间并不是一对一的关系。

**Intkam 作物模型**：主要通过设置茎的密度，叶片的去留策略，去顶时间，果实个数保留策略等控制作物的生长。

**经济模型**：主要定义了不同时间、不同果重、不同糖分樱桃番茄的价格，不同时间段内光照、加热和 CO<sub>2</sub> 的成本，以及相关的人工成本。

最终经过 24 小时的 Hackathon，我们队伍的成绩如下，最后排名 **9/21**，很遗憾未能进入到决赛。

<table>
  <thead>
    <tr style="font-weight: bold;">
      <th width=20% style="text-align: center;">Team Composition (20%)</th>
      <th width=20% style="text-align: center;">Strategy and AI Approach for the Growing Challenge (30%)</th>
      <th width=20% style="text-align: center;">Obtained Points Following Rankings in Hackathon (50%)</th>
      <th width=20% style="text-align: center;">Obtained  Final Results in Hackathon (Net Profit)</th>
      <th width=20% style="text-align: center;">Total Score</th>
    </tr>
  </thead>
    <tr>
      <td style="text-align: center;">15.6 <br/> (Ranking 6/21) <br/> (Max: 17.6) <br/> (Min: 7.6)</td>
      <td style="text-align: center;">21.6 <br/> (Ranking 4/21) <br/> (Max: 23.1) <br/> (Min: 4.8)</td>
      <td style="text-align: center;">21 <br/> (Ranking 9/21) <br/> (Max: 50) <br/> (Min: 1)</td>
      <td style="text-align: center;">92.0 <br/> (Ranking 9/21) <br/> (Max: 154.5) <br/> (Min: 0.7)</td>
      <td style="text-align: center;">58.2 <br/> (Ranking 9/21) <br/> (Max: 88.8) <br/> (Min: 13.4)</td>
    </tr>
  <tbody>
  </tbody>
</table>

{{< photoswipe-figure link="/images/cn/2019-09-21-international-autonomous-greenhouse-challenge/agc-2019-teams.png" caption="Autonomous Greenhouse Challenge 2019" caption-position="bottom" caption-effect="fade" >}}

所在的 CPlant 队伍是本次比赛中人数最多的一只队伍 (21 人，最少的队伍为 5 人，虽然人最多却未能进入决赛 :disappointed_relieved:)，评审从国籍，研究和企业组成等多个角度对团队构成进行了评分，最终我们拿到了一个中等偏上的成绩。

人工智能方法方面是我们在准备过程中讨论比较多的内容，每个人根据自己的优势不同分别负责了 Plant Growth Model, Machine Learning, Deep Learning, Reinforcement Learning 和 Knowledge Graph 等不同部分的设计。答辩过程中多位评委对于我们的 Knowledge Graph 在整个人工智能中的应用很感兴趣，在最后点评中也提到我们是唯一一只提到 Knowledge Graph 及其在智慧农业中应用的队伍。我认为智慧农业不同于其他人工智能应用领域分支，其具有一定的特殊性，数据和实验并不像其他领域容易获取和实现，我们需要更多地结合农业科学本身的相关经验和知识。由于我之前从事过 NLP 和 Knowledge Graph 相关工作，我深信 Knowledge Graph 一定会是一个将农业和人工智能有机地结合起来的好工具，但至于如果结合和实现落地还需要进一步探索和研究。最终这部分我们拿到了一个相对不错的成绩。

分数占比最多的仿真部分我们做的有所欠缺，同时这也是我们最为陌生的一个部分。整个 Hackathon 从当地时间 12 日 13 时开始，至 13 日 13 时结束，我们通宵达旦，一整夜的 Coding 陪伴我们度过了中秋佳节。整个过程中我们几乎将全部的精力投入到了 Kaspro 温室模型参数的优化中来，Intkam 作物模型则是根据相关的农业经验进行了简单的优化配置，经济模型并没有直接的控制参数，而是通过相关投入和产出进行计算得到。通过不断的优化，净收益从 10 几分不断提高到 80 几分，后面则一直卡在了 80 几分未能进一步提高。整个 Hackathon 过程中，组委会不定时地公布一些不包含具体组名的成绩统计信息，在第一天白天就已经有队伍拿到了接近 100 分的成绩，在半夜的一次公布中有队伍已经拿到了接近 120 分的净收益。面对巨大的压力，我们仍不断地优化 Kaspro 温室模型参数，虽然成绩在稳步提高，但提高的幅度甚微。在临近比赛的时候，我们终于决定在 Intkam 作物模型做一些大胆的尝试，设置了一些现实中绝对不可能达到的参数，居然取得了很高的提升。在最后 10 几分钟内我们将成绩又提高了 10 分左右，但由于时间限制我们未能来得及进一步调整测试。

所有队伍的 Net Profit 和 Points 成绩从大到小排列结果如下：

![Net Profit & Points Result](/images/cn/2019-09-21-international-autonomous-greenhouse-challenge/net-profit-and-points-results.png)

一些与现实相差很远的参数设置却能够得到一个更好的结果，这个问题我们在最开始确实没有敢想。但其实开赛前的技术文件中有提及，整个模拟就是一个黑盒游戏，并没有任何规则可言，最终的评判准则只有净收益。虽然仿真模型与现实会有些差距，但对于这个单纯的游戏而言，先入为主的种植经验确实限制了我们的想象。而对于我这个正在朝着产品经理发展的野生程序猿而言，我正需要的就是这种想象和实践想象的能力，让我以胡适先生的一段话总结这次赛事的经验教训吧：

> 大胆的假设，小心的求证。  -- 胡适

## :muscle: 壮志未酬，来年再战！:muscle:

{{< load-photoswipe >}}
