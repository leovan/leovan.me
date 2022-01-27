library(EBImage)

blox_img <- readImage('../../../static/images/cn/2022-01-27-content-based-image-retrieval/blox.jpg')
blox_harris_corner_img <- readImage('../../../static/images/cn/2022-01-27-content-based-image-retrieval/blox-harris-corner.jpg')

blox_images <- combine(
    blox_img,
    blox_harris_corner_img
)

png(filename = '../../../static/images/cn/2022-01-27-content-based-image-retrieval/blox-raw-and-harris-corner.png', width = 6, height = 3, units = 'cm', res = 150)
old_par <- par()
par(mar = c(1, 1, 1, 1))
display(blox_images, method = 'raster', all = T, spacing = 30)
par(old_par)
dev.off()