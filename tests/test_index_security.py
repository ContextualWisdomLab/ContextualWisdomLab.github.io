"""Security regression tests for the main index page."""

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"


def test_index_declares_strict_csp() -> None:
    """The main index page limits active content to same-origin assets."""
    html = INDEX.read_text(encoding="utf-8")
    match = re.search(
        r'<meta\s+http-equiv="Content-Security-Policy"\s+content="([^"]+)"',
        html,
    )
    assert match is not None, "index must declare a CSP meta policy"
    policy = match.group(1)

    for directive in (
        "default-src 'self'",
        "img-src 'self'",
        "object-src 'none'",
        "base-uri 'none'",
        "form-action 'none'",
        "upgrade-insecure-requests",
        "require-trusted-types-for 'script'",
    ):
        assert directive in policy
