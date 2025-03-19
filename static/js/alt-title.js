(function () {
  let imgs = document.getElementsByTagName("img");
  for (let i = 0; i < imgs.length; i++) {
    let img = imgs[i];
    if (!img.title) img.title = img.alt;
  }
})();
