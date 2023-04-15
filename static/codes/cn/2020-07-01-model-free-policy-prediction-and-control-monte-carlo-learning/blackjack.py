#!/usr/bin/env python
# -*- coding: utf-8 -*-

#######################################################################
# Copyright (C)                                                       #
# 2020 Leo Van (leo-van@hotmail.com)                                  #
# 2016-2018 Shangtong Zhang(zhangshangtong.cpp@gmail.com)             #
# 2016 Kenta Shimada(hyperkentakun@gmail.com)                         #
# Permission given to modify the code as long as you keep this        #
# declaration at the top                                              #
#######################################################################

# %%
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm

from matplotlib import rcParams
from mpl_toolkits.mplot3d import Axes3D

rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Source Han Sans CN']
rcParams['font.size'] = 14
rcParams['mathtext.fontset'] = 'cm'


# %%
# actions: hit or stand
# 动作：拿牌 / 停牌
ACTION_HIT = 0  # 拿牌
ACTION_STAND = 1  # 停牌，"strike" in the book
ACTIONS = [ACTION_HIT, ACTION_STAND]

# policy for player
# 玩家策略
POLICY_PLAYER = np.zeros(22, dtype=np.int)
for i in range(12, 20):
    POLICY_PLAYER[i] = ACTION_HIT
POLICY_PLAYER[20] = ACTION_STAND
POLICY_PLAYER[21] = ACTION_STAND


# function form of target policy of player
def target_policy_player(usable_ace_player, player_sum, dealer_card):
    return POLICY_PLAYER[player_sum]


# function form of behavior policy of player
def behavior_policy_player(usable_ace_player, player_sum, dealer_card):
    if np.random.binomial(1, 0.5) == 1:
        return ACTION_STAND
    return ACTION_HIT


# policy for dealer
# 庄家策略
POLICY_DEALER = np.zeros(22)
for i in range(12, 17):
    POLICY_DEALER[i] = ACTION_HIT
for i in range(17, 22):
    POLICY_DEALER[i] = ACTION_STAND


# get a new card
def get_card():
    card = np.random.randint(1, 14)
    card = min(card, 10)
    return card


# get the value of a card (11 for ace).
def card_value(card_id):
    return 11 if card_id == 1 else card_id


# play a game
# @policy_player: specify policy for player
# @initial_state: [whether player has a usable Ace, sum of player's cards, one card of dealer]
# @initial_action: the initial action
def play(policy_player, initial_state=None, initial_action=None):
    # player status

    # sum of player
    player_sum = 0

    # trajectory of player
    player_trajectory = []

    # whether player uses Ace as 11
    usable_ace_player = False

    # dealer status
    dealer_card1 = 0
    dealer_card2 = 0
    usable_ace_dealer = False

    if initial_state is None:
        # generate a random initial state

        while player_sum < 12:
            # if sum of player is less than 12, always hit
            card = get_card()
            player_sum += card_value(card)

            # If the player's sum is larger than 21, he may hold one or two aces.
            if player_sum > 21:
                assert player_sum == 22
                # last card must be ace
                player_sum -= 10
            else:
                usable_ace_player |= (1 == card)

        # initialize cards of dealer, suppose dealer will show the first card he gets
        dealer_card1 = get_card()
        dealer_card2 = get_card()

    else:
        # use specified initial state
        usable_ace_player, player_sum, dealer_card1 = initial_state
        dealer_card2 = get_card()

    # initial state of the game
    state = [usable_ace_player, player_sum, dealer_card1]

    # initialize dealer's sum
    dealer_sum = card_value(dealer_card1) + card_value(dealer_card2)
    usable_ace_dealer = 1 in (dealer_card1, dealer_card2)
    # if the dealer's sum is larger than 21, he must hold two aces.
    if dealer_sum > 21:
        assert dealer_sum == 22
        # use one Ace as 1 rather than 11
        dealer_sum -= 10
    assert dealer_sum <= 21
    assert player_sum <= 21

    # game starts!

    # player's turn
    while True:
        if initial_action is not None:
            action = initial_action
            initial_action = None
        else:
            # get action based on current sum
            action = policy_player(usable_ace_player, player_sum, dealer_card1)

        # track player's trajectory for importance sampling
        player_trajectory.append([(usable_ace_player, player_sum, dealer_card1), action])

        if action == ACTION_STAND:
            break
        # if hit, get new card
        card = get_card()
        # Keep track of the ace count. the usable_ace_player flag is insufficient alone as it cannot
        # distinguish between having one ace or two.
        ace_count = int(usable_ace_player)
        if card == 1:
            ace_count += 1
        player_sum += card_value(card)
        # If the player has a usable ace, use it as 1 to avoid busting and continue.
        while player_sum > 21 and ace_count:
            player_sum -= 10
            ace_count -= 1
        # player busts
        if player_sum > 21:
            return state, -1, player_trajectory
        assert player_sum <= 21
        usable_ace_player = (ace_count == 1)

    # dealer's turn
    while True:
        # get action based on current sum
        action = POLICY_DEALER[dealer_sum]
        if action == ACTION_STAND:
            break
        # if hit, get a new card
        new_card = get_card()
        ace_count = int(usable_ace_dealer)
        if new_card == 1:
            ace_count += 1
        dealer_sum += card_value(new_card)
        # If the dealer has a usable ace, use it as 1 to avoid busting and continue.
        while dealer_sum > 21 and ace_count:
            dealer_sum -= 10
            ace_count -= 1
        # dealer busts
        if dealer_sum > 21:
            return state, 1, player_trajectory
        usable_ace_dealer = (ace_count == 1)

    # compare the sum between player and dealer
    assert player_sum <= 21 and dealer_sum <= 21
    if player_sum > dealer_sum:
        return state, 1, player_trajectory
    elif player_sum == dealer_sum:
        return state, 0, player_trajectory
    else:
        return state, -1, player_trajectory


# Monte Carlo Sample with On-Policy
def monte_carlo_on_policy(episodes):
    states_usable_ace = np.zeros((10, 10))
    # initialize counts to 1 to avoid 0 being divided
    states_usable_ace_count = np.ones((10, 10))
    states_no_usable_ace = np.zeros((10, 10))
    # initialize counts to 1 to avoid 0 being divided
    states_no_usable_ace_count = np.ones((10, 10))
    for i in tqdm(range(0, episodes)):
        _, reward, player_trajectory = play(target_policy_player)
        for (usable_ace, player_sum, dealer_card), _ in player_trajectory:
            player_sum -= 12
            dealer_card -= 1
            if usable_ace:
                states_usable_ace_count[player_sum, dealer_card] += 1
                states_usable_ace[player_sum, dealer_card] += reward
            else:
                states_no_usable_ace_count[player_sum, dealer_card] += 1
                states_no_usable_ace[player_sum, dealer_card] += reward
    return states_usable_ace / states_usable_ace_count, states_no_usable_ace / states_no_usable_ace_count


# Monte Carlo with Exploring Starts
def monte_carlo_exploring_starts(episodes):
    # (playerSum, dealerCard, usableAce, action)
    state_action_values = np.zeros((10, 10, 2, 2))
    # initialze counts to 1 to avoid division by 0
    state_action_pair_count = np.ones((10, 10, 2, 2))

    # behavior policy is greedy
    def behavior_policy(usable_ace, player_sum, dealer_card):
        usable_ace = int(usable_ace)
        player_sum -= 12
        dealer_card -= 1
        # get argmax of the average returns(s, a)
        values_ = state_action_values[player_sum, dealer_card, usable_ace, :] / \
                  state_action_pair_count[player_sum, dealer_card, usable_ace, :]
        return np.random.choice([action_ for action_, value_ in enumerate(values_) if value_ == np.max(values_)])

    # play for several episodes
    for episode in tqdm(range(episodes)):
        # for each episode, use a randomly initialized state and action
        initial_state = [
            bool(np.random.choice([0, 1])),
            np.random.choice(range(12, 22)),
            np.random.choice(range(1, 11))]
        initial_action = np.random.choice(ACTIONS)
        current_policy = behavior_policy if episode else target_policy_player
        _, reward, trajectory = play(current_policy, initial_state, initial_action)
        first_visit_check = set()
        for (usable_ace, player_sum, dealer_card), action in trajectory:
            usable_ace = int(usable_ace)
            player_sum -= 12
            dealer_card -= 1
            state_action = (usable_ace, player_sum, dealer_card, action)
            if state_action in first_visit_check:
                continue
            first_visit_check.add(state_action)
            # update values of state-action pairs
            state_action_values[player_sum, dealer_card, usable_ace, action] += reward
            state_action_pair_count[player_sum, dealer_card, usable_ace, action] += 1

    return state_action_values / state_action_pair_count


# Monte Carlo Sample with Off-Policy
def monte_carlo_off_policy(episodes):
    initial_state = [True, 13, 2]

    rhos = []
    returns = []

    for _ in range(0, episodes):
        _, reward, player_trajectory = play(behavior_policy_player, initial_state=initial_state)

        # get the importance ratio
        numerator = 1.0
        denominator = 1.0
        for (usable_ace, player_sum, dealer_card), action in player_trajectory:
            if action == target_policy_player(usable_ace, player_sum, dealer_card):
                denominator *= 0.5
            else:
                numerator = 0.0
                break
        rho = numerator / denominator
        rhos.append(rho)
        returns.append(reward)

    rhos = np.asarray(rhos)
    returns = np.asarray(returns)
    weighted_returns = rhos * returns

    weighted_returns = np.add.accumulate(weighted_returns)
    rhos = np.add.accumulate(rhos)

    ordinary_sampling = weighted_returns / np.arange(1, episodes + 1)

    with np.errstate(divide='ignore', invalid='ignore'):
        weighted_sampling = np.where(rhos != 0, weighted_returns / rhos, 0)

    return ordinary_sampling, weighted_sampling


# %%
def plot_monte_carlo_on_policy():
    states_usable_ace_1, states_no_usable_ace_1 = monte_carlo_on_policy(10000)
    states_usable_ace_2, states_no_usable_ace_2 = monte_carlo_on_policy(500000)

    states = [
        states_usable_ace_1, states_usable_ace_2,
        states_no_usable_ace_1, states_no_usable_ace_2]

    titles = [
        '有可用 A，10000 幕后\n', '有可用 A，500000 幕后\n',
        '\n无可用 A，10000 幕后\n', '\n无可用 A，500000 幕后\n']

    fig = plt.figure(figsize=(10, 6))
    axes = [fig.add_subplot(2, 2, i, projection='3d') for i in range(1, 5)]

    for state, title, ax in zip(states, titles, axes):
        X = np.arange(1, 11)
        Y = np.arange(12, 22)
        X, Y = np.meshgrid(X, Y)

        ax.plot_wireframe(X, Y, state)
        ax.view_init(70, -60)
        ax.set_xlabel('\n庄家显示的牌')
        ax.set_xlim(1, 10)
        ax.set_xticks(list(range(1, 11)))
        ax.set_ylabel('\n  玩家总和  ')
        ax.set_ylim(12, 21)
        ax.set_yticks(list(range(12, 22)))
        ax.set_zticks([])
        ax.set_title(title)

        ax.set_proj_type('ortho')
        ax.grid(False)
        ax.w_zaxis.line.set_color((1.0, 1.0, 1.0, 0.0))

    fig.tight_layout()
    fig.savefig('blackjack-monte-carlo-on-policy.png')

    os.system('convert blackjack-monte-carlo-on-policy.png -trim blackjack-monte-carlo-on-policy.png')


# %%
def plot_monte_carlo_exploring_starts():
    state_action_values = monte_carlo_exploring_starts(500000)

    state_value_no_usable_ace = np.max(state_action_values[:, :, 0, :], axis=-1)
    state_value_usable_ace = np.max(state_action_values[:, :, 1, :], axis=-1)

    # get the optimal policy
    action_no_usable_ace = np.argmax(state_action_values[:, :, 0, :], axis=-1)
    action_usable_ace = np.argmax(state_action_values[:, :, 1, :], axis=-1)

    images = [
        action_usable_ace, state_value_usable_ace,
        action_no_usable_ace, state_value_no_usable_ace]

    titles = [
        '有可用 A，$\pi_*$', '有可用 A，$v_*$',
        '无可用 A，$\pi_*$', '无可用 A，$v_*$']

    fig = plt.figure(figsize=(10, 8))
    axes = [
        fig.add_subplot(2, 2, 1),
        fig.add_subplot(2, 2, 2, projection='3d'),
        fig.add_subplot(2, 2, 3),
        fig.add_subplot(2, 2, 4, projection='3d'),
    ]

    for idx, (image, title, ax) in enumerate(zip(images, titles, axes)):
        if idx % 2 == 0:
            sns.heatmap(
                np.flipud(image), cmap="YlGnBu", ax=ax,
                xticklabels=range(1, 11), yticklabels=list(reversed(range(12, 22))))
            ax.set_ylabel('玩家总和')
            ax.set_xlabel('庄家显示的牌')
            ax.set_title(title)
        else:
            X = np.arange(1, 11)
            Y = np.arange(12, 22)
            X, Y = np.meshgrid(X, Y)

            ax.plot_wireframe(X, Y, image)
            ax.view_init(70, -60)
            ax.set_xlabel('\n庄家显示的牌')
            ax.set_xlim(1, 10)
            ax.set_xticks(list(range(1, 11)))
            ax.set_ylabel('\n  玩家总和  ')
            ax.set_ylim(12, 21)
            ax.set_yticks(list(range(12, 22)))
            ax.set_zticks([])
            ax.set_title(title)

            ax.set_proj_type('ortho')
            ax.grid(False)
            ax.w_zaxis.line.set_color((1.0, 1.0, 1.0, 0.0))

    fig.tight_layout()
    fig.savefig('blackjack-monte-carlo-exploring-starts.png')

    os.system('convert blackjack-monte-carlo-exploring-starts.png -trim blackjack-monte-carlo-exploring-starts.png')


# %%
def plot_monte_carlo_off_policy():
    np.random.seed(3)
    true_value = -0.27726
    episodes = 10000
    runs = 100
    error_ordinary = np.zeros(episodes)
    error_weighted = np.zeros(episodes)
    for _ in tqdm(range(0, runs)):
        ordinary_sampling_, weighted_sampling_ = monte_carlo_off_policy(episodes)
        # get the squared error
        error_ordinary += np.power(ordinary_sampling_ - true_value, 2)
        error_weighted += np.power(weighted_sampling_ - true_value, 2)
    error_ordinary /= runs
    error_weighted /= runs

    fig = plt.figure(figsize=(6, 4))
    plt.plot(error_ordinary, label='原始重要度采样')
    plt.plot(error_weighted, label='加权重要度采样')
    plt.xlabel('幕数（对数尺度）')
    plt.ylabel('均方误差')
    plt.ylim((0, 5))
    plt.xscale('log')
    plt.legend()

    fig.tight_layout()
    fig.savefig('blackjack-monte-carlo-off-policy.png')

    os.system('convert blackjack-monte-carlo-off-policy.png -trim blackjack-monte-carlo-off-policy.png')


# %%
if __name__ == '__main__':
    plot_monte_carlo_on_policy()
    plot_monte_carlo_exploring_starts()
    plot_monte_carlo_off_policy()