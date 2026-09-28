"""Regression contracts for the repository-facing release ledger."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHANGELOG = ROOT / "CHANGELOG.md"


def test_unreleased_entries_use_real_line_breaks() -> None:
    """Reject escaped newlines that merge adjacent Markdown list items."""
    changelog = CHANGELOG.read_text(encoding="utf-8")
    unreleased = changelog.split("## [Unreleased]", maxsplit=1)[1]

    assert r"\n-" not in unreleased
    assert unreleased.count("\n- ") >= 2
