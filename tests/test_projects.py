"""
test_projects.py — Tests for the Custom Project Highlights section.

Covers:
  - Correct number of project cards (3)
  - Countdown Timer card content, tags, and buttons
  - 'Launch Web App Version' button is visible, points to /countdown,
    opens in the same tab, and the countdown page loads correctly
  - Flask /countdown route returns HTTP 200
  - Coming-soon placeholder cards (Spring 2026 & Summer 2026) are present
  - Both coming-soon labels are visible
"""

import pytest
from playwright.sync_api import expect


BASE_URL = "http://127.0.0.1:5000"


# ── Project section ───────────────────────────────────────────────────────────

class TestProjectsSection:

    def test_projects_section_exists(self, home_page):
        """Projects section should be in the DOM."""
        section = home_page.locator("#projects")
        assert section.count() == 1

    def test_projects_heading(self, home_page):
        """Projects section heading should say 'Custom Project Highlights'."""
        heading = home_page.locator("#projects h2")
        assert "Custom Project Highlights" in heading.inner_text()

    def test_project_cards_count(self, home_page):
        """There should be exactly 3 project cards."""
        cards = home_page.locator(".project-card")
        assert cards.count() == 3


# ── Countdown Timer card ──────────────────────────────────────────────────────

class TestCountdownTimerCard:

    def test_countdown_card_title(self, home_page):
        """First project card should be titled Countdown Timer Application."""
        first_card = home_page.locator(".project-card").first
        heading = first_card.locator("h3")
        assert "Countdown Timer" in heading.inner_text()

    def test_countdown_card_description(self, home_page):
        """Countdown card description should mention Python and Tkinter."""
        first_card = home_page.locator(".project-card").first
        text = first_card.inner_text()
        assert "Python" in text
        assert "Tkinter" in text

    def test_countdown_card_tags(self, home_page):
        """Countdown card should display tech tags."""
        first_card = home_page.locator(".project-card").first
        tags = first_card.locator(".project-tags span")
        assert tags.count() >= 3

    def test_launch_web_app_button_visible(self, home_page):
        """'Launch Web App Version' button should be visible on the card."""
        btn = home_page.locator(".project-links a", has_text="Launch Web App Version")
        assert btn.is_visible()

    def test_launch_web_app_href(self, home_page):
        """'Launch Web App Version' button href should point to the Flask /countdown route."""
        btn = home_page.locator(".project-links a", has_text="Launch Web App Version")
        assert btn.get_attribute("href") == "/countdown"

    def test_launch_web_app_opens_same_tab(self, home_page):
        """'Launch Web App Version' button should open in the same tab (no target=_blank)."""
        btn = home_page.locator(".project-links a", has_text="Launch Web App Version")
        target = btn.get_attribute("target")
        assert target != "_blank", "Button should not open in a new tab"

    def test_launch_web_app_button_opens_countdown_page(self, home_page):
        """Clicking 'Launch Web App Version' should navigate to the Countdown Timer in the same tab.

        Clicks the link, waits for navigation to complete, then verifies the correct
        page title and the main timer element are present.
        """
        btn = home_page.locator(".project-links a", has_text="Launch Web App Version")

        # Click and wait for same-tab navigation to complete
        with home_page.expect_navigation():
            btn.click()

        home_page.wait_for_load_state("load")

        # Verify the correct page loaded
        assert "Countdown Timer" in home_page.title(), (
            f"Expected 'Countdown Timer' in page title, got: '{home_page.title()}'"
        )
        assert home_page.locator("#timerDisplay").is_visible(), (
            "Timer display (#timerDisplay) not visible after navigation"
        )
        assert home_page.url.rstrip("/").endswith("/countdown"), (
            f"URL should end with /countdown, got: '{home_page.url}'"
        )

    def test_countdown_web_app_route_responds(self, page):
        """GET /countdown should return HTTP 200."""
        response = page.goto(f"{BASE_URL}/countdown")
        assert response.status == 200


# ── Coming-soon placeholder cards ────────────────────────────────────────────

class TestComingSoonCards:

    def test_spring_2026_card_exists(self, home_page):
        """A 'Spring 2026' placeholder card should be present.

        Uses text_content() (raw DOM text) rather than inner_text() so the
        check is not affected by the scroll-reveal animation which sets
        opacity:0 on cards that are below the fold in headless mode.
        """
        cards = home_page.locator(".project-card--coming-soon")
        texts = [cards.nth(i).text_content() for i in range(cards.count())]
        assert any("Spring 2026" in t for t in texts), "Spring 2026 card not found"

    def test_summer_2026_card_exists(self, home_page):
        """A 'Summer 2026' placeholder card should be present."""
        cards = home_page.locator(".project-card--coming-soon")
        texts = [cards.nth(i).text_content() for i in range(cards.count())]
        assert any("Summer 2026" in t for t in texts), "Summer 2026 card not found"

    def test_coming_soon_cards_count(self, home_page):
        """There should be exactly 2 coming-soon cards."""
        coming_soon = home_page.locator(".project-card--coming-soon")
        assert coming_soon.count() == 2

    def test_coming_soon_labels_visible(self, home_page):
        """The styled coming-soon labels should be visible."""
        labels = home_page.locator(".coming-soon-label")
        assert labels.count() == 2
        for i in range(labels.count()):
            assert labels.nth(i).is_visible()
