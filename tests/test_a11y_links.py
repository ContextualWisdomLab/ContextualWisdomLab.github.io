"""Accessibility regression tests for external links."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
I18N_JS = ROOT / "i18n.js"

def test_external_links_have_accessible_titles() -> None:
    """Ensure all links opening in a new tab have appropriate titles for accessibility."""
    html = INDEX.read_text(encoding="utf-8")
    links = re.findall(r'<a[^>]+>', html, flags=re.IGNORECASE)

    for link in links:
        if 'target="_blank"' in link or "target='_blank'" in link:
            assert 'title=' in link, f"Missing title in external link: {link}"
            assert 'data-i18n-title=' in link, f"Missing data-i18n-title in external link: {link}"
            assert 'noopener' in link, f"Missing noopener in rel attribute: {link}"
            assert 'noreferrer' in link, f"Missing noreferrer in rel attribute: {link}"

def test_i18n_supports_title_attribute() -> None:
    """Test that i18n.js correctly supports data-i18n-title."""
    content = I18N_JS.read_text(encoding="utf-8")
    assert '[data-i18n-title]' in content
    assert 'node.getAttribute("data-i18n-title")' in content
    assert '"common.newTab": "새 창에서 열림"' in content or "'common.newTab': '새 창에서 열림'" in content
    assert '"common.newTab": "Opens in a new tab"' in content or "'common.newTab': 'Opens in a new tab'" in content
