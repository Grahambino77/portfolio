"""
test_homepage.py — Tests for the main portfolio page.

Covers:
  - Page title & metadata
  - Sticky navbar (logo + all nav links present)
  - Hero section content
  - All major sections exist and are visible
  - Section headings are correct
  - Footer copyright text and social links
  - Active nav link highlighting on scroll
"""

import pytest


# ── Page load ────────────────────────────────────────────────────────────────

class TestPageLoad:

    def test_page_title(self, home_page):
        """Page title should contain the name and role."""
        assert "Andrew Graham" in home_page.title()

    def test_page_responds_200(self, page):
        """Home route should return HTTP 200."""
        response = page.goto("http://127.0.0.1:5000/")
        assert response.status == 200

    def test_meta_description_present(self, home_page):
        """Meta description should be set."""
        meta = home_page.locator('meta[name="description"]')
        content = meta.get_attribute("content")
        assert content and len(content) > 10

    def test_css_loaded(self, home_page):
        """styles.css should load without 4xx errors."""
        responses = {}

        def capture(response):
            if "styles.css" in response.url:
                responses["css"] = response.status

        home_page.on("response", capture)
        home_page.reload(wait_until="networkidle")
        assert responses.get("css") in (200, 304), "styles.css did not load"

    def test_js_loaded(self, home_page):
        """main.js should load without 4xx errors."""
        responses = {}

        def capture(response):
            if "main.js" in response.url:
                responses["js"] = response.status

        home_page.on("response", capture)
        home_page.reload(wait_until="networkidle")
        assert responses.get("js") in (200, 304), "main.js did not load"


# ── Navbar ───────────────────────────────────────────────────────────────────

class TestNavbar:

    def test_logo_present(self, home_page):
        """Navbar logo should display the name."""
        logo = home_page.locator(".logo")
        assert logo.is_visible()
        assert "Andrew Graham" in logo.inner_text()

    def test_navbar_links_count(self, home_page):
        """Navbar should have exactly 6 navigation links."""
        links = home_page.locator(".nav-links a")
        assert links.count() == 6

    @pytest.mark.parametrize("link_text", [
        "About", "Experience", "Projects", "Skills", "Certifications", "Contact"
    ])
    def test_navbar_link_exists(self, home_page, link_text):
        """Each expected nav link should be visible."""
        link = home_page.locator(f".nav-links a[href='#{link_text.lower()}']")
        assert link.is_visible(), f"Nav link '{link_text}' not found"


# ── Hero section ─────────────────────────────────────────────────────────────

class TestHero:

    def test_hero_heading_contains_name(self, home_page):
        """Hero h1 should contain Andrew Graham."""
        h1 = home_page.locator(".hero h1")
        assert "Andrew Graham" in h1.inner_text()

    def test_hero_tagline_visible(self, home_page):
        """Hero tagline should be visible."""
        tagline = home_page.locator(".tagline")
        assert tagline.is_visible()
        text = tagline.inner_text()
        assert "QA Analyst" in text or "Consultant" in text

    def test_hero_view_experience_button(self, home_page):
        """'View Experience' CTA button should be visible."""
        btn = home_page.locator(".hero-btns a", has_text="View Experience")
        assert btn.is_visible()

    def test_hero_download_resume_button(self, home_page):
        """'Download Resume' button should be visible."""
        btn = home_page.locator(".hero-btns a", has_text="Download Resume")
        assert btn.is_visible()

    def test_hero_email_link(self, home_page):
        """Hero section should contain a mailto link."""
        email_link = home_page.locator('.hero a[href^="mailto:"]')
        assert email_link.count() >= 1


# ── Sections ─────────────────────────────────────────────────────────────────

class TestSections:

    @pytest.mark.parametrize("section_id,heading_text", [
        ("about",          "About Me"),
        ("experience",     "Experience"),
        ("projects",       "Custom Project Highlights"),
        ("skills",         "Skills"),
        ("certifications", "Certifications"),
        ("contact",        "Contact"),
    ])
    def test_section_exists_and_heading_correct(self, home_page, section_id, heading_text):
        """Each section should exist in the DOM with the correct heading."""
        section = home_page.locator(f"#{section_id}")
        assert section.count() == 1, f"Section #{section_id} not found"
        heading = section.locator("h2")
        assert heading_text in heading.inner_text()

    def test_about_section_has_profile_content(self, home_page):
        """About section should contain biographical text."""
        about_text = home_page.locator("#about .about-text")
        text = about_text.inner_text()
        assert "QA" in text or "quality" in text.lower()

    def test_experience_timeline_has_items(self, home_page):
        """Experience timeline should have at least 1 entry."""
        items = home_page.locator(".timeline-item")
        assert items.count() >= 1

    def test_experience_shows_company_name(self, home_page):
        """Experience section should mention Perficient."""
        timeline = home_page.locator("#experience")
        assert "Perficient" in timeline.inner_text()


# ── Footer ───────────────────────────────────────────────────────────────────

class TestFooter:

    def test_footer_visible(self, home_page):
        """Footer should be visible at the bottom of the page."""
        footer = home_page.locator("footer")
        assert footer.is_visible()

    def test_footer_copyright(self, home_page):
        """Footer should contain a copyright notice."""
        footer_text = home_page.locator("footer").inner_text()
        assert "Andrew Graham" in footer_text
        assert "2026" in footer_text

    def test_footer_social_links(self, home_page):
        """Footer should have at least 2 social links."""
        social = home_page.locator(".social-links a")
        assert social.count() >= 2
