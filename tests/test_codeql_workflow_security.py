"""Security contracts for the repository's manual CodeQL marker workflow."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CODEQL_WORKFLOW = ROOT / ".github" / "workflows" / "codeql.yml"
CHECKOUT_V7_0_1_SHA = "3d3c42e5aac5ba805825da76410c181273ba90b1"
CODEQL_V4_37_6_SHA = "5595ccaf912efad79be6eef63a5619ff05969be3"


def _workflow_source() -> str:
    """Return the complete manual CodeQL workflow source."""
    return CODEQL_WORKFLOW.read_text(encoding="utf-8")


def test_codeql_workflow_uses_current_immutable_action_pins() -> None:
    """The diagnostic workflow pins reviewed releases and drops Git credentials."""
    workflow = _workflow_source()

    assert (
        f"uses: actions/checkout@{CHECKOUT_V7_0_1_SHA} # v7.0.1" in workflow
    )
    assert "persist-credentials: false" in workflow
    assert (
        workflow.count(
            f"uses: github/codeql-action/init@{CODEQL_V4_37_6_SHA} # v4.37.6"
        )
        == 1
    )
    assert (
        workflow.count(
            f"uses: github/codeql-action/analyze@{CODEQL_V4_37_6_SHA} # v4.37.6"
        )
        == 1
    )
