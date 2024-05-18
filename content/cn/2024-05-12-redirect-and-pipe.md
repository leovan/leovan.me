---
title: 重定向和管道 (Redirect and Pipe)
author: 范叶亮
date: '2024-05-12'
slug: redirect-and-pipe
categories:
  - Tech101
  - Linux
tags:
  - 重定向
  - redirect
  - 管道
  - pipe
  - 文件描述符
  - stdin
  - stdout
  - stderr
  - Here Document
images:
  - /images/cn/2024-05-12-redirect-and-pipe/输入输出.svg
---

# 输入输出文件描述符

在 Linux 启动后，init 进程会创建 3 个特殊的文件描述符分配给输入输出。

| 文件描述符 | 英文描述 | 中文描述 |
| ---------- | -------- | -------- |
| 0          | stdin    | 标准输入 |
| 1          | stdout   | 标准输出 |
| 2          | stderr   | 标准错误 |

默认情况下，程序经由标准输入（stdin）从键盘读取数据，并将标准输出（stdout）和标准错误（stderr）显示在屏幕上。

![](/images/cn/2024-05-12-redirect-and-pipe/输入输出.svg)

在 Linux 中，init 是所有进程的父进程，所有子进程均会继承父进程的文件描述符。因此在 Linux 中执行的所有程序都可以从 stdin 获取输入，并将结果打印到 stdout 中，同时将错误信息打印到 stderr 中。

# 重定向

当我们不希望从键盘获取标准输入或将标准输出和标准错误显示在屏幕上时，则需要采用重定向。

## 输出重定向

输出重定向的使用方式如下：

```plain
cmd [1-n]> [文件/文件描述符/设备等]
```

假设当前目录下存在一个名为 `yes.txt` 的文件，且不存在名为 `no.txt` 的文件。执行如下命令：

```sh
ls yes.txt no.txt
```

由于 `yes.txt` 存在，这部分结果将输出到 stdout，同时由于 `no.txt` 不存在，这部分结果将输出到 stderr。命令的输出结果为：

```plain
ls: cannot access 'no.txt': No such file or directory
yes.txt
```

执行如下命令：

```sh
ls yes.txt no.txt 1> success.log 2> fail.log
```

此时屏幕上将不再显示任何信息，当前目录下会生成 `success.log` 和 `fail.log` 两个文件。其中 `1> success.log` 表示将 stdout 重定向至 `success.log`，`2> fail.log` 表示将 stderr 重定向至 `fail.log`。因此 `success.log` 中的内容为 `yes.txt`，`fail.log` 中的内容为 `ls: cannot access 'no.txt': No such file or directory`。

重定向过程中，stdout 的文件描述符 `1` 可以省略，但 stderr 的文件描述符 `2` 不可以省略。因此，当只重定向 stdout 时，可简写为：

```sh
ls yes.txt no.txt > success.log
```

此时屏幕上依旧会显示 stderr 的内容 `ls: cannot access 'no.txt': No such file or directory`，而 stdout 的内容则被重定向至 `success.log` 文件中。

在 Linux 中 `&-` 和 `/dev/null` 是两个特殊的输出设备，均表示为空，输出到该设备相当于抛弃输出。因此如下两行命令分别会抛弃 stdout 和 stderr 的内容：

```sh
ls yes.txt no.txt 1>&-
ls yes.txt no.txt 2> /dev/null
```

`&` 可以表示当前进程中已经存在的描述符，`&1` 表示 stdout，`&2` 表示 stderr。因此我们可以将 stdout 和 stderr 重定向到相同文件：

```sh
ls yes.txt no.txt > out.log 2> out.log
ls yes.txt no.txt > out.log 2>&1
```

在上述两种方式中，第一种会导致 `out.log` 文件被打开两次，stdout 和 stderr 内容会相互覆盖。第二种由于 stderr 重定向给了 stdout，stdout 重定向给了 `out.log`，因此 `out.log` 仅被打开了一次。

使用 `>` 进行输出重定向时会先判断文件是否存在，如果存在会先删除再创建，不存在则直接创建，无论命令是否执行成功均会创建。使用 `>>` 进行重定向时，如果文件存在则会以添加方式打开，不存在则直接创建。

## 输入重定向

输入重定向的使用方式如下：

```plain
cmd [1-n]< [文件/文件描述符/设备等]
```

例如：

```sh
cat > out.txt < in.txt
```

此时命令将从 `in.txt` 文件中获取输入而非 stdin，并将结果重定向到 `out.txt` 文件中。

## Here Document

Here Document 是一种特殊的重定向方式，可以用来将多行输入传递给命令，使用方式如下：

```plain
cmd << delimiter
    ...
delimiter
```

这会将中间的内容 `...` 传递给命令。需要注意结尾处的 `delimiter` 的前后均不能包含任何字符，起始处的 `delimiter` 的前后空白字符将被忽略。最为常用的 `delimiter` 为 `EOF`，但这不是必须的，例如：

```sh
wc -l << SOMETHING
第一行
第二行
第三行
SOMETHING
```

上述命令的输出结果为：

```plain
3
```

# 管道

管道 `|` 可以将一个命令的 stdout 作为下一个命令的 stdin 使用，但无法对 stderr 进行处理。因此管道也可以理解为重定向的一种特殊形式。

假设存在一个如下内容的 `test.txt` 文档：

```plain
Here is a test in line 1.
Here is another test in line 2.
Here is something else in line 3.
```

利用如下命令可以过滤出包含 `test` 字符的行并显示行号：

```sh
cat test.txt | grep -n "test"
```

上述命令的输出结果为：

```plain
1:Here is a test in line 1.
2:Here is another test in line 2.
```

如果希望同时将 stdout 和 stderr 重定向到下一个命令的 stdin，可以采用如下方式：

```sh
ls yes.txt no.txt 2>&1 | grep "No such file or directory"
```

上述命令的输出结果为：

```plain
ls: no.txt: No such file or directory
```

上述命令也可以简写为：

```sh
ls yes.txt no.txt |& grep "No such file or directory"
```
