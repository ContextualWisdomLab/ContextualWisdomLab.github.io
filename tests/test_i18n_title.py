"""Test i18n title functionality presence."""

def test_i18n_title_query_selector_present() -> None:
    """Test that data-i18n-title is queried correctly in i18n.js."""
    with open("i18n.js", "r", encoding="utf-8") as f:
        content = f.read()

    assert "querySelectorAll(\"[data-i18n-title]\")" in content
    assert "getAttribute(\"title\")" in content
    assert "setAttribute(\"title\"" in content
