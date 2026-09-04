from pathlib import Path

p = Path("index.html")
s = p.read_text(encoding="utf-8")
original = s

if "body.request-only .mast-tools{display:flex !important}" not in s:
    s = s.replace("body.request-only .mast-tools,\n", "", 1)
    marker = "body.request-only footer{display:none !important}\n"
    inject = (
        "body.request-only footer{display:none !important}\n"
        "body.request-only .mast-tools{display:flex !important}\n"
        "body.request-only #jumpBtn,\n"
        "body.request-only #printBtn{display:none !important}\n"
    )
    if marker not in s:
        raise SystemExit("request-only CSS marker not found")
    s = s.replace(marker, inject, 1)

if 'var themes = ["auto", "light", "dark"]' in s:
    start_marker = "  /* ---------- theme ---------- */"
    end_marker = "  /* ---------- toast ---------- */"
    start = s.index(start_marker)
    end = s.index(end_marker, start)
    new_theme = '''  /* ---------- theme ---------- */
  var theme = "light";
  try {
    var savedTheme = localStorage.getItem("friday.theme");
    if (savedTheme === "light" || savedTheme === "dark") theme = savedTheme;
    else if (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches) theme = "dark";
  } catch (e) {}
  var applyTheme = function () {
    document.documentElement.setAttribute("data-theme", theme);
    var nextIsDark = theme === "light";
    $("themeIcon").textContent = nextIsDark ? "☽" : "☀";
    $("themeLabel").textContent = nextIsDark ? "Dark mode" : "Light mode";
    $("themeBtn").setAttribute("aria-label", nextIsDark ? "Switch to dark mode" : "Switch to light mode");
  };
  $("themeBtn").addEventListener("click", function () {
    theme = theme === "light" ? "dark" : "light";
    try { localStorage.setItem("friday.theme", theme); } catch (e) {}
    applyTheme();
  });
  applyTheme();

'''
    s = s[:start] + new_theme + s[end:]

required = [
    "body.request-only .mast-tools{display:flex !important}",
    "body.request-only #jumpBtn",
    "body.request-only #printBtn{display:none !important}",
    "Dark mode",
    "Light mode",
    'localStorage.setItem("friday.theme", theme)',
]
for item in required:
    if item not in s:
        raise SystemExit(f"theme patch verification failed: {item}")

if s != original:
    p.write_text(s, encoding="utf-8")
    print("Theme toggle patched.")
else:
    print("Theme toggle already present.")
