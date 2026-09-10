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
    """Collect anchor start tags and elements carrying an id."""

    def __init__(self) -> None:
        super().__init__()
        self.links: list[dict[str, str | None]] = []
        self.ids: set[str] = set()

    def handle_starttag(self, tag, attrs) -> None:
        attributes = dict(attrs)
        element_id = attributes.get("id")
        if element_id:
            self.ids.add(element_id)
        if tag == "a":
            self.links.append(attributes)


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
