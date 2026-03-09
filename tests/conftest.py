"""
conftest.py — Shared fixtures for the portfolio Playwright test suite.

Automatically starts and stops the Flask server so tests are self-contained.

Run all tests:
    pytest tests/ -v

Run with headed browser (watch the browser):
    pytest tests/ -v --headed

Run a specific file:
    pytest tests/test_homepage.py -v
"""

import os
import sys
import time
import socket
import subprocess
import pytest
from playwright.sync_api import sync_playwright

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
BASE_URL   = "http://127.0.0.1:5000"
ROOT_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERVER_CMD = [sys.executable, os.path.join(ROOT_DIR, "backend", "app.py")]


# ---------------------------------------------------------------------------
# Helper — wait until port 5000 is accepting connections
# ---------------------------------------------------------------------------
def _wait_for_server(host: str = "127.0.0.1", port: int = 5000, timeout: float = 15.0):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with socket.create_connection((host, port), timeout=0.5):
                return True
        except OSError:
            time.sleep(0.25)
    raise RuntimeError(f"Flask server did not start within {timeout}s")


# ---------------------------------------------------------------------------
# Session-scoped Flask server fixture
# Starts the server once per test session; stops it when tests are done.
# ---------------------------------------------------------------------------
@pytest.fixture(scope="session")
def flask_server():
    """Start the Flask dev server in a subprocess for the test session."""
    # Don't start a second server if one is already listening on port 5000
    already_running = False
    try:
        with socket.create_connection(("127.0.0.1", 5000), timeout=0.5):
            already_running = True
    except OSError:
        pass

    if already_running:
        yield BASE_URL
        return

    env = os.environ.copy()
    env["FLASK_ENV"] = "testing"

    proc = subprocess.Popen(
        SERVER_CMD,
        cwd=ROOT_DIR,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    try:
        _wait_for_server()
        yield BASE_URL
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()


# ---------------------------------------------------------------------------
# Session-scoped browser fixture
# ---------------------------------------------------------------------------
@pytest.fixture(scope="session")
def browser_instance(flask_server):
    """Launch a single Chromium browser for the entire test session."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


# ---------------------------------------------------------------------------
# Function-scoped page fixture — fresh page + context per test
# ---------------------------------------------------------------------------
@pytest.fixture
def page(browser_instance):
    context = browser_instance.new_context(viewport={"width": 1280, "height": 800})
    pg = context.new_page()
    yield pg
    pg.close()
    context.close()


# ---------------------------------------------------------------------------
# Convenience fixture — navigates to the portfolio home page
# ---------------------------------------------------------------------------
@pytest.fixture
def home_page(page):
    page.goto(BASE_URL, wait_until="load")
    return page


# ---------------------------------------------------------------------------
# Convenience fixture — navigates to the countdown web app page
# ---------------------------------------------------------------------------
@pytest.fixture
def countdown_page(page):
    page.goto(f"{BASE_URL}/countdown", wait_until="load")
    return page
