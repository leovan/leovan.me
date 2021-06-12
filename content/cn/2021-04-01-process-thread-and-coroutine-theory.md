---
title: 进程，线程和协程 (Process, Thread and Coroutine)
subtitle: 理论篇
author: 范叶亮
date: '2021-04-01'
slug: process-thread-and-coroutine-theory
show_toc: true
toc_depth: 3
categories:
  - 编程
tags:
  - 进程
  - Process
  - 线程
  - Thread
  - 协程
  - Coroutine
  - 进程间通讯
  - inter-process communicate
  - IPC
  - 生成器
  - Generator
  - 迭代器
  - Iterator
  - 并发性
  - 并行性
  - 临界区段
  - Critical Section
  - 同步原语
  - 锁
  - 互斥锁
  - Mutual Exclusion
  - Mutex
  - 信号量
  - Semaphore
  - 进程间通信
  - 管道
  - Pipe
  - Pipeline
  - 命名管道
  - Named Pipe
  - 信号
  - Signal
  - 消息队列
  - Message Queue
  - 信号量
  - Semphore
  - 共享内存
  - Shared Memory
  - 伯克利套接字
  - Internet Berkeley Sockets
  - BSD 套接字
  - BSD Sockets
  - 网络套接字
  - Network Socket
  - 线程间通信
  - 读写锁
  - 条件变量
  - 自旋锁
images:
  - /images/cn/2021-04-01-process-thread-and-coroutine-theory/single-thread-process-vs-multiple-threads-process.png
  - /images/cn/2021-04-01-process-thread-and-coroutine-theory/subroutine-vs-coroutine.png
---

> Python 实现篇请参见：[进程，线程和协程 (Process, Thread and Coroutine) - 实现篇](/cn/2021/04/process-thread-and-coroutine-python-implementation)

## 进程，线程和协程

**进程（Process）**是计算机中已运行的程序 [^process-wiki]。**线程（Thread）**是操作系统能够进行运算调度的最小单位。大部分情况下，线程被包含在进程之中，是进程中的实际运作单位。一条线程指的是进程中一个单一顺序的控制流，一个进程中可以并发多个线程，每条线程并行执行不同的任务 [^thread-wiki]。

进程和线程之间的主要区别在于：

1. 线程共享创建其进程的地址空间，进程使用自己的地址。
2. 线程可以直接访问进程的数据，进程使用其父进程数据的副本。
3. 线程可以同其进程中其他线程直接通信，进程必须使用**进程间通讯（inter-process communicate, IPC）**与同级进程通信。
4. 线程开销较小，进程开销较大。
5. 线程的创建较为容易，进程需要复制其父进程。
6. 线程可以控制相同进程的其他线程，进程只能控制其子进程。
7. 对于主线程的修改（例如：取消、优先级修改等）可能会影响进程中的其他线程，对于父进程的修改不会影响其子进程。

单线程进程和多线程进程之间的对比如下图所示：

![](/images/cn/2021-04-01-process-thread-and-coroutine-theory/single-thread-process-vs-multiple-threads-process.png)

一个关于进程和线程的形象类比如下 [^process-thread-analogy]：

1. 计算机的核心是 CPU，它承担了所有的计算任务。它就像一座工厂，时刻在运行。
2. 假定工厂的电力有限，一次只能供给一个车间使用。也就是说，一个车间开工的时候，其他车间都必须停工。背后的含义就是，单个 CPU 一次只能运行一个任务。
3. **进程**就好比工厂的车间，它代表 CPU 所能处理的单个任务。任一时刻，CPU 总是运行一个进程，其他进程处于非运行状态。
4. 一个车间里，可以有很多工人。他们协同完成一个任务。
5. **线程**就好比车间里的工人。一个进程可以包括多个线程。
6. 车间的空间是工人们共享的，比如许多房间是每个工人都可以进出的。这象征一个进程的内存空间是共享的，每个线程都可以使用这些共享内存。
7. 可是，每间房间的大小不同，有些房间最多只能容纳一个人，比如厕所。里面有人的时候，其他人就不能进去了。这代表一个线程使用某些共享内存时，其他线程必须等它结束，才能使用这一块内存。
8. 一个防止他人进入的简单方法，就是门口加一把锁。先到的人锁上门，后到的人看到上锁，就在门口排队，等锁打开再进去。这就叫“互斥锁”（Mutual Exclusion，Mutex），防止多个线程同时读写某一块内存区域。
9. 还有些房间，可以同时容纳 `$n$` 个人，比如厨房。也就是说，如果人数大于 `$n$`，多出来的人只能在外面等着。这好比某些内存区域，只能供给固定数目的线程使用。
10. 这时的解决方法，就是在门口挂 `$n$` 把钥匙。进去的人就取一把钥匙，出来时再把钥匙挂回原处。后到的人发现钥匙架空了，就知道必须在门口排队等着了。这种做法叫做“信号量”（Semaphore），用来保证多个线程不会互相冲突。不难看出，Mutex 是 Semaphore 的一种特殊情况（`$n = 1$` 时）。也就是说，完全可以用后者替代前者。但是，因为 Mutex 较为简单，且效率高，所以在必须保证资源独占的情况下，还是采用这种设计。
11. 操作系统的设计，因此可以归结为三点：(1). 以多进程形式，允许多个任务同时运行；(2). 以多线程形式，允许单个任务分成不同的部分运行；(3). 提供协调机制，一方面防止进程之间和线程之间产生冲突，另一方面允许进程之间和线程之间共享资源。

**协程**（Coroutine）是计算机程序的一类组件，推广了协作式多任务的子例程，允许执行被挂起与被恢复。相对子例程而言，协程更为一般和灵活，但在实践中使用没有子例程那样广泛。协程更适合于用来实现彼此熟悉的程序组件，如协作式多任务、异常处理、事件循环、迭代器、无限列表和管道。

**子例程**（Subroutine），是一个大型程序中的某部分代码，由一个或多个语句块组成。它负责完成某项特定任务，而且相较于其他代码，具备相对的独立性。

协程和子例程的执行过程对比如下：

![](/images/cn/2021-04-01-process-thread-and-coroutine-theory/subroutine-vs-coroutine.png)

- 子例程可以调用其他子例程，调用者等待被调用者结束后继续执行，故而子例程的生命期遵循后进先出，即最后一个被调用的子例程最先结束返回。协程的生命期完全由对它们的使用需要来决定。
- 子例程的起始处是惟一的入口点，每当子例程被调用时，执行都从被调用子例程的起始处开始。协程可以有多个入口点，协程的起始处是第一个入口点，每个 `yield` 返回出口点都是再次被调用执行时的入口点。
- 子例程只在结束时一次性的返回全部结果值。协程可以在 `yield` 时不调用其他协程，而是每次返回一部分的结果值，这种协程常称为**生成器**或**迭代器**。

协程类似于线程，但是协程是协作式多任务的，而线程是抢占式多任务的。这意味着协程提供**并发性**而非**并行性**。协程超过线程的好处是它们可以用于硬性实时的语境（在协程之间的切换不需要涉及任何系统调用或任何阻塞调用），这里不需要用来守卫**临界区段**的**同步原语**比如互斥锁、信号量等，并且不需要来自操作系统的支持。

## 通信

### 进程间通信

#### 管道

管道（Pipeline）是一系列将标准输入输出链接起来的进程，其中每一个进程的输出被直接作为下一个进程的输入。 例如：

```shell
ls -l | less
```

`ls` 用于在 Unix 下列出目录内容，`less` 是一个有搜索功能的交互式的文本分页器。这个管道使得用户可以在列出的目录内容比屏幕长时目录上下翻页。

#### 命名管道

命名管道是计算机进程间的一种先进先出通信机制。是类 Unix 系统传统管道的扩展。传统管道属于匿名管道，其生存期不超过创建管道的进程的生存期。但命名管道的生存期可以与操作系统运行期一样长。

#### 信号

信号（Signals）是 Unix、类 Unix 以及其他 POSIX 兼容的操作系统中进程间通讯的一种有限制的方式。它是一种异步的通知机制，用来提醒进程一个事件已经发生。当一个信号发送给一个进程，操作系统中断了进程正常的控制流程，此时，任何非原子操作都将被中断。如果进程定义了信号的处理函数，那么它将被执行，否则就执行默认的处理函数。

例如，在一个运行的程序的控制终端键入特定的组合键可以向它发送某些信号：<kbd>Ctrl</kbd> + <kbd>C</kbd> 发送 INT 信号（SIGINT），这会导致进程终止；<kbd>Ctrl</kbd> + <kbd>Z</kbd> 发送 TSTP 信号（SIGTSTP），这会导致进程挂起。

#### 消息队列

消息队列提供了异步的通信协议，每一个贮列中的纪录包含详细说明的资料，包含发生的时间，输入设备的种类，以及特定的输入参数，也就是说：消息的发送者和接收者不需要同时与消息队列交互。消息会保存在队列中，直到接收者取回它。

消息队列本身是异步的，它允许接收者在消息发送很长时间后再取回消息。和信号相比，消息队列能够传递更多的信息。与管道相比，消息队列提供了有格式的数据，这可以减少开发人员的工作量。

#### 信号量

信号量（Semaphore）又称为信号标，是一个同步对象，用于保持在 0 至指定最大值之间的一个计数值。当线程完成一次对该 Semaphore 对象的等待（wait）时，该计数值减一；当线程完成一次对 Semaphore 对象的释放（release）时，计数值加一。当计数值为 0，则线程等待该 Semaphore 对象不再能成功直至该 Semaphore 对象变成 signaled 状态。Semaphore 对象的计数值大于 0，为 signaled 状态；计数值等于 0，为 nonsignaled 状态.

#### 共享内存

共享内存指可被多个进程存取的内存，一个进程是一段程序的单个运行实例。在这种情况下，共享内存被用作进程间的通讯。

#### 伯克利套接字

伯克利套接字（Internet Berkeley Sockets），又称为 BSD 套接字是一种应用程序接口，主要用于实现进程间通讯，在计算机网络通讯方面被广泛使用。

### 线程间通信

#### 锁机制

- **互斥锁**：互斥锁（Mutual Exclusion，Mutex）是一种用于多线程编程中，防止两条线程同时对同一公共资源（比如全局变量）进行读写的机制。
- **条件锁**：读写锁是计算机程序的并发控制的一种同步机制，用于解决读写问题。读操作可并发重入，写操作是互斥的。
- **条件变量**：条件变量是利用线程间共享的全局变量进行同步的一种机制，主要包括两个动作：一个线程等待“条件变量的条件成立”而挂起；另一个线程使“条件成立”（给出条件成立信号）。为了防止竞争，条件变量的使用总是和一个互斥锁结合在一起。
- **自旋锁**：自旋锁是用于多线程同步的一种锁，线程反复检查锁变量是否可用。由于线程在这一过程中保持执行，因此是一种忙等待。一旦获取了自旋锁，线程会一直保持该锁，直至显式释放自旋锁。

#### 信号

同上文。

#### 信号量

同上文。

[^process-wiki]: https://zh.wikipedia.org/wiki/进程

[^thread-wiki]: https://zh.wikipedia.org/wiki/线程

[^process-thread-analogy]: https://www.ruanyifeng.com/blog/2013/04/processes_and_threads.html