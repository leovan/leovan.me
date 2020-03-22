$(document).ready(function() {
  if ($('.footnotes')) {
    $('.footnotes').before($('.donate'));
  }

  var donateButton = $('.donate-button');
  var donateSlug = $('#donate-slug').html();
  var donateModelWrapper = $('.donate-modal-wrapper');
  var donateModelBackground = $('.donate-modal-background');
  var donateBoxCloseButton = $('.donate-box-close-button');
  var donateBoxMoneyButtons = $('.donate-box-money-button');
  var donateBoxPay = $('.donate-box-pay');
  var donateBoxPayQRCode = $('.donate-box-pay-qrcode');
  var donateBoxPayMethods = $('.donate-box-pay-method');

  var donateMoney = '10';
  var donatePayMethod = 'wechat-pay';

  donateBoxCloseButton.on('click', donateModalToggle);
  $(window).on('click', donateModalOnClick);
  donateButton.on('click', donateButtonOnClick);
  donateBoxMoneyButtons.on('click', donateBoxMoneyButtonsOnClick);
  donateBoxPayMethods.on('click', donateBoxPayMethodsOnClick);

  function donateButtonOnClick() {
    donateModalToggle();
    gtagDonateButton();
  }

  function donateModalToggle() {
    theme = getTheme();

    if (theme == "dark") {
      $('.donate-box-pay-method-image.donate-light-theme').css('display', 'none');
      $('.donate-box-pay-method-image.donate-dark-theme').css('display', '');
    } else {
      $('.donate-box-pay-method-image.donate-dark-theme').css('display', 'none');
      $('.donate-box-pay-method-image.donate-light-theme').css('display', '');
    }

    donateModelWrapper.toggleClass('donate-modal-wrapper-show');

    donateBoxMoneyButtonID = '#donate-box-money-button-' + donateMoney;
    $(donateBoxMoneyButtonID).trigger('click');
  }

  function gtagDonateButton() {
    gtag('event', 'blog-donation', {
      'event_category': 'donation',
      'event_label': donateSlug
    });
  }

  function donateModalOnClick(event) {
    if ($(event.target).is(donateModelWrapper)) {
      donateModalToggle();
    }
  }

  function donateBoxMoneyButtonsOnClick() {
    donateBoxMoneyButtons.each(function() {
      $(this).html($(this).attr('data-unchecked'));
      $(this).addClass('donate-box-money-button-unchecked');
      $(this).removeClass('donate-box-money-button-checked');
    });

    $(this).html($(this).attr('data-checked'));
    $(this).removeClass('donate-box-money-button-unchecked');
    $(this).addClass('donate-box-money-button-checked');

    donateBoxShowPayQRCode(donatePayMethod, $(this).attr('data-v'));
    gtagDonatePay(donatePayMethod, $(this).attr('data-v'));
  }

  function donateBoxPayMethodsOnClick() {
    donateBoxPayMethods.each(function() {
      $(this).removeClass('donate-box-pay-method-checked');
    });

    $(this).addClass('donate-box-pay-method-checked');

    donateBoxShowPayQRCode($(this).attr('data-v'), donateMoney);
    gtagDonatePay($(this).attr('data-v'), donateMoney);
  }

  function donateBoxShowPayQRCode(currentDonatePayMethod, currentDonateMoney) {
    $('.donate-box-pay-qrcode').css('display', 'none');

    theme = getTheme();
    donateBoxPayQRCodeClass = '.donate-' + theme + '-theme.' + currentDonatePayMethod + '-' + currentDonateMoney;
    $(donateBoxPayQRCodeClass).css('display', '');

    donateBoxPay.show();

    donateMoney = currentDonateMoney;
    donatePayMethod = currentDonatePayMethod;
  }

  function gtagDonatePay(currentDonatePayMethod, currentDonateMoney) {
    var eventAction = 'blog-donation-' + currentDonatePayMethod + '-' + currentDonateMoney;
    gtag('event', eventAction, {
      'event_category': 'donation',
      'event_label': donateSlug
    });
  }
});