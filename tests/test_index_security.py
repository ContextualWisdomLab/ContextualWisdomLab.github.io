"""Security regression tests for the main index."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"

def _index_html() -> str:
    """Return the index HTML source."""
    return INDEX.read_text(encoding="utf-8")

def test_index_declares_strict_base_uri() -> None:
    """The main index must enforce base-uri 'none' to prevent base tag injection."""
    html = _index_html()
    match = re.search(
        r'<meta\s+http-equiv="Content-Security-Policy"\s+content="([^"]+)"',
        html,
    )
    assert match is not None, "index.html must declare a CSP meta policy"
    policy = match.group(1)

    assert "base-uri 'none'" in policy, "base-uri must be 'none'"
    assert "base-uri 'self'" not in policy, "base-uri must not be 'self'"
