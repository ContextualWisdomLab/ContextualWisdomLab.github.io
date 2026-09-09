"""Accessibility regression tests for links that open a new browsing context."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
I18N_JS = ROOT / "i18n.js"


def _target_blank_links(html: str) -> list[tuple[str, str]]:
    """Return opening tags and bodies for anchors that explicitly open a new tab."""
    return re.findall(
        r"(<a\b[^>]*\btarget=[\"']_blank[\"'][^>]*>)(.*?)</a>",
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )


def test_external_links_expose_spoken_and_visual_new_tab_warning() -> None:
    """Bind the warning to semantics and a persistent visual indicator, not title tooltips."""
    html = INDEX.read_text(encoding="utf-8")
    links = _target_blank_links(html)
    assert links, "Expected at least one target=_blank link"

    referenced_ids: set[str] = set()
    for opening_tag, body in links:
        describedby = re.search(
            r"\baria-describedby=[\"']([^\"']+)[\"']",
            opening_tag,
            flags=re.IGNORECASE,
        )
        assert describedby, f"Missing aria-describedby warning in external link: {opening_tag}"
        referenced_ids.update(describedby.group(1).split())

        assert re.search(
            r"<span\b(?=[^>]*\bnew-tab-indicator\b)(?=[^>]*\baria-hidden=[\"']true[\"'])[^>]*>",
            body,
            flags=re.IGNORECASE,
        ), f"Missing persistent aria-hidden visual new-tab indicator: {opening_tag}"

        assert "noopener" in opening_tag, f"Missing noopener in rel attribute: {opening_tag}"
        assert "noreferrer" in opening_tag, f"Missing noreferrer in rel attribute: {opening_tag}"

    for description_id in referenced_ids:
        assert re.search(
            rf"\bid=[\"']{re.escape(description_id)}[\"']",
            html,
            flags=re.IGNORECASE,
        ), f"aria-describedby references missing id={description_id!r}"


def test_i18n_supports_new_tab_description() -> None:
    """Keep the spoken new-tab description localized in the existing language ledger."""
    content = I18N_JS.read_text(encoding="utf-8")
    assert '"common.newTab": "새 창에서 열림"' in content or "'common.newTab': '새 창에서 열림'" in content
    assert '"common.newTab": "Opens in a new tab"' in content or "'common.newTab': 'Opens in a new tab'" in content
