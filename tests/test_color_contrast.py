"""Regression tests for color contrast on the static homepage."""

from __future__ import annotations

import re
from pathlib import Path


STYLESHEET = Path(__file__).parents[1] / "styles.css"


def css_hex_variable(css: str, name: str) -> tuple[int, int, int]:
    """Return an RGB tuple for a six-digit CSS custom-property value."""
    match = re.search(rf"{re.escape(name)}:\s*#([0-9a-fA-F]{{6}})\s*;", css)
    assert match, f"missing six-digit color variable {name}"
    value = match.group(1)
    return tuple(int(value[index : index + 2], 16) for index in (0, 2, 4))


def relative_luminance(rgb: tuple[int, int, int]) -> float:
    """Return WCAG relative luminance for an sRGB color."""
    channels = []
    for component in rgb:
        channel = component / 255
        channels.append(
            channel / 12.92
            if channel <= 0.04045
            else ((channel + 0.055) / 1.055) ** 2.4
        )
    red, green, blue = channels
    return 0.2126 * red + 0.7152 * green + 0.0722 * blue


def contrast_ratio(first: tuple[int, int, int], second: tuple[int, int, int]) -> float:
    """Return the WCAG contrast ratio between two sRGB colors."""
    lighter, darker = sorted(
        (relative_luminance(first), relative_luminance(second)), reverse=True
    )
    return (lighter + 0.05) / (darker + 0.05)


def test_dikw_step_labels_meet_wcag_aa_on_light_backgrounds() -> None:
    """Keep DIKW step labels at 4.5:1 or better on supported light surfaces."""
    css = STYLESHEET.read_text(encoding="utf-8")
    rule = re.search(r"\.dikw-grid span\s*\{(?P<body>.*?)\}", css, re.DOTALL)

    assert rule, "missing .dikw-grid span rule"
    assert "color: var(--teal);" in rule.group("body")

    foreground = css_hex_variable(css, "--teal")
    for background_name in ("--white", "--paper"):
        background = css_hex_variable(css, background_name)
        ratio = contrast_ratio(foreground, background)
        assert ratio >= 4.5, (
            f"teal on {background_name} has only {ratio:.2f}:1 contrast"
        )
