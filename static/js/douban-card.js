function doubanBookCard(bookID) {
  let url = '/data/douban/book/' + bookID + '.json';

  fetch(url, {method: 'get'}).then(response => {
    return response.json();
  }).then(data => {
    let tags = [];

    let author = data.author[0];
    tags.push(author);

    let press = data.press[0];
    tags.push(press);

    let pubdate = data.pubdate[0].substring(0, 4);
    tags.push(pubdate);

    let title = data.title;
    let rating = data.rating.value;
    let stars = Math.round(rating);
    let image = data.pic.normal;
    let intro = data.intro.replace(/[\n|\r]/g, '');

    document.querySelector('#douban-card-book-' + bookID).innerHTML = '<div class="douban-card--middle">' +
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
      '</div>';
  }).catch(error => {
    console.log(error);
  });
}

function doubanMovieCard(movidID) {
  let url = '/data/douban/movie/' + movidID + '.json';

  fetch(url, {method: 'get'}).then(response => {
    return response.json();
  }).then(data => {
    let tags = [];

    let country = data.countries[0]
    tags.push(country);

    let pubdate = data.pubdate[0].substring(0, 4);
    tags.push(pubdate);

    let director = '导演: ' + data.directors[0].name;
    tags.push(director);

    let actors = '主演: ' + data.actors.map(function(actor) { return actor.name }).join(' ');
    tags.push(actors);

    let title = data.title;
    let rating = data.rating.value;
    let stars = Math.round(rating);
    let image = data.pic.normal;
    let intro = data.intro.replace(/[\n|\r]/g, '');

    document.querySelector('#douban-card-movie-' + movidID).innerHTML = '<div class="douban-card--middle">' +
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
      '</div>';
  });
}

(function(d) {
    d.querySelectorAll('.douban-card').forEach(card => {
      let doubanID = card.getAttribute('douban-id');
      if (card.classList.contains('douban-card-book')) {
        doubanBookCard(doubanID);
      } else if (card.classList.contains('douban-card-movie')) {
        doubanMovieCard(doubanID);
      }
    });
})(document);