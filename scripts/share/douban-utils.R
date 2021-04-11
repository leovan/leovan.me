library(tidyverse)
library(httpuv)
library(httr)
library(rvest)
library(jsonlite)

DOUBAN_APIKEY <- "0dad551ec0f84ed02907ff5c42e8ec70";
DOUBAN_USER_AGENT <- "api-client/1 com.douban.frodo/7.0.1(204)";
DOUBAN_HOST <- "frodo.douban.com";
DOUBAN_API_HOST <- "https://frodo.douban.com";

DOUBAN_MOVIE_API <- "/api/v2/movie/{}";
DOUBAN_TV_API <- "/api/v2/tv/{}";
DOUBAN_BOOK_API <- "/api/v2/book/{}";

USER_AGENT <- 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'

#' 根据豆瓣 API 时间戳
#'
#' @return 豆瓣 API 时间戳
douban_timestamp <- function() {
    return(as.character(as.integer(as.numeric(Sys.time()))))
}

#' 根据豆瓣 API 签名
#'
#' @param data 豆瓣 ID
#' @param timestamp 时间戳
#' @return 豆瓣 API 签名
douban_signature <- function(data, timestamp) {
    key <- "bf7dddc7c9cfe6f7"
    sig_str <- paste0(
        "GET&", encodeURIComponent(data), "&", as.character(timestamp))
    b64_sig <- str_replace_all(hmac_sha1(key, sig_str), "[=]+$", "")
    return(encodeURIComponent(b64_sig))
}

#' 根据豆瓣 ID 利用 API 获取豆瓣电影信息
#'
#' @param douban_id 豆瓣 ID
#' @return 豆瓣电影信息
get_video_douban_info <- function(douban_id) {
    timestamp <- douban_timestamp()

    movie_sig <- douban_signature(DOUBAN_MOVIE_API, timestamp)
    movie_url <- paste0(
        DOUBAN_API_HOST,
        str_replace(DOUBAN_MOVIE_API, "\\{\\}", as.character(douban_id)),
        "?apikey=", DOUBAN_APIKEY,
        "&channel=Douban",
        "&_ts=", timestamp,
        "&_sig=", movie_sig
    )

    tv_sig <- douban_signature(DOUBAN_TV_API, timestamp)
    tv_url <- paste0(
        DOUBAN_API_HOST,
        str_replace(DOUBAN_TV_API, "\\{\\}", as.character(douban_id)),
        "?apikey=", DOUBAN_APIKEY,
        "&channel=Douban",
        "&_ts=", timestamp,
        "&_sig=", tv_sig
    )

    info <- tibble(
        title = NA, directors = NA, actors = NA, countries = NA,
        genres = NA, release_date = NA, is_tv = NA, douban_rating = NA)

    if (is.na(douban_id)) {
        return(info)
    }

    tryCatch({
        res <- POST(movie_url, user_agent(DOUBAN_USER_AGENT))
        res_json <- fromJSON(content(res, as = "text"))

        if (!is.null(res_json$code)) {
            res <- POST(tv_url, user_agent(DOUBAN_USER_AGENT))
            res_json <- fromJSON(content(res, as = "text"))
        }

        info$title <- res_json$title
        info$directors <- paste(res_json$directors$name, collapse = ", ")
        info$actors <- paste(res_json$actors$name, collapse = ", ")
        info$countries <- paste(res_json$countries, collapse = ", ")
        info$genres <- paste(res_json$genres, collapse = ", ")
        info$release_date <- res_json$pubdate %>%
            str_replace_all("\\(.+\\)", "") %>%
            min() %>%
            as.Date(format = "%Y-%m-%d")
        info$is_tv <- res_json$is_tv
        info$douban_rating <- res_json$rating$value
    }, error = function(e) {
        print(glue("{douban_id}: {e}"))
    })

    # 防止被反爬
    Sys.sleep(runif(1, 1, 2))

    return(info)
}

#' 根据豆瓣 ID 爬取豆瓣电影信息
#'
#' @param douban_id 豆瓣 ID
#' @return 豆瓣电影信息
crawl_video_douban_info <- function(douban_id) {
    info <- tibble(
        title = NA, directors = NA, actors = NA, countries = NA,
        genres = NA, release_date = NA, douban_rating = NA)

    if (!is.na(douban_id)) {
        url <- glue("https://movie.douban.com/subject/{douban_id}")

        tryCatch({
            session <- session(url, user_agent(USER_AGENT))

            title <- session %>%
                html_nodes("title") %>%
                first %>%
                html_text() %>%
                str_replace_all(" ", "")
            title <- str_split(title, "(豆瓣)")[1]
            title <- str_replace_all(title, " ", "")
            info$title <- title

            directors <- session %>%
                html_nodes('a[rel="v:directedBy"]') %>%
                html_text()
            info$directors <- paste(directors, collapse = ", ")

            actors <- session %>%
                html_nodes('a[rel="v:starring"]') %>%
                html_text()
            info$actors <- paste(actors, collapse = ", ")

            countries <- session %>%
                html_nodes("#info") %>%
                html_text() %>%
                str_replace_all("\n", "") %>%
                str_replace(".+制片国家/地区: ", "") %>%
                str_replace("语言: .+", "") %>%
                str_split(" / ", simplify = T)
            info$countries <- paste(countries, collapse = ", ")

            genres <- session %>%
                html_nodes('span[property="v:genre"]') %>%
                html_text()
            info$genres <- paste(genres, collapse = ", ")

            release_date <- session %>%
                html_nodes('span[property="v:initialReleaseDate"]') %>%
                html_text() %>%
                str_replace_all("\\(.+\\)", "") %>%
                min()
            info$release_date <- as.Date(release_date, format = "%Y-%m-%d")

            douban_rating <- session %>%
                html_nodes('strong[property="v:average"]') %>%
                html_text()
            info$douban_rating <- douban_rating
        }, error = function(e) {
            print(glue("{douban_id}: {e}"))
        })
    }

    # 防止被反爬
    Sys.sleep(runif(1, 1, 2))

    return(info)
}

#' 根据豆瓣 ID 利用 API 获取豆瓣书籍信息
#'
#' @param douban_id 豆瓣 ID
#' @return 豆瓣书籍信息
get_book_douban_info <- function(douban_id) {
    timestamp <- douban_timestamp()
    sig <- douban_signature(DOUBAN_BOOK_API, timestamp)

    url <- paste0(
        DOUBAN_API_HOST,
        str_replace(DOUBAN_BOOK_API, "\\{\\}", as.character(douban_id)),
        "?apikey=", DOUBAN_APIKEY,
        "&channel=Douban",
        "&_ts=", timestamp,
        "&_sig=", sig
    )

    info <- tibble(
        title = NA, subtitle = NA, author = NA, press = NA,
        published_date = NA, pages = NA, douban_rating = NA)

    if (is.na(douban_id)) {
        return(info)
    }

    tryCatch({
        res <- POST(url, user_agent(DOUBAN_USER_AGENT))
        res_json <- fromJSON(content(res, as = "text"))

        info$title <- res_json$title
        info$subtitle <- paste(res_json$subtitle, collapse = ", ")
        info$author <- paste(res_json$author, collapse = ", ")
        info$press <- paste(res_json$press, collapse = ", ")
        info$pages <- as.character(res_json$pages)[1]
        info$published_date <- res_json$pubdate %>%
            str_replace_all("\\(.+\\)", "") %>%
            min()
        info$douban_rating <- res_json$rating$value
    }, error = function(e) {
        print(glue("{douban_id}: {e}"))
    })

    # 防止被反爬
    Sys.sleep(runif(1, 1, 2))

    return(info)
}

#' 根据豆瓣 ID 爬取豆瓣书籍信息
#'
#' @param douban_id 豆瓣 ID
#' @return 豆瓣书籍信息
crawl_book_douban_info <- function(douban_id) {
    info <- tibble(
        title = NA, subtitle = NA, author = NA, publisher = NA,
        published_date = NA, pages = NA, douban_rating = NA)

    if (!is.na(douban_id)) {
        url <- glue("https://book.douban.com/subject/{douban_id}")

        tryCatch({
            session <- session(url, user_agent(USER_AGENT))

            info$title <- session %>%
                html_node('span[property="v:itemreviewed"]') %>%
                html_text()

            info$douban_rating <- session %>%
                html_node('strong[property="v:average"]') %>%
                html_text(trim = T)

            info_text <- session %>%
                html_node("#info") %>%
                html_text(trim = T) %>%
                str_replace_all("\n", "") %>%
                str_replace_all("\\s+", " ") %>%
                str_replace_all("【", "[") %>%
                str_replace_all("】", "]") %>%
                str_replace_all("•", "·")
            info_text_v <- session %>%
                html_node("#info") %>%
                html_children() %>%
                html_text(trim = T) %>%
                str_replace_all("\n", "") %>%
                str_replace_all("\\s", "") %>%
                str_replace_all(":.+", ":")

            info_text_keys <- info_text_v[str_detect(info_text_v, ".+:")]
            info_text_split_regex <- str_c("(", info_text_keys, ")", collapse = "|")
            info_text_values <- str_split(info_text, info_text_split_regex, simplify = T)
            info_text_values <- str_trim(info_text_values[info_text_values != ""])

            info$subtitle <- ifelse(
                "副标题:" %in% info_text_keys,
                info_text_values[which(info_text_keys == "副标题:")], NA)
            info$author <- ifelse(
                "作者:" %in% info_text_keys,
                info_text_values[which(info_text_keys == "作者:")], NA)
            info$press <- ifelse(
                "出版社:" %in% info_text_keys,
                info_text_values[which(info_text_keys == "出版社:")], NA)
            info$published_date <- ifelse(
                "出版年:" %in% info_text_keys,
                info_text_values[which(info_text_keys == "出版年:")], NA)
            info$pages <- ifelse(
                "页数:" %in% info_text_keys,
                info_text_values[which(info_text_keys == "页数:")], NA)
        }, error = function(e) {
            print(glue("{douban_id}: {e}"))
        })
    }

    # 防止被反爬
    Sys.sleep(runif(1, 1, 2))

    return(info)
}
