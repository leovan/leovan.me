#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List


class Item(object):
    """ 物品

    Attributes:
        name: 物品名称
        weight: 物品重量
        value: 物品价值

    """
    def __init__(self, name: str, weight: int, value: int):
        self._name = name
        self._weight = weight
        self._value = value

    def __repr__(self):
        return '({name}, w: {weight}, v: {value})'.format(name=self._name, weight=self._weight, value=self._value)

    @property
    def name(self):
        return self._name

    @property
    def weight(self):
        return self._weight

    @property
    def value(self):
        return self._value


class Bag(object):
    """ 背包

    Attributes:
        capacity: 背包容量
        items: 背包中的物品
        value: 背包中物品的总价值

    """

    def __init__(self, capacity: float):
        self._capacity = capacity
        self._items = []

    def __repr__(self):
        return '({items})'.format(items=', '.join([item.name for item in self._items]))

    @property
    def capacity(self):
        return self._capacity

    @property
    def items(self):
        return self._items

    @property
    def value(self):
        return sum([item.value for item in self._items])

    def add_item(self, item: Item):
        """ 添加单个物品

        Args:
            item: 物品

        Returns:

        """

        self._items.append(item)

    def add_items(self, items: List[Item]):
        """ 添加多个物品

        Args:
            items: 物品列表

        Returns:

        """

        for item in items:
            self._items.append(item)


def solve_zero_one_knapsack_dp(items: List[Item], bag_capacity: int):
    """ 利用 BP 求解 0-1 背包问题

    Args:
        items: 物品列表
        bag_capacity: 背包容量

    Returns:
        不同状态下的背包

    """

    bags = [[Bag(c) for c in range(bag_capacity + 1)] for _ in range(len(items))]

    for i in range(len(items)):
        for w in range(bag_capacity + 1):
            if i == 0 or w == 0:
                continue
            elif w < items[i].weight:
                bags[i][w].add_items(bags[i-1][w].items)
            else:
                if bags[i-1][w].value > bags[i-1][w-items[i].weight].value + items[i].value:
                    bags[i][w].add_items(bags[i-1][w].items)
                else:
                    bags[i][w].add_items(bags[i-1][w-items[i].weight].items)
                    bags[i][w].add_item(items[i])

    return bags


if __name__ == '__main__':
    bag_capacity = 10

    names = ['A', 'B', 'C', 'D', 'E']
    weights = [2, 2, 6, 5, 4]
    values = [6, 3, 5, 4, 6]

    items = [Item(name, weight, value) for name, weight, value in zip(names, weights, values)]
    items.insert(0, Item('NA', 0, 0))

    result = solve_zero_one_knapsack_dp(items, bag_capacity)

    print('Value: {value}'.format(value=result[-1][-1].value))
    print('Items: {items}'.format(items=result[-1][-1].items))
