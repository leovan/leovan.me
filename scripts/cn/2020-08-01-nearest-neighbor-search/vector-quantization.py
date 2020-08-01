# %%
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from scipy.cluster.vq import kmeans, vq
from matplotlib import rcParams

rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Source Han Sans CN']
rcParams['font.size'] = 10
rcParams['mathtext.fontset'] = 'cm'

# %%
lena = mpimg.imread('lena.png')
height, width, channel = lena.shape
lena_2d = np.reshape(lena, (height * width, channel))
ks = [2, 10, 100]
vq_images = []

# %%
for k in ks:
    centroids, distor = kmeans(lena_2d, k)
    code, distor = vq(lena_2d, centroids)
    vq_image = centroids[code, :]
    vq_images.append(np.reshape(vq_image, (height, width, channel)))

# %%
fig = plt.figure(figsize=(4, 4), dpi=100)

plt.subplot(2, 2, 1)
plt.imshow(lena)
plt.title('原始')
plt.axis('off')

for idx in range(0, 3):
    plt.subplot(2, 2, idx + 2)
    plt.imshow(vq_images[idx])
    plt.title('VQ {}'.format(ks[idx]))
    plt.axis('off')

fig.tight_layout()
fig.savefig('lena-vq.png')
