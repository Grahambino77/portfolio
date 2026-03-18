"""
test_countdown.py — Tests for the Countdown Timer web application (/countdown).

Covers:
  - Page loads with correct title
  - All UI elements are present (display, inputs, buttons, presets)
  - Input fields accept values
  - Preset buttons populate the correct time
  - Start button begins countdown (display changes)
  - Pause button halts countdown
  - Reset button restores defaults
  - Back to Portfolio link points to /
  - Progress bar is present
"""

import pytest
import time as time_module


BASE_URL = "http://127.0.0.1:5000"


# ── Page load ─────────────────────────────────────────────────────────────────

class TestCountdownPageLoad:

    def test_countdown_route_200(self, page):
        """GET /countdown should return HTTP 200."""
        response = page.goto(f"{BASE_URL}/countdown")
        assert response.status == 200

    def test_countdown_page_title(self, countdown_page):
        """Page title should contain 'Countdown Timer'."""
        assert "Countdown Timer" in countdown_page.title()

    def test_back_link_present(self, countdown_page):
        """'Back to Portfolio' link should be visible."""
        link = countdown_page.locator(".back-link")
        assert link.is_visible()
        assert link.get_attribute("href") == "/"

    def test_page_heading_visible(self, countdown_page):
        """Page heading should display 'Countdown Timer'."""
        heading = countdown_page.locator("h1")
        assert "Countdown" in heading.inner_text()
        assert "Timer" in heading.inner_text()


# ── UI elements ───────────────────────────────────────────────────────────────

class TestCountdownUIElements:

    def test_timer_display_visible(self, countdown_page):
        """Main timer display should be visible."""
        display = countdown_page.locator("#timerDisplay")
        assert display.is_visible()

    def test_hours_input_visible(self, countdown_page):
        """Hours input should be visible."""
        assert countdown_page.locator("#inputHours").is_visible()

    def test_minutes_input_visible(self, countdown_page):
        """Minutes input should be visible."""
        assert countdown_page.locator("#inputMinutes").is_visible()

    def test_seconds_input_visible(self, countdown_page):
        """Seconds input should be visible."""
        assert countdown_page.locator("#inputSeconds").is_visible()

    def test_start_button_visible(self, countdown_page):
        """Start button should be visible and enabled."""
        btn = countdown_page.locator("#btnStart")
        assert btn.is_visible()
        assert btn.is_enabled()

    def test_pause_button_visible_but_disabled(self, countdown_page):
        """Pause button should be visible but disabled before start."""
        btn = countdown_page.locator("#btnPause")
        assert btn.is_visible()
        assert not btn.is_enabled()

    def test_reset_button_visible(self, countdown_page):
        """Reset button should be visible."""
        assert countdown_page.locator("#btnReset").is_visible()

    def test_progress_bar_present(self, countdown_page):
        """Progress bar should exist in the DOM."""
        bar = countdown_page.locator("#progressBar")
        assert bar.count() == 1

    def test_status_label_shows_ready(self, countdown_page):
        """Status label should show 'Ready' on page load."""
        label = countdown_page.locator("#statusLabel")
        assert "READY" in label.inner_text().upper() or "Ready" in label.inner_text()

    def test_preset_buttons_present(self, countdown_page):
        """There should be at least 5 preset buttons."""
        presets = countdown_page.locator(".preset-btn")
        assert presets.count() >= 5

    def test_footer_visible(self, countdown_page):
        """App footer should be visible."""
        footer = countdown_page.locator(".app-footer")
        assert footer.is_visible()
        assert "Andrew Graham" in footer.inner_text()


# ── Input interaction ─────────────────────────────────────────────────────────

class TestCountdownInputs:

    def test_default_display_shows_zero_minutes(self, countdown_page):
        """Default display should show 00:00:00 (0 minutes)."""
        display = countdown_page.locator("#timerDisplay")
        assert display.inner_text() == "00:00:00"

    def test_minutes_input_default_is_zero(self, countdown_page):
        """Minutes input should default to 0."""
        value = countdown_page.locator("#inputMinutes").input_value()
        assert value == "0"

    def test_changing_minutes_updates_display(self, countdown_page):
        """Changing minutes input should update the timer display."""
        countdown_page.locator("#inputMinutes").click(click_count=3)
        countdown_page.locator("#inputMinutes").fill("10")
        countdown_page.locator("#inputMinutes").dispatch_event("input")
        countdown_page.wait_for_timeout(200)
        display = countdown_page.locator("#timerDisplay").inner_text()
        assert display == "00:10:00"

    def test_preset_1min_sets_correct_time(self, countdown_page):
        """Clicking '1 min' preset should set display to 00:01:00."""
        countdown_page.locator(".preset-btn", has_text="1 min").click()
        countdown_page.wait_for_timeout(200)
        display = countdown_page.locator("#timerDisplay").inner_text()
        assert display == "00:01:00"

    def test_preset_25min_sets_correct_time(self, countdown_page):
        """Clicking '25 min' preset should set display to 00:25:00."""
        countdown_page.locator(".preset-btn", has_text="25 min").click()
        countdown_page.wait_for_timeout(200)
        display = countdown_page.locator("#timerDisplay").inner_text()
        assert display == "00:25:00"

    def test_preset_1hr_sets_correct_time(self, countdown_page):
        """Clicking '1 hr' preset should set display to 01:00:00."""
        countdown_page.locator(".preset-btn", has_text="1 hr").click()
        countdown_page.wait_for_timeout(200)
        display = countdown_page.locator("#timerDisplay").inner_text()
        assert display == "01:00:00"


# ── Timer controls ────────────────────────────────────────────────────────────

class TestCountdownControls:

    def test_start_button_enables_pause(self, countdown_page):
        """Clicking Start should enable the Pause button."""
        countdown_page.get_by_role("button", name="5 min", exact=True).click()
        countdown_page.locator("#btnStart").click()
        countdown_page.wait_for_timeout(300)
        assert countdown_page.locator("#btnPause").is_enabled()

    def test_start_button_disables_itself(self, countdown_page):
        """Clicking Start should disable the Start button while running."""
        countdown_page.get_by_role("button", name="5 min", exact=True).click()
        countdown_page.locator("#btnStart").click()
        countdown_page.wait_for_timeout(300)
        assert not countdown_page.locator("#btnStart").is_enabled()

    def test_display_counts_down_after_start(self, countdown_page):
        """Display should change after timer starts (count down 1 second)."""
        # Set to 5 seconds for speed
        countdown_page.locator("#inputMinutes").click(click_count=3)
        countdown_page.locator("#inputMinutes").fill("0")
        countdown_page.locator("#inputMinutes").dispatch_event("input")
        countdown_page.locator("#inputSeconds").click(click_count=3)
        countdown_page.locator("#inputSeconds").fill("5")
        countdown_page.locator("#inputSeconds").dispatch_event("input")
        countdown_page.wait_for_timeout(200)

        countdown_page.locator("#btnStart").click()
        before = countdown_page.locator("#timerDisplay").inner_text()

        # Wait 1.5 seconds — display should have ticked at least once
        countdown_page.wait_for_timeout(1500)
        after = countdown_page.locator("#timerDisplay").inner_text()
        assert before != after, "Timer display did not change after starting"

    def test_pause_button_stops_countdown(self, countdown_page):
        """Clicking Pause should stop the countdown (display freezes)."""
        countdown_page.locator("#inputMinutes").click(click_count=3)
        countdown_page.locator("#inputMinutes").fill("0")
        countdown_page.locator("#inputMinutes").dispatch_event("input")
        countdown_page.locator("#inputSeconds").click(click_count=3)
        countdown_page.locator("#inputSeconds").fill("10")
        countdown_page.locator("#inputSeconds").dispatch_event("input")
        countdown_page.wait_for_timeout(200)

        countdown_page.locator("#btnStart").click()
        countdown_page.wait_for_timeout(1200)
        countdown_page.locator("#btnPause").click()
        paused_display = countdown_page.locator("#timerDisplay").inner_text()

        # Wait another second — display should NOT change while paused
        countdown_page.wait_for_timeout(1200)
        still_paused = countdown_page.locator("#timerDisplay").inner_text()
        assert paused_display == still_paused, "Timer kept ticking after Pause"

    def test_reset_restores_defaults(self, countdown_page):
        """Clicking Reset should restore the display to 00:00:00."""
        countdown_page.locator(".preset-btn", has_text="25 min").click()
        countdown_page.locator("#btnStart").click()
        countdown_page.wait_for_timeout(500)
        countdown_page.locator("#btnReset").click()
        countdown_page.wait_for_timeout(200)

        display = countdown_page.locator("#timerDisplay").inner_text()
        assert display == "00:00:00"

    def test_reset_re_enables_start_button(self, countdown_page):
        """After Reset, Start button should be re-enabled."""
        countdown_page.locator("#btnStart").click()
        countdown_page.wait_for_timeout(300)
        countdown_page.locator("#btnReset").click()
        countdown_page.wait_for_timeout(200)
        assert countdown_page.locator("#btnStart").is_enabled()

    def test_reset_disables_pause_button(self, countdown_page):
        """After Reset, Pause button should be disabled again."""
        countdown_page.locator("#btnStart").click()
        countdown_page.wait_for_timeout(300)
        countdown_page.locator("#btnReset").click()
        countdown_page.wait_for_timeout(200)
        assert not countdown_page.locator("#btnPause").is_enabled()
