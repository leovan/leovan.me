#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from typing import List


def solve_shortest_path_floyd_warshall_dp(dist: List[List[int]], dist_m: List[List[int]]):
    """ 利用 Floyd-Warshall 算法求解最短路

    Args:
        dist: 两点间的距离
        dist_m: 备忘录

    Returns:

    """

    vertex_count = len(dist)

    for k in range(vertex_count):
        for i in range(vertex_count):
            for j in range(vertex_count):
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    dist_m[i][j] = k


def get_shortest_path_floyd_warshall_dp(dist_m: List[List[int]], i: int, j: int, path: List[int]):
    """ 还原最短路路径

    Args:
        dist_m: 备忘录
        i: 起点
        j: 终点
        path: 路径

    Returns:

    """

    if i == j:
        return

    if dist_m[i][j] == 0:
        path.append(j)
    else:
        get_shortest_path_floyd_warshall_dp(dist_m, i, dist_m[i][j], path)
        get_shortest_path_floyd_warshall_dp(dist_m, dist_m[i][j], j, path)


if __name__ == '__main__':
    inf = sys.maxsize
    vertex_count = 4

    dist = [[inf if i != j else 0 for i in range(vertex_count)] for j in range(vertex_count)]
    dist[0][1] = 2
    dist[0][2] = 6
    dist[0][3] = 4
    dist[1][2] = 3
    dist[2][0] = 7
    dist[2][3] = 1
    dist[3][0] = 5
    dist[3][2] = 12

    dist_m = [[0 for _ in range(vertex_count)] for _ in range(vertex_count)]
    solve_shortest_path_floyd_warshall_dp(dist, dist_m)

    for start in range(vertex_count):
        for end in range(vertex_count):
            if start == end:
                continue

            path = []
            get_shortest_path_floyd_warshall_dp(dist_m, start, end, path)

            print('Start: {start}'.format(start=start+1))
            print('End: {end}'.format(end=end+1))
            print('Shortest Path Length: {length}'.format(length=dist[start][end]))
            print('Shortest Path: {path}\n'.format(path=' -> '.join([str(vertex) for vertex in path])))
