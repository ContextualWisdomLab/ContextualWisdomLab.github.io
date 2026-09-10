"""Security regression tests for the standalone component gallery."""

import re
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GALLERY = ROOT / "components" / "index.html"


class _ButtonCollector(HTMLParser):
    """Collect parsed button start tags with their real attribute values."""

    def __init__(self) -> None:
        super().__init__()
        self.buttons: list[dict[str, str | None]] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag == "button":
            self.buttons.append(dict(attrs))

    def handle_startendtag(self, tag: str, attrs) -> None:
        if tag == "button":
            self.buttons.append(dict(attrs))


def _parsed_buttons(html: str) -> list[dict[str, str | None]]:
    parser = _ButtonCollector()
    parser.feed(html)
    return parser.buttons


def _gallery_html() -> str:
    """Return the component gallery HTML source."""
    return GALLERY.read_text(encoding="utf-8")


def _csp_content(html: str) -> str:
    """Extract the CSP meta policy from the gallery HTML."""
    match = re.search(
        r'<meta\s+http-equiv="Content-Security-Policy"\s+content="([^"]+)"',
        html,
    )
    assert match is not None, "component gallery must declare a CSP meta policy"
    return match.group(1)


def test_component_gallery_declares_strict_csp() -> None:
    """The standalone gallery limits active content to same-origin assets."""
    policy = _csp_content(_gallery_html())

    for directive in (
        "default-src 'none'",
        "script-src 'self'",
        "img-src 'self' data:",
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


def test_component_gallery_has_no_inline_active_content() -> None:
    """Strict CSP remains enforceable without inline script or style exceptions."""
    html = _gallery_html()

    assert re.search(r"<style(?:\s|>)", html, flags=re.IGNORECASE) is None
    assert re.search(r"\sstyle\s*=", html, flags=re.IGNORECASE) is None
    assert re.search(
        r"<script(?![^>]*\bsrc=)[^>]*>", html, flags=re.IGNORECASE
    ) is None
    assert re.search(r"\son[a-z]+\s*=", html, flags=re.IGNORECASE) is None
    assert 'href="krds-gallery.css"' in html
    assert 'src="krds-gallery.js"' in html
    assert (
        '<meta name="referrer" content="strict-origin-when-cross-origin">' in html
    )


def test_component_gallery_script_avoids_unsafe_dom_sinks() -> None:
    """The extracted interaction script keeps Trusted Types enforcement viable."""
    script_path = ROOT / "components" / "krds-gallery.js"

    assert script_path.is_file()
    script = script_path.read_text(encoding="utf-8")
    assert "innerHTML" not in script
    assert "outerHTML" not in script
    assert "eval(" not in script
    assert "new Function" not in script

def test_component_gallery_inputs_have_length_limits() -> None:
    """Ensure all text-based inputs have maxlength defined to mitigate DoS risks."""
    html = _gallery_html()
    inputs = re.findall(r'<input[^>]+>', html)
    for inp in inputs:
        if 'type="checkbox"' in inp or 'type="radio"' in inp:
            continue
        assert 'maxlength=' in inp, f"Input missing maxlength: {inp}"

def test_component_gallery_buttons_have_explicit_type() -> None:
    """Every button carries a parsed type attribute of exactly 'button'."""
    buttons = _parsed_buttons(_gallery_html())

    assert buttons, "component gallery must render at least one button"
    for attrs in buttons:
        assert attrs.get("type") == "button", (
            f"Button missing type=\"button\": {attrs}"
        )
