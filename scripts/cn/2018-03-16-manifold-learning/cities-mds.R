library(maps)
library(mapdata)
library(psych)

# 中国城市信息
cities <- data.frame(
    name = c('北京', '上海', '天津', '重庆', '哈尔滨', '长春', '沈阳',
             '呼和浩特', '石家庄', '太原', '济南', '郑州', '西安', '兰州',
             '银川', '西宁', '乌鲁木齐', '合肥', '南京', '杭州', '长沙',
             '南昌', '武汉', '成都', '贵阳', '福州', '台北', '广州', '海口',
             '南宁', '昆明', '拉萨', '香港', '澳门'),
    longitude = c(116.4666667, 121.4833333, 117.1833333, 106.5333333, 
                  126.6833333, 125.3166667, 123.4, 111.8, 114.4666667, 
                  112.5666667, 117, 113.7, 108.9, 103.8166667, 106.2666667, 
                  101.75, 87.6, 117.3, 118.8333333, 120.15, 113, 115.8666667, 
                  114.35, 104.0833333, 106.7, 119.3, 121.5166667, 113.25, 
                  110.3333333, 108.3333333, 102.6833333, 91.16666667, 
                  114.1666667, 113.5),
    latitude = c(39.9, 31.23333333, 39.15, 29.53333333, 45.75, 43.86666667, 
                 41.83333333, 40.81666667, 38.03333333, 37.86666667, 
                 36.63333333, 34.8, 34.26666667, 36.05, 38.33333333, 
                 36.63333333, 43.8, 31.85, 32.03333333, 30.23333333, 
                 28.18333333, 28.68333333, 30.61666667, 30.65, 26.58333333, 
                 26.08333333, 25.05, 23.13333333, 20.03333333, 22.8, 25, 
                 29.66666667, 22.3, 22.2),
    label_pos = c(2, 4, 4, 4, 3, 4, 2, 3, 4, 2, 4, 2, 2, 4, 3, 2, 1, 3, 1, 1, 
                  2, 3, 2, 2, 1, 2, 4, 3, 1, 2, 2, 4, 4, 2)
)

# 距离信息
cities_dist <- dist(cities[, c('longitude', 'latitude')])

# MDS
mds_points <- cmdscale(cities_dist, k = 2)
mds_points[, 1] <- -mds_points[, 1]
mds_points <- rescale(mds_points, 
                      apply(cities[, c('longitude', 'latitude')], 2, mean),
                      apply(cities[, c('longitude', 'latitude')], 2, sd))
names(mds_points) <- c('longitude', 'latitude')

# 绘图
svg('cities-mds.svg', width=10, height=7)

par(family = 'Source Han Serif CN')
par(mar = c(0, 0, 0, 0))

map('china', col='darkgray', ylim=c(18, 54), panel.first=grid())
points(cities$longitude, cities$latitude, pch=19, col=rgb(0, 0, 0, 0.5))
text(cities$longitude, cities$latitude, cities$name,
     cex=0.9, col=rgb(0, 0, 0, 0.7), pos=cities$label_pos)
points(mds_points$longitude, mds_points$latitude,
       pch=19, col=rgb(0, 0, 1, 0.5))
text(mds_points$longitude, mds_points$latitude, cities$name,
     cex=0.9, col=rgb(0, 0, 1, 0.7), pos=cities$label_pos)

dev.off()
