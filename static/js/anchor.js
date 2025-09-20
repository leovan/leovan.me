(function (d) {
  d.querySelectorAll("h1,h2,h3,h4,h5,h6").forEach((el) => {
    if (el.id && !el.classList.contains("no-anchor")) {
      el.innerHTML += ` <span class="anchor"><a href="#${el.id}">&#35;</a></span>`;
    }
  });
})(document);
