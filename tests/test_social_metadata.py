"""Regression tests for link-preview metadata on the static homepage."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
CANONICAL_ORIGIN = "https://contextualwisdomlab.github.io/"


def _index_html() -> str:
    return INDEX.read_text(encoding="utf-8")


def _meta_content(html: str, attribute: str, value: str) -> str:
    match = re.search(
        rf'<meta\s+{attribute}="{re.escape(value)}"\s+content="([^"]*)"',
        html,
    )
    assert match is not None, f"missing meta {attribute}={value!r}"
    return match.group(1)


def test_open_graph_image_is_an_absolute_url() -> None:
    """Crawlers reject relative og:image values, so it must be absolute."""
    content = _meta_content(_index_html(), "property", "og:image")
    assert content.startswith("https://"), f"og:image is not absolute: {content!r}"


def test_open_graph_url_is_canonical_origin() -> None:
    """og:url pins the shared identity to the canonical deployment origin."""
    assert _meta_content(_index_html(), "property", "og:url") == CANONICAL_ORIGIN


def test_canonical_link_matches_deployment_origin() -> None:
    """A canonical link collapses duplicate URLs for search engines."""
    html = _index_html()
    match = re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"', html)
    assert match is not None, "missing rel=canonical link"
    assert match.group(1) == CANONICAL_ORIGIN


def test_twitter_card_and_image_are_present() -> None:
    """Twitter/X uses its own card keys and needs an absolute image."""
    html = _index_html()
    assert _meta_content(html, "name", "twitter:card") == "summary"
    assert _meta_content(html, "name", "twitter:image").startswith("https://")


def test_open_graph_image_dimensions_and_alt_are_declared() -> None:
    """Preview geometry and alt text are declared for predictable rendering."""
    html = _index_html()
    assert _meta_content(html, "property", "og:image:width") == "1024"
    assert _meta_content(html, "property", "og:image:height") == "1024"
    assert _meta_content(html, "property", "og:image:alt").strip() != ""


def test_open_graph_site_name_and_locale_are_declared() -> None:
    """Site identity and locale help social platforms render richer cards."""
    html = _index_html()
    assert _meta_content(html, "property", "og:site_name") == "Contextual Wisdom Lab"
    assert _meta_content(html, "property", "og:locale") == "ko_KR"
