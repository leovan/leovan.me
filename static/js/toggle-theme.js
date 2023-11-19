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
  } else {
    document.documentElement.className = "";
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