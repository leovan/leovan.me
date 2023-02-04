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
    document.getElementById("theme-toggle-icon").classList.remove("mdi-weather-night");
    document.getElementById("theme-toggle-icon").classList.add("mdi-white-balance-sunny");
  } else {
    document.documentElement.className = "";
    document.getElementById("theme-toggle-icon").classList.remove("mdi-white-balance-sunny");
    document.getElementById("theme-toggle-icon").classList.add("mdi-weather-night");
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