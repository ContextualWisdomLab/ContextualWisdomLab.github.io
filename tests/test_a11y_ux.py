"""Test UX and accessibility requirements for external links."""

from pathlib import Path


def _site_source() -> tuple[str, str]:
    """Return the homepage HTML and localization runtime sources."""
    return (
        Path("index.html").read_text(encoding="utf-8"),
        Path("i18n.js").read_text(encoding="utf-8"),
    )


def test_external_links_do_not_rely_on_title_for_context_change_warning() -> None:
    """New-window context must be exposed without hover-only title semantics."""
    html, js = _site_source()

    assert 'data-i18n-title="externalLink"' not in html
    assert 'title="새 창에서 열기"' not in html
    assert "data-i18n-title" not in js


def test_external_links_use_reusable_accessible_content_contract() -> None:
    """One runtime contract must add localized in-link context to every blank link."""
    html, js = _site_source()

    assert '"externalLink": "새 창에서 열기"' in js
    assert '"externalLink": "Opens in a new window"' in js
    assert "syncExternalLinkContext" in js
    assert "sr-only" in js

    blank_links = [line for line in html.splitlines() if 'target="_blank"' in line]
    assert blank_links
    for line in blank_links:
        assert 'rel="noopener noreferrer"' in line
        assert "data-external-link-context" in line
