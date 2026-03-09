# Andrew Graham — Personal Portfolio Website

A full-stack personal portfolio site built with **HTML/CSS/JavaScript** on the front end and **Python Flask** on the back end. Features a responsive dark-themed design, an animated contact form with Gmail integration, a Countdown Timer application (web + desktop), and a comprehensive Playwright automation test suite.

🔗 **GitHub:** https://github.com/Grahambino77/portfolio

---

## 📁 Project Structure

```
Resume/
├── index.html                    ← Main portfolio page (single-page)
├── requirements.txt              ← Python dependencies (Flask + Playwright + pytest)
├── .env                          ← 🔒 Secret credentials (never commit this)
├── .env.example                  ← Safe template — copy to .env and fill in values
├── .gitignore                    ← Excludes .env, __pycache__, venv, etc.
├── README.md                     ← You are here
│
├── backend/
│   ├── app.py                    ← Flask server (routes, email, rate limiting)
│   └── countdown_app.py          ← Python/Tkinter desktop countdown timer app
│
├── static/
│   ├── css/
│   │   └── styles.css            ← All styles (dark theme, responsive, animations)
│   ├── js/
│   │   └── main.js               ← Scroll effects, form logic, success animation
│   ├── img/
│   │   └── .gitkeep              ← Drop profile.jpg and resume.pdf here
│   ├── sounds/
│   │   └── frog.mp3              ← Alert sound — plays 3× when countdown reaches zero
│   └── countdown/
│       └── index.html            ← Countdown Timer browser/web app
│
└── tests/
    ├── conftest.py               ← Shared fixtures (auto-starts Flask, browser setup)
    ├── test_homepage.py          ← 30 tests: nav, hero, sections, footer
    ├── test_projects.py          ← 16 tests: project cards, buttons, placeholders
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
| **Gmail Sending** | HTML email sent via Gmail SMTP (TLS port 587) |
| **Rate Limiting** | Max 5 submissions per IP per 10 minutes |
| **Honeypot** | Hidden field silently rejects bot submissions |
| **Environment Variables** | Credentials stored securely in `.env` |
| **Countdown Timer (Web)** | Browser-based JS timer at `/countdown` with presets & frog alert |
| **Countdown Timer (Desktop)** | Python/Tkinter desktop app (`backend/countdown_app.py`) |
| **Playwright Test Suite** | 92 automated tests — all passing |

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
GMAIL_USER=agraham17gv@gmail.com
GMAIL_APP_PASS=your-16-char-app-password
NOTIFY_EMAIL=agraham17gv@gmail.com
```

### 4. Generate a Gmail App Password

1. Go to [myaccount.google.com/security](https://myaccount.google.com/security)
2. Enable **2-Step Verification** (required)
3. Search for **"App passwords"**
4. Select **Mail** → **Windows Computer** → Generate
5. Copy the 16-character code into `GMAIL_APP_PASS` in your `.env`

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

The project includes **92 Playwright + pytest tests** that run against the live Flask server.

### Run all tests
```powershell
python -m pytest tests/ -v
```

### Run with visible browser (headed mode)
```powershell
python -m pytest tests/ -v --headed
```

### Run a specific file
```powershell
python -m pytest tests/test_homepage.py -v
python -m pytest tests/test_countdown.py -v
```

### Test results (latest run)
```
92 passed in 28.40s
```

### Test coverage breakdown

| File | Tests | What is tested |
|---|---|---|
| `test_homepage.py` | 30 | Page title, CSS/JS loading, navbar links, hero section, all 6 page sections, footer |
| `test_projects.py` | 16 | 3 project cards, Countdown card title/description/tags/buttons/hrefs, Spring & Summer 2026 placeholders |
| `test_contact.py` | 18 | Contact details visible, form fields present, honeypot off-screen, required validation, invalid email format, `/health` JSON response |
| `test_countdown.py` | 28 | Page load, H/M/S inputs, all 7 presets, live countdown tick, Pause freezes display, Reset restores defaults |

### How `conftest.py` works
- **`flask_server` fixture** — checks if port 5000 is already in use; if not, spawns `python backend/app.py` as a subprocess and waits up to 15 seconds for it to accept connections; cleans up on session teardown
- **`browser_instance` fixture** — session-scoped Chromium browser (one instance for all 92 tests)
- **`page` fixture** — function-scoped; fresh browser context + page per test
- **`home_page` / `countdown_page`** — convenience fixtures that navigate to the relevant URL before each test

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
| `GET` | `/countdown` | Serves the Countdown Timer web app |
| `GET` | `/launch-desktop` | Spawns `countdown_app.py` as a detached subprocess; returns confirmation page |
| `POST` | `/contact` | Accepts contact form JSON, sends Gmail notification |
| `GET` | `/health` | Returns `{ "status": "ok", "email_configured": true/false }` |

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
| `playwright` | ≥ 1.42 | Browser automation for tests |
| `pytest` | ≥ 8.0 | Test framework |
| `pytest-playwright` | ≥ 0.4.4 | Playwright fixtures for pytest |

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
