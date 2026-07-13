import re

def test_i18n_input_validation():
    with open("i18n.js", "r", encoding="utf-8") as f:
        content = f.read()

    # Check for whitelist validation
    assert "allowedLanguages = [\"ko\", \"en\"]" in content or "allowedLanguages = ['ko', 'en']" in content
    assert "allowedLanguages.includes" in content

def test_i18n_html_security_tests_present():
    with open("test_i18n.html", "r", encoding="utf-8") as f:
        content = f.read()

    assert "setLanguage(\"__proto__\")" in content
    assert "setLanguage(\"<script>alert(1)<\\/script>\")" in content
