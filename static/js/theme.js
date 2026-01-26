(function () {
  document.querySelectorAll(".toggle-theme-button").forEach((el) => {
    el.addEventListener("click", toggleTheme);
  });
  setTheme(getTheme());
})();
