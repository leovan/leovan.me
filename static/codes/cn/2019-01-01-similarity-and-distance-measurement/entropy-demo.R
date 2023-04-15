library(tidyverse)
library(ggplot2)

entropy <- function(p) {
    -p * log(p) - (1-p) * log(1-p)
}

x = seq(0, 1, by=0.01)
entropy_df <- data.frame(
    x = x,
    y = entropy(x)
)

entropy_plt <- entropy_df %>%
    ggplot(aes(x=x, y=y)) +
    geom_path() +
    xlab('p') + ylab('H(X)') +
    theme_classic() +
    theme(text=element_text(family=''))

ggsave('entropy-demo.png', entropy_plt,
       width = 3, height = 2, units = 'cm',
       dpi = 100, scale = 3)
