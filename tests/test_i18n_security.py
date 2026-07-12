"""Regression tests for i18n language input validation."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
I18N = ROOT / "i18n.js"
I18N_HTML_TEST = ROOT / "test_i18n.html"


def test_set_language_validates_before_dom_or_storage_writes():
    """Untrusted language input is whitelisted before it reaches browser state."""
    source = I18N.read_text(encoding="utf-8")

    validation = source.index("if (!allowedLanguages.includes(lang))")
    html_lang_write = source.index("document.documentElement.lang = lang")
    storage_write = source.index('localStorage.setItem("cwl-language", lang)')

    assert 'const allowedLanguages = ["ko", "en"];' in source
    assert validation < html_lang_write
    assert validation < storage_write


def test_manual_i18n_harness_covers_invalid_language_payloads():
    """The browser harness keeps explicit regression cases for invalid inputs."""
    source = I18N_HTML_TEST.read_text(encoding="utf-8")

    assert 'setLanguage("__proto__")' in source
    assert 'setLanguage("<script>alert(1)<\\/script>")' in source
