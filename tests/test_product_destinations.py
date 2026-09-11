"""Regression tests for homepage product-destination correctness."""

from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
I18N = ROOT / "i18n.js"

CANONICAL_PREFIX = "https://github.com/ContextualWisdomLab/"

PROJECT_SLUGS = {
    "naruon",
    "pg-erd-cloud",
    "bandscope",
    "codec-carver",
    "newsdom-api",
    "scopeweave",
    "VibeSec",
    "fast-mlsirm",
    "wardnet",
    "Orgmetra",
    "TEPP",
    "psychometrics-commons",
    "contextual-orchestrator",
}

FORK_SLUGS = {"argos", "vooster"}


class _SectionParser(HTMLParser):
    """Track which section each external link belongs to."""

    def __init__(self) -> None:
        super().__init__()
        self.section: str | None = None
        self.links: list[tuple[str | None, dict[str, str | None]]] = []

    def handle_starttag(self, tag, attrs) -> None:
        attributes = dict(attrs)
        if tag == "section":
            self.section = attributes.get("id")
        elif tag == "a":
            self.links.append((self.section, attributes))

    def handle_endtag(self, tag) -> None:
        if tag == "section":
            self.section = None


def _parse() -> _SectionParser:
    parser = _SectionParser()
    parser.feed(INDEX.read_text(encoding="utf-8"))
    return parser


def _hrefs(parser: _SectionParser, section_id: str) -> set[str]:
    return {
        attrs["href"] or ""
        for sid, attrs in parser.links
        if sid == section_id and attrs.get("href")
    }


def test_projects_section_links_every_owned_repository() -> None:
    """Every project card points at the repository the lab owns today."""
    hrefs = _hrefs(_parse(), "projects")

    for slug in PROJECT_SLUGS:
        assert f"{CANONICAL_PREFIX}{slug}" in hrefs, (
            f"Projects section must link {CANONICAL_PREFIX}{slug}"
        )


def test_stale_renamed_repository_is_not_linked() -> None:
    """The renamed waf-ids-ai-soc URL must be gone."""
    hrefs = _hrefs(_parse(), "projects")
    assert f"{CANONICAL_PREFIX}waf-ids-ai-soc" not in hrefs, (
        "waf-ids-ai-soc must not be linked; it redirects to wardnet"
    )


def test_forks_section_links_only_owned_forks() -> None:
    """Owned forks link out; unowned forks are introduced without a dead link."""
    hrefs = _hrefs(_parse(), "forks")

    for slug in FORK_SLUGS:
        assert f"{CANONICAL_PREFIX}{slug}" in hrefs, (
            f"Forks section must link {CANONICAL_PREFIX}{slug}"
        )
    assert f"{CANONICAL_PREFIX}vooster-v2-mvp" not in hrefs, (
        "vooster-v2-mvp has no organization-owned repository and must not be linked"
    )


def test_naruon_section_offers_a_repository_action() -> None:
    """The Naruon section links to its repository, not just prose."""
    hrefs = _hrefs(_parse(), "naruon")
    assert f"{CANONICAL_PREFIX}naruon" in hrefs, (
        "Naruon section must offer an action to open its repository"
    )


def test_new_project_cards_have_bilingual_copy() -> None:
    """Every added project card has KO and EN copy in the dictionary."""
    i18n_js = I18N.read_text(encoding="utf-8")
    for key in (
        "projects.wardnetTitle",
        "projects.orgmetraTitle",
        "projects.teppTitle",
        "projects.psychometricsCommonsTitle",
        "projects.orchestratorTitle",
        "naruon.cta",
    ):
        assert i18n_js.count(f'"{key}":') == 2, (
            f"{key} must be defined once per locale"
        )


def test_new_project_links_carry_the_new_window_warning() -> None:
    """Dynamically added links follow the shared new-window accessibility contract."""
    parser = _parse()
    for section_id in ("projects", "forks", "naruon"):
        for sid, attrs in parser.links:
            if sid != section_id or attrs.get("target") != "_blank":
                continue
            assert attrs.get("aria-describedby") == "new-window-desc", (
                f"link {attrs.get('href')} must reference the shared warning"
            )
            assert attrs.get("rel") and "noopener" in attrs["rel"].split(), (
                f"link {attrs.get('href')} must keep opener isolation"
            )
