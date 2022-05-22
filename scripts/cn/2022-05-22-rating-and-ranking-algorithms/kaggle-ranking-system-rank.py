import numpy as np

import matplotlib.pyplot as plt

fig, ax = plt.subplots(1, 1)
dpi = 100

r = np.arange(1, 20, 0.01)

s = np.power(r, -0.75)
ax.plot(r, s, label=r'$\text{Rank}^{-0.75}$')

s = np.power(r, -0.6)
ax.plot(r, s, label=r'$\text{Rank}^{-0.6}$')

s = np.power(r, -0.9)
ax.plot(r, s, label=r'$\text{Rank}^{-0.9}$')

s = 1 / r
ax.plot(r, s, label=r'$\dfrac{1}{\text{Rank}}$')

ax.set_xlim(0, 20)
ax.set_ylim(0, 1)
ax.set_xticks(np.arange(1, 20))
ax.set_yticks(np.arange(0, 1.1, 0.1))

plt.legend(loc='best')
plt.tight_layout()
fig.set_size_inches(800 / dpi, 400 / dpi)
plt.savefig('kaggle-ranking-system-rank.png', dpi=dpi)