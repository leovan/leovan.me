function handleGiscusMessage(event) {
  if (event.origin !== 'https://giscus.app') return;
  if (!(typeof event.data === 'object' && event.data.giscus)) return;

  document.querySelectorAll(".giscus-component").forEach((el) => {
    el.classList.remove("hidden");
  });
  window.removeEventListener("message", handleGiscusMessage);
}

window.addEventListener("message", handleGiscusMessage);
