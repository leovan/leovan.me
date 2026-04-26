(function (d) {
  let tippy = window.tippy || undefined;
  if (!tippy) return;

  function makeTippy(el, contentFn, onTriggerFn, onUntriggerFn) {
    const tippyConfig = {
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
      tippyConfig.content = contentFn;
    }

    if (onTriggerFn) {
      tippyConfig.onTrigger = onTriggerFn;
    }

    if (onUntriggerFn) {
      tippyConfig.onUntrigger = onUntriggerFn;
    }

    tippy(el, tippyConfig);
  }

  const refs = d.querySelectorAll('a[role="doc-noteref"]');

  for (var i = 0; i < refs.length; i++) {
    const ref = refs[i];
    makeTippy(ref, function () {
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
