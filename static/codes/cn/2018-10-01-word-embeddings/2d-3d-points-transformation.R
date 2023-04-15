# Load libraries
library(tidyverse)

# Some data
alpha <- seq(0, 2*pi, by = pi/50)

set.seed(112358)

big_cycle <- tibble(
    x = 10 * cos(alpha) + runif(length(alpha), 0, 1),
    y = 10 * sin(alpha) + runif(length(alpha), 0, 1),
    type = 'b'
)

small_cycle <- tibble(
    x = 5 * cos(alpha) + runif(length(alpha), 0, 1),
    y = 5 * sin(alpha) + runif(length(alpha), 0, 1),
    type = 's'
)

two_d_data <- bind_rows(big_cycle, small_cycle) %>% 
    mutate(type = as.factor(type))

# color palette
color_palette <- c('#F8766D', '#01BFC4')

# 2d plot
two_d_plot <- ggplot(two_d_data, aes(x=x, y=y)) +
    geom_point(aes(color = type), size = 1) +
    theme_bw() +
    theme(legend.position = 'none',
          panel.grid = element_blank(),
          rect = element_blank(),
          axis.text = element_blank(),
          axis.ticks = element_blank()) +
    labs(x = 'x', y = 'y') +
    scale_colour_manual(values = color_palette)
print(two_d_plot)
ggsave('2d-points.png',
       plot = two_d_plot, device = 'png',
       width = 6, height = 6, units = 'cm',
       dpi = 100, scale = 1)

# Kernel function
kernel_2d_to_3d <- function(two_d_data) {
    tibble(
        x = two_d_data$x ^ 2,
        y = two_d_data$y ^ 2,
        z = two_d_data$y,
        type = two_d_data$type
    )
}

# 3d data
three_d_data <- kernel_2d_to_3d(two_d_data)


# 3d plot
library(plot3D)

png(filename = '3d-points.png',
    width = 6, height = 6, units = 'cm', res = 100)

old_par <- par()
par(mar = c(0, 0, 0, 0))

with(three_d_data, {
    scatter3D(x, y, z, 
              colvar = as.integer(type),
              phi = 30, theta = 20,
              bty = 'g', pch = 20, cex = 0.5,
              colkey = F, col = color_palette)
    plain_x <- c(min(x), 0.5 * (max(x) - min(x)) + min(x), 
                 0.5 * (max(x) - min(x)) + min(x), min(x))
    plain_y <- c(0.5 * (max(y) - min(y)) + min(y), 0,
                 0, 0.5 * (max(y) - min(y)) + min(y))
    plain_z <- c(min(z), min(z),
                 max(z), max(z))
    polygon3D(plain_x, plain_y, plain_z, alpha = 0.6, add = TRUE)
})

par(old_par)

dev.off()
