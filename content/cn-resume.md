---
title: 简历
author: 范叶亮
date: '2017-12-04'
lastmod: '2019-06-25'
slug: cn/resume
disable_author_date: true
disable_donate: true
disable_comments: true
disable_adsense: true
---

## 范叶亮

## <span class="mdi mdi-bullseye-arrow"></span> 研究兴趣

- 深度学习 (Deep Learning)
- 强化学习 (Reinforcement Learning)
- 自然语言处理 (Natural Language Processing)
- 复杂网络 (Complex Network)
- 知识图谱 (Knowledge Graph)
- 因果推断和推理 (Causal Inference & Reasoning)

## <span class="mdi mdi-school-outline"></span> 教育背景

- 2012.09 ~ 2015.03 **河北工业大学** 信息管理 硕士
- 2008.09 ~ 2012.07 **河北工业大学** 工商管理 学士

## <span class="mdi mdi-account-group-outline"></span> 工作经历

1. 2015.03 ~ 至今 **京东数字科技 (京东金融)** 高级研究员

## <span class="mdi mdi-clipboard-list-outline"></span> 项目经历

### 智慧农业

_2019.07 ~ 至今 高级研究员_

- **智能种植和智能禽类解决方案**：主导构思和设计智能种植和智能禽类商业模式和技术解决方案。带领算法和产品团队设计和实现了整个解决方案中的相关数据和算法模型，完成 SaaS 和 APP 原型设计，**从 0 到 1** 地实现了整体解决方案从 MVP 到真实生产环境的落地。
- **智能环控**：设计和实现了基于时间序列分析，深度学习和强化学习的智能环控算法和解决方案。将智能环控算法拆解为环境模型和控制模型两部分，实现了同一作物和家畜在不同环境下种养殖模型的复用。通过专家知识引擎和机器学习算法实现了在保持现有能耗不变的前提下各项环境指标控制误差相比于人工降低了了 **50%+**。参加 2019 年国际智慧温室种植挑战赛，在 24 小时 Hackathon 模拟挑战赛中，获得人工智能策略方法 **4/21** 名，虚拟西红柿种植净利润 **9/21** 名。
- **智能集蛋**：设计和实现了一套基于计算机视觉和 IoT 传感器的智能集蛋装置和算法。在笼养模式集蛋过程中，利用摄像头和 IoT 传感器采集的数据实现了鸡蛋计数和隶属笼体的识别，准确率 **99%+**。通过鸡蛋隶属笼体识别可以精准分析不同笼体内的料蛋比，为淘汰鸡提供强有力的数据支持，同时也为蛋品的溯源提供了更细力度的数据。

### Daat (复杂网络和知识图谱)

_2018.04 ~ 2019.06 项目负责人_

- **数据知识工程和知识问答系统**：设计和构建数据仓库，数据集市和数据工具领域的知识本体，并据此进行知识抽取和知识库构建。设计和实现了数据知识问答系统，包括：用户问题意图识别，槽填充，查询改写，结果排序以及基于深度语义模型 (DSSM) 的问题匹配。问答系统主要用于辅助数据使用者对于仓库和集市数据的查询使用，以及相关概念、流程、工具等方面问题的解答。
- **自动化敏感信息识别**：对于入库到数据仓库中的数据进行自动敏感信息识别，辅助数据加密策略实施。根据数据的元信息 (例如：表名，表注释，字段名，字段注释等) 和值信息 (即字段存储的数据值)，利用 Wide & Deep 网络构建识别模型。提取传统特征构建 Wide 网络，针对文本特征，利用 Char Embedding + CNN 构建 Deep 网络，模型测试数据的 F1-Score 为 **0.95+**。
- **大规模异构网络嵌入**：实现针对**千万级别顶点**和**亿级别边**的异构网络嵌入算法。通过 Alias 方法进行高效地加权节点采样，实现了基于具有丰富业务含义元路径 (Meta-Path) 和其他算法的网络节点嵌入。利用异构网络节点嵌入结果作为节点特征 (例如：用户，商品等) 为其他业务模型和系统提供服务。
- **基于用户网络和用户行为的推荐和营销**：通过用户的历史购买记录构建包含用户，商品 (实物，理财等) 等多类型节点和边的异构网络，并利用异构网络嵌入算法构建不同类型节点的向量表示。结合用户传统特征和用户在线行为，构建推荐候选结果生成和营销人群生成模型，结合最终业务模型，平均辅助提升效果 **20%+**。

### 全视之眼 (中文地址分析)

_2015.03 ~ 2018.04 项目负责人_

- **地址分析算法引擎**：设计和开发中文地址分词，分类，完整度，POI 识别，相似度等基础算法和服务，算法平均准确率 **90%+**。
- **地址画像系统**：依托地址分析算法引擎，设计地址 POI。 画像相关指标体系，存储和服务框架。对内，服务于线下支付等场景下的营销和运营，平均提升用户转化率 **30%+**；对外，接入京东金融稻田等平台，提供精确查询，模糊查询和经纬度范围查询等多种查询方式，实现金融科技的对外输出。
- **授信和反欺诈模型**：依据地址画像构建授信策略，辅筛选和授信用户超过 **1000 万人**；依托地址分析算法和地址画像，构建中介识别等反欺诈模型，识别套现订单金额约 **20 万元/日**。
- 全视之眼项目斩获 2017 年度京东集团京芽杯创新大赛 **“创新种子奖”**，排名 **20/378**。
- **企业地址画像系统**：构建企业、地址和用户关系，设计企业地址画像相关指标体系，服务于 [**京东企业信用**](https://icredit.jd.com/)。
- **农村金融小站选址系统**：根据地址画像系统，结合农村金融相关业务，构建基于地址画像的农村金融小站选址模型和系统。

### 用户行为分析

_2017.10 ~ 2017.12 算法设计和开发_

- 设计开发了一种 Behavior2Vec 用户行为表示方法，基于层次聚类和深度搜索，构建了一个用于识别用户异常行为的混合模型。在校园白条中介激活和账号盗用问题上，相比传统的 Bag of Words 和 N-GRAM 等表示方法，在保证**准确率 80%+** 的前提下，提高异常用户识别数量 **3+ 倍**。

### 动产融资

_2015.03 ~ 2015.10 算法设计和开发_

- 设计开发一种基于 Bass 扩散模型，优化的时间序列相似度和聚类的混合产品生命周期识别模型，尾货识别**准确率 95%+**，辅助贷款方商品质押准入决策和质押率的制定。
- 设计开发不同数据源的商品信息融合模型，相同商品识别**准确率 90%+**，配合 ElasticSearch 开发商品模糊匹配查询服务，为商品质押提供精准的价格等相关信息。

## <span class="mdi mdi-cog-outline"></span> 专业技能

### 开发语言

- R: <span class="mdi mdi-star"></span><span class="mdi mdi-star"></span><span class="mdi mdi-star"></span><span class="mdi mdi-star"></span><span class="mdi mdi-star-outline"></span>
- Python: <span class="mdi mdi-star"></span><span class="mdi mdi-star"></span><span class="mdi mdi-star"></span><span class="mdi mdi-star"></span><span class="mdi mdi-star-outline"></span>
- SQL: <span class="mdi mdi-star"></span><span class="mdi mdi-star"></span><span class="mdi mdi-star"></span><span class="mdi mdi-star"></span><span class="mdi mdi-star-outline"></span>
- HTML / CSS / JavaScript: <span class="mdi mdi-star"></span><span class="mdi mdi-star"></span><span class="mdi mdi-star"></span><span class="mdi mdi-star-outline"></span><span class="mdi mdi-star-outline"></span>

### 框架

- Tensorflow: <span class="mdi mdi-star"></span><span class="mdi mdi-star"></span><span class="mdi mdi-star"></span><span class="mdi mdi-star-outline"></span><span class="mdi mdi-star-outline"></span>
- PyTorch: <span class="mdi mdi-star"></span><span class="mdi mdi-star"></span><span class="mdi mdi-star"></span><span class="mdi mdi-star-outline"></span><span class="mdi mdi-star-outline"></span>
- Qt: <span class="mdi mdi-star"></span><span class="mdi mdi-star"></span><span class="mdi mdi-star"></span><span class="mdi mdi-star-outline"></span><span class="mdi mdi-star-outline"></span>
- React: <span class="mdi mdi-star"></span><span class="mdi mdi-star"></span><span class="mdi mdi-star-outline"></span><span class="mdi mdi-star-outline"></span><span class="mdi mdi-star-outline"></span>

### 工具

- Axure: <span class="mdi mdi-star"></span><span class="mdi mdi-star"></span><span class="mdi mdi-star"></span><span class="mdi mdi-star"></span><span class="mdi mdi-star-outline"></span>
- Sketch: <span class="mdi mdi-star"></span><span class="mdi mdi-star"></span><span class="mdi mdi-star"></span><span class="mdi mdi-star"></span><span class="mdi mdi-star-outline"></span>
- Omnigraffle: <span class="mdi mdi-star"></span><span class="mdi mdi-star"></span><span class="mdi mdi-star"></span><span class="mdi mdi-star"></span><span class="mdi mdi-star-outline"></span>

### 外语能力

- 英语: CET6，能说，会写，菜单就都不懂了...
- 韩语: 为了更好的看懂优秀的韩国电影努力学习中...

## <span class="mdi mdi-seal-variant"></span> 研究成果

### 论文

1. Zhou, F., Yin, H., Zhan, L., Li, H., Fan, Y., & Jiang, L. (2018). A Novel Ensemble Strategy Combining Gradient Boosted Decision Trees and Factorization Machine Based Neural Network for Clicks Prediction. In _2018 International Conference on Big Data and Artificial Intelligence (BDAI)_ (pp. 29-33). IEEE.
2. Li, J., **Fan, Y.\***, Xu, Y., & Feng, H. (2013). An Improved Forecasting Algorithm for Spare Parts of Short Life Cycle Products Based on EMD-SVM. In _Information Science and Cloud Computing Companion (ISCC-C), 2013 International Conference on_ (pp. 722-727). IEEE.
3. **Fan, Y.**, Li, J., Chu, C. (2014). [IEAF: A Hybrid Method for Forecasting Short Life Cycle Spare Parts](https://cdn.leovan.me/documents/publications/IEAF.pdf). _Unpublished_.

### 专利

1. 一种中文地址分词方法及系统 (发明，[CN 105159949](http://epub.cnipa.gov.cn/patent/CN105159949B)，授权，第一发明人，2015)
2. 一种产品库存预测方法及装置 (发明，[CN 106056239](http://epub.cnipa.gov.cn/patent/CN106056239A)，授权，第一发明人，2016)
3. 一种产品生命周期的识别方法和装置 (发明，[CN 106408217](http://epub.cnipa.gov.cn/patent/CN106408217A)，实审，第一发明人，2017)
4. 一种计算地址相似度的方法和装置 (发明，[CN 107239442](http://epub.cnipa.gov.cn/patent/CN107239442A)，实审，第一发明人，2017)
5. 数据仓库信息处理方法、装置、系统、介质 (发明，[CN 109388637](http://epub.cnipa.gov.cn/patent/CN109388637A)，实审，第一发明人，2018)
6. 确定表字段的类型的方法和装置 (发明，[CN 109784407](http://epub.cnipa.gov.cn/patent/CN109784407A)，实审，第一发明人，2018)
7. 一种数据处理方法、装置、设备及介质 (发明，[CN 110309235](http://epub.cnipa.gov.cn/patent/CN110309235A)，实审，第一发明人，2019)
8. 用于生成信息的方法和装置 (发明，申请中，第一发明人，2019)

### 开源项目

- Github: https://github.com/leovan ![github-followers](https://img.shields.io/github/followers/leovan?style=social&label=Follow)

1. [Python 数据科学导论](https://github.com/leovan/data-science-introduction-with-python)，一份以 Python 为基础的数据科学入门教程。![github-stars](https://img.shields.io/github/stars/leovan/data-science-introduction-with-python.svg?style=social&label=Stars)
2. [R 语言数据科学导论](https://github.com/leovan/data-science-introduction-with-r)，一份以 R 语言为基础的数据科学入门教程。![github-stars](https://img.shields.io/github/stars/leovan/data-science-introduction-with-r.svg?style=social&label=Stars)
3. [Sci-Hub EVA](https://github.com/leovan/SciHubEVA)，Sci-Hub EVA 是一个跨平台的 Sci-Hub 界面化应用。![github-stars](https://img.shields.io/github/stars/leovan/SciHubEVA.svg?style=social&label=Stars)

<h2><a href="//cdn.leovan.me/documents/cv/FanYeliang-CV-zh.pdf" target="_blank" style="border: none;">离线版本 <span class="mdi mdi-download"></span></a></h2>
