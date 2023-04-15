# 轮盘赌
library(virdis)
library(tikzDevice)

options(tikzDefaultEngine='pdftex')
options(tikzDocumentDeclaration='\\documentclass[tikz,crop,convert={outext=.png}]{standalone}')

l <- c('$x_1$', '$x_2$', '$x_3$', '$x_4$', '$x_5$', '$x_6$')
f <- c(100, 60, 60, 40, 30, 20)
p <- f / sum(f)
cp <- cumsum(p)

pie(p, labels=l, col=viridis(length(l)))

tikz('roulette-wheel.tex', width=3, height=3, standAlone=T)
pie(p, labels=l, col=viridis(length(l)))
dev.off()

system('pdflatex --shell-escape roulette-wheel.tex')
system('convert roulette-wheel.png -trim +repage roulette-wheel.png')
system('convert roulette-wheel.png -resize 200 roulette-wheel.png')
