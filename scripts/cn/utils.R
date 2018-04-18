library(RCurl)
library(rjson)

#' 年份 转 年份可读文本
#' 
#' @param year 年份数值
#' @return 年份可读文本
which_year_ <- function(year) {
    ifelse(is.na(year), '忘了是哪年', paste0(year, ' 年'))
}

#' 日期 格式化为 月-日
#' 
#' @param date 日期
#' @return 格式化后的 月-日
date_month_day_format_ <- function(date) {
    ifelse(is.na(date), '', paste(month(date), day(date), sep = '-'))
}

#' 评分 转 星星
#' 
#' @param 评分 (十分制)
#' @return 星星 (五星制)
stars_ <- function(rating) {
    ifelse(is.na(rating), '', paste0('<div class="star-rating" data-rating="', rating / 2, '"></div>'))
}

#' 根据 IMDB ID 获取 IMDB 评分
#'
#' @param imdb_id IMDB ID
#' @return IMDB 评分
imdb_rating_ <- function(imdb_id) {
    url <- paste0('http://www.theimdbapi.org/api/movie?movie_id=', imdb_id)
    res <- getURL(url)
    res_json <- fromJSON(res)
    res_json$rating
}

#' 根据豆瓣 ID 获取豆瓣评分
#'
#' @param douban_id 豆瓣 ID
#' @return 豆瓣评分
douban_rating_ <- function(douban_id) {
    url <- paste0('https://api.douban.com/v2/movie/subject/', douban_id)
    res <- getURL(url)
    res_json <- fromJSON(res)
    res_json$rating$average
}
