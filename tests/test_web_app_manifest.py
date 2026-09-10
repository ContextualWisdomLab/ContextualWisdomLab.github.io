"""Regression tests for the web app manifest and its homepage wiring."""

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifest.webmanifest"
INDEX = ROOT / "index.html"

HEX_COLOR = re.compile(r"^#[0-9a-fA-F]{6}$")


def _manifest() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def _index() -> str:
    return INDEX.read_text(encoding="utf-8")


def test_homepage_links_the_manifest_and_theme_color() -> None:
    """A manifest has no effect unless the page links it."""
    html = _index()
    assert 'rel="manifest" href="manifest.webmanifest"' in html, (
        "index.html must reference manifest.webmanifest"
    )
    assert re.search(r'<meta\s+name="theme-color"\s+content="#16263d"', html), (
        "index.html must set the theme-color meta to the brand ink color"
    )


def test_homepage_declares_ios_touch_icon() -> None:
    """iOS ignores the web manifest icons; apple-touch-icon drives the home screen."""
    html = _index()
    match = re.search(
        r'<link\s+rel="apple-touch-icon"\s+href="([^"]+)"', html
    )
    assert match is not None, (
        "index.html must declare apple-touch-icon or iOS home-screen installs "
        "fall back to a screenshot of the page"
    )
    assert (ROOT / match.group(1)).is_file(), (
        f"apple-touch-icon references missing asset {match.group(1)}"
    )


def test_csp_allows_the_linked_manifest() -> None:
    """default-src 'none' would block the manifest unless manifest-src permits it."""
    html = _index()
    csp = re.search(
        r'<meta\s+http-equiv="Content-Security-Policy"\s+content="([^"]+)"', html
    )
    assert csp is not None, "index.html must declare a CSP meta policy"
    policy = csp.group(1)
    assert "default-src 'none'" in policy
    assert "manifest-src 'self'" in policy, (
        "CSP must explicitly allow manifest-src 'self'; otherwise default-src "
        "'none' blocks manifest.webmanifest and the install experience breaks"
    )


def test_manifest_has_required_fields() -> None:
    """The manifest must carry the fields browsers need to install the site."""
    data = _manifest()
    for field in ("name", "short_name", "start_url", "display", "icons"):
        assert data.get(field), f"manifest must declare {field!r}"
    assert data["start_url"] == "/", "start_url should be the site root"
    assert data["display"] in {"standalone", "minimal-ui", "fullscreen"}, (
        "display must be a valid manifest display mode"
    )


def test_manifest_colors_match_brand_tokens() -> None:
    """theme_color/background_color must be valid hex and match the CSS tokens."""
    data = _manifest()
    for field in ("theme_color", "background_color"):
        assert HEX_COLOR.match(data.get(field, "")), f"{field} must be a #rrggbb color"

    css = (ROOT / "styles.css").read_text(encoding="utf-8")
    assert data["theme_color"].lower() == "#16263d", "theme_color should be --ink"
    assert "--ink: #16263d" in css.lower()
    assert data["background_color"].lower() == "#f7f5f0", "background should be --paper"
    assert "--paper: #f7f5f0" in css.lower()


def test_manifest_icons_exist_and_declare_sizes() -> None:
    """Every icon must exist on disk and declare its size and purpose."""
    icons = _manifest()["icons"]
    assert any(icon.get("sizes") == "1024x1024" for icon in icons), (
        "a standard 1024x1024 install icon must be present"
    )
    for icon in icons:
        assert icon.get("src") and icon.get("sizes") and icon.get("type")
        assert (ROOT / icon["src"]).is_file(), (
            f"manifest references missing icon {icon['src']}"
        )
