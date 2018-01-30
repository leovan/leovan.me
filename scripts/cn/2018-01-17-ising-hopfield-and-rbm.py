# -*- coding: UTF-8 -*-

# %%
import numpy as np
from matplotlib import pyplot as plt, gridspec
from tfrbm import BBRBM
from tensorflow.examples.tutorials.mnist import input_data

# %%
# fix ssl error when downloading files
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# %%
# read mnist data
mnist = input_data.read_data_sets('../../data/MNIST', one_hot=True)
mnist_train_images = mnist.train.images
mnist_test_images = mnist.test.images
mnist_test_labels = mnist.test.labels

# %%
# fit Bernoulli-Bernoulli RBM model
bbrbm = BBRBM(n_visible=784,
              n_hidden=64,
              learning_rate=0.01,
              momentum=0.95,
              use_tqdm=True)

bbrbm_errs = bbrbm.fit(mnist_train_images, n_epoches=30, batch_size=10)

# %%
# sava trained RBM model
bbrbm.save_weights('../../output/cn/2018-01-17-ising-hopfield-and-rbm/mnist-bbrbm', 'default')
# bbrbm.load_weights('../../output/cn/2018-01-17-ising-hopfield-and-rbm/mnist-bbrbm', 'default')

# %%
# plot bbrbm errors
plt.style.use('ggplot')
plt.plot(bbrbm_errs)
plt.savefig('../../static/cn/2018-01-17-ising-hopfield-and-rbm/bbrbm-mnist-errs.png', bbox_inches='tight')

# %%
# sample test data and reconstruct data
mnist_test_images_samples = np.zeros([10 * 10, 784])
mnist_test_images_samples_rec = np.zeros([10 * 10, 784])
mnist_test_images_samples_plt = np.zeros([10 * 10 * 2, 784])

digits_current_counts = np.zeros(10, dtype=np.int32)
digits_total_counts = np.ones(10, dtype=np.int32) * 10

for idx in range(mnist_test_images.shape[0]):
    image = mnist_test_images[idx, ]
    label = mnist_test_labels[idx, ]

    for digit in range(10):
        digit_label = np.zeros(10)
        digit_label[digit] = 1

        if (label == digit_label).all() and digits_current_counts[digit] < 10:
            nrow = digits_current_counts[digit]
            sample_idx = nrow * 10 + digit
            mnist_test_images_samples[sample_idx, ] = image
            mnist_test_images_samples_rec[sample_idx, ] = \
                bbrbm.reconstruct(image.reshape([1, -1]))
            mnist_test_images_samples_plt[sample_idx * 2, ] = \
                mnist_test_images_samples[sample_idx, ]
            mnist_test_images_samples_plt[sample_idx * 2 + 1, ] = \
                mnist_test_images_samples_rec[sample_idx, ]
            digits_current_counts[digit] += 1

    if (digits_current_counts == digits_total_counts).all():
        break


# %%
# funtion of plotting mnist data
def plot_mnist(mnist_images, nrows, ncols, cmap='gray'):
    fig = plt.figure(figsize=(ncols, nrows))
    gs = gridspec.GridSpec(nrows, ncols)
    gs.update(wspace=0.025, hspace=0.025)

    for nrow in range(nrows):
        for ncol in range(ncols):
            ax = plt.subplot(gs[nrow, ncol])
            idx = nrow * ncols + ncol
            minist_image = mnist_images[idx, ].reshape([28, 28])
            ax.imshow(minist_image, cmap=cmap)
            ax.axis('off')

    return fig

# %%
# plot test data and reconstruct data
bbrbm_fig = plot_mnist(mnist_test_images_samples_plt, 10, 20)
bbrbm_fig.savefig('../../static/cn/2018-01-17-ising-hopfield-and-rbm/bbrbm-mnist.png', bbox_inches='tight')

# %%
# reconstruct error
bbrbm.get_err(mnist_test_images_samples)
