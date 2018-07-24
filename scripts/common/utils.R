library(tidyverse)
library(glue)
library(httr)
library(jsonlite)
library(rvest)

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

#' 根据 IMDB ID 获取 IMDB 评分
#'
#' @param imdb_id IMDB ID
#' @return IMDB 评分
get_imdb_rating <- function(imdb_id) {
    rating <- NA
    
    if (!is.na(imdb_id)) {
        url <- glue('https://www.omdbapi.com/?apikey=31ee42cc&i={imdb_id}')
        
        tryCatch({
            res <- GET(url)
            res_json <- fromJSON(content(res, as = 'text'))
            
            if (res_json$Response == 'True') {
                rating <- res_json$imdbRating
                
                if (rating == 'N/A') {
                    rating <- NA
                }
            }
        }, error = function(e) {
            print(imdb_id)
            stop(e)
        })
    }
    
    rating
}
get_imdb_rating <- Vectorize(get_imdb_rating)

#' 根据豆瓣 ID 获取豆瓣信息
#'
#' @param douban_id 豆瓣 ID
#' @return 豆瓣信息
get_douban_info <- function(douban_id) {
    info <- tibble(
        name_zh = NA, name = NA, directors = NA, casts = NA, countries = NA,
        genres = NA, douban_rating = NA)
    
    if (!is.na(douban_id)) {
        url <- glue('https://api.douban.com/v2/movie/subject/{douban_id}')
        
        tryCatch({
            res <- GET(url)
            res_json <- fromJSON(content(res, as = 'text'))
            
            if (res_json$code == 200) {
                info$name_zh <- res_json$title
                info$name <- res_json$original_title
                info$directors <- paste(res_json$directors$name, collapse=',')
                info$casts <- paste(res_json$casts$name, collapse=',')
                info$countries <- paste(res_json$countries, collapse=',')
                info$genres <- paste(res_json$genres, collapse=',')
                info$douban_rating <- res_json$rating$average
            }
        }, error = function(e) {
            print(douban_id)
        })
    }
    
    info
}

#' 根据豆瓣 ID 爬取豆瓣信息
#'
#' @param douban_id 豆瓣 ID
#' @return 豆瓣信息
crawl_douban_info <- function(douban_id) {
    info <- tibble(
        name_zh = NA, name = NA, directors = NA, casts = NA, countries = NA,
        genres = NA, release_date = NA, douban_rating = NA)
    
    if (!is.na(douban_id)) {
        url <- glue('https://movie.douban.com/subject/{douban_id}')
        
        tryCatch({
            ua <- 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
            session <- html_session(url, user_agent(ua))
            
            name_all <- session %>%
                html_nodes("#content h1 span") %>%
                first %>%
                html_text()
            name_all <- name_all %>% str_split(' ', simplify = T)
            if (length(name_all) == 1) {
                info$name_zh = name_all
                info$name = name_all
            } else {
                info$name_zh = name_all[1]
                info$name = paste(name_all[2:length(name_all)], collapse=' ')
            }
            
            directors <- session %>%
                html_nodes('a[rel="v:directedBy"]') %>%
                html_text()
            info$directors <- paste(directors, collapse=',')
            
            casts <- session %>%
                html_nodes('a[rel="v:starring"]') %>%
                html_text()
            info$casts <- paste(casts, collapse=',')
            
            countries <- session %>%
                html_nodes('#info') %>%
                html_text() %>%
                str_replace_all('\n', '') %>%
                str_replace('.+制片国家/地区: ', '') %>%
                str_replace('语言: .+', '') %>%
                str_split(' / ', simplify = T)
            info$countries <- paste(countries, collapse=',')
            
            genres <- session %>%
                html_nodes('span[property="v:genre"]') %>%
                html_text()
            info$genres <- paste(genres, collapse=',')
            
            release_date <- session %>%
                html_nodes('span[property="v:initialReleaseDate"]') %>%
                html_text() %>%
                str_replace_all('\\(.+\\)', '') %>%
                min()
            info$release_date <- as.Date(release_date, format='%Y-%m-%d')
            
            douban_rating <- session %>%
                html_nodes('strong[property="v:average"]') %>%
                html_text()
            info$douban_rating <- douban_rating
        }, error = function(e) {
            print(douban_id)
        })
    }
    
    # 防止被反爬
    Sys.sleep(2)
    
    info
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
#' @param imdb_rating IMDB RATING
#' @param douban_id IMDB ID
#' @return IMDB RATING 的 HTML 代码
gen_imdb_rating_html <- function(imdb_rating, imdb_id) {
    if (is.na(imdb_rating) || is.na(imdb_id)) {
        imdb_rating
    } else {
        link <- glue('https://www.imdb.com/title/{imdb_id}')
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
#' @param douban_rating 豆瓣 RATING
#' @param douban_id 豆瓣 ID
#' @return 豆瓣 RATING 的 HTML 代码
gen_douban_rating_html <- function(douban_rating, douban_id) {
    if (is.na(douban_rating) || is.na(douban_id)) {
        douban_rating
    } else {
        link <- glue('https://movie.douban.com/subject/{douban_id}')
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
