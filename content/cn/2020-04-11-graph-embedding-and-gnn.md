---
title: 图嵌入 (Graph Embedding) 和图神经网络 (Graph Neural Network)
author: 范叶亮
date: '2020-04-11'
slug: graph-embedding-and-gnn
show_toc: true
toc_depth: 2
categories:
  - 深度学习
  - 表示学习
tags:
  - 图嵌入
  - 网络嵌入
  - 图表示学习
  - 网络表示学习
  - Graph Embedding
  - Random Walk
  - DeepWalk
  - node2vec
  - APP
  - Matrix Fractorization
  - GraRep
  - HOPE
  - Meta Paths
  - metapath2vec
  - HIN2Vec
  - SDNE
  - DNGR
  - LINE
  - 图神经网络
  - Graph Neural Networks
  - GNN
  - Graph Convolutional Networks
  - GCN
  - ChebNet
  - DCNN
  - GraphSAGE
  - Graph Recurrent Networks
  - GGNN
  - Tree LSTM
  - Graph LSTM
  - Graph Attention Networks
  - GAT
images:
  - /images/cn/2020-04-11-graph-embedding-and-gnn/graph-embedding-vs-graph-neural-networks.png
  - /images/cn/2020-04-11-graph-embedding-and-gnn/gnn-graph-types.png
  - /images/cn/2020-04-11-graph-embedding-and-gnn/gnn-training-methods.png
  - /images/cn/2020-04-11-graph-embedding-and-gnn/gnn-propagation-steps.png
---

图（Graph / Network）数据类型可以自然地表达物体和物体之间的联系，在我们的日常生活与工作中无处不在。例如：微信和新浪微博等构成了人与人之间的社交网络；互联网上成千上万个页面构成了网页链接网络；国家城市间的运输交通构成了物流网络。

{{% figure src="/images/cn/2020-04-11-graph-embedding-and-gnn/graph.png" title="图片来源：[The power of relationships in data](https://www.allthingsdistributed.com/2019/12/power-of-relationships.html)" %}}

通常定义一个图 `$G = \left(V, E\right)$`，其中 `$V$` 为**顶点（Vertices）**集合，`$E$` 为**边（Edges）**集合。对于一条边 `$e = u, v$` 包含两个**端点（Endpoints）** `$u$` 和 `$v$`，同时 `$u$` 可以称为 `$v$` 的**邻居（Neighbor）**。当所有的边为有向边时，图称之为**有向（Directed）**图，当所有边为无向边时，图称之为**无向（Undirected）**图。对于一个顶点 `$v$`，令 `$d \left(v\right)$` 表示连接的边的数量，称之为**度（Degree）**。对于一个图 `$G = \left(V, E\right)$`，其**邻接矩阵（Adjacency Matrix）** `$A \in \mathbb{A}^{|V| \times |V|}$` 定义为：

`$$
A_{i j}=\left\{\begin{array}{ll}
1 & \text { if }\left\{v_{i}, v_{j}\right\} \in E \text { and } i \neq j \\
0 & \text { otherwise }
\end{array}\right.
$$`

作为一个典型的非欧式数据，对于图数据的分析主要集中在节点分类，链接预测和聚类等。对于图数据而言，**图嵌入（Graph / Network Embedding）**和**图神经网络（Graph Neural Networks, GNN）**是两个类似的研究领域。图嵌入旨在将图的节点表示成一个低维向量空间，同时保留网络的拓扑结构和节点信息，以便在后续的图分析任务中可以直接使用现有的机器学习算法。一些基于深度学习的图嵌入同时也属于图神经网络，例如一些基于图自编码器和利用无监督学习的图卷积神经网络等。下图描述了图嵌入和图神经网络之间的差异：

{{< figure src="/images/cn/2020-04-11-graph-embedding-and-gnn/graph-embedding-vs-graph-neural-networks.png" >}}

{{% blockquote type="warn" %}}
本文中**图嵌入**和**网络表示学习**均表示 Graph / Network Embedding。
{{% /blockquote %}}

## 图嵌入

> 本节内容主要参考自：  
> A Comprehensive Survey of Graph Embedding: Problems, Techniques and Applications [^cai2018comprehensive]  
> Graph Embedding Techniques, Applications, and Performance: A Survey [^goyal2018graph]  
> Representation Learning on Graphs: Methods and Applications [^hamilton2017representation]

使用邻接矩阵的网络表示存在计算效率的问题，邻接矩阵 `$A$` 使用 `$|V| \times |V|$` 的存储空间表示一个图，随着节点个数的增长，这种表示所需的空间成指数增长。同时，在邻接矩阵中绝大多数是 0，数据的稀疏性使得快速有效的学习方式很难被应用。

网路表示学习是指学习得到网络中节点的低维向量表示，形式化地，网络表示学习的目标是对每个节点 `$v \in V$` 学习一个实值向量 `$R_v \in \mathbb{R}^k$`，其中 `$k \ll |V|$` 表示向量的维度。经典的 Zachary's karate club 网络的嵌入可视化如下图所示：

{{< figure src="/images/cn/2020-04-11-graph-embedding-and-gnn/karate-graph-embedding.png" >}}

### Random Walk

基于随机游走的图嵌入通过使得图上一个短距的随机游走中共现的节点具有更相似的表示的方式来优化节点的嵌入。

#### DeepWalk

DeepWalk [^perozzi2014deepwalk] 算法主要包含两个部分：一个随机游走序列生成器和一个更新过程。随机游走序列生成器首先在图 `$G$` 中均匀地随机抽样一个随机游走 `$\mathcal{W}_{v_i}$` 的根节点 `$v_i$`，接着从节点的邻居中均匀地随机抽样一个节点直到达到设定的最大长度 `$t$`。对于一个生成的以 `$v_i$` 为中心左右窗口为 `$w$` 的随机游走序列 `$v_{i-w}, \dotsc, v_{i-1}, v_i, v_{i+1}, \dotsc, v_{i+m}$`，DeepWalk 利用 SkipGram 算法通过最大化以 `$v_i$` 为中心，左右 `$w$` 为窗口的同其他节点共现概率来优化模型：

`$$
\text{Pr} \left(\left\{v_{i-w}, \dotsc, v_{i+w}\right\} \setminus v_i \mid \Phi \left(v_i\right)\right) = \prod_{j=i-w, j \neq i}^{i+w} \text{Pr} \left(v_j \mid \Phi \left(v_i\right)\right)
$$`

DeepWalk 和 Word2Vec 的类比如下表所示：

| 模型     | 目标 | 输入     | 输出     |
| -------- | ---- | -------- | -------- |
| Word2Vec | 词   | 句子     | 词嵌入   |
| DeepWalk | 节点 | 节点序列 | 节点嵌入 |

#### node2vec

node2vec [^grover2016node2vec] 通过改变随机游走序列生成的方式进一步扩展了 DeepWalk 算法。DeepWalk 选取随机游走序列中下一个节点的方式是均匀随机分布的，而 node2vec 通过引入两个参数 `$p$` 和 `$q$`，将**宽度优先搜索**和**深度优先搜索**引入了随机游走序列的生成过程。 宽度优先搜索注重邻近的节点并刻画了相对局部的一种网络表示， 宽度优先中的节点一般会出现很多次，从而降低刻画中心节点的邻居节点的方差， 深度优先搜索反映了更高层面上的节点之间的同质性。

{{< figure src="/images/cn/2020-04-11-graph-embedding-and-gnn/node2vec.png" >}}

node2vec 中的两个参数 `$p$` 和 `$q$` 控制随机游走序列的跳转概率。假设上一步游走的边为 `$\left(t, v\right)$`， 那么对于节点 `$v$` 的不同邻居，node2vec 根据 `$p$` 和 `$q$` 定义了不同的邻居的跳转概率，`$p$` 控制跳向上一个节点的邻居的概率，`$q$` 控制跳向上一个节点的非邻居的概率，具体的未归一的跳转概率值 `$\pi_{vx} = \alpha_{pq} \left(t, x\right)$` 如下所示：

`$$
\alpha_{p q}(t, x)=\left\{\begin{array}{cl}
\dfrac{1}{p}, & \text { if } d_{t x}=0 \\
1, & \text { if } d_{t x}=1 \\
\dfrac{1}{q}, & \text { if } d_{t x}=2
\end{array}\right.
$$`

其中，`$d_{tx}$` 表示节点 `$t$` 和 `$x$` 之间的最短距离。为了获得最优的超参数 `$p$` 和 `$q$` 的取值，node2vec 通过半监督形式，利用网格搜索最合适的参数学习节点表示。

#### APP

之前的基于随机游走的图嵌入方法，例如：DeepWalk，node2vec 等，都无法保留图中的非对称信息。然而非对称性在很多问题，例如：社交网络中的链路预测、电商中的推荐等，中至关重要。在有向图和无向图中，非对称性如下图所示：

{{< figure src="/images/cn/2020-04-11-graph-embedding-and-gnn/asymmetric-proximity.png" >}}

为了保留图的非对称性，对于每个节点 `$v$` 设置两个不同的角色：源和目标，分别用 `$\overrightarrow{s_{v}}$` 和 `$\overrightarrow{t_{v}}$` 表示。对于每个从 `$u$` 开始以 `$v$` 结尾的采样序列，利用 `$(u, v)$` 表示采样的节点对。则利用源节点 `$u$` 预测目标节点 `$v$` 的概率如下：

`$$
p(v | u)=\frac{\exp (\overrightarrow{s_{u}} \cdot \overrightarrow{t_{v}})}{\sum_{n \in V} \exp (\overrightarrow{s_{u}} \cdot \overrightarrow{t_{n}})}
$$`

通过 Skip-Gram 和负采样对模型进行优化，损失函数如下：

`$$
\begin{aligned}
\ell &= \log \sigma(\overrightarrow{s_{u}} \cdot \overrightarrow{t_{v}})+k \cdot E_{t_{n} \sim P_{D}}[\log \sigma(-\overrightarrow{s_{u}} \cdot \overrightarrow{t_{n}})] \\
&= \sum_{u} \sum_{v} \# \text {Sampled}_{u}(v) \cdot \left(\log \sigma(\overrightarrow{s_{u}} \cdot \overrightarrow{t_{v}}) + k \cdot E_{t_{n} \sim P_{D}}[\log \sigma(-\overrightarrow{s_{u}} \cdot \overrightarrow{t_{n}})]\right)
\end{aligned}
$$`

其中，我们根据分布 `$P_D \left(n\right) \sim \dfrac{1}{|V|}$` 随机负采样 `$k$` 个节点对，`$\# \text{Sampled}_{u}(v)$` 为采样的 `$\left(u, v\right)$` 对的个数，`$\sigma$` 为 sigmoid 函数。通常情况下，`$\# \text{Sampled}_{u}(v) \neq \# \text{Sampled}_{v}(u)$`，即 `$\left(u, v\right)$` 和 `$\left(v, u\right)$` 的观测数量是不同的。模型利用 Monte-Carlo End-Point 采样方法 [^fogaras2005towards] 随机的以 `$v$` 为起点和 `$\alpha$` 为停止概率采样 `$p$` 条路径。这种采样方式可以用于估计任意一个节点对之间的 Rooted PageRank [^haveliwala2002topic] 值，模型利用这个值估计由 `$v$` 到达 `$u$` 的概率。

### Matrix Fractorization

#### GraRep

GraRep [^cao2015grarep] 提出了一种基于矩阵分解的图嵌入方法。对于一个图 `$G$`，利用邻接矩阵 `$S$` 定义图的度矩阵：

`$$
D_{i j}=\left\{\begin{array}{ll}
\sum_{p} S_{i p}, & \text { if } i=j \\
0, & \text { if } i \neq j
\end{array}\right.
$$`

则一阶转移概率矩阵定义如下：

`$$
A = D^{-1} S
$$`

其中，`$A_{i, j}$` 表示通过一步由 `$v_i$` 转移到 `$v_j$` 的概率。所谓的全局特征包含两个部分：

1. 捕获两个节点之间的长距离特征
2. 分别考虑按照不同转移步数的连接

下图展示了 `$k = 1, 2, 3, 4$` 情况下的强（上）弱（下）关系：

{{< figure src="/images/cn/2020-04-11-graph-embedding-and-gnn/grarep.png" >}}

利用 Skip-Gram 和 NCE（noise contrastive estimation）方法，对于一个 `$k$` 阶转移，可以将模型归结到一个矩阵 `$Y_{i, j}^k$` 的分解问题：

`$$
Y_{i, j}^{k}=W_{i}^{k} \cdot C_{j}^{k}=\log \left(\frac{A_{i, j}^{k}}{\sum_{t} A_{t, j}^{k}}\right)-\log (\beta)
$$`

其中，`$W$` 和 `$C$` 的每一行分别为节点 `$w$` 和 `$c$` 的表示，`$\beta = \lambda / N$`，`$\lambda$` 为负采样的数量，`$N$` 为图中边的个数。

之后为了减少噪音，模型将 `$Y^k$` 中所有的负值替换为 0，通过 SVD（方法详情见参见[之前博客](/cn/2017/12/evd-svd-and-pca/)）得到节点的 `$d$` 维表示：

`$$
\begin{aligned}
X_{i, j}^{k} &= \max \left(Y_{i, j}^{k}, 0\right) \\
X^{k} &= U^{k} \Sigma^{k}\left(V^{k}\right)^{T} \\
X^{k} \approx X_{d}^{k} &= U_{d}^{k} \Sigma_{d}^{k}\left(V_{d}^{k}\right)^{T} \\
X^{k} \approx X_{d}^{k} &= W^{k} C^{k} \\
W^{k} &= U_{d}^{k}\left(\Sigma_{d}^{k}\right)^{\frac{1}{2}} \\
C^{k} &= \left(\Sigma_{d}^{k}\right)^{\frac{1}{2}} V_{d}^{k T}
\end{aligned}
$$`

最终，通过对不同 `$k$` 的表示进行拼接得到节点最终的表示。

#### HOPE

HOPE [^ou2016asymmetric] 对于每个节点最终生成两个嵌入表示：一个是作为源节点的嵌入表示，另一个是作为目标节点的嵌入表示。模型通过近似高阶相似性来保留非对称传递性，其优化目标为：

`$$
\min \left\|\mathbf{S}-\mathbf{U}^{s} \cdot \mathbf{U}^{t^{\top}}\right\|_{F}^{2}
$$`

其中，`$\mathbf{S}$` 为相似矩阵，`$\mathbf{U}^s$` 和 `$\mathbf{U}^t$` 分别为源节点和目标节点的向量表示。下图展示了嵌入向量可以很好的保留非对称传递性：

{{< figure src="/images/cn/2020-04-11-graph-embedding-and-gnn/hope.png" >}}

对于 `$\mathbf{S}$` 有多种可选近似度量方法：Katz Index，Rooted PageRank（RPR），Common Neighbors（CN），Adamic-Adar（AA）。这些度量方法可以分为两类：全局近似（Katz Index 和 RPR）和局部近似（CN 和 AA）。

算法采用了一个广义 SVD 算法（JDGSVD）来解决使用原始 SVD 算法计算复杂度为`$O \left(N^3\right)$` 过高的问题，从而使得算法可以应用在更大规模的图上。

### Meta Paths

#### matapath2vec

matapath2vec [^dong2017metapath2vec] 提出了一种基于元路径的异构网络表示学习方法。在此我们引入 3 个定义：

1. **异构网络（(Heterogeneous information network，HIN）**可以定义为一个有向图 `$G = \left(V, E\right)$`，一个节点类型映射 `$\tau: V \to A$` 和一个边类型映射 `$\phi: E \to R$`，其中对于 `$v \in V$` 有 `$\tau \left(v\right) \in A$`，`$e \in E$` 有 `$\phi \left(e\right) \in R$`，且 `$|A| + |R| > 1$`。
2. **网络模式（Network schema）**定义为 `$T_G = \left(A, R\right)$`，为一个包含节点类型映射 `$\tau \left(v\right) \in A$` 和边映射 `$\phi \left(e\right) \in R$` 异构网络的 `$G = \left(V, E\right)$` 的元模板。
3. **元路径（Meta-path）**定义为网络模式 `$T_G = \left(A, R\right)$` 上的一条路径 `$P$`，形式为 `$A_{1} \stackrel{R_{1}}{\longrightarrow} A_{2} \stackrel{R_{2}}{\longrightarrow} \cdots \stackrel{R_{l}}{\longrightarrow} A_{l+1}$`。

下图展示了一个学术网络和部分元路径：

{{< figure src="/images/cn/2020-04-11-graph-embedding-and-gnn/metapaths.png" >}}

其中，APA 表示一篇论文的共同作者，APVPA 表示两个作者在同一个地方发表过论文。

metapath2vec 采用了基于元路径的随机游走来生成采样序列，这样就可以保留原始网络中的语义信息。对于一个给定的元路径模板 `$P: A_{1} \stackrel{R_{1}}{\longrightarrow} A_{2} \stackrel{R_{2}}{\longrightarrow} \cdots A_{t} \stackrel{R_{t}}{\longrightarrow} A_{t+1} \cdots \stackrel{R_{l}}{\longrightarrow} A_{l}$`，第 `$i$` 步的转移概率为：

`$$
p\left(v^{i+1} | v_{t}^{i}, P\right)=\left\{\begin{array}{ll}
\dfrac{1}{\left|N_{t+1}\left(v_{t}^{i}\right)\right|} & \left(v_{t}^{i}, v^{i+1}\right) \in E, \phi\left(v^{i+1}\right)=A_{t+1} \\
0 & \left(v_{t}^{i}, v^{i+1}\right) \in E, \phi\left(v^{i+1}\right) \neq A_{t+1} \\
0 & \left(v_{t}^{i}, v^{i+1}\right) \notin E
\end{array}\right.
$$`

其中，`$v^i_t \in A_t$`，`$N_{t+1} \left(v^i_t\right)$` 表示节点 `$v^i_t$` 类型为 `$A_{t+1}$` 的邻居。之后，则采用了类似 DeepWalk 的方式进行训练得到节点表示。

#### HIN2Vec

HIN2Vec [^fu2017hin2vec] 提出了一种利用多任务学习通过多种关系进行节点和元路径表示学习的方法。模型最初是希望通过一个多分类模型来预测任意两个节点之间所有可能的关系。假设对于任意两个节点，所有可能的关系集合为 `$R = \{\text{P-P, P-A, A-P, P-P-P, P-P-A, P-A-P, A-P-P, A-P-A}\}$`。假设一个实例 `$P_1$` 和 `$A_1$` 包含两种关系：`$\text{P-A}$` 和 `$\text{P-P-A}$`，则对应的训练数据为 `$\langle x: P_1, y: A_1, output: \left[0, 1, 0, 0, 1, 0, 0, 0\right] \rangle$`。

但实际上，扫描整个网络寻找所有可能的关系是不现实的，因此 HIN2Vec 将问题简化为一个给定两个节点判断之间是否存在一个关系的二分类问题，如下图所示：

{{< figure src="/images/cn/2020-04-11-graph-embedding-and-gnn/hin2vec.png" >}}

模型的三个输入分别为节点 `$x$` 和 `$y$`，以及关系 `$r$`。在隐含层输入被转换为向量 `$W_{X}^{\prime} \vec{x}, W_{Y}^{\prime} \vec{y}$` 和 `$f_{01}\left(W_{R}^{\prime} \vec{r}\right)$`。需要注意对于关系 `$r$`，模型应用了一个正则化函数 `$f_{01} \left(\cdot\right)$` 使得 `$r$` 的向量介于 `$0$` 和 `$1$` 之间。之后采用逐元素相乘对三个向量进行汇总 `$W_{X}^{\prime} \vec{x} \odot W_{Y}^{\prime} \vec{y} \odot f_{01}\left(W_{R}^{\prime} \vec{r}\right)$`。在最后的输出层，通过计算 `$sigmoid \left(\sum W_{X}^{\prime} \vec{x} \odot W_{Y}^{\prime} \vec{y} \odot f_{01}\left(W_{R}^{\prime} \vec{r}\right)\right)$` 得到最终的预测值。

在生成训练数据时，HIN2Vec 采用了完全随机游走进行节点采样，而非 metapath2vec 中的按照给定的元路径的方式。通过随机替换 `$x, y, r$` 中的任何一个可以生成负样本，但当网络中的关系数量较少，节点数量远远大于关系数量时，这种方式很可能产生错误的负样本，因此 HIN2Vec 只随机替换 `$x, y$`，保持 `$r$` 不变。

### Deep Learning

#### SDNE

SDNE [^wang2016structural] 提出了一种利用自编码器同时优化一阶和二阶相似度的图嵌入算法，学习得到的向量能够保留局部和全局的结构信息。SDNE 使用的网络结构如下图所示：

{{< figure src="/images/cn/2020-04-11-graph-embedding-and-gnn/sdne.png" >}}

对于二阶相似度，自编码器的目标是最小化输入和输出的重构误差。SDNE 采用邻接矩阵作为自编码器的输入，`$\mathbf{x}_i = \mathbf{s}_i$`，每个 `$\mathbf{s}_i$` 包含了节点 `$v_i$` 的邻居结构信息。模型的损失函数如下：

`$$
\mathcal{L}=\sum_{i=1}^{n}\left\|\hat{\mathbf{x}}_{i}-\mathbf{x}_{i}\right\|_{2}^{2}
$$`

由于网络的稀疏性，邻接矩阵中的非零元素远远少于零元素，因此模型采用了一个带权的损失函数：

`$$
\begin{aligned}
\mathcal{L}_{2nd} &=\sum_{i=1}^{n}\left\|\left(\hat{\mathbf{x}}_{i}-\mathbf{x}_{i}\right) \odot \mathbf{b}_{i}\right\|_{2}^{2} \\
&=\|(\hat{X}-X) \odot B\|_{F}^{2}
\end{aligned}
$$`

其中，`$\odot$` 表示按位乘，`$\mathbf{b}_i = \left\{b_{i, j}\right\}_{j=1}^{n}$`，如果 `$s_{i, j} = 0$` 则 `$b_{i, j} = 1$` 否则 `$b_{i, j} = \beta > 1$`。

对于一阶相似度，模型利用了一个监督学习模块最小化节点在隐含空间中距离。损失函数如下：

`$$
\begin{aligned}
\mathcal{L}_{1st} &=\sum_{i, j=1}^{n} s_{i, j}\left\|\mathbf{y}_{i}^{(K)}-\mathbf{y}_{j}^{(K)}\right\|_{2}^{2} \\
&=\sum_{i, j=1}^{n} s_{i, j}\left\|\mathbf{y}_{i}-\mathbf{y}_{j}\right\|_{2}^{2}
\end{aligned}
$$`

最终，模型联合损失函数如下：

`$$
\begin{aligned}
\mathcal{L}_{mix} &=\mathcal{L}_{2nd}+\alpha \mathcal{L}_{1st}+\nu \mathcal{L}_{reg} \\
&=\|(\hat{X}-X) \odot B\|_{F}^{2}+\alpha \sum_{i, j=1}^{n} s_{i, j}\left\|\mathbf{y}_{i}-\mathbf{y}_{j}\right\|_{2}^{2}+\nu \mathcal{L}_{reg}
\end{aligned}
$$`

其中，`$\mathcal{L}_{reg}$` 为 L2 正则项。

#### DNGR

DNGR [^cao2016deep] 提出了一种利用基于 Stacked Denoising Autoencoder（SDAE）提取特征的网络表示学习算法。算法的流程如下图所示：

{{< figure src="/images/cn/2020-04-11-graph-embedding-and-gnn/dngr.png" >}}

模型首先利用 Random Surfing 得到一个概率共现（PCO）矩阵，之后利用其计算得到 PPMI 矩阵，最后利用 SDAE 进行特征提取得到节点的向量表示。

对于传统的将图结构转换为一个线性序列方法存在几点缺陷：

1. 采样序列边缘的节点的上下文信息很难被捕捉。
2. 很难直接确定游走的长度和步数等超参数，尤其是对于大型网络来说。

受 PageRank 思想影响，作者采用了 Random Surfing 模型。定义转移矩阵 `$A$`，引入行向量 `$p_k$`，第 `$j$` 个元素表示通过 `$k$` 步转移之后到达节点 `$j$` 的概率。`$p_0$` 为一个初始向量，其仅第 `$i$` 个元素为 1，其它均为 0。在考虑以 `$1 - \alpha$` 的概率返回初始节点的情况下有：

`$$
p_{k}=\alpha \cdot p_{k-1} A+(1-\alpha) p_{0}
$$`

在不考虑返回初始节点的情况下有：

`$$
p_{k}^{*}=p_{k-1}^{*} A=p_{0} A^{k}
$$`

直观而言，两个节点越近，两者的关系越亲密，因此通过同当前节点的相对距离来衡量上下文节点的重要性是合理的。基于此，第 `$i$` 个节点的表示可以用如下方式构造：

`$$
r=\sum_{k=1}^{K} w(k) \cdot p_{k}^{*}
$$`

其中，`$w \left(\cdot\right)$` 是一个衰减函数。

利用 PCO 计算得到 PPMI 后，再利用一个 SDAE 进行特征提取。Stacking 策略可以通过不同的网络层学习得到不同层级的表示，Denoising 策略则通过去除数据中的噪声，增加结果的鲁棒性。同时，SNGR 相比基于 SVD 的方法效率更高。

### Others

#### LINE

LINE [^tang2015line] 提出了一个用于大规模网络嵌入的方法，其满足如下 3 个要求：

1. 同时保留节点之间的一阶相似性（first-order proximity）和二阶相似性（second-order proximity）。
2. 可以处理大规模网络，例如：百万级别的顶点和十亿级别的边。
3. 可以处理有向，无向和带权的多种类型的图结构。

给定一个无向边 `$\left(i, j\right)$`，点 `$v_i$` 和 `$v_j$` 的联合概率如下：

`$$
p_{1}\left(v_{i}, v_{j}\right)=\frac{1}{1+\exp \left(-\vec{u}_{i}^{T} \cdot \vec{u}_{j}\right)}
$$`

其中，`$\vec{u}_{i} \in R^{d}$` 为节点 `$v_i$` 的低维向量表示。在空间 `$V \times V$` 上，分布 `$p \left(\cdot, \cdot\right)$` 的经验概率为 `$\hat{p}_1 \left(i, j\right) = \dfrac{w_{ij}}{V}$`，其中 `$W = \sum_{\left(i, j\right) \in E} w_{ij}$`。通过最小化两个分布的 KL 散度来优化模型，则目标函数定义如下：

`$$
O_{1}=-\sum_{(i, j) \in E} w_{i j} \log p_{1}\left(v_{i}, v_{j}\right)
$$`

需要注意的是一阶相似度仅可用于无向图，通过最小化上述目标函数，我们可以将任意顶点映射到一个 `$d$` 维空间向量。

二阶相似度既可以用于无向图，也可以用于有向图。二阶相似度假设共享大量同其他节点连接的节点之间是相似的，每个节点被视为一个特定的上下文，则在上下文上具有类似分布的节点是相似的。在此，引入两个向量 `$\vec{u}_{i}$` 和 `$\vec{u}_{\prime i}$`，其中 `$\vec{u}_{i}$` 是 `$v_i$` 做为节点的表示，`$\vec{u}_{\prime i}$` 是 `$v_i$` 做为上下文的表示。对于一个有向边 `$\left(i, j\right)$`，由 `$v_i$` 生成上下文 `$v_j$` 的概率为：

`$$
p_{2}\left(v_{j} | v_{i}\right)=\frac{\exp \left(\vec{u}_{j}^{\prime T} \cdot \vec{u}_{i}\right)}{\sum_{k=1}^{|V|} \exp \left(\vec{u}_{k}^{\prime T} \cdot \vec{u}_{i}\right)}
$$`

其中，`$|V|$` 为节点或上下文的数量。在此我们引入一个参数 `$\lambda_i$` 用于表示节点 `$v_i$` 的重要性程度，重要性程度可以利用度或者 PageRank 算法进行估计。经验分布 `$\hat{p}_{2}\left(\cdot \mid v_{i}\right)$` 定义为 `$\hat{p}_{2}\left(v_{j} \mid v_{i}\right)=\dfrac{w_{i j}}{d_{i}}$`，其中 `$w_{ij}$` 为边 `$\left(i, j\right)$` 的权重，`$d_i$` 为节点 `$v_i$` 的出度。LINE 中采用 `$d_i$` 作为节点的重要性 `$\lambda_i$`，利用 KL 散度同时忽略一些常量，目标函数定义如下：

`$$
O_{2}=-\sum_{(i, j) \in E} w_{i j} \log p_{2}\left(v_{j} \mid v_{i}\right)
$$`

LINE 采用负采样的方式对模型进行优化，同时利用 Alias 方法 [^walker1974new] [^walker1977efficient] 加速采样过程。

## 图神经网络

> 本节内容主要参考自：  
> Deep Learning on Graphs: A Survey [^zhang2020deep]  
> A Comprehensive Survey on Graph Neural Networks [^wu2020comprehensive]  
> Graph Neural Networks: A Review of Methods and Applications [^zhou2018graph]  
> Introduction to Graph Neural Networks [^liu2020introduction]

图神经网络（Graph Neural Network，GNN）最早由 Scarselli 等人 [^scarselli2008graph] 提出。图中的一个节点可以通过其特征和相关节点进行定义，GNN 的目标是学习一个状态嵌入 `$\mathbf{h}_v \in \mathbb{R}^s$` 用于表示每个节点的邻居信息。状态嵌入 `$\mathbf{h}_v$` 可以生成输出向量 `$\mathbf{o}_v$` 用于作为预测节点标签的分布等。

下面三张图分别从图的类型，训练方法和传播过程角度列举了不同 GNN 的变种 [^zhou2018graph]。

{{< figure src="/images/cn/2020-04-11-graph-embedding-and-gnn/gnn-graph-types.png" >}}

{{< figure src="/images/cn/2020-04-11-graph-embedding-and-gnn/gnn-training-methods.png" >}}

{{< figure src="/images/cn/2020-04-11-graph-embedding-and-gnn/gnn-propagation-steps.png" >}}

下面我们主要从模型的角度分别介绍不同种类的 GNN。

### Graph Neural Networks

为了根据邻居更新节点的状态，定义一个用于所有节点的函数 `$f$`，称之为 _local transition function_。定义一个函数 `$g$`，用于生成节点的输出，称之为 _local output function_。有：

`$$
\begin{array}{c}
\mathbf{h}_{v}=f\left(\mathbf{x}_{v}, \mathbf{x}_{co[v]}, \mathbf{h}_{ne[v]}, \mathbf{x}_{ne[v])}\right. \\
\mathbf{o}_{v}=g\left(\mathbf{h}_{v}, \mathbf{x}_{v}\right)
\end{array}
$$`

其中，`$\mathbf{x}$` 表示输入特征，`$\mathbf{h}$` 表示隐含状态。`$co[v]$` 为连接到节点 `$v$` 的边集，`$ne[v]$` 为节点 `$v$` 的邻居。

{{< figure src="/images/cn/2020-04-11-graph-embedding-and-gnn/graph-example.png" >}}

上图中，`$\mathbf{x}_1$` 表示 `$l_1$` 的输入特征，`$co[l_1]$` 包含了边 `$l_{(1, 4)}, l_{(6, 1)}, l_{(1, 2)}$` 和 `$l_{(3, 1)}$`，`$ne[l_1]$` 包含了节点 `$l_2, k_3, l_4$` 和 `$l_6$`。

令 `$\mathbf{H}, \mathbf{O}, \mathbf{X}$` 和 `$\mathbf{X}_N$` 分别表示状态、输出、特征和所有节点特征的向量，有：

`$$
\begin{aligned}
&\mathbf{H}=F(\mathbf{H}, \mathbf{X})\\
&\mathbf{O}=G\left(\mathbf{H}, \mathbf{X}_{N}\right)
\end{aligned}
$$`

其中，`$F$` 为 _global transition function_，`$G$` 为 _global output function_，分别为图中所有节点的 local transition function `$f$` 和 local output function `$g$` 的堆叠版本。依据 Banach 的 Fixed Point Theorem [^khamsi2011introduction]，GNN 利用传统的迭代方式计算状态：

`$$
\mathbf{H}^{t+1}=F\left(\mathbf{H}^{t}, \mathbf{X}\right)
$$`

其中，`$\mathbf{H}^t$` 表示第  `$t$` 论循环 `$\mathbf{H}$` 的值。

介绍完 GNN 的框架后，下一个问题就是如果学习得到 local transition function `$f$` 和 local output function `$g$`。在包含目标信息（`$\mathbf{t}_v$` 对于特定节点）的监督学习情况下，损失为：

`$$
loss = \sum_{i=1}^{p} \left(\mathbf{t}_i - \mathbf{o}_i\right)
$$`

其中，`$p$` 为用于监督学习的节点数量。利用基于梯度下降的学习方法优化模型后，我们可以得到针对特定任务的训练模型和图中节点的隐含状态。

尽管实验结果表明 GNN 是一个用于建模结构数据的强大模型，但对于一般的 GNN 模型仍存在如下缺陷：

1. 对于固定点，隐含状态的更新是低效地。
2. GNN 在每一轮计算中共享参数，而常见的神经网络结构在不同层使用不同的参数。同时，隐含节点状态的更新可以进一步应用 RNN 的思想。
3. 边上的一些信息特征并没有被有效的建模，同时如何学习边的隐含状态也是一个重要问题。
4. 如果我们更关注节点的表示而非图的表示，当迭代轮数 `$T$` 很大时使用固定点是不合适的。这是因为固定点表示的分布在数值上会更加平滑，从而缺少用于区分不同节点的信息。

### Graph Convolutional Networks

图卷积神经网络是将用于传统数据（例如：图像）的卷积操作应用到图结构的数据中。核心思想在于学习一个函数 `$f$`，通过聚合节点 `$v_i$` 自身的特征 `$\mathbf{X}_i$` 和邻居的特征 `$\mathbf{X}_j$` 获得节点的表示，其中 `$j \in N\left(v_i\right)$` 为节点的邻居。

下图展示了一个用于节点表示学习的 GCN 过程：

{{< figure src="/images/cn/2020-04-11-graph-embedding-and-gnn/gcn.png" >}}

GCN 在构建更复杂的图神经网路中扮演了一个核心角色：

{{< figure src="/images/cn/2020-04-11-graph-embedding-and-gnn/gcn-classification.png" title="包含 Pooling 模块用于图分类的 GCN" >}}

{{< figure src="/images/cn/2020-04-11-graph-embedding-and-gnn/gcn-auto-encoder.png" title="包含 GCN 的图自编码器" >}}

{{< figure src="/images/cn/2020-04-11-graph-embedding-and-gnn/gcn-graph-spatial-temporal-network.png" title="包含 GCN 的图时空网络" >}}

GCN 方法可以分为两大类：基于频谱（Spectral Methods）和基于空间（Spatial Methods）的方法。

#### 基于频谱的方法（Spectral Methods）

基于频谱的方法将图视为无向图进行处理，图的一种鲁棒的数学表示为标准化的图拉普拉斯矩阵：

`$$
\mathbf{L}=\mathbf{I}_{\mathbf{n}}-\mathbf{D}^{-\frac{1}{2}} \mathbf{A} \mathbf{D}^{-\frac{1}{2}}
$$`

其中，`$\mathbf{A}$` 为图的邻接矩阵，`$\mathbf{D}$` 为节点度的对角矩阵，`$\mathbf{D}_{ii} = \sum_{j} \left(\mathbf{A}_{i, j}\right)$`。标准化的拉普拉斯矩阵具有实对称半正定的性质，因此可以分解为：

`$$
\mathbf{L}=\mathbf{U} \mathbf{\Lambda} \mathbf{U}^{T}
$$`

其中，`$\mathbf{U}=\left[\mathbf{u}_{\mathbf{0}}, \mathbf{u}_{\mathbf{1}}, \cdots, \mathbf{u}_{\mathbf{n}-\mathbf{1}}\right] \in \mathbf{R}^{N \times N}$` 是由 `$\mathbf{L}$` 的特征向量构成的矩阵，`$\mathbf{\Lambda}$` 为特征值的对角矩阵，`$\mathbf{\Lambda}_{ii} = \lambda_i$`。在图信号处理过程中，一个图信号 `$\mathbf{x} \in \mathbb{R}^N$` 是一个由图的节点构成的特征向量，其中 `$\mathbf{x}_i$` 表示第 `$i$` 个节点的值。对于信号 `$\mathbf{x}$`，图上的傅里叶变换可以定义为：

`$$
\mathscr{F}(\mathbf{x})=\mathbf{U}^{T} \mathbf{x}
$$`

傅里叶反变换定义为：

`$$
\mathscr{F}^{-1}(\hat{\mathbf{x}})=\mathbf{U} \hat{\mathbf{x}}
$$`

其中，`$\hat{\mathbf{x}}$` 为傅里叶变换后的结果。

转变后信号 `$\hat{\mathbf{x}}$` 的元素为新空间图信号的坐标，因此输入信号可以表示为：

`$$
\mathbf{x}=\sum_{i} \hat{\mathbf{x}}_{i} \mathbf{u}_{i}
$$`

这正是傅里叶反变换的结果。那么对于输入信号 `$\mathbf{x}$` 的图卷积可以定义为：

`$$
\begin{aligned}
\mathbf{x} *_{G} \mathbf{g} &=\mathscr{F}^{-1}(\mathscr{F}(\mathbf{x}) \odot \mathscr{F}(\mathbf{g})) \\
&=\mathbf{U}\left(\mathbf{U}^{T} \mathbf{x} \odot \mathbf{U}^{T} \mathbf{g}\right)
\end{aligned}
$$`

其中，`$\mathbf{g} \in \mathbb{R}^N$` 为滤波器，`$\odot$` 表示逐元素乘。假设定义一个滤波器 `$\mathbf{g}_{\theta}=\operatorname{diag}\left(\mathbf{U}^{T} \mathbf{g}\right)$`，则图卷积可以简写为：

`$$
\mathbf{x} *_{G} \mathbf{g}_{\theta}=\mathbf{U} \mathbf{g}_{\theta} \mathbf{U}^{T} \mathbf{x}
$$`

基于频谱的图卷积网络都遵循这样的定义，不同之处在于不同滤波器的选择。

一些代表模型及其聚合和更新方式如下表所示：

| 模型                                   | 聚合方式                                                     | 更新方式                                                     |
| -------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| ChebNet [^defferrard2016convolutional] | `$\mathbf{N}_{k}=\mathbf{T}_{k}(\tilde{\mathbf{L}}) \mathbf{X}$` | `$\mathbf{H}=\sum_{k=0}^{K} \mathbf{N}_{k} \mathbf{\Theta}_{k}$` |
| 1st-order model                        | `$\begin{array}{l} \mathbf{N}_{0}=\mathbf{X} \\ \mathbf{N}_{1}=\mathbf{D}^{-\frac{1}{2}} \mathbf{A} \mathbf{D}^{-\frac{1}{2}} \mathbf{X} \end{array}$` | `$\mathbf{H}=\mathbf{N}_{0} \mathbf{\Theta}_{0}+\mathbf{N}_{1} \mathbf{\Theta}_{1}$` |
| Single parameter                       | `$\mathbf{N}=\left(\mathbf{I}_{N}+\mathbf{D}^{-\frac{1}{2}} \mathbf{A} \mathbf{D}^{-\frac{1}{2}}\right) \mathbf{X}$` | `$\mathbf{H}=\mathbf{N} \mathbf{\Theta}$`                    |
| GCN [^kipf2016semi]                    | `$\mathbf{N}=\tilde{\mathbf{D}}^{-\frac{1}{2}} \tilde{\mathbf{A}} \tilde{\mathbf{D}}^{-\frac{1}{2}} \mathbf{X}$` | `$\mathbf{H}=\mathbf{N} \mathbf{\Theta}$`                    |

#### 基于空间的方法（Spatial Methods）

基于空间的方法通过节点的空间关系来定义图卷积操作。为了将图像和图关联起来，可以将图像视为一个特殊形式的图，每个像素点表示一个节点，如下图所示：

{{< figure src="/images/cn/2020-04-11-graph-embedding-and-gnn/spatial-based-gcn.png" >}}

每个像素同周围的像素相连，以 `$3 \times 3$` 为窗口，每个节点被 8 个邻居节点所包围。通过对中心节点和周围邻居节点的像素值进行加权平均来应用一个 `$3 \times 3$` 大小的滤波器。由于邻居节点的特定顺序，可以在不同位置共享权重。同样对于一般的图，基于空间的图卷积通过对中心和邻居节点的聚合得到节点新的表示。

为了使节点可以感知更深和更广的范围，通常的做法是将多个图卷积层堆叠在一起。根据堆叠方式的不同，基于空间的图卷积可以进一步分为两类：基于循环（Recurrent-based）和基于组合（Composition-based）的。基于循环的方法使用相同的图卷积层来更新隐含表示，基于组合的方式使用不同的图卷积层更新隐含表示，两者差异如下图所示：

{{< figure src="/images/cn/2020-04-11-graph-embedding-and-gnn/recurrent-based-vs-composition-based.png" >}}

一些代表模型及其聚合和更新方式如下表所示：

| 模型                                    | 聚合方式                                                     | 更新方式                                                     |
| --------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Neural FPs [^duvenaud2015convolutional] | `$\mathbf{h}_{\mathcal{N}_{v}}^{t}=\mathbf{h}_{v}^{t-1}+\sum_{k=1}^{\mathcal{N}_{v}} \mathbf{h}_{k}^{t-1}$` | `$\mathbf{h}_{v}^{t}=\sigma\left(\mathbf{h}_{\mathcal{N}_{v}}^{t} \mathbf{W}_{L}^{\mathcal{N}_{v}}\right)$` |
| DCNN [^atwood2016diffusion]             | Node classification:<br/>`$\mathbf{N}=\mathbf{P}^{*} \mathbf{X}$`<br/> Graph classification:<br/>`$\mathbf{N}=1_{N}^{T} \mathbf{P}^{*} \mathbf{X} / N$` | `$\mathbf{H}=f\left(\mathbf{W}^{c} \odot \mathbf{N}\right)$` |
| GraphSAGE [^hamilton2017inductive]      | `$\mathbf{h}_{\mathcal{N}_{v}}^{t}=\text{AGGREGATE}_{t}\left(\left\{\mathbf{h}_{u}^{t-1}, \forall u \in \mathcal{N}_{v}\right\}\right)$` | `$\mathbf{h}_{v}^{t}=\sigma\left(\mathbf{W}^{t} \cdot\left[\mathbf{h}_{v}^{t-1} \Vert \mathbf{h}_{\mathcal{N}_{v}}^{t}\right]\right)$` |

### Graph Recurrent Networks

一些研究尝试利用门控机制（例如：GRU 或 LSTM）用于减少之前 GNN 模型在传播过程中的限制，同时改善在图结构中信息的长距离传播。GGNN [^li2015gated] 提出了一种使用 GRU 进行传播的方法。它将 RNN 展开至一个固定 `$T$` 步，然后通过基于时间的传导计算梯度。传播模型的基础循环方式如下：

`$$
\begin{aligned}
&\mathbf{a}_{v}^{t}=\mathbf{A}_{v}^{T}\left[\mathbf{h}_{1}^{t-1} \ldots \mathbf{h}_{N}^{t-1}\right]^{T}+\mathbf{b}\\
&\mathbf{z}_{v}^{t}=\sigma\left(\mathbf{W}^{z} \mathbf{a}_{v}^{t}+\mathbf{U}^{z} \mathbf{h}_{v}^{t-1}\right)\\
&\mathbf{r}_{v}^{t}=\sigma\left(\mathbf{W}^{r} \mathbf{a}_{v}^{t}+\mathbf{U}^{r} \mathbf{h}_{v}^{t-1}\right)\\
&\begin{array}{l}
\widetilde{\mathbf{h}}_{v}^{t}=\tanh \left(\mathbf{W} \mathbf{a}_{v}^{t}+\mathbf{U}\left(\mathbf{r}_{v}^{t} \odot \mathbf{h}_{v}^{t-1}\right)\right) \\
\mathbf{h}_{v}^{t}=\left(1-\mathbf{z}_{v}^{t}\right) \odot \mathbf{h}_{v}^{t-1}+\mathbf{z}_{v}^{t} \odot \widetilde{\mathbf{h}}_{v}^{t}
\end{array}
\end{aligned}
$$`

节点 `$v$` 首先从邻居汇总信息，其中 `$\mathbf{A}_v$` 为图邻接矩阵 `$\mathbf{A}$` 的子矩阵表示节点 `$v$` 及其邻居的连接。类似 GRU 的更新函数，通过结合其他节点和上一时间的信息更新节点的隐状态。`$\mathbf{a}$` 用于获取节点 `$v$` 邻居的信息，`$\mathbf{z}$` 和 `$\mathbf{r}$` 分别为更新和重置门。

GGNN 模型设计用于解决序列生成问题，而之前的模型主要关注单个输出，例如：节点级别或图级别的分类问题。研究进一步提出了 Gated Graph Sequence Neural Networks（GGS-NNs），使用多个 GGNN 产生一个输出序列 `$\mathbf{o}^{(1)}, \cdots, \mathbf{o}^{(K)}$`，如下图所示：

{{< figure src="/images/cn/2020-04-11-graph-embedding-and-gnn/ggs-nn.png" >}}

上图中使用了两个 GGNN，`$\mathcal{F}_o^{(k)}$` 用于从 `$\mathcal{\boldsymbol{X}}^{(k)}$` 预测 `$\mathbf{o}^{(k)}$`，`$\mathcal{F}_x^{(k)}$` 用于从 `$\mathcal{\boldsymbol{X}}^{(k)}$` 预测 `$\mathcal{\boldsymbol{X}}^{(k+1)}$`。令 `$\mathcal{\boldsymbol{H}}^{(k, t)}$` 表示第 `$k$` 步输出的第 `$t$` 步传播，`$\mathcal{\boldsymbol{H}}^{(k, 1)}$` 在任意 `$k$` 步初始化为 `$\mathcal{\boldsymbol{X}}^{(k)}$`，`$\mathcal{\boldsymbol{H}}^{(t, 1)}$` 在任意 `$t$` 步初始化为 `$\mathcal{\boldsymbol{X}}^{(t)}$`，`$\mathcal{F}_o^{(k)}$` 和 `$\mathcal{F}_x^{(k)}$` 可以为不同模型也可以共享权重。

一些代表模型及其聚合和更新方式如下表所示：

| 模型                                     | 聚合方式                                                     | 更新方式                                                     |
| ---------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| GGNN [^li2015gated]                      | `$\mathbf{h}_{\mathcal{N}_{v}}^{t}=\sum_{k \in \mathcal{N}_{v}} \mathbf{h}_{k}^{t-1}+\mathbf{b}$` | `$\begin{aligned} &\mathbf{z}_{v}^{t}=\sigma\left(\mathbf{W}^{z} \mathbf{h}_{\mathcal{N}_{v}}^{t}+\mathbf{U}^{z} \mathbf{h}_{v}^{t-1}\right)\\ &\mathbf{r}_{v}^{t}=\sigma\left(\mathbf{W}^{r} \mathbf{h}_{\mathcal{N}_{v}}^{z}+\mathbf{U}^{r} \mathbf{h}_{v}^{t-1}\right)\\ &\begin{array}{l} \widetilde{\mathbf{h}}_{v}^{t}=\tanh \left(\mathbf{W h}_{\mathcal{N}_{v}}^{t}+\mathbf{U}\left(\mathbf{r}_{v}^{t} \odot \mathbf{h}_{v}^{t-1}\right)\right) \\ \mathbf{h}_{v}^{t}=\left(1-\mathbf{z}_{v}^{t}\right) \odot \mathbf{h}_{v}^{t-1}+\mathbf{z}_{v}^{t} \odot \widetilde{\mathbf{h}}_{v}^{t} \end{array} \end{aligned}$` |
| Tree LSTM (Child sum) [^tai2015improved] | `$\mathbf{h}_{\mathcal{N}_{v}}^{t}=\sum_{k \in \mathcal{N}_{v}} \mathbf{h}_{k}^{t-1}$` | `$\begin{aligned} &\mathbf{i}_{v}^{t}=\sigma\left(\mathbf{W}^{i} \mathbf{x}_{v}^{t}+\mathbf{U}^{i} \mathbf{h}_{\mathcal{N}_{v}}^{t}+\mathbf{b}^{i}\right)\\ &\mathbf{f}_{v k}^{t}=\sigma\left(\mathbf{W}^{f} \mathbf{x}_{v}^{t}+\mathbf{U}^{f} \mathbf{h}_{k}^{t-1}+\mathbf{b}^{f}\right)\\ &\mathbf{o}_{v}^{t}=\sigma\left(\mathbf{W}^{o} \mathbf{x}_{v}^{t}+\mathbf{U}^{o} \mathbf{h}_{\mathcal{N}_{v}}^{t}+\mathbf{b}^{o}\right)\\ &\mathbf{u}_{v}^{t}=\tanh \left(\mathbf{W}^{u} \mathbf{x}_{v}^{t}+\mathbf{U}^{u} \mathbf{h}_{\mathcal{N}_{v}}^{t}+\mathbf{b}^{u}\right)\\ &\begin{array}{l} \mathbf{c}_{v}^{t}=\mathbf{i}_{v}^{t} \odot \mathbf{u}_{v}^{t}+\sum_{k \in \mathcal{N}_{v}} \mathbf{f}_{v k}^{t} \odot \mathbf{c}_{k}^{t-1} \\ \mathbf{h}_{v}^{t}=\mathbf{o}_{v}^{t} \odot \tanh \left(\mathbf{c}_{v}^{t}\right) \end{array} \end{aligned}$` |
| Tree LSTM (N-ary) [^tai2015improved]     | `$\begin{aligned} &\mathbf{h}_{\mathcal{N}_{v}}^{t i}=\sum_{l=1}^{K} \mathbf{U}_{l}^{i} \mathbf{h}_{v l}^{t-1}\\ &\mathbf{h}_{\mathcal{N}_{v} k}^{t f}=\sum_{l=1}^{K} \mathbf{U}_{k l}^{f} \mathbf{h}_{v l}^{t-1}\\ &\mathbf{h}_{\mathcal{N}_{v}}^{t o}=\sum_{l=1}^{K} \mathbf{U}_{l}^{o} \mathbf{h}_{v l}^{t-1}\\ &\mathbf{h}_{\mathcal{N}_{v}}^{t u}=\sum_{l=1}^{K} \mathbf{U}_{l}^{u} \mathbf{h}_{v l}^{t-1} \end{aligned}$` | `$\begin{aligned} &\mathbf{i}_{v}^{t}=\sigma\left(\mathbf{W}^{i} \mathbf{x}_{v}^{t}+\mathbf{h}_{\mathcal{N}_{v},}^{t i}+\mathbf{b}^{i}\right)\\ &\mathbf{f}_{v k}^{t}=\sigma\left(\mathbf{W}^{f} \mathbf{x}_{v}^{t}+\mathbf{h}_{\mathcal{N}_{v} k}^{f f}+\mathbf{b}^{f}\right)\\ &\mathbf{o}_{v}^{t}=\sigma\left(\mathbf{W}^{o} \mathbf{x}_{v}^{t}+\mathbf{h}_{\mathcal{N}_{v}}^{t o}+\mathbf{b}^{o}\right)\\ &\mathbf{u}_{v}^{t}=\tanh \left(\mathbf{W}^{u} \mathbf{x}_{v}^{t}+\mathbf{h}_{\mathcal{N}_{v}}^{t u}+\mathbf{b}^{u}\right)\\ &\mathbf{c}_{v}^{t}=\mathbf{i}_{v}^{t} \odot \mathbf{u}_{v}^{t}+\sum_{l=1}^{K} \mathbf{f}_{v l}^{t} \odot \mathbf{c}_{v l}^{t-1}\\ &\mathbf{h}_{v}^{t}=\mathbf{o}_{v}^{t} \odot \tanh \left(\mathbf{c}_{v}^{t}\right) \end{aligned}$` |
| Graph LSTM [^peng2017cross]              | `$\begin{aligned} \mathbf{h}_{\mathcal{N}_{v}}^{t i}=\sum_{k \in \mathcal{N}_{v}} \mathbf{U}_{m(v, k)}^{i} \mathbf{h}_{k}^{t-1} \\ \mathbf{h}_{\mathcal{N}_{v}}^{t o}=\sum_{k \in \mathcal{N}_{v}} \mathbf{U}_{m(v, k)}^{o} \mathbf{h}_{k}^{t-1} \\ \mathbf{h}_{\mathcal{N}_{v}}^{t u}=\sum_{k \in \mathcal{N}_{v}} \mathbf{U}_{m(v, k)}^{u} \mathbf{h}_{k}^{t-1} \end{aligned}$` | `$\begin{aligned} &\mathbf{i}_{v}^{t}=\sigma\left(\mathbf{W}^{i} \mathbf{x}_{v}^{t}+\mathbf{h}_{\mathcal{N}_{v}}^{t i}+\mathbf{b}^{i}\right)\\ &\mathbf{f}_{v k}^{t}=\sigma\left(\mathbf{W}^{f} \mathbf{x}_{v}^{t}+\mathbf{U}_{m(v, k)}^{f} \mathbf{h}_{k}^{t-1}+\mathbf{b}^{f}\right)\\ &\mathbf{o}_{v}^{t}=\sigma\left(\mathbf{W}^{o} \mathbf{x}_{v}^{t}+\mathbf{h}_{\mathcal{N}_{v}}^{t o}+\mathbf{b}^{o}\right)\\ &\mathbf{u}_{v}^{t}=\tanh \left(\mathbf{W}^{u} \mathbf{x}_{v}^{t}+\mathbf{h}_{\mathcal{N}_{v}}^{t u}+\mathbf{b}^{u}\right)\\ &\begin{array}{l} \mathbf{c}_{v}^{t}=\mathbf{i}_{v}^{t} \odot \mathbf{u}_{v}^{t}+\sum_{k \in \mathcal{N}_{v}} \mathbf{f}_{v k}^{t} \odot \mathbf{c}_{k}^{t-1} \\ \mathbf{h}_{v}^{t}=\mathbf{o}_{v}^{t} \odot \tanh \left(\mathbf{c}_{v}^{t}\right) \end{array} \end{aligned}$` |

### Graph Attention Networks

与 GCN 对于节点所有的邻居平等对待相比，注意力机制可以为每个邻居分配不同的注意力评分，从而识别更重要的邻居。

GAT [^velickovic2017graph] 将注意力机制引入传播过程，其遵循自注意力机制，通过对每个节点邻居的不同关注更新隐含状态。GAT 定义了一个图注意力层（_graph attentional layer_），通过堆叠构建图注意力网络。对于节点对 `$\left(i, j\right)$`，基于注意力机制的系数计算方式如下：

`$$
\alpha_{i j}=\frac{\exp \left(\text { LeakyReLU }\left(\overrightarrow{\mathbf{a}}^{T}\left[\mathbf{W} \vec{h}_{i} \| \mathbf{W} \vec{h}_{j}\right]\right)\right)}{\sum_{k \in N_{i}} \exp \left(\text { LeakyReLU }\left(\overrightarrow{\mathbf{a}}^{T}\left[\mathbf{W} \vec{h}_{i} \| \mathbf{W} \vec{h}_{k}\right]\right)\right)}
$$`

其中，`$\alpha_{i j}$` 表示节点 `$j$` 对 `$i$` 的注意力系数，`$N_i$` 表示节点 `$i$` 的邻居。令 `$\mathbf{h}=\left\{\vec{h}_{1}, \vec{h}_{2}, \ldots, \vec{h}_{N}\right\}, \vec{h}_{i} \in \mathbb{R}^{F}$` 表示输入节点特征，其中 `$N$` 为节点的数量，`$F$` 为特征维度，则节点的输出特征（可能为不同维度 `$F^{\prime}$`）为 `$\mathbf{h}^{\prime}=\left\{\vec{h}_{1}^{\prime}, \vec{h}_{2}^{\prime}, \ldots, \vec{h}_{N}^{\prime}\right\}, \vec{h}_{i}^{\prime} \in \mathbb{R}^{F^{\prime}}$`。`$\mathbf{W} \in \mathbb{R}^{F^{\prime} \times F}$` 为所有节点共享的线性变换的权重矩阵，`$a: \mathbb{R}^{F^{\prime}} \times \mathbb{R}^{F^{\prime}} \rightarrow \mathbb{R}$` 用于计算注意力系数。最后的输出特征计算方式如下：

`$$
\vec{h}_{i}^{\prime}=\sigma\left(\sum_{j \in \mathcal{N}_{i}} \alpha_{i j} \mathbf{W} \vec{h}_{j}\right)
$$`

注意力层采用多头注意力机制来稳定学习过程，之后应用 `$K$` 个独立的注意力机制计算隐含状态，最后通过拼接或平均得到输出表示：

`$$
\vec{h}_{i}^{\prime}=\Vert_{k=1}^{K} \sigma\left(\sum_{j \in \mathcal{N}_{i}} \alpha_{i j}^{k} \mathbf{W}^{k} \vec{h}_{j}\right)
$$`

`$$
\vec{h}_{i}^{\prime}=\sigma\left(\frac{1}{K} \sum_{k=1}^{K} \sum_{j \in \mathcal{N}_{i}} \alpha_{i j}^{k} \mathbf{W}^{k} \vec{h}_{j}\right)
$$`

其中，`$\Vert$` 表示连接操作，`$\alpha_{ij}^k$` 表示第 `$k$` 个注意力机制计算得到的标准化的注意力系数。整个模型如下图所示：

{{< figure src="/images/cn/2020-04-11-graph-embedding-and-gnn/gat.png" >}}

GAT 中的注意力架构有如下几个特点：

1. 针对节点对的计算是并行的，因此计算过程是高效的。
2. 可以处理不同度的节点并对邻居分配对应的权重。
3. 可以容易地应用到归纳学习问题中去。

### 应用

图神经网络已经被应用在监督、半监督、无监督和强化学习等多个领域。下图列举了 GNN 在不同领域内相关问题中的应用，具体模型论文请参考 Graph Neural Networks: A Review of Methods and Applications 原文 [^zhou2018graph]。

{{< figure src="/images/cn/2020-04-11-graph-embedding-and-gnn/applications.png" >}}

## 开放资源

### 开源实现

| 项目                                                         | 框架                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| [rusty1s/pytorch_geometric](https://github.com/rusty1s/pytorch_geometric) | <i class="icon icon-pytorch">PyTorch</i>                    |
| [dmlc/dgl](https://github.com/dmlc/dgl)                      | <i class="icon icon-pytorch">PyTorch</i>, <i class="icon icon-tensorflow">TF</i> & <i class="icon icon-mxnet">MXNet</i> |
| [alibaba/euler](https://github.com/alibaba/euler)            | <i class="icon icon-tensorflow">TF</i>                      |
| [alibaba/graph-learn](https://github.com/alibaba/graph-learn) | <i class="icon icon-tensorflow">TF</i>                      |
| [deepmind/graph_nets](https://github.com/deepmind/graph_nets) | <i class="icon icon-tensorflow">TF</i> & <i class="icon icon-sonnet">Sonnet</i> |
| [facebookresearch/PyTorch-BigGraph](https://github.com/facebookresearch/PyTorch-BigGraph) | <i class="icon icon-pytorch">PyTorch</i>                    |
| [tencent/plato](https://github.com/tencent/plato)            |                                                              |
| [PaddlePaddle/PGL](https://github.com/PaddlePaddle/PGL)      | <i class="icon icon-paddlepaddle"></i> PaddlePaddle          |
| [Accenture/AmpliGraph](https://github.com/Accenture/AmpliGraph) | <i class="icon icon-tensorflow">TF</i>                      |
| [danielegrattarola/spektral](https://github.com/danielegrattarola/spektral) | <i class="icon icon-tensorflow">TF</i>                      |
| [THUDM/cogdl](https://github.com/THUDM/cogdl/)               | <i class="icon icon-pytorch">PyTorch</i>                    |
| [DeepGraphLearning/graphvite](https://github.com/DeepGraphLearning/graphvite) | <i class="icon icon-pytorch">PyTorch</i>                    |

### 论文列表和评测

- [Must-read papers on network representation learning (NRL) / network embedding (NE)](https://github.com/thunlp/NRLPapers)
- [Must-read papers on graph neural networks (GNN)](https://github.com/thunlp/GNNPapers)
- [DeepGraphLearning/LiteratureDL4Graph](https://github.com/DeepGraphLearning/LiteratureDL4Graph)
- [nnzhan/Awesome-Graph-Neural-Networks](https://github.com/nnzhan/Awesome-Graph-Neural-Networks)
- [graphdeeplearning/benchmarking-gnns](https://github.com/graphdeeplearning/benchmarking-gnns)
- [Open Graph Benchmark](https://ogb.stanford.edu/)

[^cai2018comprehensive]: Cai, H., Zheng, V. W., & Chang, K. C. C. (2018). A comprehensive survey of graph embedding: Problems, techniques, and applications. _IEEE Transactions on Knowledge and Data Engineering_, 30(9), 1616-1637.

[^goyal2018graph]: Goyal, P., & Ferrara, E. (2018). Graph embedding techniques, applications, and performance: A survey. _Knowledge-Based Systems_, 151, 78-94.

[^hamilton2017representation]: Hamilton, W. L., Ying, R., & Leskovec, J. (2017). Representation learning on graphs: Methods and applications. _arXiv preprint arXiv:1709.05584_.

[^perozzi2014deepwalk]: Perozzi, B., Al-Rfou, R., & Skiena, S. (2014). Deepwalk: Online learning of social representations. In _Proceedings of the 20th ACM SIGKDD international conference on Knowledge discovery and data mining_ (pp. 701-710).

[^grover2016node2vec]: Grover, A., & Leskovec, J. (2016). node2vec: Scalable feature learning for networks. In _Proceedings of the 22nd ACM SIGKDD international conference on Knowledge discovery and data mining_ (pp. 855-864).

[^tang2015line]: Tang, J., Qu, M., Wang, M., Zhang, M., Yan, J., & Mei, Q. (2015). Line: Large-scale information network embedding. In _Proceedings of the 24th international conference on world wide web_ (pp. 1067-1077).

[^walker1974new]: Walker, A. J. (1974). New fast method for generating discrete random numbers with arbitrary frequency distributions. _Electronics Letters_, 10(8), 127-128.

[^walker1977efficient]: Walker, A. J. (1977). An efficient method for generating discrete random variables with general distributions. _ACM Transactions on Mathematical Software (TOMS)_, 3(3), 253-256.

[^fogaras2005towards]: Fogaras, D., Rácz, B., Csalogány, K., & Sarlós, T. (2005). Towards scaling fully personalized pagerank: Algorithms, lower bounds, and experiments. _Internet Mathematics_, 2(3), 333-358.

[^haveliwala2002topic]: Haveliwala, T. H. (2002). Topic-sensitive PageRank. In _Proceedings of the 11th international conference on World Wide Web_ (pp. 517-526).

[^cao2015grarep]: Cao, S., Lu, W., & Xu, Q. (2015). Grarep: Learning graph representations with global structural information. In _Proceedings of the 24th ACM international on conference on information and knowledge management_ (pp. 891-900).

[^ou2016asymmetric]: Ou, M., Cui, P., Pei, J., Zhang, Z., & Zhu, W. (2016). Asymmetric transitivity preserving graph embedding. In _Proceedings of the 22nd ACM SIGKDD international conference on Knowledge discovery and data mining_ (pp. 1105-1114).

[^donnat2018learning]: Donnat, C., Zitnik, M., Hallac, D., & Leskovec, J. (2018). Learning structural node embeddings via diffusion wavelets. In _Proceedings of the 24th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining_ (pp. 1320-1329).

[^dong2017metapath2vec]: Dong, Y., Chawla, N. V., & Swami, A. (2017). metapath2vec: Scalable representation learning for heterogeneous networks. In _Proceedings of the 23rd ACM SIGKDD international conference on knowledge discovery and data mining_ (pp. 135-144).

[^fu2017hin2vec]: Fu, T. Y., Lee, W. C., & Lei, Z. (2017). Hin2vec: Explore meta-paths in heterogeneous information networks for representation learning. In _Proceedings of the 2017 ACM on Conference on Information and Knowledge Management_ (pp. 1797-1806).

[^wang2016structural]: Wang, D., Cui, P., & Zhu, W. (2016). Structural deep network embedding. In _Proceedings of the 22nd ACM SIGKDD international conference on Knowledge discovery and data mining_ (pp. 1225-1234).

[^cao2016deep]: Cao, S., Lu, W., & Xu, Q. (2016). Deep neural networks for learning graph representations. In _Thirtieth AAAI conference on artificial intelligence_.

[^scarselli2008graph]: Scarselli, F., Gori, M., Tsoi, A. C., Hagenbuchner, M., & Monfardini, G. (2008). The graph neural network model. _IEEE Transactions on Neural Networks_, 20(1), 61-80.

[^zhou2018graph]: Zhou, J., Cui, G., Zhang, Z., Yang, C., Liu, Z., Wang, L., ... & Sun, M. (2018). Graph neural networks: A review of methods and applications. _arXiv preprint arXiv:1812.08434_.

[^liu2020introduction]: Liu, Z., & Zhou, J. (2020). Introduction to Graph Neural Networks. _Synthesis Lectures on Artificial Intelligence and Machine Learning_, 14(2), 1–127.

[^khamsi2011introduction]: Khamsi, M. A., & Kirk, W. A. (2011). _An introduction to metric spaces and fixed point theory_ (Vol. 53). John Wiley & Sons.

[^zhang2020deep]: Zhang, Z., Cui, P., & Zhu, W. (2020). Deep learning on graphs: A survey. _IEEE Transactions on Knowledge and Data Engineering_.

[^wu2020comprehensive]: Wu, Z., Pan, S., Chen, F., Long, G., Zhang, C., & Philip, S. Y. (2020). A comprehensive survey on graph neural networks. _IEEE Transactions on Neural Networks and Learning Systems_.

[^defferrard2016convolutional]: Defferrard, M., Bresson, X., & Vandergheynst, P. (2016). Convolutional neural networks on graphs with fast localized spectral filtering. In _Advances in neural information processing systems_ (pp. 3844-3852).

[^kipf2016semi]: Kipf, T. N., & Welling, M. (2016). Semi-supervised classification with graph convolutional networks. _arXiv preprint arXiv:1609.02907_.

[^duvenaud2015convolutional]: Duvenaud, D. K., Maclaurin, D., Iparraguirre, J., Bombarell, R., Hirzel, T., Aspuru-Guzik, A., & Adams, R. P. (2015). Convolutional networks on graphs for learning molecular fingerprints. In _Advances in neural information processing systems_ (pp. 2224-2232).

[^atwood2016diffusion]: Atwood, J., & Towsley, D. (2016). Diffusion-convolutional neural networks. In _Advances in neural information processing systems_ (pp. 1993-2001).

[^hamilton2017inductive]: Hamilton, W., Ying, Z., & Leskovec, J. (2017). Inductive representation learning on large graphs. In _Advances in neural information processing systems_ (pp. 1024-1034).

[^li2015gated]: Li, Y., Tarlow, D., Brockschmidt, M., & Zemel, R. (2015). Gated graph sequence neural networks. _arXiv preprint arXiv:1511.05493._

[^tai2015improved]: Tai, K. S., Socher, R., & Manning, C. D. (2015). Improved Semantic Representations From Tree-Structured Long Short-Term Memory Networks. In _Proceedings of the 53rd Annual Meeting of the Association for Computational Linguistics and the 7th International Joint Conference on Natural Language Processing_ (Volume 1: Long Papers) (pp. 1556-1566).

[^peng2017cross]: Peng, N., Poon, H., Quirk, C., Toutanova, K., & Yih, W. T. (2017). Cross-sentence n-ary relation extraction with graph lstms. _Transactions of the Association for Computational Linguistics_, 5, 101-115.

[^velickovic2017graph]: Veličković, P., Cucurull, G., Casanova, A., Romero, A., Lio, P., & Bengio, Y. (2017). Graph attention networks. _arXiv preprint arXiv:1710.10903._
