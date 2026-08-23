"""Contract checks for the lowercase LineageWeave ontology route."""

import hashlib
import json
import mimetypes
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ONTOLOGY = ROOT / "lineageweave" / "ontology"
CANONICAL = "https://contextualwisdomlab.github.io/lineageweave/ontology"
SOURCE_COMMIT = "c8a4be8fc2417f05d53fb68d32d9e59c3d443e25"


def test_route_publishes_canonical_generated_artifacts_with_provenance() -> None:
    """The owned route retains its source identity, digest, and format links."""
    manifest = json.loads((ONTOLOGY / "manifest.json").read_text(encoding="utf-8"))
    published_source_copy = ONTOLOGY / "ontology.ttl"
    page = (ONTOLOGY / "index.html").read_text(encoding="utf-8")

    assert manifest["documentation_url"] == CANONICAL
    assert manifest["source_commit"] == SOURCE_COMMIT
    assert manifest["source_sha256"] == hashlib.sha256(
        published_source_copy.read_bytes()
    ).hexdigest()
    assert set(manifest["generated_artifacts"]) <= {path.name for path in ONTOLOGY.iterdir()}
    assert f'<link rel="canonical" href="{CANONICAL}">' in page
    assert 'id="Post"' in page and f"{CANONICAL}#Post" in page
    for name, media_type in (
        ("ontology.ttl", "text/turtle"),
        ("ontology.jsonld", "application/ld+json"),
        ("ontology.nt", "application/n-triples"),
    ):
        assert f'href="{name}" type="{media_type}"' in page
    assert mimetypes.guess_type("ontology.ttl")[0] == "text/turtle"
    assert mimetypes.guess_type("ontology.nt")[0] == "application/n-triples"


def test_compatibility_artifact_only_maps_validated_representative_classes() -> None:
    """The copied compatibility graph does not invent broad namespace equivalence."""
    compatibility = (ONTOLOGY / "namespace-compatibility.ttl").read_text(encoding="utf-8")

    assert "owl:equivalentClass" in compatibility
    assert "canonical:Post owl:equivalentClass legacy:Post" in compatibility
    assert "owl:equivalentProperty" not in compatibility
    assert "owl:sameAs" not in compatibility
