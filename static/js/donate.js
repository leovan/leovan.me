var wechatPayLogos = {
  'light': '/images/donate/wechat-pay-logo-light-theme.png',
  'dark': '/images/donate/wechat-pay-logo-dark-theme.png'
};

var alipayLogos = {
  'light': '/images/donate/alipay-logo-light-theme.png',
  'dark': '/images/donate/alipay-logo-dark-theme.png'
};

var qrcodes = {
  'wechat-pay-2-light': '/images/donate/wechat-pay-2-light-theme.png',
  'wechat-pay-2-dark': '/images/donate/wechat-pay-2-dark-theme.png',
  'wechat-pay-5-light': '/images/donate/wechat-pay-5-light-theme.png',
  'wechat-pay-5-dark': '/images/donate/wechat-pay-5-dark-theme.png',
  'wechat-pay-10-light': '/images/donate/wechat-pay-10-light-theme.png',
  'wechat-pay-10-dark': '/images/donate/wechat-pay-10-dark-theme.png',
  'wechat-pay-50-light': '/images/donate/wechat-pay-50-light-theme.png',
  'wechat-pay-50-dark': '/images/donate/wechat-pay-50-dark-theme.png',
  'wechat-pay-100-light': '/images/donate/wechat-pay-100-light-theme.png',
  'wechat-pay-100-dark': '/images/donate/wechat-pay-100-dark-theme.png',
  'wechat-pay-custom-light': '/images/donate/wechat-pay-custom-light-theme.png',
  'wechat-pay-custom-dark': '/images/donate/wechat-pay-custom-dark-theme.png',
  'alipay-2-light': '/images/donate/alipay-2-light-theme.png',
  'alipay-2-dark': '/images/donate/alipay-2-dark-theme.png',
  'alipay-5-light': '/images/donate/alipay-5-light-theme.png',
  'alipay-5-dark': '/images/donate/alipay-5-dark-theme.png',
  'alipay-10-light': '/images/donate/alipay-10-light-theme.png',
  'alipay-10-dark': '/images/donate/alipay-10-dark-theme.png',
  'alipay-50-light': '/images/donate/alipay-50-light-theme.png',
  'alipay-50-dark': '/images/donate/alipay-50-dark-theme.png',
  'alipay-100-light': '/images/donate/alipay-100-light-theme.png',
  'alipay-100-dark': '/images/donate/alipay-100-dark-theme.png',
  'alipay-custom-light': '/images/donate/alipay-custom-light-theme.png',
  'alipay-custom-dark': '/images/donate/alipay-custom-dark-theme.png'
};

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
    var qrcodeKey = donatePayMethod + '-' + donateMoney + '-' + theme;
    $('#donate-box-pay-method-image-wechat-pay').attr('src', wechatPayLogos[theme]);
    $('#donate-box-pay-method-image-alipay').attr('src', alipayLogos[theme]);
    $('#donate-box-pay-qrcode').attr('src', qrcodes[qrcodeKey]);

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
    var qrcodeKey = currentDonatePayMethod + '-' + currentDonateMoney + '-' + getTheme();
    $('#donate-box-pay-qrcode').attr('src', qrcodes[qrcodeKey]);

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