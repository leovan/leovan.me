import numpy as np

import matplotlib.pyplot as plt

fig, ax = plt.subplots(1, 1)
dpi = 100


def score_func(p, t, g):
    return (p - 1) / np.power((t + 2), g)


t = np.arange(0, 25, 0.01)

s1 = score_func(10, t, 2)
ax.plot(t, s1, label=r'$\dfrac{\left(10 - 1\right)}{\left(t + 2\right)^{2}}$')

s2 = score_func(10, t, 1.8)
ax.plot(t, s2, label=r'$\dfrac{\left(10 - 1\right)}{\left(t + 2\right)^{1.8}}$')

s3 = score_func(10, t, 1.6)
ax.plot(t, s3, label=r'$\dfrac{\left(10 - 1\right)}{\left(t + 2\right)^{1.6}}$')

plt.legend(loc='best')
plt.tight_layout()
fig.set_size_inches(800 / dpi, 400 / dpi)
plt.savefig('hacker-news-g.png', dpi=dpi)
