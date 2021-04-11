function doubanBookCard(bookID) {
  var url = '/data/douban/book/' + bookID + '.json';

  $.ajax({
    url: url,
    type: 'GET',
    dataType: 'JSON',
    success: function(data) {
      var tags = [];

      var author = data.author[0];
      tags.push(author);

      var press = data.press[0];
      tags.push(press);

      var pubdate = data.pubdate[0].substring(0, 4);
      tags.push(pubdate);

      var title = data.title;
      var rating = data.rating.value;
      var stars = Math.round(rating);
      var image = data.pic.normal;
      var intro = data.intro.replace(/[\n|\r]/g, '');

      $('#douban-card-book-' + bookID).html(
        '<div class="douban-card--middle">' +
          '<div class="douban-card--title">' +
            '<a href="https://book.douban.com/subject/' + bookID + '/" target="_blank">' + title + '</a>' +
          '</div>' +
          '<div class="douban-card--stars-rating">' +
            '<span class="douban-card--logo-dou">豆</span>' +
            '<span class="douban-card--logo-rating">豆瓣评分</span>' +
            '<span class="douban-card--stars douban-card--stars-' + stars + '"></span>' +
            '<span class="douban-card--rating">' + rating + '</span>' +
          '</div>' +
          '<div class="douban-card--tags">' + tags.join(' / ') + '</div>' +
          '<div class="douban-card--summary">' + intro + '</div>' +
        '</div>' +
        '<div class="douban-card--right">' +
          '<img src="' + image + '" referrerPolicy="no-referrer" />' +
        '</div>'
      );
    }
  });
}

function doubanMovieCard(movidID) {
  var url = '/data/douban/movie/' + movidID + '.json';

  $.ajax({
    url: url,
    method: 'GET',
    dataType: 'JSON',
    success: function(data) {
      var tags = [];

      var country = data.countries[0]
      tags.push(country);

      var pubdate = data.pubdate[0].substring(0, 4);
      tags.push(pubdate);

      var director = '导演: ' + data.directors[0].name;
      tags.push(director);

      var actors = '主演: ' + data.actors.map(function(actor) { return actor.name }).join(' ');
      tags.push(actors);

      var title = data.title;
      var rating = data.rating.value;
      var stars = Math.round(rating);
      var image = data.pic.normal;
      var intro = data.intro.replace(/[\n|\r]/g, '');

      $('#douban-card-movie-' + movidID).html(
        '<div class="douban-card--middle">' +
          '<div class="douban-card--title">' +
            '<a href="https://movie.douban.com/subject/' + movidID + '/" target="_blank">' + title + '</a>' +
          '</div>' +
          '<div class="douban-card--stars-rating">' +
            '<span class="douban-card--logo-dou">豆</span>' +
            '<span class="douban-card--logo-rating">豆瓣评分</span>' +
            '<span class="douban-card--stars douban-card--stars-' + stars + '"></span>' +
            '<span class="douban-card--rating">' + rating + '</span>' +
          '</div>' +
          '<div class="douban-card--tags">' + tags.join(' / ') + '</div>' +
          '<div class="douban-card--summary">' + intro + '</div>' +
        '</div>' +
        '<div class="douban-card--right">' +
          '<img src="' + image + '" referrerPolicy="no-referrer" />' +
        '</div>'
      );
    }
  });
}

$(document).ready(function() {
    $('.douban-card').each(function() {
      var doubanID = $(this).attr('douban-id');
      if ($(this).hasClass('douban-card-book')) {
        doubanBookCard(doubanID);
      } else if ($(this).hasClass('douban-card-movie')) {
        doubanMovieCard(doubanID);
      }
    });
});