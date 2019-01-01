library(dtw)

data('aami3a')

query <- window(aami3a, start=2.7, end=5)
reference <- window(aami3a, start=0, end=2)

idx <- seq(0, 6.28, len=100)
query <- sin(idx) + runif(100)/10
reference <- cos(idx)

alignment <- dtw(query, reference, step=asymmetric, keep=T)

png('dtw-twoway.png', width=600, height=400, units='px', pointsize=16)
par(mar=c(1, 1, 1, 1))
plot(alignment, type='twoway', off=-2, match.indices=20)
dev.off()

hq <- (0:8)/8
hq <- round(hq*100)      #  indices in query for  pi/4 .. 7/4 pi
hw <- (alignment$index1 %in% hq)   # where are they on the w. curve?
hi <- (1:length(alignment$index1))[hw]   # get the indices of TRUE elems
alignment <- dtw(query, reference, step=asymmetric, keep=T)

png('dtw-threeway.png', width=600, height=600, units='px', pointsize=16)
par(mar=c(1, 1, 1, 1))
plot(alignment, type='threeway', match.indices=hi)
dev.off()
