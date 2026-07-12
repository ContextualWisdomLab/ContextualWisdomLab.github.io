"""Regression tests for performance-sensitive site CSS."""

from html.parser import HTMLParser
import re
from pathlib import Path


INDEX = Path(__file__).resolve().parents[1] / "index.html"
STYLES = Path(__file__).resolve().parents[1] / "styles.css"


class ImageCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.images: list[dict[str, str | None]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "img":
            self.images.append(dict(attrs))


def _images() -> list[dict[str, str | None]]:
    parser = ImageCollector()
    parser.feed(INDEX.read_text(encoding="utf-8"))
    return parser.images


def _rule(selector: str) -> str:
    css = STYLES.read_text(encoding="utf-8")
    match = re.search(rf"{re.escape(selector)}\s*\{{(?P<body>[^}}]+)\}}", css)
    assert match is not None, f"missing CSS rule: {selector}"
    return match.group("body")


def test_sections_defer_offscreen_rendering_with_stable_placeholder():
    """Ordinary sections retain their measured-size fallback while skipped."""
    rule = _rule(".section")

    assert "content-visibility: auto;" in rule
    assert "contain-intrinsic-size: 600px;" in rule
    assert "contain-intrinsic-size: auto 600px;" in rule


def test_tall_sections_reserve_larger_intrinsic_block_size():
    """Content-heavy sections reserve enough space to avoid scrollbar jumps."""
    rule = _rule(".section.dikw, .section.projects")

    assert "contain-intrinsic-size: 1000px;" in rule
    assert "contain-intrinsic-size: auto 1000px;" in rule


def test_lcp_image_prioritizes_synchronous_paint():
    """The hero LCP SVG keeps high priority without async decoding."""
    context_art = next(img for img in _images() if img.get("class") == "context-art")

    assert context_art["fetchpriority"] == "high"
    assert "decoding" not in context_art


def test_non_lcp_images_decode_asynchronously():
    """Non-LCP images use async decoding to reduce main-thread jank."""
    non_lcp_images = [img for img in _images() if img.get("class") != "context-art"]

    assert non_lcp_images
    assert all(img.get("decoding") == "async" for img in non_lcp_images)
