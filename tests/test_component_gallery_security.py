"""Security and accessibility regression tests for the component gallery."""

import re
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GALLERY = ROOT / "components" / "index.html"
GALLERY_SCRIPT = ROOT / "components" / "krds-gallery.js"


class _RoleCollector(HTMLParser):
    """Collect element attributes for ARIA roles used by the gallery."""

    def __init__(self) -> None:
        """Initialize an empty mapping from ARIA role to attribute dictionaries."""
        super().__init__()
        self.elements_by_role: dict[str, list[dict[str, str | None]]] = {}

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        """Record attributes for elements that declare an explicit ARIA role."""
        del tag
        attributes = dict(attrs)
        role = attributes.get("role")
        if role is not None:
            self.elements_by_role.setdefault(role, []).append(attributes)


def _gallery_html() -> str:
    """Return the component gallery HTML source."""
    return GALLERY.read_text(encoding="utf-8")


def _gallery_script() -> str:
    """Return the component gallery interaction script."""
    return GALLERY_SCRIPT.read_text(encoding="utf-8")


def _csp_content(html: str) -> str:
    """Extract the CSP meta policy from the HTML."""
    match = re.search(
        r'<meta\s+http-equiv="Content-Security-Policy"\s+content="([^"]+)"',
        html,
    )
    assert match is not None, "component gallery must declare a CSP meta policy"
    return match.group(1)


def _role_elements(html: str) -> dict[str, list[dict[str, str | None]]]:
    """Return gallery elements grouped by their explicit ARIA role."""
    collector = _RoleCollector()
    collector.feed(html)
    return collector.elements_by_role


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
    assert GALLERY_SCRIPT.is_file()
    script = _gallery_script()
    assert "innerHTML" not in script
    assert "outerHTML" not in script
    assert "eval(" not in script
    assert "new Function" not in script


def test_component_gallery_inputs_have_length_limits() -> None:
    """Ensure text-based inputs have length limits to bound browser work."""
    html = _gallery_html()
    inputs = re.findall(r"<input[^>]+>", html)
    for input_element in inputs:
        if 'type="checkbox"' in input_element or 'type="radio"' in input_element:
            continue
        assert "maxlength=" in input_element, (
            f"Input missing maxlength: {input_element}"
        )


def test_tab_markup_uses_one_roving_tab_stop() -> None:
    """Exactly one tab is initially keyboard reachable and selected."""
    roles = _role_elements(_gallery_html())
    tablists = roles.get("tablist", [])
    tabs = roles.get("tab", [])
    panels = roles.get("tabpanel", [])

    assert len(tablists) == 1
    assert tablists[0].get("aria-label"), "tablist needs an accessible name"
    assert len(tabs) >= 2
    assert len(panels) == len(tabs)

    selected_tabs = [tab for tab in tabs if tab.get("aria-selected") == "true"]
    keyboard_tabs = [tab for tab in tabs if tab.get("tabindex") == "0"]
    assert len(selected_tabs) == 1
    assert keyboard_tabs == selected_tabs
    assert all(tab.get("tabindex") in {"0", "-1"} for tab in tabs)

    panel_ids = {panel.get("id") for panel in panels}
    tab_ids = {tab.get("id") for tab in tabs}
    assert all(tab.get("aria-controls") in panel_ids for tab in tabs)
    assert all(panel.get("aria-labelledby") in tab_ids for panel in panels)
    assert all(panel.get("tabindex") == "0" for panel in panels)
