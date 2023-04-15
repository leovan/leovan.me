#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Mr. Black on 2018-01-29

import os
from tqdm import trange

import numpy as np
import pandas as pd

from matplotlib import pyplot as plt, gridspec

from keras.layers import Input, Dense, Reshape, Flatten
from keras.layers import BatchNormalization
from keras.layers.advanced_activations import LeakyReLU
from keras.models import Sequential, Model
from keras.optimizers import Adam
from keras.datasets import mnist

import tensorflow as tf
from keras.callbacks import TensorBoard

class ImageGAN():
    def __init__(self, width, height, channels, a_optimizer=Adam(1e-4, beta_1=0.5),
                 g_optimizer=Adam(1e-4, beta_1=0.5), d_optimizer=Adam(1e-4, beta_1=0.5),
                 noise_dim=100, hidden_dim=1024):
        '''

        Args:
            width: 图像宽度
            height: 图像高度
            channels: 图像颜色通道数
            a_optimizer: 对抗网络优化器
            g_optimizer: 生成器优化器
            d_optimizer: 判别器优化器
            noise_dim: 噪音数据维度
            hidden_dim: 隐含层最大维度
        '''

        self._data_path = os.path.join(os.path.dirname(__file__), '../../../data')

        self._width = width
        self._height = height
        self._channels = channels
        self._input_shape = (width, height, channels)

        self._a_optimizer = a_optimizer
        self._g_optimizer = g_optimizer
        self._d_optimizer = d_optimizer

        self._noise_dim = noise_dim
        self._noise_shape = (noise_dim, )
        self._hidden_dim = hidden_dim

        self._plt_noises_nrows = 10
        self._plt_noises_ncols = 10
        self._plt_default_noises = np.random.normal(0, 1,
            (self._plt_noises_nrows * self._plt_noises_ncols, self._noise_dim))

        # 构建和编译判别器
        self._discriminator = self.build_discriminator()
        self._discriminator.compile(loss='binary_crossentropy', optimizer=d_optimizer,
                                    metrics=['accuracy'])

        # 构建和编译生成器
        self._generator = self.build_generator()
        self._generator.compile(loss='binary_crossentropy', optimizer=g_optimizer)

        # 生成器利用噪声数据作为输入
        noise = Input(shape=self._noise_shape)
        generated_image = self._generator(noise)

        # 当训练整个对抗网络时，仅训练生成器
        self._discriminator.trainable = False

        # 判别器将生成的图像作为输入
        label = self._discriminator(generated_image)

        # 构建和编译整个对抗网络
        self._adversarial = Model(noise, label)
        self._adversarial.compile(loss='binary_crossentropy', optimizer=a_optimizer)

    def build_generator(self):
        model = Sequential()

        model.add(Dense(int(self._hidden_dim / 4), input_shape=self._noise_shape))
        model.add(LeakyReLU(alpha=0.2))
        model.add(BatchNormalization(momentum=0.8))
        model.add(Dense(int(self._hidden_dim / 2)))
        model.add(LeakyReLU(alpha=0.2))
        model.add(BatchNormalization(momentum=0.8))
        model.add(Dense(self._hidden_dim))
        model.add(LeakyReLU(alpha=0.2))
        model.add(BatchNormalization(momentum=0.8))
        model.add(Dense(np.prod(self._input_shape), activation='tanh'))
        model.add(Reshape(self._input_shape))

        print('Generator Summary: ')
        model.summary()

        noise = Input(shape=self._noise_shape)
        image = model(noise)

        return Model(noise, image)


    def build_discriminator(self):
        model = Sequential()

        model.add(Flatten(input_shape=self._input_shape))
        model.add(Dense(int(self._hidden_dim / 2)))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Dense(int(self._hidden_dim / 4)))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Dense(1, activation='sigmoid'))

        print('Discriminator Summary: ')
        model.summary()

        image = Input(shape=self._input_shape)
        label = model(image)

        return Model(image, label)


    def train(self, x_train, output_dir, iters, batch_size=32, k=1, save_interval=200):
        ''' 训练模型
        
        Args:
            x_train: 训练数据
            output_dir: 相关输出路径
            iters: 迭代次数
            batch_size: 批大小
            k: K
            save_interval: 结果保存间隔

        '''
        tensor_board_cb = TensorBoard(os.path.join(output_dir, 'logs'), histogram_freq=0,
                                      write_graph=True, write_images=True)
        tensor_board_cb.set_model(self._adversarial)

        d_loss_history = []
        d_acc_history = []
        g_loss_history = []

        t_iters = trange(iters)
        for iter in t_iters:
            # 训练判别器
            d_output_sum = 0.0
            for _ in range(k):
                train_indices = np.random.randint(0, x_train.shape[0], batch_size)
                train_images = x_train[train_indices]

                noises = np.random.normal(0, 1, (batch_size, self._noise_dim))
                generated_images = self._generator.predict(noises)

                d_output_real = self._discriminator.train_on_batch(train_images, np.ones((batch_size, 1)))
                d_output_fake = self._discriminator.train_on_batch(generated_images, np.zeros((batch_size, 1)))
                d_output_sum += 0.5 * np.add(d_output_real, d_output_fake)

            # 训练生成器
            noises = np.random.normal(0, 1, (batch_size, self._noise_dim))
            labels = np.ones((batch_size, 1))

            g_output = self._adversarial.train_on_batch(noises, labels)

            # 记录历史
            d_loss = d_output_sum[0] / k
            d_acc = d_output_sum[1] / k
            g_loss = g_output

            d_loss_history.append(d_loss)
            d_acc_history.append(d_acc)
            g_loss_history.append(g_loss)

            # 打印信息
            t_iters.set_postfix(
                d_acc='%.2f%%' % (d_acc * 100),
                d_loss='%.2f' % d_loss,
                g_loss='%.2f' % g_loss)

            # TensorBoard
            self.write_tf_summary(tensor_board_cb,
                                  ['d_loss', 'd_acc', 'g_loss'],
                                  [d_loss, d_acc, g_loss],
                                  iter)

            # 保存生成的图片
            if iter % save_interval == 0:
                self.save_image(output_dir, iter, iters)

        # 保存生成的图片
        self.save_image(output_dir, iters, iters)

        # 保存历史
        history = pd.DataFrame({
            'discriminator_loss': d_loss_history,
            'discriminator_accuracy': d_acc_history,
            'generator_loss': g_loss_history
        })
        history.to_csv(os.path.join(output_dir, 'history.csv'), index=False)


    def write_tf_summary(self, callback, names, values, epoch):
        for name, value in zip(names, values):
            summary = tf.Summary()
            summary_value = summary.value.add()
            summary_value.simple_value = value
            summary_value.tag = name
            callback.writer.add_summary(summary, epoch)
            callback.writer.flush()


    def save_image(self, output_path, iter, iters, default_noise=True):
        noises = self._plt_default_noises if default_noise else \
            np.random.normal(0, 1, (self._plt_noises_nrows * self._plt_noises_ncols, self._noise_dim))
        images = self._generator.predict(noises) * 0.5 + 0.5

        fig = plt.figure(figsize=(6, 6))
        gs = gridspec.GridSpec(self._plt_noises_nrows, self._plt_noises_ncols)
        gs.update(wspace=0.025, hspace=0.025)

        for nrow in range(self._plt_noises_nrows):
            for ncol in range(self._plt_noises_ncols):
                ax = plt.subplot(gs[nrow, ncol])
                idx = nrow * self._plt_noises_ncols + ncol

                if self._channels == 1:
                    ax.imshow(images[idx, :, :, 0], cmap='gray')
                elif self._channels == 3:
                    ax.imshow(images[idx, :, :, 0:2])

                ax.axis('off')

        image_name_format = 'mnist-gan-epoch-{:0>%dd}.png' % int(np.ceil(np.log10(iters)))
        fig.tight_layout()
        fig.savefig(os.path.join(output_path, 'images', image_name_format.format(iter)))
        plt.close()


    def plot_history(self, history_file_path, history_plt_path):
        history = pd.read_csv(history_file_path)

        plt.style.use('ggplot')
        fig = plt.figure(figsize=(6, 6))
        gs = gridspec.GridSpec(2, 2)

        plt.subplot(gs[0, 0])
        plt.plot(history['discriminator_loss'], linewidth=0.6)
        plt.title('Discriminator Loss')

        plt.subplot(gs[0, 1])
        plt.plot(history['generator_loss'], linewidth=0.6)
        plt.title('Generator Loss')

        plt.subplot(gs[1, :])
        plt.plot(history['discriminator_accuracy'], linewidth=0.6)
        plt.title('Discriminator Accuracy')

        fig.tight_layout()
        fig.savefig(history_plt_path)
        plt.close()


    def mnist_preprocess(self, data):
        scaled_data = (data.astype(np.float32) - 127.5) / 127.5
        return np.expand_dims(scaled_data, axis=3)


    def train_mnist(self):
        mnist_path = os.path.join(self._data_path, 'MNIST/mnist.npz')
        print('Loading MNIST from %s' % (mnist_path))
        (x_train, _), (_, _) = mnist.load_data(mnist_path)

        x_train = self.mnist_preprocess(x_train)
        self.train(x_train,
                   os.path.join(os.path.dirname(__file__),
                                '../../../outputs/cn/2018-02-03-gan-introduction/mnist-gan-keras'),
                   iters=30000, save_interval=1000)


if __name__ == '__main__':
    mnist_gan = ImageGAN(width=28, height=28, channels=1)
    mnist_gan.train_mnist()
    # output_dir = os.path.join(os.path.dirname(__file__),
    #                           '../../../outputs/cn/2018-02-03-gan-intro/mnist-gan-keras')
    # history_file_path = os.path.join(output_dir, 'history.csv')
    # history_plt_path = os.path.join(output_dir, 'history.png')
    # image_gan.plot_history(history_file_path, history_plt_path)
