(function (d) {
  function tippyHover(el, contentFn, onTriggerFn, onUntriggerFn) {
    const config = {
      allowHTML: true,
      maxWidth: 640,
      delay: 100,
      arrow: false,
      appendTo: function (el) {
        return d.querySelector(".content");
      },
      interactive: true,
      interactiveBorder: 10,
      placement: "bottom-start",
    };

    if (contentFn) {
      config.content = contentFn;
    }

    if (onTriggerFn) {
      config.onTrigger = onTriggerFn;
    }

    if (onUntriggerFn) {
      config.onUntrigger = onUntriggerFn;
    }

    window.tippy(el, config);
  }

  const refs = d.querySelectorAll('a[role="doc-noteref"]');

  for (var i = 0; i < refs.length; i++) {
    const ref = refs[i];
    tippyHover(ref, function () {
      let href = ref.getAttribute("href");
      try {
        href = new URL(href).hash;
      } catch {}
      const id = href.replace(/^#\/?/, "");
      const note = d.getElementById(id);

      if (note) {
        return note.innerHTML;
      } else {
        return "";
      }
    });
  }
})(document);
