"""Security regression test for button types."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_buttons_have_explicit_type() -> None:
    """Ensure all <button> elements have an explicit type attribute to prevent accidental form submissions."""
    for html_file in ROOT.rglob("*.html"):
        html = html_file.read_text(encoding="utf-8")
        buttons = re.findall(r'<button[^>]*>', html, flags=re.IGNORECASE)
        for button in buttons:
            assert 'type=' in button.lower(), f"Button missing type attribute in {html_file.name}: {button}"
