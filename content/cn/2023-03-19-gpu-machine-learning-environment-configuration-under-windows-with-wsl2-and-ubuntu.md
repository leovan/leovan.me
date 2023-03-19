---
title: 在 Windows 下利用 WSL2 和 Ubuntu 配置 GPU 机器学习环境 (GPU Machine Leanring Environment Configuration under Windows with WSL2 and Ubuntu)
author: 范叶亮
date: '2023-03-19'
slug: gpu-machine-learning-environment-configuration-under-windows-with-wsl2-and-ubuntu
categories:
  - Tech101
  - 编程
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

> 本文主要面向希望在游戏空闲时段将显卡用于科学事业的朋友们😎。

> 本文以 Windows 11 22H2 版本为例，不确保在其他版本系统下完全适用。

## 终端

工欲善其事必先利其器，开发离不开那个黑框框，所以我们需要把这个黑框框变得更好看更好用些。Windows 终端是一个新的支持 PowerShell 和 WSL bash 的应用，通过[应用商店](https://aka.ms/terminal) 直接进行安装。

建议安装最新版的 PowerShell 作为命令行环境，相关下载和配置详见[官网](https://learn.microsoft.com/zh-cn/powershell/)。

为了更好的在终端中显示中英文和图标，推荐使用 [Sarasa Term SC Nerd](https://github.com/laishulu/Sarasa-Term-SC-Nerd) 作为终端显示字体。

## WSL

以管理员模式打开 PowerShell 或 Windows 命令提示符，输入如下命令，并重启计算机：

```powershell
wsl --install
```

此命令会启用 WSL 并安装 Ubuntu 发行版 Linux。通过 `wsl -l -o` 可以查看所有 Linux 的发行版：

![](/images/cn/2023-03-19-gpu-machine-learning-environment-configuration-under-windows-with-wsl2-and-ubuntu/wsl-linux-distributions.png)

通过 `wsl --install <发行版名称>` 可以安装其他发行版 Linux。通过 `wsl -l -v` 可以查看当前运行的 WSL 版本：

![](/images/cn/2023-03-19-gpu-machine-learning-environment-configuration-under-windows-with-wsl2-and-ubuntu/wsl-running.png)

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
sudo sh cuda_11.8.0_520.61.05_linux.run --toolkit
```

其中 `--toolkit` 表示仅安装 CUDA 工具箱。

![](/images/cn/2023-03-19-gpu-machine-learning-environment-configuration-under-windows-with-wsl2-and-ubuntu/cuda-installation-eula.png)

在弹出的 EULA 界面输入 `accept` 进入安装选项界面：

![](/images/cn/2023-03-19-gpu-machine-learning-environment-configuration-under-windows-with-wsl2-and-ubuntu/cuda-installation-options.png)

仅保留 `CUDA Toolkit 11.8` 即可，切换到 `Install` 并按回车键进行安装。

将如下内容添加到 `~/.bashrc` 文件尾部：

```shell
export PATH=/usr/local/cuda/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
```

通过 `source ~/.bashrc` 或 `source ~/.zshrc` 使路径立即生效。输入 `nvcc -V` 查看 CUDA 编译器驱动版本：

![](/images/cn/2023-03-19-gpu-machine-learning-environment-configuration-under-windows-with-wsl2-and-ubuntu/nvcc-version.png)

### cuDNN

从 Nvidia 官网（<https://developer.nvidia.com/rdp/cudnn-archive>）下载适用于 Linux 和上述安装 CUDA 版本的 cuDNN，在此选择的版本为 `v8.8.0 for CUDA 11.x`，安装包格式为 `Local Installer for Linux x86_64 (Tar)`。

> 注意：cuDNN 需要注册账户后方可进行下载。

下载完毕后运行如下命令进行解压：

```shell
tar -xvf cudnn-linux-x86_64-8.8.0.121_cuda11-archive.tar.xz
```

运行如下命令将其移动到 CUDA 目录：

```
sudo mv cudnn-*-archive/include/cudnn*.h /usr/local/cuda/include
sudo mv -P cudnn-*-archive/lib/libcudnn* /usr/local/cuda/lib64 
sudo chmod a+r /usr/local/cuda/include/cudnn*.h /usr/local/cuda/lib64/libcudnn*
```

## 机器学习环境

### Python

Ubuntu 22.04 系统已经安装了 Python 3.10 版本，Python 3.10 在常用机器学习库上具有较好的兼容性。因此，以 Python 3.10 版本为例，使用 `venv` 创建机器学习虚拟环境。在系统层面安装 `venv` 并创建虚拟环境：

```shell
sudo apt install python3.10-venv
mkdir ~/sdk
python3.10 -m venv ~/sdk/python310
source ~/sdk/python310/bin/activate
```

### PyTorch

PyTorch 的 2.0 版本支持的最高 CUDA 即为 11.8，输入如下命令安装 PyTorch：

```shell
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

惊奇的发现 PyTorch 的安装包 `torch-2.0.0+cu118-cp310-cp310-linux_x86_64.whl` 竟然超过 2GB。安装完毕后发现 PyTorch 内嵌了 CUDA 和 cuDNN。内嵌的好处是可以做到安装即用，但如果和其他包依赖的系统 CUDA 和 cuDNN 版本不一致，容易出现各种意想不到的问题。在 Python 中运行如下命令验证 PyTorch 是否可以正常调用显卡：

```python
import torch

# PyTorch 版本
torch.__version__
# 2.0.0+cu118

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

输入如下命令安装 Tensorflow：

```shell
pip install tensorflow
```

在 Python 中运行如下命令验证 Tensorflow 是否可以正常调用显卡：

```python
import tensorflow as tf

# Tensorflow 版本
tf.__version__
# 2.11.0

# CUDA 是否可用
tf.test.is_gpu_available()
# True

# GPU 数量
len(tf.config.experimental.list_physical_devices('GPU'))
# 1

# GPU 名称
tf.test.gpu_device_name()
# /device:GPU:0
```
