"""Test that i18n.js supports data-i18n-title properly."""
from pathlib import Path
import re

def test_i18n_title_support() -> None:
    """Test that i18n.js statically parses [data-i18n-title]."""
    content = Path("i18n.js").read_text(encoding="utf-8")
    assert "[data-i18n], [data-i18n-title]" in content
    assert 'node.hasAttribute("data-i18n-title")' in content
    assert 'node.setAttribute("title"' in content
