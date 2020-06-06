# %%
import math
import numpy as np

import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Source Han Sans CN']
rcParams['font.size'] = 16
rcParams['mathtext.fontset'] = 'cm'
rcParams['text.usetex'] = True

from scipy.spatial.distance import cdist

# %%
def kernel_se(x1, x2, var_f, l):
    """ Squared Exponential Kernel

    Args:
        x1:
        x2:
        var_f: signal variance hyper-parameter
        l: length scale hyper-parameter
    """

    return var_f * np.exp((-cdist(x1, x2)**2) / (2 * l**2))

# %%
def sample(mu, var, num_samples, num_test_points, jitter=1e-10, random_seed=1123):
    """ Sample from a multivariate Gaussian

    Args:
        mu: mean
        var: variance
        num_samples: num of samples
        num_test_points: num of test points
        jitter: small number to ensure numerical stability (eigenvalues of K can decay rapidly)
        random_seed: random seed
    """

    np.random.seed(random_seed)
    # cholesky decomposition (square root) of covariance matrix
    L = np.linalg.cholesky(var + jitter * np.eye(var.shape[0]))
    return mu + L @ np.random.normal(size=(num_test_points, num_samples))

# %%
x_min, x_max = -5, 5
num_samples = 10
num_test_points = 100
var_f, l = 1, 1
x_star = np.linspace(x_min * 1.4, x_max * 1.4, num_test_points).reshape(-1, 1)
k_se = kernel_se(x_star, x_star, var_f, l)
f_prior = sample(0, k_se, num_samples, num_test_points)
std = np.sqrt(np.diag(k_se))

# %%
fig = plt.figure(figsize=(12, 5))

# plot the sampled values as functions of x_star
plt.subplot(1, 2, 1)
plt.plot(x_star, f_prior)
plt.title('{} samples from the GP prior'.format(num_samples))
plt.fill_between(x_star.flatten(), 0-2*std, 0+2*std, label='$\pm$2 standard deviations of posterior', color='#dddddd')
plt.legend()

# visualize the covariance function
plt.subplot(1, 2, 2)
plt.title('Prior covariance $K(X_*, X_*)$')
plt.contourf(k_se)
plt.show()

# %%
def f(x):
    return np.sin(x) + 0.1 * np.cos(2 * x)

# %%
np.random.seed(1123)
x_train = np.random.uniform(x_min, x_max, size=(12, 1))
y_train = f(x_train)

# %%
fig = plt.figure(figsize=(6, 4))

plt.plot(x_star, f(x_star), color='black', label='Underlying function')
plt.scatter(x_train, y_train, color='black', label='Training points')
plt.legend()
plt.show()

# %%
def gp_regression(X, y, k, x_star, var_f, l):
    # calculate mean
    L = np.linalg.cholesky(k(X, X, var_f, l))
    alpha = np.linalg.solve(L.T, np.linalg.solve(L, y))
    mu = k(X, x_star, var_f, l).T @ alpha

    # calculate variance
    v = np.linalg.solve(L, k(X, x_star, var_f, l))
    var = k(x_star, x_star, var_f, l) - v.T @ v

    return mu, var

# %%
mu, var = gp_regression(x_train, y_train, kernel_se, x_star, var_f, l)
std = np.sqrt(np.diag(var))
f_post = sample(mu, var, num_samples)

# %%
fig = plt.figure(figsize=(12, 5))

# plot underlying function, training data, posterior mean and +/- 2 standard deviations
plt.subplot(1, 2, 1)
plt.title('Posterior - Observations')
plt.fill_between(x_star.flatten(), mu.flatten()-2*std, mu.flatten()+2*std, label='$\pm$2 standard deviations of posterior', color='#dddddd')
plt.plot(x_star, f(x_star), 'b-', label='Underlying function')
plt.plot(x_star, mu, 'r-', label='Mean of posterior')  # plot mean of posterior
plt.plot(x_train, y_train, 'kx', ms=8 ,label='Training input-target pairs')
plt.legend()

# plot samples from posterior
plt.subplot(1, 2, 2)
plt.title('%i samples from GP posterior' % num_samples)
plt.plot(x_star, f_post)  # plot samples from posterior
plt.plot(x_train, y_train, 'kx', ms=8 ,label='Training input-target pairs')
plt.show()

# %%
kk = kernel_se(x_star, x_train, 1, 1) @ np.linalg.inv(kernel_se(x_train, x_train, 1, 1)) @ kernel_se(x_train, x_star, 1, 1)

# %%
fig = plt.figure(figsize=(18, 5))

plt.subplot(1, 3, 1)
plt.title('Prior covariance\n$K(X_*, X_*)$')
plt.contourf(k_se)

plt.subplot(1, 3, 2)
plt.title('$K(X_*, X) K(X, X)^{-1} K(X, X_*)$')
plt.contourf(kk)

plt.subplot(1, 3, 3)
plt.title('Posterior covariance\n$K(X_*, X_*) - K(X_*, X) K(X, X)^{-1} K(X, X_*)$')
plt.contourf(var)
plt.show()

# %%
