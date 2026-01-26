let lightGiscusCss = "{{ absURL "css/giscus-light.css" }}";
let darkGiscusCss= "{{ absURL "css/giscus-dark.css" }}";

function getTheme() {
  let theme = "light";

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

function setGiscusTheme(theme) {
  document.querySelectorAll(".giscus-frame").forEach((el) => {
    if (el.contentWindow) {
      el.contentWindow.postMessage(
        {
          giscus: {
            setConfig: {
              theme: theme === "dark" ? darkGiscusCss : lightGiscusCss,
            }
          }
        },
        "https://giscus.app"
      );
    }
  });
}

function setTheme(theme) {
  localStorage.setItem("theme", theme);

  if (theme === "dark") {
    document.documentElement.classList.add("dark");
  } else {
    document.documentElement.classList.remove("dark");
  }

  setGiscusTheme(theme);
}

function toggleTheme() {
  let theme = getTheme();

  if (theme === "light") {
    setTheme("dark");
  } else {
    setTheme("light");
  }
}

function isLocalNetwork() {
  let hostname = window.location.hostname;

  if (["localhost", "127.0.0.1", "", "::1"].includes(hostname)) {
    return true;
  }

  if (
    hostname.startsWith("192.168.") ||
    hostname.startsWith("10.") ||
    hostname.startsWith("172.") ||
    hostname.endsWith(".local")
  ) {
    return true;
  }

  return false;
}

function isMyDomain() {
  let hostname = window.location.hostname;

  if (hostname === "leovan.me") {
    return true;
  }

  return false;
}

function isValidDomain() {
  return isLocalNetwork() || isMyDomain();
}
