#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Mr. Black on 2018-02-05

import numpy as np

EPSILON = 1e-7


def beales_func(params):
    x, y = params[0], params[1]

    return (1.5 - x + x*y)**2 + \
           (2.25 - x + x*y**2)**2 + \
           (2.625 - x + x*y**3)**2


def beales_d_func(params):
    x, y = params[0], params[1]

    dx = 2*(x*y**3 - x + 2.625)*(y**3 - 1) + \
         2*(x*y**2 - x + 2.25)*(y**2 - 1) + \
         2*(x*y - x + 1.5)*(y - 1)
    dy = 6*(x*y**3 - x + 2.625)*x*y**2 + \
         4*(x*y**2 - x + 2.25)*x*y + \
         2*(x*y - x + 1.5)*x

    return np.array([dx, dy])


def saddle_func(params):
    x, y = params[0], params[1]

    return x**2 - y**2


def saddle_d_func(params):
    x, y = params[0], params[1]

    return np.array([2*x, -2*y])


class Optimizer():
    def update_params(self, params):
        raise NotImplementedError

    def get_params_history(self, init_params, iters):
        params_history = [init_params]
        params = init_params

        for iter in range(iters):
            params = self.update_params(params)
            params_history.append(params)

        return params_history


class SGD(Optimizer):
    def __init__(self, d_func, lr=1e-3, momentum=0., decay=0., nesterov=False):
        self.iterations = 0
        self.d_func = d_func
        self.lr = lr
        self.momentum = momentum
        self.moments = None
        self.decay = decay
        self.initial_decay = decay
        self.nesterov = nesterov

    def update_params(self, params):
        grads = self.d_func(params)
        self.iterations += 1

        lr = self.lr
        if self.initial_decay > 0:
            lr *= (1. / (1. + self.decay * self.iterations))

        # momentum
        if self.moments is None:
            self.moments = np.zeros(params.shape)

        v = self.momentum * self.moments - lr * grads
        self.moments = v

        if self.nesterov:
            new_params = params + self.momentum * v - lr * grads
        else:
            new_params = params + v

        return new_params


class Adagard(Optimizer):
    def __init__(self, d_func, lr=1e-2, decay=0.):
        self.iterations = 0
        self.d_func = d_func
        self.lr = lr
        self.decay = decay
        self.initial_decay = decay
        self.accumulators = None


    def update_params(self, params):
        grads = self.d_func(params)
        self.iterations += 1

        lr = self.lr
        if self.initial_decay > 0:
            lr *= (1. / (1. + self.decay * self.iterations))

        if self.accumulators is None:
            self.accumulators = np.zeros(params.shape)

        self.accumulators += np.square(grads)
        new_params = params - self.lr * grads / \
                     (np.sqrt(self.accumulators) + EPSILON)

        return new_params


class Adadelta(Optimizer):
    def __init__(self, d_func, lr=1e0, rho=0.95, decay=0.):
        self.iterations = 0
        self.d_func = d_func
        self.lr = lr
        self.rho = rho
        self.decay = decay
        self.initial_decay = decay
        self.accumulators = None
        self.delta_accumulators = None


    def update_params(self, params):
        grads = self.d_func(params)
        self.iterations += 1

        lr = self.lr
        if self.initial_decay > 0:
            lr *= (1. / (1. + self.decay * self.iterations))

        if self.accumulators is None:
            self.accumulators = np.zeros(params.shape)
        if self.delta_accumulators is None:
            self.delta_accumulators = np.zeros(params.shape)

        self.accumulators = self.rho * self.accumulators + \
                            (1. - self.rho) * np.square(grads)

        update = grads * np.sqrt(self.delta_accumulators + EPSILON) / \
                 np.sqrt(self.accumulators + EPSILON)
        new_params = params - self.lr * update

        self.delta_accumulators = self.rho * self.delta_accumulators + \
                                  (1. - self.rho) * np.square(update)

        return new_params


class RMSprop(Optimizer):
    def __init__(self, d_func, lr=1e-3, rho=0.9, decay=0.):
        self.iterations = 0
        self.d_func = d_func
        self.lr = lr
        self.rho = rho
        self.decay = decay
        self.initial_decay = decay
        self.accumulators = None


    def update_params(self, params):
        grads = self.d_func(params)
        self.iterations += 1

        lr = self.lr
        if self.initial_decay > 0:
            lr *= (1. / (1. + self.decay * self.iterations))

        if self.accumulators is None:
            self.accumulators = np.zeros(params.shape)

        self.accumulators = self.rho * self.accumulators + \
                            (1. - self.rho) * np.square(grads)
        new_params = params - self.lr * grads / \
                     (np.sqrt(self.accumulators) + EPSILON)

        return new_params


class Adam(Optimizer):
    def __init__(self, d_func,lr=1e-3, beta_1=0.9, beta_2=0.999, decay=0., amsgrad=False):
        self.iterations = 0
        self.d_func = d_func
        self.lr = lr
        self.beta_1 = beta_1
        self.beta_2 = beta_2
        self.amsgrad = amsgrad
        self.decay = decay
        self.initial_decay = decay
        self.ms = None
        self.vs = None
        self.vhats = None


    def update_params(self, params):
        grads = self.d_func(params)
        self.iterations += 1

        lr = self.lr
        if self.initial_decay > 0:
            lr *= (1. / (1. + self.decay * self.iterations))

        t = self.iterations + 1.
        lr_t = lr * (np.sqrt(1. - np.power(self.beta_2, t)) / (1. - np.power(self.beta_1, t)))

        if self.ms is None:
            self.ms = np.zeros(params.shape)
        if self.vs is None:
            self.vs = np.zeros(params.shape)
        if self.vhats is None:
            if self.amsgrad:
                self.vhats = np.zeros(params.shape)

        self.ms = self.beta_1 * self.ms + (1. - self.beta_1) * grads
        self.vs = self.beta_2 * self.vs + (1. - self.beta_2) * np.square(grads)

        if self.amsgrad:
            self.vhats = np.maximum(self.vhats, self.vs)
            new_params = params - lr_t * self.ms / (np.sqrt(self.vhats) + EPSILON)
        else:
            new_params = params - lr_t * self.ms / (np.sqrt(self.vs) + EPSILON)

        return new_params


class Adamax(Optimizer):
    def __init__(self, d_func,lr=2e-3, beta_1=0.9, beta_2=0.999, decay=0.):
        self.iterations = 0
        self.d_func = d_func
        self.lr = lr
        self.beta_1 = beta_1
        self.beta_2 = beta_2
        self.decay = decay
        self.initial_decay = decay
        self.ms = None
        self.us = None


    def update_params(self, params):
        grads = self.d_func(params)
        self.iterations += 1

        lr = self.lr
        if self.initial_decay > 0:
            lr *= (1. / (1. + self.decay * self.iterations))

        t = self.iterations + 1.
        lr_t = lr * (1. - np.power(self.beta_1, t))

        if self.ms is None:
            self.ms = np.zeros(params.shape)
        if self.us is None:
            self.us = np.zeros(params.shape)

        self.ms = self.beta_1 * self.ms + (1. - self.beta_1) * grads
        self.us = np.maximum(self.beta_2 * self.us, np.abs(grads))

        new_params = params - lr_t * self.ms / (self.us + EPSILON)

        return new_params


class Nadam(Optimizer):
    def __init__(self, d_func,lr=2e-3, beta_1=0.9, beta_2=0.999, schedule_decay=0.004):
        self.iterations = 0
        self.d_func = d_func
        self.m_schedule = 1
        self.lr = lr
        self.beta_1 = beta_1
        self.beta_2 = beta_2
        self.schedule_decay = schedule_decay
        self.ms = None
        self.vs = None


    def update_params(self, params):
        grads = self.d_func(params)
        self.iterations += 1

        t = self.iterations + 1.
        momentum_cache_t = self.beta_1 * (1. - 0.5 * np.power(0.96, t * self.schedule_decay))
        momentum_cache_t_1 = self.beta_1 * (1. - 0.5 * np.power(0.96, (t + 1) * self.schedule_decay))
        m_schedule_new = self.m_schedule * momentum_cache_t
        m_schedule_next = self.m_schedule * momentum_cache_t * momentum_cache_t_1
        self.m_schedule = m_schedule_new

        if self.ms is None:
            self.ms = np.zeros(params.shape)
        if self.vs is None:
            self.vs = np.zeros(params.shape)

        g_prime = grads / (1. - m_schedule_new)
        self.ms = self.beta_1 * self.ms + (1. - self.beta_1) * grads
        ms_prime = self.ms / (1. - m_schedule_next)
        self.vs = self.beta_2 * self.vs + (1. - self.beta_2) * np.square(grads)
        vs_prime = self.vs / (1. - np.power(self.beta_2, t))
        ms_bar = (1. - momentum_cache_t) * g_prime + momentum_cache_t_1 * ms_prime

        new_params = params - self.lr * ms_bar / (np.sqrt(vs_prime) + EPSILON)

        return new_params


if __name__ == '__main__':
    pass
