(function(d) {
  d.querySelectorAll("h1,h2,h3,h4,h5,h6").forEach(h => {
    if (h.id && !h.classList.contains("no-anchor")) {
      h.innerHTML += ` <span class="anchor"><a href="#${h.id}">&#35;</a></span>`;
    }
  });
})(document);