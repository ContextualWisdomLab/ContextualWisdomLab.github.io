"""Security regression tests for the main index.html."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"

def test_index_declares_strict_base_uri() -> None:
    """The main index.html restricts base-uri to 'none'."""
    html = INDEX.read_text(encoding="utf-8")
    match = re.search(
        r'<meta\s+http-equiv="Content-Security-Policy"\s+content="([^"]+)"',
        html,
    )
    assert match is not None, "index.html must declare a CSP meta policy"
    policy = match.group(1)
    assert "base-uri 'none'" in policy
