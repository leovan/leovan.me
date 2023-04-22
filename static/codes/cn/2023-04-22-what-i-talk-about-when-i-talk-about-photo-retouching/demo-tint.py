import cv2

import numpy as np


def __keep_original_lightness(original_image, image):
  original_l = cv2.cvtColor(original_image, cv2.COLOR_BGR2HLS)[..., 1]
  h, l, s = cv2.split(cv2.cvtColor(image, cv2.COLOR_BGR2HLS))

  return cv2.cvtColor(cv2.merge([h, original_l, s]), cv2.COLOR_HLS2BGR)


def apply_tint(image, tint, keep_original_lightness: bool = True):
  b, g, r = cv2.split(image)
  n_g = np.clip(g.astype(np.single) + tint, 0, 255).astype(np.uint8)
  ret_image = cv2.merge([b, n_g, r])

  return __keep_original_lightness(image, ret_image) \
    if keep_original_lightness else ret_image


img = cv2.imread('demo.jpg')
cv2.imwrite('demo-color-tint-negative.jpg', apply_tint(img, -30))
cv2.imwrite('demo-color-tint-positive.jpg', apply_tint(img, +30))