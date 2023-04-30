library(tidyverse)
library(glue)

#' 年份 转 年份可读文本
#'
#' @param y 年份数值
#' @return 年份可读文本
gen_which_year <- function(y) {
    y <- tryCatch({
        year(y)
    }, error = function(err) {
        y
    })

    if (is.na(y)) {
        y <- "忘了是哪年"
    } else if (is.numeric(y)) {
        y <- glue("{y} 年")
    }

    return(y)
}
gen_which_year <- Vectorize(gen_which_year)

#' 年份 转 年份排序
#'
#' @param y 年份数值
#' @return 年份排序
gen_which_year_order <- function(y) {
    y <- tryCatch({
        year(y)
    }, error = function(err) {
        y
    })

    if (is.numeric(y)) {
        y <- y
    } else if (y == "高中") {
        y <- 2004
    } else if (y == "大学") {
        y <- 2007
    } else {
        y <- NA
    }

    return(y)
}
gen_which_year_order <- Vectorize(gen_which_year_order)

#' 日期 格式化为 月-日
#'
#' @param date 日期
#' @return 格式化后的 月-日
format_month_day <- function(date) {
    ifelse(is.na(date), "", glue(
        "{month}-{day}", month = month(date), day = day(date)))
}

#' 获取 SPAN HTML
#'
#' @param span_class SPAN 类名
#' @param span_value SPAN 值
#' @return SPAN HTML
gen_span_html <- function(span_class, span_value) {
    glue("<span class=\"{span_class}\">{span_value}</span>")
}

#' 获取 IMDB ID 的 HTML 代码
#'
#' @param imdb_id IMDB ID
#' @return IMDB ID HTML 代码
gen_imdb_id_html <- function(imdb_id) {
    gen_span_html("imdb-id", imdb_id)
}

#' 获取 IMDB RATING 的 HTML 代码
#'
#' @param imdb_rating IMDB RATING
#' @param douban_id IMDB ID
#' @return IMDB RATING 的 HTML 代码
gen_video_imdb_rating_link_html <- function(imdb_rating, imdb_id) {
    if (is.na(imdb_rating) || is.na(imdb_id)) {
        imdb_rating
    } else {
        link <- glue("https://www.imdb.com/title/{imdb_id}")
        gen_linked_text_html(imdb_rating, link)
    }
}
gen_video_imdb_rating_link_html <- Vectorize(gen_video_imdb_rating_link_html)

#' 获取豆瓣 ID 的 HTML 代码
#'
#' @param douban_id 豆瓣 ID
#' @return 豆瓣 ID HTML 代码
gen_douban_id_html <- function(douban_id) {
    gen_span_html("douban-id", douban_id)
}

#' 获取豆瓣电影 LINK 的 HTML 代码
#'
#' @param douban_rating 豆瓣 RATING
#' @param douban_id 豆瓣 ID
#' @return 豆瓣电影 LINKG 的 HTML 代码
gen_video_douban_rating_link_html <- function(douban_rating, douban_id) {
    if (is.na(douban_rating) || is.na(douban_id)) {
        douban_rating
    } else {
        link <- glue("https://movie.douban.com/subject/{douban_id}")
        gen_linked_text_html(douban_rating, link)
    }
}
gen_video_douban_rating_link_html <- Vectorize(gen_video_douban_rating_link_html)

#' 获取豆瓣书籍 LINK 的 HTML 代码
#'
#' @param douban_rating 豆瓣 RATING
#' @param douban_id 豆瓣 ID
#' @return 豆瓣书籍 LINKG 的 HTML 代码
gen_book_douban_rating_link_html <- function(douban_rating, douban_id) {
    if (is.na(douban_rating) || is.na(douban_id)) {
        douban_rating
    } else {
        link <- glue("https://book.douban.com/subject/{douban_id}")
        gen_linked_text_html(douban_rating, link)
    }
}
gen_book_douban_rating_link_html <- Vectorize(gen_book_douban_rating_link_html)

#' 获取带超链接的文本
#'
#' @param text 文本
#' @param link 超链接
#' @return 带超链接的文本
gen_linked_text_html <- function(text, link, target="_black") {
    if (is.na(link)) {
        text
    } else {
        glue("<a href=\"{link}\" target=\"{target}\">{text}</a>")
    }
}
gen_linked_text_html <- Vectorize(gen_linked_text_html)

#' 添加锚点
#'
#' @param html HTML
#' @param anchor 锚点 ID
#' @return 带有锚点的 HTML
add_anchor <- function(html, anchor) {
    glue("<span id=\"{anchor}\">{html}</span>")
}

#' 清理 HTML 表格
#'
#' @param html HTML
#' @return 清理后 HTML 表格
clean_html_table <- function(html) {
    str_replace_all(html, "\\s+style=\"text-align:[a-zA-Z]+;\"", "")
}
