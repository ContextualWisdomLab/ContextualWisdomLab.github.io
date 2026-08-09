"""Regression tests for performance-sensitive site CSS and image hints."""

import re
from html.parser import HTMLParser
from pathlib import Path


INDEX = Path(__file__).resolve().parents[1] / "index.html"
STYLES = Path(__file__).resolve().parents[1] / "styles.css"


class _ImageParser(HTMLParser):
    """Collect literal image attributes from the static homepage."""

    def __init__(self) -> None:
        """Initialize an empty image collection."""
        super().__init__()
        self.images: list[dict[str, str | None]] = []

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        """Record each ``img`` element encountered by the parser."""
        if tag == "img":
            self.images.append(dict(attrs))


def _rule(selector: str) -> str:
    """Return the declaration body for one exact CSS selector."""
    css = STYLES.read_text(encoding="utf-8")
    match = re.search(rf"{re.escape(selector)}\s*\{{(?P<body>[^}}]+)\}}", css)
    assert match is not None, f"missing CSS rule: {selector}"
    return match.group("body")


def _homepage_images() -> list[dict[str, str | None]]:
    """Parse and return every homepage image with its literal attributes."""
    parser = _ImageParser()
    parser.feed(INDEX.read_text(encoding="utf-8"))
    assert parser.images, "homepage must contain at least one image"
    return parser.images


def test_sections_defer_offscreen_rendering_with_stable_placeholder() -> None:
    """Ordinary sections retain their measured-size fallback while skipped."""
    rule = _rule(".section")

    assert "content-visibility: auto;" in rule
    assert "contain-intrinsic-size: 600px;" in rule
    assert "contain-intrinsic-size: auto 600px;" in rule


def test_tall_sections_reserve_larger_intrinsic_block_size() -> None:
    """Content-heavy sections reserve enough space to avoid scrollbar jumps."""
    rule = _rule(".section.dikw, .section.projects")

    assert "contain-intrinsic-size: 1000px;" in rule
    assert "contain-intrinsic-size: auto 1000px;" in rule


def test_eager_images_leave_decoding_to_the_user_agent() -> None:
    """Eager images use the standards-defined default ``auto`` decode hint."""
    eager_images = [
        image for image in _homepage_images() if image.get("loading") != "lazy"
    ]

    assert eager_images, "the initial viewport must contain eager images"
    assert all(image.get("decoding") is None for image in eager_images)


def test_lazy_images_decode_asynchronously() -> None:
    """Deferred images remain explicitly asynchronous and cannot pass vacuously."""
    lazy_images = [
        image for image in _homepage_images() if image.get("loading") == "lazy"
    ]

    assert lazy_images, "the long homepage must retain deferred images"
    assert all(image.get("decoding") == "async" for image in lazy_images)


def test_lcp_candidate_is_eager_and_high_priority() -> None:
    """The declared LCP candidate is eager without a forced decode strategy."""
    lcp_candidates = [
        image
        for image in _homepage_images()
        if image.get("fetchpriority") == "high"
    ]

    assert len(lcp_candidates) == 1
    lcp_candidate = lcp_candidates[0]
    assert lcp_candidate.get("loading") != "lazy"
    assert lcp_candidate.get("decoding") is None


def test_project_cards_are_fully_clickable_via_pseudo_element() -> None:
    """Project cards expose the complete card as the link target."""
    article_rule = _rule(".project-grid article")
    assert "position: relative;" in article_rule

    after_rule = _rule(".project-grid h3 a::after")
    assert "position: absolute;" in after_rule
    assert "inset: 0;" in after_rule


def test_skip_link_animates_transform_not_top() -> None:
    """Skip link must animate the compositor-only transform, never top."""
    rule = _rule(".skip-link")

    assert "transform: translateY(-100%);" in rule
    assert "transition: transform" in rule
    assert "transition: top" not in rule
