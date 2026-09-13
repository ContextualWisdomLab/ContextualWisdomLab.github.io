"""Regression tests for the accessible new-window warning on external links."""

from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
NOT_FOUND = ROOT / "404.html"
I18N = ROOT / "i18n.js"
PAGES = (INDEX, NOT_FOUND)

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


def _parse_page(page: Path) -> _LinkParser:
    parser = _LinkParser()
    parser.feed(page.read_text(encoding="utf-8"))
    assert parser.links, f"{page.name} must contain at least one anchor"
    return parser


def _external_links(
    parser: _LinkParser, page: Path
) -> list[dict[str, str | None]]:
    external = [a for a in parser.links if a.get("target") == "_blank"]
    assert external, f"{page.name} must contain at least one external link"
    return external


def test_external_links_reference_the_new_window_description() -> None:
    """Every static page binds each new-window link to its shared warning."""
    for page in PAGES:
        parser = _parse_page(page)
        assert DESC_ID in parser.ids, (
            f"{page.name} must define the #{DESC_ID} description element"
        )
        for anchor in _external_links(parser, page):
            assert anchor.get("aria-describedby") == DESC_ID, (
                f"External link {anchor.get('href')} in {page.name} "
                f"must reference #{DESC_ID}"
            )


def test_homepage_external_links_keep_the_localized_title() -> None:
    """Homepage titles stay supplemental localized hover metadata."""
    parser = _parse_page(INDEX)

    for anchor in _external_links(parser, INDEX):
        assert anchor.get("title") == EXPECTED["title"], (
            f"External link {anchor.get('href')} is missing the Korean title"
        )
        assert anchor.get("data-i18n-title") == EXPECTED["key"], (
            f"External link {anchor.get('href')} is missing data-i18n-title"
        )


def test_404_external_links_keep_the_static_new_window_title() -> None:
    """The script-free 404 page keeps an explicit Korean new-window title."""
    parser = _parse_page(NOT_FOUND)

    for anchor in _external_links(parser, NOT_FOUND):
        assert anchor.get("title") == EXPECTED["title"], (
            f"External link {anchor.get('href')} in 404.html is missing its title"
        )


def test_i18n_has_new_tab_translation() -> None:
    """Both homepage dictionaries define the localized new-window warning."""
    i18n_js = I18N.read_text(encoding="utf-8")
    assert f'"{EXPECTED["key"]}": "새 창에서 열림"' in i18n_js
    assert f'"{EXPECTED["key"]}": "Opens in a new window"' in i18n_js


def test_visually_hidden_class_is_defined_for_each_page() -> None:
    """Description elements rely on the shared CSP-safe external class."""
    css = (ROOT / "styles.css").read_text(encoding="utf-8")
    assert ".visually-hidden {" in css
    for page in PAGES:
        markup = page.read_text(encoding="utf-8")
        assert f'id="{DESC_ID}" class="visually-hidden"' in markup


def test_external_links_keep_opener_and_referrer_policy() -> None:
    """Every new-context link retains opener isolation and referrer policy."""
    for page in PAGES:
        parser = _parse_page(page)
        for anchor in _external_links(parser, page):
            rel_tokens = {
                token.lower() for token in (anchor.get("rel") or "").split()
            }
            assert "noopener" in rel_tokens, (
                f"External link {anchor.get('href')} in {page.name} "
                "must keep opener isolation"
            )
            assert "noreferrer" in rel_tokens, (
                f"External link {anchor.get('href')} in {page.name} "
                "must keep the product referrer policy"
            )
