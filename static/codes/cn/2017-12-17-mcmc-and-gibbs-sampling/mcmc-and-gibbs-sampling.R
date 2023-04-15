# Load library
library(tidyverse)
library(ggforce)

# Estimate PI
r <- 2
center_x <- r
center_y <- r

## Plot 1
segment_margin <- r/4
p <- ggplot() +
    geom_rect(aes(xmin = 0, ymin = 0, xmax = 2*r, ymax = 2*r),
              fill = 'gray', color = 'black') +
    geom_circle(aes(x0 = center_x, y0 = center_y, r = r,
                    fill = r), fill = 'white', show.legend = F) +
    geom_segment(aes(x = center_x, y = center_y,
                     xend = center_x + r, yend = center_y),
                 arrow = arrow(angle = 20, length = unit(0.15, 'inches')),
                 size = 0.6) +
    annotate('text', x = center_x + r/2, y = center_y + r/6,
             label = 'italic(r)', size = 6, parse = T) +
    coord_fixed() +
    theme_void()
print(p)

ggsave('../../static/images/cn/2017-12-17-mcmc-and-gibbs-sampling/mc-pi.png', p, device = 'png',
       width = 6, height = 6, units = 'cm',
       dpi = 150, scale = 1)

## Plot 2
distance <- function(point_x, point_y, center_x, center_y) {
    sqrt((point_x - center_x)^2 + (point_y - center_y)^2)
}

points_generator <- function(size) {
    set.seed(112358)
    points_x <- runif(size, min = 0, max = 2*r)
    points_y <- runif(size, min = 0, max = 2*r)

    tibble(
        x = points_x,
        y = points_y,
        in_cycle = ifelse(
            distance(points_x, points_y, center_x, center_y) > r, 0, 1)
    )
}

sizes <- c(1000, 10000, 100000, 1000000, 10000000)
estimated_pi <- sapply(sizes, function(size) {
    points <- points_generator(size)
    sum(points$in_cycle) * 4 / size
})
print(estimated_pi)

points <- points_generator(1000)
p <- ggplot() +
    geom_point(aes(x = x, y = y, color = as.factor(in_cycle)),
               data = points, size = 1, show.legend = F) +
    geom_circle(aes(x0 = center_x, y0 = center_y, r = r)) +
    coord_fixed() +
    theme_void()
print(p)

ggsave('../../static/images/cn/2017-12-17-mcmc-and-gibbs-sampling/mc-pi-simulation.png', p, device = 'png',
       width = 6, height = 6, units = 'cm',
       dpi = 150, scale = 1)

# Markov Chain
p <- matrix(c(0.65, 0.28, 0.07,
              0.15, 0.67, 0.18,
              0.12, 0.36, 0.52),
            3, 3, byrow = T)
pi <- matrix(c(0.21, 0.68, 0.11), 1, 3, byrow = T)

for (i in 1:10) {
    pi_current <- pi[i, ]
    pi_next <- pi_current %*% p
    pi <- rbind(pi, pi_next)
}

colnames(pi) <- c('下层', '中层', '上层')
rownames(pi) <- 0:10
print(pi)

pi <- matrix(c(0.75, 0.15, 0.1), 1, 3, byrow = T)

for (i in 1:10) {
    pi_current <- pi[i, ]
    pi_next <- pi_current %*% p
    pi <- rbind(pi, pi_next)
}

colnames(pi) <- c('下层', '中层', '上层')
rownames(pi) <- 0:10
print(pi)

# Gibbs Sampling
library(tidyverse)
library(grid)
library(gridExtra)
library(animation)

mu_x <- 0
mu_y <- 0
sigma_x <- 10
sigma_y <- 1
rho <- 0.8

iter <- 1000
samples <- matrix(c(mu_x, mu_y), 1, 2, byrow = T)

set.seed(112358)
for (i in 1:iter) {
    sample_x <- mu_x +
        sigma_x * rho * (samples[i, 2] - mu_y) / sigma_y +
        sigma_x * sqrt(1 - rho^2) * rnorm(1)
    sample_y <- mu_y +
        sigma_y * rho * (sample_x - mu_x) / sigma_x +
        sigma_y * sqrt(1 - rho^2) * rnorm(1)
    samples <- rbind(samples, c(sample_x, sample_y))
}

samples_df <- as.data.frame(samples)
colnames(samples_df) <- c('x', 'y')

frame_plot <- function(samples) {
    p_samples <- ggplot(samples) +
        geom_point(aes(x, y)) +
        xlim(-40, 40) + ylim(-4, 4) +
        theme(text = element_text(size = 20))
    p_samples_ <- ggplot_gtable(ggplot_build(p_samples))
    
    p_density_x <- ggplot(samples) +
        geom_histogram(aes(x = x, y = ..density..),
                       bins = 30, color = 'grey', fill = 'grey') +
        stat_function(fun = dnorm, n = iter,
                      args = list(mean = mu_x, sd = sigma_x)) +
        xlim(-40, 40) +
        coord_cartesian(ylim = c(0, 0.05)) +
        theme_void() +
        theme(axis.text = element_blank(),
              axis.title = element_blank(),
              axis.ticks = element_blank())
    p_density_x_ <- ggplot_gtable(ggplot_build(p_density_x))
    
    p_density_y <- ggplot(samples) +
        geom_histogram(aes(x = y, y = ..density..),
                       bins = 30, boundary = 0,
                       color = 'grey', fill = 'grey') +
        stat_function(fun = dnorm, n = iter,
                      args = list(mean = mu_y, sd = sigma_y)) +
        xlim(-4, 4) +
        coord_flip(ylim = c(0, 0.4)) +
        theme_void() +
        theme(axis.text = element_blank(),
              axis.title = element_blank(),
              axis.ticks = element_blank())
    p_density_y_ <- ggplot_gtable(ggplot_build(p_density_y))
    
    p_empty <- ggplot() + theme_void()
    
    width_max <- unit.pmax(p_samples_$widths[2:3],
                           p_density_x_$widths[2:3])
    height_max <- unit.pmax(p_samples_$heights[7:8],
                            p_density_y_$heights[7:8])
    
    p_samples_$widths[2:3] <- width_max
    p_density_x_$widths[2:3] <- width_max
    p_samples_$heights[7:8] <- height_max
    p_density_y_$heights[7:8] <- height_max
    
    grid.arrange(p_density_x_, p_empty,
                 p_samples_, p_density_y_,
                 ncol = 2, nrow = 2,
                 widths = c(4, 1), heights = c(1, 4))
}

saveGIF({
    ani.options(nmax = iter)
    steps <- 10
    for (i in seq(steps, iter, by = steps)) {
        samples_df %>% slice(1:i) %>% frame_plot()
        ani.pause()
    }
}, interval = 0.001, movie.name =
    'gibbs-sampling-bivariate-guassian-distribution.gif',
ani.width = 600, ani.height = 600)

samples_df %>% slice(1:10) %>% frame_plot()
samples_df %>% frame_plot()
