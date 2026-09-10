"""Regression tests for localized new-window warnings on external links."""

from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
I18N = ROOT / "i18n.js"

EXPECTED_KO_TITLE = "새 창에서 열림"
EXPECTED_EN_TITLE = "Opens in a new window"


class _AnchorParser(HTMLParser):
    """Collect literal anchor attributes from the static homepage."""

    def __init__(self) -> None:
        """Initialize an empty anchor collection."""
        super().__init__()
        self.anchors: list[dict[str, str | None]] = []

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        """Record each ``a`` element encountered by the parser."""
        if tag == "a":
            self.anchors.append(dict(attrs))


def _external_links() -> list[dict[str, str | None]]:
    """Parse and return every anchor that opens in a new browsing context."""
    parser = _AnchorParser()
    parser.feed(INDEX.read_text(encoding="utf-8"))
    external = [a for a in parser.anchors if a.get("target") == "_blank"]
    assert external, "homepage must contain at least one external link"
    return external


def test_external_links_have_accessible_titles() -> None:
    """Every ``target="_blank"`` anchor carries both title attributes."""
    for anchor in _external_links():
        assert anchor.get("title") == EXPECTED_KO_TITLE, (
            f"External link {anchor.get('href')} is missing the Korean title"
        )
        assert anchor.get("data-i18n-title") == "common.newTab", (
            f"External link {anchor.get('href')} is missing data-i18n-title"
        )


def test_i18n_has_new_tab_translation() -> None:
    """Both dictionaries define the localized new-window warning."""
    i18n_js = I18N.read_text(encoding="utf-8")
    assert f'"common.newTab": "{EXPECTED_KO_TITLE}"' in i18n_js
    assert f'"common.newTab": "{EXPECTED_EN_TITLE}"' in i18n_js
