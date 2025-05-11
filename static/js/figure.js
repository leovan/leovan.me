(window.onresize = function () {
  document.querySelectorAll("figure > img").forEach((el) => {
    if (window.innerWidth >= 960) {
      el.style.setProperty("max-width", el.dataset.largeMaxWidth);
    } else if (window.innerWidth >= 480) {
      el.style.setProperty("max-width", el.dataset.middleMaxWidth);
    } else {
      el.style.setProperty("max-width", el.dataset.smallMaxWidth);
    }
  });
})();
