library(lubridate)
library(glue)
library(httr)
library(jsonlite)

#' 年份 转 年份可读文本
#' 
#' @param year 年份数值
#' @return 年份可读文本
which_year_ <- function(year) {
    ifelse(is.na(year), '忘了是哪年', glue('{year} 年'))
}

#' 日期 格式化为 月-日
#' 
#' @param date 日期
#' @return 格式化后的 月-日
date_month_day_format_ <- function(date) {
    ifelse(is.na(date), '', glue('{month}-{day}', month = month(date), day = day(date)))
}

#' 评分 转 星星
#' 
#' @param 评分 (十分制)
#' @return 星星 (五星制)
stars_ <- function(rating) {
    ifelse(is.na(rating), '', glue('<span class="star-rating" data-rating="{rating}"></span>',
                                   rating = rating / 2))
}

#' 根据 IMDB ID 获取 IMDB 评分
#'
#' @param imdb_id IMDB ID
#' @return IMDB 评分
imdb_rating_ <- function(imdb_id) {
    url <- glue('https://www.omdbapi.com/?apikey=31ee42cc&i={imdb_id}')
    res <- GET(url)
    res_json <- fromJSON(content(res, as = 'text'))
    rating <- res_json$imdbRating
    
    list(rating = rating, html = glue('<span class="imdb-rating"></span>'))
}

#' 根据豆瓣 ID 获取豆瓣评分
#'
#' @param douban_id 豆瓣 ID
#' @return 豆瓣评分
douban_rating_ <- function(douban_id) {
    url <- glue('https://api.douban.com/v2/movie/subject/{douban_id}')
    res <- GET(url)
    res_json <- fromJSON(content(res, as = 'text'))
    rating <- res_json$rating$average
    
    list(rating = rating, html = glue('<span class="douban-rating"></span>'))
}

#' 获取 IMDB ID 的 HTML 代码
#' 
#' @param imdb_id IMDB ID
#' @return IMDB ID HTML 代码
imdb_id_html_ <- function(imdb_id) {
    glue('<span class="imdb-id">{imdb_id}</span>')
}

#' 获取豆瓣 ID 的 HTML 代码
#' 
#' @param douban_id 豆瓣 ID
#' @return 豆瓣 ID HTML 代码
douban_id_html_ <- function(douban_id) {
    glue('<span class="douban-id">{douban_id}</span>')
}

#' 获取带超链接的文本
#' 
#' @param text 文本
#' @param link 超链接
#' @return 带超链接的文本
linked_text_ <- function(text, link) {
    ifelse(is.na(link), text, text_spec(text, link = link))
}
