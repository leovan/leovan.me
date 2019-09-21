library(tidyverse)

results <- data.frame(
    team_num = c(
        14, 12, 2, 11, 8, 3, 15, 7, 9, 17,
        1, 13, 18, 5, 4, 10, 20, 21, 16, 6, 19),
    team_name = c(
        'AiCU', 'DIGLILOG', 'IUA.CAAS', 'The Automators', 'Automatoes',
        'Koifish', 'StomData', 'KyotoAgri', 'CPlant', 'Automato', 'Amazona',
        'Tomato Federation', 'Dewey eGardener', 'TOPmatoes', 'Tomatinators',
        'Rotterdam.AI', 'Saturnalia', 'Hitomato', 'RedMachine',
        'Human-AI Copperation', 'Cydonia'
    ),
    tc = c(
        16, 15.6, 14.4, 16.8, 17.6, 11.6, 16, 12.2, 15.6, 15,
        14.4, 14, 11.8, 15.8, 16.8, 16, 10.4, 8.8, 11.4, 9.6, 7.6
    ),
    s_ai = c(
        22.8, 23.1, 18, 21.6, 22.8, 14.4, 17.4, 12.9, 21.6, 21.3,
        19.5, 17.4, 12.6, 19.8, 15.6, 18.6, 16.2, 16.2, 14.4, 14.4, 4.8
    ),
    pr = c(
        50, 46, 42, 30, 24, 38, 27, 34, 21, 18,
        12, 9, 15, 3, 5, 2, 7, 8, 6, 4, 1
    ),
    np = c(
        154.5, 147.7, 120.5, 103.3, 94.4, 114.8, 95.3, 105.3, 92.0, 88.1,
        73.1, 63.4, 74.2, 22.7, 53.8, 20.6, 62.8, 63.2, 56.7, 26.8, 0.7
    ),
    stringsAsFactors = F
)

p_results <- data.frame(
    team_num = c(results$team_num, results$team_num),
    team_name = c(results$team_name, results$team_name),
    result =c(results$np, results$pr),
    result_type = c(rep('Net Profit', 21), rep('Points', 21))
)

library(ggsci)

ggplot(p_results) +
    geom_bar(
        aes(x=reorder(team_name, -result), y=result, fill=result_type),
        stat='identity', position = 'identity') +
    xlab('') + ylab('') +
    theme(
        text = element_text(family='Source Han Sans'),
        axis.title.x = element_blank(),
        axis.line.x = element_blank(),
        axis.ticks.x = element_blank(),
        axis.text.x = element_blank(),
        legend.title = element_blank(),
        legend.justification = c(1.2, 1.2),
        legend.position = c(1, 1)) +
    scale_fill_jco()

ggsave(
    'net-profit-and-points-results.png',
    width = 4, height = 2, dpi = 150, scale = 1.5)
