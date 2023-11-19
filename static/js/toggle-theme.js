function getTheme() {
  theme = Cookies.get("theme", {path: "/"});

  if (theme == "dark") {
    theme = "dark";
  } else {
    theme = "light";
  }

  return theme;
}

function setTheme(theme) {
  Cookies.set("theme", theme, {path: "/"});

  if (theme == "dark") {
    document.documentElement.className = "dark";
    document.getElementById("theme-toggle-icon").classList.remove("material-symbols-dark-mode-outline");
    document.getElementById("theme-toggle-icon").classList.add("material-symbols-light-mode-outline");
  } else {
    document.documentElement.className = "";
    document.getElementById("theme-toggle-icon").classList.remove("material-symbols-light-mode-outline");
    document.getElementById("theme-toggle-icon").classList.add("material-symbols-dark-mode-outline");
  }
}

function toggleTheme() {
  theme = getTheme();

  if (theme == "light") {
    setTheme("dark");
  } else {
    setTheme("light");
  }
}

(function() {
  document.getElementById("theme-toggle-icon").onclick = toggleTheme;
  setTheme(getTheme());
})();