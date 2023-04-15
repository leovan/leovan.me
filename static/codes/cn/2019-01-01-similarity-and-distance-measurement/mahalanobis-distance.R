library(philentropy)
library(StatMatch)
library(tidyverse)
library(ggplot2)
library(gridExtra)

set.seed(112358)
x <- rnorm(300, 0, 50)
y <- rnorm(300, 0, 10)
samples_df <- data.frame(
    x = x*cos(pi/4) + y*sin(pi/4),
    y = x*cos(pi/4) - y*sin(pi/4)
)

plot(samples_df)
text(samples_df)

points_idx <- c(63, 61, 200)

samples_mahalanobis <- mahalanobis.dist(samples_df)
samples_euclidean <- distance(samples_df, method='euclidean')

samples_pca <- prcomp(samples_df, center=T)
samples_pca_df <- as.data.frame(samples_pca$x)
names(samples_pca_df) <- c('x', 'y')

samples_svd <- svd(samples_df)
samples_svd_df <- as.data.frame(samples_svd$u)
names(samples_svd_df) <- c('x', 'y')

points_svd_df <- data.frame(
    x = samples_svd_df$x[points_idx],
    y = samples_svd_df$y[points_idx]
)

samples_df$x <- samples_df$x - mean(samples_df$x)
samples_df$y <- samples_df$y - mean(samples_df$y)

points_df <- data.frame(
    x = samples_df$x[points_idx],
    y = samples_df$y[points_idx]
)

points_svd_df <- data.frame(
    x = samples_svd_df$x[points_idx],
    y = samples_svd_df$y[points_idx]
)

samples_lines <- data.frame(
    x = c(samples_pca$rotation[1, ]) * -160,
    y = c(samples_pca$rotation[2, ]) * -160,
    xend = c(samples_pca$rotation[1, ]) * 160,
    yend = c(samples_pca$rotation[2, ]) * 160
)

point_color = '#333333'
line_color = '#9933FF'

samples_plt <- samples_df %>%
    ggplot(aes(x=x, y=y)) +
    geom_point(size=1, color=point_color) +
    geom_point(aes(x, y, color=as.factor(seq(length(points_idx)))),
               data=points_df, show.legend=F, size=2) +
    coord_fixed(xlim=c(-120, 120), ylim=c(-120, 120)) +
    geom_segment(aes(x=x, xend=xend, y=y, yend=yend),
                 data=samples_lines, linetype='dashed', color=line_color) +
    theme_classic() +
    theme(axis.title=element_blank())

samples_svd_plt <- samples_svd_df %>%
    ggplot(aes(x=x, y=y)) +
    geom_point(size=1, color=point_color) +
    geom_point(aes(x, y, color=as.factor(seq(length(points_idx)))),
               data=points_svd_df, show.legend=F, size=2) +
    coord_fixed(xlim=c(-0.2, 0.2), ylim=c(-0.2, 0.2)) +
    geom_vline(aes(xintercept=0), linetype='dashed', color=line_color) +
    geom_hline(aes(yintercept=0), linetype='dashed', color=line_color) +
    theme_classic() +
    theme(axis.title=element_blank())

mul_plt <- grid.arrange(samples_plt, samples_svd_plt, ncol=2)

ggsave('mahalanobis-distance.png',
       mul_plt, device = 'png',
       width = 8, height = 4, units = 'cm',
       dpi = 150, scale = 2)
