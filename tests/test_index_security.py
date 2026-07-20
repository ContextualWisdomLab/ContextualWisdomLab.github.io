"""Security tests for the main index.html."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"


def _index_html() -> str:
    """Return the index HTML source."""
    return INDEX.read_text(encoding="utf-8")


def _csp_content(html: str) -> str:
    """Extract the CSP meta policy from the index HTML."""
    match = re.search(
        r'<meta\s+http-equiv="Content-Security-Policy"\s+content="([^"]+)"',
        html,
    )
    assert match is not None, "index must declare a CSP meta policy"
    return match.group(1)


def test_index_declares_strict_csp() -> None:
    """The main site limits active content to strict whitelist."""
    policy = _csp_content(_index_html())

    for directive in (
        "default-src 'none'",
        "script-src 'self'",
        "style-src 'self'",
        "img-src 'self'",
        "font-src 'self'",
        "connect-src 'self'",
        "object-src 'none'",
        "base-uri 'none'",
        "form-action 'none'",
        "frame-src 'none'",
        "upgrade-insecure-requests",
        "require-trusted-types-for 'script'",
    ):
        assert directive in policy, f"Missing {directive} in CSP"
    assert "'unsafe-inline'" not in policy
    assert "'unsafe-eval'" not in policy
