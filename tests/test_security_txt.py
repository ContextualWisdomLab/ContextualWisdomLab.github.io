"""Regression tests for the RFC 9116 vulnerability disclosure file."""

import re
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SECURITY_TXT = ROOT / ".well-known" / "security.txt"
SECURITY_MD = ROOT / "SECURITY.md"

ORIGIN = "https://contextualwisdomlab.github.io"


def _fields() -> dict[str, list[str]]:
    parsed: dict[str, list[str]] = {}
    for raw in SECURITY_TXT.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        name, _, value = line.partition(":")
        parsed.setdefault(name.strip().lower(), []).append(value.strip())
    return parsed


def _one(fields: dict[str, list[str]], name: str) -> str:
    values = fields.get(name)
    assert values, f"security.txt must declare a {name} field"
    return values[0]


def test_security_txt_served_from_well_known() -> None:
    """GitHub Pages serves dotfiles literally, so .nojekyll must exist."""
    assert SECURITY_TXT.is_file(), ".well-known/security.txt must exist"
    assert (ROOT / ".nojekyll").is_file(), (
        ".nojekyll is required for GitHub Pages to serve .well-known/"
    )


def test_security_txt_has_required_fields() -> None:
    """RFC 9116 requires Contact and Expires."""
    fields = _fields()
    assert "contact" in fields and "expires" in fields, (
        "RFC 9116 requires both Contact and Expires"
    )


def test_expires_is_valid_and_in_the_future() -> None:
    """An expired security.txt is treated as absent by tooling."""
    expires = _one(_fields(), "expires").replace("Z", "+00:00")
    parsed = datetime.fromisoformat(expires)
    assert parsed.tzinfo is not None, "Expires must carry a timezone (RFC 3339)"
    assert parsed > datetime.now(timezone.utc), "security.txt has expired"


def test_contact_matches_the_security_policy_intake() -> None:
    """The published contact must be the same intake SECURITY.md describes."""
    contact = _one(_fields(), "contact")
    policy = SECURITY_MD.read_text(encoding="utf-8")
    assert contact.startswith("https://"), "Contact must be an absolute URL"
    assert contact in policy, (
        "security.txt Contact must match the reporting URL in SECURITY.md"
    )


def test_canonical_and_policy_point_to_live_locations() -> None:
    """Canonical must be the deployed URL and Policy must name a real file."""
    fields = _fields()
    canonical = _one(fields, "canonical")
    assert canonical == f"{ORIGIN}/.well-known/security.txt", (
        "Canonical must be the absolute URL this file is served from"
    )
    policy = _one(fields, "policy")
    assert policy.startswith("https://"), "Policy must be an absolute URL"
    assert re.search(r"SECURITY\.md$", policy) and SECURITY_MD.is_file(), (
        "Policy must point at the repository SECURITY.md"
    )
