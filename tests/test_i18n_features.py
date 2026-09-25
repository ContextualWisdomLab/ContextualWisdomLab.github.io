from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_i18n_js_supports_title_translation() -> None:
    js = (ROOT / "i18n.js").read_text(encoding="utf-8")
    assert "data-i18n-title" in js
    assert "querySelectorAll(\"[data-i18n], [data-i18n-title]\")" in js
    assert "node.getAttribute" in js
    assert "node.dataset" not in js

def test_index_html_uses_title_translation() -> None:
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    assert "data-i18n-title" in html

def test_i18n_optimizations() -> None:
    js = (ROOT / "i18n.js").read_text(encoding="utf-8")
    assert "getElementById(\"footer-logo\")" in js
    assert "hasAttribute" not in js or "node.hasAttribute" not in js # Ensure hasAttribute is not used redundantly for i18n
