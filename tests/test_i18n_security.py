"""Test i18n security and cached DOM translation behavior."""

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

def test_i18n_input_validation() -> None:
    """Test that allowedLanguages validation logic is correctly implemented in i18n.js."""
    with open("i18n.js", "r", encoding="utf-8") as f:
        content = f.read()

    # Check for whitelist validation
    assert "allowedLanguages = [\"ko\", \"en\"]" in content or "allowedLanguages = ['ko', 'en']" in content
    assert "allowedLanguages.includes" in content

def test_i18n_html_security_tests_present() -> None:
    """Test that explicit __proto__ and XSS payload checks exist in the HTML test harness."""
    with open("test_i18n.html", "r", encoding="utf-8") as f:
        content = f.read()

    assert "setLanguage(\"__proto__\")" in content
    assert "setLanguage(\"<script>alert(1)<\\/script>\")" in content


def test_i18n_attribute_cache_is_reused_across_language_switches() -> None:
    """Repeated language changes reuse cached keys while updating the DOM."""
    script_path = ROOT / "i18n.js"
    harness = r'''
const fs = require("node:fs");
const script = fs.readFileSync(0, "utf8");
const reads = {i18n: 0, lang: 0};

function nodeWith(attributes, text = "") {
  return {
    attributes: {...attributes},
    textContent: text,
    listeners: {},
    getAttribute(name) {
      if (name === "data-i18n") reads.i18n += 1;
      if (name === "data-lang") reads.lang += 1;
      return this.attributes[name] ?? null;
    },
    setAttribute(name, value) { this.attributes[name] = String(value); },
    addEventListener(type, callback) { this.listeners[type] = callback; },
  };
}

const translated = [
  nodeWith({"data-i18n": "nav.intro"}),
  nodeWith({"data-i18n": "nav.problem"}),
];
const buttons = [
  nodeWith({"data-lang": "ko", "aria-pressed": "false"}),
  nodeWith({"data-lang": "en", "aria-pressed": "false"}),
];
global.window = {location: {search: "?lang=en"}};
global.localStorage = {getItem: () => null, setItem: () => {}};
Object.defineProperty(global, "navigator", {value: {language: "en-US"}});
global.document = {
  documentElement: {lang: ""},
  title: "",
  querySelectorAll(selector) {
    if (selector === "[data-i18n]") return translated;
    if (selector === "[data-lang]") return buttons;
    return [];
  },
  querySelector: () => null,
};

eval(script);
const firstEnglish = translated.map((node) => node.textContent);
setLanguage("ko");
const korean = translated.map((node) => node.textContent);
setLanguage("en");
const secondEnglish = translated.map((node) => node.textContent);

if (reads.i18n !== translated.length) {
  throw new Error(`translation keys read ${reads.i18n} times`);
}
if (reads.lang !== buttons.length * 2) {
  throw new Error(`language keys read ${reads.lang} times`);
}
if (JSON.stringify(firstEnglish) !== JSON.stringify(secondEnglish)) {
  throw new Error("English translations changed after a round trip");
}
if (JSON.stringify(firstEnglish) === JSON.stringify(korean)) {
  throw new Error("language switch did not update translated text");
}
if (buttons[0].attributes["aria-pressed"] !== "false" ||
    buttons[1].attributes["aria-pressed"] !== "true") {
  throw new Error("language button state is inconsistent");
}
'''
    completed = subprocess.run(
        ["node", "-e", harness],
        input=script_path.read_text(encoding="utf-8"),
        capture_output=True,
        check=False,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
