import re
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"

def test_external_links_have_accessible_titles():
    html = INDEX.read_text(encoding="utf-8")

    # Find all anchor tags
    links = re.findall(r'<a\s+[^>]*>', html)

    for link in links:
        if 'target="_blank"' in link:
            assert 'title="새 창에서 열림"' in link or "title='새 창에서 열림'" in link, f"External link {link} is missing a title attribute"
            assert 'data-i18n-title="common.newTab"' in link or "data-i18n-title='common.newTab'" in link, f"External link {link} is missing a data-i18n-title attribute"

def test_i18n_has_new_tab_translation():
    i18n_js = (ROOT / "i18n.js").read_text(encoding="utf-8")
    assert '"common.newTab": "새 창에서 열림"' in i18n_js
