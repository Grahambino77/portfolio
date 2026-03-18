# Andrew Graham — Personal Portfolio Website

A full-stack personal portfolio site built with **HTML/CSS/JavaScript** on the front end and **Python Flask** on the back end. Features a responsive dark-themed design, an animated contact form with Resend email integration, a Countdown Timer application (web + desktop), and a comprehensive Playwright automation test suite.

🔗 **GitHub:** https://github.com/Grahambino77/portfolio

---

## 📁 Project Structure

```
Resume/
├── index.html                    ← Main portfolio page (single-page)
├── pytest.ini                    ← pytest config — auto-generates HTML report on every run
├── requirements.txt              ← Python dependencies (Flask + Playwright + pytest)
├── .env                          ← 🔒 Secret credentials (never commit this)
├── .env.example                  ← Safe template — copy to .env and fill in values
├── .gitignore                    ← Excludes .env, __pycache__, venv, reports/, etc.
├── README.md                     ← You are here
│
├── backend/
│   ├── app.py                    ← Flask server (routes, Resend email, rate limiting)
│   └── countdown_app.py          ← Python/Tkinter desktop countdown timer app
│
├── static/
│   ├── css/
│   │   └── styles.css            ← All styles (dark theme, responsive, animations)
│   ├── js/
│   │   └── main.js               ← Scroll effects, smooth-scroll nav, form logic
│   ├── img/
│   │   └── .gitkeep              ← Drop profile.jpg and resume.pdf here
│   ├── sounds/
│   │   └── frog.mp3              ← Alert sound — plays 3× when countdown reaches zero
│   └── countdown/
│       └── index.html            ← Countdown Timer browser/web app
│
├── reports/                      ← Auto-generated HTML test reports (gitignored)
│   ├── report.html               ← Always the most recent run — easy to open
│   └── report_YYYY-MM-DD_HH-MM-SS.html  ← Timestamped archive of every run
│
└── tests/
    ├── conftest.py               ← Shared fixtures (auto-starts Flask, browser setup)
    ├── test_homepage.py          ← 30 tests: nav, hero, sections, footer
    ├── test_nav_links.py         ← 31 tests: global nav anchor links & smooth-scroll
    ├── test_projects.py          ← 14 tests: project cards, buttons, placeholders
    ├── test_contact.py           ← 18 tests: form fields, validation, health endpoint
    └── test_countdown.py         ← 28 tests: timer UI, inputs, controls, countdown logic
```

---

## ✨ Features

| Feature | Details |
|---|---|
| **Responsive Design** | Mobile-first layout using CSS Grid & Flexbox |
| **Sticky Navbar** | Active link highlighting as you scroll |
| **Scroll-Reveal** | Elements animate in using `IntersectionObserver` |
| **Experience Timeline** | Vertical timeline with role history and skill tags |
| **Skills Grid** | Four categorized skill groups (QA, Tools, Code, Professional) |
| **Certifications** | Card grid with hover effects |
| **Contact Form** | Validated form with animated SVG checkmark on success |
| **Resend Email** | HTML email sent via Resend API (HTTPS — works on Render free tier) |
| **Rate Limiting** | Max 5 submissions per IP per 10 minutes |
| **Honeypot** | Hidden field silently rejects bot submissions |
| **Environment Variables** | Credentials stored securely in `.env` |
| **Countdown Timer (Web)** | Browser-based JS timer at `/countdown` with presets & frog alert |
| **Countdown Timer (Desktop)** | Python/Tkinter desktop app (`backend/countdown_app.py`) |
| **Playwright Test Suite** | 121 automated tests — all passing |
| **HTML Test Report** | Auto-generated `reports/report.html` on every `pytest` run |

---

## 🚀 Getting Started

### 1. Install Python dependencies

```powershell
python -m pip install -r requirements.txt
```

### 2. Install Playwright browser (for running tests)

```powershell
python -m playwright install chromium
```

### 3. Configure environment variables

Copy the example file and fill in your values:

```powershell
copy .env.example .env
```

Then open `.env` and update:

```env
SECRET_KEY=your-long-random-secret-key
RESEND_API_KEY=re_your_resend_api_key
NOTIFY_EMAIL=agraham17gv@gmail.com
RESEND_FROM=Portfolio Contact <onboarding@resend.dev>
```

### 4. Get a Resend API key

The contact form sends email via [Resend](https://resend.com) (HTTPS API — not blocked by Render's free tier).

1. Sign up at [resend.com](https://resend.com)
2. Create an API key under **API Keys**
3. Copy it into `RESEND_API_KEY` in your `.env`
4. Set `NOTIFY_EMAIL` to the address where you want to receive contact messages

### 5. Add your images

Place these files in `static/img/`:
- `profile.jpg` — your profile photo (displays in the About section)
- `resume.pdf` — your resume (linked from the Download button)

### 6. Run the Flask server

```powershell
python backend/app.py
```

Then open **http://127.0.0.1:5000** in your browser.

---

## 🌐 Page Sections

| Section | Description |
|---|---|
| **Hero** | Name, title, contact info, CTA buttons |
| **About** | Professional summary with profile photo |
| **Experience** | Animated timeline — Sr. Consultant → Consultant → Associate |
| **Projects** | Countdown Timer app + Spring/Summer 2026 placeholders |
| **Skills** | QA & Testing · Tools & Platforms · Programming & Web · Professional |
| **Certifications** | 6 certifications displayed as interactive cards |
| **Contact** | Contact details + validated email form |

---

## ⏱️ Countdown Timer Application

The portfolio features a fully functional Countdown Timer available in two versions:

### Web App (Browser)
- Accessible at **http://127.0.0.1:5000/countdown**
- Linked from the project card via **🌐 Launch Web App Version**
- Built in HTML/CSS/JavaScript — no install required
- Features: H/M/S inputs, 7 quick presets, progress bar, Pause/Resume/Reset
- Plays **frog.mp3 three times** when the timer hits zero (served from `/static/sounds/frog.mp3`)

### Desktop App (Python/Tkinter)
- Launch via **🖥 Launch Desktop App** button on the portfolio
  - This hits `GET /launch-desktop` which spawns the app as a detached subprocess
- Or run directly:
  ```powershell
  python backend/countdown_app.py
  ```
- Built with Python + Tkinter + threading
- Uses Windows MCI (`ctypes.windll.winmm`) to play the frog.mp3 alert 3 times
- Same feature set as the web version (presets, pause/resume, progress bar, flash animation)

| Feature | Python/Tkinter | JavaScript/Browser |
|---|---|---|
| Tick engine | `threading.Thread` + `time.sleep(1)` | `setInterval(tick, 1000)` |
| UI updates | `self.after(0, callback)` | DOM updates each tick |
| Progress bar | `ttk.Progressbar` | CSS width transition |
| Sound alert | Windows MCI via `ctypes` | `new Audio().play()` |
| Alert on done | Flash animation + modal | Pulse animation + overlay |

---

## 🧪 Automated Test Suite

The project includes **121 Playwright + pytest tests** across 5 files, all running against the live Flask server. Every `pytest` run automatically produces `reports/report.html` — a self-contained HTML report you can open in any browser.

### Run all tests
```powershell
python -m pytest tests/
```

### Run with a visible browser window
```powershell
# Open Chromium and watch the tests execute
python -m pytest tests/ --headed

# Slow each action down by 600 ms so you can follow along
python -m pytest tests/ --headed --slowmo 600
```

### Run a specific file or class
```powershell
python -m pytest tests/test_nav_links.py -v
python -m pytest tests/test_homepage.py -v
python -m pytest tests/test_countdown.py -v
python -m pytest tests/test_nav_links.py::TestNavLinkNavigation -v
```

### Run only tests matching a keyword
```powershell
python -m pytest tests/ -k "scroll"
python -m pytest tests/ -k "Contact"
```

### HTML report — latest run & archived history
Every run overwrites `reports/report.html` (always current) **and** saves a permanent timestamped copy so no run is ever lost:

```
reports/report.html                        ← most recent run — always up to date
reports/report_2026-03-18_12-23-46.html   ← archived snapshot of that run
reports/report_2026-03-18_11-49-54.html   ← archived snapshot of a previous run
```

Open the latest report:
```powershell
Invoke-Item "C:\Users\agrah\Resume\reports\report.html"
```
All report files are gitignored — they are never committed to GitHub.

### Test results (latest run)
```
121 passed in 48.90s
```

### Test coverage breakdown

| File | Tests | What is tested |
|---|---|---|
| `test_homepage.py` | 30 | Page title, CSS/JS loading, navbar, hero section, all 6 page sections, footer |
| `test_nav_links.py` | 31 | All 6 nav links present with correct `href` and label text; visible on desktop; smooth-scroll lands within 100 px of target; section enters viewport |
| `test_projects.py` | 14 | 3 project cards, Countdown card title/description/tags/button/href, Spring & Summer 2026 placeholders |
| `test_contact.py` | 18 | Contact details visible, form fields present, honeypot off-screen, required validation, invalid email format, `/health` JSON keys |
| `test_countdown.py` | 28 | Page load, H/M/S inputs, all 7 presets, live countdown tick, Pause freezes display, Reset restores defaults |

### How `conftest.py` works
- **`flask_server` fixture** — checks if port 5000 is already in use; if not, spawns `python backend/app.py` as a subprocess and waits up to 15 seconds for it to accept connections; cleans up on session teardown
- **`browser_instance` fixture** — session-scoped Chromium; reads `--headed` and `--slowmo` CLI flags so the browser opens visibly when requested
- **`page` fixture** — function-scoped; fresh browser context + page per test
- **`home_page` / `countdown_page`** — convenience fixtures that navigate to the relevant URL before each test
- **`pytest_sessionfinish` hook** — runs at the end of every session; copies `reports/report.html` to a timestamped archive (`reports/report_YYYY-MM-DD_HH-MM-SS.html`) so previous runs are never lost

### Note on nav smooth-scroll tests
`main.js` intercepts every `a[href^="#"]` click with `e.preventDefault()` and uses `window.scrollTo({behavior:'smooth'})` with a 70 px sticky-header offset. This intentionally skips native anchor navigation (the URL hash is never updated). `test_nav_links.py` therefore asserts on `window.scrollY` and uses a JS-polling wait (samples every 80 ms until `scrollY` stops moving) instead of a fixed sleep.

---

## 🛡️ Spam Protection (3 Layers)

1. **Honeypot field** — Hidden `<input>` invisible to humans (positioned at `left: -9999px`); bots that auto-fill it are silently rejected
2. **Rate limiting** — `flask-limiter` caps submissions at **5 per 10 minutes per IP**; returns HTTP 429
3. **Server-side validation** — All fields required, email regex-validated, field lengths capped (name ≤ 100, message ≤ 5000 chars)

---

## 🔌 API Endpoints

| Method | Route | Description |
|---|---|---|
| `GET` | `/` | Serves `index.html` |
| `GET` | `/countdown` | Serves the Countdown Timer web app (`static/countdown/index.html`) |
| `GET` | `/launch-desktop` | Redirects to `/download/countdown-timer` |
| `GET` | `/download/countdown-timer` | Serves `CountdownTimer.exe` as a direct file download |
| `POST` | `/contact` | Accepts contact form JSON, sends notification email via Resend API |
| `GET` | `/health` | Returns `{ "status": "ok", "resend_api_key_set": bool, "notify_email_set": bool, "resend_from": str }` |

### Contact endpoint — request body

```json
{
  "name":     "Jane Doe",
  "email":    "jane@example.com",
  "message":  "Hello!",
  "honeypot": ""
}
```

---

## 📦 Dependencies

| Package | Version | Purpose |
|---|---|---|
| `flask` | ≥ 3.0 | Web framework & routing |
| `flask-limiter` | ≥ 3.5 | Rate limiting / spam protection |
| `python-dotenv` | ≥ 1.0 | Load `.env` into `os.environ` |
| `resend` | ≥ 2.0 | Resend HTTP API client for sending contact emails |
| `gunicorn` | latest | WSGI server for production deployment |
| `playwright` | ≥ 1.42 | Browser automation for tests |
| `pytest` | ≥ 8.0 | Test framework |
| `pytest-playwright` | ≥ 0.4.4 | Playwright fixtures for pytest |
| `pytest-html` | ≥ 4.0 | Generates self-contained HTML test reports |
| `pytest-metadata` | ≥ 2.0 | Adds environment metadata to the HTML report |

```powershell
python -m pip install -r requirements.txt
python -m playwright install chromium
```

---

## 🔧 Customization

| What to change | Where |
|---|---|
| Name, title, contact info | `index.html` → Hero section |
| About / summary text | `index.html` → About section |
| Work experience | `index.html` → Experience section |
| Projects | `index.html` → Projects section |
| Skills | `index.html` → Skills section |
| Certifications | `index.html` → Certifications section |
| Accent color | `static/css/styles.css` → `--clr-accent: #e94560` |
| Background color | `static/css/styles.css` → `--clr-bg: #0f0f0f` |
| Social links | `index.html` → Footer (update `href="#"` with real URLs) |
| Alert sound | Replace `static/sounds/frog.mp3` with any MP3 |

---

## 🚢 Deployment Notes

> The Flask dev server (`debug=True`) is for **local development only**.
> For production, use a WSGI server:

```powershell
# Option A — Waitress (Windows-friendly)
python -m pip install waitress
python -c "from waitress import serve; from backend.app import app; serve(app, host='0.0.0.0', port=8080)"

# Option B — Gunicorn (Linux/macOS)
pip install gunicorn
gunicorn -w 4 backend.app:app
```

Set environment variables on your host (Heroku, Railway, Render, etc.) instead of using a `.env` file in production.

---

## 📝 License

This project is for personal use. Feel free to adapt it for your own portfolio.

---

*Built by Andrew Graham · QA Analyst & Business Consultant · Northville, MI*
