"""Regression contracts for visible external-link indicators."""

from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"


class _ExternalLinkParser(HTMLParser):
    """Collect new-tab anchors and their translation/icon descendants."""

    def __init__(self) -> None:
        super().__init__()
        self.links: list[dict[str, object]] = []
        self._current: dict[str, object] | None = None

    def handle_starttag(self, tag, attrs) -> None:
        attributes = dict(attrs)
        if tag == "a" and attributes.get("target") == "_blank":
            self._current = {
                "href": attributes.get("href"),
                "anchor_i18n": attributes.get("data-i18n"),
                "child_i18n": False,
                "indicator": False,
            }
            self.links.append(self._current)
            return
        if self._current is not None and tag == "span":
            if attributes.get("data-i18n"):
                self._current["child_i18n"] = True
            if attributes.get("aria-hidden") == "true":
                self._current["indicator"] = True

    def handle_endtag(self, tag) -> None:
        if tag == "a":
            self._current = None


def _parse_index() -> _ExternalLinkParser:
    parser = _ExternalLinkParser()
    parser.feed(INDEX.read_text(encoding="utf-8"))
    assert parser.links, "homepage must contain new-tab links"
    return parser


def test_every_new_tab_link_has_a_visible_decorative_indicator() -> None:
    """Each new-tab destination is visually predictable before activation."""
    parser = _parse_index()
    missing = [link["href"] for link in parser.links if not link["indicator"]]
    assert missing == [], f"new-tab links without a visible indicator: {missing}"


def test_translated_link_text_does_not_replace_the_indicator() -> None:
    """Locale updates target a child span so the decorative icon survives."""
    parser = _parse_index()
    unsafe = [
        link["href"]
        for link in parser.links
        if link["indicator"] and link["anchor_i18n"] and not link["child_i18n"]
    ]
    assert unsafe == [], f"locale replacement would remove indicators: {unsafe}"
