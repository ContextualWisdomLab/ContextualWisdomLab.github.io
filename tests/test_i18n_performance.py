import re
from pathlib import Path

def test_url_search_params_truthiness_check() -> None:
    """URLSearchParams 객체 생성 시 불필요한 파싱 오버헤드를 줄이기 위한 조건문이 있는지 확인합니다."""
    content = Path("i18n.js").read_text(encoding="utf-8")
    assert "window.location.search ?" in content or "if (window.location.search)" in content
    assert "new URLSearchParams" in content
