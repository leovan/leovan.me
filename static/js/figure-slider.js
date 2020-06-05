$(document).ready(function() {
  var figureSliderIntervalIDS = [];

  function figureSliderNext(image, scrollBar, baseURL, imageFilenamePrefix, imageFormat) {
    var imageMinIndex = parseInt(scrollBar.attr("min"));
    var imageMaxIndex = parseInt(scrollBar.attr("max"));
    var imageCurrentIndex = parseInt(scrollBar.val());

    if (imageCurrentIndex == imageMaxIndex) {
      imageCurrentIndex = imageMinIndex;
    } else {
      imageCurrentIndex += 1;
    }

    scrollBar.val(imageCurrentIndex);
    figureSliderShowImage(image, baseURL, imageFilenamePrefix, imageCurrentIndex, imageFormat);
  }

  function figureSliderPrevious(image, scrollBar, baseURL, imageFilenamePrefix, imageFormat) {
    var imageMinIndex = parseInt(scrollBar.attr("min"));
    var imageMaxIndex = parseInt(scrollBar.attr("max"));
    var imageCurrentIndex = parseInt(scrollBar.val());

    if (imageCurrentIndex == imageMinIndex) {
      imageCurrentIndex = imageMaxIndex;
    } else {
      imageCurrentIndex -= 1;
    }

    scrollBar.val(imageCurrentIndex);
    figureSliderShowImage(image, baseURL, imageFilenamePrefix, imageCurrentIndex, imageFormat);
  }

  function figureURL(baseURL, imageFilenamePrefix, imageIndex, imageFormat) {
    return baseURL + imageFilenamePrefix + imageIndex + "." + imageFormat;
  }

  function figureSliderShowImage(image, baseURL, imageFilenamePrefix, imageIndex, imageFormat) {
    var imageURL = figureURL(baseURL, imageFilenamePrefix, imageIndex, imageFormat);
    image.attr("src", imageURL);
  }

  function figureSliderPlay(buttonPlayPause) {
    buttonPlayPause.removeClass("figure-slider-button-play");
    buttonPlayPause.addClass("figure-slider-button-pause");
    var buttonPlayPauseIcon = buttonPlayPause.find("span").first();
    buttonPlayPauseIcon.removeClass("mdi-play");
    buttonPlayPauseIcon.addClass("mdi-pause");
  }

  function figureSliderPause(buttonPlayPause) {
    buttonPlayPause.removeClass("figure-slider-button-pause");
    buttonPlayPause.addClass("figure-slider-button-play");
    var buttonPlayPauseIcon = buttonPlayPause.find("span").first();
    buttonPlayPauseIcon.removeClass("mdi-pause");
    buttonPlayPauseIcon.addClass("mdi-play");
  }

  function figureSliderTogglePlayPause(image, buttonPlayPause, scrollBar, figureSliderIndex, milliseconds, baseURL, imageFilenamePrefix, imageFormat) {
    function playNext() {
      figureSliderNext(image, scrollBar, baseURL, imageFilenamePrefix, imageFormat);
    }

    if (buttonPlayPause.hasClass("figure-slider-button-play")) {
      figureSliderPlay(buttonPlayPause);
      figureSliderIntervalIDS[figureSliderIndex] = setInterval(playNext, milliseconds);
    } else {
      figureSliderPause(buttonPlayPause);
      clearInterval(figureSliderIntervalIDS[figureSliderIndex]);
    }
  }

  $(".figure-slider").each(function() {
    var baseURL = $(this).find(".base-url").first().html();
    var imageFilenamePrefix = $(this).find(".image-filename-prefix").first().html();
    var imageFormat = $(this).find(".image-format").first().html();
    var milliseconds = $(this).find(".milliseconds").first().html();
    var image = $(this).find(".figure-slider-image").first();
    var scrollBar = $(this).find(".figure-slider-scroll-bar").first();
    var buttonPrevious = $(this).find(".figure-slider-button-previous").first();
    var buttonNext = $(this).find(".figure-slider-button-next").first();
    var buttonPlayPause = $(this).find(".figure-slider-button-play-pause").first();
    var figureSliderIndex = figureSliderIntervalIDS.length;

    figureSliderIntervalIDS.push(false);

    buttonPlayPause.click(function () {
      figureSliderTogglePlayPause(image, buttonPlayPause, scrollBar, figureSliderIndex, milliseconds, baseURL, imageFilenamePrefix, imageFormat);
    });
    buttonPrevious.click(function () {
      figureSliderPrevious(image, scrollBar, baseURL, imageFilenamePrefix, imageFormat);
    });
    buttonNext.click(function () {
      figureSliderNext(image, scrollBar, baseURL, imageFilenamePrefix, imageFormat);
    });
    scrollBar.on("input", function () {
      var imageCurrentIndex = scrollBar.val();
      figureSliderShowImage(image, baseURL, imageFilenamePrefix, imageCurrentIndex, imageFormat);
    });
  });
});