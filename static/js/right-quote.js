(function() {
  let quotes = document.getElementsByTagName('blockquote'), i, quote;
  for (i = 0; i < quotes.length; i++) {
    quote = quotes[i];
    let n = quote.children.length;
    if (n === 0) continue;
    let el = quote.children[n - 1];
    if (!el || el.nodeName !== 'P') continue;
    // right-align a quote footer if it starts with ---
    if (/^—/.test(el.textContent)) el.style.textAlign = 'right';
  }
})();