library(tidyverse)
library(glue)
library(httr)
library(jsonlite)

#' 年份 转 年份可读文本
#' 
#' @param year 年份数值
#' @return 年份可读文本
gen_which_year <- function(year) {
    ifelse(is.na(year), '忘了是哪年', glue('{year} 年'))
}

#' 日期 格式化为 月-日
#' 
#' @param date 日期
#' @return 格式化后的 月-日
format_month_day <- function(date) {
    ifelse(is.na(date), '', glue(
        '{month}-{day}', month = month(date), day = day(date)))
}

#' 评分 转 星星
#' 
#' @param 评分 (十分制)
#' @return 星星 (五星制)
gen_stars_html <- function(rating) {
    ifelse(is.na(rating), '', glue(
        '<span class="star-rating" data-rating="{rating}"></span>',
        rating = rating / 2))
}

#' 根据 IMDB ID 获取 IMDB 评分
#'
#' @param imdb_id IMDB ID
#' @return IMDB 评分
get_imdb_rating <- function(imdb_id) {
    url <- glue('https://www.omdbapi.com/?apikey=31ee42cc&i={imdb_id}')
    res <- GET(url)
    res_json <- fromJSON(content(res, as = 'text'))
    
    res_json$imdbRating
}
get_imdb_rating <- Vectorize(get_imdb_rating)

#' 根据豆瓣 ID 获取豆瓣信息
#'
#' @param douban_id 豆瓣 ID
#' @return 豆瓣信息
get_douban_info <- function(douban_id) {
    url <- glue('https://api.douban.com/v2/movie/subject/{douban_id}')
    res <- GET(url)
    res_json <- fromJSON(content(res, as = 'text'))
    
    tibble(
        name_zh = res_json$title,
        name = res_json$original_title,
        directors = paste(res_json$directors$name, collapse=','),
        casts = paste(res_json$casts$name, collapse=','),
        countries = paste(res_json$countries, collapse=','),
        genres = paste(res_json$genres, collapse=','),
        douban_rating = res_json$rating$average)
}

#' 获取 SPAN HTML
#' 
#' @param span_class SPAN 类名
#' @param span_value SPAN 值
#' @return SPAN HTML
gen_span_html <- function(span_class, span_value) {
    glue('<span class="{span_class}">{span_value}</span>')
}

#' 获取 IMDB ID 的 HTML 代码
#' 
#' @param imdb_id IMDB ID
#' @return IMDB ID HTML 代码
gen_imdb_id_html <- function(imdb_id) {
    gen_span_html('imdb-id', imdb_id)
}

#' 获取 IMDB RATING 的 HTML 代码
#' 
#' @param douban_id IMDB RATING
#' @return IMDB RATING 的 HTML 代码
gen_imdb_rating_html <- function(imdb_rating, imdb_id) {
    if (is.na(imdb_rating)) {
        imdb_rating
    } else {
        link = glue('https://www.imdb.com/title/{imdb_id}')
        gen_linked_text_html(imdb_rating, link)
    }
}
gen_imdb_rating_html <- Vectorize(gen_imdb_rating_html)

#' 获取豆瓣 ID 的 HTML 代码
#' 
#' @param douban_id 豆瓣 ID
#' @return 豆瓣 ID HTML 代码
gen_douban_id_html <- function(douban_id) {
    gen_span_html('douban-id', douban_id)
}

#' 获取豆瓣 RATING 的 HTML 代码
#' 
#' @param douban_id 豆瓣 RATING
#' @return 豆瓣 RATING 的 HTML 代码
gen_douban_rating_html <- function(douban_rating, douban_id) {
    if (is.na(douban_rating)) {
        douban_rating
    } else {
        link = glue('https://movie.douban.com/subject/{douban_id}')
        gen_linked_text_html(douban_rating, link)
    }
}
gen_douban_rating_html <- Vectorize(gen_douban_rating_html)

#' 获取带超链接的文本
#' 
#' @param text 文本
#' @param link 超链接
#' @return 带超链接的文本
gen_linked_text_html <- function(text, link, target='_black') {
    if (is.na(link)) {
        text
    } else {
        glue('<a href="{link}" target="{target}">{text}</a>')
    }
}
gen_linked_text_html <- Vectorize(gen_linked_text_html)

#' 添加锚点
#' 
#' @param html HTML
#' @param anchor 锚点 ID
#' @return 带有锚点的 HTML
add_anchor <- function(html, anchor) {
    glue('<span id="{anchor}">{html}</span>')
}
