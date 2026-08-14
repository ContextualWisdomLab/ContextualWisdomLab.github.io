"""Security contracts for the repository's manual CodeQL marker workflow."""

from __future__ import annotations

from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CODEQL_WORKFLOW = ROOT / ".github" / "workflows" / "codeql.yml"
CHECKOUT_V7_0_1_SHA = "3d3c42e5aac5ba805825da76410c181273ba90b1"
CODEQL_V4_37_6_SHA = "5595ccaf912efad79be6eef63a5619ff05969be3"


def _parse_scalar(raw_value: str) -> str | bool:
    """Parse the small set of YAML scalars used by the workflow contract."""
    value = raw_value.split(" #", 1)[0].strip()
    if value == "false":
        return False
    if value == "true":
        return True
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def _workflow_structure(workflow_path: Path = CODEQL_WORKFLOW) -> dict[str, Any]:
    """Parse the workflow subset needed to bind permissions and action steps."""
    permissions: dict[str, str | bool] = {}
    jobs: dict[str, dict[str, Any]] = {}
    current_job: dict[str, Any] | None = None
    current_step: dict[str, Any] | None = None
    current_section: str | None = None
    in_step_with = False
    in_job_permissions = False

    for raw_line in workflow_path.read_text(encoding="utf-8").splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        line = raw_line.strip()

        if indent == 0:
            current_job = None
            current_step = None
            in_step_with = False
            in_job_permissions = False
            current_section = line[:-1] if line.endswith(":") else None
            continue

        if current_section == "permissions" and indent == 2:
            key, separator, value = line.partition(":")
            assert separator, f"malformed permissions entry: {line!r}"
            permissions[key] = _parse_scalar(value)
            continue

        if current_section != "jobs":
            continue

        if indent == 2 and line.endswith(":"):
            job_name = line[:-1]
            current_job = {"steps": [], "permissions": {}}
            jobs[job_name] = current_job
            current_step = None
            in_step_with = False
            in_job_permissions = False
            continue

        if current_job is None:
            continue

        if indent == 4:
            in_job_permissions = line == "permissions:"
            continue

        if indent == 6 and in_job_permissions:
            key, separator, value = line.partition(":")
            assert separator, f"malformed job permissions entry: {line!r}"
            current_job["permissions"][key] = _parse_scalar(value)
            continue

        if indent == 6 and line.startswith("- "):
            current_step = {}
            current_job["steps"].append(current_step)
            in_step_with = False
            in_job_permissions = False
            first_key, separator, value = line[2:].partition(":")
            if separator:
                current_step[first_key] = _parse_scalar(value)
            continue

        if current_step is None:
            continue

        if indent == 8:
            key, separator, value = line.partition(":")
            if not separator:
                continue
            if key == "with" and not value.strip():
                current_step["with"] = {}
                in_step_with = True
            else:
                current_step[key] = _parse_scalar(value)
                in_step_with = False
            continue

        if indent == 10 and in_step_with:
            key, separator, value = line.partition(":")
            assert separator, f"malformed step input: {line!r}"
            current_step["with"][key] = _parse_scalar(value)

    return {"permissions": permissions, "jobs": jobs}


def _single_action_step(workflow: dict[str, Any], action: str) -> dict[str, Any]:
    """Return the sole workflow step whose action belongs to ``action``."""
    steps = [
        step
        for job in workflow["jobs"].values()
        for step in job["steps"]
        if str(step.get("uses", "")).startswith(f"{action}@")
    ]
    assert len(steps) == 1, f"expected exactly one {action} step, found {len(steps)}"
    return steps[0]


def test_codeql_workflow_uses_current_immutable_action_pins() -> None:
    """Bind each reviewed action and security control to its exact YAML step."""
    workflow = _workflow_structure()

    assert workflow["permissions"] == {"contents": "read"}
    for job in workflow["jobs"].values():
        effective_permissions = workflow["permissions"] | job["permissions"]
        assert effective_permissions == {"contents": "read"}

    checkout = _single_action_step(workflow, "actions/checkout")
    assert checkout["uses"] == f"actions/checkout@{CHECKOUT_V7_0_1_SHA}"
    assert checkout.get("with", {}).get("persist-credentials") is False

    init = _single_action_step(workflow, "github/codeql-action/init")
    assert init["uses"] == f"github/codeql-action/init@{CODEQL_V4_37_6_SHA}"

    analyze = _single_action_step(workflow, "github/codeql-action/analyze")
    assert analyze["uses"] == f"github/codeql-action/analyze@{CODEQL_V4_37_6_SHA}"
    assert analyze.get("if") == "${{ false }}"


def test_job_permissions_are_parsed_for_effective_policy(tmp_path: Path) -> None:
    """Job-level overrides must be visible to the read-only permission gate."""
    workflow_path = tmp_path / "workflow.yml"
    workflow_path.write_text(
        """permissions:
  contents: read
jobs:
  unsafe:
    permissions:
      contents: write
    steps:
      - run: echo unsafe
""",
        encoding="utf-8",
    )

    workflow = _workflow_structure(workflow_path)

    assert workflow["jobs"]["unsafe"]["permissions"] == {"contents": "write"}
    effective_permissions = (
        workflow["permissions"] | workflow["jobs"]["unsafe"]["permissions"]
    )
    assert effective_permissions != {"contents": "read"}

