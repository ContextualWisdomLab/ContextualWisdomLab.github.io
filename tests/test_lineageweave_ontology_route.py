"""Contract checks for the lowercase LineageWeave ontology route."""

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ONTOLOGY = ROOT / "lineageweave" / "ontology"
CANONICAL = "https://contextualwisdomlab.github.io/lineageweave/ontology"
SOURCE_COMMIT = "6eff57051687a69ac503be026eec724d18e81b8c"


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
    assert "Lookup code</dt><dd><span>None" not in page
    assert 'href="http://' not in page
    assert 'header a { color: #fff; }' in page
    assert '<a href="../../">LineageWeave</a>' in page


def test_project_mentions_reify_their_post_and_project() -> None:
    """Published N-Triples retain the source/predicate/object restrictions."""
    triples = (ONTOLOGY / "ontology.nt").read_text(encoding="utf-8")
    restrictions = {
        "subject": (
            "http://www.w3.org/1999/02/22-rdf-syntax-ns#subject",
            f"{CANONICAL}#Post",
            "http://www.w3.org/2002/07/owl#allValuesFrom",
        ),
        "predicate": (
            "http://www.w3.org/1999/02/22-rdf-syntax-ns#predicate",
            f"{CANONICAL}#mentionsProject",
            "http://www.w3.org/2002/07/owl#hasValue",
        ),
        "object": (
            "http://www.w3.org/1999/02/22-rdf-syntax-ns#object",
            f"{CANONICAL}#Project",
            "http://www.w3.org/2002/07/owl#allValuesFrom",
        ),
    }
    for property_iri, value_iri, value_predicate in restrictions.values():
        node_match = re.search(
            rf"^(?P<node>_:[^ ]+) <http://www.w3.org/2002/07/owl#onProperty> <{re.escape(property_iri)}> \.$",
            triples,
            re.MULTILINE,
        )
        assert node_match
        assert (
            f"{node_match.group('node')} <{value_predicate}> <{value_iri}> ."
            in triples
        )


def test_compatibility_artifact_only_maps_validated_representative_classes() -> None:
    """The copied compatibility graph does not invent broad namespace equivalence."""
    compatibility = (ONTOLOGY / "namespace-compatibility.ttl").read_text(encoding="utf-8")

    assert "owl:equivalentClass" in compatibility
    assert "canonical:Post owl:equivalentClass legacy:Post" in compatibility
    assert "owl:equivalentProperty" not in compatibility
    assert "owl:sameAs" not in compatibility


def test_support_profile_uses_the_canonical_namespace() -> None:
    """The public support profile does not mint deprecated product terms."""
    profile = (ONTOLOGY / "prov-o-support-profile.ttl").read_text(encoding="utf-8")

    assert f"@prefix : <{CANONICAL}#> ." in profile
    assert "https://contextualwisdomlab.github.io/LineageWeave/ontology#" not in profile
