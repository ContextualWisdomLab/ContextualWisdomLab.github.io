"""Security regression test for button types."""
from pathlib import Path
from html.parser import HTMLParser
import pytest

ROOT = Path(__file__).resolve().parents[1]

class ButtonTypeParser(HTMLParser):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.failed_buttons = []

    def handle_starttag(self, tag, attrs):
        if tag == 'button':
            attr_dict = dict(attrs)
            if 'type' not in attr_dict:
                self.failed_buttons.append(f"Button missing type attribute in {self.filename}")

def test_buttons_have_explicit_type() -> None:
    """Ensure all <button> elements have an explicit type attribute to prevent accidental form submissions."""
    target_files = [
        ROOT / "index.html",
        ROOT / "components" / "index.html",
        ROOT / "test_i18n.html",
    ]
    for html_file in target_files:
        assert html_file.is_file(), f"Expected test file missing: {html_file}"
        html = html_file.read_text(encoding="utf-8")
        parser = ButtonTypeParser(html_file.name)
        parser.feed(html)
        assert not parser.failed_buttons, "\n".join(parser.failed_buttons)

def test_button_parser_detects_missing_type() -> None:
    """Verify that the ButtonTypeParser correctly identifies buttons without a type."""
    html = '<form><button>Submit</button><button type="button">Cancel</button></form>'
    parser = ButtonTypeParser("mock.html")
    parser.feed(html)
    assert len(parser.failed_buttons) == 1
    assert "mock.html" in parser.failed_buttons[0]
