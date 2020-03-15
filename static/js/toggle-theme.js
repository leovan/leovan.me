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
    document.getElementById("dark-mode-style").removeAttribute("disabled");
    document.getElementById("light-dark-mode-icon").classList.remove("mdi-weather-night");
    document.getElementById("light-dark-mode-icon").classList.add("mdi-white-balance-sunny");
  } else {
    document.getElementById("dark-mode-style").setAttribute("disabled", "disabled");
    document.getElementById("light-dark-mode-icon").classList.remove("mdi-white-balance-sunny");
    document.getElementById("light-dark-mode-icon").classList.add("mdi-weather-night");
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

document.getElementById("light-dark-mode-action").addEventListener("click", toggleTheme);
setTheme(getTheme());