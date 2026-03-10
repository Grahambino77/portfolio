"""
app.py — Flask backend for Andrew Graham's Portfolio
Run (from project root):
    python backend/app.py

Required packages:
    pip install flask flask-limiter python-dotenv
"""

import os
import re
import smtplib
import logging
import threading
from email.mime.multipart import MIMEMultipart
from email.mime.text      import MIMEText
from datetime             import datetime

from flask          import Flask, request, jsonify, send_from_directory
from flask_limiter  import Limiter
from flask_limiter.util import get_remote_address
from dotenv         import load_dotenv

# ---------------------------------------------------------------------------
# Load environment variables from .env (dev) or system env (production)
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))   # .../backend
ROOT_DIR = os.path.dirname(BASE_DIR)                     # .../Resume
load_dotenv(os.path.join(ROOT_DIR, ".env"))

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(
    __name__,
    static_folder=os.path.join(ROOT_DIR, "static"),
    template_folder=ROOT_DIR,
)

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "change-me-in-production")

# ---------------------------------------------------------------------------
# Rate limiting  (spam protection — layer 1)
# ---------------------------------------------------------------------------
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=[],                    # no global limit; set per-route
    storage_uri="memory://",
    swallow_errors=True,                  # prevent storage errors from causing 500s
)

# ---------------------------------------------------------------------------
# Email configuration (loaded from .env)
# ---------------------------------------------------------------------------
GMAIL_USER    = os.environ.get("GMAIL_USER", "").strip()
# Strip spaces so the password works whether entered as "abcd efgh ijkl mnop" or "abcdefghijklmnop"
GMAIL_PASS    = os.environ.get("GMAIL_APP_PASS", "").replace(" ", "").strip()
NOTIFY_EMAIL  = os.environ.get("NOTIFY_EMAIL", GMAIL_USER).strip()

EMAIL_REGEX = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def send_gmail(sender_name: str, sender_email: str, message: str) -> None:
    """Send a contact notification email via Gmail SMTP (TLS on port 587)."""
    if not GMAIL_USER or not GMAIL_PASS:
        raise EnvironmentError("GMAIL_USER or GMAIL_APP_PASS not configured in .env")

    subject = f"Portfolio Contact: {sender_name}"

    html_body = f"""
    <html><body style="font-family:Arial,sans-serif;color:#333;">
      <h2 style="color:#e94560;">New Portfolio Contact</h2>
      <table style="border-collapse:collapse;width:100%;max-width:600px;">
        <tr>
          <td style="padding:8px 12px;font-weight:bold;background:#f5f5f5;border:1px solid #ddd;width:120px;">Name</td>
          <td style="padding:8px 12px;border:1px solid #ddd;">{sender_name}</td>
        </tr>
        <tr>
          <td style="padding:8px 12px;font-weight:bold;background:#f5f5f5;border:1px solid #ddd;">Email</td>
          <td style="padding:8px 12px;border:1px solid #ddd;"><a href="mailto:{sender_email}">{sender_email}</a></td>
        </tr>
        <tr>
          <td style="padding:8px 12px;font-weight:bold;background:#f5f5f5;border:1px solid #ddd;vertical-align:top;">Message</td>
          <td style="padding:8px 12px;border:1px solid #ddd;white-space:pre-wrap;">{message}</td>
        </tr>
        <tr>
          <td style="padding:8px 12px;font-weight:bold;background:#f5f5f5;border:1px solid #ddd;">Received</td>
          <td style="padding:8px 12px;border:1px solid #ddd;">{datetime.now().strftime('%B %d, %Y at %I:%M %p')}</td>
        </tr>
      </table>
    </body></html>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = f"Portfolio Contact Form <{GMAIL_USER}>"
    msg["To"]      = NOTIFY_EMAIL
    msg["Reply-To"] = f"{sender_name} <{sender_email}>"

    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.ehlo()
        server.starttls()
        server.login(GMAIL_USER, GMAIL_PASS)
        server.sendmail(GMAIL_USER, NOTIFY_EMAIL, msg.as_string())


# ---------------------------------------------------------------------------
# Routes — Frontend
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    """Serve the portfolio front page."""
    return send_from_directory(ROOT_DIR, "index.html")


@app.route("/countdown")
def countdown():
    """Serve the Countdown Timer web application."""
    return send_from_directory(
        os.path.join(ROOT_DIR, "static", "countdown"), "index.html"
    )


@app.route("/launch-desktop")
def launch_desktop():
    """
    Kept for backwards compatibility — now redirects to the exe download page.
    (The subprocess approach only works on the local dev machine, not on Render.)
    """
    from flask import redirect
    return redirect("/download/countdown-timer")


@app.route("/download/countdown-timer")
def download_countdown_timer():
    """
    Serve CountdownTimer.exe as a direct file download.

    The .exe lives at static/files/CountdownTimer.exe and is tracked in git
    so it deploys to Render automatically.  Visitors download it and run it
    locally on Windows — no Python install required.
    """
    files_dir = os.path.join(ROOT_DIR, "static", "files")
    filename  = "CountdownTimer.exe"

    if not os.path.isfile(os.path.join(files_dir, filename)):
        logger.error("CountdownTimer.exe not found at %s", files_dir)
        return (
            "<h2 style='font-family:sans-serif;color:#e94560;text-align:center;"
            "margin-top:20vh'>⚠️ File not available — please check back soon.</h2>",
            404,
        )

    return send_from_directory(
        files_dir,
        filename,
        as_attachment=True,
        download_name="CountdownTimer.exe",
    )


# ---------------------------------------------------------------------------
# Routes — Contact Form
# ---------------------------------------------------------------------------

@app.route("/contact", methods=["POST"])
@limiter.limit("5 per 10 minutes")           # spam protection — layer 2 (rate limit)
def contact():
    """
    POST /contact
    Body (JSON): { "name", "email", "message", "honeypot" }
    Returns    : { "message" } on success  (200)
               : { "error"   } on failure  (400 / 429 / 500)
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid request — expected JSON body."}), 400

    # ── Spam protection layer 3: honeypot field ──────────────────────────────
    # The hidden <input name="honeypot"> should always be empty for real users.
    # Bots that auto-fill all fields will populate it and get silently rejected.
    honeypot = (data.get("honeypot") or "").strip()
    if honeypot:
        logger.warning("Honeypot triggered — bot submission rejected.")
        # Return 200 to avoid giving bots feedback; just silently discard
        return jsonify({"message": "Thanks for reaching out!"}), 200

    # ── Field extraction ──────────────────────────────────────────────────────
    name    = (data.get("name")    or "").strip()
    email   = (data.get("email")   or "").strip()
    message = (data.get("message") or "").strip()

    # ── Validation ────────────────────────────────────────────────────────────
    if not name or not email or not message:
        return jsonify({"error": "All fields (name, email, message) are required."}), 400

    if len(name) > 100:
        return jsonify({"error": "Name is too long (max 100 characters)."}), 400

    if not EMAIL_REGEX.match(email):
        return jsonify({"error": "Please enter a valid email address."}), 400

    if len(message) > 5000:
        return jsonify({"error": "Message is too long (max 5000 characters)."}), 400

    # ── Send email in a background thread ────────────────────────────────────
    # Sending SMTP email can take 10-30 s on some networks.  Gunicorn kills the
    # worker after 30 s, which returns a bare 500 *before* any Flask error handler
    # runs.  Offloading to a daemon thread lets us return 200 instantly and send
    # the email in the background without racing gunicorn's timeout.
    def _email_worker():
        try:
            send_gmail(name, email, message)
            logger.info("Email sent. From: %s <%s>", name, email)
        except EnvironmentError as exc:
            logger.warning(
                "Email not configured (%s). [CONTACT] Name: %s | Email: %s | Message: %s",
                exc, name, email, message,
            )
        except smtplib.SMTPAuthenticationError:
            logger.error(
                "Gmail auth failed — check GMAIL_USER / GMAIL_APP_PASS in Render env vars. "
                "[CONTACT] Name: %s | Email: %s | Message: %s", name, email, message,
            )
        except Exception as exc:
            logger.error(
                "Email error (%s). [CONTACT] Name: %s | Email: %s | Message: %s",
                exc, name, email, message,
            )

    threading.Thread(target=_email_worker, daemon=True).start()
    return jsonify({"message": "Thanks for reaching out! I'll get back to you soon."}), 200


# ---------------------------------------------------------------------------
# Custom error handler for rate-limit exceeded (429)
# ---------------------------------------------------------------------------

@app.errorhandler(429)
def rate_limit_handler(e):
    return jsonify({
        "error": "Too many messages sent. Please wait a few minutes before trying again."
    }), 429


# ---------------------------------------------------------------------------
# Health-check
# ---------------------------------------------------------------------------

@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "email_configured": bool(GMAIL_USER and GMAIL_PASS),
        "gmail_user_set": bool(GMAIL_USER),
        "gmail_pass_set": bool(GMAIL_PASS),
        "notify_email_set": bool(NOTIFY_EMAIL),
    }), 200


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True, port=5000)
