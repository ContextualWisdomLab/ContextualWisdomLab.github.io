"""Regression tests for the custom 404 page (404.html)."""

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "404.html"
INDEX = ROOT / "index.html"


def _page() -> str:
    """Read the candidate 404 document as UTF-8 source."""
    return PAGE.read_text(encoding="utf-8")


def _index() -> str:
    """Read the homepage source used to validate 404 navigation targets."""
    return INDEX.read_text(encoding="utf-8")


def test_404_page_exists_and_is_self_contained() -> None:
    """GitHub Pages serves 404.html, so it must exist and load only local assets."""
    assert PAGE.is_file(), "404.html must exist so GitHub Pages serves a branded page"
    html = _page()

    assert 'href="styles.css"' in html
    assert 'href="404.css"' in html
    assert (ROOT / "404.css").is_file(), "404.css referenced by 404.html must exist"


def test_404_page_stays_strict_csp_safe() -> None:
    """The 404 page must not weaken CSP with inline script, style, or handlers."""
    html = _page()

    assert re.search(r"<style(?:\s|>)", html, flags=re.IGNORECASE) is None
    assert re.search(r"\sstyle\s*=", html, flags=re.IGNORECASE) is None
    assert re.search(
        r"<script(?![^>]*\bsrc=)[^>]*>", html, flags=re.IGNORECASE
    ) is None
    assert re.search(r"\son[a-z]+\s*=", html, flags=re.IGNORECASE) is None
    assert "default-src 'none'" in html
    assert "script-src 'none'" in html
    assert "connect-src 'none'" in html
    assert re.search(r"<script\b", html, flags=re.IGNORECASE) is None


def test_404_page_is_not_indexed_and_offers_a_way_back() -> None:
    """A missing page must not be indexed and must link the visitor home."""
    html = _page()

    assert re.search(r'<meta\s+name="robots"\s+content="noindex"', html) is not None
    assert 'href="/"' in html, "404 page must link back to the site root"


def test_404_skip_link_targets_local_main() -> None:
    """The skip link must move focus within the 404 page, not navigate home."""
    html = _page()
    assert '<a href="#top" class="skip-link">' in html
    assert '<main id="top" tabindex="-1"' in html


def test_404_internal_fragments_exist_on_the_homepage() -> None:
    """Every in-page fragment the 404 nav points to must exist on index.html."""
    index = _index()
    fragments = {
        fragment
        for fragment in re.findall(r'href="/#([a-z0-9-]+)"', _page())
    }
    assert fragments, "404 page should offer in-page navigation anchors"

    for fragment in sorted(fragments):
        assert f'id="{fragment}"' in index, (
            f"404.html links to #/… but index.html has no id={fragment!r}"
        )


def test_404_assets_referenced_exist_on_disk() -> None:
    """Local image/icon assets referenced by the 404 page must be present."""
    for asset in re.findall(r'(?:href|src)="(assets/[^"#?]+)"', _page()):
        assert (ROOT / asset).is_file(), f"404.html references missing asset {asset}"


def test_404_page_external_links_accessible() -> None:
    """External links on the 404 page must be accessible."""
    html = _page()

    # Check visually hidden description span
    assert '<span id="new-window-desc" class="visually-hidden">새 창에서 열림</span>' in html, (
        "404 page must contain the visually hidden description for new window links"
    )

    # Verify all external links reference it
    from html.parser import HTMLParser

    class _LinkParser(HTMLParser):
        def __init__(self) -> None:
            super().__init__()
            self.links: list[dict[str, str | None]] = []

        def handle_starttag(self, tag, attrs) -> None:
            if tag == "a":
                self.links.append(dict(attrs))

    parser = _LinkParser()
    parser.feed(html)

    external_links = [a for a in parser.links if a.get("target") == "_blank"]
    assert len(external_links) > 0, "404 page should have external links"

    for anchor in external_links:
        assert anchor.get("aria-describedby") == "new-window-desc", (
            f"External link {anchor.get('href')} must reference #new-window-desc"
        )
        assert anchor.get("title") == "새 창에서 열림", (
            f"External link {anchor.get('href')} must have the correct title"
        )
        rel_tokens = {token.lower() for token in (anchor.get("rel") or "").split()}
        assert "noopener" in rel_tokens, (
            f"External link {anchor.get('href')} must keep opener isolation"
        )
        assert "noreferrer" in rel_tokens, (
            f"External link {anchor.get('href')} must keep the product referrer policy"
        )
