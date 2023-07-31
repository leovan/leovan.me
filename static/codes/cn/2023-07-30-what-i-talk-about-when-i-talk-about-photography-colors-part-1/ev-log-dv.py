import numpy as np
import matplotlib.pyplot as plt

x = np.arange(0, 8, 0.01)
y = 32 * x

x_dots = [0, 1, 2, 3, 4, 5, 6, 7, 8]
y_dots = 32 * np.array(x_dots)

fig, axes = plt.subplots(1, 2, width_ratios=[20, 1])

axes[0].plot(x, y, color='black')

for x_dot, y_dot in zip(x_dots, y_dots):
    axes[0].plot([x_dot, x_dot], [0, y_dot], color='black', ls='dotted')
    axes[0].plot([0, x_dot], [y_dot, y_dot], color='black', ls='dotted')

axes[0].set_xticks(x_dots)
axes[0].set_yticks(y_dots)

axes[0].set_xlim(0, 8)
axes[0].set_ylim(0, 256)

axes[0].set_xlabel('EV')
axes[0].set_ylabel(r'曝光量 $\log$ 值')

axes[0].set_aspect(1 / 32.)

colorbar = np.outer(np.arange(256, 0, -1), np.ones(10))
axes[1].imshow(colorbar, aspect='auto', cmap=plt.get_cmap('Greys'))

for y_dot in y_dots:
    axes[1].axhline(y=y_dot, color='red')

axes[1].set_xlim(0, 1)
axes[1].set_ylim(0, 256)

axes[1].axis('off')

plt.tight_layout()
fig.set_size_inches(4.6, 4)
plt.savefig('ev-log-dv.png', dpi=100)