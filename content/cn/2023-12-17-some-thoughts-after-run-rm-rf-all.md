---
title: 从 rm -rf * 说起
subtitle: 喜新、怀旧、再出发
author: 范叶亮
date: '2023-12-17'
slug: some-thoughts-after-run-rm-rf-all
categories:
  - 生活
  - 思考
tags:
  - 喜新
  - 厌旧
  - 怀旧
  - 念想
  - 再出发
---

故事要从昨晚的事故说起，在软路由中删除了一个 Docker 容器，想着相关配置和数据目录也都用不到了就删掉吧。进入目录后「聪明」的我就执行了 `rm -rf *`，等回头去看命令执行情况已然为时已晚。为什么说我「聪明」呢，因为自从知道[一个空格引起的 /usr 被删除的血案](https://github.com/MrMEEE/bumblebee-Old-and-abbandoned/issues/123)后，在做删除动作时我都会谨慎再谨慎，然而这次的悲剧在于目录下通过 NFS 挂载了 NAS 上的远程目录，删除前忘记取消挂载了，结果就是 NAS 上 4 块盘里面的影视资料被我一键清空了。

想着十多个 TB 的影视资料就这么没了，到也没有太伤感，毕竟技术男认为总还是可以恢复的，无非就是费些时间的问题。所以做的第一件事就是把 NAS 关机了，因为一旦再写入新的数据，被删除的数据可能就真的无法恢复了。关机后就开始找 SATA 线（NAS 里面是 3.5 寸的机械硬盘，使用 SATA 口通信），发现没有就赶紧买了一根第二天可以到的，至此第一笔 60 大洋（3.5 寸的硬盘还得单独供电，好不容易找到一个便宜的带电源的套装）损失就出去了。然后就开始各种找资料，NAS 里面的硬盘格式是 Btrfs 的，可用的恢复工具一下子就少了，翻着翻着发现就已经凌晨一点。怀着一丝丝担忧还是决定先睡了，明天早起再说吧，反正 SATA 线最快也得下午才能到。

# 喜新

这一切的一切要往前捯就只怪我「喜新厌旧」。搬到新家利用软路由和 NAS [搭建了一套家庭影音中心](/cn/2023/01/build-home-media-center-with-jellyfin-on-openwrt/)，老老实实看就得了呗，非要瞎鼓捣。在 Jellyfin 中显示的影视信息读取的元信息文件有些问题，提的 [PR](https://github.com/jellyfin/jellyfin/pull/10339) 也是做了各种测试才成功合并到主干，尽管只是改了一行代码的位置，但维护人员的严谨还是很让我受教的。虽然合并到了主干，但由于大版本更新发布还未确定时间，当时自己就临时针对当前版本调整了代码编译部署到了自己的软路由上先用起来了。

后续稳定版本也发布了几个修复问题的小版本更新，但合并的代码并不在更新范围内，自己懒了也就没再更新 Docker 镜像。直到昨天晚上也许就是闲来无事，想着要不就更新到非稳定版本用吧，同时一不做二不休还把刮削用的 tinyMediaManager 也更新下吧，然后就没有然后了，事故就发生了。

我是一个比较喜欢尝鲜的人，每天到公司不执行一下 `brew update & brew upgrade` 就不舒服。而且还不能搞成定时任务，就得手动执行，然后看着相关工具更新到最新版本就会很舒服。我承认在一些「大型」项目中，兼容和稳定才是第一追求，但我认为我还真么参与到过那种「大」到处处都要为兼容和稳定考虑的项目中过，所以我还是很喜欢尝试新的特性。当然工作中尝鲜用到的也得至少是正式发布的版本。最近的一次大迁移就是把我所有的 Python 项目都从 3.7 升级到了 3.10，为啥不是 3.11 呢，因为有些依赖包没我走得快，对 3.11 还不支持。我大部分是在做数据和算法工作，少部分时间也会用 Python 写一些工程性质的代码，在这个领域我认为「喜新」是一件好事，这会让你在面对一个问题时更有可能说出「我行」。

# 怀旧

我其实还挺两面派的，刚刚还在「喜新厌旧」，现在又说「怀旧」。老人经常说人要有个「念想」，但此时此刻我发现我的「念想」有点儿多了，多到可能束缚到了我的前行。NAS 是我大概 6 年前买的了，去年淘汰了里面两块老旧的小硬盘，又补上了两块 8TB 的。里面存的都是从 PT 站下载的高清影视资料，今年也终于成功的将 PT 站的账号升到了永久保号的等级，看了看上传量也近 20TB 了。文件被删掉的那一刻都是在想怎么恢复，但当发现恢复有一定的难度后，我突然有在想要不要恢复。

其实这么多年下载了这么多高清的影视资料，真正回过头再去看的次数不算多，一是没那么多时间，二是有新的内容可以选择。所以这么多「怀旧」的东西可能并不是「念想」，而只是满足「占有欲」的电子榨菜。这就和[买书与读书](/cn/2018/07/buy-books-hoard-books-and-read-books/)是一回事儿，不是买了书有了书，知识就是你的了。多年前的我认识到了这个问题，但好像改进的并不理想，尤其是疫情这几年，身体没空去旅行，然而思想也没有在路上。不过感觉近期有所改善，至少近几个月快读完三本书了。

中午眯了会儿醒来还是决定把四块硬盘重新格式化了，也正好把之前一个磁盘和存储空间顺序不一致的问题做了纠正，如实让我这个强迫症选手舒服了一些。后面把原来移动硬盘中的照片重新又备份了一份到 NAS 中，「念想」这东西有点儿就够了。弄完了，心情一下子轻松了不少，毕竟不用再为恢复数据发愁了，尤其是在这种你还不知道能不能恢复的情况下。唯一还有些心疼的就是花 60 大洋买的 SATA 线，看了看快递小哥已经送上货了，就留着吧，万一将来有啥用呢。

# 再出发

后疫情时代的第一年马上就要过去了，这一年的种种个人感觉都不尽如人意，也正是不如人意才会让我去思考更多，改变更多。变革不一定会创造机会，哪怕创造了机会能不能抓住也难说，但对变革的思考和自身的改变是可以主动发起的。抛下一些陈旧的包袱，再去想想你真正想要的，透彻一些，会发现变革不一定是坏事。

大家都在往前走，这是我们认为的，也是我们想要的，至少是我想要的。可我真的在往前走吗？或许慢慢地陷入了舒适圈，或许被过往的「念想」不知不觉牵绊住了，所以不经意的一个变数，或好或坏，都给了我们重新审视自我和世界的机会。停下来，思考片刻，再出发，来得及，也值得。