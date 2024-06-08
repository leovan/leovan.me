---
title: 在 OpenWrt 中安装 Jellyfin 搭建家庭影音中心
author: 范叶亮
date: '2023-01-24'
slug: build-home-media-center-with-jellyfin-on-openwrt
categories:
  - 生活
tags:
  - OpenWrt
  - Jellyfin
  - NAS
  - PT
  - Plex
  - Apple TV
  - Chromecast
  - Google TV
  - Infuse
  - Docker
  - TMM
  - tinyMediaManager
  - 刮削
  - 影音中心
  - Swiftfin
  - Findroid
images:
  - /images/cn/2023-01-24-build-home-media-center-with-jellyfin-on-openwrt/tmm-init.png
  - /images/cn/2023-01-24-build-home-media-center-with-jellyfin-on-openwrt/jellyfin-movie-info.png
---

# 历史尝试

入手 NAS 已经近 5 年的时间了，最初只是用来挂 PT 下载，然后在各种设备上通过 SMB 共享播放上面的视频。后面也尝试在利用 Plex 搭建家庭影音中心，但由于 Plex 的高级功能需要付费也就作罢。今年搬家后整体对各种硬件做了升级，换了软路由，做了基于 AC+AP 的全屋 WiFi，NAS 换了更大的硬盘，客厅和卧室各安装了一个投影机，入了 Apple TV 4K 和 Chromecast with Google TV 4K 两个盒子。购买 Apple TV 时买了有 Infuse 的套餐，果然没有花钱的不是，Infuse 无论是从 UI 还是体验上都算优秀，但由于仅限于苹果生态，且可玩性较差，最终也只是沦为了 Apple TV 上的本地播放器。

秉着「付费虽美丽，免费更开心」的原则，最终选择了基于 Jellyfin 的方案。由于 NAS 的 CPU 性能并不高，为了不给 NAS 其他功能带来过多压力，同时考虑软路由性能过剩，因此决定将 Jellyfin 安装在软路由上，再将 NAS 的资源挂载到软路由来实现整体解决方案。

在做 Jellyfin 选型时，其吸引我的最大优点就是开源，同时各个平台的客户端也都在官方应用商店有上架，这极大的简化了客户端的安装流程。付费解决方案，例如：Plex，Emby（在 3.5.3 之后闭源），由于有更多资金的支持，肯定在一些方面会优于 Jellyfin。其他的免费解决方案，例如：NAS 自带的 Video Station，Kodi（大学时代就曾在电脑上安装过）等在不同方面也各有差异。关于不同解决方案的一些差异在此就不再做深入探究，有兴趣的同学可以自行 Google，不过也要注意很多文章时间会比较久了，与当下的实际情况会有部分出入。

# 硬件设备

## 服务端设备

| 设备   | 系统    | CPU                                                   | 内存 | 用途                                     | 网络连接   | 位置   |
| :----- | :------ | :---------------------------------------------------- | :--- | :--------------------------------------- | :--------- | :----- |
| 软路由 | OpwnWrt | Intel Celeron N5105<br/>2.0-2.9 GHz<br/>4 核心 4 线程 | 4GB  | 主路由<br/>代理服务器<br/>内网穿透服务器 | 有线 1000M | 客厅   |
| NAS    | DSM 7   | Intel Celeron J3355<br/>2.0-2.5 GHz<br/>2 核心 2 线程 | 6GB  | 共享存储<br/>PT 下载<br/>迅雷远程下载    | 有线 1000M | 衣帽间 |

NAS 通过有线网络与主路由直连，虽然主路由网口为 2.5G，但由于 NAS 网口仅为 1000M，而且又懒于把 NAS 上的双网口做链路聚合，因此实际通讯也就限制为 1000M，但对于家庭影音中心也基本够用了。主路由上游使用了运营商提供的光猫，虽然已经改了桥接模式，但由于运营商提供的光猫 LAN 口也是 1000M 的，因此外网也无法突破千兆限制，当然还是由于 10G EPON 的万兆光猫太贵，压制了我鼓捣的欲望。

NAS 自带的内存为 2G，后面加了一条 4G 的内存扩容到 6G，最初也是计划用 NAS 玩一玩 Docker 的。但碍于 J3355 这颗 CPU 性能一般，运行太多东西给 NAS 的基本功能会带来不小压力，我想这也是群辉官方并没有给 DS418play 这款 NAS 提供 Docker 应用的主要原因吧。软路由当时买了非裸机的丐版，但由于并没有用其做太多事情，空闲内存基本上还有 3.5G 左右，因此为了充分利用 N5105 这颗 CPU，最终决定将需要视频解码这类耗 CPU 的任务交给软路由了。不过买的这款软路由是被动散热，正常待机就干到 60 摄氏度左右了，CPU 占用上来了估计有望突破 100 摄氏度😂。

## 客户端设备

| 设备                         | 系统             | 用途       | 网络/视频连接            | 位置 |
| :--------------------------- | :--------------- | :--------- | :----------------------- | ---- |
| Apple TV 4K                  | tvOS 16          | 主电视盒子 | 有线 1000M               | 客厅 |
| 明基 TK850                   | -                | 主投影机   | HDMI 2.1                 | 客厅 |
| Chromecast with Google TV 4K | Android 12 原生  | 次电视盒子 | 无线 WiFi 5              | 主卧 |
| 小明 Q2 Pro                  | Android 9 非原生 | 次投影机   | 无线 WiFi 5<br/>HDMI 2.1 | 主卧 |
| PC                           | Windows 11       | 台式机     | 有线 1000M               | 主卧 |
| Macbook Pro                  | macOS 13         | 笔记本     | 无线 WiFi 5              | -    |
| iPhone 13 Pro                | iOS 16           | 主手机     | 无线 WiFi 6              | -    |
| Google Pixel 6 Pro           | Android 13 原生  | 备用手机   | 无线 WiFi 6              | -    |
| iPad Pro                     | iPadOS 16        | 平板电脑   | 无线 WiFi 6              | -    |

所有客户端通过 H3C 的 1000M AC+AP 采用有线或无线间接连接到主路由。综上所述，家里各种内外部线路就都是 1000M 的理论带宽了。

客户端设备几乎覆盖了所有常用的系统，Jellyfin 在各个系统上均提供了客户端，而且可以在官方商店直接安装，这也是最终确认选择 Jellyfin 的关键一点。毕竟服务端搞得再好，客户端安装费劲的不行也是很痛苦的，尤其是在苹果生态中，官方商店的支持会让你泪大喜奔的。

# NAS 准备

由于 Jellyfin 安装在软路由上，因此需要将 NAS 上的媒体文件夹通过 NFS 映射到软路由上，首先需要在 NAS 上配置客户端。进入 NAS，打开 `控制面板`，进入 `文件服务`，确保 `启用 NFS 服务`，最大 NFS 协议选择 `NFSv4.1`：

![](/images/cn/2023-01-24-build-home-media-center-with-jellyfin-on-openwrt/nas-file-services-nfs.png)

进入 `共享文件夹`，选择需要通过 NFS 共享的文件夹：

![](/images/cn/2023-01-24-build-home-media-center-with-jellyfin-on-openwrt/nas-shared-folders.png)

单击 `编辑` 进入共享文件夹设置：

{{< figure src="/images/cn/2023-01-24-build-home-media-center-with-jellyfin-on-openwrt/nas-shared-folder-nfs.png" large-max-width="60%" middle-max-width="80%" >}}

在 `NFS 权限` 标签页单击 `新增` 添加新客户端：

{{< figure src="/images/cn/2023-01-24-build-home-media-center-with-jellyfin-on-openwrt/nas-shared-folder-nfs-new-client.png" large-max-width="60%" middle-max-width="80%" >}}

相关配置如图所示，其中 `服务器名称或 IP 地址` 为客户端 IP 地址（即软路由 IP 地址）。依次为所有需要共享的文件夹进行相同配置。

# OpenWrt 准备

软路由自带了 128G 的 NVME 固态硬盘，系统采用了 eSir 编译的高大全版本。为了后续安装扩展包和 Docker，对硬盘重新进行分区。

通过 `系统 > TTYD终端` 在输入用户名（`root`）和密码后可以进入软路由命令行，输入 `fdisk -l` 可以查看所有可用块设备的信息：

```
Disk /dev/nvme0n1: 119.24 GiB, 128035676160 bytes, 250069680 sectors
...

Device               Start       End   Sectors  Size Type
/dev/nvme0n1p1         512     33279     32768   16M Linux filesystem
/dev/nvme0n1p2       33280   1057279   1024000  500M Linux filesystem
/dev/nvme0n1p128        34       511       478  239K BIOS boot

Partition table entries are not in disk order.
```

输入 `cfdisk /dev/nvme0n1` 进入分区工具：

![](/images/cn/2023-01-24-build-home-media-center-with-jellyfin-on-openwrt/opwnert-cfdisk-01.png)

使用上下键选择分区，左右键选择要操作的选项。选中 `Free space`，使用 `[New]` 选项建立新的分区，输入分区大小，例如：`32G`：

![](/images/cn/2023-01-24-build-home-media-center-with-jellyfin-on-openwrt/opwnert-cfdisk-02.png)

本例计划为 overlay 分配 32G，为 docker 分配 32G，剩余全部分配给 data：

![](/images/cn/2023-01-24-build-home-media-center-with-jellyfin-on-openwrt/opwnert-cfdisk-03.png)

使用 `[Write]` 选项将结果写入分区表，并在确认处输入 `yes` 提交：

![](/images/cn/2023-01-24-build-home-media-center-with-jellyfin-on-openwrt/opwnert-cfdisk-04.png)

提交完毕后使用 `[Quit]` 选项退出分区工具。再次输入 `fdisk -l` 可以查看所有可用块设备的信息：

```
Disk /dev/nvme0n1: 119.24 GiB, 128035676160 bytes, 250069680 sectors
...

Device               Start       End   Sectors  Size Type
/dev/nvme0n1p1         512     33279     32768   16M Linux filesystem
/dev/nvme0n1p2       33280   1057279   1024000  500M Linux filesystem
/dev/nvme0n1p3     1058816  68167679  67108864   32G Linux filesystem
/dev/nvme0n1p4    68167680 135276543  67108864   32G Linux filesystem
/dev/nvme0n1p5   135276544 250068991 114792448 54.7G Linux filesystem
/dev/nvme0n1p128        34       511       478  239K BIOS boot

Partition table entries are not in disk order.
```

分别对新分区进行格式化：

```bash
mkfs.ext4 /dev/nvme0n1p3
mkfs.ext4 /dev/nvme0n1p4
mkfs.ext4 /dev/nvme0n1p5
```

将 `/dev/nvme0n1p3` 挂载至 `/mnt/nvme0n1p3`：

```bash
mount /dev/nvme0n1p3 /mnt/nvme0n1p3
```

将 `/overlay` 分区数据全部复制到 `/mnt/nvme0n1p3` 中：

```bash
cp -R /overlay/* /mnt/nvme0n1p3/
```

以上完成后，进入 OpenWrt 管理后台，在 `系统 > 挂载点` 菜单的 `挂载点` 处，单击 `添加` 按钮添加挂载点，将 `/dev/nvme0n1p3` 挂载为 `/overlay`，将 `/dev/nvme0n1p4` 挂载为 `/opt`，将 `/dev/nvme0n1p5` 挂载为 `/data`：

{{< figure src="/images/cn/2023-01-24-build-home-media-center-with-jellyfin-on-openwrt/mount-overlay.png" large-max-width="60%" middle-max-width="80%" >}}

{{< figure src="/images/cn/2023-01-24-build-home-media-center-with-jellyfin-on-openwrt/mount-docker.png" large-max-width="60%" middle-max-width="80%" >}}

{{< figure src="/images/cn/2023-01-24-build-home-media-center-with-jellyfin-on-openwrt/mount-data.png" large-max-width="60%" middle-max-width="80%" >}}

单击 `保存&应用` 后重启路由器，重启完毕后在命令行输入 `df -h` 可以看出所有分区均成功挂载：

```
Filesystem                Size      Used Available Use% Mounted on
...
/dev/nvme0n1p3           31.2G     87.9M     26.6G   0% /overlay
overlayfs:/overlay       31.2G     87.9M     26.6G   0% /
/dev/nvme0n1p4           31.2G    356.0K     29.6G   0% /opt
/dev/nvme0n1p5           53.6G     24.0K     50.8G   0% /data
...
```

在 `/data` 目录中创建用于字体的目录：

```bash
mkdir /data/fonts
```

下载 CJK 相关字体至该目录，例如：[Noto Sans CJK](https://github.com/notofonts/noto-cjk/tree/main/Sans)。

在 `/data` 目录中创建用于 Jellyfin 的目录：

```bash
mkdir /data/docker
mkdir /data/docker/jellyfin
mkdir /data/docker/jellyfin/config
mkdir /data/docker/jellyfin/config/fonts
mkdir /data/docker/jellyfin/cache
mkdir /data/docker/jellyfin/media
mkdir /data/docker/jellyfin/media/nas
mkdir /data/docker/jellyfin/media/nas/disk1
mkdir /data/docker/jellyfin/media/nas/disk2
mkdir /data/docker/jellyfin/media/nas/disk3
mkdir /data/docker/jellyfin/media/nas/disk4
```

由于在 Docker 中需要使用 `1000:1000` 作为 UID 和 GID 运行 Jellyfin，需要将 `jellyfin` 目录修改为对应所有者：

```
chown -R 1000:1000 /data/docker/jellyfin/
```

进入命令行，输入如下命令将 NAS 上配置好的共享文件夹挂载到 Jellyfin 的相关目录：

```bash
mount.nfs -w 192.168.5.10:/volume1/Disk1 /data/docker/jellyfin/media/nas/disk1 -o nolock
mount.nfs -w 192.168.5.10:/volume2/Disk2 /data/docker/jellyfin/media/nas/disk2 -o nolock
mount.nfs -w 192.168.5.10:/volume3/Disk3 /data/docker/jellyfin/media/nas/disk3 -o nolock
mount.nfs -w 192.168.5.10:/volume4/Disk4 /data/docker/jellyfin/media/nas/disk4 -o nolock
```

为了保证每次启动软路由时能够自动挂载，请将上述内容添加至 `系统 > 启动项` 菜单下的 `本地启动脚本` 文本框的 `exit 0` 之前：

{{< figure src="/images/cn/2023-01-24-build-home-media-center-with-jellyfin-on-openwrt/startup-script.png" large-max-width="60%" middle-max-width="80%" >}}

# Jellyfin 部署

在 OpenWrt 上安装 Jellyfin 需要使用 Docker 进行部署。首先在 `Docker > 镜像` 菜单的 `拉取镜像` 处填写 `jellyfin/jellyfin:latest`，然后单击 `拉取`：

{{< figure src="/images/cn/2023-01-24-build-home-media-center-with-jellyfin-on-openwrt/docker-pull.png" large-max-width="60%" middle-max-width="80%" >}}

拉取完毕后即可在 `镜像概览` 处查看已下载的镜像：

![](/images/cn/2023-01-24-build-home-media-center-with-jellyfin-on-openwrt/docker-images.png)

进入软路由命令行，输入 `ls /dev/dri`，如果输出如下则表示 CPU 支持硬件加速：

```
card0       renderD128
```

为了确保在 Docker 中其他用户可以使用该设备，输入如下命令设置设备权限：

```bash
chmod 777 /dev/dri/*
```

通过 `Docker > 容器` 菜单，单击 `添加` 按钮添加容器。单击 `命令行` 并复制如下内容，单击 `提交` 解析命令行：

```
docker run -d \
 --name=jellyfin \
 --hostname=jellyfin \
 --pull=always \
 --privileged \
 --volume /data/docker/jellyfin/config:/config \
 --volume /data/docker/jellyfin/cache:/cache \
 --volume /data/docker/jellyfin/media:/media \
 --volume /data/fonts:/usr/local/share/fonts \
 --user 1000:1000 \
 --net=host \
 --restart=unless-stopped \
 --device /dev/dri/renderD128:/dev/dri/renderD128 \
 --device /dev/dri/card0:/dev/dri/card0 \
 jellyfin/jellyfin
```

相关参数说明如下：

| 参数                                             | 说明                               |
| :----------------------------------------------- | :--------------------------------- |
| --name=jellyfin                                  | 镜像名称                           |
| --hostname=jellyfin                              | 主机名称                           |
| --pull=always                                    | 运行前总是先拉取镜像               |
| --privileged                                     | 特权模式                           |
| --volume /data/docker/jellyfin/config:/config    | 配置文件目录                       |
| --volume /data/docker/jellyfin/cache:/cache      | 缓存文件目录                       |
| --volume /data/docker/jellyfin/media:/media      | 媒体文件目录                       |
| --volume /data/fonts:/usr/local/share/fonts      | 备用字体目录                       |
| --user 1000:1000                                 | 运行时用户和用户组                 |
| --net=host                                       | 网络类型：同宿主机相同网络         |
| --restart=unless-stopped                         | 重启策略：在容器退出时总是重启容器 |
| --device /dev/dri/renderD128:/dev/dri/renderD128 | 硬件加速设备                       |
| --device /dev/dri/card0:/dev/dri/card0           | 硬件加速设备                       |

如果 `总是先拉取镜像` 未成功自动勾选，可以手动勾选确保运行前拉取最新镜像。单击 `提交` 创建容器。创建完毕后容器列表即出现 Jellyfin 容器：

![](/images/cn/2023-01-24-build-home-media-center-with-jellyfin-on-openwrt/docker-container-created.png)

勾选 Jellyfin 容器，单击 `启动` 按钮启动容器：

![](/images/cn/2023-01-24-build-home-media-center-with-jellyfin-on-openwrt/docker-container-running.png)

# Jellyfin 配置

通过 `http://192.168.5.1:8096` 进入 Jellyfin，`首选显示语言` 选择 `汉语（简化字）`：

![](/images/cn/2023-01-24-build-home-media-center-with-jellyfin-on-openwrt/jellyfin-setup-language.png)

单击 `下一个`，根据个人情况设置 `用户名` 和 `密码`：

![](/images/cn/2023-01-24-build-home-media-center-with-jellyfin-on-openwrt/jellyfin-setup-username-password.png)

单击 `下一个`，设置媒体库：

![](/images/cn/2023-01-24-build-home-media-center-with-jellyfin-on-openwrt/jellyfin-setup-media-library.png)

单击 `+` 添加媒体库：

![](/images/cn/2023-01-24-build-home-media-center-with-jellyfin-on-openwrt/jellyfin-setup-media-library-movie.png)

根据实际情况进行配置：

1. 选择 `内容类型` 并填写 `显示名称`。
2. 在 `文件夹` 中添加所有包含当前类型媒体的文件夹。
3. `首选下载语言` 选择 `Chinese`。
4. `国家/地区` 选择 `People's Republic of China`。
5. 取消勾选 `元数据下载器` 和 `图片获取程序` 中所有选项。
6. 其他设置暂时保持默认。

单击 `下一个`，设置首选元数据语言：

![](/images/cn/2023-01-24-build-home-media-center-with-jellyfin-on-openwrt/jellyfin-setup-meta-language.png)

单击 `下一个`，设置远程访问：

![](/images/cn/2023-01-24-build-home-media-center-with-jellyfin-on-openwrt/jellyfin-setup-remote-access.png)

单击 `下一个`，完成设置：

![](/images/cn/2023-01-24-build-home-media-center-with-jellyfin-on-openwrt/jellyfin-setup-finish.png)

单击 `完成` 进入登录界面：

![](/images/cn/2023-01-24-build-home-media-center-with-jellyfin-on-openwrt/jellyfin-login.png)

进入系统后，单击左侧菜单按钮，选择 `管理 > 控制台` 菜单。进入 `控制台` 后，选择 `服务器 > 播放` 菜单。将 `转码` 中的 `硬件加速` 选择为 `Video Acceleration API (VAAPI)`，注意确认 `VA-API 设备` 是否为 `/dev/dri/renderD128`，并在 `启用硬件解码` 勾选所有媒体类型。注意确认 `硬件编码选项` 中的 `启用硬件编码` 选项已勾选。

![](/images/cn/2023-01-24-build-home-media-center-with-jellyfin-on-openwrt/jellyfin-hardware-acceleration.png)

{{% admonition type="tip" title="" %}}
根据[官方文档](https://jellyfin.org/docs/general/administration/hardware-acceleration/#intel-gen9-and-gen11-igpus)说明，针对部分 CPU（例如：N5105）需要勾选 `启用低电压模式的 Intel H.264 硬件编码器`以确保硬件加速正常工作。
{{% /admonition %}}

在 `服务器 > 播放` 菜单中，勾选 `启用备用字体`，将 `备用字体文件路径` 设置为 `/usr/local/share/fonts`。

# TMM 刮削

tinyMediaManager 是一个用 Java/Swing 编写的媒体管理工具，它可以为多种媒体服务器提供元数据。TMM 提供了多个平台的客户端，但为了多客户端刮削时数据共享，本例也使用 Docker 进行安装。

在软路由 `/data` 目录中创建用于 TMM 的目录：

```bash
mkdir /data/docker/tinymediamanager
mkdir /data/docker/tinymediamanager/config
mkdir /data/docker/tinymediamanager/media
mkdir /data/docker/tinymediamanager/media/nas
mkdir /data/docker/tinymediamanager/media/nas/disk1
mkdir /data/docker/tinymediamanager/media/nas/disk2
mkdir /data/docker/tinymediamanager/media/nas/disk3
mkdir /data/docker/tinymediamanager/media/nas/disk4
```

进入命令行，输入如下命令将 NAS 上配置好的共享文件夹挂载到 TMM 的相关目录：

```bash
mount.nfs -w 192.168.5.10:/volume1/Disk1 /data/docker/tinymediamanager/media/nas/disk1 -o nolock
mount.nfs -w 192.168.5.10:/volume2/Disk2 /data/docker/tinymediamanager/media/nas/disk2 -o nolock
mount.nfs -w 192.168.5.10:/volume3/Disk3 /data/docker/tinymediamanager/media/nas/disk3 -o nolock
mount.nfs -w 192.168.5.10:/volume4/Disk4 /data/docker/tinymediamanager/media/nas/disk4 -o nolock
```

为了保证每次启动软路由时能够自动挂载，请将上述内容添加至 `系统 > 启动项` 菜单下的 `本地启动脚本` 文本框的 `exit 0` 之前。

在 `Docker > 镜像` 菜单的 `拉取镜像` 处填写 `romancin/tinymediamanager:latest-v4`，然后单击 `拉取`。

通过 `Docker > 容器` 菜单，单击 `添加` 按钮添加容器。单击 `命令行` 并复制如下内容，单击 `提交` 解析命令行：

```
docker run -d \
 --name=tinymediamanager \
 --hostname=tinymediamanager \
 --pull=always \
 --privileged \
 --volume /data/docker/tinymediamanager/config:/config \
 --volume /data/docker/tinymediamanager/media:/media \
 --user root:root \
 --env ENABLE_CJK_FONT=1 \
 --publish 5800:5800 \
 --restart=unless-stopped \
 romancin/tinymediamanager:latest-v4
```

如果 `总是先拉取镜像` 未成功自动勾选，可以手动勾选确保运行前拉取最新镜像。单击 `提交` 创建容器。勾选 TMM 容器，单击 `启动` 按钮启动容器。

安装完毕后重启容器。通过 `http://192.168.5.1:5800` 进入 TMM：

![](/images/cn/2023-01-24-build-home-media-center-with-jellyfin-on-openwrt/tmm-init.png)

根据向导进行配置，设置中文界面后需要重启容器生效。

{{% admonition type="warning" title="" %}}
PT 用户注意，**不要**开启任何自动重命名，**不要**将 NFO 保存为与媒体文件相同的文件名，避免覆盖原始内容从而导致做种错误。
{{% /admonition %}}

根据个人喜好配置好 TMM 后即可对媒体文件进行刮削了，在此不再详细展开刮削过程。由于原始文件的命名可能导致自动获取的信息有误，因此建议对每一个媒体文件刮削结果进行人工复核。

{{% admonition type="tip" title="" %}}
Docker 版本 TMM 不支持输入中文，在通过 `Clipboard` 内外传输剪切板时中文也会出现乱码，且目前暂时无法修复。
{{% /admonition %}}

4.0 之后版本的 TMM 免费版不再支持自动下载字幕，由于 TMM 采用 [Open Subtitles](https://www.opensubtitles.org/)，对于有需要双语字幕和特效字幕的同学并不友好。建议还是自行手动下载字幕并放置在媒体文件中，在此提供几个不错的字幕下载网站：

- 伪射手：[https://assrt.net](https://assrt.net)
- SubHD：[https://subhd.tv/sub/new](https://subhd.tv/sub/new)
- 字幕组（需注册）：[https://www.yysub.net/subtitle](https://www.yysub.net/subtitle)

# 测试

经过 TMM 刮削后，Jellyfin 即可自动识别元数据，示例电影的详细信息如下如所示：

![](/images/cn/2023-01-24-build-home-media-center-with-jellyfin-on-openwrt/jellyfin-movie-info.png)

单击播放后，通过播放信息查看，已经可以使用 Jellyfin 实现转码在线播放：

![](/images/cn/2023-01-24-build-home-media-center-with-jellyfin-on-openwrt/jellyfin-movie-play.png)

测试完成后即可在各个终端安装相应的的客户端：

1. iPhone & iPad & Apple TV：建议使用 [Swiftfin](https://github.com/jellyfin/swiftfin)，官方应用，原生界面体验，[应用商店](https://apps.apple.com/zh/app/swiftfin/id1604098728)直接下载安装。
2. Android 手机：建议使用 [Findroid](https://github.com/jarnedemeulemeester/findroid)，第三方应用，原生界面体验，[应用商店](https://play.google.com/store/apps/details?id=dev.jdtech.jellyfin)直接下载安装，非原生 Android 系统可以在 [Github 页面](https://github.com/jarnedemeulemeester/findroid/releases)下载离线 apk 文件安装。
3. Android TV：建议使用 [Jellyfin for Android TV](https://github.com/jellyfin/jellyfin-androidtv)，官方应用，[应用商店](https://play.google.com/store/apps/details?id=org.jellyfin.androidtv)直接下载安装，非原生 Android 系统可以在 [Github 页面](https://github.com/jellyfin/jellyfin-androidtv/releases)下载离线 apk 文件安装。

可以在[官方客页面](https://jellyfin.org/downloads/clients/all/)探索更多官方和第三方客户端。在电视盒子等仅用于播放视频的设备上，可以尝试启用 [Direct Play](https://jellyfin.org/docs/general/server/transcoding#types-of-transcoding)，当然也需要根据电视盒子的特性进行调整，避免部分格式的视频和音频无法正常解析。
