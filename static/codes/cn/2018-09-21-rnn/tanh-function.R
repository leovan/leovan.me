library(tidyverse)
library(showtext)
font_add('Source Han Serif SC', 'SourceHanSerif.ttc')

tanhd <- deriv(y ~ tanh(x), 'x', func = T)
x = seq(-3, 3, by = 0.01)

tanh_df <- tibble(x = x, y = tanh(x), `function` = 'tanh')
tanhd_df <- tibble(x = x, y = c(attr(tanhd(x), 'gradient')), `function` = 'tanh\'')

df <- tanh_df %>% union_all(tanhd_df)

fig <- ggplot(df, aes(x, y)) +
    geom_path(aes(color = `function`)) +
    theme(legend.justification=c(1, 0), legend.position=c(.95, .05)) +
    theme(text = element_text(family = 'Source Han Serif SC')) +
    theme(axis.title = element_blank())
ggsave('tanh-function.png', fig, device = 'png',
       width = 3, height = 2, units = 'cm', dpi = 100, scale = 3)
