# %%
from sys import flags
import numpy as np
import cv2 as cv

from copy import deepcopy

# %%
img = cv.imread('../../../static/images/cn/2022-01-27-content-based-image-retrieval/home.jpg')
gray_img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

# %%
sift = cv.SIFT_create()

# %%
key_points = sift.detect(gray_img, None)

# %%
ret_img = deepcopy(img)
ret_img = cv.drawKeypoints(gray_img, key_points, ret_img, flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# %%
cv.imwrite('../../../static/images/cn/2022-01-27-content-based-image-retrieval/home-sift-key-points.jpg', ret_img)

# %%
