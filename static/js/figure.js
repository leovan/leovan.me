(function (d) {
  function oneChild(el) {
    if (el.childElementCount !== 1) return false;
    const nodes = el.childNodes;
    if (nodes.length === 1) return true;
    for (let i in nodes) {
      let node = nodes[i];
      if (node.nodeName === "#text" && !/^\s$/.test(node.textContent))
        return false;
    }
    return true;
  }
  function centerEl(tagName) {
    d.querySelectorAll(tagName).forEach((tag) => {
      let parent = tag.parentElement;
      // center an image if it is the only element of its parent
      if (oneChild(parent)) {
        // if there is a link on image, check grandparent
        const parentA = parent.nodeName === "A";
        if (parentA) {
          parent = parent.parentElement;
          if (!oneChild(parent)) return;
          parent.firstElementChild.style.border = "none";
        }
        if (parent.nodeName === "P") {
          parent.style.textAlign = "center";
          if (!parentA && tagName === "img") {
            parent.innerHTML =
              '<a href="' +
              tag.src +
              '" style="border: none;">' +
              tag.outerHTML +
              "</a>";
          }
        }
      }
    });
  }
  ["img", "embed", "object"].forEach((tag) => centerEl(tag));
})(document);

(window.onresize = function () {
  function setMaxSize(el) {
    if (window.innerWidth >= 1280) {
      el.style.setProperty("max-width", el.dataset.largeMaxWidth);
      el.style.setProperty("max-height", el.dataset.largeMaxHeight);
    } else if (window.innerWidth >= 768) {
      el.style.setProperty("max-width", el.dataset.middleMaxWidth);
      el.style.setProperty("max-height", el.dataset.middleMaxHeight);
    } else {
      el.style.setProperty("max-width", el.dataset.smallMaxWidth);
      el.style.setProperty("max-height", el.dataset.smallMaxHeight);
    }
  }
  document.querySelectorAll("figure > img").forEach(setMaxSize);
  document.querySelectorAll(".shortcode-image-compare").forEach(setMaxSize);
})();
