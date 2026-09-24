"""Regression tests for the accessible new-window warning on external links."""

from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
I18N = ROOT / "i18n.js"

DESC_ID = "new-window-desc"

EXPECTED = {
    "title": "새 창에서 열림",
    "key": "common.newTab",
}


class _LinkParser(HTMLParser):
    """Collect link attributes and the hidden visual warning inside each link."""

    def __init__(self) -> None:
        super().__init__()
        self.links: list[dict[str, str | None]] = []
        self.ids: set[str] = set()
        self.indicator_link_indexes: set[int] = set()
        self._current_link_index: int | None = None
        self._hidden_span_depth = 0

    def handle_starttag(self, tag, attrs) -> None:
        attributes = dict(attrs)
        element_id = attributes.get("id")
        if element_id:
            self.ids.add(element_id)
        if tag == "a":
            self.links.append(attributes)
            self._current_link_index = len(self.links) - 1
            return
        if (
            tag == "span"
            and self._current_link_index is not None
            and attributes.get("aria-hidden") == "true"
        ):
            self._hidden_span_depth = 1
        elif self._hidden_span_depth:
            self._hidden_span_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if self._hidden_span_depth:
            self._hidden_span_depth -= 1
        if tag == "a":
            self._current_link_index = None
            self._hidden_span_depth = 0

    def handle_data(self, data: str) -> None:
        if (
            self._current_link_index is not None
            and self._hidden_span_depth
            and data.strip() == "↗"
        ):
            self.indicator_link_indexes.add(self._current_link_index)


def _parse_index() -> _LinkParser:
    parser = _LinkParser()
    parser.feed(INDEX.read_text(encoding="utf-8"))
    assert parser.links, "homepage must contain at least one anchor"
    return parser


def _external_links(parser: _LinkParser) -> list[dict[str, str | None]]:
    external = [a for a in parser.links if a.get("target") == "_blank"]
    assert external, "homepage must contain at least one external link"
    return external


def test_external_links_reference_the_new_window_description() -> None:
    """Every external link points at the shared visually hidden warning."""
    parser = _parse_index()

    assert DESC_ID in parser.ids, (
        f"homepage must define the #{DESC_ID} description element"
    )
    for anchor in _external_links(parser):
        assert anchor.get("aria-describedby") == DESC_ID, (
            f"External link {anchor.get('href')} must reference #{DESC_ID}"
        )


def test_external_links_keep_the_localized_title() -> None:
    """The title stays as supplemental hover metadata in both locales."""
    parser = _parse_index()

    for anchor in _external_links(parser):
        assert anchor.get("title") == EXPECTED["title"], (
            f"External link {anchor.get('href')} is missing the Korean title"
        )
        assert anchor.get("data-i18n-title") == EXPECTED["key"], (
            f"External link {anchor.get('href')} is missing data-i18n-title"
        )


def test_non_button_external_links_have_hidden_visual_warning() -> None:
    """Text links expose a visual new-window cue without duplicating AT output."""
    parser = _parse_index()
    text_link_count = 0

    for index, anchor in enumerate(parser.links):
        if anchor.get("target") != "_blank":
            continue
        classes = set((anchor.get("class") or "").split())
        if "button" in classes:
            assert index not in parser.indicator_link_indexes, (
                f"Button-style external link {anchor.get('href')} should not gain a redundant arrow"
            )
            continue
        text_link_count += 1
        assert index in parser.indicator_link_indexes, (
            f"Text external link {anchor.get('href')} needs an aria-hidden ↗ warning"
        )

    assert text_link_count > 0, "homepage must retain at least one text external link"


def test_i18n_has_new_tab_translation() -> None:
    """Both dictionaries define the localized new-window warning."""
    i18n_js = I18N.read_text(encoding="utf-8")
    assert f'"{EXPECTED["key"]}": "새 창에서 열림"' in i18n_js
    assert f'"{EXPECTED["key"]}": "Opens in a new window"' in i18n_js


def test_visually_hidden_class_is_defined() -> None:
    """The description element relies on a CSP-safe external class."""
    css = (ROOT / "styles.css").read_text(encoding="utf-8")
    assert ".visually-hidden {" in css
    index = INDEX.read_text(encoding="utf-8")
    assert f'id="{DESC_ID}" class="visually-hidden"' in index


def test_external_links_keep_opener_and_referrer_policy() -> None:
    """Every new-context link retains explicit opener isolation and referrer policy."""
    parser = _parse_index()

    for anchor in _external_links(parser):
        rel_tokens = {token.lower() for token in (anchor.get("rel") or "").split()}
        assert "noopener" in rel_tokens, (
            f"External link {anchor.get('href')} must keep opener isolation"
        )
        assert "noreferrer" in rel_tokens, (
            f"External link {anchor.get('href')} must keep the product referrer policy"
        )
