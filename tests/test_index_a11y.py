import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"

def test_section_landmarks_have_labels() -> None:
    """Ensure all sections with IDs have aria-labelledby to act as distinct region landmarks."""
    html = INDEX.read_text(encoding="utf-8")

    # Find all <section> tags
    sections = re.findall(r'<section\s+([^>]+)>', html, flags=re.IGNORECASE)

    for sec_attrs in sections:
        # Check if the section has an id
        id_match = re.search(r'id="([^"]+)"', sec_attrs, flags=re.IGNORECASE)
        if id_match:
            sec_id = id_match.group(1)
            # Ensure it has an aria-labelledby attribute
            assert re.search(rf'aria-labelledby="{sec_id}-title"', sec_attrs, flags=re.IGNORECASE) is not None, \
                f"Section with id '{sec_id}' is missing aria-labelledby='{sec_id}-title'"

            # Ensure there is an element with that ID in the HTML
            assert re.search(rf'id="{sec_id}-title"', html, flags=re.IGNORECASE) is not None, \
                f"Missing element with id='{sec_id}-title' referenced by section '{sec_id}'"
