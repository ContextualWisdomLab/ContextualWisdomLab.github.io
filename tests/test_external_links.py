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


def _parse_html(file_path: Path) -> _LinkParser:
    parser = _LinkParser()
    parser.feed(file_path.read_text(encoding="utf-8"))
    return parser


def _external_links(parser: _LinkParser, file_name: str) -> list[dict[str, str | None]]:
    external = [a for a in parser.links if a.get("target") == "_blank"]
    return external


def test_external_links_reference_the_new_window_description() -> None:
    """Every external link points at the shared visually hidden warning."""
    for html_file in ROOT.rglob("*.html"):
        if ".git" in html_file.parts or ".pytest_cache" in html_file.parts or "components" in html_file.parts:
            continue

        parser = _parse_html(html_file)
        external = _external_links(parser, html_file.name)
        if not external:
            continue

        assert DESC_ID in parser.ids, (
            f"{html_file.name} must define the #{DESC_ID} description element"
        )
        for anchor in external:
            assert anchor.get("aria-describedby") == DESC_ID, (
                f"External link {anchor.get('href')} in {html_file.name} must reference #{DESC_ID}"
            )


def test_external_links_keep_the_localized_title() -> None:
    """The title stays as supplemental hover metadata in both locales."""
    for html_file in ROOT.rglob("*.html"):
        if ".git" in html_file.parts or ".pytest_cache" in html_file.parts or "components" in html_file.parts:
            continue

        parser = _parse_html(html_file)
        external = _external_links(parser, html_file.name)

        for anchor in external:
            assert anchor.get("title") == EXPECTED["title"], (
                f"External link {anchor.get('href')} in {html_file.name} is missing the Korean title"
            )

            # 404.html does not load i18n.js, so we only expect data-i18n-title on the homepage
            if html_file.name == "index.html":
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
    for html_file in ROOT.rglob("*.html"):
        if ".git" in html_file.parts or ".pytest_cache" in html_file.parts or "components" in html_file.parts:
            continue

        parser = _parse_html(html_file)
        external = _external_links(parser, html_file.name)
        if not external:
            continue

        html_content = html_file.read_text(encoding="utf-8")
        assert f'id="{DESC_ID}" class="visually-hidden"' in html_content, (
            f"{html_file.name} must define the visually-hidden class on the description element"
        )


def test_external_links_keep_opener_and_referrer_policy() -> None:
    """Every new-context link retains explicit opener isolation and referrer policy."""
    for html_file in ROOT.rglob("*.html"):
        if ".git" in html_file.parts or ".pytest_cache" in html_file.parts or "components" in html_file.parts:
            continue

        parser = _parse_html(html_file)
        external = _external_links(parser, html_file.name)

        for anchor in external:
            rel_tokens = {token.lower() for token in (anchor.get("rel") or "").split()}
            assert "noopener" in rel_tokens, (
                f"External link {anchor.get('href')} in {html_file.name} must keep opener isolation"
            )
            assert "noreferrer" in rel_tokens, (
                f"External link {anchor.get('href')} in {html_file.name} must keep the product referrer policy"
            )
