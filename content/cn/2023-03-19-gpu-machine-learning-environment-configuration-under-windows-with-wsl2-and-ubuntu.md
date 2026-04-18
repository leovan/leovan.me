---
title: 在 Windows 下利用 WSL2 和 Ubuntu 配置 GPU 机器学习环境
author: 范叶亮
date: 2023-03-19
slug: gpu-machine-learning-environment-configuration-under-windows-with-wsl2-and-ubuntu
categories:
  - 教程
tags:
  - GPU
  - WSL
  - WSL2
  - Ubuntu
  - 机器学习
  - 深度学习
  - CUDA
  - cuDNN
  - PyTorch
  - Tensorflow
---

> 本文主要面向希望在游戏空闲时段将显卡用于科学事业的朋友们 😎。

> 更新于 2024-05-19

## 终端

工欲善其事必先利其器，开发离不开那个黑框框，所以我们需要把这个黑框框变得更好看更好用些。Windows 终端是一个新的支持 PowerShell 和 WSL bash 的应用，通过[应用商店](https://aka.ms/terminal) 直接进行安装。

建议安装最新版的 PowerShell 作为命令行环境，相关下载和配置详见[官网](https://learn.microsoft.com/zh-cn/powershell/)。

为了更好的在终端中显示中英文和图标，推荐使用 [Sarasa Term SC Nerd](https://github.com/laishulu/Sarasa-Term-SC-Nerd) 作为终端显示字体。

## 网络

为了方便使用，网络设置采用桥接模式。桥接模式需要在 Windows 中启用 Hyper-V（仅 Windows 专业版支持）。通过启用或关闭 Windows 功能开启 Hyper-V，然后重启电脑生效。

![](/images/cn/2023-03-19-gpu-machine-learning-environment-configuration-under-windows-with-wsl2-and-ubuntu/hyper-v.png)

在 Hyper-V 中创建一个新的交换机，在连接类型中选择外部网络，并根据电脑的网络连接情况选择对应的桥接网卡。

![](/images/cn/2023-03-19-gpu-machine-learning-environment-configuration-under-windows-with-wsl2-and-ubuntu/hyper-v-switch.png)

通过 `Get-VMSwitch -SwitchType External` 可以查看创建的交换机：

```plain
Name SwitchType NetAdapterInterfaceDescription
---- ---------- ------------------------------
WSL  External   Realtek Gaming 2.5GbE Family Controller
```

在 Home 目录创建 `.wslconfig` 文件，并添加如下内容：

```ini
[wsl2]
networkingMode=bridged
vmSwitch=WSL
ipv6=true
```

其中，`vmSwitch` 填写创建的交换机的名称。

## WSL

以管理员模式打开 PowerShell 或 Windows 命令提示符，输入如下命令，并重启计算机：

```powershell
wsl --install
```

此命令会启用 WSL 并安装 Ubuntu 发行版 Linux。通过 `wsl -l -o` 可以查看所有 Linux 的发行版：

```plain
以下是可安装的有效分发的列表。
请使用“wsl --install -d <分发>”安装。

NAME                                   FRIENDLY NAME
Ubuntu                                 Ubuntu
Debian                                 Debian GNU/Linux
kali-linux                             Kali Linux Rolling
Ubuntu-18.04                           Ubuntu 18.04 LTS
Ubuntu-20.04                           Ubuntu 20.04 LTS
Ubuntu-22.04                           Ubuntu 22.04 LTS
Ubuntu-24.04                           Ubuntu 24.04 LTS
OracleLinux_7_9                        Oracle Linux 7.9
OracleLinux_8_7                        Oracle Linux 8.7
OracleLinux_9_1                        Oracle Linux 9.1
openSUSE-Leap-15.5                     openSUSE Leap 15.5
SUSE-Linux-Enterprise-Server-15-SP4    SUSE Linux Enterprise Server 15 SP4
SUSE-Linux-Enterprise-15-SP5           SUSE Linux Enterprise 15 SP5
openSUSE-Tumbleweed                    openSUSE Tumbleweed
```

通过 `wsl --install -d <发行版名称>` 可以安装其他发行版 Linux，本文以 Ubuntu 22.04 为例。通过 `wsl -l -v` 可以查看当前运行的 WSL 版本：

```plain
  NAME                   STATE           VERSION
* Ubuntu-22.04           Running         2
```

通过 `wsl` 新安装的 Linux 默认已经设置为 WSL 2。

进入 Ubuntu 命令行，输入如下命令安装必要的系统依赖：

```shell
sudo apt install gcc
```

安装 zsh 作为 Ubuntu 默认的 Shell：

```shell
sudo apt install zsh
```

安装 [Oh My Zsh](https://ohmyz.sh/) 来提升 zsh 的易用性。

## 显卡

### 驱动

从 Nvidia 官网（<https://www.nvidia.cn/geforce/drivers>）下载适用于 Windows 的最新驱动并安装。进入 Windows 命令行，输入 `nvidia-smi` 命令查看显卡状态：

![](/images/cn/2023-03-19-gpu-machine-learning-environment-configuration-under-windows-with-wsl2-and-ubuntu/nvidia-smi-windows.png)

Ubuntu 中不再需要额外安装显卡驱动，进入 Ubuntu 命令行，输入 `nvidia-smi` 命令查看显卡状态：

![](/images/cn/2023-03-19-gpu-machine-learning-environment-configuration-under-windows-with-wsl2-and-ubuntu/nvidia-smi-ubuntu.png)

不难看出，出了 `nvidia-smi` 工具版本不同外，显卡驱动和 CUDA 版本均是相同的。

### CUDA

从 Nvidia 官网（<https://developer.nvidia.com/cuda-toolkit-archive>）下载适用于 WSL Ubuntu 的 CUDA，在此选择的版本为 `11.8.0`（具体请参考例如 Tensorflow 等所需工具的依赖版本），相关平台选项如下：

- Operating System：Linux
- Architecture：x86_64
- Distribution：WSL-Ubuntu
- Version：2.0
- Installer Type：runfile (local)

下载完毕后运行如下命令进行安装：

```shell
chmod +x cuda_11.8.0_520.61.05_linux.run
sudo ./cuda_11.8.0_520.61.05_linux.run --toolkit
```

其中 `--toolkit` 表示仅安装 CUDA 工具箱。

![](/images/cn/2023-03-19-gpu-machine-learning-environment-configuration-under-windows-with-wsl2-and-ubuntu/cuda-installation-eula.png)

在弹出的 EULA 界面输入 `accept` 进入安装选项界面：

![](/images/cn/2023-03-19-gpu-machine-learning-environment-configuration-under-windows-with-wsl2-and-ubuntu/cuda-installation-options.png)

仅保留 `CUDA Toolkit 11.8` 即可，切换到 `Install` 并按回车键进行安装。

将如下内容添加到 `~/.bashrc` 文件尾部：

```shell
export PATH=/usr/local/cuda/bin:$PATH
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda/lib64:/usr/local/cuda/extras/CUPTI/lib64
```

通过 `source ~/.bashrc` 或 `source ~/.zshrc` 使路径立即生效。输入 `nvcc -V` 查看 CUDA 编译器驱动版本：

![](/images/cn/2023-03-19-gpu-machine-learning-environment-configuration-under-windows-with-wsl2-and-ubuntu/nvcc-version.png)

### cuDNN

从 Nvidia 官网（<https://developer.nvidia.com/rdp/cudnn-archive>）下载适用于 Linux 和上述安装 CUDA 版本的 cuDNN，在此选择的版本为 `v8.8.0 for CUDA 11.x`，安装包格式为 `Local Installer for Linux x86_64 (Tar)`。

> 注意：cuDNN 需要注册账户后方可进行下载。

下载完毕后运行如下命令进行解压：

```shell
tar -xvf cudnn-linux-x86_64-8.9.7.29_cuda11-archive.tar.xz
```

运行如下命令将其移动到 CUDA 目录：

```
sudo mv cudnn-*-archive/include/cudnn*.h /usr/local/cuda/include
sudo mv cudnn-*-archive/lib/libcudnn* /usr/local/cuda/lib64
sudo chmod a+r /usr/local/cuda/include/cudnn*.h /usr/local/cuda/lib64/libcudnn*
```

## 机器学习环境

### Python

Ubuntu 22.04 系统已经安装了 Python 3.10 版本，Python 3.10 在常用机器学习库上具有较好的兼容性。因此，以 Python 3.10 版本为例，使用 `venv` 创建机器学习虚拟环境。在系统层面安装 `venv` 并创建虚拟环境：

```shell
sudo apt install python3-venv
mkdir ~/SDK
python3.10 -m venv ~/SDK/python310
source ~/SDK/python310/bin/activate
```

### PyTorch

输入如下命令安装 PyTorch：

```shell
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

安装完毕后发现 PyTorch 内嵌了 CUDA 和 cuDNN。内嵌的好处是可以做到安装即用，但如果和其他包依赖的系统 CUDA 和 cuDNN 版本不一致，容易出现各种意想不到的问题。在 Python 中运行如下命令验证 PyTorch 是否可以正常调用显卡：

```python
import torch

# PyTorch 版本
torch.__version__
# 2.3.0+cu118

# CUDA 是否可用
torch.cuda.is_available()
# True

# GPU 数量
torch.cuda.device_count()
# 1

# GPU 名称
torch.cuda.get_device_name(0)
# NVIDIA GeForce RTX 3070 Ti
```

### Tensorflow

输入如下命令安装 Tensorflow（2.14.1 版本支持 CUDA 11.8）：

```shell
pip install tensorflow==2.14.1
```

在 Python 中运行如下命令验证 Tensorflow 是否可以正常调用显卡：

```python
import tensorflow as tf

# Tensorflow 版本
tf.__version__
# 2.15.1

# GPU 设备
tf.config.list_physical_devices('GPU')
# [PhysicalDevice(name='/physical_device:GPU:0', device_type='GPU')]

# GPU 名称
tf.test.gpu_device_name()
# /device:GPU:0
```

### PyCharm

配置 PyCharm 使用 WSL 中的 Python 请参见 [Configure an interpreter using WSL](https://www.jetbrains.com/help/pycharm/using-wsl-as-a-remote-interpreter.html)。
