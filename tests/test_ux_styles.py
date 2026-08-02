"""Regression tests for UX-focused CSS styles."""

import re
from pathlib import Path

STYLES = Path(__file__).resolve().parents[1] / "styles.css"

def test_buttons_have_active_state_for_tactile_feedback():
    """Ensure buttons provide tactile feedback on click."""
    css = STYLES.read_text(encoding="utf-8")
    assert ".button:active" in css
    assert ".language-switch button:active" in css
    assert "transform: scale(0.96);" in css
