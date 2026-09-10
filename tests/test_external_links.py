from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"


class _LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.links.append(dict(attrs))


def test_external_links_have_accessible_titles():
    """All target=_blank links must have i18n title attributes."""
    html = INDEX.read_text(encoding="utf-8")
    parser = _LinkParser()
    parser.feed(html)

    for attrs in parser.links:
        if attrs.get("target") == "_blank":
            assert attrs.get("title") == "새 창에서 열림", f"External link missing title: {attrs}"
            assert attrs.get("data-i18n-title") == "common.newTab", f"External link missing i18n title: {attrs}"


def test_i18n_has_new_tab_translation():
    """The i18n dictionary must contain the translation for new tabs."""
    i18n_js = (ROOT / "i18n.js").read_text(encoding="utf-8")
    assert '"common.newTab": "새 창에서 열림"' in i18n_js
    assert '"common.newTab": "Opens in a new window"' in i18n_js
