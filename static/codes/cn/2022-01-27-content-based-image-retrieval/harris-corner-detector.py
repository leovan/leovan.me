# %%
import numpy as np
import cv2 as cv

from copy import deepcopy

# %%
img = cv.imread('../../../static/images/cn/2022-01-27-content-based-image-retrieval/blox.jpg')
gray_img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

# %%
harris_corner = cv.cornerHarris(np.float32(gray_img), 2, 3, 0.04)

# %%
corner = cv.dilate(harris_corner, None)

# %%
ret_img = deepcopy(img)
ret_img[corner > 0.01 * corner.max()] = [0, 255, 0]

# %%
cv.imwrite('../../../static/images/cn/2022-01-27-content-based-image-retrieval/blox-harris-corner.jpg', ret_img)

# %%
