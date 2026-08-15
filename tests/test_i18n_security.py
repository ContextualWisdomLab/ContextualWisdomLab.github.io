"""Security contracts for the static site's language-selection boundary."""

from __future__ import annotations

import re
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
I18N_SOURCE = REPOSITORY_ROOT / "i18n.js"
I18N_BROWSER_HARNESS = REPOSITORY_ROOT / "test_i18n.html"
STATIC_INVALID_LANGUAGE_WARNING = (
    '"[Security] Invalid language requested. Falling back to default."'
)


def test_i18n_input_validation() -> None:
    """Language selection uses the finite Korean/English allow-list."""
    content = I18N_SOURCE.read_text(encoding="utf-8")

    assert re.search(
        r"allowedLanguages\s*=\s*\[(?:\"ko\",\s*\"en\"|'ko',\s*'en')\]",
        content,
    )
    assert "allowedLanguages.includes(lang)" in content


def test_i18n_html_security_tests_present() -> None:
    """The browser harness retains prototype and markup-shaped invalid inputs."""
    content = I18N_BROWSER_HARNESS.read_text(encoding="utf-8")

    assert 'setLanguage("__proto__")' in content
    assert 'setLanguage("<script>alert(1)<\\/script>")' in content


def test_invalid_language_warning_never_contains_the_untrusted_value() -> None:
    """The invalid-language branch emits one constant warning without ``lang``."""
    content = I18N_SOURCE.read_text(encoding="utf-8")
    invalid_branch = re.search(
        r"if\s*\(!allowedLanguages\.includes\(lang\)\)\s*\{"
        r"(?P<body>.*?)"
        r"\n\s*lang\s*=\s*[\"']ko[\"'];",
        content,
        re.DOTALL,
    )

    assert invalid_branch is not None
    warning_arguments = re.findall(
        r"console\.warn\((.*?)\);",
        invalid_branch.group("body"),
        re.DOTALL,
    )
    assert warning_arguments == [STATIC_INVALID_LANGUAGE_WARNING]
    assert "${lang}" not in invalid_branch.group("body")
    assert not re.search(r"console\.warn\([^)]*\blang\b", invalid_branch.group("body"))
