$(document).ready(function() {
    $(".imdb-rating").each(function() {
        var imdb_id = $(this).closest("tr").find(".imdb-id:first").html();
        var url = "https://www.omdbapi.com/?apikey=31ee42cc&i=" +
            imdb_id + "&callback=?";
        var current_elem = $(this);
        
        $.getJSON(url, function(res_json) {
            var linked_rating = '<a href="https://www.imdb.com/title/' +
                imdb_id + '" target="_blank">' + res_json.imdbRating + '</a>';
            current_elem.html(linked_rating);
        });
    });
    
    $(".douban-rating").each(function() {
        var douban_id = $(this).closest("tr").find('.douban-id:first').html();
        var url = "https://api.douban.com/v2/movie/subject/" +
            douban_id + "?callback=?";
        var current_elem = $(this);
        
        $.getJSON(url, function(res_json) {
            var linked_rating = '<a href="https://movie.douban.com/subject/' +
                douban_id + '" target="_blank">' + res_json.rating.average + '</a>';
            current_elem.html(linked_rating);
        });
    });
    
    $(".star-rating").starRating({
      totalStars: 5,
      strokeWidth: 3,
      starSize: 20,
      readOnly: true
    });
});
