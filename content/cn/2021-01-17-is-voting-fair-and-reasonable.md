---
title: 投票公平合理吗？
author: 范叶亮
date: '2021-01-17'
slug: is-voting-fair-and-reasonable
categories:
  - 思辨
tags:
  - 投票
  - 公平
  - 合理
  - 陶片放逐制
  - 克里斯提尼
  - 美国选举
  - 美国大选
  - 选举人团
  - 聚会
  - 团建
  - 烧烤
  - 火锅
  - 多数制
  - Plurality Voting System
  - 多数代表制
  - Majoritarian Representation
  - 相对多数
  - Relative Plurality
  - 绝对多数
  - Absolute Majority
  - 波达计数法
  - Borda Count
  - 孔多塞
  - Condorcet
  - 孔多塞胜利者
  - 孔多塞赢家
  - 孔多赛循环
  - 孔多塞悖论
  - Condorcet Paradox
  - 投票悖论
  - Voting Paradox
  - Facebook
  - 肯尼斯·阿罗
  - Kenneth Arrow
  - 一致性
  - Unanimity
  - 帕累托最优
  - Pareto Efficiency
  - 非独裁
  - Non-Dictatorship
  - 独立于无关选项
  - IIA
  - 阿罗悖论
  - Arrow Paradox
images:
  - /images/cn/2021-01-17-is-voting-fair-and-reasonable/agma-ostrakon-aristide.png
  - /images/cn/2021-01-17-is-voting-fair-and-reasonable/usa-electoral-college-2020-with-results.png
  - /images/cn/2021-01-17-is-voting-fair-and-reasonable/barbecue-or-hot-pot.png
  - /images/cn/2021-01-17-is-voting-fair-and-reasonable/facemash.png
---

> 只有道德上的相对民主，没有制度上的绝对公平，求同存异才能长治久安。

# 无处不在的投票

在古代雅典城邦有一项政治制度称之为[**陶片放逐制**](https://zh.wikipedia.org/wiki/陶片放逐制)，是由雅典政治家[克里斯提尼](https://zh.wikipedia.org/wiki/克里斯提尼)于公元前 510 年创立。雅典人民可以通过投票强制将某个人放逐，目的在于驱逐可能威胁雅典的民主制度的政治人物。投票者在选票——陶罐碎片较为平坦处，刻上他认为应该被放逐者的名字，投入本部落的投票箱。如果选票总数未达到 6000，此次投票即宣告无效；如果超过 6000，再按票上的名字将票分类，得票最多的人士即为当年放逐的人选。

![](/images/cn/2021-01-17-is-voting-fair-and-reasonable/agma-ostrakon-aristide.png)

美国总统选举的方式称为[**选举人团**](https://zh.wikipedia.org/wiki/選舉人團_\(美國\))，是一种间接选举，旨在选出美国总统和副总统。根据《美国宪法》及其修正案，美国各州公民先选出该州的选举人，再由选举人代表该州投票。不采用普选制度的原因，主要是由于美国是联邦制国家，并考虑到各州的特定地理及历史条件，制宪元老决定采取选举人团制度，保障各州权益，所以美国没有公民直选的总统。

![](/images/cn/2021-01-17-is-voting-fair-and-reasonable/usa-electoral-college-2020-with-results.png)

离我们最近的可能就是朋友聚会吃什么这个问题了，烧烤还是火锅，这是个问题。当然，只要你想要，还可以：蒸羊羔、蒸熊掌、蒸鹿尾儿、烧花鸭、烧雏鸡、烧子鹅 ......

![](/images/cn/2021-01-17-is-voting-fair-and-reasonable/barbecue-or-hot-pot.png)

# 投票制度

## 多数制

[**多数制**](https://zh.wikipedia.org/wiki/多數制)（Plurality Voting System）的原则是“胜者全取”，又被称为**多数代表制**（Majoritarian Representation），分成**相对多数**（Relative Plurality）和**绝对多数**（Absolute Majority）。相对多数制即不论票数多少，得票最多的候选人便可当选。绝对多数制指候选人需要得到指定的票数方可当选，门槛在设定上须达有效票之过半数、三分之二、四分之三或五分之四等多数，亦可以是更高的比例或数字。

多数制的优点在于简单易行，缺点在于当选票分散的越平均，投票结果的争议性就会越大。例如：有 10 人参与投票，有 3 人选择吃火锅，有 3 人选择吃烧烤，有 4 人选择吃家常菜。根据多数制规则，最终的选择为吃家常菜，但会有 6/10 的人没有得到满意的结果。

## 波达计数法

[**波达计数法**](https://zh.wikipedia.org/wiki/波達計數法)（Borda Count）是通过投票人对候选者进行排序，如果候选者在选票的排第一位，它就得某个分数，排第二位得一个较小的分数，如此类推，分数累计下来最高分的候选者便取胜。

波达计数法相比于多数制不容易选出比较有争议的选项。假设有一场选举，共 4 位候选人，共收集到有效选票 100 张，选票统计结果（理论山可能出现的选票类型为 `$4! = 24$` 种可能，简单起见，示例中仅有 4 种可能）如下：

| #    | 51 票    | 5 票     | 23 票    | 21 票    |
| :--: | :------: | :------: | :------: | :------: |
| 1    | **张三** | **王五** | 李四     | 马六     |
| 2    | **王五** | 李四     | **王五** | **王五** |
| 3    | 李四     | 马六     | 马六     | 李四     |
| 4    | 马六     | **张三** | **张三** | **张三** |

选举采用排名第 `$n$` 位得 `$4 - n$` 分的准则，每个人的分数如下：

- 张三：`$51 \times 3 + 5 \times 0 + 23 \times 0 + 21 \times 0 = 153$`
- 李四：`$51 \times 1 + 5 \times 2 + 23 \times 3 + 21 \times 1 = 151$`
- 王五：`$51 \times 2 + 5 \times 3 + 23 \times 2 + 21 \times 2 = 205$`
- 马六：`$51 \times 0 + 5 \times 1 + 23 \times 1 + 21 \times 3 = 91$`

按照多数制应该是张三获胜（得到第 1 名的票数最多，共计 51 票）。不过通过波达计数法可以发现大家对张三的喜好比较极端：只有特别喜欢（排名第 1）和特别不喜欢（排名第 4）两种情况，所以张三是一个**具有争议的人**。但王五不同，虽然其获得第 1 的选票并不多，但是获得第 2 的选票很多，说明**大部分人都是比较能接受**王五的。

波达计数法同时也存在几个问题：

1. 不同的权重的计分规则，可能得到不同结果。以下表为例：

    | #    | 2 票 | 3 票 | 4 票 | #    |
    | :--: | :--: | :--: | :--: | :--: |
    | 2 分 | A    | A    | C    | 5 分 |
    | 1 分 | B    | C    | B    | 2 分 |
    | 0 分 | C    | B    | A    | 1 分 |

    采用左边权重的计分结果为：A：10 分，B：6 分，C：11 分，则 C 胜出。采用右边权重的计分结果为：A：29 分，B：15 分，C：28 分，则 A 胜出。不难看出，多数投票制是波达计数法的一个特例，即第 1 名的权重为非零值，其余名次权重均为零。

2. 容易出现恶意投票局面。参与的人在投票时往往会掺杂个人情感，假设存在这样一次选举：张三、李四、王五三人竞选班长，张三和李四是最有希望竞争班长的人员，而王五则表现平庸。参与投票的同学几乎近一半的人支持张三，近一半的人支持李四，很少人支持王五。参与投票的同学自认为都很“聪明”，担心自己不支持的人（假设为李四）担任班长，同时认为王五没希望竞选成功，因此在排序时会把王五排在第 2 名，把李四排在第 3 名。此时，张三和李四都变成了具有争议的人，那么选举的结果就很有可能是王五获胜。

## 孔多赛投票制

波达计数法还存在一个严重的问题是，当其中一个选项退出后，投票的结果会发生变化。仍然以上文中的例子为例：

| #    | 2 分 | 1 分 | 0 分 | #    | 1 分 | 0 分 |
| :--: | :--: | :--: | :--: | :--: | :--: | :--: |
| 2 票 | A    | B    | C    | 2 票 | A    | C    |
| 3 票 | A    | C    | B    | 3 票 | A    | C    |
| 4 票 | C    | B    | A    | 4 票 | C    | A    |

在包含选项 B 时，投票结果为：A：10 分，B：6 分，C：11 分，C 获胜。当把选项 B 去掉后，投票结果为：A：5 分，C：4 分，A 获胜。去掉选项 B，规则没有发生变化（不同排名之间权重相差为 1），投票人的意愿也没有发生变化（候选人的相对名次没有发生变动），但投票结果却截然不同。

为了解决这个问题，**孔多赛**提供了采用两两对决的方式进行投票。投票人依旧按照类似波达计数法对候选人进行排序，但与波达计数法不同的是并不进行计分而是需要统计出所有两两对决的情况。上面这个例子中两两对决的情况有 6 种：`A > B`，`B > A`，`B > C`，`C > B`，`A > C`，`C > A`，对决的统计结果如下表所示：

| #    | 5 次 | 4 次 | 2 次 | 7 次 | 5 次 | 4 次 |
| :--: | :--: | :--: | :--: | :--: | :--: | :--: |
| 1 分 | A    | B    | B    | C    | A    | C    |
| 0 分 | B    | A    | C    | B    | C    | A    |

由于 `A > B` 有 5 次，`B > A` 有 4 次，因此在 A 和 B 的两两对决中获胜的是 A。同理可得，在 A 和 C 的两两对决中获胜的是 A，在 B 和 C 的两两对决中获胜的是 C。当存在很多选项时，假设选项 A 在与任何其它选项的两两比较中都能胜出，那 A 称为**孔多塞胜利者**。

如果你对 Facebook 历史有了解，早期扎克伯格在哈佛大学就读学士期间，写了一个名为 Facemash 的网站程序，根据哈佛校内报纸《The Harvard Crimson》，Facemash 会从校内的网络上收集照片，每次将两张照片并排后让用户选择“更火辣”的照片。Facemash 就采取了类似孔多塞投票的方法对女生进行投票，下图是电影[社交网络](https://movie.douban.com/subject/3205624/)中这个原型的截图：

![](/images/cn/2021-01-17-is-voting-fair-and-reasonable/facemash.png)

孔多塞投票制由于统计比较麻烦，现实生活中使用的情况不多。同时，孔多塞投票也存在一个问题，即**孔多塞循环**。假设 A 和 B 对决的优胜者为 A，B 和 C 对决的优胜者为 B，C 和 A 对决的优胜者为 C，则没有一个选项打败其他所有选项，那么这样就无法得到投票的结果。这称之为[**孔多塞悖论**](https://zh.wikipedia.org/wiki/投票悖论)（投票悖论），在这个假想情况中，集体倾向可以是循环性的，即使个人的倾向不是。

# 所以呢？

所以什么样的投票才算是公平合理的投票呢？[肯尼斯·阿罗](https://zh.wikipedia.org/wiki/肯尼斯·阿罗)给出了一个解答。

有 `$N$` 种选择，有 `$m$` 个决策者，他们每个人都对这 `$N$` 个选择有一个从优至劣的排序。我们要设计一种选举法则，使得将这 `$m$` 个排序的信息汇总成一个新的排序，称为投票结果。我们希望这种法则满足[以下条件](https://zh.wikipedia.org/wiki/阿罗悖论)：

1. **一致性（Unanimity）**。或称为[帕累托最优](https://zh.wikipedia.org/wiki/帕累托最优)（Pareto Efficiency），即如果所有的 `$m$` 个决策者都认为选择 `$A$` 优于 `$B$`，那么在投票结果中，`$A$` 也优于 `$B$`。
2. **非独裁（Non-Dictatorship）**。不存在一个决策者 `$X$`，使得投票结果总是等同于 `$X$` 的排序。
3. **独立于无关选项（Independence of Irrelevant Alternatives，IIA)）**。如果现在一些决策者改了主意，但是在每个决策者的排序中，`$A$` 和 `$B$` 的相对位置不变，那么在投票结果中 `$A$` 和 `$B$` 的相对位置也不变。

如果选项 `$N \geq 3$`，投票人数 `$m \geq 2$` 时，没有任何一种投票规则能够满足以上 3 点，这就是[阿罗悖论](https://zh.wikipedia.org/wiki/阿罗悖论)。所以只有道德上的相对民主，没有制度上的绝对公平，求同存异才能长治久安。

> 本文参考自《[投票公平合理吗？为什么没有绝对的公平？阿罗不可能定理](https://www.youtube.com/watch?v=9Oisrp99L14)》。
