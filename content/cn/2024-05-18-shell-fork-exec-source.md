---
title: Shell 调用方式 fork，exec 和 source (Run Shell with fork, exec and source)
author: 范叶亮
date: '2024-05-18'
slug: shell-fork-exec-source
categories:
  - Tech101
  - Linux
tags:
  - shell
  - fork
  - exec
  - source
---

在 Linux 中调用一个脚本有多种方式，例如 fork，exec 和 source。其中 fork 为 Linux 系统调用，exec 和 source 均为 bash 内部命令。下面以 `parent.sh` 和 `child.sh` 两个脚本演示不同调用方式的区别。

`parent.sh` 内容如下：

```sh
#!/bin/bash

echo "--------------------------------------------------"
echo "Before calling child.sh"
echo "--------------------------------------------------"
echo "PID for parent.sh: $$"

var="parent"
export var

echo "In parent.sh, set var=$var"
echo "In parent.sh, variable var=$var"

echo "--------------------------------------------------"
case $1 in
    exec)
        echo "Call child.sh using exec"
        exec ./child.sh ;;
    source)
        echo "Call child.sh using source"
        source ./child.sh ;;
    *)
        echo "Call child.sh using fork"
        ./child.sh ;;
esac

echo "After calling child.sh"
echo "--------------------------------------------------"
echo "PID for parent.sh: $$"
echo "In parent.sh, variable var=$var"
echo "--------------------------------------------------"
```

`child.sh` 内容如下：

```sh
#!/bin/bash

echo "--------------------------------------------------"
echo "PID for child.sh: $$"
echo "In child.sh, variable var=$var from parent.sh"

var="child"
export var

echo "In child.sh, set var=$var"
echo "In child.sh, variable var=$var"
echo "--------------------------------------------------"
```

为了确保脚本可执行，需为其添加执行权限：

```sh
chmod +x parent.sh child.sh
```

# fork

fork 通过进程复制来创建一个新进程，新进程称为子进程，当前进程称为父进程。在 fork 之后，子进程拥有父进程的副本，但两者的 PID 不同，同时子进程也拥有父进程的所有属性，例如：环境变量、打开的文件描述符等。

通过 fork 调用是最普遍的方式。在当前终端中通过 `./run.sh` 执行时，终端会新建一个子 shell 执行 `run.sh`，子 shell 执行时，父 shell 仍在运行，当子 shell 运行完毕后会返回父 shell。

运行如下命令进行 fork 方式调用测试：

```sh
./parent.sh fork
```

测试结果如下：

```plain
--------------------------------------------------
Before calling child.sh
--------------------------------------------------
PID for parent.sh: 7149
In parent.sh, set var=parent
In parent.sh, variable var=parent
--------------------------------------------------
Call child.sh using fork
--------------------------------------------------
PID for child.sh: 7150
In child.sh, variable var=parent from parent.sh
In child.sh, set var=child
In child.sh, variable var=child
--------------------------------------------------
After calling child.sh
--------------------------------------------------
PID for parent.sh: 7149
In parent.sh, variable var=parent
--------------------------------------------------
```

# exec

exec 与 fork 不同，其不需要开启一个新的 shell 执行子脚本。使用 exec 执行一个新脚本后，父脚本中 exec 后的内容将不再执行。

运行如下命令进行 exec 方式调用测试：

```sh
./parent.sh exec
```

测试结果如下：

```plain
--------------------------------------------------
Before calling child.sh
--------------------------------------------------
PID for parent.sh: 9629
In parent.sh, set var=parent
In parent.sh, variable var=parent
--------------------------------------------------
Call child.sh using exec
--------------------------------------------------
PID for child.sh: 9629
In child.sh, variable var=parent from parent.sh
In child.sh, set var=child
In child.sh, variable var=child
--------------------------------------------------
```

# source

source 同 exec 类似，也不需要开启一个新的 shell 执行子脚本。使用 source 执行一个新脚本后，父脚本中 source 后的内容可以继续执行。

运行如下命令进行 source 方式调用测试：

```sh
./parent.sh source
```

测试结果如下：

```plain
--------------------------------------------------
Before calling child.sh
--------------------------------------------------
PID for parent.sh: 10274
In parent.sh, set var=parent
In parent.sh, variable var=parent
--------------------------------------------------
Call child.sh using source
--------------------------------------------------
PID for child.sh: 10274
In child.sh, variable var=parent from parent.sh
In child.sh, set var=child
In child.sh, variable var=child
--------------------------------------------------
After calling child.sh
--------------------------------------------------
PID for parent.sh: 10274
In parent.sh, variable var=child
--------------------------------------------------
```
