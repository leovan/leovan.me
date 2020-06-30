#!/usr/bin/env python
# -*- coding: utf-8 -*-

#######################################################################
# Copyright (C)                                                       #
# 2020 Leo Van (leo-van@hotmail.com)                                  #
# 2016 Shangtong Zhang(zhangshangtong.cpp@gmail.com)                  #
# 2016 Kenta Shimada(hyperkentakun@gmail.com)                         #
# 2017 Aja Rangaswamy (aja004@gmail.com)                              #
# Permission given to modify the code as long as you keep this        #
# declaration at the top                                              #
#######################################################################

import time
import pickle
import itertools
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import multiprocessing as mp

from functools import partial
from scipy.stats import poisson

from matplotlib import rcParams

rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Source Han Sans CN']


# maximum # of cars in each location
MAX_CARS = 20

# maximum # of cars to move during night
MAX_MOVE_OF_CARS = 5

# expectation for rental requests in first location
RENTAL_REQUEST_FIRST_LOC = 3

# expectation for rental requests in second location
RENTAL_REQUEST_SECOND_LOC = 4

# expectation for # of cars returned in first location
RETURNS_FIRST_LOC = 3

# expectation for # of cars returned in second location
RETURNS_SECOND_LOC = 2

# discount
DISCOUNT = 0.9

# reward earned by a car
RENT_REWARD = 10

# cost of moving a car
MOVE_CAR_COST = -2

# An up bound for poisson distribution
# If n is greater than this value, then the probability of getting n is truncated to 0
POISSON_UPPER_BOUND = 11

# Probability for poisson distribution
# @lam: lambda should be less than 10 for this function
poisson_cache = dict()


def poisson_distribution(n, lam):
    global poisson_cache

    key = n * 10 + lam
    if key not in poisson_cache:
        poisson_cache[key] = poisson.pmf(n, lam)

    return poisson_cache[key]


class CarRentalPolicyIteration(object):
    def __init__(self, truncate=9, delta=1e-1, gamma=0.9, n_jobs=-1):
        super(CarRentalPolicyIteration, self).__init__()

        self._TRUNCATE = truncate
        self._DELTA = delta
        self._GAMMA = gamma

        if n_jobs <= 0:
            self._N_JOBS = mp.cpu_count()
        else:
            self._N_JOBS = n_jobs

        self._actions = np.arange(-MAX_MOVE_OF_CARS, MAX_MOVE_OF_CARS + 1)
        self._inverse_actions = {elem: idx[0] for idx, elem in np.ndenumerate(self._actions)}
        self._values = np.zeros((MAX_CARS + 1, MAX_CARS + 1))
        self._policy = np.zeros(self._values.shape, dtype=np.int)

        self._policy_history = [np.copy(self._policy)]

    def solve(self):
        iterations = 0
        total_start_time = time.time()

        while True:
            start_time = time.time()
            self._values = self.policy_evaluation(self._policy, self._values)
            elapsed_time = time.time() - start_time
            print(f'Policy evaluation elapsed time: {elapsed_time} seconds.')

            start_time = time.time()
            policy_change, self._policy = self.policy_improvement(self._policy, self._values, self._actions)
            elapsed_time = time.time() - start_time
            print(f'Policy improvement elapsed time: {elapsed_time} seconds.')

            self._policy_history.append(np.copy(self._policy))

            if policy_change == 0:
                break

            iterations += 1

        total_elapsed_time = time.time() - total_start_time
        print(f'Optimal policy is reached after {iterations} iterations in {total_elapsed_time} seconds.')

        with open('car-rental-policy-history.pkl', 'wb') as f:
            pickle.dump(self._policy_history, f)

        with open('car-rental-optimal-values.pkl', 'wb') as f:
            pickle.dump(self._values, f)

    def policy_evaluation(self, policy, values):
        while True:
            new_values = np.copy(values)
            k = np.arange(MAX_CARS + 1)
            all_states = ((i, j) for i, j in itertools.product(k, k))

            results = []
            with mp.Pool(processes=self._N_JOBS) as p:
                cook = partial(self.expected_return_policy_evaluation, policy, values)
                results = p.map(cook, all_states)

            for v, i, j in results:
                new_values[i, j] = v

            values_difference = np.abs(new_values - values).sum()
            print(f'Values difference: {values_difference}')

            values = new_values
            if values_difference < self._DELTA:
                print('Values are converged.')
                return values

    def policy_improvement(self, policy, values, actions):
        new_policy = np.copy(policy)
        expected_action_returns = np.zeros((MAX_CARS + 1, MAX_CARS + 1, np.size(actions)))
        cooks = dict()

        with mp.Pool(processes=self._N_JOBS) as p:
            for action in actions:
                k = np.arange(MAX_CARS + 1)
                all_states = ((i, j) for i, j in itertools.product(k, k))
                cooks[action] = partial(self.expected_return_policy_improvement, action, values)
                results = p.map(cooks[action], all_states)

                for v, i, j, a in results:
                    expected_action_returns[i, j, self._inverse_actions[a]] = v

        for i in range(expected_action_returns.shape[0]):
            for j in range(expected_action_returns.shape[1]):
                new_policy[i, j] = actions[np.argmax(expected_action_returns[i, j])]

        policy_change = (new_policy != policy).sum()
        print(f'Policy changed in {policy_change} states.')

        return policy_change, new_policy

    def bellman(self, values, action, state, constant_returned_cars=False):
        expected_return = 0
        expected_return += MOVE_CAR_COST * abs(action)

        for rental_request_first_loc in range(self._TRUNCATE):
            for rental_request_second_loc in range(self._TRUNCATE):

                num_of_cars_first_loc = int(min(state[0] - action, MAX_CARS))
                num_of_cars_second_loc = int(min(state[1] + action, MAX_CARS))

                real_rental_first_loc = min(num_of_cars_first_loc, rental_request_first_loc)
                real_rental_second_loc = min(num_of_cars_second_loc, rental_request_second_loc)

                reward = (real_rental_first_loc + real_rental_second_loc) * RENT_REWARD
                num_of_cars_first_loc -= real_rental_first_loc
                num_of_cars_second_loc -= real_rental_second_loc

                prob_rental = poisson_distribution(rental_request_first_loc, RENTAL_REQUEST_FIRST_LOC) * \
                    poisson_distribution(rental_request_second_loc, RENTAL_REQUEST_SECOND_LOC)

                if constant_returned_cars:
                    returned_cars_first_loc = RETURNS_FIRST_LOC
                    returned_cars_second_loc = RETURNS_SECOND_LOC
                    num_of_cars_first_loc = min(num_of_cars_first_loc + returned_cars_first_loc, MAX_CARS)
                    num_of_cars_second_loc = min(num_of_cars_second_loc + returned_cars_second_loc, MAX_CARS)
                    expected_return += prob_rental * \
                        (reward + DISCOUNT * values[num_of_cars_first_loc, num_of_cars_second_loc])
                else:
                    for returned_cars_first_loc in range(self._TRUNCATE):
                        for returned_cars_second_loc in range(self._TRUNCATE):
                            prob_return = poisson_distribution(returned_cars_first_loc, RETURNS_FIRST_LOC) * \
                                poisson_distribution(returned_cars_second_loc, RETURNS_SECOND_LOC)

                            num_of_cars_first_loc_ = min(num_of_cars_first_loc + returned_cars_first_loc, MAX_CARS)
                            num_of_cars_second_loc_ = min(num_of_cars_second_loc + returned_cars_second_loc, MAX_CARS)

                            expected_return += prob_return * prob_rental * \
                                (reward + DISCOUNT * values[num_of_cars_first_loc_, num_of_cars_second_loc_])

        return expected_return

    def expected_return_policy_evaluation(self, policy, values, state):
        action = policy[state[0], state[1]]
        expected_return = self.bellman(values, action, state)
        return expected_return, state[0], state[1]

    def expected_return_policy_improvement(self, action, values, state):
        if not ((state[0] >= action >= 0) or (state[1] >= -action > 0)):
            return -float('inf'), state[0], state[1], action

        expected_return = self.bellman(values, action, state)
        return expected_return, state[0], state[1], action

    @classmethod
    def plot_policy_history(cls, policy_history, values, figure_filename='car-rental-policy-history.png'):
        _, axes = plt.subplots(3, 2, figsize=(8, 10))
        axes = axes.flatten()

        for idx, policy in enumerate(policy_history[:5]):
            fig = sns.heatmap(np.flipud(policy), cmap='YlGnBu', ax=axes[idx])
            fig.set_yticklabels(fig.get_yticklabels()[::-1])
            fig.set_ylabel('地点 1 汽车数量')
            fig.set_xlabel('地点 2 汽车数量')
            fig.set_title(f'策略 {idx}')

        fig = sns.heatmap(np.flipud(values), cmap='YlGnBu', ax=axes[-1])
        fig.set_yticklabels(fig.get_yticklabels()[::-1])
        fig.set_ylabel('地点 1 汽车数量')
        fig.set_xlabel('地点 2 汽车数量')
        fig.set_title('最优值')

        plt.tight_layout()
        plt.savefig(figure_filename, dpi=100)
        plt.close()


if __name__ == '__main__':
    solver = CarRentalPolicyIteration()
    solver.solve()

    with open('car-rental-policy-history.pkl', 'rb') as f:
        policy_history = pickle.load(f)

    with open('car-rental-optimal-values.pkl', 'rb') as f:
        optimal_values = pickle.load(f)

    solver.plot_policy_history(policy_history, optimal_values)
