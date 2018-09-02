library(EBImage)

filter_identity_img <- readImage('../../../static/images/cn/2018-08-25-cnn/lena-filter-identity.png')
filter_edge_img <- readImage('../../../static/images/cn/2018-08-25-cnn/lena-filter-edge.png')
filter_sharpen_img <- readImage('../../../static/images/cn/2018-08-25-cnn/lena-filter-sharpen.png')
filter_gaussian_blur_img <- readImage('../../../static/images/cn/2018-08-25-cnn/lena-filter-gaussian-blur.png')

lena_images <- combine(
    filter_identity_img,
    filter_edge_img,
    filter_sharpen_img,
    filter_gaussian_blur_img
)
png(filename = '../../../static/images/cn/2018-08-25-cnn/lena-filters.png',
    width = 6, height = 6, units = 'cm', res = 150)
old_par <- par()
par(mar = c(1, 1, 1, 1))
display(lena_images, method = 'raster', all = T, spacing = 30)
par(old_par)
dev.off()
