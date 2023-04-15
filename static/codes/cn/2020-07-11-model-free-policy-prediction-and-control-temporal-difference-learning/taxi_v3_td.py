#!/usr/bin/env python
# -*- coding: utf-8 -*-

# %%
import os
import gym
import numpy as np
import matplotlib.pyplot as plt

from collections import defaultdict, deque
from tqdm import trange

from matplotlib import rcParams

rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Source Han Sans CN']
rcParams['font.size'] = 14
rcParams['mathtext.fontset'] = 'cm'


# %%
class TaxiV3Agent(object):
    def __init__(
        self,
        algorithm='q_learning',
        num_actions=6,
        alpha=0.3,
        gamma=0.8,
        epsilon=0.9,
        epsilon_decay=0.9,
        epsilon_min=0.01
    ):
        if algorithm not in ['q_learning', 'sarsa', 'expected_sarsa']:
            raise ValueError('Unsupported algorithm [{}]'.format(algorithm))

        self._algorithm = algorithm
        self._num_actions = num_actions
        self._alpha = alpha
        self._gamma = gamma
        self._epsilon = epsilon
        self._epsilon_decay = epsilon_decay
        self._epsilon_min = epsilon_min

        self._env = gym.make('Taxi-v3')
        self._q_table = defaultdict(lambda: np.zeros(self._num_actions))

    def update_epsilon(self):
        self._epsilon = max(self._epsilon * self._epsilon_decay, self._epsilon_min)

    def best_action(self, state):
        return np.argmax(self._q_table[state])

    def epsilon_greedy_action(self, state):
        if np.random.random() > self._epsilon:
            return self.best_action(state)
        else:
            return np.random.randint(0, self._num_actions)

    def step(self, state, action, reward, next_state, done):
        if self._algorithm == 'q_learning':
            self.step_q_learning(state, action, reward, next_state, done)
        elif self._algorithm == 'sarsa':
            self.step_sarsa(state, action, reward, next_state, done)
        elif self._algorithm == 'expected_sarsa':
            self.step_expected_sarsa(state, action, reward, next_state, done)
        else:
            raise ValueError('Unsupported algorithm [{}]'.format(self._algorithm))

    def step_q_learning(self, state, action, reward, next_state, done):
        if not done:
            self._q_table[state][action] += self._alpha * (
                reward + self._gamma * np.max(self._q_table[next_state]) - self._q_table[state][action])
        else:
            self._q_table[state][action] += self._alpha * (reward - self._q_table[state][action])
            self.update_epsilon()

    @staticmethod
    def action_probs(action_values, epsilon, num_actions):
        probs = np.ones(num_actions) * epsilon / num_actions
        best_action = np.argmax(action_values)
        probs[best_action] = 1 - epsilon + (epsilon / num_actions)

        return probs

    def step_sarsa(self, state, action, reward, next_state, done):
        if not done:
            probs = self.action_probs(self._q_table[next_state], self._epsilon, self._num_actions)
            next_action = np.argmax(np.cumsum(probs) > np.random.random())
            self._q_table[state][action] += self._alpha * (
                reward + self._gamma * self._q_table[next_state][next_action] - self._q_table[state][action])
        else:
            self._q_table[state][action] += self._alpha * (reward - self._q_table[state][action])
            self.update_epsilon()

    def step_expected_sarsa(self, state, action, reward, next_state, done):
        if not done:
            probs = self.action_probs(self._q_table[next_state], self._epsilon, self._num_actions)
            self._q_table[state][action] += self._alpha * (
                reward + self._gamma * np.dot(probs, self._q_table[next_state] - self._q_table[state][action]))
        else:
            self._q_table[state][action] += self._alpha * (reward - self._q_table[state][action])
            self.update_epsilon()

    def train(self, num_episodes=20000, rewards_window=100):
        avg_rewards = deque(maxlen=num_episodes)
        best_avg_reward = -np.inf
        sampled_rewards = deque(maxlen=rewards_window)

        for episode in trange(1, num_episodes + 1):
            state = self._env.reset()
            sampled_reward = 0

            while True:
                action = self.epsilon_greedy_action(state)
                next_state, reward, done, _ = self._env.step(action)
                self.step(state, action, reward, next_state, done)
                sampled_reward += reward
                state = next_state

                if done:
                    sampled_rewards.append(sampled_reward)
                    break

            if episode >= rewards_window:
                avg_reward = np.mean(sampled_rewards)
                avg_rewards.append(avg_reward)

                if avg_reward > best_avg_reward:
                    best_avg_reward = avg_reward

        return avg_rewards, best_avg_reward

    def evaluate(self, max_steps=100):
        state = self._env.reset()
        done = False
        steps = 0
        total_reward = 0

        os.system('clear')
        self._env.render()

        while not done and steps < max_steps:
            steps += 1
            action = self.best_action(state)
            new_state, reward, done, _ = self._env.step(action)
            total_reward += reward
            state = new_state

            os.system('clear')
            self._env.render()

        return total_reward, steps


def plot_avg_rewards(avg_rewards_lst, algorithms, max_episode=1000):
    fig = plt.figure(figsize=(6, 4))

    for avg_rewards, algorithm in zip(avg_rewards_lst, algorithms):
        plt.plot(list(range(max_episode)), list(avg_rewards)[0:max_episode], label=algorithm)

    plt.xlabel('幕')
    plt.ylabel('回报')
    plt.legend(loc='lower right')

    fig.tight_layout()
    fig.savefig('taxi-v3-rewards.png', dpi=75)


# %%
if __name__ == '__main__':
    print('Q-learning')
    agent_q_learning = TaxiV3Agent(algorithm='q_learning')
    avg_rewards_q_learning, best_avg_reward_q_learning = agent_q_learning.train()
    print('Best Average Reward: {}'.format(best_avg_reward_q_learning))

    print('Sarsa')
    agent_sarsa = TaxiV3Agent(algorithm='sarsa')
    avg_rewards_sarsa, best_avg_reward_sarsa = agent_sarsa.train()
    print('Best Average Reward: {}'.format(best_avg_reward_sarsa))

    print('Expected Sarsa')
    agent_expected_sarsa = TaxiV3Agent(algorithm='expected_sarsa')
    avg_rewards_expected_sarsa, best_avg_reward_expected_sarsa = agent_expected_sarsa.train()
    print('Best Average Reward: '.format(best_avg_reward_expected_sarsa))

    plot_avg_rewards(
        [avg_rewards_q_learning, avg_rewards_sarsa, avg_rewards_expected_sarsa],
        ['Q-learning', 'Sarsa', 'Expected Sarsa'])
