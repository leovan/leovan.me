# Load libraries
library(EBImage)

# EVD
A <- matrix(c(3, -2, -0.9, 0,
              -2, 4, 1, 0,
              0, 0, -1, 0,
              -0.5, -0.5, 0.1, 1),
            4, 4, byrow = T)
A_eig <- eigen(A)
print(A_eig)

A_re <- A_eig$vectors %*%
    diag(A_eig$values) %*%
    solve(A_eig$vectors)
print(A_re)

save_width <- 256
save_hegith <- 256

# RGB image
lena_std <- readImage('../../static/images/cn/2017-12-11-evd-svd-and-pca/lena-std.tif')
writeImage(resize(lena_std, save_width, save_hegith),
           '../../static/images/cn/2017-12-11-evd-svd-and-pca/lena-std.png')

# Gray image
lena_gray <- channel(lena_std, 'gray')

# SVD
lena_gray_svd <- svd(lena_gray)
u <- lena_gray_svd$u
v <- lena_gray_svd$v
d <- diag(lena_gray_svd$d)

# Reconstruction
lena_gray_20_20 <- u[, 1:20] %*% d[1:20, 1:20] %*% t(v[, 1:20])
lena_gray_50_100 <- u[, 1:50] %*% d[1:50, 1:100] %*% t(v[, 1:100])
lena_gray_200_200 <- u[, 1:200] %*% d[1:200, 1:200] %*% t(v[, 1:200])

# Display 4 images
lena_images <- combine(
    lena_gray,
    lena_gray_20_20,
    lena_gray_50_100,
    lena_gray_200_200
)
png(filename = '../../static/images/cn/2017-12-11-evd-svd-and-pca/lena-reconstruction.png',
    width = 6, height = 6, units = 'cm', res = 150)
old_par <- par()
par(mar = c(1, 1, 1, 1))
display(lena_images, method = 'raster', all = T, spacing = 30)
par(old_par)
dev.off()

# PCA demo
x <- matrix(c(-1, -1, 0, 0, 2,
              -2, 0, 0, 1, 1),
            5, 2, byrow = F)
x_pca <- prcomp(x)
print(x_pca)
summary(x_pca)
x_ <- predict(x_pca, x)
print(x_)
