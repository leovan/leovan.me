library(tidyverse)
library(httpuv)
library(httr)
library(rvest)
library(jsonlite)
library(stringr)

API_KEY <- "0dad551ec0f84ed02907ff5c42e8ec70"
API_SECRET <- "bf7dddc7c9cfe6f7"
USER_AGENTS <- c(
  "api-client/1 com.douban.frodo/7.22.0.beta9(231) Android/23 product/Mate 40 vendor/HUAWEI model/Mate 40 brand/HUAWEI  rom/android  network/wifi  platform/AndroidPad",
  "api-client/1 com.douban.frodo/7.18.0(230) Android/22 product/MI 9 vendor/Xiaomi model/MI 9 brand/Android  rom/miui6  network/wifi  platform/mobile nd/1",
  "api-client/1 com.douban.frodo/7.1.0(205) Android/29 product/perseus vendor/Xiaomi model/Mi MIX 3  rom/miui6  network/wifi  platform/mobile nd/1",
  "api-client/1 com.douban.frodo/7.3.0(207) Android/22 product/MI 9 vendor/Xiaomi model/MI 9 brand/Android  rom/miui6  network/wifi platform/mobile nd/1"
)
BASE_URL <- "https://frodo.douban.com/api/v2"

#' 豆瓣 API 签名
#'
#' @param url API URL
#' @param ts 时间戳
#' @return 豆瓣 API 签名
douban_sign <- function(url, ts, method = "GET") {
  url_path <- paste0("/", httr::parse_url(url)$path)
  raw_sign <- paste(
    str_to_upper(method),
    URLencode(url_path, reserved = T),
    as.character(ts),
    sep = "&"
  )
  return(hmac_sha1(API_SECRET, raw_sign))
}

#' 豆瓣 API 结果
#'
#' @param url API URL
#' @return 豆瓣 API 结果
douban_api <- function(url, ...) {
  req_url <- paste0(BASE_URL, url)

  params <- list()
  params <- c(params, list(...))

  ts <- format(Sys.time(), "%Y%m%d")
  sig <- douban_sign(req_url, ts)

  params$apiKey <- API_KEY
  params$os_rom <- "android"
  params$`_ts` <- ts
  params$`_sig` <- sig

  req_url <- parse_url(req_url)
  req_url$query <- params
  req_url <- build_url(req_url)

  res_json <- list()

  tryCatch(
    {
      res <- GET(req_url, user_agent(sample(USER_AGENTS, 1)))
      res_json <- stri_unescape_unicode(content(res, as = "text"))
    },
    error = function(e) {
      print(glue("{url}: {e}"))
    }
  )

  return(res_json)
}

#' 根据豆瓣 ID 利用 API 获取豆瓣电影信息
#'
#' @param douban_id 豆瓣 ID
#' @return 豆瓣电影信息
get_video_douban_info <- function(douban_id, is_tv) {
  if (is_tv) {
    res_json <- douban_api(paste0("/tv/", douban_id))
  } else {
    res_json <- douban_api(paste0("/movie/", douban_id))
  }
  res_json <- fromJSON(res_json, flatten = T)
  movie_info <- list()

  movie_info$title <- res_json$title
  movie_info$directors <- paste(res_json$directors$name, collapse = ", ")
  movie_info$actors <- paste(res_json$actors$name, collapse = ", ")
  movie_info$countries <- paste(res_json$countries, collapse = ", ")
  movie_info$genres <- paste(res_json$genres, collapse = ", ")
  movie_info$release_date <- res_json$pubdate |>
    str_replace_all("\\(.+\\)", "") |>
    min() |>
    as.Date(format = "%Y-%m-%d")
  movie_info$douban_rating <- res_json$rating$value

  return(movie_info)
}
get_video_douban_info <- Vectorize(get_video_douban_info)

#' 根据豆瓣 ID 利用 API 获取豆瓣书籍信息
#'
#' @param douban_id 豆瓣 ID
#' @return 豆瓣书籍信息
get_book_douban_info <- function(douban_id) {
  res_json <- douban_api(paste0("/book/", douban_id))
  res_json <- fromJSON(res_json, flatten = T)
  book_info <- list()

  book_info$title <- res_json$title
  book_info$subtitle <- paste(res_json$subtitle, collapse = ", ")
  book_info$author <- paste(res_json$author, collapse = ", ")
  book_info$press <- paste(res_json$press, collapse = ", ")
  book_info$pages <- as.character(res_json$pages)[1]
  book_info$published_date <- res_json$pubdate |>
    str_replace_all("\\(.+\\)", "") |>
    min()
  book_info$douban_rating <- res_json$rating$value

  return(book_info)
}
get_book_douban_info <- Vectorize(get_book_douban_info)
