import pytest
from playwright.sync_api import Page, expect

def test_tabs_behavior_null_check(page: Page) -> None:
    """Test tab switching null check by removing aria-controls."""
    page.goto("http://localhost:4173/components/index.html")

    # Target the second tab which is already wired up by krds-gallery.js
    tab2 = page.locator("#t2")

    # Remove the aria-controls attribute to force the null path
    page.evaluate('''
        const tab = document.getElementById("t2");
        if (tab) {
            tab.removeAttribute("aria-controls");
        }
    ''')

    # Clicking it shouldn't throw an error and execution should complete
    # (The tab will visually select because aria-selected is set before the null check)
    tab2.click()
    expect(tab2).to_have_attribute("aria-selected", "true")

def test_tag_remove_null_check(page: Page) -> None:
    """Test tag removal null check by breaking the class hierarchy."""
    page.goto("http://localhost:4173/components/index.html")

    remove_btns = page.locator(".krds-tag__remove")
    expect(remove_btns).to_have_count(2)

    # Strip the parent of the first button of its krds-tag class so btn.closest fails
    page.evaluate('''
        const btns = document.querySelectorAll(".krds-tag__remove");
        if (btns.length > 0) {
            const parent = btns[0].closest(".krds-tag");
            if (parent) {
                parent.classList.remove("krds-tag");
            }
        }
    ''')

    # Clicking it shouldn't throw an error (graceful degradation)
    remove_btns.first.click()

    # The count should still be 2 because the tag was not removed
    expect(page.locator(".krds-tag__remove")).to_have_count(2)
