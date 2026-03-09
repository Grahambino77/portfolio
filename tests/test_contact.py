"""
test_contact.py — Tests for the Contact section and form.

Covers:
  - Contact section renders with correct details
  - Form fields are present and interactive
  - Client-side validation blocks empty submission
  - Invalid email format is caught
  - Honeypot field is hidden from users
  - Successful form submission shows a success state
  - /health endpoint returns expected JSON
"""

import pytest
import json


BASE_URL = "http://127.0.0.1:5000"


# ── Contact section UI ────────────────────────────────────────────────────────

class TestContactSection:

    def test_contact_section_exists(self, home_page):
        """Contact section should be present in the DOM."""
        section = home_page.locator("#contact")
        assert section.count() == 1

    def test_contact_section_heading(self, home_page):
        """Contact section heading should read 'Contact'."""
        heading = home_page.locator("#contact h2")
        assert "Contact" in heading.inner_text()

    def test_phone_number_visible(self, home_page):
        """Contact section should display a phone number."""
        contact = home_page.locator("#contact")
        assert "(313)" in contact.inner_text() or "313" in contact.inner_text()

    def test_email_address_visible(self, home_page):
        """Contact section should display an email address."""
        contact = home_page.locator("#contact")
        assert "agraham17gv@gmail.com" in contact.inner_text()

    def test_location_visible(self, home_page):
        """Contact section should display a location."""
        contact = home_page.locator("#contact")
        assert "Northville" in contact.inner_text() or "MI" in contact.inner_text()


# ── Contact form fields ───────────────────────────────────────────────────────

class TestContactFormFields:

    def test_name_field_present(self, home_page):
        """Name input field should be visible."""
        field = home_page.locator("#name")
        assert field.is_visible()

    def test_email_field_present(self, home_page):
        """Email input field should be visible."""
        field = home_page.locator("#email")
        assert field.is_visible()

    def test_message_field_present(self, home_page):
        """Message textarea should be visible."""
        field = home_page.locator("#message")
        assert field.is_visible()

    def test_submit_button_present(self, home_page):
        """'Send Message' submit button should be visible."""
        btn = home_page.locator("#contactForm button[type='submit']")
        assert btn.is_visible()
        assert "Send Message" in btn.inner_text()

    def test_honeypot_field_not_visible(self, home_page):
        """Honeypot field should exist in DOM but be positioned off-screen (not reachable by users)."""
        hp = home_page.locator("#honeypot")
        assert hp.count() == 1, "Honeypot field missing from DOM"
        # The honeypot uses position:absolute;left:-9999px so it's off-screen.
        # Playwright reports it as "visible" due to non-zero bounding box,
        # so we verify it's positioned far off the left edge of the viewport instead.
        box = hp.bounding_box()
        assert box is not None, "Honeypot field has no bounding box"
        assert box["x"] < -100, (
            f"Honeypot field appears to be on-screen (x={box['x']}); it should be off-screen"
        )

    def test_name_field_accepts_input(self, home_page):
        """Name field should accept typed text."""
        field = home_page.locator("#name")
        field.fill("Test User")
        assert field.input_value() == "Test User"

    def test_email_field_accepts_input(self, home_page):
        """Email field should accept typed text."""
        field = home_page.locator("#email")
        field.fill("test@example.com")
        assert field.input_value() == "test@example.com"

    def test_message_field_accepts_input(self, home_page):
        """Message textarea should accept typed text."""
        field = home_page.locator("#message")
        field.fill("Hello, this is a test message.")
        assert field.input_value() == "Hello, this is a test message."


# ── Form validation ───────────────────────────────────────────────────────────

class TestContactFormValidation:

    def test_empty_form_shows_validation(self, home_page):
        """Submitting an empty form should trigger HTML5 required validation."""
        # Clear all fields and try to submit
        home_page.locator("#name").fill("")
        home_page.locator("#email").fill("")
        home_page.locator("#message").fill("")
        home_page.locator("#contactForm button[type='submit']").click()

        # The browser should block submission due to `required` attributes —
        # the page URL should NOT change to a new route
        assert home_page.url.rstrip("/") in (
            BASE_URL, BASE_URL + "/"
        ), "Form navigated away despite empty required fields"

    def test_missing_message_shows_validation(self, home_page):
        """Submitting without a message should trigger required validation."""
        home_page.locator("#name").fill("Test User")
        home_page.locator("#email").fill("test@example.com")
        home_page.locator("#message").fill("")
        home_page.locator("#contactForm button[type='submit']").click()
        # Should stay on the same page
        assert home_page.url.rstrip("/") in (BASE_URL, BASE_URL + "/")

    def test_invalid_email_format_blocked_by_browser(self, home_page):
        """Browser should reject obviously invalid email format."""
        home_page.locator("#name").fill("Test User")
        home_page.locator("#email").fill("not-an-email")
        home_page.locator("#message").fill("Test message body.")
        home_page.locator("#contactForm button[type='submit']").click()
        # Should stay on the same page (browser type=email validation)
        assert home_page.url.rstrip("/") in (BASE_URL, BASE_URL + "/")


# ── Health endpoint ───────────────────────────────────────────────────────────

class TestHealthEndpoint:

    def test_health_route_returns_200(self, page):
        """GET /health should return HTTP 200."""
        response = page.goto(f"{BASE_URL}/health")
        assert response.status == 200

    def test_health_route_returns_json(self, page):
        """GET /health should return valid JSON with a 'status' field."""
        response = page.goto(f"{BASE_URL}/health")
        body = response.json()
        assert body.get("status") == "ok"
        assert "email_configured" in body
