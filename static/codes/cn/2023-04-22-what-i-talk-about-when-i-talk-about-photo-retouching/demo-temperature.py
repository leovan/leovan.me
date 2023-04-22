import math
import cv2

import numpy as np


def __kelvin_to_rgb(kelvin: int) -> (int, int, int):
  kelvin = np.clip(kelvin, min_val=1000, max_val=40000)
  temperature = kelvin / 100.0

  # 红色通道
  if temperature < 66.0:
      red = 255
  else:
      # a + b x + c Log[x] /.
      # {a -> 351.97690566805693`,
      # b -> 0.114206453784165`,
      # c -> -40.25366309332127
      # x -> (kelvin/100) - 55}
      red = temperature - 55.0
      red = 351.97690566805693 + 0.114206453784165 * red \
            - 40.25366309332127 * math.log(red)

  # 绿色通道
  if temperature < 66.0:
      # a + b x + c Log[x] /.
      # {a -> -155.25485562709179`,
      # b -> -0.44596950469579133`,
      # c -> 104.49216199393888`,
      # x -> (kelvin/100) - 2}
      green = temperature - 2
      green = -155.25485562709179 - 0.44596950469579133 * green \
              + 104.49216199393888 * math.log(green)
  else:
      # a + b x + c Log[x] /.
      # {a -> 325.4494125711974`,
      # b -> 0.07943456536662342`,
      # c -> -28.0852963507957`,
      # x -> (kelvin/100) - 50}
      green = temperature - 50.0
      green = 325.4494125711974 + 0.07943456536662342 * green \
              - 28.0852963507957 * math.log(green)

  # 蓝色通道
  if temperature >= 66.0:
      blue = 255
  elif temperature <= 20.0:
      blue = 0
  else:
      # a + b x + c Log[x] /.
      # {a -> -254.76935184120902`,
      # b -> 0.8274096064007395`,
      # c -> 115.67994401066147`,
      # x -> kelvin/100 - 10}
      blue = temperature - 10.0
      blue = -254.76935184120902 + 0.8274096064007395 * blue \
             + 115.67994401066147 * math.log(blue)

  return np.clip(red, 0, 255), np.clip(green, 0, 255), np.clip(blue, 0, 255)


def __mix_color(v1, v2, ratio: float):
  return np.array((1.0 - ratio) * v1 + 0.5).astype(np.uint8) \
      + np.array(ratio * v2).astype(np.uint8)


def __keep_original_lightness(original_image, image):
  original_l = cv2.cvtColor(original_image, cv2.COLOR_BGR2HLS)[..., 1]
  h, l, s = cv2.split(cv2.cvtColor(image, cv2.COLOR_BGR2HLS))

  return cv2.cvtColor(cv2.merge([h, original_l, s]), cv2.COLOR_HLS2BGR)


def apply_temperature(
        image,
        temperature,
        keep_original_lightness: bool = True):
  b, g, r = cv2.split(image)
  n_b = np.clip(b.astype(np.single) - temperature, 0, 255).astype(np.uint8)
  n_r = np.clip(r.astype(np.single) + temperature, 0, 255).astype(np.uint8)
  ret_image = cv2.merge([n_b, g, n_r])

  return __keep_original_lightness(image, ret_image) \
      if keep_original_lightness else ret_image


def apply_kelvin(
        image,
        kelvin: int,
        strength: float = 0.6,
        keep_original_lightness: bool = True):
  b, g, r = cv2.split(image)
  k_r, k_g, k_b = __kelvin_to_rgb(kelvin)
  n_r, n_g, n_b = __mix_color(r, k_r, strength), \
      __mix_color(g, k_g, strength), __mix_color(b, k_b, strength)
  ret_image = cv2.merge([n_b, n_g, n_r])

  return __keep_original_lightness(image, ret_image) \
      if keep_original_lightness else ret_image


img = cv2.imread('demo.jpg')
cv2.imwrite('demo-color-temperature-cold.jpg', apply_kelvin(img, 5000))
cv2.imwrite('demo-color-temperature-cold.jpg', apply_kelvin(img, 10000))