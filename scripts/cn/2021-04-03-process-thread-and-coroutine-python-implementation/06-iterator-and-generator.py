#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections

from collections.abc import Iterable, Iterator, Generator
from inspect import getgeneratorstate


def test_instances():
    a_str = 'Leo Van'
    print('字符串: {}'.format(a_str))
    print(isinstance(a_str, Iterable))
    print(isinstance(a_str, Iterator))
    print(isinstance(a_str, Generator))

    a_list = [1, 1, 2, 3, 5, 8]
    print('列表: {}'.format(a_list))
    print(isinstance(a_list, Iterable))
    print(isinstance(a_list, Iterator))
    print(isinstance(a_list, Generator))

    a_dict = {'name': 'Leo Van', 'gender': 'Male'}
    print('字典: {}'.format(a_dict))
    print(isinstance(a_dict, Iterable))
    print(isinstance(a_dict, Iterator))
    print(isinstance(a_dict, Generator))

    a_deque = collections.deque('abcdefg')
    print('Deque: {}'.format(a_deque))
    print(isinstance(a_deque, Iterable))
    print(isinstance(a_deque, Iterator))
    print(isinstance(a_deque, Generator))

    a_iter = iter(a_list)
    print('Iter: {}'.format(a_iter))
    print(isinstance(a_iter, Iterable))
    print(isinstance(a_iter, Iterator))
    print(isinstance(a_iter, Generator))


class MyList(object):
    def __init__(self, end):
        super(MyList, self).__init__()

        self.end = end

    def __repr__(self):
        return '[{}]'.format(', '.join([str(ele) for ele in self]))

    def __iter__(self):
        return MyListIterator(self.end)


class MyListIterator(object):
    def __init__(self, end):
        super(MyListIterator, self).__init__()

        self.data = end
        self.start = 0

    def __iter__(self):
        return self

    def __next__(self):
        while self.start < self.data:
            self.start += 1
            return self.start - 1

        raise StopIteration


def test_list_iterator():
    my_list = MyList(3)

    print('MyList: {}'.format(my_list))
    print(isinstance(my_list, Iterable))
    print(isinstance(my_list, Iterator))

    for ele in my_list:
        print(ele)

    my_list_iterator = MyListIterator(3)

    print('MyListIterator: {}'.format(my_list_iterator))
    print(isinstance(my_list_iterator, Iterable))
    print(isinstance(my_list_iterator, Iterator))

    for ele in my_list_iterator:
        print(ele)

    my_iterator = iter(my_list)

    print('MyIterator: {}'.format(my_iterator))
    print(isinstance(my_iterator, Iterable))
    print(isinstance(my_iterator, Iterator))

    while True:
        try:
            print(next(my_iterator))
        except StopIteration as e:
            return


def test_list_generator():
    a_list = [x for x in range(10)]
    print(isinstance(a_list, Generator))

    a_generator = (x for x in range(10))
    print(isinstance(a_generator, Generator))


def my_yield(n):
    now = 0

    while now < n:
        yield now
        now += 1

    raise StopIteration


def test_my_yield():
    gen = my_yield(4)
    print(gen)
    print(isinstance(gen, Generator))
    print(getgeneratorstate(gen))

    print(gen.send(None))
    print(next(gen))
    print(getgeneratorstate(gen))

    print(gen.send(None))
    print(next(gen))
    print(getgeneratorstate(gen))

    gen.close()
    print(getgeneratorstate(gen))


if __name__ == '__main__':
    line_sep = '-' * 60

    print(line_sep)
    print('测试类型')
    print(line_sep)
    test_instances()
    print(line_sep)

    print(line_sep)
    print('测试迭代器')
    print(line_sep)
    test_list_iterator()
    print(line_sep)

    print(line_sep)
    print('测试 Generator')
    print(line_sep)
    test_list_generator()
    print(line_sep)

    print(line_sep)
    print('测试 Yield')
    print(line_sep)
    test_my_yield()
    print(line_sep)
