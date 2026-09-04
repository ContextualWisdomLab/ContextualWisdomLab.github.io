"""Test i18n security and runtime boundary behavior."""

import shutil
import subprocess

import pytest


def test_i18n_input_validation() -> None:
    """Test that allowedLanguages validation logic is correctly implemented in i18n.js."""
    with open("i18n.js", "r", encoding="utf-8") as f:
        content = f.read()

    # Check for whitelist validation
    assert "allowedLanguages = [\"ko\", \"en\"]" in content or "allowedLanguages = ['ko', 'en']" in content
    assert "allowedLanguages.includes" in content


def test_i18n_html_security_tests_present() -> None:
    """Test that explicit __proto__ and XSS payload checks exist in the HTML test harness."""
    with open("test_i18n.html", "r", encoding="utf-8") as f:
        content = f.read()

    assert "setLanguage(\"__proto__\")" in content
    assert "setLanguage(\"<script>alert(1)<\\/script>\")" in content


def test_i18n_avoids_log_injection() -> None:
    """Test that console.warn does not interpolate user input."""
    with open("i18n.js", "r", encoding="utf-8") as f:
        content = f.read()

    assert 'console.warn("[Security] Invalid language requested. Falling back to default.");' in content


def test_i18n_environment_validation() -> None:
    """Execute the i18n runtime without browser globals and require a clean exit."""
    node = shutil.which("node")
    if node is None:
        pytest.skip("Node.js is required for the non-browser i18n runtime contract")

    probe = r"""
const fs = require("fs");
const vm = require("vm");
const source = fs.readFileSync("i18n.js", "utf8");
const context = { console };
vm.createContext(context);
vm.runInContext(source + "\npreferredLanguage(); setLanguage('en');", context);
"""
    completed = subprocess.run(
        [node, "-e", probe],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
