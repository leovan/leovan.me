$(document).ready(function() {
  if ($('.footnotes')) {
    $('.footnotes').before($('.donate'));
  }
  
  var donateButton = $('.donate-button');
  var donateModelWrapper = $('.donate-modal-wrapper');
  var donateModelBackground = $('.donate-modal-background');
  var donateBoxCloseButton = $('.donate-box-close-button');
  var donateBoxMoneyButtons = $('.donate-box-money-button');
  var donateBoxPay = $('.donate-box-pay');
  var donatePayQRCode = $('.donate-pay-qrcode');
  var donatePayMethods = $('.donate-pay-method');
  
  var donateMoney = '0';
  var donatePayMethod = 'wechat-pay';
    
  donateButton.on('click', donateModalToggle);
  donateBoxCloseButton.on('click', donateModalToggle);
  $(window).on('click', donateModalOnClick);
  
  donateBoxMoneyButtons.on('click', donateBoxMoneyButtonsOnClick);
  donatePayMethods.on('click', donatePayMethodsOnClick);
  
  function donateModalToggle() {
    donateModelWrapper.toggleClass('donate-modal-wrapper-show');
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
    
    donateShowPayQRCode(donatePayMethod, $(this).attr('data-v'));
  }
  
  function donatePayMethodsOnClick() {
    donatePayMethods.each(function() {
      $(this).removeClass('donate-pay-method-checked');
    });
    
    $(this).addClass('donate-pay-method-checked');
    
    donateShowPayQRCode($(this).attr('data-v'), donateMoney);
  }
  
  function donateShowPayQRCode(currentDonatePayMethod, currentDonateMoney) {
    if (currentDonateMoney !== '0' && (currentDonateMoney !== donateMoney || currentDonatePayMethod !== donatePayMethod)) {
      donatePayQRCodeImageSrc = '/images/donate/' + currentDonatePayMethod + '-' + currentDonateMoney + '.png';
      donatePayQRCode.attr('src', donatePayQRCodeImageSrc);
      donateBoxPay.show();
        
      donateMoney = currentDonateMoney;
      donatePayMethod = currentDonatePayMethod;
    }
  }
});