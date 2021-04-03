#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import requests

from threading import Thread
from multiprocessing import Process


def timer(task_mode):
    def wrapper(func):
        def decorator(*args, **kwargs):
            task_type = kwargs.setdefault('task_type', None)
            start_time = time.time()
            func(*args, **kwargs)
            end_time = time.time()
            print('耗时（{} - {}）: {}'.format(task_mode, task_type, end_time - start_time))
        return decorator
    return wrapper


def cpu_bound_task(x=1, y=1):
    c = 0

    while c < 500000:
        c += 1
        x += x
        y += y


def disk_io_bound_task():
    with open('tmp.log', 'w') as f:
        for idx in range(5000000):
            f.write('{}\n'.format(idx))


def web_io_bound_task():
    try:
        requests.get('https://www.baidu.com')
    except Exception as e:
        pass


def simulation_io_bound_task():
    time.sleep(2)


@timer('单线程')
def single_thread(func, task_type='', n=10):
    for idx in range(n):
        func()


@timer('多线程')
def multi_threads(func, task_type='', n=10):
    threads = {}

    for idx in range(n):
        t = Thread(target=func)
        threads[idx] = t
        t.start()

    for thread in threads.values():
        thread.join()


@timer('多进程')
def multi_processes(func, task_type='', n=10):
    processes = {}

    for idx in range(n):
        p = Process(target=func)
        processes[idx] = p
        p.start()

    for process in processes.values():
        process.join()


if __name__ == '__main__':
    line_sep = '-' * 60

    print(line_sep)
    print('单线程')
    print(line_sep)
    single_thread(cpu_bound_task, task_type='CPU 密集型任务')
    single_thread(disk_io_bound_task, task_type='磁盘 IO 密集型任务')
    single_thread(web_io_bound_task, task_type='网络 IO 密集型任务')
    single_thread(simulation_io_bound_task, task_type='模拟 IO 密集型任务')
    print(line_sep)

    print(line_sep)
    print('多线程')
    print(line_sep)
    multi_threads(cpu_bound_task, task_type='CPU 密集型任务')
    multi_threads(disk_io_bound_task, task_type='磁盘 IO 密集型任务')
    multi_threads(web_io_bound_task, task_type='网络 IO 密集型任务')
    multi_threads(simulation_io_bound_task, task_type='模拟 IO 密集型任务')
    print(line_sep)

    print(line_sep)
    print('多进程')
    print(line_sep)
    multi_processes(cpu_bound_task, task_type='CPU 密集型任务')
    multi_processes(disk_io_bound_task, task_type='磁盘 IO 密集型任务')
    multi_processes(web_io_bound_task, task_type='网络 IO 密集型任务')
    multi_processes(simulation_io_bound_task, task_type='模拟 IO 密集型任务')
    print(line_sep)
