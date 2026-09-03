from pathlib import Path

def test_i18n_supports_title_attribute() -> None:
    """Test that i18n.js supports data-i18n-title."""
    content = Path("i18n.js").read_text(encoding="utf-8")
    assert "data-i18n-title" in content
    assert "getAttribute(\"title\")" in content or "getAttribute('title')" in content
    assert "setAttribute(\"title\"" in content or "setAttribute('title'" in content
