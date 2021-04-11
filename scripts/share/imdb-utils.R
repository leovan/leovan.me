library(tidyverse)
library(glue)
library(httr)
library(jsonlite)

#' 根据 IMDB ID 获取电影 IMDB 评分
#'
#' @param imdb_id IMDB ID
#' @return 电影 IMDB 评分
get_video_imdb_rating <- function(imdb_id) {
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

    return(rating)
}
get_video_imdb_rating <- Vectorize(get_video_imdb_rating)