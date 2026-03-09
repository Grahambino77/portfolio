"""
countdown_app.py — Countdown Timer Desktop Application
Built with Python + Tkinter

Run from the project root:
    python backend/countdown_app.py

Features:
- Hours / Minutes / Seconds inputs
- Start, Pause/Resume, Reset controls
- Real-time countdown display with color feedback
- Animated progress bar
- Quick-preset buttons (5 min, 10 min, 25 min, etc.)
- Plays frog.mp3 three times when the timer reaches zero
- Multithreaded — UI stays responsive during countdown
"""

import os
import time
import threading
import ctypes
import tkinter as tk
from tkinter import ttk, font as tkfont

# ---------------------------------------------------------------------------
# Path helpers
# ---------------------------------------------------------------------------
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR    = os.path.dirname(BACKEND_DIR)
SOUND_FILE  = os.path.join(ROOT_DIR, "static", "sounds", "frog.mp3")

# ---------------------------------------------------------------------------
# Sound playback (Windows built-in — no extra packages needed)
# Uses the Windows MCI (Media Control Interface) via ctypes
# ---------------------------------------------------------------------------

def _play_mp3_once(path: str) -> None:
    """Play an MP3 file synchronously using the Windows MCI interface."""
    winmm = ctypes.windll.winmm
    alias = "countdown_alert"
    winmm.mciSendStringW(f'open "{path}" type mpegvideo alias {alias}', None, 0, None)
    winmm.mciSendStringW(f'play {alias} wait', None, 0, None)
    winmm.mciSendStringW(f'close {alias}', None, 0, None)


def play_alert_sound(path: str, times: int = 3) -> None:
    """Play the alert sound `times` times in a background thread."""
    def _worker():
        for _ in range(times):
            try:
                _play_mp3_once(path)
            except Exception as e:
                print(f"[Sound] Could not play audio: {e}")
    threading.Thread(target=_worker, daemon=True).start()


# ---------------------------------------------------------------------------
# Colour palette (matches the portfolio dark theme)
# ---------------------------------------------------------------------------
BG         = "#0f0f0f"
SURFACE    = "#1a1a2e"
ACCENT     = "#e94560"
ACCENT2    = "#0f3460"
TEXT       = "#e0e0e0"
MUTED      = "#a0a0b0"
WHITE      = "#ffffff"
GREEN      = "#4caf50"
CARD_BG    = "#16213e"


# ---------------------------------------------------------------------------
# Helper — format total seconds → "HH:MM:SS"
# ---------------------------------------------------------------------------
def fmt(secs: int) -> str:
    h, rem = divmod(abs(secs), 3600)
    m, s   = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


# ---------------------------------------------------------------------------
# Main application class
# ---------------------------------------------------------------------------
class CountdownApp(tk.Tk):

    PRESETS = [
        ("1 min",  60),
        ("5 min",  300),
        ("10 min", 600),
        ("15 min", 900),
        ("25 min", 1500),
        ("30 min", 1800),
        ("1 hr",   3600),
    ]

    def __init__(self):
        super().__init__()

        self.title("⏱  Countdown Timer — Andrew Graham")
        self.configure(bg=BG)
        self.resizable(False, False)

        # Centre window on screen
        w, h = 540, 560
        sx, sy = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"{w}x{h}+{(sx - w)//2}+{(sy - h)//2}")

        # State
        self._total    = 0      # original duration for progress %
        self._remaining = 0     # seconds left
        self._running  = False
        self._thread   = None

        self._build_ui()
        self._update_display()

    # ── UI construction ──────────────────────────────────────────────────────

    def _build_ui(self):
        outer = tk.Frame(self, bg=BG, padx=24, pady=24)
        outer.pack(fill="both", expand=True)

        # ── Title ────────────────────────────────────────────────────────────
        title_font = tkfont.Font(family="Segoe UI", size=20, weight="bold")
        tk.Label(
            outer, text="⏱  Countdown Timer",
            font=title_font, bg=BG, fg=ACCENT
        ).pack(pady=(0, 4))

        tk.Label(
            outer, text="Set hours, minutes & seconds — then start.",
            font=("Segoe UI", 10), bg=BG, fg=MUTED
        ).pack(pady=(0, 20))

        # ── Input card ───────────────────────────────────────────────────────
        card = tk.Frame(outer, bg=SURFACE, padx=20, pady=20)
        card.pack(fill="x", pady=(0, 16))

        input_frame = tk.Frame(card, bg=SURFACE)
        input_frame.pack()

        lbl_font  = ("Segoe UI", 9)
        inp_font  = ("Segoe UI", 28, "bold")
        colon_font = ("Segoe UI", 26, "bold")

        def make_field(parent, label_text, var, col):
            f = tk.Frame(parent, bg=SURFACE)
            f.grid(row=0, column=col, padx=4)
            tk.Label(f, text=label_text, font=lbl_font, bg=SURFACE, fg=MUTED).pack()
            tk.Spinbox(
                f, from_=0, to=99 if label_text == "Hours" else 59,
                textvariable=var, font=inp_font, width=3,
                bg=CARD_BG, fg=WHITE, insertbackground=WHITE,
                buttonbackground=ACCENT2, relief="flat",
                justify="center",
                command=self._on_input_change
            ).pack()
            var.trace_add("write", lambda *_: self._on_input_change())

        self._var_h = tk.StringVar(value="0")
        self._var_m = tk.StringVar(value="5")
        self._var_s = tk.StringVar(value="0")

        make_field(input_frame, "Hours",   self._var_h, 0)
        tk.Label(input_frame, text=":", font=colon_font, bg=SURFACE, fg=MUTED).grid(row=0, column=1)
        make_field(input_frame, "Minutes", self._var_m, 2)
        tk.Label(input_frame, text=":", font=colon_font, bg=SURFACE, fg=MUTED).grid(row=0, column=3)
        make_field(input_frame, "Seconds", self._var_s, 4)

        # ── Countdown display ─────────────────────────────────────────────────
        self._display_font = tkfont.Font(family="Segoe UI", size=52, weight="bold")
        self._display_lbl  = tk.Label(
            outer, text="00:05:00",
            font=self._display_font,
            bg=BG, fg=TEXT
        )
        self._display_lbl.pack(pady=(4, 6))

        # ── Progress bar ──────────────────────────────────────────────────────
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure(
            "Custom.Horizontal.TProgressbar",
            troughcolor=SURFACE,
            background=ACCENT,
            bordercolor=BG,
            lightcolor=ACCENT,
            darkcolor=ACCENT2,
        )
        self._progress = ttk.Progressbar(
            outer, style="Custom.Horizontal.TProgressbar",
            orient="horizontal", length=480, mode="determinate",
            maximum=100, value=100
        )
        self._progress.pack(pady=(0, 6))

        # ── Status label ──────────────────────────────────────────────────────
        self._status_lbl = tk.Label(
            outer, text="READY",
            font=("Segoe UI", 10), bg=BG, fg=MUTED
        )
        self._status_lbl.pack(pady=(0, 16))

        # ── Control buttons ───────────────────────────────────────────────────
        btn_frame = tk.Frame(outer, bg=BG)
        btn_frame.pack(pady=(0, 16))

        btn_cfg = dict(font=("Segoe UI", 11, "bold"), relief="flat",
                       padx=20, pady=8, cursor="hand2", bd=0)

        self._btn_start = tk.Button(
            btn_frame, text="▶  Start",
            bg=GREEN, fg=WHITE, activebackground="#45a049",
            command=self._on_start, **btn_cfg
        )
        self._btn_start.grid(row=0, column=0, padx=6)

        self._btn_pause = tk.Button(
            btn_frame, text="⏸  Pause",
            bg=ACCENT, fg=WHITE, activebackground="#c73652",
            command=self._on_pause, state="disabled", **btn_cfg
        )
        self._btn_pause.grid(row=0, column=1, padx=6)

        self._btn_reset = tk.Button(
            btn_frame, text="↺  Reset",
            bg=SURFACE, fg=MUTED, activebackground=CARD_BG,
            command=self._on_reset, **btn_cfg
        )
        self._btn_reset.grid(row=0, column=2, padx=6)

        # ── Preset buttons ────────────────────────────────────────────────────
        tk.Label(
            outer, text="QUICK PRESETS",
            font=("Segoe UI", 8), bg=BG, fg=MUTED
        ).pack(pady=(0, 6))

        preset_frame = tk.Frame(outer, bg=BG)
        preset_frame.pack()

        for i, (label, secs) in enumerate(self.PRESETS):
            tk.Button(
                preset_frame, text=label,
                font=("Segoe UI", 9), relief="flat",
                bg=ACCENT2, fg=TEXT,
                activebackground=ACCENT, activeforeground=WHITE,
                padx=10, pady=4, cursor="hand2",
                command=lambda s=secs: self._apply_preset(s)
            ).grid(row=0, column=i, padx=4)

    # ── Preset handler ────────────────────────────────────────────────────────

    def _apply_preset(self, seconds: int):
        if self._running:
            return
        self._remaining = 0          # flag: not mid-run
        self._total     = 0
        h, rem = divmod(seconds, 3600)
        m, s   = divmod(rem, 60)
        self._var_h.set(str(h))
        self._var_m.set(str(m))
        self._var_s.set(str(s))
        self._display_lbl.config(text=fmt(seconds), fg=TEXT)
        self._progress["value"] = 100
        self._status_lbl.config(text="READY", fg=MUTED)
        self._btn_start.config(text="▶  Start", state="normal")
        self._btn_pause.config(state="disabled")

    # ── Input change (sync display while user types) ──────────────────────────

    def _on_input_change(self):
        if not self._running and self._remaining == 0:
            try:
                secs = self._read_inputs()
                self._display_lbl.config(text=fmt(secs), fg=TEXT)
                self._progress["value"] = 100
            except ValueError:
                pass

    def _read_inputs(self) -> int:
        h = int(self._var_h.get() or 0)
        m = int(self._var_m.get() or 0)
        s = int(self._var_s.get() or 0)
        return h * 3600 + m * 60 + s

    # ── Start ─────────────────────────────────────────────────────────────────

    def _on_start(self):
        if self._running:
            return

        if self._remaining == 0:
            # Fresh start — read the inputs
            try:
                self._remaining = self._read_inputs()
                self._total     = self._remaining
            except ValueError:
                self._status_lbl.config(text="Invalid input.", fg=ACCENT)
                return

        if self._remaining <= 0:
            self._status_lbl.config(text="Set a time greater than 0.", fg=ACCENT)
            return

        self._running = True
        self._set_inputs_state("disabled")
        self._btn_start.config(state="disabled")
        self._btn_pause.config(state="normal")
        self._status_lbl.config(text="RUNNING…", fg=GREEN)
        self._display_lbl.config(fg=GREEN)

        # Spin up the countdown thread
        self._thread = threading.Thread(target=self._tick_loop, daemon=True)
        self._thread.start()

    # ── Countdown loop (runs in background thread) ────────────────────────────

    def _tick_loop(self):
        while self._running and self._remaining > 0:
            time.sleep(1)
            if self._running:         # check again after sleep
                self._remaining -= 1
                self.after(0, self._update_display)

        if self._running:             # naturally reached zero (not reset)
            self._running = False
            self.after(0, self._on_done)

    # ── Update display (called on main thread via after()) ────────────────────

    def _update_display(self):
        self._display_lbl.config(text=fmt(self._remaining))
        pct = (self._remaining / self._total * 100) if self._total > 0 else 100
        self._progress["value"] = pct

    # ── Done ──────────────────────────────────────────────────────────────────

    def _on_done(self):
        self._remaining = 0
        self._display_lbl.config(text="00:00:00", fg=ACCENT)
        self._progress["value"] = 0
        self._status_lbl.config(text="⏰  TIME'S UP!", fg=ACCENT)
        self._btn_start.config(state="disabled")
        self._btn_pause.config(state="disabled")
        self._set_inputs_state("normal")

        # Flash the display 3 times, then play the alert sound
        self._flash(6)
        play_alert_sound(SOUND_FILE, times=3)

    def _flash(self, count: int):
        """Alternate display colour to draw attention (called recursively)."""
        if count <= 0:
            self._display_lbl.config(fg=ACCENT)
            return
        colour = BG if count % 2 == 0 else ACCENT
        self._display_lbl.config(fg=colour)
        self.after(400, lambda: self._flash(count - 1))

    # ── Pause / Resume ────────────────────────────────────────────────────────

    def _on_pause(self):
        if self._running:
            self._running = False
            self._btn_start.config(text="▶  Resume", state="normal")
            self._btn_pause.config(state="disabled")
            self._display_lbl.config(fg=ACCENT)
            self._status_lbl.config(text="PAUSED", fg=ACCENT)

    # ── Reset ─────────────────────────────────────────────────────────────────

    def _on_reset(self):
        self._running   = False
        self._remaining = 0
        self._total     = 0

        self._var_h.set("0")
        self._var_m.set("5")
        self._var_s.set("0")

        self._display_lbl.config(text="00:05:00", fg=TEXT)
        self._progress["value"] = 100
        self._status_lbl.config(text="READY", fg=MUTED)
        self._btn_start.config(text="▶  Start", state="normal")
        self._btn_pause.config(state="disabled")
        self._set_inputs_state("normal")

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _set_inputs_state(self, state: str):
        """Enable or disable all Spinbox widgets."""
        for widget in self.winfo_children():
            self._set_children_state(widget, state)

    def _set_children_state(self, parent, state):
        for child in parent.winfo_children():
            if isinstance(child, tk.Spinbox):
                child.config(state=state)
            self._set_children_state(child, state)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    app = CountdownApp()
    app.mainloop()
