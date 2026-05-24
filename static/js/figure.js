(function (d) {
  function setImageMaxSize(imgEl) {
    if (window.innerWidth >= 1280) {
      imgEl.style.setProperty("max-width", imgEl.dataset.largeMaxWidth);
      imgEl.style.setProperty("max-height", imgEl.dataset.largeMaxHeight);
    } else if (window.innerWidth >= 768) {
      imgEl.style.setProperty("max-width", imgEl.dataset.middleMaxWidth);
      imgEl.style.setProperty("max-height", imgEl.dataset.middleMaxHeight);
    } else {
      imgEl.style.setProperty("max-width", imgEl.dataset.smallMaxWidth);
      imgEl.style.setProperty("max-height", imgEl.dataset.smallMaxHeight);
    }
  }

  const imageResizeObserver = new ResizeObserver((entries) => {
    entries.forEach((entry) => {
      setImageMaxSize(entry.target);
    });
  });

  d.querySelectorAll("figure > img").forEach(imgEl => imageResizeObserver.observe(imgEl));
  d.querySelectorAll(".shortcode-image-compare").forEach(imgEl => imageResizeObserver.observe(imgEl));

  function setFigureFootnotePadding(figureEl) {
    const footnote = figureEl.querySelector(".figure-foot");

    if (!footnote) {
      return;
    }

    const img = figureEl.querySelector("img");

    if (img.classList.contains("lazyload")) {
      return;
    }

    const figureWidth = figureEl.offsetWidth;
    const imgWidth = img.offsetWidth;
    const padding = (figureWidth - imgWidth) / 2;

    footnote.style.setProperty("padding-left", `${padding}px`);
    footnote.style.setProperty("padding-right", `${padding}px`);
  }

  const figureFootnoteResizeObserver = new ResizeObserver((entries) => {
    entries.forEach((entry) => {
      setFigureFootnotePadding(entry.target);
    });
  });

  d.querySelectorAll("figure").forEach(figureEl => figureFootnoteResizeObserver.observe(figureEl));
})(document);
