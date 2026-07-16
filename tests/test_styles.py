"""Regression tests for performance-sensitive site CSS."""

import re
from html.parser import HTMLParser
from pathlib import Path


INDEX = Path(__file__).resolve().parents[1] / "index.html"
STYLES = Path(__file__).resolve().parents[1] / "styles.css"


class _ImageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images: list[dict[str, str | None]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "img":
            self.images.append(dict(attrs))


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


def test_images_decode_without_blocking_rendering():
    """Only off-screen raster images opt into asynchronous decoding."""
    parser = _ImageParser()
    parser.feed(INDEX.read_text(encoding="utf-8"))

    assert parser.images
    assert all(image.get("decoding") == "async" for image in parser.images if image.get("loading") == "lazy" and not image.get("src", "").endswith(".svg"))
