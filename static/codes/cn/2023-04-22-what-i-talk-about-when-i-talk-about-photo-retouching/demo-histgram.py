import cv2

import numpy as np
import matplotlib.pyplot as plt

gray_img = cv2.imread('demo.jpg', cv2.IMREAD_GRAYSCALE)
img = cv2.imread('demo.jpg')
img_channels = cv2.split(img)
height, width = gray_img.shape
gray_img_hist = cv2.calcHist([gray_img], [0], None, [256], [0, 256])
img_channels_hist = [cv2.calcHist([img_channel], [0], None, [256], [0, 256])
                     for img_channel in img_channels]

fig, ax = plt.subplots(1, 1)

ax.plot(gray_img_hist, color='0.6', label='灰')

for (img_channel_hist, color, label) in zip(
  img_channels_hist, ['#6695ff', '#70df5f', '#f74048'], ['蓝', '绿', '红']):
    ax.plot(img_channel_hist, color=color, label=label)

segments = [0, 28, 85, 170, 227, 255]
segments_text = ['黑色', '阴影', '曝光', '高光', '白色']

for (left_border, right_border, segment_text) in \
        zip(segments[:-1], segments[1:], segments_text):
  if left_border != 0:
    ax.axvline(x=left_border, ymin=0, color='black')
  
  ax.annotate(
      segment_text,
      xy=((left_border + right_border) / 2, np.max(img_channels_hist) / 3),
      ha='center')

ax.legend(loc='upper center')
plt.xlim([0, 256])
ax.set_xticks([0, 32, 64, 96, 128, 160, 192, 224, 256])
ax.axes.get_yaxis().set_visible(False)

plt.tight_layout()
fig.set_size_inches(8, 4)
plt.savefig('demo-image-histgram.png', dpi=100)