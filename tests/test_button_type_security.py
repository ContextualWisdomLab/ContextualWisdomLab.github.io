"""Regression tests for explicit HTML button behavior."""

from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ButtonTypeParser(HTMLParser):
    def __init__(self, filename: str) -> None:
        super().__init__()
        self.filename = filename
        self.failed_buttons: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "button":
            attr_dict = dict(attrs)
            if "type" not in attr_dict:
                self.failed_buttons.append(
                    f"Button missing type attribute in {self.filename}"
                )


def test_buttons_have_explicit_type() -> None:
    """Require button intent to stay explicit if a component is later placed in a form."""
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
    """Keep the regression harness sensitive to the HTML default-submit case."""
    html = '<form><button>Submit</button><button type="button">Cancel</button></form>'
    parser = ButtonTypeParser("mock.html")
    parser.feed(html)
    assert len(parser.failed_buttons) == 1
    assert "mock.html" in parser.failed_buttons[0]
