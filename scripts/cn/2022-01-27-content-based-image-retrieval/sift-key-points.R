library(EBImage)

home_img <- readImage('../../../static/images/cn/2022-01-27-content-based-image-retrieval/home.jpg')
home_sift_key_points_img <- readImage('../../../static/images/cn/2022-01-27-content-based-image-retrieval/home-sift-key-points.jpg')

home_images <- combine(
    home_img,
    home_sift_key_points_img
)

png(filename = '../../../static/images/cn/2022-01-27-content-based-image-retrieval/home-raw-and-sift-key-points.png', width = 14, height = 5, units = 'cm', res = 150)
old_par <- par()
par(mar = c(1, 1, 1, 1))
display(home_images, method = 'raster', all = T, spacing = 30)
par(old_par)
dev.off()