"""Regression tests for crawler metadata (robots.txt, sitemap.xml)."""

import re
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
ROBOTS = ROOT / "robots.txt"
SITEMAP = ROOT / "sitemap.xml"

ORIGIN = "https://contextualwisdomlab.github.io"
SITEMAP_NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"


def _robots() -> str:
    return ROBOTS.read_text(encoding="utf-8")


def _urls() -> list[dict[str, str]]:
    root = ET.fromstring(SITEMAP.read_text(encoding="utf-8"))
    return [
        {child.tag.replace(SITEMAP_NS, ""): (child.text or "").strip()
         for child in url}
        for url in root.findall(f"{SITEMAP_NS}url")
    ]


def test_robots_allows_crawling_and_points_to_sitemap() -> None:
    """robots.txt must permit crawling and advertise the canonical sitemap."""
    assert ROBOTS.is_file(), "robots.txt must exist at the site root"

    text = _robots()
    assert re.search(r"(?m)^User-agent:\s*\*$", text) is not None
    assert re.search(r"(?m)^Allow:\s*/$", text) is not None
    assert re.search(r"(?m)^Disallow:\s*$", text) is None
    assert (
        f"Sitemap: {ORIGIN}/sitemap.xml" in _robots()
    ), "robots.txt must advertise the absolute sitemap URL on the canonical origin"


def test_sitemap_is_well_formed_and_canonical() -> None:
    """sitemap.xml must parse and list only absolute canonical-origin URLs."""
    assert SITEMAP.is_file(), "sitemap.xml must exist at the site root"

    urls = _urls()
    assert urls, "sitemap.xml must contain at least one <url> entry"

    locs = [entry["loc"] for entry in urls]
    assert len(locs) == len(set(locs)), "sitemap.xml must not repeat a <loc>"

    for loc in locs:
        parsed = urlparse(loc)
        assert parsed.scheme == "https" and parsed.netloc, f"{loc} must be absolute"
        assert loc.startswith(ORIGIN + "/") or loc == ORIGIN, (
            f"{loc} must live on the canonical origin {ORIGIN}"
        )


def test_sitemap_entries_resolve_to_real_routes() -> None:
    """Every sitemap URL must map to a page shipped in the repository."""
    routes = {"/": ROOT / "index.html", "/components/": ROOT / "components" / "index.html"}
    dirs = {"/": ROOT, "/components/": ROOT / "components"}

    for entry in _urls():
        path = urlparse(entry["loc"]).path
        assert path in routes, f"{entry['loc']} is not a known site route"
        assert routes[path].is_file(), f"{path} has no index.html to serve"
        lastmod = entry.get("lastmod", "")
        assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", lastmod), (
            f"{entry['loc']} needs an ISO lastmod date, got {lastmod!r}"
        )
