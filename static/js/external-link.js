(function(d) {
  const r = /^(https?:)?\/\//;
  d.querySelectorAll('a').forEach(a => {
    // add _blank target to external links
    if (r.test(a.getAttribute('href'))) {
      a.target = '_blank';
    }
    // shorten bare links
    if (a.childElementCount === 0) {
      a.innerText = a.innerText.replace(r, '').replace(/#.*$/, '');
    }
  })
})(document);