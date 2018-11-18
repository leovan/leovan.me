#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List


def solve_longest_common_subsequence_dp(x: List[str], y: List[str]):
    """ 利用 BP 求解最长公共子序列问题

    Args:
        x: 序列 X
        y: 序列 Y

    Returns:
        c_l: 不同状态下的最长公共子序列长度
        c_m: 不同状态下的最长公共子序列备忘录 (用于还原最长公共子序列)

    """

    m = len(x) + 1
    n = len(y) + 1

    c_l = [[0 for _ in range(n)] for _ in range(m)]
    c_m = [['' for _ in range(n)] for _ in range(m)]

    for i in range(m):
        for j in range(n):
            if i == 0 or j == 0:
                c_m[i][j] = 'NA'
            elif x[i-1] == y[j-1]:
                c_l[i][j] = c_l[i - 1][j - 1] + 1
                c_m[i][j] = '↖'
            else:
                if c_l[i][j-1] <= c_l[i-1][j]:
                    c_l[i][j] = c_l[i-1][j]
                    c_m[i][j] = '↑'
                else:
                    c_l[i][j] = c_l[i][j-1]
                    c_m[i][j] = '←'

    return c_l, c_m


def get_longest_common_subsequence_dp(c_m: List[List[str]], x: List[str], i: int, j: int, s: List[str]):
    """ 还原最长公共子序列

    Args:
        c_m: 不同状态下的最长公共子序列备忘录
        x: 序列 X
        i: 序列 X 的下标
        j: 序列 Y 的下标
        s: 最长公共子序列

    Returns:
        最长公共子序列

    """

    if i == 0 or j == 0:
        return

    if c_m[i][j] == '↖':
        s.insert(0, x[i-1])
        get_longest_common_subsequence_dp(c_m, x, i-1, j-1, s)
    elif c_m[i][j] == '↑':
        get_longest_common_subsequence_dp(c_m, x, i-1, j, s)
    else:
        get_longest_common_subsequence_dp(c_m, x, i, j-1, s)


if __name__ == '__main__':
    x = ['A', 'B', 'C', 'B', 'D', 'A', 'B']
    y = ['B', 'D', 'C', 'A', 'B', 'A']

    c_l, c_m = solve_longest_common_subsequence_dp(x, y)
    s = []
    get_longest_common_subsequence_dp(c_m, x, len(x), len(y), s)

    print('Longest Common Subsequence Length: {length}'.format(length=c_l[len(x)][len(y)]))
    print('Longest Common Subsequence: {subsequence}'.format(subsequence=s))
