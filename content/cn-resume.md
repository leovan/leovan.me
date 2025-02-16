---
title: 简历
author: 范叶亮
date: '2017-12-04'
lastmod: '2023-04-01'
slug: cn/resume
disable_author_date: true
disable_donate: true
disable_comments: true
disable_adsense: true
disable_mathjax: true
disable_prismjs: true
---

# 范叶亮

# <span class="material-symbols material-symbols-target-outline"></span> 研究兴趣

- 现从事**数据科学**在**安全风险**领域的**技术应用**和**产品设计**。
- 对**数据科学**在**农业**和**工业**领域的应用充满兴趣。

# <span class="material-symbols material-symbols-school-outline"></span> 教育背景

- 2012.09 ~ 2015.03 **河北工业大学** 信息管理 硕士
- 2008.09 ~ 2012.07 **河北工业大学** 工商管理 学士

# <span class="material-symbols material-symbols-groups-outline"></span> 工作经历

1. 2020.08 ~ 至今 **美团** 风险数据挖掘专家
2. 2015.04 ~ 2020.08 **京东** 高级算法工程师

# <span class="material-symbols material-symbols-list-alt-outline"></span> 项目经历

## 安全和风险

_2020.08 ~ 至今 风险数据挖掘专家_

## 智慧农业

_2019.07 ~ 2020.08 算法 & 产品负责人_

- **智能种植和智能禽类解决方案**：主导构思和设计了智能种植和智能禽类商业模式和技术解决方案。带领算法和产品团队设计和实现了整个解决方案中的相关数据和算法模型，完成 SaaS 和 APP 原型设计，**从 0 到 1** 地实现了整体解决方案从 MVP 到真实生产环境的落地。
- **智能环控**：设计和实现了基于时间序列分析，深度学习和强化学习的智能环控算法和解决方案。将智能环控算法拆解为环境模型和控制模型两部分，实现了同一作物和家畜在不同环境下种养殖模型的复用。通过专家知识引擎和机器学习算法实现了在保持现有产量不变的前提下各项环境指标控制误差相比于人工降低了 **50%+**，整体平均成本（水，电，肥等）降低 **20%+**。参加 2019 年国际智慧温室种植挑战赛，在 24 小时 Hackathon 模拟挑战赛中，获得人工智能策略方法 **4/21** 名，虚拟西红柿种植净利润 **9/21** 名。
- **智能集蛋**：设计和实现了一套基于计算机视觉和 IoT 传感器的智能集蛋装置和算法。在笼养模式集蛋过程中，利用摄像头和 IoT 传感器采集的数据实现了鸡蛋计数和隶属笼体的识别，准确率 **99%+**。通过鸡蛋隶属笼体识别可以精准分析不同笼体内的料蛋比，为淘汰鸡提供强有力的数据支持，同时也为蛋品的溯源提供了更细力度的数据。

## Daat (复杂网络和知识图谱)

_2018.04 ~ 2019.06 项目负责人_

- **数据知识工程和知识问答系统**：设计和构建数据仓库，数据集市和数据工具领域的知识本体，并据此进行知识抽取和知识库构建。设计和实现了数据知识问答系统，包括：用户问题意图识别，槽填充，查询改写，结果排序以及基于深度语义模型的问题匹配。问答系统主要用于辅助数据使用者对于仓库和集市数据的查询使用，以及相关概念、流程、工具等方面问题的解答。系统服务内部 **3000+** 用户，数据相关问题咨询人工解答量降低 **50%+**。
- **自动化敏感信息识别**：对于入库到数据仓库中的数据进行自动敏感信息识别，辅助数据加密策略实施。根据数据的元信息 (例如：表名，表注释，字段名，字段注释等) 和值信息 (即字段存储的数据值)，利用 Wide & Deep 网络构建识别模型。提取传统特征构建 Wide 网络，针对文本特征，利用 Char Embedding + CNN 构建 Deep 网络，模型测试数据的 F1-Score 为 **0.95+**。
- **大规模异构网络嵌入**：实现针对**千万级别顶点**和**亿级别边**的异构网络嵌入算法。通过 Alias 方法进行高效地加权节点采样，实现了基于具有丰富业务含义元路径 (Meta-Path) 和其他算法的网络节点嵌入。利用异构网络节点嵌入结果作为节点特征 (例如：用户，商品等) 为风控，营销和推荐等业务模型和系统提供服务。
- **基于用户网络和用户行为的推荐和营销**：通过用户的历史购买记录构建包含用户，商品 (实物，理财等) 等多类型节点和边的异构网络，并利用异构网络嵌入算法构建不同类型节点的向量表示。结合用户传统特征和用户在线行为，构建推荐候选结果生成和营销人群生成模型，结合最终业务模型，平均辅助提升效果 **20%+**。

## 全视之眼 (中文地址分析)

_2015.04 ~ 2018.04 项目负责人_

- **地址分析算法引擎**：设计和开发中文地址分词，分类，完整度，POI 识别，相似度等基础算法和服务，算法平均准确率 **90%+**。
- **地址画像系统**：依托地址分析算法引擎，设计地址 POI。 画像相关指标体系，存储和服务框架。对内，服务于线下支付等场景下的营销和运营，平均提升用户转化率 **30%+**；对外，接入京东金融稻田等平台，提供精确查询，模糊查询和经纬度范围查询等多种查询方式，实现金融科技的对外输出。
- **授信和反欺诈模型**：依据地址画像构建授信策略，辅筛选和授信用户超过 **1000 万人**。依托地址分析算法和地址画像，构建中介识别等反欺诈模型，识别套现订单金额约 **20 万元/日**。
- 全视之眼项目斩获 2017 年度京东集团京芽杯创新大赛 **“创新种子奖”**，排名 **20/378**。
- **企业地址画像系统**：构建企业、地址和用户关系，设计企业地址画像相关指标体系，服务于 [**京东企业信用**](https://icredit.jd.com/)，对内外部提供离线数据和实时查询服务。
- **农村金融小站选址模型**：根据地址画像系统，结合农村金融相关业务，构建基于地址画像的农村金融小站选址模型和系统，为农村金融小站的线下选址提供辅助决策。

## 用户行为分析

_2017.10 ~ 2017.12 算法设计和开发_

- 设计开发了一种 Behavior2Vec 用户行为表示方法，基于层次聚类和深度搜索，构建了一个用于识别用户异常行为的混合模型。在校园白条中介激活和账号盗用问题上，相比传统的 Bag of Words 和 N-GRAM 等表示方法，在保证**准确率 80%+** 的前提下，提高异常用户识别数量 **3+ 倍**。

## 动产融资

_2015.04 ~ 2015.10 算法设计和开发_

- 设计开发一种基于 Bass 扩散模型，优化的时间序列相似度和聚类算法的混合产品生命周期识别模型，尾货识别**准确率 95%+**，辅助贷款方商品质押准入决策和质押率的制定。
- 设计开发不同数据源的商品信息融合模型，相同商品识别**准确率 90%+**，配合 ElasticSearch 开发商品模糊匹配查询服务，为商品质押提供精准的价格等相关信息。

# <span class="material-symbols material-symbols-settings-outline"></span> 专业技能

## 开发语言

- <i class="icon icon-python">Python</i>: <span class="material-symbols material-symbols-star-fill"></span><span class="material-symbols material-symbols-star-fill"></span><span class="material-symbols material-symbols-star-fill"></span><span class="material-symbols material-symbols-star-fill"></span><span class="material-symbols material-symbols-star-outline"></span>
- <i class="icon icon-r">R</i>: <span class="material-symbols material-symbols-star-fill"></span><span class="material-symbols material-symbols-star-fill"></span><span class="material-symbols material-symbols-star-fill"></span><span class="material-symbols material-symbols-star-fill"></span><span class="material-symbols material-symbols-star-outline"></span>
- <i class="icon icon-javascript">JavaScript</i> / <i class="icon icon-typescript">TypeScript</i>: <span class="material-symbols material-symbols-star-fill"></span><span class="material-symbols material-symbols-star-fill"></span><span class="material-symbols material-symbols-star-fill"></span><span class="material-symbols material-symbols-star-outline"></span><span class="material-symbols material-symbols-star-outline"></span>

## 平台框架

- <i class="icon icon-pytorch">PyTorch</i>: <span class="material-symbols material-symbols-star-fill"></span><span class="material-symbols material-symbols-star-fill"></span><span class="material-symbols material-symbols-star-fill"></span><span class="material-symbols material-symbols-star-outline"></span><span class="material-symbols material-symbols-star-outline"></span>
- <i class="icon icon-spark">Spark</i>: <span class="material-symbols material-symbols-star-fill"></span><span class="material-symbols material-symbols-star-fill"></span><span class="material-symbols material-symbols-star-fill"></span><span class="material-symbols material-symbols-star-outline"></span><span class="material-symbols material-symbols-star-outline"></span>
- <i class="icon icon-qt">Qt</i>: <span class="material-symbols material-symbols-star-fill"></span><span class="material-symbols material-symbols-star-fill"></span><span class="material-symbols material-symbols-star-fill"></span><span class="material-symbols material-symbols-star-outline"></span><span class="material-symbols material-symbols-star-outline"></span>
- <i class="icon icon-react">React</i>: <span class="material-symbols material-symbols-star-fill"></span><span class="material-symbols material-symbols-star-fill"></span><span class="material-symbols material-symbols-star-outline"></span><span class="material-symbols material-symbols-star-outline"></span><span class="material-symbols material-symbols-star-outline"></span>

## 外语能力

- 英语: CET6 518，能说，会写，看菜单略费劲...

# <span class="material-symbols material-symbols-award-star-outline"></span> 研究成果

## 论文

1. Zhou, F., Yin, H., Zhan, L., Li, H., **Fan, Y.**, & Jiang, L. (2018). A Novel Ensemble Strategy Combining Gradient Boosted Decision Trees and Factorization Machine Based Neural Network for Clicks Prediction. In _2018 International Conference on Big Data and Artificial Intelligence (BDAI)_ (pp. 29-33). IEEE.
2. Li, J., **Fan, Y.\***, Xu, Y., & Feng, H. (2013). An Improved Forecasting Algorithm for Spare Parts of Short Life Cycle Products Based on EMD-SVM. In _Information Science and Cloud Computing Companion (ISCC-C), 2013 International Conference on_ (pp. 722-727). IEEE.
3. **Fan, Y.**, Li, J., Chu, C. (2014). [IEAF: A Hybrid Method for Forecasting Short Life Cycle Spare Parts](https://cdn.leovan.me/documents/publications/IEAF.pdf). _Unpublished_.

## 专利

1. 一种中文地址分词方法及系统 (发明，[CN 105159949](http://epub.cnipa.gov.cn/patent/CN105159949B)，**授权**，第一发明人，2015)
2. 一种产品库存预测方法及装置 (发明，[CN 106056239](http://epub.cnipa.gov.cn/patent/CN106056239B)，**授权**，第一发明人，2016)
3. 数据仓库信息处理方法、装置、系统、介质 (发明，[CN 109388637](http://epub.cnipa.gov.cn/patent/CN109388637B)，**授权**，第一发明人，2018)
4. 一种数据处理方法、装置、设备及介质 (发明，[CN 110309235](http://epub.cnipa.gov.cn/patent/CN110309235B)，**授权**，第一发明人，2019)
6. 用于生成信息的方法和装置 (发明，[CN 110309235](http://epub.cnipa.gov.cn/patent/CN112395490B)，**授权**，第一发明人，2019)

## 技术项目

- **技术主页**：[https://leovan.tech](https://leovan.tech)
- **Github**: [https://github.com/leovan](https://github.com/leovan) ![github-followers](https://img.shields.io/github/followers/leovan?style=social&label=Follow)

1. [R 语言数据科学导论](https://ds-r.leovan.tech)：一份以 R 语言为基础的数据科学入门教程。![github-stars](https://img.shields.io/github/stars/leovan/data-science-introduction-with-r.svg?style=social&label=Stars)
2. [Python 数据科学导论](https://ds-python.leovan.tech)：一份以 Python 为基础的数据科学入门教程。![github-stars](https://img.shields.io/github/stars/leovan/data-science-introduction-with-python.svg?style=social&label=Stars)
3. [Sci-Hub EVA](https://github.com/leovan/SciHubEVA)：Sci-Hub EVA 是一个跨平台的 Sci-Hub 界面化应用。![github-stars](https://img.shields.io/github/stars/leovan/SciHubEVA.svg?style=social&label=Stars)
4. [XGMML](https://github.com/leovan/xgmml)：XGMML 是一个用于解析和生成 XGMML 文件的 Python 库。![github-stars](https://img.shields.io/github/stars/leovan/xgmml.svg?style=social&label=Stars)
5. [中文 Duckling](https://github.com/leovan/duckling-chinese)：中文 Duckling 是基于 Jpype1 的 [duckling-fork-chinese](https://github.com/XiaoMi/MiNLP/tree/main/duckling-fork-chinese) 的 Python 封装版本，提供例如时间、日期、数字等中文解析服务。![github-stars](https://img.shields.io/github/stars/leovan/duckling-chinese.svg?style=social&label=Stars)
6. [Hive 函数](https://hive-functions.leovan.tech)：实用自定义 Hive 函数集。 ![github-stars](https://img.shields.io/github/stars/leovan/hive-functions.svg?style=social&label=Stars)
7. [Cytoscape 中文用户手册](https://cytoscape.leovan.tech)：Cytoscape 中文用户手册。 ![github-stars](https://img.shields.io/github/stars/leovan/cytoscape-manual.svg?style=social&label=Stars)
8. [Quarto 伪代码扩展](https://github.com/leovan/quarto-pseudocode)：一个用于在 `html` 和 `pdf` 文档中渲染伪代码的 Quarto 扩展。![github-stars](https://img.shields.io/github/stars/leovan/quarto-pseudocode.svg?style=social&label=Stars)
9. [Quarto 水印扩展](https://github.com/leovan/quarto-watermark)：一个用于在 `html` 和 `pdf` 文档中添加水印的 Quarto 扩展。![github-stars](https://img.shields.io/github/stars/leovan/quarto-watermark.svg?style=social&label=Stars)
10. [Quarto 样式文本扩展](https://github.com/leovan/quarto-style-text)：一个用于在 `html` 和 `pdf` 文档中渲染样式文本的 Quarto 扩展。![github-stars](https://img.shields.io/github/stars/leovan/quarto-style-text.svg?style=social&label=Stars)
11. [Rasa 中文文档](https://rasa.leovan.tech)：Rasa 中文文档。 ![github-stars](https://img.shields.io/github/stars/leovan/rasa-doc.svg?style=social&label=Stars)
12. [Rasa Pro 中文文档](https://rasa-pro.leovan.tech)：Rasa Pro 中文文档。 ![github-stars](https://img.shields.io/github/stars/leovan/rasa-pro-doc.svg?style=social&label=Stars)

<h2 style="text-align: right;"><a href="//cdn.leovan.me/documents/cv/FanYeliang-CV-zh.pdf" target="_blank" style="border: none;">离线版本 <span class="material-symbols material-symbols-download-outline"></span></a></h2>

<p class="kai" style="text-align: right;">更新于：2025-02-16</p>
