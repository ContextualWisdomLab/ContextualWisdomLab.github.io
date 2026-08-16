"""Executable static-site contracts for links that open a new tab."""

from html.parser import HTMLParser
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
INDEX_HTML = (ROOT / "index.html").read_text(encoding="utf-8")
I18N_SOURCE = (ROOT / "i18n.js").read_text(encoding="utf-8")


class _ExternalLinkParser(HTMLParser):
    """Collect visible text and attributes for target-blank anchors."""

    def __init__(self) -> None:
        super().__init__()
        self.links: list[dict[str, object]] = []
        self._current: dict[str, object] | None = None
        self._anchor_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if self._current is not None:
            self._anchor_depth += 1
            return
        if tag != "a":
            return
        attributes = {key: value or "" for key, value in attrs}
        if attributes.get("target") != "_blank":
            return
        self._current = {"attributes": attributes, "text": []}
        self._anchor_depth = 0

    def handle_data(self, data: str) -> None:
        if self._current is not None:
            text = self._current["text"]
            assert isinstance(text, list)
            text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if self._current is None:
            return
        if self._anchor_depth > 0:
            self._anchor_depth -= 1
            return
        if tag != "a":
            return
        text = self._current["text"]
        assert isinstance(text, list)
        self._current["text"] = "".join(text).strip()
        self.links.append(self._current)
        self._current = None


class TestExternalLinkAccessibility(unittest.TestCase):
    """Keep visual new-tab cues aligned with secure accessible semantics."""

    def test_every_target_blank_link_retains_opener_isolation_and_visible_text(self) -> None:
        """Every real target-blank link must be safe and have a visible label."""
        parser = _ExternalLinkParser()
        parser.feed(INDEX_HTML)

        self.assertGreater(len(parser.links), 0)
        for link in parser.links:
            attributes = link["attributes"]
            assert isinstance(attributes, dict)
            rel = set(str(attributes.get("rel", "")).split())
            self.assertIn("noopener", rel)
            self.assertIn("noreferrer", rel)
            self.assertTrue(str(link["text"]).strip())

    def test_i18n_contract_localizes_new_tab_accessible_name(self) -> None:
        """The language switch must add a localized cue without losing visible text."""
        self.assertRegex(
            I18N_SOURCE,
            r'"a11y\.opensNewTab"\s*:\s*"새 탭에서 열림"',
        )
        self.assertRegex(
            I18N_SOURCE,
            r'"a11y\.opensNewTab"\s*:\s*"opens in a new tab"',
        )
        self.assertIn(
            'document.querySelectorAll(\'a[target="_blank"]\')',
            I18N_SOURCE,
        )
        self.assertIn('dict["a11y.opensNewTab"]', I18N_SOURCE)
        self.assertRegex(
            I18N_SOURCE,
            re.compile(
                r"linkText\s*=\s*link\.textContent\.trim\(\).*?"
                r"accessibleName\s*=\s*`\$\{linkText\} \(\$\{dict\[[\"']a11y\.opensNewTab[\"']\]\}\)`.+?"
                r"link\.setAttribute\(\s*[\"']aria-label[\"']\s*,\s*accessibleName\s*\)",
                re.DOTALL,
            ),
        )

    def test_homepage_product_destinations_use_current_owned_repos(self) -> None:
        """Project and fork cards must open the current owned repositories."""
        parser = _ExternalLinkParser()
        parser.feed(INDEX_HTML)
        hrefs = []
        for link in parser.links:
            attributes = link["attributes"]
            assert isinstance(attributes, dict)
            hrefs.append(str(attributes.get("href", "")))

        self.assertIn("https://github.com/ContextualWisdomLab/wardnet", hrefs)
        self.assertIn("https://github.com/ContextualWisdomLab/argos", hrefs)
        self.assertIn("https://github.com/ContextualWisdomLab/vooster", hrefs)
        self.assertNotIn(
            "https://github.com/ContextualWisdomLab/waf-ids-ai-soc",
            hrefs,
        )
        self.assertNotIn(
            "https://github.com/ContextualWisdomLab/vooster-v2-mvp",
            hrefs,
        )
        self.assertIn('"projects.wardnetTitle"', I18N_SOURCE)
        self.assertNotIn("projects.wafIdsTitle", I18N_SOURCE)
        self.assertNotIn("waf-ids-ai-soc", INDEX_HTML)


if __name__ == "__main__":
    unittest.main()
