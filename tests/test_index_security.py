"""Security tests for the main site index.html."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"

def _index_html() -> str:
    """Return the main index HTML source."""
    return INDEX.read_text(encoding="utf-8")

def _csp_content(html: str) -> str:
    """Extract the CSP meta policy from the HTML."""
    match = re.search(
        r'<meta\s+http-equiv="Content-Security-Policy"\s+content="([^"]+)"',
        html,
    )
    assert match is not None, "index.html must declare a CSP meta policy"
    return match.group(1)

def test_index_declares_base_uri_none() -> None:
    """The main site prevents base tag injection attacks."""
    policy = _csp_content(_index_html())
    assert "base-uri 'none'" in policy
    assert "base-uri 'self'" not in policy
