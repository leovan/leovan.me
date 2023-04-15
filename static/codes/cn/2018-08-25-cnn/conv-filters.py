# -*- coding: UTF-8 -*-

# %%
import matplotlib.pyplot as plt
import cv2
import numpy as np

img = plt.imread('../../../static/images/cn/2017-12-11-evd-svd-and-pca/lena-std.png')
plt.imshow(img)

# %%
# Edge Detection
filter_identity = np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]])
filter_identity_img = cv2.filter2D(img, -1, filter_identity)

plt.imshow(filter_identity_img)
plt.imsave('../../../static/images/cn/2018-08-25-cnn/lena-filter-identity.png', filter_identity_img)

# %%
# Edge Detection
filter_edge = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])
filter_edge_img = cv2.filter2D(img, -1, filter_edge)

plt.imshow(filter_edge_img)
plt.imsave('../../../static/images/cn/2018-08-25-cnn/lena-filter-edge.png', filter_edge_img)

# %%
# Sharpen
filter_sharpen = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
filter_sharpen_img = cv2.filter2D(img, -1, filter_sharpen)

plt.imshow(filter_sharpen_img)
plt.imsave('../../../static/images/cn/2018-08-25-cnn/lena-filter-sharpen.png', filter_sharpen_img)

# %%
# Gaussian Blur
filter_gaussian_blur = np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]]) / 16
filter_gaussian_blur_img = cv2.filter2D(img, -1, filter_gaussian_blur)

plt.imshow(filter_gaussian_blur_img)
plt.imsave('../../../static/images/cn/2018-08-25-cnn/lena-filter-gaussian-blur.png', filter_gaussian_blur_img)
