library(tidyverse)
library(ggthemes)
library(showtext)

showtext_auto()

glove_100_df <- read_tsv('glove-100-angular-k-10.tsv')
sift_128_df <- read_tsv('sift-128-euclidean-k-10.tsv')

y_log_mb <- as.numeric(1:10 %o% 10^(0:5))

glove_p <- ggplot(glove_100_df) +
    geom_point(aes(x=recall, y=queries_per_sec, color=method)) +
    geom_line(aes(x=recall, y=queries_per_sec, color=method)) +
    scale_y_log10(limits=c(8, 1e5), minor_breaks=y_log_mb) +
    xlab('召回率') + ylab('每秒查询') + labs(color='') +
    scale_color_tableau(palette='Tableau 20') +
    theme(
        text=element_text(family='Source Han Sans')
    )

glove_p

ggsave('glove-100-k-10.png', glove_p, width=6, height=4, dpi=150)

sift_p <- ggplot(sift_128_df) +
    geom_point(aes(x=recall, y=queries_per_sec, color=method)) +
    geom_line(aes(x=recall, y=queries_per_sec, color=method)) +
    scale_y_log10(limits=c(1e1, 1e5), minor_breaks=y_log_mb) +
    xlab('召回率') + ylab('每秒查询') + labs(color='') +
    scale_color_tableau(palette='Tableau 20') +
    theme(
        text=element_text(family='Source Han Sans')
    )

sift_p

ggsave('sift-128-k-10.png', sift_p, width=6, height=4, dpi=150)
