"""Static-site accessibility contracts for external links."""

import re
import unittest
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX_HTML = (ROOT / "index.html").read_text(encoding="utf-8")
I18N_JS = (ROOT / "i18n.js").read_text(encoding="utf-8")


class _TargetBlankParser(HTMLParser):
    """Collect target-blank anchors and their relationship tokens."""

    def __init__(self) -> None:
        super().__init__()
        self.target_blank_links: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return
        values = {name: value or "" for name, value in attrs}
        if values.get("target") == "_blank":
            self.target_blank_links.append(values)


class ExternalLinkSemanticsTest(unittest.TestCase):
    """Keep visual and assistive-technology new-tab cues aligned."""

    def test_target_blank_links_keep_opener_isolation(self) -> None:
        """Every new-tab link must retain noopener and noreferrer."""
        parser = _TargetBlankParser()
        parser.feed(INDEX_HTML)
        self.assertGreater(len(parser.target_blank_links), 0)
        for link in parser.target_blank_links:
            rel_tokens = set(link.get("rel", "").split())
            self.assertIn("noopener", rel_tokens)
            self.assertIn("noreferrer", rel_tokens)

    def test_i18n_adds_localized_accessible_new_tab_names(self) -> None:
        """CSS-generated arrows must be complemented by localized semantics."""
        self.assertRegex(
            I18N_JS,
            re.compile(r'"a11y\.opensNewTab"\s*:\s*"[^\"]+"'),
        )
        self.assertIn('document.querySelectorAll(\'a[target="_blank"]\')', I18N_JS)
        self.assertIn('link.setAttribute("aria-label",', I18N_JS)
        self.assertIn('dict["a11y.opensNewTab"]', I18N_JS)
        self.assertIn("updateExternalLinkLabels(dict);", I18N_JS)


if __name__ == "__main__":
    unittest.main()
