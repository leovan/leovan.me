#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from threading import Thread


def func(name='Python'):
    for idx in range(2):
        print('Hello, {}'.format(name))
        time.sleep(1)


def test_thread_1():
    thread_1 = Thread(target=func)
    thread_1.start()
    thread_2 = Thread(target=func, args=('Leo', ))
    thread_2.start()


class MyThread(Thread):
    def __init__(self, name='Python'):
        super(MyThread, self).__init__()
        self.name = name

    def run(self):
        for idx in range(2):
            print('Hello, {}'.format(self.name))
            time.sleep(1)


def test_thread_2():
    thread_1 = MyThread()
    thread_2 = MyThread('Leo')

    thread_1.start()
    thread_2.start()


def test_thread_3():
    # 创建线程
    t = Thread(target=func)

    # 启动线程
    t.start()

    # 阻塞线程
    t.join()

    # 判断线程是否处于执行状态
    # True: 执行中，False: 其他
    t.is_alive()

    # 这是线程是否随主线程退出而退出
    # 默认为 False
    t.daemon = True

    # 设置线程名称
    t.name = 'My Thread'


if __name__ == '__main__':
    test_thread_1()
    test_thread_2()
