---
title: 真实世界网络结构 (Structure of Real-World Network)
subtitle: 复杂网络系列
author: 范叶亮
date: '2020-11-28'
slug: structure-of-real-world-network
show_toc: true
toc_depth: 3
categories:
  - 机器学习
  - 复杂网络
tags:
  - 复杂网络
  - 分支
  - Components
  - 弱连通分支
  - Weakly Connected Component
  - 强连通分支
  - Strongly Connected Component
  - 外向分支
  - In-component
  - 内向分支
  - Out-component
  - 领结图
  - Bow Tie Diagram
  - 小世界效应
  - Small-world Effect
  - 度分布
  - Degree Distribution
  - 度序列
  - Degree Sequence
  - 幂律
  - Power Law
  - 无标度网络
  - Scale-free Network
  - 聚类系数
images:
  - /images/cn/2020-11-28-structure-of-real-world-network/components-in-an-undirected-network.png
---

> 本文为[《复杂网络系列》](/categories/复杂网络/)文章  
> 本文内容主要参考自：《网络科学引论》[^newman2014networks]

## 分支

在无向网络中，一个典型的现象是很多网络都有一个分支，该分支占据了网络的绝大部分，而剩余部分则被划分为大量的小分支，这些小分支之间彼此并不相连。如下图所示：

![](/images/cn/2020-11-28-structure-of-real-world-network/components-in-an-undirected-network.png)

一个网络通常不能有两个或更多占据网络大部分的大分支。如果将一个 `$n$` 个顶点的网络分解为两个分支，每个分支约为 `$\dfrac{1}{2} n$` 个顶点，则两个分支的顶点之间会有 `$\dfrac{1}{4} n^2$` 个顶点对，这些顶点对有可能一个顶点在一个大分支中，而另一个顶点在另外一个大分支中。如果在任何一个顶点对之间有一条边，那么这两个分支就会合并为一个分支。

有向图中分支分为两种：**弱连通分支**和**强连通分支**。弱连通分支的定义与无向网络的分支定义类似，强连通分支是指网络顶点的一个最大子集，该子集中的顶点能够通过有向路径到达其余所有顶点，同时也能够通过有向路径从其余所有顶点到达。

每个连通分支拥有**外向分支**（即从强连通分支中的任意顶点出发，沿着有向路径能够到达的所有顶点的集合）和**内向分支**（即沿着有向路径能够到达强连通分支的所有顶点的集合）。利用**“领结”图**可以很好地刻画有向网络的总体情况，万维网的“领结”图如下所示：

![](/images/cn/2020-11-28-structure-of-real-world-network/components-in-a-directed-network.png)

## 小世界效应

**小世界效应**（small-world effect）是指对于大多数网络而言，网络顶点之间的测地距离都惊人的小，例如：[六度分隔理论](https://zh.wikipedia.org/wiki/%E5%85%AD%E5%BA%A6%E5%88%86%E9%9A%94%E7%90%86%E8%AE%BA)。网络的数学模型显示出网络测地路径长度的数量级通常与网络定点数 `$n$` 成对数关系 ，即 `$\log n$`。

## 度分布

顶点的度是指连接到它的边的数量。**度分布**（degree distribution）`$p_k$` 是指网络中节点度的概率分布，也可以理解为从网络中随机选择一个顶点，其度为 `$k$` 的概率。**度序列**（degree sequence）是指所有顶点度的集合。

根据度 `$k$` 描述出大型网络的度分布有着非常重要的作用，下图给出了 Internet 的度分布：

![](/images/cn/2020-11-28-structure-of-real-world-network/degree-distribution-of-the-internet.png)

现实世界中，几乎所有网络的度分布都有类似的由度较大的核心顶点构成的尾部，统计上称为**右偏**（right-skewed）的。

## 幂律和无标度网络

以 Internet 为例，下图给出了度分布的一个有趣特征，下图使用了对数标度重新绘制了上图的直方图：

![](/images/cn/2020-11-28-structure-of-real-world-network/power-law-degree-distribution-of-the-internet.png)

如上图所示，对数处理后，分布大致遵循一条直线。度分布 `$p_k$` 的对数与度 `$k$` 的对数之间具有线性函数关系：

`$$
\ln p_k = - \alpha \ln k + c
$$`

对两侧同时做指数运算，有：

`$$
p_k = C k^{- \alpha}
$$`

其中，`$C = e^c$` 是一个常数。这种形式的分布，即按照 `$k$` 的幂变化，称为**幂律**（power law）。在不同类型的网络中，幂律度分布是普遍存在的，常数 `$\alpha$` 是幂律的指数，该值的典型取值区间为 `$2 \leq \alpha \leq 3$`。通常，度分布并非在整个区间都遵循幂律分布，当 `$k$` 较小时，度分布并不是单调的。具有幂律度分布的网络也称为**无标度网络**（scale-free network）。

观察幂律分布的另外一种方式是构建**累积分布函数**，定义如下：

`$$
P_k = \sum_{k' = k}^{\infty} p_{k'}
$$`

假设度分布 `$p_k$` 在尾部服从幂律，确切地讲，对于某个 `$k_{\min}$`，当 `$k \geq k_{\min}$` 时有 `$p_k = C k^{- \alpha}$`，则对于 `$k \geq k_{\min}$`，有：

`$$
P_{k}=C \sum_{k^{\prime}=k}^{\infty} k^{\prime-\alpha} \simeq C \int_{k}^{\infty} k^{\prime-\alpha} \mathrm{d} k^{\prime}=\frac{C}{\alpha-1} k^{-(\alpha-1)}
$$`

这里通过积分来近似求和是合理的，因为当 `$k$` 值较大时，幂律函数的变化率较小。所以，如果度分布 `$p_k$` 服从幂律，那么 `$p_k$` 的累积分布函数也服从幂律。

## 聚类系数

聚类系数是度量某个顶点的两个邻居顶点也互为邻居的平均概率。该测度计算值与随机条件下得到的期望值之间有较大的差异，这种巨大差异可能也显示出了真正发挥作用的社会效应。在合作网络中，与随机选择合作者相比，实际的合作网络中包含更多的三角形结构。这种现象背后有很多原因，其中一个原因可能是人们会介绍其合作者认识，而这些合作者两两之间也开始进行合作。

随着度的增加，局部聚类系数不断减少，这种现象的一个可能的解释是顶点分成紧密的群组或社团，同一个群组内部的顶点之间连接较多。在表现出此类行为的网络中，属于小型群组的顶点的度较小，因为这种群组的成员也相对较少，但在较大的群组中的顶点的度较大。同时，小型群组中的顶点的局部聚类系数较高。出现这种情况是因为将每个群组与网络的其余部分隔离开之后，每个群组大体上相当于一个小型网络，较小的网络会有更大的聚类系数。当对不同规模的网络取平均之后，会发现度小的顶点具有较高的聚类系数，如下图所示：

![](/images/cn/2020-11-28-structure-of-real-world-network/local-clustering-as-a-function-of-degree-on-the-internet.png)

[^newman2014networks]: Newman, M. E. J. (2014) _网络科学引论_. 电子工业出版社.
