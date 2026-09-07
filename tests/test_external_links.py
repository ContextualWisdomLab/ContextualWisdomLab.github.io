from pathlib import Path
from bs4 import BeautifulSoup
import pytest

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"

def test_external_links_have_accessible_titles():
    html = INDEX.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")
    external_links = soup.find_all("a", attrs={"target": "_blank"})

    for link in external_links:
        assert link.has_attr("title"), f"External link {link} is missing a title attribute"
        assert link.has_attr("data-i18n-title"), f"External link {link} is missing a data-i18n-title attribute"
        assert link["data-i18n-title"] == "common.newTab"

def test_i18n_has_new_tab_translation():
    i18n_js = (ROOT / "i18n.js").read_text(encoding="utf-8")
    assert '"common.newTab": "새 창에서 열림"' in i18n_js
