"""Regression tests for .gitignore hygiene around local runtime state."""

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GITIGNORE = ROOT / ".gitignore"

# Machine-local OpenCode Loop artifacts: session JSON and logs can contain
# conversation content, so they must never be staged by a broad `git add .`.
PRIVATE_STATE = ".opencode/opencode-loop/"
PRIVATE_PATHS = [
    ".opencode/opencode-loop/loop.log",
    ".opencode/opencode-loop/ses_example.json",
    ".opencode/opencode-loop/goals/ses_example-goal.md",
]


def _patterns() -> list[str]:
    return [
        line.strip()
        for line in GITIGNORE.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    ]


def test_local_loop_state_is_ignored() -> None:
    """Loop session/log state is excluded while project config stays shareable."""
    patterns = _patterns()
    assert PRIVATE_STATE in patterns, (
        f".gitignore must ignore {PRIVATE_STATE!r} so loop state cannot be committed"
    )
    assert ".opencode/" not in patterns, (
        "ignoring all of .opencode/ would also drop shareable project config"
    )


def test_loop_state_paths_are_reported_ignored_by_git() -> None:
    """Git itself must classify representative loop-state paths as ignored."""
    for path in PRIVATE_PATHS:
        result = subprocess.run(
            ["git", "check-ignore", "--no-index", "-q", path],
            cwd=ROOT,
            capture_output=True,
        )
        assert result.returncode == 0, f"git does not ignore {path}"
