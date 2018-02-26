#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Mr. Black on 2018-02-06

import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets

def BGD(x, y, lr=1e-2, epochs=100):
    m = x.shape[0]
    theta = np.ones(x.shape[1])
    J_history = []
    x_transpose = x.transpose()

    hypothesis = np.dot(x, theta)
    loss = y - hypothesis
    J = np.sum(loss ** 2) / (2 * m)
    J_history.append(J)

    for epoch in range(epochs):
        hypothesis = np.dot(x, theta)
        loss = y - hypothesis
        J = np.sum(loss**2) / (2 * m)
        J_history.append(J)

        gradient = np.dot(x_transpose, loss) / m
        theta += lr * gradient

    return (theta, J_history)


def SGD(x, y, lr=1e-2, epochs=100):
    m = x.shape[0]
    theta = np.ones(x.shape[1])
    J_history = []

    hypothesis = np.dot(x, theta)
    loss = y - hypothesis
    J = np.sum(loss ** 2) / (2 * m)
    J_history.append(J)

    for epoch in range(epochs):
        indices = np.random.permutation(y.shape[0])
        x, y = x[indices], y[indices]

        for index in indices:
            hypothesis = np.dot(x[index], theta)
            loss = y[index] - hypothesis
            gradient = np.dot(x[index].transpose(), loss)
            theta += lr * gradient

        hypothesis = np.dot(x, theta)
        loss = y - hypothesis
        J = np.sum(loss**2) / (2 * m)
        J_history.append(J)

    return (theta, J_history)


def MBGD(x, y, batch_size=10, lr=1e-2, epochs=100):
    m = x.shape[0]
    theta = np.ones(x.shape[1])
    J_history = []

    hypothesis = np.dot(x, theta)
    loss = y - hypothesis
    J = np.sum(loss ** 2) / (2 * m)
    J_history.append(J)

    for epoch in range(epochs):
        indices = np.random.permutation(y.shape[0])
        x, y = x[indices], y[indices]
        indices_batches = np.array_split(range(y.shape[0]), batch_size)

        for indices_batch in indices_batches:
            hypothesis = np.dot(x[indices_batch], theta)
            loss = y[indices_batch] - hypothesis
            gradient = np.dot(x[indices_batch].transpose(), loss) / batch_size
            theta += lr * gradient

        hypothesis = np.dot(x, theta)
        loss = y - hypothesis
        J = np.sum(loss**2) / (2 * m)
        J_history.append(J)

    return (theta, J_history)


if __name__ == '__main__':
    x, y = datasets.make_regression(n_samples=100, n_features=1, n_informative=1,
                                    random_state=0, noise=35)
    lr = 1e-3
    epochs = 100
    batch_size = 10

    bgd_theta, bdg_J_history = BGD(x, y, lr=lr, epochs=epochs)
    sgd_theta, sgd_J_history = SGD(x, y, lr=lr, epochs=epochs)
    mbgd_theta, mbgd_J_history = MBGD(x, y, batch_size=batch_size, lr=lr, epochs=epochs)

    fig = plt.figure(figsize=(4, 3))
    ax = fig.subplots()
    plt.plot(bdg_J_history, label='BGD')
    plt.plot(sgd_J_history, label='SGD')
    plt.plot(sgd_J_history, label='MBGD')
    plt.legend(loc='best')
    plt.show()
