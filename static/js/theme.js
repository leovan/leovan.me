function getTheme() {
  theme = "light";

  if ("theme" in localStorage) {
    theme = localStorage.getItem("theme");
  } else {
    if (window.matchMedia("(prefers-color-scheme: dark)").matches) {
      theme = "dark";
    }
  }

  if (theme === "dark") {
    theme = "dark";
  } else {
    theme = "light";
  }

  return theme;
}

function setTheme(theme) {
  localStorage.setItem("theme", theme);

  if (theme == "dark") {
    document.documentElement.className = "dark";
  } else {
    document.documentElement.className = "";
  }
}

function toggleTheme() {
  theme = getTheme();

  if (theme === "light") {
    setTheme("dark");
  } else {
    setTheme("light");
  }
}

(function () {
  document.querySelectorAll(".theme-toggle").forEach(el => {
    el.addEventListener("click", toggleTheme);
  });
  setTheme(getTheme());
})();
