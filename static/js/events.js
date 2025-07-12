(window.onresize = function () {
  function setMaxWidth(el) {
    if (window.innerWidth >= 1440) {
      el.style.setProperty("max-width", el.dataset.largeMaxWidth);
    } else if (window.innerWidth >= 960) {
      el.style.setProperty("max-width", el.dataset.middleMaxWidth);
    } else {
      el.style.setProperty("max-width", el.dataset.smallMaxWidth);
    }
  }
  document.querySelectorAll("figure > img").forEach(setMaxWidth);
  document.querySelectorAll(".image-compare").forEach(setMaxWidth);
})();
