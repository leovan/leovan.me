(function(d) {
  let wechatPayLogos = {
    'light': '/images/donate/wechat-pay-logo-light-theme.png',
    'dark': '/images/donate/wechat-pay-logo-dark-theme.png'
  };

  let alipayLogos = {
    'light': '/images/donate/alipay-logo-light-theme.png',
    'dark': '/images/donate/alipay-logo-dark-theme.png'
  };

  let qrcodes = {
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

  if (d.querySelector('.footnotes')) {
    let footnotes = d.querySelector('.footnotes')
    footnotes.parentNode.insertBefore(d.querySelector('.donate'), footnotes);
  }

  let donateButton = d.querySelector('.donate-button');
  let donateModelWrapper = d.querySelector('.donate-modal-wrapper');
  let donateBoxCloseButton = d.querySelector('.donate-box-close-button');
  let donateBoxMoneyButtons = d.querySelectorAll('.donate-box-money-button');
  let donateBoxPay = d.querySelector('.donate-box-pay');
  let donateBoxPayMethods = d.querySelectorAll('.donate-box-pay-method');

  let donateMoney = '10';
  let donatePayMethod = 'wechat-pay';

  donateBoxCloseButton.addEventListener('click', donateModalToggle);
  window.addEventListener('click', donateModalOnClick);
  donateButton.addEventListener('click', donateModalToggle);
  donateBoxMoneyButtons.forEach(btn => {
    btn.addEventListener('click', donateBoxMoneyButtonsOnClick);
  });
  donateBoxPayMethods.forEach(btn => {
    btn.addEventListener('click', donateBoxPayMethodsOnClick);
  });

  function donateModalToggle() {
    theme = getTheme();
    let qrcodeKey = donatePayMethod + '-' + donateMoney + '-' + theme;
    d.querySelector('#donate-box-pay-method-image-wechat-pay').setAttribute('src', wechatPayLogos[theme]);
    d.querySelector('#donate-box-pay-method-image-alipay').setAttribute('src', alipayLogos[theme]);
    d.querySelector('#donate-box-pay-qrcode').setAttribute('src', qrcodes[qrcodeKey]);

    donateModelWrapper.classList.toggle('donate-modal-wrapper-show');

    let donateBoxMoneyButtonID = '#donate-box-money-button-' + donateMoney;
    d.querySelector(donateBoxMoneyButtonID).click();
  }

  function donateModalOnClick(event) {
    if (event.target === donateModelWrapper) {
      donateModalToggle();
    }
  }

  function donateBoxMoneyButtonsOnClick() {
    donateBoxMoneyButtons.forEach(btn => {
      btn.innerHTML = btn.getAttribute('data-unchecked');
      btn.classList.add('donate-box-money-button-unchecked');
      btn.classList.remove('donate-box-money-button-checked');
    });

    this.innerHTML = this.getAttribute('data-checked');
    this.classList.add('donate-box-money-button-checked');
    this.classList.remove('donate-box-money-button-unchecked');

    donateBoxShowPayQRCode(donatePayMethod, this.getAttribute('data-v'));
  }

  function donateBoxPayMethodsOnClick() {
    donateBoxPayMethods.forEach(btn => {
      btn.classList.remove('donate-box-pay-method-checked');
    });

    this.classList.add('donate-box-pay-method-checked');

    donateBoxShowPayQRCode(this.getAttribute('data-v'), donateMoney);
  }

  function donateBoxShowPayQRCode(currentDonatePayMethod, currentDonateMoney) {
    let qrcodeKey = currentDonatePayMethod + '-' + currentDonateMoney + '-' + getTheme();
    d.querySelector('#donate-box-pay-qrcode').setAttribute('src', qrcodes[qrcodeKey]);

    donateBoxPay.style.display = 'block';

    donateMoney = currentDonateMoney;
    donatePayMethod = currentDonatePayMethod;
  }

  donateModelWrapper.style.display = 'flex';
})(document);