library(tidyverse)
library(maps)
library(mapdata)
library(animation)
library(glue)

city_coordinate <- read_tsv('city-coordinate.tsv')
city_path <- read_tsv('city-path.tsv', col_types='cd')
label_pos = c(2, 4, 4, 4, 3, 4, 2, 3, 4, 2, 4, 2, 2, 4, 3, 2, 1, 3, 1, 1, 
              2, 3, 2, 2, 1, 2, 4, 3, 1, 2, 2, 4, 4, 2)

plot_path <- function(path_str, fitness, iter) {
    map('china', col='darkgray', ylim=c(18, 54), panel.first=grid())
    points(city_coordinate$longitude, city_coordinate$latitude,
           pch=19, col=rgb(0, 0, 0, 0.5))
    text(city_coordinate$longitude, city_coordinate$latitude, city_coordinate$city,
         cex=0.9, col=rgb(0, 0, 0, 0.7), pos=label_pos)
    
    path = str_split(path_str, ',', simplify=T)
    path = as.numeric(path)
    
    for (i in 0:(length(path)-1)) {
        segments(city_coordinate$longitude[path[i+1] + 1],
                 city_coordinate$latitude[path[i+1] + 1],
                 city_coordinate$longitude[path[(i+1) %% length(path) + 1] + 1],
                 city_coordinate$latitude[path[(i+1) %% length(path) + 1] + 1],
                 col='red', lwd=2, lty=3)
    }
    
    text(75, 21, glue('Iter: {iter}, Distance: {fitness} km'), pos=4)
}

iters = seq(1, 1000, by=10)

saveGIF({
    for (iter in iters) {
        par(family = 'Source Han Serif CN')
        par(mar = c(0, 0, 0, 0))
        plot_path(city_path$path[iter], as.integer(city_path$fitness[iter] / 1000), iter)
    }
}, interval = 0.1, movie.name = 'ga-tsp.gif', ani.width = 600, ani.height = 420)

system('gifsicle -O3 ga-tsp.gif -o ga-tsp.gif')
