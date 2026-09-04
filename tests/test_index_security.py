"""Security regression tests for the main page (index.html)."""

import re
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"


class _BlankTargetAnchorParser(HTMLParser):
    """Collect anchors that intentionally open a new browsing context."""

    def __init__(self) -> None:
        super().__init__()
        self.anchors: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "a":
            return
        normalized = {name.lower(): value or "" for name, value in attrs}
        if normalized.get("target", "").lower() == "_blank":
            self.anchors.append(normalized)


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


def test_blank_target_links_keep_explicit_opener_and_referrer_policy() -> None:
    """New-context links keep explicit opener isolation and referrer suppression."""
    parser = _BlankTargetAnchorParser()
    parser.feed(_index_html())

    assert parser.anchors, "index.html must exercise the outbound-link policy"
    for anchor in parser.anchors:
        rel_tokens = {token.lower() for token in anchor.get("rel", "").split()}
        assert "noopener" in rel_tokens, (
            f"target=_blank link must keep explicit opener isolation: {anchor}"
        )
        assert "noreferrer" in rel_tokens, (
            f"target=_blank link must keep the product referrer policy: {anchor}"
        )
