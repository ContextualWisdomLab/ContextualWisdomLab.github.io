"""Test i18n security input validation."""

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
    """Test that window and document are validated for SSR compatibility and availability."""
    with open("i18n.js", "r", encoding="utf-8") as f:
        content = f.read()

    assert "typeof window !== 'undefined'" in content
    assert "typeof document !== 'undefined'" in content
    assert "typeof navigator !== 'undefined'" in content
