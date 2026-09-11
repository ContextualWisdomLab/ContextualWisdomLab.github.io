"""Regression tests for labelled section landmarks on the homepage."""

from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"


class _LandmarkParser(HTMLParser):
    """Collect <section> start tags and every element id in document order."""

    def __init__(self) -> None:
        super().__init__()
        self.sections: list[dict[str, str | None]] = []
        self.ids: set[str] = set()

    def handle_starttag(self, tag, attrs) -> None:
        attributes = dict(attrs)
        element_id = attributes.get("id")
        if element_id:
            self.ids.add(element_id)
        if tag == "section":
            self.sections.append(attributes)


def _parse_index() -> _LandmarkParser:
    parser = _LandmarkParser()
    parser.feed(INDEX.read_text(encoding="utf-8"))
    assert parser.sections, "homepage must contain at least one section"
    return parser


def test_labelled_sections_reference_an_existing_heading() -> None:
    """Each aria-labelledby target must resolve to a real id in the document."""
    parser = _parse_index()

    labelled = [s for s in parser.sections if s.get("aria-labelledby")]
    assert labelled, "homepage sections must expose accessible names"

    for section in labelled:
        target = section["aria-labelledby"]
        assert target in parser.ids, (
            f"section #{section.get('id')} references missing id {target!r}"
        )


def test_identified_sections_are_all_labelled() -> None:
    """Every identifiable section landmark must carry an accessible name."""
    parser = _parse_index()

    for section in parser.sections:
        if section.get("id"):
            assert section.get("aria-labelledby"), (
                f"section #{section['id']} must reference a heading via aria-labelledby"
            )
