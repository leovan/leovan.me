#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Mr. Black on 2018-02-05

from itertools import zip_longest
import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from matplotlib.colors import LogNorm
from matplotlib import animation
from IPython.display import HTML

from optimizers import *


def get_beales_optimizers(d_func, base_lr=1e-3):
    optimizers = []
    methods = []

    # SGD
    sgd_optimizer = SGD(d_func=d_func, lr=base_lr/2)
    optimizers.append(sgd_optimizer)
    methods.append('SGD')

    # Momentum
    momentum_optimizer = SGD(d_func=d_func, momentum=0.9, lr=base_lr/2)
    optimizers.append(momentum_optimizer)
    methods.append('Momentum')

    # NAG
    nag_optimizer = SGD(d_func=d_func, momentum=0.9, nesterov=True, lr=base_lr/2)
    optimizers.append(nag_optimizer)
    methods.append('NAG')

    # Adagrad
    adagrad_optimizer = Adagard(d_func=d_func, lr=base_lr*20)
    optimizers.append(adagrad_optimizer)
    methods.append('Adagrad')

    # Adadelta
    adadelta_optimizer = Adadelta(d_func=d_func)
    optimizers.append(adadelta_optimizer)
    methods.append('Adadelta')

    # RMSprop
    rmsprop_optimizer = RMSprop(d_func=d_func, lr=base_lr*20)
    optimizers.append(rmsprop_optimizer)
    methods.append("RMSprop")

    # Adam
    adam_optimizer = Adam(d_func=d_func, lr=base_lr*20)
    optimizers.append(adam_optimizer)
    methods.append("Adam")

    # Adamax
    adamax_optimizer = Adamax(d_func=d_func, lr=base_lr*20)
    optimizers.append(adamax_optimizer)
    methods.append("Adamax")

    # Nadam
    nadam_optimizer = Nadam(d_func=d_func, lr=base_lr*20)
    optimizers.append(nadam_optimizer)
    methods.append("Nadam")

    # AMSGrad
    amsgrad_optimizer = Adam(d_func=d_func, lr=base_lr*20, amsgrad=True)
    optimizers.append(amsgrad_optimizer)
    methods.append("AMSGrad")

    return (optimizers, methods)


def get_saddle_optimizers(d_func, base_lr=1e-3):
    optimizers = []
    methods = []

    # SGD
    sgd_optimizer = SGD(d_func=d_func, lr=base_lr*10)
    optimizers.append(sgd_optimizer)
    methods.append('SGD')

    # Momentum
    momentum_optimizer = SGD(d_func=d_func, momentum=0.9, lr=base_lr*10)
    optimizers.append(momentum_optimizer)
    methods.append('Momentum')

    # NAG
    nag_optimizer = SGD(d_func=d_func, momentum=0.9, nesterov=True, lr=base_lr*10)
    optimizers.append(nag_optimizer)
    methods.append('NAG')

    # Adagrad
    adagrad_optimizer = Adagard(d_func=d_func, lr=base_lr*20)
    optimizers.append(adagrad_optimizer)
    methods.append('Adagrad')

    # Adadelta
    adadelta_optimizer = Adadelta(d_func=d_func)
    optimizers.append(adadelta_optimizer)
    methods.append('Adadelta')

    # RMSprop
    rmsprop_optimizer = RMSprop(d_func=d_func, lr=base_lr*20)
    optimizers.append(rmsprop_optimizer)
    methods.append("RMSprop")

    # Adam
    adam_optimizer = Adam(d_func=d_func, lr=base_lr*20)
    optimizers.append(adam_optimizer)
    methods.append("Adam")

    # Adamax
    adamax_optimizer = Adamax(d_func=d_func, lr=base_lr*20)
    optimizers.append(adamax_optimizer)
    methods.append("Adamax")

    # Nadam
    nadam_optimizer = Nadam(d_func=d_func, lr=base_lr*20)
    optimizers.append(nadam_optimizer)
    methods.append("Nadam")

    # AMSGrad
    amsgrad_optimizer = Adam(d_func=d_func, lr=base_lr*20, amsgrad=True)
    optimizers.append(amsgrad_optimizer)
    methods.append("AMSGrad")

    return (optimizers, methods)


class TrajectoryAnimation2D(animation.FuncAnimation):

    def __init__(self, *paths, labels=[], fig=None, ax=None, steps=1, frames=None,
                 interval=60, repeat_delay=5, blit=True, **kwargs):

        if fig is None:
            if ax is None:
                fig, ax = plt.subplots()
            else:
                fig = ax.get_figure()
        else:
            if ax is None:
                ax = fig.gca()

        self.fig = fig
        self.ax = ax

        self.paths = paths

        self.steps = steps

        if frames is None:
            frames = int(max(path.shape[1] for path in paths) / steps)

        self.lines = [ax.plot([], [], label=label, lw=2)[0]
                      for _, label in zip_longest(paths, labels)]
        self.points = [ax.plot([], [], 'o', color=line.get_color())[0]
                       for line in self.lines]

        super(TrajectoryAnimation2D, self).__init__(fig, self.animate, init_func=self.init_anim,
                                                    frames=frames, interval=interval, blit=blit,
                                                    repeat_delay=repeat_delay, **kwargs)

    def init_anim(self):
        for line, point in zip(self.lines, self.points):
            line.set_data([], [])
            point.set_data([], [])
        return self.lines + self.points

    def animate(self, i):
        for line, point, path in zip(self.lines, self.points, self.paths):
            line.set_data(*path[::, :i*self.steps])
            point.set_data(*path[::, i*self.steps - 1:i*self.steps])
        return self.lines + self.points


class TrajectoryAnimation3D(animation.FuncAnimation):

    def __init__(self, *paths, z_paths, labels=[], fig=None, ax=None, steps=1, frames=None,
                 interval=60, repeat_delay=5, blit=True, **kwargs):

        if fig is None:
            if ax is None:
                fig, ax = plt.subplots()
            else:
                fig = ax.get_figure()
        else:
            if ax is None:
                ax = fig.gca()

        self.fig = fig
        self.ax = ax

        self.paths = paths
        self.z_paths = z_paths

        self.steps = steps

        if frames is None:
            frames =int(max(path.shape[1] for path in paths) / steps)

        self.lines = [ax.plot([], [], [], label=label, lw=2)[0]
                      for _, label in zip_longest(paths, labels)]
        self.points = [ax.plot([], [], [], 'o', color=line.get_color())[0]
                      for line in self.lines]

        super(TrajectoryAnimation3D, self).__init__(fig, self.animate, init_func=self.init_anim,
                                                    frames=frames, interval=interval, blit=blit,
                                                    repeat_delay=repeat_delay, **kwargs)

    def init_anim(self):
        for line, point in zip(self.lines, self.points):
            line.set_data([], [])
            line.set_3d_properties([])
            point.set_data([], [])
            point.set_3d_properties([])
        return self.lines + self.points


    def animate(self, i):
        for line, point, path, z_paths in zip(self.lines, self.points, self.paths, self.z_paths):
            line.set_data(*path[::, :i*self.steps])
            line.set_3d_properties(z_paths[:i*self.steps])
            point.set_data(*path[::, i*self.steps-1:i*self.steps])
            point.set_3d_properties(z_paths[i*self.steps-1:i*self.steps])
        return self.lines


def beales_2d_plot(x_min=-4.5, x_max=4.5, x_step=0.2,
                   y_min=-4.5, y_max=4.5, y_step=0.2):
    x, y = np.meshgrid(np.arange(x_min, x_max + x_step, x_step),
                       np.arange(y_min, y_max + y_step, y_step))
    z = beales_func([x, y])
    minima_xy = np.array([3, 0.5]).reshape(-1, 1)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.contour(x, y, z, levels=np.logspace(0, 5, 35), norm=LogNorm(), cmap='viridis')
    ax.plot(*minima_xy, 'r*', markersize=10)

    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)

    ax.set_xticks([])
    ax.set_yticks([])

    fig.tight_layout()

    return (fig, ax)


def beales_2d_animation():
    optimizers, methods = get_beales_optimizers(d_func=beales_d_func)

    paths = [np.array(optimizer.get_params_history(np.array([2., 1.7]), 3000)).T
             for optimizer in optimizers]

    fig, ax = beales_2d_plot()
    return TrajectoryAnimation2D(*paths, labels=methods, ax=ax, steps=10)


def beales_3d_plot(x_min=-4.5, x_max=4.5, x_step=0.2,
                   y_min=-4.5, y_max=4.5, y_step=0.2):
    x, y = np.meshgrid(np.arange(x_min, x_max + x_step, x_step),
                       np.arange(y_min, y_max + y_step, y_step))
    z = beales_func([x, y])
    minima_xy = np.array([3, 0.5]).reshape(-1, 1)
    minima_z = beales_func(minima_xy)

    fig = plt.figure(figsize=(8, 6))
    ax = plt.axes(projection='3d', elev=50, azim=-120)
    ax.plot_surface(x, y, z, norm=LogNorm(), rstride=1, cstride=1,
                    edgecolor='none', alpha=0.8, cmap='viridis')
    ax.plot(*minima_xy, minima_z, 'r*', markersize=10)

    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)

    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_zticklabels([])

    fig.tight_layout()

    return (fig, ax)


def beales_3d_animation():
    optimizers, methods = get_beales_optimizers(d_func=beales_d_func)

    paths = [np.array(optimizer.get_params_history(np.array([2., 1.7]), 3000)).T
             for optimizer in optimizers]
    z_paths = [beales_func(path) for path in paths]

    fig, ax = beales_3d_plot()
    return TrajectoryAnimation3D(*paths, z_paths=z_paths, labels=methods, ax=ax, steps=10)


def saddle_3d_plot(x_min=-2, x_max=2, x_step=0.1,
                   y_min=-2, y_max=2, y_step=0.1):
    x, y = np.meshgrid(np.arange(x_min, x_max + x_step, x_step),
                       np.arange(y_min, y_max + y_step, y_step))
    z = saddle_func([x, y])

    fig = plt.figure(figsize=(8, 6))
    ax = plt.axes(projection='3d', elev=50, azim=-50)
    ax.plot_surface(x, y, z, rstride=1, cstride=1,
                    edgecolor='none', alpha=0.8, cmap='viridis')

    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)

    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_zticklabels([])

    fig.tight_layout()

    return (fig, ax)


def saddle_3d_animation():
    optimizers, methods = get_saddle_optimizers(d_func=saddle_d_func)

    paths = [np.array(optimizer.get_params_history(np.array([-0.5, -1e-4]), 300)).T
             for optimizer in optimizers]
    z_paths = [saddle_func(path) for path in paths]

    fig, ax = saddle_3d_plot()
    return TrajectoryAnimation3D(*paths, z_paths=z_paths, labels=methods, ax=ax, steps=1)


if __name__ == '__main__':
    gif_writer = animation.ImageMagickWriter(fps=60)
    mp4_writer = animation.FFMpegWriter(fps=60, bitrate=1800, metadata=dict(artist='Mr. Black'))

    beales_2d_plt, _ = beales_2d_plot()
    beales_2d_plt.show()
    beales_2d_anim = beales_2d_animation()
    beales_2d_anim.ax.legend(loc='upper left', fontsize='xx-large')
    beales_2d_anim.save('beales-2d-anim.gif', writer=gif_writer)
    beales_2d_anim.save('beales-2d-anim.mp4', writer=mp4_writer)

    beales_3d_plt, _ = beales_3d_plot()
    beales_3d_plt.show()
    beales_3d_anim = beales_3d_animation()
    beales_3d_anim.ax.legend(loc='upper left', fontsize='xx-large')
    beales_3d_anim.save('beales-3d-anim.gif', writer=gif_writer)
    beales_3d_anim.save('beales-3d-anim.mp4', writer=mp4_writer)

    saddle_3d_plt, _ = saddle_3d_plot()
    saddle_3d_plt.show()
    saddle_3d_anim = saddle_3d_animation()
    saddle_3d_anim.ax.legend(loc='upper right', fontsize='xx-large')
    saddle_3d_anim.save('saddle-3d-anim.gif', writer=gif_writer)
    saddle_3d_anim.save('saddle-3d-anim.mp4', writer=mp4_writer)
