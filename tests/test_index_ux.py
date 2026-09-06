"""Test that index.html has UX enhancements."""
from pathlib import Path
import re

def test_external_links_have_title() -> None:
    """Test that external links have data-i18n-title."""
    content = Path("index.html").read_text(encoding="utf-8")
    links = re.findall(r'<a\s+[^>]*target="_blank"[^>]*>', content)
    for link in links:
        assert 'data-i18n-title' in link
        assert 'common.newWindow' in link
