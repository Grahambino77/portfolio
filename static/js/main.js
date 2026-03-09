/* =========================================================
   main.js — Personal Portfolio
   ========================================================= */

'use strict';

/* ----------------------------------------------------------
   1. Active nav-link highlighting on scroll
---------------------------------------------------------- */
const sections    = document.querySelectorAll('section[id]');
const navLinks    = document.querySelectorAll('.nav-links a');

function highlightNav() {
  let scrollY = window.scrollY;

  sections.forEach(section => {
    const sectionTop    = section.offsetTop - 80;
    const sectionHeight = section.offsetHeight;
    const sectionId     = section.getAttribute('id');

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
const formStatus  = document.getElementById('formStatus');
const submitBtn   = contactForm ? contactForm.querySelector('button[type="submit"]') : null;

/** Simple email format validator */
function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

/** Display a status message under the contact form */
function setStatus(msg, type = 'info') {
  if (!formStatus) return;
  formStatus.textContent = msg;
  formStatus.className   = 'form-status form-status--' + type;
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
  overlay.id        = 'successOverlay';
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

    const name     = document.getElementById('name').value.trim();
    const email    = document.getElementById('email').value.trim();
    const message  = document.getElementById('message').value.trim();
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
      submitBtn.disabled    = true;
      submitBtn.textContent = 'Sending…';
    }
    setStatus('', 'info');

    try {
      const response = await fetch('/contact', {
        method : 'POST',
        headers: { 'Content-Type': 'application/json' },
        body   : JSON.stringify({ name, email, message, honeypot }),
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
        submitBtn.disabled    = false;
        submitBtn.textContent = 'Send Message';
      }
    }
  });
}

/* ----------------------------------------------------------
   4. Smooth scroll — adds a small offset to account for
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
      const top    = target.getBoundingClientRect().top + window.scrollY - offset;
      window.scrollTo({ top, behavior: 'smooth' });
    }
  });
});

/* ----------------------------------------------------------
   5. Scroll-to-top button (injected dynamically)
---------------------------------------------------------- */
const scrollBtn = document.createElement('button');
scrollBtn.id        = 'scrollTopBtn';
scrollBtn.innerHTML = '&#8679;';
scrollBtn.title     = 'Back to top';
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
   6. CSS class injected by JS for scroll-reveal transitions
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
