# %%
import numpy as np
import pandas as pd

from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Source Han Sans CN']
rcParams['mathtext.fontset'] = 'cm'

from tqdm import trange
from plotnine import *

# %%
class Bandit:
    def __init__(
        self, k_arm=10, epsilon=0., initial=0., step_size=0.1, sample_averages=False, ucb_param=None,
        gradient=False, gradient_baseline=False, true_reward=0.):
        self.k = k_arm
        self.step_size = step_size
        self.sample_averages = sample_averages
        self.indices = np.arange(self.k)
        self.time = 0
        self.ucb_param = ucb_param
        self.gradient = gradient
        self.gradient_baseline = gradient_baseline
        self.average_reward = 0
        self.true_reward = true_reward
        self.epsilon = epsilon
        self.initial = initial

    def reset(self):
        self.q_true = np.random.randn(self.k) + self.true_reward

        self.q_estimation = np.zeros(self.k) + self.initial

        self.action_count = np.zeros(self.k)

        self.best_action = np.argmax(self.q_true)

        self.time = 0

    def act(self):
        if np.random.rand() < self.epsilon:
            return np.random.choice(self.indices)

        if self.ucb_param is not None:
            UCB_estimation = self.q_estimation + \
                self.ucb_param * np.sqrt(np.log(self.time + 1) / (self.action_count + 1e-5))
            q_best = np.max(UCB_estimation)
            return np.random.choice(np.where(UCB_estimation == q_best)[0])

        if self.gradient:
            exp_est = np.exp(self.q_estimation)
            self.action_prob = exp_est / np.sum(exp_est)
            return np.random.choice(self.indices, p=self.action_prob)

        q_best = np.max(self.q_estimation)

        return np.random.choice(np.where(self.q_estimation == q_best)[0])

    def step(self, action):
        reward = np.random.randn() + self.q_true[action]
        self.time += 1
        self.action_count[action] += 1
        self.average_reward += (reward - self.average_reward) / self.time

        if self.sample_averages:
            self.q_estimation[action] += (reward - self.q_estimation[action]) / self.action_count[action]
        elif self.gradient:
            one_hot = np.zeros(self.k)
            one_hot[action] = 1
            if self.gradient_baseline:
                baseline = self.average_reward
            else:
                baseline = 0
            self.q_estimation += self.step_size * (reward - baseline) * (one_hot - self.action_prob)
        else:
            self.q_estimation[action] += self.step_size * (reward - self.q_estimation[action])

        return reward


def simulate(runs, time, bandits):
    rewards = np.zeros((len(bandits), runs, time))
    best_action_counts = np.zeros(rewards.shape)

    for i, bandit in enumerate(bandits):
        for r in trange(runs):
            bandit.reset()
            for t in range(time):
                action = bandit.act()
                reward = bandit.step(action)
                rewards[i, r, t] = reward
                if action == bandit.best_action:
                    best_action_counts[i, r, t] = 1

    mean_best_action_counts = best_action_counts.mean(axis=1)
    mean_rewards = rewards.mean(axis=1)

    return mean_best_action_counts, mean_rewards

# %%
np.random.seed(112358)
dataset = np.random.randn(200, 10) + np.random.randn(10)
df = pd.DataFrame(dataset)
df_long = pd.melt(df, [], var_name='action', value_name='reward_distribution')
df_long['action'] = pd.Categorical(df_long['action'])

# %%
p = (ggplot(df_long) +
    geom_violin(
        aes(x='action', y='reward_distribution'),
        draw_quantiles=0.5) +
    xlab('动作') + ylab('收益分布') +
    scale_y_continuous(
        limits=[-5, 4],
        breaks=list(range(-5, 5)),
        labels=['-5', '-4', '-3', '-2', '-1', '0', '1', '2', '3', '4']) +
    theme_xkcd() +
    theme(
        axis_title=element_text(family='Source Han Sans CN', size=10)
    )
)

p.save('action-reward-distribution.png', width=6, height=4, dpi=100)

# %%
runs = 2000
time = 1000
epsilons = [0, 0.1, 0.01]
bandits = [Bandit(epsilon=eps, sample_averages=True) for eps in epsilons]
best_action_counts, average_rewards = simulate(runs, time, bandits)

# %%
average_rewards_df = pd.DataFrame(average_rewards.transpose())
average_rewards_df['step'] = average_rewards_df.index
average_rewards_df_long = pd.melt(average_rewards_df, ['step'], var_name='action', value_name='average_reward')

# %%
p = (ggplot(average_rewards_df_long) +
    geom_line(aes(x='step', y='average_reward', color='action')) +
    xlab('训练步数') + ylab('平均收益') + labs(color='方法') +
    scale_y_continuous(
        limits=[0, 1.5],
        breaks=[0, 0.5, 1, 1.5]
    ) +
    scale_colour_manual(
        labels=[r'$\epsilon = 0$', r'$\epsilon = 0.1$', r'$\epsilon = 0.01$'],
        values=['#729ece', '#ff9e4a', '#67bf5c']) +
    theme_xkcd() +
    theme(
        axis_title=element_text(family='Source Han Sans CN', size=10),
        legend_title=element_text(family='Source Han Sans CN', size=10),
        legend_text=element_text(family='Source Han Sans CN', size=10),
        legend_direction='horizontal',
        legend_position=(0.5, 0.25)
    )
)

p.save('epsilon-greedy-step-average-reward.png', width=6, height=4, dpi=100)

# %%
best_action_counts_df = pd.DataFrame(best_action_counts.transpose())
best_action_counts_df['step'] = best_action_counts_df.index
best_action_counts_df_long = pd.melt(best_action_counts_df, ['step'], var_name='action', value_name='best_action_ratio')

# %%
p = (ggplot(best_action_counts_df_long) +
    geom_line(aes(x='step', y='best_action_ratio', color='action')) +
    xlab('训练步数') + ylab('最优动作占比') + labs(color='方法') +
    scale_y_continuous(
        limits=[0, 1],
        breaks=[0, 0.2, 0.4, 0.6, 0.8, 1.0],
        labels=['0%', '20%', '40%', '60%', '80%', '100%']
    ) +
    scale_colour_manual(
        labels=[r'$\epsilon = 0$', r'$\epsilon = 0.1$', r'$\epsilon = 0.01$'],
        values=['#729ece', '#ff9e4a', '#67bf5c']) +
    theme_xkcd() +
    theme(
        axis_title=element_text(family='Source Han Sans CN', size=10),
        axis_text=element_text(family='Source Han Sans CN', size=10),
        legend_title=element_text(family='Source Han Sans CN', size=10),
        legend_text=element_text(family='Source Han Sans CN', size=10),
        legend_direction='horizontal',
        legend_position=(0.5, 0.25)
    )
)

p.save('epsilon-greedy-step-best-action-ratio.png', width=6, height=4, dpi=100)

# %%
runs = 2000
time = 1000
bandits = []
bandits.append(Bandit(epsilon=0, initial=5, step_size=0.1))
bandits.append(Bandit(epsilon=0.1, initial=0, step_size=0.1))
best_action_counts, _ = simulate(runs, time, bandits)

# %%
best_action_counts_df = pd.DataFrame(best_action_counts.transpose())
best_action_counts_df['step'] = best_action_counts_df.index
best_action_counts_df_long = pd.melt(best_action_counts_df, ['step'], var_name='action', value_name='best_action_ratio')

# %%
p = (ggplot(best_action_counts_df_long) +
    geom_line(aes(x='step', y='best_action_ratio', color='action')) +
    xlab('训练步数') + ylab('最优动作占比') + labs(color='方法') +
    scale_y_continuous(
        limits=[0, 1],
        breaks=[0, 0.2, 0.4, 0.6, 0.8, 1.0],
        labels=['0%', '20%', '40%', '60%', '80%', '100%']
    ) +
    scale_colour_manual(
        labels=[r'$Q_1 = 5, \epsilon = 0$', r'$Q_1 = 0, \epsilon = 0.1$'],
        values=['#729ece', '#ff9e4a']) +
    theme_xkcd() +
    theme(
        axis_title=element_text(family='Source Han Sans CN', size=10),
        axis_text=element_text(family='Source Han Sans CN', size=10),
        legend_title=element_text(family='Source Han Sans CN', size=10),
        legend_position=(0.7, 0.3)
    )
)

p.save('epsilon-greedy-different-parameters-best-action-ratio.png', width=6, height=4, dpi=100)

# %%
runs = 2000
time = 1000
bandits = []
bandits.append(Bandit(epsilon=0, ucb_param=2, sample_averages=True))
bandits.append(Bandit(epsilon=0.1, sample_averages=True))
_, average_rewards = simulate(runs, time, bandits)

# %%
average_rewards_df = pd.DataFrame(average_rewards.transpose())
average_rewards_df['step'] = average_rewards_df.index
average_rewards_df_long = pd.melt(average_rewards_df, ['step'], var_name='action', value_name='average_reward')

# %%
p = (ggplot(average_rewards_df_long) +
    geom_line(aes(x='step', y='average_reward', color='action')) +
    xlab('训练步数') + ylab('平均收益') + labs(color='方法') +
    scale_y_continuous(
        limits=[0, 1.6],
        breaks=[0, 0.5, 1, 1.5]
    ) +
    scale_colour_manual(
        labels=[r'UCB $c = 0$', r'$\epsilon$-Greedy $\epsilon = 0.1$'],
        values=['#729ece', '#ff9e4a']) +
    theme_xkcd() +
    theme(
        axis_title=element_text(family='Source Han Sans CN', size=10),
        legend_title=element_text(family='Source Han Sans CN', size=10),
        legend_text=element_text(family='Source Han Sans CN', size=10),
        legend_position=(0.7, 0.3)
    )
)

p.save('epsilon-greedy-ucb-step-average-reward.png', width=6, height=4, dpi=100)

# %%
runs = 2000
time = 1000
bandits = []
bandits.append(Bandit(gradient=True, step_size=0.1, gradient_baseline=True, true_reward=4))
bandits.append(Bandit(gradient=True, step_size=0.1, gradient_baseline=False, true_reward=4))
bandits.append(Bandit(gradient=True, step_size=0.4, gradient_baseline=True, true_reward=4))
bandits.append(Bandit(gradient=True, step_size=0.4, gradient_baseline=False, true_reward=4))
best_action_counts, _ = simulate(runs, time, bandits)

# %%
best_action_counts_df = pd.DataFrame(best_action_counts.transpose())
best_action_counts_df['step'] = best_action_counts_df.index
best_action_counts_df_long = pd.melt(best_action_counts_df, ['step'], var_name='action', value_name='best_action_ratio')

# %%
p = (ggplot(best_action_counts_df_long) +
    geom_line(aes(x='step', y='best_action_ratio', color='action')) +
    xlab('训练步数') + ylab('最优动作占比') + labs(color='方法') +
    scale_y_continuous(
        limits=[-0.25, 1],
        breaks=[0, 0.2, 0.4, 0.6, 0.8, 1.0],
        labels=['0%', '20%', '40%', '60%', '80%', '100%']
    ) +
    scale_colour_manual(
        labels=[
            r'$\alpha = 0.1$，含基准项',
            r'$\alpha = 0.1$，不含基准项',
            r'$\alpha = 0.4$，含基准项',
            r'$\alpha = 0.4$，不含基准项'],
        values=['#729ece', '#ff9e4a', '#67bf5c', '#ed665d']) +
    guides(color=guide_legend(ncol=2)) +
    theme_xkcd() +
    theme(
        axis_title=element_text(family='Source Han Sans CN', size=10),
        axis_text=element_text(family='Source Han Sans CN', size=10),
        legend_title=element_text(family='Source Han Sans CN', size=10),
        legend_text_legend=element_text(family='Source Han Sans CN', size=10),
        legend_position=(0.5, 0.27)
    )
)

p.save('gradient-different-parameters-best-action-ratios.png', width=6, height=4, dpi=100)

# %%
runs = 2000
time = 1000
generators = [
    lambda epsilon: Bandit(epsilon=epsilon, sample_averages=True),
    lambda alpha: Bandit(gradient=True, step_size=alpha, gradient_baseline=True),
    lambda coef: Bandit(epsilon=0, ucb_param=coef, sample_averages=True),
    lambda initial: Bandit(epsilon=0, initial=initial, step_size=0.1)]
parameters = [
    np.arange(-7, -1, dtype=np.float),
    np.arange(-5, 2, dtype=np.float),
    np.arange(-4, 3, dtype=np.float),
    np.arange(-2, 3, dtype=np.float)]

bandits = []
for generator, parameter in zip(generators, parameters):
    for param in parameter:
        bandits.append(generator(pow(2, param)))

_, average_rewards = simulate(runs, time, bandits)
rewards = np.mean(average_rewards, axis=1)

# %%
methods = [[str(i)] * len(parameters[i]) for i in range(len(parameters))]

rewards_df = pd.DataFrame({
    'reward': rewards,
    'parameter': np.concatenate(parameters, axis=0),
    'method': np.concatenate(methods, axis=0),
})

# %%
p = (ggplot(rewards_df) +
    geom_line(aes(x='parameter', y='reward', color='method')) +
    xlab(r'参数 $2^x$') + ylab('平均收益') + labs(color='方法') +
    scale_y_continuous(
        limits=[0.75, 1.5],
        breaks=[0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5]
    ) +
    scale_x_continuous(
        limits=[-7, 2],
        breaks=list(range(-7, 3)),
        labels=['1/128', '1/64', '1/32', '1/16', '1/8', '1/4', '1/2', '1', '2', '4']
    ) +
    scale_colour_manual(
        labels=[
            r'$\epsilon$-Greedy',
            r'Gradient Bandit',
            r'UCB',
            r'乐观初始化贪婪方法 $\alpha=0.1$'],
        values=['#729ece', '#ff9e4a', '#67bf5c', '#ed665d']) +
    guides(color=guide_legend(ncol=2)) +
    theme_xkcd() +
    theme(
        axis_title=element_text(family='Source Han Sans CN', size=10),
        axis_text=element_text(family='Source Han Sans CN', size=10),
        legend_title=element_text(family='Source Han Sans CN', size=10),
        legend_text=element_text(family='Source Han Sans CN', size=10),
        legend_position=(0.5, 0.3)
    )
)

p.save('different-methods-performance.png', width=6, height=4, dpi=100)
