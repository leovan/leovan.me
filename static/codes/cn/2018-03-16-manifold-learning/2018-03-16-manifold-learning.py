#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Mr. Black on 2018-02-28

import numpy as np
from scipy.sparse.csgraph import shortest_path
from sklearn import manifold, datasets, neighbors
from sklearn.utils import check_random_state

from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Source Han Serif CN']
rcParams['font.size'] = 8
rcParams['lines.markersize'] = 2

import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter
from mpl_toolkits.mplot3d import Axes3D

from time import time

def genPoints(n_points=1000, func_name='swiss-roll'):
    if func_name == 'swiss-roll':
        points, colors = datasets.make_swiss_roll(n_points, random_state=0)
    elif func_name == 's-curve':
        points, colors = datasets.make_s_curve(n_points, random_state=0)
    elif func_name == 'severed-sphere':
        random_state = check_random_state(0)
        p = random_state.rand(n_points) * (2 * np.pi - 0.55)
        t = random_state.rand(n_points) * np.pi

        indices = ((t < (np.pi - (np.pi / 8))) & (t > ((np.pi / 8))))
        colors = p[indices]
        points = np.c_[np.sin(t[indices]) * np.cos(p[indices]),
                  np.sin(t[indices]) * np.sin(p[indices]),
                  np.cos(t[indices])]
    else:
        raise ValueError('Unsupported function [%s]' % func_name)

    return points, colors


def get_manifold(points, method='lle',
                 n_neighbors=10, n_components=2,
                 max_iter=100, n_init=1,
                 init='pca', random_state=0):
    print('Fitting with {method}'.format(method=method))

    if method == 'lle':
        m_points = manifold.LocallyLinearEmbedding(n_neighbors, n_components,
                                                   eigen_solver='dense',
                                                   method='standard',
                                                   random_state=random_state).fit_transform(points)
    elif method == 'ltsa':
        m_points = manifold.LocallyLinearEmbedding(n_neighbors, n_components,
                                                   eigen_solver='dense',
                                                   method='ltsa',
                                                   random_state=random_state).fit_transform(points)
    elif method == 'hessian-lle':
        m_points = manifold.LocallyLinearEmbedding(n_neighbors, n_components,
                                                   eigen_solver='dense',
                                                   method='hessian',
                                                   random_state=random_state).fit_transform(points)
    elif method == 'modified-lle':
        m_points = manifold.LocallyLinearEmbedding(n_neighbors, n_components,
                                                   eigen_solver='dense',
                                                   method='modified',
                                                   random_state=random_state).fit_transform(points)
    elif method == 'isomap':
        m_points = manifold.Isomap(n_neighbors, n_components).fit_transform(points)
    elif method == 'mds':
        m_points = manifold.MDS(n_components, max_iter=max_iter, n_init=n_init,
                                random_state=random_state).fit_transform(points)
    elif method == 'le':
        m_points = manifold.SpectralEmbedding(n_components, n_neighbors=n_neighbors,
                                              random_state=random_state).fit_transform(points)
    elif method == 'tsne':
        m_points = manifold.TSNE(n_components, init=init, random_state=random_state).fit_transform(points)
    else:
        raise ValueError('Unsupported method [%s] ' % method)

    return m_points


def plot_func(func_name, ax=None, cmap=None):
    if ax is None:
        ax = plt.axes(projection='3d', elev=50, azim=-120)

    if cmap is None:
        cmap = 'nipy_spectral'

    points, colors = genPoints(func_name=func_name)
    ax.scatter(points[:, 0], points[:, 1], points[:, 2], c=colors, cmap=cmap)
    ax.view_init(4, -72)


def plot_manifolds(save_path, cmap=None):
    func_names = ['swiss-roll', 's-curve', 'severed-sphere']
    labels = ['Swiss Roll', 'S Curve', 'Severed Sphere']

    fig = plt.figure(figsize=(6, 2))
    for i, (func_name, label) in enumerate(zip(func_names, labels)):
        points, colors = genPoints(func_name=func_name)

        ax = fig.add_subplot(1, 3, 1 + i, projection='3d')
        ax.scatter(points[:, 0], points[:, 1], points[:, 2], s=2, c=colors, cmap=cmap)
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_zticklabels([])
        ax.view_init(4, -72)
        ax.dist = 8
        plt.title(label)

    fig.tight_layout()
    fig.show()
    fig.savefig(save_path)


def plot_manifold_dim_reduction(func_name, save_path, cmap=None):
    methods = ['mds', 'isomap', 'lle', 'hessian-lle', 'modified-lle', 'ltsa', 'le', 'tsne']
    labels = ['MDS', 'Isomap', 'LLE', 'Hessian LLE', 'Modified LLE', 'LTSA', 'Laplacian Eigenmaps', 't-SNE']
    points, colors = genPoints(func_name=func_name)

    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(3, 3, 1, projection='3d')
    ax.scatter(points[:, 0], points[:, 1], points[:, 2], s=2, c=colors, cmap=cmap)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_zticklabels([])
    ax.view_init(4, -72)
    ax.dist = 8

    for i, (method, label) in enumerate(zip(methods, labels)):
        t_start = time()
        m_points = get_manifold(points, method=method)
        t_end = time()

        ax = fig.add_subplot(3, 3, 2 + i)
        plt.scatter(m_points[:, 0], m_points[:, 1], c=colors, cmap=cmap)
        plt.title("%s\n(in %.2g sec.)" % (label, t_end - t_start))
        ax.xaxis.set_major_formatter(NullFormatter())
        ax.yaxis.set_major_formatter(NullFormatter())

    fig.tight_layout()
    fig.show()
    fig.savefig(save_path)


def plot_mnist_manifold_dim_reduction(save_path, cmap=None):
    methods = ['mds', 'isomap', 'lle', 'hessian-lle', 'modified-lle', 'ltsa', 'le', 'tsne']
    labels = ['MDS', 'Isomap', 'LLE', 'Hessian LLE', 'Modified LLE', 'LTSA', 'Laplacian Eigenmaps', 't-SNE']
    mnist = datasets.load_digits(n_class=10)
    points = mnist.data
    colors = mnist.target

    fig = plt.figure(figsize=(6, 6))

    for i, (method, label) in enumerate(zip(methods, labels)):
        t_start = time()
        m_points = get_manifold(points, method=method)
        t_end = time()

        ax = fig.add_subplot(3, 3, 2 + i)
        plt.scatter(m_points[:, 0], m_points[:, 1], c=colors, cmap=cmap)
        plt.title("%s\n(in %.2g sec.)" % (label, t_end - t_start))
        ax.xaxis.set_major_formatter(NullFormatter())
        ax.yaxis.set_major_formatter(NullFormatter())

    fig.tight_layout()
    fig.show()
    fig.savefig(save_path)


def plot_mnist_t_sne(save_path, cmap=None):
    mnist = datasets.load_digits(n_class=10)
    points = mnist.data
    colors = mnist.target

    fig = plt.figure(figsize=(4, 4))
    ax = fig.subplots()

    m_points = manifold.TSNE(n_components=2, init='pca', random_state=0).fit_transform(points)
    plt.scatter(m_points[:, 0], m_points[:, 1], c='white')
    for i in range(points.shape[0]):
        plt.text(m_points[i, 0], m_points[i, 1], str(int(colors[i])),
                 color=cmap(colors[i] / 10.))

    ax.axis('off')
    fig.tight_layout()
    fig.show()
    fig.savefig(save_path)


def plot_isomap(save_path, cmap=None):
    points, colors = genPoints(func_name='swiss-roll')
    points_min = np.min(points, 0)
    points_max = np.max(points, 0)
    start_base_point = [4./5., 2./3., 4./5.] * (points_max - points_min) + points_min
    end_base_point = [1./2., 1./3., 3./5.] * (points_max - points_min) + points_min
    start_point_idx = np.sum(np.power(points - start_base_point, 2), 1).argmin()
    end_point_idx = np.sum(np.power(points - end_base_point, 2), 1).argmin()

    n_neighbors = 10

    nbrs = neighbors.NearestNeighbors(n_neighbors=n_neighbors)
    nbrs.fit(points)

    kng = neighbors.kneighbors_graph(nbrs, n_neighbors, mode='distance')
    _, predecessors = shortest_path(kng, method='auto', directed=False, return_predecessors=True)
    path = []
    current = end_point_idx
    while current != start_point_idx:
        path.append(current)
        current = predecessors[start_point_idx, current]
    path.append(start_point_idx)
    path = path[::-1]

    fig = plt.figure(figsize=(6, 2))

    ax = fig.add_subplot(1, 3, 1, projection='3d')
    ax.scatter(points[:, 0], points[:, 1], points[:, 2], s=2, c='gray')
    ax.scatter(points[[start_point_idx, end_point_idx], 0],
               points[[start_point_idx, end_point_idx], 1],
               points[[start_point_idx, end_point_idx], 2],
               s=10, c='blue')
    ax.plot(points[[start_point_idx, end_point_idx], 0],
            points[[start_point_idx, end_point_idx], 1],
            points[[start_point_idx, end_point_idx], 2],
            c='blue', linewidth=1)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_zticklabels([])
    ax.view_init(4, -72)
    ax.dist = 7

    ax = fig.add_subplot(1, 3, 2, projection='3d')
    ax.scatter(points[:, 0], points[:, 1], points[:, 2], s=2, c='gray')

    connections = kng.tocoo()
    distance_mean = np.mean(connections.data)
    distance_std = np.std(connections.data)
    for from_idx, to_idx, distance in zip(connections.row, connections.col, connections.data):
        if distance < distance_mean + 3 * distance_std:
            ax.plot(points[[from_idx, to_idx], 0],
                    points[[from_idx, to_idx], 1],
                    points[[from_idx, to_idx], 2],
                    c='gray', linewidth=0.1)

    for from_idx, to_idx in zip(path[:-1], path[1:]):
        ax.plot(points[[from_idx, to_idx], 0],
                points[[from_idx, to_idx], 1],
                points[[from_idx, to_idx], 2],
                c='red', linewidth=1)

    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_zticklabels([])
    ax.view_init(4, -72)
    ax.dist = 7

    ax = fig.add_subplot(1, 3, 3)
    m_points = manifold.Isomap(n_neighbors, 2).fit_transform(points)
    ax.scatter(m_points[:, 0], m_points[:, 1], s=2, c='gray')
    for from_idx, to_idx, distance in zip(connections.row, connections.col, connections.data):
        if distance < distance_mean + 3 * distance_std:
            ax.plot(m_points[[from_idx, to_idx], 0],
                    m_points[[from_idx, to_idx], 1],
                    c='gray', linewidth=0.1)

    ax.plot(m_points[[start_point_idx, end_point_idx], 0],
            m_points[[start_point_idx, end_point_idx], 1],
            c='blue', linewidth=1)

    for from_idx, to_idx in zip(path[:-1], path[1:]):
        ax.plot(m_points[[from_idx, to_idx], 0],
                m_points[[from_idx, to_idx], 1],
                c='red', linewidth=1)

    ax.xaxis.set_major_formatter(NullFormatter())
    ax.yaxis.set_major_formatter(NullFormatter())

    fig.tight_layout()
    fig.show()
    fig.savefig(save_path)


if __name__ == '__main__':
    plot_manifolds('manifold-examples.png', cmap=plt.cm.Spectral)

    plot_manifold_dim_reduction('swiss-roll', 'swiss-roll.png', cmap=plt.cm.Spectral)
    plot_manifold_dim_reduction('s-curve', 's-curve.png', cmap=plt.cm.Spectral)
    plot_manifold_dim_reduction('severed-sphere', 'severed-sphere.png', cmap=plt.cm.Spectral)

    plot_isomap('swiss-roll-isomap.png', cmap=plt.cm.Spectral)

    plot_mnist_t_sne('mnist-t-sne.png', cmap=plt.cm.tab10)
