"""Regression test for bounded query parsing in the language resolver."""

import re
from pathlib import Path

I18N = Path(__file__).resolve().parents[1] / "i18n.js"


def test_url_search_params_truthiness_check() -> None:
    """URLSearchParams is only constructed when a query string exists."""
    content = I18N.read_text(encoding="utf-8")

    guarded = re.search(
        r"window\.location\.search\s*\?\s*new URLSearchParams\(window\.location\.search\)",
        content,
    )
    assert guarded is not None, (
        "preferredLanguage() must guard the URLSearchParams construction "
        "behind a window.location.search truthiness check"
    )
