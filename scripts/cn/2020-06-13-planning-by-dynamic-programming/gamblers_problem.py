#!/usr/bin/env python
# -*- coding: utf-8 -*-

#######################################################################
# Copyright (C)                                                       #
# 2016-2018 Shangtong Zhang(zhangshangtong.cpp@gmail.com)             #
# 2016 Kenta Shimada(hyperkentakun@gmail.com)                         #
# 2020 Leo Van (leo-van@hotmail.com)                                  #
# Permission given to modify the code as long as you keep this        #
# declaration at the top                                              #
#######################################################################

import numpy as np
import matplotlib.pyplot as plt

from matplotlib import rcParams

rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Source Han Sans CN']


class GamblersProblemValueIteration(object):
    def __init__(self, goal=100, head_prob=0.4, delta=1e-9):
        super(GamblersProblemValueIteration, self).__init__()

        self._GOAL = goal
        self._HEAD_PROB = head_prob
        self._DELTA = delta

        self._states = np.arange(goal + 1)
        self._state_values = np.zeros(goal + 1)
        self._state_values[goal] = 1.0
        self._policy = np.zeros(goal + 1)
        self._state_values_history = []

    def value_iteration(self):
        while True:
            old_states_values = np.copy(self._state_values)
            self._state_values_history.append(old_states_values)

            for state in self._states[1:self._GOAL]:
                actions = np.arange(min(state, self._GOAL - state) + 1)
                action_returns = [
                    self._HEAD_PROB * self._state_values[state + action] +
                    (1 - self._HEAD_PROB) * self._state_values[state - action] for action in actions]
                new_value = np.max(action_returns)
                self._state_values[state] = new_value

            values_difference = np.abs(self._state_values - old_states_values).max()
            print(f'Values difference: {values_difference}')

            if values_difference < self._DELTA:
                self._state_values_history.append(self._state_values)
                break

    def optimal_policy(self):
        for state in self._states[1:self._GOAL]:
            actions = np.arange(min(state, self._GOAL - state) + 1)
            action_returns = [
                self._HEAD_PROB * self._state_values[state + action] +
                (1 - self._HEAD_PROB) * self._state_values[state - action] for action in actions]
            self._policy[state] = actions[np.argmax(np.round(action_returns[1:], 5)) + 1]

    def plot_state_values_history(self, figure_filename='gamblers-problem-value-iteration.png'):
        plt.figure(figsize=(4, 3))
        labels = {
            1: '遍历 1',
            2: '遍历 2',
            3: '遍历 3',
            32: '遍历 32',
            (len(self._state_values_history) - 1): '最终价值函数'
        }

        for idx, state_value in enumerate(self._state_values_history):
            if idx in labels:
                plt.plot(state_value, label=labels[idx])
            elif idx > 0:
                plt.plot(state_value)

        plt.xlabel('赌资')
        plt.ylabel('价值估计')
        plt.legend(loc='best')

        plt.tight_layout()
        plt.savefig(figure_filename, dpi=100)
        plt.close()

    def plot_optimal_policy(self, figure_filename='gamblers-problem-optimal-policy.png'):
        states, policy_ = [], []

        for state, policy in zip(self._states, self._policy):
            states.append(state - 0.5)
            policy_.append(policy)
            states.append(state + 0.5)
            policy_.append(policy)

        plt.figure(figsize=(4, 2.5))
        plt.plot(states, policy_)
        plt.xlabel('赌资')
        plt.ylabel('最后策略（赌注）')

        plt.tight_layout()
        plt.savefig(figure_filename, dpi=100)
        plt.close()


if __name__ == '__main__':
    solver = GamblersProblemValueIteration()
    solver.value_iteration()
    solver.optimal_policy()
    solver.plot_state_values_history()
    solver.plot_optimal_policy()
