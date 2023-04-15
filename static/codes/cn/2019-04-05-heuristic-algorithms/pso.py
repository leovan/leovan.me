# %%
import numpy as np
import matplotlib.pyplot as plt

from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D

from pyswarms.single.global_best import GlobalBestPSO


# %%
def rosenbrock_opt(xy, a=1, b=100, c=0):
    return (a - xy[:, 0]) ** 2 + b * (xy[:, 1] - xy[:, 0] ** 2) ** 2 + c

def rosenbrock_fig(X, Y, a=1, b=100, c=0):
    return (a - X) ** 2 + b * (Y - X ** 2) ** 2 + c

# %%
X, Y = np.arange(-2, 2, 0.05), np.arange(-1, 3, 0.05)
X, Y = np.meshgrid(X, Y)
Z = rosenbrock_fig(X, Y)

# %%
def plot_rosenbrock(
    X, Y, Z, fig,
    xlim=(-2, 2), ylim=(-1, 3), zlim=(0, 2500), **kwargs):
    ax = Axes3D(fig)
    ax.view_init(45, -125)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_zlim(*zlim)
    ax.plot_surface(
        X, Y, Z, rstride=1, cstride=1,
        cmap=plt.get_cmap('viridis'), **kwargs)
    
    return ax

# %%
x_max = (2, 3)
x_min = (-2, -1)
bounds = (x_min, x_max)
options = {'c1': 0.5, 'c2': 0.3, 'w': 0.9}
optimizer = GlobalBestPSO(n_particles=50, dimensions=2, options=options, bounds=bounds)

# %%
cost, pos = optimizer.optimize(rosenbrock_opt, 200)

# %%
history_pos = optimizer.pos_history

# %%
def gen_rosenbrock_pso_animation(history_pos):
    X, Y = np.arange(-2, 2, 0.05), np.arange(-1, 3, 0.05)
    X, Y = np.meshgrid(X, Y)
    Z = rosenbrock_fig(X, Y)

    fig = plt.figure(figsize=(6.4, 4.8), dpi=50)

    def gen_frame(frame):
        fig.clear()

        XP = history_pos[frame][:, 0].T
        YP = history_pos[frame][:, 1].T
        ZP = rosenbrock_fig(XP, YP)

        ax = plot_rosenbrock(X, Y, Z, fig, alpha=0.6)
        ax.scatter(XP, YP, ZP, c='black', marker='.')

        return fig

    return animation.FuncAnimation(fig, gen_frame, frames=200)

# %%
anim = gen_rosenbrock_pso_animation(history_pos)
anim.save('rosenbrock-pso.gif', writer='imagemagick', fps=20, dpi=50)
