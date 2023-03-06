(function(d) {
  // 修复链接中的中文无法自动识别的问题（非完美修复）
  d.querySelectorAll(".footnotes > ol > li > p").forEach(el => {
    let childNodes = el.childNodes;
    if (childNodes.length === 3 && childNodes[0].nodeName === "A" && childNodes[1].nodeName === "#text" && childNodes[2].nodeName === "A") {
      let footnoteLink = childNodes[0];
      let extraText = childNodes[1];

      if (extraText.textContent.match(/^[^\s]+/g)) {
        let fixedFootnoteLinkText = footnoteLink.textContent + extraText.textContent.match(/^[^\s]+/g);
        footnoteLink.setAttribute("href", fixedFootnoteLinkText);
        footnoteLink.innerText = fixedFootnoteLinkText;

        extraText.data = extraText.textContent.replace(/^[^\s]+/g, "");
      }
    }
  });
})(document);