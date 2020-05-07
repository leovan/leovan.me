---
title: 在群晖 NAS 上编译安装 tmux
author: 范叶亮
date: '2020-05-07'
slug: compile-and-install-tmux-on-synology-nas
categories:
  - 编程
tags:
  - 群晖
  - Synology
  - NAS
  - tmux
  - 编译
  - 构建
images:
  - /images/cn/2020-05-07-compile-and-install-tmux-on-synology-nas/tmux-installed.png
---

## 工具链安装

登录 NAS 控制台，在系统根目录创建 `toolkit` 目录：

```shell
sudo mkdir /toolkit
sudo chown -R username:users /toolkit
```

其中 `username` 为使用的用户名，如果后续使用过程中出现磁盘空间不足的问题，可以在其他具有较大容量的分区建立 `toolkit`，再在根目录建立软链进行使用：

```shell
mkdir /xxx/toolkit
sudo ln -s /xxx/toolkit /toolkit
sudo chown -R username:users /toolkit
```

之后下载相关工具脚本：

```shell
cd /toolkit
git clone https://github.com/SynologyOpenSource/pkgscripts-ng.git
```

工具脚本使用 Python 3 实现，请确保 NAS 已经安装 Python 3，后续使用过程中如果提示相关 Python 扩展包未安装的情况请自行安装后重试。实验的 Synology NAS 为 DS418play，系统版本为 **DSM 6.2.2** 系统，处理器为 INTEL Celeron J3355 处理器（产品代号：**Apollo Lake**），首先利用 `EnvDeploy` 下载所需的编译环境：

```shell
cd /toolkit/pkgscripts-ng
sudo ./EnvDeploy -v 6.2 -p apollolake
```

请根据自己机器的系统版本和处理器类型自行调整 `-v` 和 `-p` 参数。如果下载速度较慢可以手动从 https://sourceforge.net/projects/dsgpl/files/toolkit/DSM6.2/ 下载下列文件：

```
base_env-6.2.txz
ds.apollolake-6.2.dev.txz
ds.apollolake-6.2.env.txz
```

将其放置到 `/toolkit/toolkit_tarballs` 目录中，然后通过如下命令进行部署安装：

```shell
sudo ./EnvDeploy -v 6.2 -p apollolake -t /toolkit/toolkit_tarballs
```

## 编译 tmux

在 `/toolkit` 目录下建立 `source` 文件夹，并将 tmux 源代码（本文以 3.1b 版本为例）下载到该文件夹中：

```shell
cd /toolkit
mkdir source
cd source
wget https://github.com/tmux/tmux/releases/download/3.1b/tmux-3.1b.tar.gz
tar -zxvf tmux-3.1b.tar.gz
mv tmux-3.1b tmux
```

在 tmux 源代码根目录中建立 `SynoBuildConf` 文件夹，并在文件夹中创建如下文件：

```shell
cd /toolkit/source/tmux
mkdir SynoBuildConf
```

`build`

```bash
#!/bin/bash

case ${MakeClean} in
	[Yy][Ee][Ss])
		make distclean
		;;
esac

NCURSES_INCS="$(pkg-config ncurses --cflags)"
NCURSES_LIBS="$(pkg-config ncurses --libs)"

CFLAGS="${CFLAGS} ${NCURSES_INCS}"
LDFLAGS="${LDFLAGS} ${NCURSES_LIBS}"

env CC="${CC}" AR="${AR}" CFLAGS="${CFLAGS}" LDFLAGS="${LDFLAGS}" \
./configure ${ConfigOpt}

make ${MAKE_FLAGS}
```

`depends`

```bash
[default]
all="6.2"
```

`install`

```bash
#!/bin/bash

PKG_NAME="tmux"
TGZ_DIR="/tmp/_${PKG_NAME}_tgz"
PKG_DIR="/tmp/_${PKG_NAME}_pkg"
PKG_DEST="/image/packages"

source /pkgscripts-ng/include/pkg_util.sh

create_package_tgz() {
	### clear destination directory
	for dir in $TGZ_DIR $PKG_DIR; do
		rm -rf "$dir"
	done
	for dir in $TGZ_DIR $PKG_DIR; do
		mkdir -p "$dir"
	done

	### install needed file into TGZ_DIR
	DESTDIR="${TGZ_DIR}" make install

	### create package.tgz
	pkg_make_package $TGZ_DIR $PKG_DIR
}

create_package_spk(){
	### Copy package center scripts to PKG_DIR
	cp -r synology/scripts/ $PKG_DIR

	### Copy package icon
	cp -av synology/PACKAGE_ICON*.PNG $PKG_DIR

	### Generate INFO file
	synology/INFO.sh > INFO
	cp INFO $PKG_DIR

	### Create the final spk.
	mkdir -p $PKG_DEST
	pkg_make_spk $PKG_DIR $PKG_DEST
}

main() {
	create_package_tgz
	create_package_spk
}

main "$@"
```

在 tmux 源代码根目录中建立 `synology` 文件夹，并在文件夹中创建如下文件：

```shell
cd /toolkit/source/tmux
mkdir synology
```

`INFO.sh`

```bash
#!/bin/sh

. /pkgscripts-ng/include/pkg_util.sh

package="tmux"
version="3.1b"
displayname="tmux"
arch="$(pkg_get_platform) "
maintainer="Leo Van"
maintainer_url="https://leovan.me"
distributor="Leo Van"
distributor_url="https://leovan.me"
description="tmux is a terminal multiplexer: it enables a number of terminals to be created, accessed, and controlled from a single screen. tmux may be detached from a screen and continue running in the background, then later reattached."
support_url="https://github.com/tmux/tmux"
thirdparty="yes"
startable="no"
silent_install="yes"
silent_upgrade="yes"
silent_uninstall="yes"

[ "$(caller)" != "0 NULL" ] && return 0

pkg_dump_info
```

并为其添加运行权限：

```shell
cd /toolkit/source/tmux/scripts
chmod u+x INFO.sh
```

下载 tmux 图标并将其重命名：

```shell
cd /toolkit/source/tmux/synology
wget https://raw.githubusercontent.com/tmux/tmux/master/logo/tmux-logo-huge.png
convert tmux-logo-huge.png -crop 480x480+0+0 -resize 72x PACKAGE_ICON.PNG
convert tmux-logo-huge.png -crop 480x480+0+0 -resize 256x PACKAGE_ICON_256.PNG
```

此处需要使用 [ImageMagick](https://www.imagemagick.org/) 对图标进行裁剪和缩放，请自行安装，或在本地对图片进行处理后上传到指定目录。在 `/toolkit/source/tmux/synology` 目录中建立 `scripts` 文件夹，并在文件夹中创建如下文件：

```shell
cd /toolkit/source/tmux/synology
mkdir scripts
```

`postinst`

```bash
#!/bin/sh

ln -sf "$SYNOPKG_PKGDEST/usr/local/bin/tmux" /usr/bin/
```

`postuninst`

```bash
#!/bin/sh

rm -f /usr/local/bin/tmux
rm -f /usr/bin/tmux
```

`postupgrade`

```bash
#!/bin/sh

exit 0
```

`preinst`

```bash
#!/bin/sh

exit 0
```

`preuninst`

```bash
#!/bin/sh

exit 0
```

`preupgrade`

```bash
#!/bin/sh

exit 0
```

`start-stop-status`

```bash
#!/bin/sh

case $1 in
	start)
		exit 0
	;;
	stop)
		exit 0
	;;
	status)
		if [ -h "/usr/bin/tmux" ]; then
			exit 0
		else
			exit 1
		fi
	;;
	killall)
        ;;
	log)
		exit 0
	;;
esac
```

为所有文件添加运行权限：

```shell
cd /toolkit/source/tmux/synology/scripts
chmod u+x *
```

利用 `PkgCreate.py` 构建 `tmux` 扩展包：

```shell
sudo ./PkgCreate.py -v 6.2 -p apollolake tmux
```

最终构建完毕的扩展包位于 `/toolkit/build_env/ds.apollolake-6.2/image/packages` 中。

## 安装 tmux

在 `/toolkit/build_env/ds.apollolake-6.2/image/packages` 目录中有两个编译好的扩展包，分别是 `tmux-apollolake-3.1b_debug.spk` 和 `tmux-apollolake-3.1b.spk`。其中 `tmux-apollolake-3.1b.spk` 为 Release 版本，传输到本地，通过 NAS 的套件中心手动安装即可。安装完毕后，套件中心的“已安装”会出现 tmux，如下图所示：

![](/images/cn/2020-05-07-compile-and-install-tmux-on-synology-nas/tmux-installed.png)

进入 NAS 控制台，运行 `tmux -V` 可以得到安装好的 tmux 版本信息：

```shell
tmux 3.1b
```

在此放出编译好的 [tmux 扩展包](https://cdn.leovan.me/packages/synology/tmux-apollolake-3.1b.spk)，方便和 DS418play 具有相同系统的 CPU 架构的小伙伴直接使用。

> 本文主要参考了 Synology 官方的扩展包构建指南：https://help.synology.com/developer-guide/create_package/index.html
