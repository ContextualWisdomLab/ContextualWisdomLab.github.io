"""Test i18n security input validation."""

from __future__ import annotations

import subprocess
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
I18N_SCRIPT = REPOSITORY_ROOT / "i18n.js"


def _run_i18n_harness(harness: str) -> subprocess.CompletedProcess[str]:
    """Execute a dependency-free Node harness against the checked-in i18n script."""
    return subprocess.run(
        ["node", "-e", harness],
        input=I18N_SCRIPT.read_text(encoding="utf-8"),
        capture_output=True,
        check=False,
        text=True,
    )


def test_i18n_input_validation() -> None:
    """Test that allowedLanguages validation logic is correctly implemented in i18n.js."""
    with open("i18n.js", "r", encoding="utf-8") as f:
        content = f.read()

    # Check for whitelist validation
    assert (
        'allowedLanguages = ["ko", "en"]' in content
        or "allowedLanguages = ['ko', 'en']" in content
    )
    assert "allowedLanguages.includes" in content


def test_i18n_html_security_tests_present() -> None:
    """Test that explicit __proto__ and XSS payload checks exist in the HTML test harness."""
    with open("test_i18n.html", "r", encoding="utf-8") as f:
        content = f.read()

    assert 'setLanguage("__proto__")' in content
    assert 'setLanguage("<script>alert(1)<\\/script>")' in content


def test_i18n_avoids_log_injection() -> None:
    """Test that console.warn does not interpolate user input."""
    with open("i18n.js", "r", encoding="utf-8") as f:
        content = f.read()

    assert (
        'console.warn("[Security] Invalid language requested. Falling back to default.");'
        in content
    )


def test_i18n_environment_validation() -> None:
    """Executing the script in a non-browser context must not throw."""
    harness = r"""
const fs = require("node:fs");
const script = fs.readFileSync(0, "utf8");

global.window = undefined;
global.document = undefined;
global.navigator = undefined;

eval(script);

if (typeof setLanguage !== "function") {
  throw new Error("setLanguage was not defined");
}
if (setLanguage("en") !== undefined) {
  throw new Error("setLanguage must be a no-op without a DOM");
}
"""
    completed = _run_i18n_harness(harness)
    assert completed.returncode == 0, completed.stderr


def test_i18n_dom_guard_prevents_partial_init_without_document() -> None:
    """A window without a document must not trigger DOM access on init or direct calls."""
    harness = r"""
const fs = require("node:fs");
const script = fs.readFileSync(0, "utf8");

global.window = {location: {search: "?lang=en"}, localStorage: {getItem: () => null, setItem: () => {}}};
global.document = undefined;
global.navigator = {language: "ko-KR"};

eval(script);

// Direct calls must also fail safely rather than dereferencing a missing document.
if (setLanguage("en") !== undefined) {
  throw new Error("setLanguage must be a no-op without a document");
}
if (setLanguage("ko") !== undefined) {
  throw new Error("setLanguage must be a no-op without a document");
}
"""
    completed = _run_i18n_harness(harness)
    assert completed.returncode == 0, completed.stderr


import re


def _csp_content_test_i18n(html: str) -> str:
    """Extract the CSP meta policy from the HTML."""
    match = re.search(
        r'<meta\s+http-equiv="Content-Security-Policy"\s+content="([^"]+)"',
        html,
    )
    assert match is not None, "test_i18n.html must declare a CSP meta policy"
    return match.group(1)


def test_i18n_test_declares_strict_csp() -> None:
    """The i18n test page limits active content using a strict deny-by-default CSP."""
    from pathlib import Path

    html = (Path(__file__).resolve().parents[1] / "test_i18n.html").read_text(
        encoding="utf-8"
    )
    policy = _csp_content_test_i18n(html)
    for directive in (
        "default-src 'none'",
        "script-src 'self' 'unsafe-inline'",
        "style-src 'none'",
        "img-src 'self'",
        "font-src 'none'",
        "connect-src 'none'",
        "object-src 'none'",
        "base-uri 'none'",
        "form-action 'none'",
        "frame-src 'none'",
        "upgrade-insecure-requests",
    ):
        assert directive in policy
    assert "'unsafe-eval'" not in policy
