library(tidyverse)
library(glue)
library(httr)
library(jsonlite)
library(rvest)

ua <- 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'

#' 年份 转 年份可读文本
#' 
#' @param y 年份数值
#' @return 年份可读文本
gen_which_year <- function(y) {
    y = tryCatch({
        year(y)
    }, error = function(err) {
        y
    })
    
    if (is.na(y)) {
        y = '忘了是哪年'
    } else if (is.numeric(y)) {
        y = glue('{y} 年')
    }
    
    y
}
gen_which_year = Vectorize(gen_which_year)

#' 年份 转 年份排序
#' 
#' @param y 年份数值
#' @return 年份排序
gen_which_year_order <- function(y) {
    y = tryCatch({
        year(y)
    }, error = function(err) {
        y
    })
    
    if (is.numeric(y)) {
        y = y
    } else if (y == '高中') {
        y = 2004
    } else if (y == '大学') {
        y = 2007
    } else {
        y = NA
    }
    
    y
}
gen_which_year_order <- Vectorize(gen_which_year_order)

#' 日期 格式化为 月-日
#' 
#' @param date 日期
#' @return 格式化后的 月-日
format_month_day <- function(date) {
    ifelse(is.na(date), '', glue(
        '{month}-{day}', month = month(date), day = day(date)))
}

#' 根据 IMDB ID 获取电影 IMDB 评分
#'
#' @param imdb_id IMDB ID
#' @return 电影 IMDB 评分
get_movie_imdb_rating <- function(imdb_id) {
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
get_movie_imdb_rating <- Vectorize(get_movie_imdb_rating)

#' 根据豆瓣 ID 爬取豆瓣电影信息
#'
#' @param douban_id 豆瓣 ID
#' @return 豆瓣电影信息
crawl_movie_douban_info <- function(douban_id) {
    info <- tibble(
        name_zh = NA, name = NA, directors = NA, casts = NA, countries = NA,
        genres = NA, release_date = NA, douban_rating = NA)
    
    if (!is.na(douban_id)) {
        url <- glue('https://movie.douban.com/subject/{douban_id}')
        
        tryCatch({
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

#' 根据豆瓣 ID 爬取豆瓣书籍信息
#'
#' @param douban_id 豆瓣 ID
#' @return 豆瓣书籍信息
crawl_book_douban_info <- function(douban_id) {
    info <- tibble(
        title_zh = NA, title = NA, author = NA, publisher = NA, 
        published_date = NA, pages = NA, douban_rating = NA)
    
    if (!is.na(douban_id)) {
        url <- glue('https://book.douban.com/subject/{douban_id}')
        
        tryCatch({
            session <- html_session(url, user_agent(ua))
            
            info$title_zh <- session %>%
                html_node('span[property="v:itemreviewed"]') %>%
                html_text()
            
            info$douban_rating <- session %>%
                html_node('strong[property="v:average"]') %>%
                html_text(trim=T)
            
            info_text <- session %>%
                html_node('#info') %>%
                html_text(trim=T) %>%
                str_replace_all('\n', '') %>%
                str_replace_all('\\s+', ' ') %>% 
                str_replace_all('【', '[') %>%
                str_replace_all('】', ']') %>%
                str_replace_all('•', '·')
            info_text_v <- session %>%
                html_node('#info') %>%
                html_children() %>%
                html_text(trim=T) %>%
                str_replace_all('\n', '') %>%
                str_replace_all('\\s', '') %>%
                str_replace_all(':.+', ':')
            
            info_text_keys <- info_text_v[str_detect(info_text_v, '.+:')]
            info_text_split_regex <- str_c('(', info_text_keys, ')', collapse='|')
            info_text_values <- str_split(info_text, info_text_split_regex, simplify=T)
            info_text_values <- str_trim(info_text_values[info_text_values!=''])
            
            info$subtitle_zh <- ifelse('副标题:' %in% info_text_keys,
                                       info_text_values[which(info_text_keys=='副标题:')], NA)
            info$title <- ifelse('原作名:' %in% info_text_keys,
                                 info_text_values[which(info_text_keys=='原作名:')], NA)
            info$author <- ifelse('作者:' %in% info_text_keys,
                                  info_text_values[which(info_text_keys=='作者:')], NA)
            info$publisher <- ifelse('出版社:' %in% info_text_keys,
                                     info_text_values[which(info_text_keys=='出版社:')], NA)
            info$published_date <- ifelse('出版年:' %in% info_text_keys,
                                          info_text_values[which(info_text_keys=='出版年:')], NA)
            info$pages <- ifelse('页数:' %in% info_text_keys,
                                 info_text_values[which(info_text_keys=='页数:')], NA)
        }, error = function(e) {
            print(glue('[{douban_id}] ERROR: {e}'))
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
gen_movie_imdb_rating_link_html <- function(imdb_rating, imdb_id) {
    if (is.na(imdb_rating) || is.na(imdb_id)) {
        imdb_rating
    } else {
        link <- glue('https://www.imdb.com/title/{imdb_id}')
        gen_linked_text_html(imdb_rating, link)
    }
}
gen_movie_imdb_rating_link_html <- Vectorize(gen_movie_imdb_rating_link_html)

#' 获取豆瓣 ID 的 HTML 代码
#' 
#' @param douban_id 豆瓣 ID
#' @return 豆瓣 ID HTML 代码
gen_douban_id_html <- function(douban_id) {
    gen_span_html('douban-id', douban_id)
}

#' 获取豆瓣电影 LINK 的 HTML 代码
#' 
#' @param douban_rating 豆瓣 RATING
#' @param douban_id 豆瓣 ID
#' @return 豆瓣电影 LINKG 的 HTML 代码
gen_movie_douban_rating_link_html <- function(douban_rating, douban_id) {
    if (is.na(douban_rating) || is.na(douban_id)) {
        douban_rating
    } else {
        link <- glue('https://movie.douban.com/subject/{douban_id}')
        gen_linked_text_html(douban_rating, link)
    }
}
gen_movie_douban_rating_link_html <- Vectorize(gen_movie_douban_rating_link_html)

#' 获取豆瓣书籍 LINK 的 HTML 代码
#' 
#' @param douban_rating 豆瓣 RATING
#' @param douban_id 豆瓣 ID
#' @return 豆瓣书籍 LINKG 的 HTML 代码
gen_book_douban_rating_link_html <- function(douban_rating, douban_id) {
    if (is.na(douban_rating) || is.na(douban_id)) {
        douban_rating
    } else {
        link <- glue('https://book.douban.com/subject/{douban_id}')
        gen_linked_text_html(douban_rating, link)
    }
}
gen_book_douban_rating_link_html <- Vectorize(gen_book_douban_rating_link_html)

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

#' 清理 HTML 表格
#' 
#' @param html HTML
#' @return 清理后 HTML 表格
clean_html_table <- function(html) {
    html %>% str_replace_all('\\s+style="text-align:[a-zA-Z]+;"', '')
}
