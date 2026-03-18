"""
test_nav_links.py — Tests for the global navigation anchor links.

Covers:
  - All 6 nav links are present in the DOM
  - Each nav link has the correct href anchor value
  - Each nav link displays the correct label text
  - Each nav link is visible on load (desktop viewport)
  - Clicking each nav link smooth-scrolls to the correct section
    (main.js uses e.preventDefault() + window.scrollTo(), so the URL hash
    is intentionally not updated — scroll position is asserted instead)
  - Clicking each nav link brings the target section into the viewport
"""

import pytest


# ── Expected nav link data ────────────────────────────────────────────────────

NAV_LINKS = [
    ("About",          "#about"),
    ("Experience",     "#experience"),
    ("Projects",       "#projects"),
    ("Skills",         "#skills"),
    ("Certifications", "#certifications"),
    ("Contact",        "#contact"),
]


# ── Presence & attributes ─────────────────────────────────────────────────────

class TestNavLinkPresence:
    """Verify every nav anchor exists in the DOM with the right attributes."""

    def test_nav_link_count(self, home_page):
        """Global nav should contain exactly 6 anchor links."""
        links = home_page.locator(".nav-links a")
        assert links.count() == 6, (
            f"Expected 6 nav links, found {links.count()}"
        )

    @pytest.mark.parametrize("label, href", NAV_LINKS)
    def test_nav_link_href(self, home_page, label, href):
        """Each nav link should have the correct href anchor value."""
        link = home_page.locator(f".nav-links a[href='{href}']")
        assert link.count() == 1, (
            f"Nav link with href='{href}' not found in the DOM"
        )

    @pytest.mark.parametrize("label, href", NAV_LINKS)
    def test_nav_link_text(self, home_page, label, href):
        """Each nav link should display the expected label text."""
        link = home_page.locator(f".nav-links a[href='{href}']")
        actual_text = link.inner_text().strip()
        assert actual_text == label, (
            f"Expected link text '{label}', got '{actual_text}'"
        )


# ── Visibility ────────────────────────────────────────────────────────────────

class TestNavLinkVisibility:
    """Verify every nav anchor is visible on a standard desktop viewport."""

    @pytest.mark.parametrize("label, href", NAV_LINKS)
    def test_nav_link_is_visible(self, home_page, label, href):
        """Nav link should be visible without any user interaction."""
        link = home_page.locator(f".nav-links a[href='{href}']")
        assert link.is_visible(), (
            f"Nav link '{label}' (href='{href}') is not visible"
        )


# ── Click behaviour — hash & scroll ──────────────────────────────────────────

class TestNavLinkNavigation:
    """Verify clicking each nav link scrolls to the correct in-page section.

    Note on URL hash: main.js attaches a smooth-scroll listener to every
    anchor whose href starts with '#'. It calls e.preventDefault() and uses
    window.scrollTo() with a 70 px sticky-header offset, which intentionally
    bypasses native anchor navigation and leaves the URL hash unchanged.
    The tests below verify scroll position and viewport visibility instead.
    """

    @pytest.mark.parametrize("label, href", NAV_LINKS)
    def test_click_smooth_scrolls_to_section(self, home_page, label, href):
        """Clicking a nav link should smooth-scroll the page to the target section.

        main.js uses e.preventDefault() + window.scrollTo() so the URL hash is
        never updated. We verify that window.scrollY lands within 100 px of
        (section.offsetTop - 70), matching the offset used in main.js.

        Instead of a fixed sleep we poll window.scrollY every 80 ms and wait
        until it stops changing — this handles any scroll distance reliably.
        """
        section_id = href.lstrip("#")  # e.g. "#about" -> "about"

        link = home_page.locator(f".nav-links a[href='{href}']")
        link.click()

        # Wait until window.scrollY hasn't changed between two consecutive 80 ms
        # samples, meaning the smooth-scroll animation has fully settled.
        home_page.wait_for_function(
            """() => new Promise(resolve => {
                let prev = window.scrollY;
                const id = setInterval(() => {
                    if (window.scrollY === prev) { clearInterval(id); resolve(true); }
                    prev = window.scrollY;
                }, 80);
            })""",
            timeout=3000,
        )

        scroll_y = home_page.evaluate("window.scrollY")
        section_top = home_page.evaluate(
            f"document.getElementById('{section_id}').offsetTop"
        )

        nav_offset = 70  # sticky header clearance used in main.js
        expected_scroll = max(0, section_top - nav_offset)
        tolerance = 100  # px — accounts for sub-pixel rounding & layout reflow

        assert abs(scroll_y - expected_scroll) <= tolerance, (
            f"After clicking '{label}', expected window.scrollY ≈ {expected_scroll}px "
            f"(#{section_id}.offsetTop {section_top}px − {nav_offset}px header offset), "
            f"but got scrollY = {scroll_y}px (delta = {abs(scroll_y - expected_scroll)}px)"
        )

    @pytest.mark.parametrize("label, href", NAV_LINKS)
    def test_click_brings_section_into_viewport(self, home_page, label, href):
        """Clicking a nav link should scroll the target section into the viewport."""
        section_id = href.lstrip("#")  # e.g. "#about" -> "about"

        link = home_page.locator(f".nav-links a[href='{href}']")
        link.click()

        # Wait for any smooth-scroll animation to finish
        home_page.wait_for_timeout(600)

        section = home_page.locator(f"#{section_id}")
        assert section.count() == 1, (
            f"Target section '#{section_id}' not found in DOM"
        )

        # is_visible() confirms the element is in the layout and not hidden
        assert section.is_visible(), (
            f"Section '#{section_id}' is not visible after clicking '{label}' nav link"
        )

        # Verify the section top is at or near the visible area of the page
        bounding_box = section.bounding_box()
        assert bounding_box is not None, (
            f"Could not get bounding box for section '#{section_id}'"
        )

        viewport_height = home_page.viewport_size["height"]
        # The section's top edge should be within one viewport height of position 0
        # (i.e. it has been scrolled near the top of the screen)
        assert bounding_box["y"] < viewport_height, (
            f"Section '#{section_id}' top ({bounding_box['y']}px) is below the "
            f"viewport height ({viewport_height}px) — page may not have scrolled"
        )
