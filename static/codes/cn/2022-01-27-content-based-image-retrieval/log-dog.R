library(tidyverse)
library(showtext)

gaussian_func <- function(x, y, sigma) {
    return(1 / (2 * pi * sigma ^ 2) * exp(- (x ^ 2 + y ^ 2) / (2 * sigma ^ 2)))
}

laplacian_func <- function(x, y, sigma) {
    return((-2 * sigma ^ 2 + x ^ 2 + y ^ 2) / (2 * pi * sigma ^ 6) * (exp(- (x ^ 2 + y ^ 2) / (2 * sigma ^ 2))))
}

dog_func <- function(x, y, sigma, k) {
    return(gaussian_func(x, y, k * sigma) - gaussian_func(x, y, sigma))
}

x <- seq(-8, 8, 0.01)
sigma <- 1.6
k <- sqrt(2)
laplacian_y <- laplacian_func(x, 0, sigma)
dog_y <- dog_func(x, 0, sigma, k)

laplacian_df <- tibble(
    x = x,
    y = laplacian_y,
    type = 'LoG'
)
dog_df <- tibble(
    x = x,
    y = dog_y,
    type = 'DoG'
)
plot_df <- rbind(laplacian_df, dog_df)

p <- ggplot(plot_df) +
    geom_line(aes(x, y, color = type)) +
    geom_vline(xintercept = 0) +
    geom_hline(yintercept = 0) +
    xlab('') + ylab('') +
    labs(color='') +
    theme_minimal() +
    theme(
        legend.position = c(0.8, 0.2),
        legend.title = element_blank(),
        legend.background = element_rect(linetype='solid')
    )
print(p)

ggsave('../../../static/images/cn/2022-01-27-content-based-image-retrieval/log-dog.png', p, width=4, height=3, dpi=120)