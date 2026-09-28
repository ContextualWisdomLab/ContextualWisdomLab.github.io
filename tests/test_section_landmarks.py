"""Regression tests for labelled section landmarks on the homepage."""

from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"


class _LandmarkParser(HTMLParser):
    """Collect section attributes and heading ids in document order."""

    def __init__(self) -> None:
        super().__init__()
        self.sections: list[dict[str, str | None]] = []
        self.heading_ids: list[str] = []

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        """Record section attributes and labelled-heading identities."""
        attributes = dict(attrs)
        if tag == "section":
            self.sections.append(attributes)
        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            heading_id = attributes.get("id")
            if heading_id:
                self.heading_ids.append(heading_id)


def _parse_index() -> _LandmarkParser:
    """Parse the homepage with the standard-library HTML parser."""
    parser = _LandmarkParser()
    parser.feed(INDEX.read_text(encoding="utf-8"))
    assert parser.sections, "homepage must contain at least one section"
    return parser


def test_labelled_sections_reference_one_existing_heading() -> None:
    """Each aria-labelledby target must resolve to exactly one heading id."""
    parser = _parse_index()

    for section in parser.sections:
        target = section.get("aria-labelledby")
        assert target, (
            f"section #{section.get('id')} must reference a heading via aria-labelledby"
        )
        assert parser.heading_ids.count(target) == 1, (
            f"section #{section.get('id')} must reference one existing heading; "
            f"found {parser.heading_ids.count(target)} for {target!r}"
        )


def test_all_sections_are_labelled_including_anonymous_sections() -> None:
    """Prevent an id-less section from bypassing the landmark contract."""
    parser = _parse_index()

    assert all(section.get("aria-labelledby") for section in parser.sections)
