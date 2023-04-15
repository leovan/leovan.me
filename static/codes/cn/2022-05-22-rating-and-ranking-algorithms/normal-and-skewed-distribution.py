import numpy as np

from scipy.special import erf
import matplotlib.pyplot as plt


def pdf(x, mu=0, sigma=1):
    return 1.0 / (np.sqrt(2 * np.pi) * sigma) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)


def cdf(x):
    return (1 + erf(x / np.sqrt(2))) / 2


def skew(x, e, w, a):
    t = (x - e) / w
    return 100 / w * pdf(t) * cdf(a * t)


n = 65

fig, axes = plt.subplots(1, 3)
dpi = 100

x = np.linspace(-3, 14, n)
y = skew(x, 0, 4.4, 4)
axes[0].plot(x, y)
axes[0].get_xaxis().set_visible(False)
axes[0].get_yaxis().set_visible(False)
axes[0].set_title('正偏态分布')
axes[0].set_ylim(-1, 9)

idx_mode = list(y).index(np.max(y))
axes[0].plot([x[idx_mode], x[idx_mode]], [0, y[idx_mode]])
axes[0].annotate('众数', (x[idx_mode], -0.8), ha='center', fontsize=12)
axes[0].plot([x[idx_mode + 12], x[idx_mode + 12]], [0, y[idx_mode + 12]])
axes[0].annotate('中位数', (x[idx_mode + 12], -0.8), ha='center', fontsize=12)
axes[0].plot([x[idx_mode + 18], x[idx_mode + 18]], [0, y[idx_mode + 18]])
axes[0].annotate('平均数', (x[idx_mode + 18], -0.8), ha='left', fontsize=12)

x = np.linspace(-6, 6, n)
y = skew(x, 0, 2.5, 0)
axes[1].plot(x, y)
axes[1].get_xaxis().set_visible(False)
axes[1].get_yaxis().set_visible(False)
axes[1].set_title('正态分布')
axes[1].set_ylim(-1, 9)

idx_mode = list(y).index(np.max(y))
axes[1].plot([x[idx_mode], x[idx_mode]], [0, y[idx_mode]])
axes[1].annotate('众数 = 中位数 = 平均数', (x[idx_mode], -0.8), ha='center', fontsize=12)

x = np.linspace(-14, 3, n)
y = skew(x, 0, 4.4, -4)
axes[2].plot(x, y)
axes[2].get_xaxis().set_visible(False)
axes[2].get_yaxis().set_visible(False)
axes[2].set_title('负偏态分布')
axes[2].set_ylim(-1, 9)

idx_mode = list(y).index(np.max(y))
axes[2].plot([x[idx_mode], x[idx_mode]], [0, y[idx_mode]])
axes[2].annotate('众数', (x[idx_mode], -0.8), ha='center', fontsize=12)
axes[2].plot([x[idx_mode - 12], x[idx_mode - 12]], [0, y[idx_mode - 12]])
axes[2].annotate('中位数', (x[idx_mode - 12], -0.8), ha='center', fontsize=12)
axes[2].plot([x[idx_mode - 18], x[idx_mode - 18]], [0, y[idx_mode - 18]])
axes[2].annotate('平均数', (x[idx_mode - 18], -0.8), ha='right', fontsize=12)

plt.subplots_adjust(left=0, bottom=0, right=1, top=0.9, wspace=0.1, hspace=0.1)
fig.set_size_inches(1200 / dpi, 300 / dpi)
plt.savefig('normal-and-skewed-distribution.png', dpi=dpi)
