import numpy as np

import matplotlib.pyplot as plt

fig, ax = plt.subplots(1, 1)
dpi = 80

x = np.arange(-1000, 1000)

y = 1 / (1 + np.power(10, x / 400))
ax.plot(x, y, label=r'$\dfrac{1}{1 + 10^{\frac{x}{400}}}$')

y = 1 / (1 + np.power(10, x / 200))
ax.plot(x, y, label=r'$\dfrac{1}{1 + 10^{\frac{x}{200}}}$')

y = 1 / (1 + np.power(10, x / 600))
ax.plot(x, y, label=r'$\dfrac{1}{1 + 10^{\frac{x}{600}}}$')

plt.legend(loc='best')
plt.tight_layout()
fig.set_size_inches(450 / dpi, 300 / dpi)
plt.savefig('elo-logistic-distribution.png', dpi=dpi)