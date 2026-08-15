"""Contracts for the repository-owned static-site test workflow."""

from __future__ import annotations

from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
CI_WORKFLOW = REPOSITORY_ROOT / ".github" / "workflows" / "ci.yml"
STATIC_TEST_RUNNER = REPOSITORY_ROOT / "scripts" / "run_static_tests.py"
CHECKOUT_V7_0_1_SHA = "3d3c42e5aac5ba805825da76410c181273ba90b1"
EXACT_EVENT_REPOSITORY = (
    "repository: ${{ github.event.pull_request.head.repo.full_name || github.repository }}"
)
EXACT_EVENT_SHA = "${{ github.event.pull_request.head.sha || github.sha }}"


def test_static_test_runner_is_repository_owned_and_fail_closed() -> None:
    """The test entry point discovers plain tests and rejects fixture drift."""
    assert STATIC_TEST_RUNNER.is_file()
    runner = STATIC_TEST_RUNNER.read_text(encoding="utf-8")

    for contract in (
        'glob("test_*.py")',
        'name.startswith("test_")',
        "inspect.signature(test_function)",
        "parameter-free tests only",
        "traceback.print_exc()",
        "return 1",
    ):
        assert contract in runner


def test_ci_executes_static_tests_without_ambient_write_authority() -> None:
    """Pull requests run the repository test entry point with read-only authority."""
    assert CI_WORKFLOW.is_file()
    workflow = CI_WORKFLOW.read_text(encoding="utf-8")

    assert "pull_request:" in workflow
    assert "push:" in workflow
    assert "pull_request_target:" not in workflow
    assert "permissions:\n  contents: read" in workflow
    assert f"actions/checkout@{CHECKOUT_V7_0_1_SHA}" in workflow
    assert "persist-credentials: false" in workflow
    assert "python3 scripts/run_static_tests.py" in workflow


def test_ci_checks_out_and_proves_the_literal_event_source() -> None:
    """PR validation runs the contributor head, not GitHub's synthetic merge ref."""
    workflow = CI_WORKFLOW.read_text(encoding="utf-8")

    assert EXACT_EVENT_REPOSITORY in workflow
    assert f"ref: {EXACT_EVENT_SHA}" in workflow
    assert f"EXPECTED_SHA: {EXACT_EVENT_SHA}" in workflow
    assert 'test "$(git rev-parse HEAD)" = "$EXPECTED_SHA"' in workflow
