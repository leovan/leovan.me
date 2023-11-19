let figureSliderIntervalIDS = [];

function figureSliderNext(image, scrollBar, baseURL, imageFilenamePrefix, imageFormat) {
  let imageMinIndex = parseInt(scrollBar.getAttribute('min'));
  let imageMaxIndex = parseInt(scrollBar.getAttribute('max'));
  let imageCurrentIndex = parseInt(scrollBar.value);

  if (imageCurrentIndex == imageMaxIndex) {
    imageCurrentIndex = imageMinIndex;
  } else {
    imageCurrentIndex += 1;
  }

  scrollBar.value = imageCurrentIndex;
  figureSliderShowImage(image, baseURL, imageFilenamePrefix, imageCurrentIndex, imageFormat);
}

function figureSliderPrevious(image, scrollBar, baseURL, imageFilenamePrefix, imageFormat) {
  let imageMinIndex = parseInt(scrollBar.getAttribute('min'));
  let imageMaxIndex = parseInt(scrollBar.getAttribute('max'));
  let imageCurrentIndex = parseInt(scrollBar.value);

  if (imageCurrentIndex == imageMinIndex) {
    imageCurrentIndex = imageMaxIndex;
  } else {
    imageCurrentIndex -= 1;
  }

  scrollBar.value = imageCurrentIndex;
  figureSliderShowImage(image, baseURL, imageFilenamePrefix, imageCurrentIndex, imageFormat);
}

function figureURL(baseURL, imageFilenamePrefix, imageIndex, imageFormat) {
  return baseURL + imageFilenamePrefix + imageIndex + '.' + imageFormat;
}

function figureSliderShowImage(image, baseURL, imageFilenamePrefix, imageIndex, imageFormat) {
  let imageURL = figureURL(baseURL, imageFilenamePrefix, imageIndex, imageFormat);
  image.setAttribute('src', imageURL);
}

function figureSliderPlay(buttonPlayPause) {
  buttonPlayPause.classList.remove('figure-slider-button-play');
  buttonPlayPause.classList.add('figure-slider-button-pause');
  let buttonPlayPauseIcon = buttonPlayPause.querySelector('span');
  buttonPlayPauseIcon.classList.remove('material-symbols-play-outline');
  buttonPlayPauseIcon.classList.add('material-symbols-pause-outline');
}

function figureSliderPause(buttonPlayPause) {
  buttonPlayPause.classList.remove('figure-slider-button-pause');
  buttonPlayPause.classList.add('figure-slider-button-play');
  let buttonPlayPauseIcon = buttonPlayPause.querySelector('span');
  buttonPlayPauseIcon.classList.remove('material-symbols-pause-outline');
  buttonPlayPauseIcon.classList.add('material-symbols-play-outline');
}

function figureSliderTogglePlayPause(image, buttonPlayPause, scrollBar, figureSliderIndex, milliseconds, baseURL, imageFilenamePrefix, imageFormat) {
  function playNext() {
    figureSliderNext(image, scrollBar, baseURL, imageFilenamePrefix, imageFormat);
  }

  if (buttonPlayPause.classList.contains('figure-slider-button-play')) {
    figureSliderPlay(buttonPlayPause);
    figureSliderIntervalIDS[figureSliderIndex] = setInterval(playNext, milliseconds);
  } else {
    figureSliderPause(buttonPlayPause);
    clearInterval(figureSliderIntervalIDS[figureSliderIndex]);
  }
}

function figureSliderPreloadImages(baseURL, imageFilenamePrefix, imageFormat, scrollBar) {
  let imageMinIndex = parseInt(scrollBar.getAttribute('min'));
  let imageMaxIndex = parseInt(scrollBar.getAttribute('max'));

  for (let imageIndex = imageMinIndex; imageIndex <= imageMaxIndex; imageIndex++) {
    let imageSrc = figureURL(baseURL, imageFilenamePrefix, imageIndex, imageFormat);
    (new Image()).src = imageSrc;
  }
}

(function(d) {
  d.querySelectorAll('.figure-slider').forEach(slider => {
    let baseURL = slider.querySelector('.base-url').innerHTML;
    let imageFilenamePrefix = slider.querySelector('.image-filename-prefix').innerHTML;
    let imageFormat = slider.querySelector('.image-format').innerHTML;
    let milliseconds = slider.querySelector('.milliseconds').innerHTML;
    let image = slider.querySelector('.figure-slider-image');
    let scrollBar = slider.querySelector('.figure-slider-scroll-bar');
    let buttonPrevious = slider.querySelector('.figure-slider-button-previous');
    let buttonNext = slider.querySelector('.figure-slider-button-next');
    let buttonPlayPause = slider.querySelector('.figure-slider-button-play-pause');
    let figureSliderIndex = figureSliderIntervalIDS.length;

    figureSliderIntervalIDS.push(false);

    figureSliderPreloadImages(baseURL, imageFilenamePrefix, imageFormat, scrollBar);

    buttonPlayPause.addEventListener('click', function() {
      figureSliderTogglePlayPause(image, buttonPlayPause, scrollBar, figureSliderIndex, milliseconds, baseURL, imageFilenamePrefix, imageFormat)
    });
    buttonPrevious.addEventListener('click', function() {
      figureSliderPrevious(image, scrollBar, baseURL, imageFilenamePrefix, imageFormat)
    });
    buttonNext.addEventListener('click', function() {
      figureSliderNext(image, scrollBar, baseURL, imageFilenamePrefix, imageFormat)
    });
    scrollBar.addEventListener('input', function() {
      let imageCurrentIndex = scrollBar.value;
      figureSliderShowImage(image, baseURL, imageFilenamePrefix, imageCurrentIndex, imageFormat);
    });
  });
})(document);