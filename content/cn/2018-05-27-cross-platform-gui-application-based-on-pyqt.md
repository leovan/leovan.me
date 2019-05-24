---
title: 基于 PyQt5/PySide2 和 QML 的跨平台 GUI 程序开发
author: 范叶亮
date: '2018-05-27'
slug: cross-platform-gui-application-based-on-pyqt
categories:
  - 编程
tags:
  - Qt
  - PyQt
  - PyQt5
  - PySide2
  - QML
  - GUI
  - Cross-Platform
  - 跨平台
images:
  - /images/cn/2018-05-27-cross-platform-gui-application-based-on-pyqt/app.png
  - /images/cn/2018-05-27-cross-platform-gui-application-based-on-pyqt/preferences.png
  - /images/cn/2018-05-27-cross-platform-gui-application-based-on-pyqt/dmg.png
  - /images/cn/2018-05-27-cross-platform-gui-application-based-on-pyqt/nsis.png
---

先聊聊写界面化程序的目的，在 B/S 结构软件盛行的今天，C/S 结构的软件还有人用吗？答案是肯定的，至少你想用 B/S 结构的软件的时候你得有个 C/S 结构的浏览器，对吧？这样说显得有点抬杠，当然，我认为最重要的还是“简单”，或者说“用户友好”。再 Geek 的人应该也喜欢有的时候偷懒，虽然我称不上 Geek，但也经常在黑框框中不用鼠标敲着各种代码，但是还是希望能够有些小工具只要能够点个几下就能帮忙干些事情的。至于对于更普通的用户而言，就应该更加希望能够用最“简单，清晰，明了”的方式“快速”的完成一项任务，有点像 Windows 用户把桌面上的快捷方式拖到回收站，然后和我说：好了，程序卸载了，我只能回答说：或许你该换个 MAC。

## :exclamation: 更新 :exclamation:

[SciHubEVA](https://github.com/leovan/SciHubEVA) 最新版本已经采用 [PySide2](https://wiki.qt.io/Qt_for_Python) 进行改写，Windows 版本安装包构建工作迁移至 [Inno Setup 6](http://www.jrsoftware.org/isinfo.php)，更多变更请参见 [CHANGELOG](https://github.com/leovan/SciHubEVA/blob/master/CHANGELOG.md)。

## 跨平台 GUI 程序开发方案选型

所以，写个带界面的小工具就是把你的想法更好的服务自己和别人的一个好途径，那么问题来了，对于我这做算法的种业余编程选手，怎么搞定界面化应用呢？虽然是业余编程选手，也也一路从 Logo，Basic，VB，C/C++，Java，R，Python 等等走来，当然很多都是从入门到放弃，总之对于同时需要兼顾一定美感的我，总结了几种跨平台界面化的解决方案。

1. [JavaFX](http://www.oracle.com/technetwork/java/javafx/overview/index.html)，基于 JVM，一次编译处处运行，配合 Material Design 风格的 [JFoenix](https://github.com/jfoenixadmin/JFoenix)，应该是能写出很漂亮的界面的。
2. [Qt](https://www.qt.io/)，一次编写处处编译，配合 [Qt Quick](http://doc.qt.io/qt-5/qtquick-index.html) 和 [QML](http://doc.qt.io/qt-5/qtqml-index.html)，可以把前后端分离。原生 C++ 语言支持，同时有 Python 绑定，对于 Python 比较熟的同学相对友好。界面风格上在较新的 Qt Quick 中也支持了 [Material Design 风格](http://doc.qt.io/Qt-5/qtquickcontrols2-material.html)。
3. [Electron](https://electronjs.org/)，使用 JavaScript, HTML 和 CSS 等 Web 技术创建原生程序的框架，很多优秀的应用都是用这个来搞的，例如：[Visual Studio Code](https://github.com/Microsoft/vscode)，[Hyper](https://github.com/zeit/hyper) 等。

我不认为这 3 种方法孰优孰劣，因为毕竟我们的目的是快速的搞定一个漂亮的小工具，因此到底选哪个完全取决于个人对相关技术的熟悉程度。因此，对于我这个搞算法的，最终选择了 Qt 的 Python 绑定 [PyQt](https://riverbankcomputing.com/software/pyqt/intro)。作为 R 的忠实用户，实在是没找到特别好的解决方案，只能找个借口说我们 R 就不是干这个用的......

## 环境配置

当然选择 PyQt 也是有些个人的倾向在里面的，写 C++ 的年代就用过 Qt，对于原理多少有些了解。不过针对 PyQt，以及其与 Qt Quick 和 QML 的结合使用在后面开发时发现相关文档比较少，只能一步一步地趟雷了。毕竟要做跨平台的 GUI 程序开发，因此本文会针对 macOS 和 Windows 两个系统做相关说明，Linux 系统由于发行版本太多就不做说明了，大部分情况应该和 macOS 类似。

- Python (开发语言)

Python 的版本选择了 3.5，因为在后面选择 3.6 时发现编译打包的时候会有些错误，没有细究，简单 Google 了此类问题，发现回退到 3.5 版本就没问题了，可能需要相关打包工具的更新才能有对 3.6 更好的支持。如果使用 Conda 建立虚拟环境，建议新建一个干净的 Python 3.5 的环境。

- Qt 和 PyQt (界面化)

Qt 和 PyQt 均采用比较新的版本，版本号需大于 5.10。Qt 直接从官网下载安装即可，理论上不需要安装 Qt，因为 PyQt 中包含了运行时环境，安装 Qt 的目的是为了使用其可视化的 Qt Creator，设计界面的时候会比较方便。如果使用 Conda 建立 Python 虚拟环境，请使用 pip 安装 PyQt 的对应版本，Conda 中的 PyQt 的版本相对较低，一些新的 Qt 特性不支持。

- PyInstaller (编译打包)

[PyInstaller](https://www.pyinstaller.org/) 是一个用于打包 Python 代码到一个本地化可执行程序的工具，安装其最新版本即可：`pip install PyInstaller`。

- appdmg 和 NSIS (安装包制作)

[appdmg](https://github.com/LinusU/node-appdmg) 是 macOS 下一个用于制作 DMG 镜像的工具，使用前先安装 [Node.js](https://nodejs.org)，再通过 `npm install -g appdmg` 安装最新版即可。[NSIS](https://sourceforge.net/projects/nsis/) 是 Windows 下一个用于制作安装包的工具，NSIS 的一个问题是不支持 Unicode，因此对于包含中文字符的脚本需要以 GBK 编码格式保存。Unicode 版本的 NSIS 为 [Unicode NSIS](http://www.scratchpaper.com)，不过 Unicode NSIS 已经长时间未更新，因此本文依旧将 NSIS 作为安装包制作工具。

## 界面设计

通过需求分析，整个工具最核心的两个界面为程序主界面和配置信息界面：

![APP](/images/cn/2018-05-27-cross-platform-gui-application-based-on-pyqt/app.png)

程序主界面包含了待搜索的信息，保存的路径，相关的按钮和日志输出。

![PREFERENCES](/images/cn/2018-05-27-cross-platform-gui-application-based-on-pyqt/preferences.png)

配置信息界面以配置项的分组不同分别包括通用，网络和代理等相关的配置信息更改。

整个界面设计采用了 Google 的 [Material Design](https://material.io/design/) 风格，尤其是在没有 UI 支援的情况下，使用这个风格至少不会让你的应用太丑。在 PyQt 中，可以通过 [多种方式](http://doc.qt.io/Qt-5/qtquickcontrols2-styles.html) 启用 Material Design 风格。

## 程序开发

本文以 [Sci-Hub EVA](https://github.com/leovan/SciHubEVA) 作为示例介绍 PyQt 的跨平台 GUI 程序开发。Sci-Hub EVA 是一个利用 Sci-Hub API 下载论文的界面化小工具，功能相对简单。首先介绍一下工程的目录：

```{txt}
docs\
images\
translations\
ui\
BUILDING.md
Info.plist
LICENSE
README.md
SciHubEVA.conf
SciHubEVA.cpp
SciHubEVA.dmg.json
SciHubEVA.nsi
SciHubEVA.pro
SciHubEVA.qrc
SciHubEVA.win.version
requirements.txt
scihub_add_scihub_url.py
scihub_api.py
scihub_conf.py
scihub_eva.py
scihub_preferences.py
scihub_resources.py
scihub_utils.py
version_updater.py
```

其中，`docs` 目录为项目的一些文档，`images` 目录为项目的相关图片文件，`translations` 目录为项目的 i18n 翻译文件，`ui` 目录为相关的界面文件 (QML 文件)，`Info.plist` 为 macOS 程序信息文件，`SciHubEVA.conf` 为程序配置文件，`SciHubEVA.cpp` 为 Qt 生成的 C++ 主文件，`SciHubEVA.dmg.json` 为利用 appdmg 制作 DMG 镜像的配置文件，`SciHubEVA.nsi` 为利用 NSIS 制作 Windows 安装包的脚本文件，`SciHubEVA.pro` 为程序的 Qt 主项目文件，，`SciHubEVA.qrc` 为程序的资源文件，`SciHubEVA.win.version` 为打包 Windows 的版本信息文件，`requirements.txt` 为 Python 依赖包信息文件，`scihu_*.py` 为程序实现相关 Python 代码，`version_updater.py` 为版本更新的小工具。

下文中不会介绍具体的业务逻辑代码，而是对开发过程中的一些核心点和注意事项进行简单的介绍。

### Python 与 QML 通信

首先，对于每一个界面 (QML 文件)，我们都有一个与之对应 Python 文件 (除非该页面没有具体的业务逻辑，例如：`ui\SciHubEVAAbout.qml` 为关于页面，`ui\SciHubEVAMenuBar.qml` 为菜单栏)，以主页面 (`ui\SciHubEVA.qml` 和 `scihub_eva.py`) 为例，我们为每个界面创建一个类，同时该类集成自 Qt 的一个基类：

```{python}
class SciHubEVA(QObject):
    pass
```

Python 代码同界面交互的核心是通过 Qt 的 [**信号与槽**](http://doc.qt.io/qt-5/signalsandslots.html)，同样在 PyQt 中也是利用 [相同的机制](http://pyqt.sourceforge.net/Docs/PyQt5/signals_slots.html)。简单的理解 PyQt 与 QML 的信号与槽，可以认为**信号**就是**函数的定义**，**槽**就是**函数的实现**。同时，信号和槽往往会位于不同的地方，例如：信号定义在 Python 中，则对应的槽会在 QML 中，反之亦然，当然这并不是一定的。两者通过 `connect()` 函数连接起来，当触发一个信号时，槽就会接受到信号传递的参数，并执行槽里面相应的逻辑。

### i18n

Qt 对于多语言支持比较完善，在 QML 中对于需要翻译的地方利用 `qsTr()` 函数处理待翻译的文本即可，例如：

```{qml}
Label {
    id: labelQuery
    text: qsTr("Query: ")
}
```

在 Python 代码中，对于继承自 `QObject` 的类，可以利用基类中的 `tr()` 函数处理待翻译的文本即可，例如：

```{python}
self.tr('Saved PDF as: ')
```

同时将具有待翻译文本的文件加入到 `SciHubEVA.pro` 的主工程文件中，用于后续翻译处理：

```{text}
lupdate_only {
SOURCES += \
    ui/SciHubEVA.qml \
    ui/SciHubEVAAbout.qml \
    ui/SciHubEVAMenuBar.qml \
    ui/SciHubEVAPreferences.qml \
    ui/SciHubEVAAddSciHubURL.qml \
    scihub_api.py
}

TRANSLATIONS += \
    translations/SciHubEVA_zh_CN.ts
```

因为 Python 代码中也有需要翻译的文件，因此我们需要运行如下命令生成翻译的源文件：

```{bash}
lupdate SciHubEVA.pro
pylupdate5 SciHubEVA.pro
```

这样在 `translations` 目录即可生成待翻译的源文件 (ts 文件)，利用 Qt 自带的 Liguist 可以对其进行编辑，翻译并保存后，利用如下命令生成翻译的结果文件：

```{bash}
lrelease SciHubEVA.pro
```

在 `translations` 目录即可生成待翻译的结果文件 (qm 文件)。

### 资源文件

在 GUI 编程中，我们不可避免的会使用到各种各样的资源，例如：图片，音频，字体等等。Qt 中提供了一种[资源管理方案](http://doc.qt.io/qt-5/resources.html)，可以在不同场景下使用 (Python 和 QML 中均可)。`SciHubEVA.qrc` 定义了所有使用到的资源：

```{xml}
<RCC>
    <qresource prefix="/">
        <file>ui/SciHubEVA.qml</file>
        <file>ui/SciHubEVAMenuBar.qml</file>
        <file>ui/SciHubEVAAbout.qml</file>
        <file>ui/SciHubEVAPreferences.qml</file>
        <file>ui/SciHubEVAAddSciHubURL.qml</file>
        <file>images/about.png</file>
    </qresource>
</RCC>
```

在 QML 中使用示例如下：

```{qml}
Image {
    id: imageAboutLogo
    source: "qrc:/images/about.png"
}
```

在 Python 中使用示例如下：

```{python}
self._engine = QQmlApplicationEngine()
self._engine.load('qrc:/ui/SciHubEVA.qml')
```

使用 `qrc` 文件管理资源文件的一个好处就是不需要担心各种相对路径和绝对路径带来的找不到文件的错误，但同时一个缺点是当资源文件更新后，需要运行 `pyrcc5 SciHubEVA.qrc -o scihub_resources.py` 更新资源，同时还需要在主程序代码中引入生成的 Python 资源代码。

### 界面线程分离

写 GUI 应用的一个重要问题就是界面线程的分离，需要把耗时的业务逻辑摘出来，单独作为一个线程运行，这样才不会造成界面的“假死”情况。`scihub_api.py` 中的 `SciHubAPI` 作为下载文章的主类，下载过程相对耗时。因为其既需要 Qt 中的 `tr()` 函数，也需要线程，通过 Python 的多继承，`SciHubAPI` 类构造如下：

```{python}
class SciHubAPI(QObject, threading.Thread):
    pass
```

## 编译打包

PyInstaller 是一个用于打包 Python 代码到一个本地化可执行程序的工具，详细的使用方法请参见[官方文档](https://www.pyinstaller.org/documentation.html)。同样，我们在此仅说明打包过程中遇到的一些问题。

### macOS

macOS 下的编译打包命令如下：

```{bash}
# 清理相关目录和文件
rm -rf build
rm -rf dist
rm -f SciHubEVA.spec

# 重新生成资源文件
rm -f scihub_resources.py
pyrcc5 SciHubEVA.qrc -o scihub_resources.py

# 编译打包
pyinstaller -w scihub_eva.py \
  --hidden-import "PyQt5.Qt" \
  --hidden-import "PyQt5.QtQuick" \
  --add-data "LICENSE:." \
  --add-data "SciHubEVA.conf:." \
  --add-data "images/SciHubEVA.png:images" \
  --add-data "translations/SciHubEVA_zh_CN.qm:translations" \
  --name "SciHubEVA" \
  --icon "images/SciHubEVA.icns"

# 拷贝程序信息
cp Info.plist dist/SciHubEVA.app/Contents
```

编译打包过程中的 `--hidden-import` 参数是因为我们使用了 Qt Quick 和 QML 相关框架，但是在 Python 代码中我们并没有显式的引入这两个包，因此我们需要告知 PyInstaller 我们使用了这两个包，这样 PyInstaller 才会把相关的动态链接库拷贝到打包的程序中。

打包好的程序 `SciEvaHub.app` 会保存在 `dist` 目录中。由于目前无论是 macOS 还是 Windows 系统，高分辨率已经比较常见，为了适应高分辨率，我们需要在代码中添加相应的支持，在入口 Python 文件中，我们需要在头部添加如下信息：

```{python}
if hasattr(Qt, 'AA_EnableHighDpiScaling'):
    QGuiApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
    QGuiApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
```

同时针对 macOS 系统，我们需要在 `Info.plist` 中添加如下信息以支持高分辨率：

```{xml}
<key>NSHighResolutionCapable</key>
<string>True</string>
<key>NSSupportsAutomaticGraphicsSwitching</key>
<string>True</string>
```

`Info.plist` 中的其他信息针对性进行修改即可，最后将其拷贝到打包好的程序中。

### Windows

Windows 下的编译打包命令如下：

```{dos}
rem 清理相关目录和文件
rd /s /Q build
rd /s /Q dist
del /Q SciHubEVA.spec

rem 重新生成资源文件
del /Q scihub_resources.py
pyrcc5 SciHubEVA.qrc -o scihub_resources.py

rem 编译打包
pyinstaller -w scihub_eva.py ^
  --hidden-import "PyQt5.Qt" ^
  --hidden-import "PyQt5.QtQuick" ^
  --add-data "LICENSE;." ^
  --add-data "SciHubEVA.conf;." ^
  --add-data "images/SciHubEVA.png;images" ^
  --add-data "translations/SciHubEVA_zh_CN.qm;translations" ^
  --name "SciHubEVA" ^
  --icon "images/SciHubEVA.ico" ^
  --version-file "SciHubEVA.win.version"
```

编译打包过程中的 `--version-file` 参数是 Windows 程序的相关版本信息，具体请参见微软的 [Version Information Structures](http://msdn.microsoft.com/en-us/library/ff468916(v=vs.85).aspx)。

打包好的程序会在 `dist\SciHubEVA` 目录中，该目录还包含了所有运行时所需的文件。

## 安装包制作

### macOS

macOS 下我们使用 appdmg 工具将编译打包好的程序制作成 DMG 镜像文件。DMG 镜像文件可以对原始的程序进行压缩，便于分发。appdmg 通过一个 JSON 文件控制 DMG 镜像的制作，详细的 JSON 格式和相关参数请参见 [官方文档](https://github.com/LinusU/node-appdmg)，Sci-Hub EVA 的 DMG 制作 JSON 文件如下：

```{json}
{
    "title": "Sci-Hub EVA",
    "icon": "images/SciHubEVA.icns",
    "icon-size": 100,
    "background": "images/SciHubEVA-dmg-backgroud.png",
    "format": "UDZO",
    "window": {
        "size": {
            "width": 600,
            "height": 400
        }
    },
    "contents": [
        {
            "x": 100,
            "y": 150,
            "type": "file",
            "path": "dist/SciHubEVA.app"
        },
        {
            "x": 300,
            "y": 150,
            "type": "link",
            "path": "/Applications"
        }
    ]
}
```

打包好后的 DMG 镜像效果如下：

![DMG](/images/cn/2018-05-27-cross-platform-gui-application-based-on-pyqt/dmg.png)

### Windows

Windows 下我们使用 NSIS 构建安装包，同样 NSIS 也支持多语言安装包构建，但请注意，NSIS 程序本身并不支持 Unicode，因此 NSIS 安装包的脚本需使用 GBK 编码保存。构建好的安装包的安装界面如下：

![NSIS](/images/cn/2018-05-27-cross-platform-gui-application-based-on-pyqt/nsis.png)

整个 Sci-Hub EVA 的编译打包和安装包制作过程请参见 [构建说明文档](https://github.com/leovan/SciHubEVA/tree/master/building)。
