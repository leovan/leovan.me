---
title: 虚拟环境准备 (Virtual Environment Preparation)
author: 范叶亮
date: '2021-06-12'
slug: virtual-env-preparation
categories:
  - Tech101
  - 编程
tags:
  - 虚拟环境
  - VirtualBox
  - Ubuntu
  - Ubuntu Server
  - 虚拟机
  - 固定 IP
  - Host-only Adapter
  - NAT
  - Bridged
  - 免密
  - 免密码
  - 免密登录
  - OpenSSH
  - SSH
images:
  - /images/tech101/2021-06-12-virtual-env-preparation/install-virtualbox.png
  - /images/tech101/2021-06-12-virtual-env-preparation/install-virtualbox-extension-pack.png
  - /images/tech101/2021-06-12-virtual-env-preparation/virtualbox-add-host-only-network.png
  - /images/tech101/2021-06-12-virtual-env-preparation/virtualbox-new-virtual-machine-1.png
  - /images/tech101/2021-06-12-virtual-env-preparation/virtualbox-new-virtual-machine-2.png
  - /images/tech101/2021-06-12-virtual-env-preparation/virtualbox-settings-system-motherboard.png
  - /images/tech101/2021-06-12-virtual-env-preparation/virtualbox-settings-system-processor.png
  - /images/tech101/2021-06-12-virtual-env-preparation/virtualbox-settings-display-acceleration.png
  - /images/tech101/2021-06-12-virtual-env-preparation/virtualbox-settings-network-adapter-1.png
  - /images/tech101/2021-06-12-virtual-env-preparation/virtualbox-settings-network-adapter-2.png
  - /images/tech101/2021-06-12-virtual-env-preparation/virtualbox-settings-storage.png
  - /images/tech101/2021-06-12-virtual-env-preparation/virtualbox-settings-storage-add-disk.png
  - /images/tech101/2021-06-12-virtual-env-preparation/install-ubuntu-language.png
  - /images/tech101/2021-06-12-virtual-env-preparation/install-ubuntu-keyboard.png
  - /images/tech101/2021-06-12-virtual-env-preparation/install-ubuntu-network-before.png
  - /images/tech101/2021-06-12-virtual-env-preparation/install-ubuntu-network-manual.png
  - /images/tech101/2021-06-12-virtual-env-preparation/install-ubuntu-network-after.png
  - /images/tech101/2021-06-12-virtual-env-preparation/install-ubuntu-archive-mirror.png
  - /images/tech101/2021-06-12-virtual-env-preparation/install-ubuntu-storage-1.png
  - /images/tech101/2021-06-12-virtual-env-preparation/install-ubuntu-storage-2.png
  - /images/tech101/2021-06-12-virtual-env-preparation/install-ubuntu-profile.png
  - /images/tech101/2021-06-12-virtual-env-preparation/install-ubuntu-ssh.png
  - /images/tech101/2021-06-12-virtual-env-preparation/install-ubuntu-snaps.png
  - /images/tech101/2021-06-12-virtual-env-preparation/install-ubuntu-complete.png
  - /images/tech101/2021-06-12-virtual-env-preparation/ubuntu-login.png
  - /images/tech101/2021-06-12-virtual-env-preparation/clone-virtual-machine-1.png
  - /images/tech101/2021-06-12-virtual-env-preparation/clone-virtual-machine-2.png
---

本文以 VirtualBox 和 Ubuntu Server 为例，介绍在 macOS 下搭建 3 台虚拟机集群过程。

## 安装 VirtualBox

从[官网](https://www.virtualbox.org/wiki/Downloads)下载最新版本的 VirtualBox 和 VirtualBox Extension Pack，本文以 6.1.22 版本为例。根据安装向导安装 VirtualBox。

![](/images/tech101/2021-06-12-virtual-env-preparation/install-virtualbox.png)

双击下载好的 `.vbox-extpack` 安装文件安装 VirtualBox Extension Pack。

![](/images/tech101/2021-06-12-virtual-env-preparation/install-virtualbox-extension-pack.png)

通过 `File -> Host Network Manager...` 为 VirtualBox 添加一块网卡。

![](/images/tech101/2021-06-12-virtual-env-preparation/virtualbox-add-host-only-network.png)

## 安装 Ubuntu Server

### 虚拟机配置

从[官网](https://ubuntu.com/download/server)下载最新版本的 Ubuntu Server，本文以 20.04.2 LTS 版本为例。在 VirtualBox 通过 `New` 按钮添加新的虚拟机，首先为虚拟机配置名称，存储路径和内存大小等基本信息：

![](/images/tech101/2021-06-12-virtual-env-preparation/virtualbox-new-virtual-machine-1.png)

单击 `Create` 后为虚拟机配置磁盘类型和大小：

![](/images/tech101/2021-06-12-virtual-env-preparation/virtualbox-new-virtual-machine-2.png)

单击 `Create` 完成创建。创建完毕后，在左侧列表中选择创建好的虚拟机，通过 `Settings` 按钮打开设置对话框，在 `System - Motherboard` 标签页去除掉软盘启动 `Boot Order - Floppy`，同时也可以再次调整内存大小：

![](/images/tech101/2021-06-12-virtual-env-preparation/virtualbox-settings-system-motherboard.png)

在 `System - Processor` 标签页可以调整虚拟机使用 CPU 的数量：

![](/images/tech101/2021-06-12-virtual-env-preparation/virtualbox-settings-system-processor.png)

在 `Display - Acceleration` 标签页可以调整使用的现存大小：

![](/images/tech101/2021-06-12-virtual-env-preparation/virtualbox-settings-display-acceleration.png)

在 `Network - Adapter 1` 标签页选择 `NAT` 网络类型，该网卡用于虚拟机连接外部网络：

![](/images/tech101/2021-06-12-virtual-env-preparation/virtualbox-settings-network-adapter-1.png)

在 `Network - Adapter 2` 标签页选择 `Host-only Adapter` 网络类型，名称选择上文 VirtualBox 配置的 `vboxnet0`，该网卡用于虚拟机连接内部网络：

![](/images/tech101/2021-06-12-virtual-env-preparation/virtualbox-settings-network-adapter-2.png)

在 `Network - Adapter 2` 标签页为光驱选择挂载的磁盘镜像：

![](/images/tech101/2021-06-12-virtual-env-preparation/virtualbox-settings-storage.png)

添加下载好的 Ubuntu Server ISO 磁盘镜像：

![](/images/tech101/2021-06-12-virtual-env-preparation/virtualbox-settings-storage-add-disk.png)

### Ubuntu Server 安装配置

单击 `Start` 按钮启动虚拟机，启动后等待片刻，在语言选择页面选择 `English`：

![](/images/tech101/2021-06-12-virtual-env-preparation/install-ubuntu-language.png)

在键盘布局页面采用默认配置，`Done` 进入下一步：

![](/images/tech101/2021-06-12-virtual-env-preparation/install-ubuntu-keyboard.png)

在网络配置页面，上文中配置了两块网卡，在此我们需要对于 Host-only Adapter 网卡 `enp0s8` 进行配置，NAT 网卡 `enp0s3` 采用默认即可：

![](/images/tech101/2021-06-12-virtual-env-preparation/install-ubuntu-network-before.png)

进入配置后选择手动 `Nanual`，在 Subnet 中输入 `192.168.56.0/24`（参考上文中 VirtualBox 添加的网卡设置），在 Address 中输入 `192.168.56.1`，在 Gateway 中输入 `192.168.56.1`，`Save` 进行保存：

![](/images/tech101/2021-06-12-virtual-env-preparation/install-ubuntu-network-manual.png)

配置完后，结果如下，`Done` 进入下一步：

![](/images/tech101/2021-06-12-virtual-env-preparation/install-ubuntu-network-after.png)

在镜像配置页面，根据实际情况选择一个合适的镜像地址，本文采用清华大学的镜像地址 `https://mirrors.tuna.tsinghua.edu.cn/ubuntu/`，`Done` 进入下一步：

![](/images/tech101/2021-06-12-virtual-env-preparation/install-ubuntu-archive-mirror.png)

在存储配置页面，为了方便起见选择使用整个磁盘，`Done` 进入下一步：

![](/images/tech101/2021-06-12-virtual-env-preparation/install-ubuntu-storage-1.png)

确认磁盘配置信息，`Done` 进入下一步：

![](/images/tech101/2021-06-12-virtual-env-preparation/install-ubuntu-storage-2.png)

在用户信息配置页面，输入用户名和密码等信息，`Done` 进入下一步：

![](/images/tech101/2021-06-12-virtual-env-preparation/install-ubuntu-profile.png)

在 SSH 配置页面，选择安装 OpenSSH server，`Done` 进入下一步：

![](/images/tech101/2021-06-12-virtual-env-preparation/install-ubuntu-ssh.png)

在软件包配置页面，跳过安装，`Done` 进入下一步：

![](/images/tech101/2021-06-12-virtual-env-preparation/install-ubuntu-snaps.png)

安装完毕后，`Reboot Now` 重启虚拟机：

![](/images/tech101/2021-06-12-virtual-env-preparation/install-ubuntu-complete.png)

## 配置 Ubuntu Server

### 克隆虚拟机

重启后，输入用户名和密码即可进入系统：

![](/images/tech101/2021-06-12-virtual-env-preparation/ubuntu-login.png)

通过如下命令更新系统软件到最新版本：

```shell
sudo apt update
sudo apt upgrade
sudo apt autoremove
```

输入以下命令进行关机：

```shell
sudo shutdown now
```

右键单击虚拟机 Ubuntu Server 1，选择 `Clone` 对虚拟机进行克隆，选择为所有网卡重新生成 MAC 地址，然后单击 `Continue`：

![](/images/tech101/2021-06-12-virtual-env-preparation/clone-virtual-machine-1.png)

选择 `Full clone` 模式，单击 `Continue` 完成克隆：

![](/images/tech101/2021-06-12-virtual-env-preparation/clone-virtual-machine-2.png)

### 配置网络

分别进入虚拟机 2 和 3，修改固定 IP 地址为 `191.168.56.102` 和 `191.168.56.103`。

```shell
sudo vi /etc/netplan/00-installer-config.yaml
```

```yaml
# This is the network config written by 'subiquity'
network:
  ethernets:
    enp0s3:
      dhcp4:true
    enp0s8:
      addresses:
      - 192.168.56.101/24
      gateway4: 192.168.56.1
      nameservers:
        addresses: []
        search: []
  version: 2
```

将配置文件中 `00-installer-config.yaml` 的 `192.168.56.101` 修改为对应的 IP。然后执行：

```shell
sudo netplan apply
```

让配置生效。

为三台虚拟机修改主机名为 `vm-01`，`vm-02` 和 `vm-03`：

```shell
sudo hostnamectl set-hostname vm-0x
```

为三台虚拟机设置 IP 和主机名映射：

```shell
sudo vi /etc/hosts
```

在结尾添加：

```txt
# VM
192.168.56.101 vm-01
192.168.56.102 vm-02
192.168.56.103 vm-03
```

### 配置 SSH

分别进入三台虚拟机并生成密钥：

```shell
ssh-keygen -t rsa
```

这会在 `~/.ssh` 目录生成一对密钥，其中 `id_rsa` 是私钥，`id_rsa.pub` 是公钥。

将三台机器中的 `id_rsa.pub` 导出合并到 `~/.ssh/authorized_keys` 文件中，为了方便可以将自己电脑的 `id_rsa.pub` 也合并到其中实现免密登录。

登录任意每台虚拟机，通过如下命令测试是否可以免密登录：

```shell
ssh vm-01
ssh vm-02
ssh vm-03
```
