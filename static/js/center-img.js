(function(d) {
  function one_child(el) {
    if (el.childElementCount !== 1) return false;
    const nodes = el.childNodes;
    if (nodes.length === 1) return true;
    for (let i in nodes) {
      let node = nodes[i];
      if (node.nodeName === '#text' && !/^\s$/.test(node.textContent)) return false;
    }
    return true;
  }
  function center_el(tagName) {
    d.querySelectorAll(tagName).forEach(tag => {
      let parent = tag.parentElement;
      // center an image if it is the only element of its parent
      if (one_child(parent)) {
        // if there is a link on image, check grandparent
        const parentA = parent.nodeName === 'A';
        if (parentA) {
          parent = parent.parentElement;
          if (!one_child(parent)) return;
          parent.firstElementChild.style.border = 'none';
        }
        if (parent.nodeName === 'P') {
          parent.style.textAlign = 'center';
          if (!parentA && tagName === 'img') {
            parent.innerHTML = '<a href="' + tag.src + '" style="border: none;">' +
              tag.outerHTML + '</a>';
          }
        }
      }
    });
  }
  ['img', 'embed', 'object'].forEach(tag => center_el(tag));
  // also center paragraphs that contain `* * *`
  d.querySelectorAll('p').forEach(p => {
    if (p.innerText === '* * *') p.style.textAlign = 'center';
  });
})(document);