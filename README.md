# Andrew Graham — Personal Portfolio Website

A full-stack personal portfolio site built with **HTML/CSS/JavaScript** on the front end and **Python Flask** on the back end. Features a responsive dark-themed design, an animated contact form with Gmail integration, and multiple layers of spam protection.

---

## 📁 Project Structure

```
Resume/
├── index.html               ← Main portfolio page (single-page)
├── requirements.txt         ← Python dependencies
├── .env                     ← 🔒 Secret credentials (never commit this)
├── .env.example             ← Safe template — copy to .env and fill in values
├── .gitignore               ← Excludes .env, __pycache__, venv, etc.
├── README.md                ← You are here
│
├── backend/
│   └── app.py               ← Flask server (routes, email, rate limiting)
│
└── static/
    ├── css/
    │   └── styles.css       ← All styles (dark theme, responsive, animations)
    ├── js/
    │   └── main.js          ← Scroll effects, form logic, success animation
    └── img/
        └── .gitkeep         ← Drop profile.jpg and resume.pdf here
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

---

## 🚀 Getting Started

### 1. Install Python dependencies

```powershell
python -m pip install -r requirements.txt
```

> **Note:** Use `python -m pip` on Windows if `pip` is not on your PATH.

### 2. Configure environment variables

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

### 3. Generate a Gmail App Password

1. Go to [myaccount.google.com/security](https://myaccount.google.com/security)
2. Enable **2-Step Verification** (required)
3. Search for **"App passwords"**
4. Select **Mail** → **Windows Computer** → Generate
5. Copy the 16-character code into `GMAIL_APP_PASS` in your `.env`

> ⚠️ Use your App Password — **not** your regular Gmail password.

### 4. Add your images

Place these files in `static/img/`:
- `profile.jpg` — your profile photo (displays in the About section)
- `resume.pdf` — your resume (linked from the Download button)

### 5. Run the server

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
| **Projects** | Python debugging tools, countdown timer, QA dashboards |
| **Skills** | QA & Testing · Tools & Platforms · Programming & Web · Professional |
| **Certifications** | 6 certifications displayed as interactive cards |
| **Contact** | Contact details + validated email form |

---

## 🛡️ Spam Protection (3 Layers)

1. **Honeypot field** — Hidden `<input>` invisible to humans; bots that auto-fill it are silently rejected with no error feedback
2. **Rate limiting** — `flask-limiter` caps submissions at **5 per 10 minutes per IP address**; returns HTTP 429 with a friendly message
3. **Server-side validation** — All fields are required, email is regex-validated, and field lengths are capped (name ≤ 100, message ≤ 5000 chars)

---

## 🔌 API Endpoints

| Method | Route | Description |
|---|---|---|
| `GET` | `/` | Serves `index.html` |
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

Install all at once:
```powershell
python -m pip install -r requirements.txt
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

---

## 🚢 Deployment Notes

> The Flask dev server (`debug=True`) is for **local development only**.  
> For production, use a production WSGI server:

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
