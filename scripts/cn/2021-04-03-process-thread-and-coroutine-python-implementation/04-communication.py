#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

from queue import Queue
from threading import Thread, Event, Condition


class EventThread(Thread):
    def __init__(self, name, event):
        super(EventThread, self).__init__()

        self.name = name
        self.event = event

    def run(self):
        print('线程 {} 启动于 {}'.format(self.name, time.ctime(time.time())))
        self.event.wait()
        print('线程 {} 结束于 {}'.format(self.name, time.ctime(time.time())))


def test_event(n):
    threads = {}
    event = Event()

    for tid in range(n):
        threads[tid] = EventThread(str(tid), event)

    event.clear()

    for thread in threads.values():
        thread.start()

    print('等待 3 秒钟 ...')
    time.sleep(3)

    print('唤醒所有线程 ...')
    event.set()


class Seeker(Thread):
    def __init__(self, condition, name):
        super(Seeker, self).__init__()

        self.condition = condition
        self.name = name

    def run(self):
        time.sleep(1) # 确保先运行 Hider 中的方法

        self.condition.acquire()

        print('{}: 我把眼睛蒙好了'.format(self.name))
        self.condition.notify()
        self.condition.wait()
        print('{}: 我找到你了'.format(self.name))
        self.condition.notify()

        self.condition.release()
        print('{}: 我赢了'.format(self.name))


class Hider(Thread):
    def __init__(self, condition, name):
        super(Hider, self).__init__()

        self.condition = condition
        self.name = name

    def run(self):
        self.condition.acquire()

        self.condition.wait()
        print('{}: 我藏好了'.format(self.name))
        self.condition.notify()
        self.condition.wait()
        self.condition.release()
        print('{}: 被你找到了'.format(self.name))


def test_hide_and_seek():
    condition = Condition()

    seeker = Seeker(condition, 'Seeker')
    hider = Hider(condition, 'Hider')

    seeker.start()
    hider.start()


class Student(object):
    def __init__(self, name):
        super(Student, self).__init__()

        self.name = name

    def speak(self):
        print('{}: 到'.format(self.name))


class Teacher(object):
    def __init__(self, queue):
        super(Teacher, self).__init__()

        self.queue = queue

    def call(self, student_name):
        if student_name == 'exit':
            print('老师: 点名结束，开始上课')
        else:
            print('老师: {}'.format(student_name))

        self.queue.put(student_name)


class CallManager(Thread):
    def __init__(self, queue):
        super(CallManager, self).__init__()

        self.students = {}
        self.queue = queue

    def put(self, student):
        self.students.setdefault(student.name, student)

    def run(self):
        while True:
            student_name = self.queue.get()

            if student_name == 'exit':
                break
            elif student_name in self.students:
                self.students[student_name].speak()
            else:
                print('学生: 老师，没有 {} 这个人'.format(student_name))


def test_call():
    queue = Queue()

    teacher = Teacher(queue=queue)
    s1 = Student(name='张三')
    s2 = Student(name='李四')

    cm = CallManager(queue)
    cm.put(s1)
    cm.put(s2)

    cm.start()

    print('开始点名')
    teacher.call('张三')
    time.sleep(1)
    teacher.call('李四')
    time.sleep(1)
    teacher.call('王五')
    time.sleep(1)
    teacher.call('exit')


if __name__ == '__main__':
    line_sep = '-' * 60

    print(line_sep)
    print('测试 Event')
    print(line_sep)
    test_event(6)
    time.sleep(3)
    print(line_sep)

    time.sleep(3)

    print(line_sep)
    print('测试 Condition')
    print(line_sep)
    test_hide_and_seek()
    time.sleep(3)
    print(line_sep)

    time.sleep(3)

    print(line_sep)
    print('测试 Queue')
    print(line_sep)
    test_call()
    time.sleep(3)
    print(line_sep)
