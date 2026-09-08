"""Tests for UX/accessibility enhancements."""
import re
from pathlib import Path

def test_external_links_have_a11y_tooltips() -> None:
    html = Path("index.html").read_text(encoding="utf-8")
    links = re.findall(r'<a[^>]*target="_blank"[^>]*>', html)
    assert len(links) > 0
    for link in links:
        assert 'title="새 탭에서 열기"' in link
        assert 'data-i18n-title="a11y.newWindow"' in link

def test_i18n_uses_getattribute_not_dataset() -> None:
    js = Path("i18n.js").read_text(encoding="utf-8")
    assert "node.dataset.i18n" not in js
    assert 'node.getAttribute("data-i18n")' in js
    assert 'node.getAttribute("data-i18n-title")' in js
