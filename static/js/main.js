/* =========================================================
   main.js — Personal Portfolio
   ========================================================= */

'use strict';

/* ----------------------------------------------------------
   0. Mobile hamburger menu toggle
---------------------------------------------------------- */
const navToggle = document.getElementById('navToggle');
const navMenu = document.getElementById('navLinks');   // the <ul> element

if (navToggle && navMenu) {
  navToggle.addEventListener('click', () => {
    const isOpen = navMenu.classList.toggle('open');
    navToggle.classList.toggle('open', isOpen);
    navToggle.setAttribute('aria-expanded', String(isOpen));
  });

  // Close the menu whenever a nav link is clicked
  navMenu.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      navMenu.classList.remove('open');
      navToggle.classList.remove('open');
      navToggle.setAttribute('aria-expanded', 'false');
    });
  });

  // Close the menu if the user taps outside the header
  document.addEventListener('click', (e) => {
    if (!e.target.closest('header')) {
      navMenu.classList.remove('open');
      navToggle.classList.remove('open');
      navToggle.setAttribute('aria-expanded', 'false');
    }
  });
}

/* ----------------------------------------------------------
   1. Active nav-link highlighting on scroll
---------------------------------------------------------- */
const sections = document.querySelectorAll('section[id]');
const navLinks = document.querySelectorAll('.nav-links a');

function highlightNav() {
  let scrollY = window.scrollY;

  sections.forEach(section => {
    const sectionTop = section.offsetTop - 80;
    const sectionHeight = section.offsetHeight;
    const sectionId = section.getAttribute('id');

    if (scrollY >= sectionTop && scrollY < sectionTop + sectionHeight) {
      navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${sectionId}`) {
          link.classList.add('active');
        }
      });
    }
  });
}

window.addEventListener('scroll', highlightNav);

/* ----------------------------------------------------------
   2. Scroll-reveal animation using IntersectionObserver
---------------------------------------------------------- */
const revealElements = document.querySelectorAll(
  '.project-card, .section-title, .about-grid, .skills-list li'
);

const revealObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        revealObserver.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.15 }
);

revealElements.forEach(el => {
  el.classList.add('reveal');
  revealObserver.observe(el);
});

/* ----------------------------------------------------------
   3. Contact form — client-side validation, honeypot spam
      protection, submission, and success animation.
      Sends a POST request to the Flask backend at /contact.
---------------------------------------------------------- */
const contactForm = document.getElementById('contactForm');
const formStatus = document.getElementById('formStatus');
const submitBtn = contactForm ? contactForm.querySelector('button[type="submit"]') : null;

/** Simple email format validator */
function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

/** Display a status message under the contact form */
function setStatus(msg, type = 'info') {
  if (!formStatus) return;
  formStatus.textContent = msg;
  formStatus.className = 'form-status form-status--' + type;
}

/**
 * Show a full success overlay inside the contact section.
 * Fades in a checkmark + message, then auto-hides after 5 s.
 */
function showSuccessAnimation() {
  // Remove any existing overlay
  const old = document.getElementById('successOverlay');
  if (old) old.remove();

  const overlay = document.createElement('div');
  overlay.id = 'successOverlay';
  overlay.className = 'success-overlay';
  overlay.innerHTML = `
    <div class="success-box">
      <div class="success-checkmark">
        <svg viewBox="0 0 52 52" class="checkmark-svg">
          <circle class="checkmark-circle" cx="26" cy="26" r="25" fill="none"/>
          <path  class="checkmark-tick"   fill="none" d="M14 27 l8 8 l16-16"/>
        </svg>
      </div>
      <h3 class="success-title">Message Sent!</h3>
      <p  class="success-msg">Thanks for reaching out, I'll get back to you soon.</p>
      <button class="btn btn-primary success-close" id="successClose">Close</button>
    </div>
  `;

  // Insert after the contact form
  contactForm.parentNode.insertBefore(overlay, contactForm.nextSibling);

  // Trigger animation on next frame
  requestAnimationFrame(() => overlay.classList.add('visible'));

  // Auto-dismiss after 5 s
  const timer = setTimeout(() => dismissSuccess(overlay), 5000);

  document.getElementById('successClose').addEventListener('click', () => {
    clearTimeout(timer);
    dismissSuccess(overlay);
  });
}

function dismissSuccess(overlay) {
  overlay.classList.remove('visible');
  overlay.addEventListener('transitionend', () => overlay.remove(), { once: true });
}

if (contactForm) {
  contactForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const name = document.getElementById('name').value.trim();
    const email = document.getElementById('email').value.trim();
    const message = document.getElementById('message').value.trim();
    // Honeypot — must stay empty; bots fill it, real users don't see it
    const honeypot = document.getElementById('honeypot')?.value || '';

    // ── Client-side validation ──────────────────────────────
    if (!name || !email || !message) {
      setStatus('Please fill in all fields.', 'error');
      return;
    }
    if (!isValidEmail(email)) {
      setStatus('Please enter a valid email address.', 'error');
      return;
    }

    // ── Disable submit button & show loading state ──────────
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.textContent = 'Sending…';
    }
    setStatus('', 'info');

    try {
      const response = await fetch('/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email, message, honeypot }),
      });

      const data = await response.json().catch(() => ({}));

      if (response.ok) {
        contactForm.reset();
        setStatus('', 'info');
        showSuccessAnimation();         // ← success animation
      } else {
        setStatus(data.error || '❌ Something went wrong. Please try again.', 'error');
      }
    } catch (err) {
      console.error('Contact form error:', err);
      setStatus('❌ Network error. Please check your connection.', 'error');
    } finally {
      // Re-enable submit button
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Send Message';
      }
    }
  });
}

/* ----------------------------------------------------------
   4. GitHub API — Repositories & Recent Commits
      Fetches public repos and recent push events for
      Grahambino77 and renders them into the #github section.
---------------------------------------------------------- */

// ── Config ────────────────────────────────────────────────
// Replace 'YOUR_TOKEN_HERE' with a GitHub Personal Access
// Token (read-only / public repos scope) to avoid rate limits.
const GITHUB_TOKEN = '***REMOVED***';
const GITHUB_USERNAME = 'Grahambino77';

/** Shared fetch wrapper — adds auth header when a token is set */
async function ghFetch(url) {
  const headers = { 'Accept': 'application/vnd.github+json' };
  if (GITHUB_TOKEN && GITHUB_TOKEN !== '***REMOVED***') {
    headers['Authorization'] = `Bearer ${GITHUB_TOKEN}`;
  }
  const res = await fetch(url, { headers });
  if (!res.ok) {
    throw new Error(`GitHub API error ${res.status}: ${res.statusText}`);
  }
  return res.json();
}

/** Convert an ISO date string into a relative-time label (e.g. "3 days ago") */
function timeAgo(isoString) {
  const now = Date.now();
  const then = new Date(isoString).getTime();
  const diffSec = Math.floor((now - then) / 1000);

  const table = [
    [60, 'just now', 1],
    [3600, 'minute', 60],
    [86400, 'hour', 3600],
    [604800, 'day', 86400],
    [2592000, 'week', 604800],
    [31536000, 'month', 2592000],
    [Infinity, 'year', 31536000],
  ];

  for (const [limit, label, divisor] of table) {
    if (diffSec < limit) {
      if (label === 'just now') return label;
      const n = Math.floor(diffSec / divisor);
      return `${n} ${label}${n !== 1 ? 's' : ''} ago`;
    }
  }
  return 'a while ago';
}

/** Render an inline error message into a container element */
function renderGhError(container, message) {
  container.innerHTML = `
    <div class="gh-error">
      <span class="gh-error-icon">⚠️</span>
      <span>${message}</span>
    </div>`;
}

// ── Repositories ──────────────────────────────────────────
async function loadGhRepos() {
  const container = document.getElementById('ghRepos');
  if (!container) return;

  try {
    const repos = await ghFetch(
      `https://api.github.com/users/${GITHUB_USERNAME}/repos?sort=updated&per_page=100`
    );

    // Filter: prefer repos with the "portfolio" topic; fall back to top-6 non-forks
    const portfolio = repos.filter(r => Array.isArray(r.topics) && r.topics.includes('portfolio'));
    const toShow = portfolio.length > 0
      ? portfolio
      : repos.filter(r => !r.fork).slice(0, 6);

    if (toShow.length === 0) {
      container.innerHTML = '<p class="gh-loading" style="padding:0">No repositories to display yet.</p>';
      return;
    }

    container.innerHTML = toShow.map(repo => {
      const lang = repo.language || null;
      const desc = repo.description
        ? `<p class="gh-repo-desc">${repo.description}</p>`
        : '<p class="gh-repo-desc" style="font-style:italic;opacity:0.5">No description provided.</p>';

      const langBadge = lang
        ? `<span class="gh-repo-lang">
             <span class="gh-lang-dot" data-lang="${lang}"></span>
             ${lang}
           </span>`
        : '';

      return `
        <div class="gh-repo-card">
          <a class="gh-repo-name" href="${repo.html_url}" target="_blank" rel="noopener noreferrer">
            <span class="gh-repo-name-icon">📁</span>
            ${repo.name}
          </a>
          ${desc}
          <div class="gh-repo-meta">
            ${langBadge}
          </div>
        </div>`;
    }).join('');

  } catch (err) {
    console.error('GitHub repos fetch error:', err);
    renderGhError(container, 'Unable to load repositories right now. Please try again later.');
  }
}

// ── Recent Commits (PushEvents) ───────────────────────────
async function loadGhCommits() {
  const container = document.getElementById('ghCommits');
  if (!container) return;

  try {
    const events = await ghFetch(
      `https://api.github.com/users/${GITHUB_USERNAME}/events/public`
    );

    // Keep only PushEvents and extract up to 10 commits (newest first)
    const commitRows = [];
    for (const event of events) {
      if (event.type !== 'PushEvent') continue;
      const repoName = event.repo?.name ?? 'unknown/repo';
      const repoUrl = `https://github.com/${repoName}`;
      const pushedAt = event.created_at;

      for (const commit of (event.payload?.commits ?? [])) {
        commitRows.push({ message: commit.message, repoName, repoUrl, pushedAt });
        if (commitRows.length >= 10) break;
      }
      if (commitRows.length >= 10) break;
    }

    if (commitRows.length === 0) {
      container.innerHTML = '<p class="gh-loading" style="padding:0">No recent commit activity found.</p>';
      return;
    }

    container.innerHTML = commitRows.map(({ message, repoName, repoUrl, pushedAt }) => {
      // Truncate long commit messages gracefully
      const shortMsg = message.length > 120 ? message.slice(0, 117) + '…' : message;
      // Strip org prefix from repo name for display
      const displayRepo = repoName.includes('/') ? repoName.split('/')[1] : repoName;

      return `
        <div class="gh-commit-item">
          <span class="gh-commit-dot" aria-hidden="true"></span>
          <div class="gh-commit-body">
            <p class="gh-commit-msg">${shortMsg}</p>
            <div class="gh-commit-meta">
              <a class="gh-commit-repo" href="${repoUrl}" target="_blank" rel="noopener noreferrer">${displayRepo}</a>
              <span class="gh-commit-sep">·</span>
              <span>${timeAgo(pushedAt)}</span>
            </div>
          </div>
        </div>`;
    }).join('');

  } catch (err) {
    console.error('GitHub commits fetch error:', err);
    renderGhError(container, 'Unable to load recent commits right now. Please try again later.');
  }
}

// ── Kick off both fetches in parallel ─────────────────────
loadGhRepos();
loadGhCommits();

/* ----------------------------------------------------------
   5. Smooth scroll — adds a small offset to account for
       the sticky header height
---------------------------------------------------------- */
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', (e) => {
    const targetId = anchor.getAttribute('href');
    if (targetId === '#') return;

    const target = document.querySelector(targetId);
    if (target) {
      e.preventDefault();
      const offset = 70;
      const top = target.getBoundingClientRect().top + window.scrollY - offset;
      window.scrollTo({ top, behavior: 'smooth' });
    }
  });
});

/* ----------------------------------------------------------
   6. Scroll-to-top button (injected dynamically)
---------------------------------------------------------- */
const scrollBtn = document.createElement('button');
scrollBtn.id = 'scrollTopBtn';
scrollBtn.innerHTML = '&#8679;';
scrollBtn.title = 'Back to top';
scrollBtn.style.cssText = `
  position: fixed;
  bottom: 32px;
  right: 32px;
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: #e94560;
  color: #fff;
  font-size: 1.4rem;
  border: none;
  cursor: pointer;
  display: none;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 14px rgba(233,69,96,0.45);
  z-index: 999;
  transition: opacity 0.3s ease;
`;
document.body.appendChild(scrollBtn);

window.addEventListener('scroll', () => {
  scrollBtn.style.display = window.scrollY > 400 ? 'flex' : 'none';
});

scrollBtn.addEventListener('click', () => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
});

/* ----------------------------------------------------------
   7. CSS class injected by JS for scroll-reveal transitions
      (styles defined here so no extra CSS file changes needed)
---------------------------------------------------------- */
const revealStyle = document.createElement('style');
revealStyle.textContent = `
  .reveal {
    opacity: 0;
    transform: translateY(24px);
    transition: opacity 0.6s ease, transform 0.6s ease;
  }
  .reveal.visible {
    opacity: 1;
    transform: translateY(0);
  }
  .nav-links a.active {
    color: #e94560;
  }
`;
document.head.appendChild(revealStyle);
