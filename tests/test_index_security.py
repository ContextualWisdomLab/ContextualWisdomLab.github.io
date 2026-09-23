"""Security regression tests for the main page (index.html)."""

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"


def _index_html() -> str:
    """Return the main index.html source."""
    return INDEX.read_text(encoding="utf-8")


def _csp_content(html: str) -> str:
    """Extract the CSP meta policy from the HTML."""
    match = re.search(
        r'<meta\s+http-equiv="Content-Security-Policy"\s+content="([^"]+)"',
        html,
    )
    assert match is not None, "index.html must declare a CSP meta policy"
    return match.group(1)


def test_index_declares_strict_csp() -> None:
    """The main page limits active content using a strict deny-by-default CSP."""
    policy = _csp_content(_index_html())

    for directive in (
        "default-src 'none'",
        "script-src 'self'",
        "img-src 'self'",
        "font-src 'self'",
        "connect-src 'self'",
        "object-src 'none'",
        "base-uri 'none'",
        "form-action 'none'",
        "frame-src 'none'",
        "upgrade-insecure-requests",
        "require-trusted-types-for 'script'",
        "style-src 'self'",
    ):
        assert directive in policy
    assert "'unsafe-inline'" not in policy
    assert "'unsafe-eval'" not in policy

def test_index_has_no_inline_active_content() -> None:
    """Strict CSP remains enforceable without inline script or style exceptions."""
    html = _index_html()

    assert re.search(r"<style(?:\s|>)", html, flags=re.IGNORECASE) is None
    assert re.search(r"\sstyle\s*=", html, flags=re.IGNORECASE) is None
    assert re.search(
        r"<script(?![^>]*\bsrc=)[^>]*>", html, flags=re.IGNORECASE
    ) is None
    assert re.search(r"\son[a-z]+\s*=", html, flags=re.IGNORECASE) is None
    assert 'href="styles.css"' in html
    assert 'src="i18n.js"' in html
    assert (
        '<meta name="referrer" content="strict-origin-when-cross-origin">' in html
    )
