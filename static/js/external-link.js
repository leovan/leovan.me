(function(d) {
  const r = /^(https?:)?\/\//;
  d.querySelectorAll('a').forEach(a => {
    // add _blank target to external links
    if (r.test(a.getAttribute('href'))) {
      a.target = '_blank';
    }
  })
})(document);