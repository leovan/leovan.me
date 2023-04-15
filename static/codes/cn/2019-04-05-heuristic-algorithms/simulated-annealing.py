# %%
import os
import random
import numpy as np

from mayavi import mlab
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.image import imsave


# %%
def func(X, Y):
    return np.exp(-(X**2 + Y**2)) + 2 * np.exp(-((X - 1.7)**2 + (Y - 1.7)**2))


# %%
def neighbours(x_idx, y_idx, x_min_idx, x_max_idx, y_min_idx, y_max_idx):
    X_idx = []
    Y_idx = []

    if x_idx - 1 >= x_min_idx:
        X_idx.append(x_idx - 1)
        Y_idx.append(y_idx)

    if x_idx + 1 <= x_max_idx:
        X_idx.append(x_idx + 1)
        Y_idx.append(y_idx)

    if y_idx - 1 >= y_min_idx:
        X_idx.append(x_idx)
        Y_idx.append(y_idx - 1)

    if y_idx + 1 <= y_max_idx:
        X_idx.append(x_idx)
        Y_idx.append(y_idx + 1)

    return X_idx, Y_idx


# %%
def hill_climbing_next_point(X, Y, x_idx, y_idx):
    z = func(X[x_idx], Y[y_idx])
    X_idx, Y_idx = neighbours(x_idx, y_idx, 0, len(X), 0, len(Y))

    next_x_idx, next_y_idx = None, None

    for neighbour_x_idx, neighbour_y_idx in zip(X_idx, Y_idx):
        neighbour_z = func(X[neighbour_x_idx], Y[neighbour_y_idx])

        if neighbour_z > z:
            next_x_idx = neighbour_x_idx
            next_y_idx = neighbour_y_idx
            z = neighbour_z

    return next_x_idx, next_y_idx


# %%
def hill_climbing(X, Y, init_x_idx, init_y_idx):
    x_idx = init_x_idx
    y_idx = init_y_idx

    X_path = []
    Y_path = []

    while x_idx is not None and y_idx is not None:
        X_path.append(X[x_idx])
        Y_path.append(Y[y_idx])

        x_idx, y_idx = hill_climbing_next_point(X, Y, x_idx, y_idx)

    return np.array(X_path), np.array(Y_path)


# %%
def simulated_annealing_next_point(
        x, y, x_min, x_max, y_min, y_max, temp, init_temp):
    range_scale = max(temp / init_temp, 0.2)

    range_x_min = x - (x - x_min) * range_scale
    range_x_max = x + (x_max - x) * range_scale
    range_y_min = y - (y - y_min) * range_scale
    range_y_max = y + (y_max - y) * range_scale

    tmp_x = random.random() * (range_x_max - range_x_min) + range_x_min
    tmp_y = random.random() * (range_y_max - range_y_min) + range_y_min

    z = func(np.array([x]), np.array([y]))
    tmp_z = func(np.array([tmp_x]), np.array([tmp_y]))

    next_x, next_y = None, None

    if tmp_z > z:
        next_x, next_y = tmp_x, tmp_y
    else:
        p = np.exp((tmp_z - z) / temp)
        if random.random() < p:
            next_x, next_y = tmp_x, tmp_y

    return next_x, next_y


# %%
def simulated_annealing(
        X, Y, init_x, init_y,
        init_temp=200, temp_delta=0.98, temp_min=1e-10, random_seed=112358):
    X_path = [init_x]
    Y_path = [init_y]

    x_min, x_max = min(X), max(X)
    y_min, y_max = min(Y), max(Y)
    x, y = init_x, init_y

    temp = init_temp
    random.seed(random_seed)

    while temp > temp_min:
        next_x, next_y = simulated_annealing_next_point(
                x, y, x_min, x_max, y_min, y_max, temp, init_temp)

        if next_x is not None and next_y is not None:
            x, y = next_x, next_y
            X_path.append(x)
            Y_path.append(y)

        temp *= temp_delta

    return np.array(X_path), np.array(Y_path)


# %%
def draw_surface(X, Y):
    X, Y = np.meshgrid(X, Y)
    Z = func(X, Y)

    mlab.mesh(X, Y, Z, colormap='viridis')


# %%
def draw_path(X, Y, Z):
    colors = [(1, 1, 1, 1), (0.97, 0.09, 0.58, 1)]
    colors_map = LinearSegmentedColormap.from_list('PINK', colors)

    for idx, (x, y, z) in enumerate(zip(X, Y, Z)):
        color = colors_map(float(idx) / len(X))[:3]
        mlab.points3d(x, y, z, color=color, scale_factor=0.05)

    mlab.points3d(X[0], Y[0], Z[0], color=colors[0][:3], scale_factor=0.15)
    mlab.points3d(X[-1], Y[-1], Z[-1], color=colors[1][:3], scale_factor=0.15)


# %%
def make_frames(X, Y, X_path, Y_path):
    Z_path = func(X_path, Y_path)

    colors = [(1, 1, 1, 1), (0.97, 0.09, 0.58, 1)]
    colors_map = LinearSegmentedColormap.from_list('PINK', colors)

    mlab.view(-60, 75, 15)

    draw_surface(X, Y)

    frames = []

    for idx, (x, y, z) in enumerate(zip(X_path, Y_path, Z_path)):
        if idx == 0:
            mlab.points3d(x, y, z, color=colors[0][:3], scale_factor=0.15)
        elif idx == len(Z_path) - 1:
            mlab.points3d(x, y, z, color=colors[1][:3], scale_factor=0.15)
        else:
            color = colors_map(float(idx) / len(X))[:3]
            mlab.points3d(x, y, z, color=color, scale_factor=0.05)

        frames.append(mlab.screenshot(fig, mode='rgba', antialiased=True))

    return frames


# %%
def plot_hill_climbing(init_x_idx, init_y_idx):
    X = np.arange(-2, 4, 0.01)
    Y = np.arange(-2, 4, 0.01)

    X_path, Y_path = hill_climbing(X, Y, init_x_idx, init_y_idx)
    Z_path = func(X_path, Y_path)

    draw_surface(X, Y)
    draw_path(X_path, Y_path, Z_path)

    mlab.view(-60, 75, 15)


# %%
def make_hill_climbing_frames(init_x_idx, init_y_idx):
    X = np.arange(-2, 4, 0.01)
    Y = np.arange(-2, 4, 0.01)

    X_path, Y_path = hill_climbing(X, Y, init_x_idx, init_y_idx)

    return make_frames(X, Y, X_path, Y_path)


# %%
def plot_simulated_annealing(init_x, init_y, random_seed=112358):
    X = np.arange(-2, 4, 0.01)
    Y = np.arange(-2, 4, 0.01)

    X_path, Y_path = simulated_annealing(
            X, Y, init_x, init_y, random_seed=random_seed)
    Z_path = func(X_path, Y_path)

    draw_surface(X, Y)
    draw_path(X_path, Y_path, Z_path)

    mlab.view(-60, 75, 15)


# %%
def make_simulated_annealing_frames(
        init_x_idx, init_y_idx, random_seed=112358):
    X = np.arange(-2, 4, 0.01)
    Y = np.arange(-2, 4, 0.01)

    X_path, Y_path = simulated_annealing(
            X, Y, init_x_idx, init_y_idx, random_seed=random_seed)

    return make_frames(X, Y, X_path, Y_path)


# %%
fig = mlab.figure(size=(400, 400))


# %%
plot_hill_climbing(350, 50)
fig_screenshot = mlab.screenshot(fig, mode='rgba', antialiased=True)
imsave('hill-climbing-1.png', fig_screenshot)
mlab.clf()


# %%
plot_hill_climbing(550, 250)
fig_screenshot = mlab.screenshot(fig, mode='rgba', antialiased=True)
imsave('hill-climbing-2.png', fig_screenshot)
mlab.clf()


# %%
os.system('convert hill-climbing-1.png hill-climbing-2.png -gravity south +append hill-climbing.png')
os.system('convert hill-climbing.png -trim hill-climbing.png')

# %%
plot_simulated_annealing(1.5, -1.5, random_seed=1)
fig_screenshot = mlab.screenshot(fig, mode='rgba', antialiased=True)
imsave('simulated-annealing-1.png', fig_screenshot)
mlab.clf()


# %%
plot_simulated_annealing(3.5, 0.5, random_seed=2)
fig_screenshot = mlab.screenshot(fig, mode='rgba', antialiased=True)
imsave('simulated-annealing-2.png', fig_screenshot)
mlab.clf()


# %%
frames = make_hill_climbing_frames(350, 50)

for idx, frame in enumerate(frames):
    imsave('hill-climbing-1-frame-{:0>3d}.png'.format(idx), frame)

mlab.clf()

frames = make_hill_climbing_frames(550, 250)

for idx, frame in enumerate(frames):
    imsave('hill-climbing-2-frame-{:0>3d}.png'.format(idx), frame)

mlab.clf()


# %%
os.system('convert simulated-annealing-1.png simulated-annealing-2.png -gravity south +append simulated-annealing.png')
os.system('convert simulated-annealing.png -trim simulated-annealing.png')
