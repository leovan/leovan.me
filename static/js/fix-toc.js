(function() {
  const toc = document.getElementById('TableOfContents');
  if (!toc) return;
  // fix header ids and a hrefs if a header contains a link
  toc.querySelectorAll('a[href^="#"]').forEach((a) => {
    let id = a.getAttribute('href').replace(/^#/, '');
    const h = document.getElementById(id);
    // remove the URL from the id
    id = id.replace(/-https?-.+$/, '');
    if (h) h.id = id; a.href = '#' + id;
    // if the TOC item has two <a>'s, remove the second if the first is empty
    if (a.innerHTML !== '') return;
    const a2 = a.nextElementSibling;
    if (!a2 || a2.tagName !== 'A') return;
    a.innerHTML = a2.innerHTML;
    a2.remove();
  });
  // Blackfriday may generate a TOC that has an empty bullet when all headings
  // are h2 and there is no h1: https://github.com/gohugoio/hugo/issues/1778#issuecomment-420036687
  let li, ul = toc.querySelector('ul');
  if (ul.childElementCount !== 1) return;
  li = ul.firstElementChild;
  if (li.tagName !== 'LI') return;
  // remove <ul><li></li></ul> where <ul> only contains one <li>
  ul.outerHTML = li.innerHTML;
})();