"""Test UX/A11y requirements."""
from pathlib import Path

def test_external_links_have_title() -> None:
    """Test that all external links have a dynamic title attribute for a11y."""
    html = Path("index.html").read_text(encoding="utf-8")
    js = Path("i18n.js").read_text(encoding="utf-8")

    # Verify dynamic logic
    assert "data-i18n-title" in js
    assert '"externalLink": "새 창에서 열기"' in js

    # Check target="_blank" has associated attributes using independent tokens
    for line in html.splitlines():
        if 'target="_blank"' in line:
            assert "data-i18n-title" in line
            assert "externalLink" in line
            assert "title" in line
