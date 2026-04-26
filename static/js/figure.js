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
