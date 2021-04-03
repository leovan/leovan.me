#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import random

from threading import Thread, Lock, RLock


LOCK = Lock()


def job1(n=10):
    global C

    for idx in range(n):
        C += 1
        print('Job1: {}'.format(C))
        time.sleep(random.random())


def job2(n=10):
    global C

    for idx in range(n):
        C += 10
        print('Job2: {}'.format(C))
        time.sleep(random.random())


def test_job():
    global C
    C = 0

    t1 = Thread(target=job1)
    t2 = Thread(target=job2)

    t1.start()
    t2.start()

    t1.join()
    t2.join()


def job1_with_lock(n=10):
    global C, LOCK

    LOCK.acquire()

    for idx in range(n):
        C += 1
        print('Job1: {}'.format(C))
        time.sleep(random.random())

    LOCK.release()


def job2_with_lock(n=10):
    global C, LOCK

    LOCK.acquire()

    for idx in range(n):
        C += 10
        print('Job2: {}'.format(C))
        time.sleep(random.random())

    LOCK.release()


def test_job_with_lock():
    global C, LOCK

    C = 0
    LOCK = Lock()

    t1 = Thread(target=job1_with_lock)
    t2 = Thread(target=job2_with_lock)

    t1.start()
    t2.start()

    t1.join()
    t2.join()


def lock_with_lock(n=10):
    c = 0
    lock = Lock()

    with lock:
        for idx in range(n):
            c += 1
            with lock:
                print(c)


def test_lock_with_lock():
    t = Thread(target=lock_with_lock)
    t.start()
    t.join(timeout=3)


def rlock_with_lock(n=10):
    c = 0
    lock = RLock()

    with lock:
        for idx in range(n):
            c += 1
            with lock:
                print(c)


def test_rlock_with_lock():
    t = Thread(target=rlock_with_lock)
    t.start()
    t.join()


if __name__ == '__main__':
    line_sep = '-' * 60

    print(line_sep)
    print('无锁')
    print(line_sep)
    test_job()
    print(line_sep)

    print(line_sep)
    print('有锁')
    print(line_sep)
    test_job_with_lock()
    print(line_sep)

    print(line_sep)
    print('锁嵌套 - Lock')
    print(line_sep)
    test_lock_with_lock()
    print(line_sep)

    print(line_sep)
    print('锁嵌套 - RLock')
    print(line_sep)
    test_rlock_with_lock()
    print(line_sep)

    sys.exit()
