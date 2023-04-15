library(tidyverse)
library(gridExtra)
library(showtext)
font_add('Source Han Serif SC', 'SourceHanSerif.ttc')

set.seed(112358)

sne_crowding <- function(n_points=1000, dims=c(2, 3, 5, 10)) {
    dims %>% map(function(dim_) {
        1:dim_ %>% set_names(paste0('d_', 1:dim_)) %>% map_dfc(function(col_) {
            # 为了保证过滤后点的数量，在此多生成一些点
            runif(n_points * dim_^ 3)
        })
    }) %>% map(function(df) {
        dist_ <- df %>% mutate_all(funs(.^2)) %>% rowSums %>% sqrt %>% as_tibble
        colnames(dist_) <- c('distance')
        dist_ %>% filter(distance < 1.0) %>% slice(1:n_points)
    })
}

sne_crowding_plot <- function(df, title) {
    ggplot(df, aes(distance)) +
        geom_histogram(bins=50) + ggtitle(title) + xlim(c(0, 1)) +
        theme(text = element_text(family = 'Source Han Serif SC'))
}

sne_crowding_res <- sne_crowding()
sne_crowding_fig <- arrangeGrob(
    sne_crowding_plot(sne_crowding_res[[1]], '2 维'),
    sne_crowding_plot(sne_crowding_res[[2]], '3 维'),
    sne_crowding_plot(sne_crowding_res[[3]], '4 维'),
    sne_crowding_plot(sne_crowding_res[[4]], '10 维'),
    ncol = 2, nrow = 2)
ggsave('sne-crowding.png', sne_crowding_fig, device = 'png',
       width = 4, height = 4, units = 'cm', dpi = 100, scale = 3)

distance <- seq(0, 5, 0.01)
gassion_p <- dnorm(distance)
t_p <- dt(distance, 1)

probability_df <- tibble(
    distance = distance,
    gassion = gassion_p,
    t = t_p
)
names(probability_df) <- c('distance', 'Gassion 分布', 't 分布')

probability_df <- gather(probability_df, distribution, probability, -distance)

probability_fig <- ggplot(probability_df, aes(distance, probability)) +
    geom_line(aes(color=distribution)) +
    theme(legend.justification=c(1, 1), legend.position=c(1, 1))+
    theme(text = element_text(family = 'Source Han Serif SC'))
ggsave('gassion-t-comparison.png', probability_fig, device = 'png',
       width = 4, height = 3, units = 'cm', dpi = 100, scale = 3)

