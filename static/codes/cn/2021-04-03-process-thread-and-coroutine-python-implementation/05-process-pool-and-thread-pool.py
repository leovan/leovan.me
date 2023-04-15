#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import threading

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed


def print_func(n=3):
    for idx in range(n):
        print('运行 {}-{}'.format(threading.get_ident(), idx))
        time.sleep(1)


def return_func(n=3):
    res = []

    for idx in range(n):
        res.append('{}-{}'.format(threading.get_ident(), idx))
        time.sleep(1)

    return res


def test_thread_pool_print(n=3, m=6):
    with ThreadPoolExecutor(max_workers=n) as executor:
        for _ in range(m):
            executor.submit(print_func)


def test_process_pool_print(n=3, m=6):
    with ProcessPoolExecutor(max_workers=n) as executor:
        for _ in range(m):
            executor.submit(print_func)


def test_thread_pool_return(n=3, m=6):
    with ThreadPoolExecutor(max_workers=n) as executor:
        futures = [executor.submit(return_func) for _ in range(m)]

        for future in as_completed(futures):
            print(future.result())


def test_process_pool_return(n=3, m=6):
    with ProcessPoolExecutor(max_workers=n) as executor:
        futures = [executor.submit(return_func) for _ in range(m)]

        for future in as_completed(futures):
            print(future.result())


if __name__ == '__main__':
    line_sep = '-' * 60

    print(line_sep)
    print('测试线程池')
    print(line_sep)
    test_thread_pool_print()
    print(line_sep)

    print(line_sep)
    print('测试进程池')
    print(line_sep)
    test_process_pool_print()
    print(line_sep)

    print(line_sep)
    print('测试线程池')
    print(line_sep)
    test_thread_pool_return()
    print(line_sep)

    print(line_sep)
    print('测试进程池')
    print(line_sep)
    test_process_pool_return()
    print(line_sep)
