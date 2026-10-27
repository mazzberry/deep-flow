# 🍅 FocusFlow — فوکس‌فلو

A minimal, distraction-free **Pomodoro timer** with a fully **Persian (RTL)** interface, built with Python and PySide6.

FocusFlow stays out of your way: one ring, one button, one keyboard shortcut. Set a focus length and a break length, press **Space**, and let the clock do the rest. When a session ends it rings a synthesized bell, congratulates you, and starts your break automatically.

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)
![PySide6](https://img.shields.io/badge/PySide6-6.6%2B-41CD52?logo=qt&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey)
![UI](https://img.shields.io/badge/UI-Persian%20%7C%20RTL-FF6A1F)

---

## Table of contents

- [Why FocusFlow](#why-focusflow)
- [Features](#features)
- [Preview](#preview)
- [Quick start](#quick-start)
- [Requirements](#requirements)
- [Usage](#usage)
  - [Timer workflow](#timer-workflow)
  - [Keyboard shortcuts](#keyboard-shortcuts)
  - [Changing the durations](#changing-the-durations)
- [How it works](#how-it-works)
  - [State machine](#state-machine)
  - [Timing model](#timing-model)
- [Project structure](#project-structure)
- [Architecture](#architecture)
- [Customization](#customization)
  - [Colors and typography](#colors-and-typography)
  - [Default durations](#default-durations)
  - [Persian fonts](#persian-fonts)
- [Data and persistence](#data-and-persistence)
- [Troubleshooting](#troubleshooting)
- [Development](#development)
  - [Headless smoke test](#headless-smoke-test)
  - [Packaging a standalone binary](#packaging-a-standalone-binary)
- [Known limitations](#known-limitations)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [خلاصه فارسی](#خلاصه-فارسی)

---

## Why FocusFlow

Most Pomodoro apps are dashboards: tasks, tags, charts, accounts, sync. FocusFlow is the opposite — a single small window that answers exactly two questions:

1. *How much time is left?*
2. *Am I focusing or resting?*

Everything is in Persian and laid out right-to-left, with Persian numerals in the countdown so the timer reads naturally at a glance.

---

## Features

- 🍅 **Classic Pomodoro flow** — focus session → automatic break → back to focus.
- ⭕ **Animated circular progress ring** that drains as the session runs out.
- 🎨 **Two-mode color language** — orange while focusing, amber while resting.
- ⌨️ **Spacebar control** — start, pause, and resume without touching the mouse.
- ➕ **In-app duration steppers** — 1–180 minutes for focus, 1–60 minutes for break.
- 💾 **Preferences persist** across launches via `QSettings`.
- 🔔 **Synthesized bell chime** (no bundled audio file) with a system-beep fallback.
- 🧮 **Session counter** for completed focus blocks.
- 🪟 **Modal completion dialogs** that stay on top and re-activate the window.
- 🧭 **Right-to-left layout** with Persian digits and localized labels.
- 🪶 **Zero third-party dependencies** beyond PySide6.
- 🧩 **Small, readable codebase** — ~640 lines across 9 modules.

---

## Preview

```
┌──────────────────────────────────┐
│          🍅  فوکس‌فلو             │
│                                  │
│       ( تمرکز )  ( استراحت )      │
│  ┌────────────────────────────┐  │
│  │                            │  │
│  │         ╭────────╮         │  │
│  │        │  ۲۴:۳۷  │         │  │
│  │        │  تمرکز  │         │  │
│  │         ╰────────╯         │  │
│  │                            │  │
│  │  🍅 جلسه‌های تکمیل‌شده: ۳    │  │
│  └────────────────────────────┘  │
│                                  │
│  ┌────────────────────────────┐  │
│  │           شروع             │  │
│  └────────────────────────────┘  │
│  ┌──────────┐   ┌──────────┐     │
│  │   ریست   │   │ رد کردن  │     │
│  └──────────┘   └──────────┘     │
│  ┌────────────────────────────┐  │
│  │ زمان تمرکز      − ۲۵ +  دقیقه │  │
│  │ زمان استراحت    −  ۵ +  دقیقه │  │
│  └────────────────────────────┘  │
│      کلید فاصله: شروع / توقف      │
└──────────────────────────────────┘
```

> The window is 430 × 760 by default and cannot be shrunk below that, so the ring always has room to breathe.

---

## Quick start

```bash
git clone <repository-url>
cd 1.FoucusFlow

python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
python main.py
```

Or run it as a module:

```bash
python -m focusflow
```

A single-file install works too:

```bash
pip install "PySide6>=6.6"
python main.py
```

---

## Requirements

| Requirement | Version | Notes |
|---|---|---|
| Python | 3.9+ | Developed and verified on Python 3.12.3 |
| PySide6 | 6.6+ | Verified with PySide6 6.11.2 |
| Audio | optional | Provided by `PySide6.QtMultimedia`; falls back to `QApplication.beep()` |
| Display | any | X11, Wayland, Windows, or macOS |

There are no database, network, or account requirements.

---

## Usage

### Timer workflow

1. **Start** — press the big button (or **Space**). The ring begins draining.
2. **Pause / resume** — press again at any time. The remaining time is preserved exactly.
3. **Session ends** — a bell rings, a congratulation dialog appears, and the completed count increments.
4. **Break starts automatically** — accept the dialog and the amber break timer is already running.
5. **Break ends** — a second dialog appears; on confirmation the app returns to an idle focus timer, ready for the next round.
6. **Reset** — returns the current mode to its full duration and stops the clock.
7. **Skip** — jumps straight to the other mode (idle), without counting a session.

> The completion dialog is modal and always-on-top. The bell loops three times and stops when you dismiss the dialog.

### Keyboard shortcuts

| Key | Action |
|---|---|
| `Space` | Start / pause / resume the timer |

The shortcut is registered on the main window, so it works whenever the window has focus and no dialog is open.

### Changing the durations

Use the `−` / `+` steppers in the settings card:

| Setting | Range | Default |
|---|---|---|
| Focus (زمان تمرکز) | 1–180 minutes | 25 |
| Break (زمان استراحت) | 1–60 minutes | 5 |

- Holding a stepper button auto-repeats after 350 ms, then every 80 ms.
- Changes are **saved immediately** and reset the current timer.
- Steppers are **disabled while the timer is running or paused**; the hint *«برای تغییر زمان‌ها، تایمر را ریست کنید.»* appears instead. Reset first to unlock them.

---

## How it works

### State machine

```
                 toggle / Space
   ┌────────┐  ─────────────────▶  ┌──────────┐
   │  Idle  │                        │ Running  │
   │ (full) │  ◀─────────────────    │ (ticking)│
   └────────┘   toggle / Space       └──────────┘
       ▲             (pause)               │
       │                                   │ remaining_ms == 0
       │ reset                             ▼
       │                            ┌──────────────┐
       │                            │  Finished    │
       │                            │ bell + modal │
       │                            └──────────────┘
       │                                   │
       │        break done                 │ focus done
       └───────────────────────────────────┤
                                           ▼
                                    switch to the other
                                    mode (break auto-starts,
                                    focus waits for input)
```

Mode switching is handled by `set_mode()`, which always stops the ticker and reloads the duration for the new mode. Only the transition **focus → break** auto-starts; **break → focus** intentionally waits for the user.

### Timing model

- The ticker fires every **100 ms** (`QTimer`), not every second.
- The end of a session is stored as an absolute `time.monotonic()` deadline, so pause/resume and UI stalls cannot accumulate drift.
- `remaining_ms` is recomputed from the deadline on every tick.
- Displayed seconds are rounded **up** (`(ms + 999) // 1000`), so the timer shows `00:01` until the session is truly over.
- The ring's progress is `remaining_ms / total_ms`, so the arc drains clockwise from the top.

---

## Project structure

```
1.FoucusFlow/
├── main.py                     # Convenience entry point → focusflow.app.run()
├── requirements.txt            # PySide6>=6.6
├── README.md
└── focusflow/
    ├── __init__.py             # Package docstring and __version__
    ├── __main__.py             # Enables `python -m focusflow`
    ├── app.py                  # QApplication bootstrap, RTL + font setup
    ├── window.py               # Main window, UI assembly, timer state machine
    ├── theme.py                # Palette, Persian digits, stylesheet helpers
    ├── storage.py              # AppSettings wrapper around QSettings
    ├── audio.py                # Bell WAV synthesis + QSoundEffect playback
    └── widgets/
        ├── __init__.py         # Public widget exports
        ├── ring.py            # Circular countdown painter
        ├── stepper.py         # −/+ numeric control with auto-repeat
        └── finish_dialog.py   # Modal session-complete dialog
```

---

## Architecture

| Module | Responsibility | Key API |
|---|---|---|
| `focusflow/app.py` | Creates the `QApplication`, forces `RightToLeft`, applies the font stack, shows the window. | `run() -> int` |
| `focusflow/window.py` | Owns all timer state and builds the interface from chips, cards, the ring, buttons, and steppers. | `FocusFlow`, `toggle()`, `reset()`, `skip()`, `tick()`, `finished()` |
| `focusflow/theme.py` | Central design tokens: colors, font list, default durations, Persian digit translation, stylesheet builders. | `fa()`, `darker()`, `app_stylesheet()`, `main_button_style()`, `chip_style()` |
| `focusflow/storage.py` | Persists focus/break minutes under `QSettings("FocusFlow", "FocusFlow")`. | `AppSettings.focus_min`, `.break_min`, `.save()` |
| `focusflow/audio.py` | Synthesizes a 3-second bell from additive sine partials, caches it as WAV, plays it via `QSoundEffect`. | `make_bell_wav()`, `Bell.play()`, `Bell.stop()` |
| `widgets/ring.py` | Custom-painted dual-arc progress ring with the countdown and status text. | `Ring.update_state(progress, color, text, subtext)` |
| `widgets/stepper.py` | Bounded numeric stepper emitting `changed(int)`. | `Stepper(value, lo, hi)`, signal `changed` |
| `widgets/finish_dialog.py` | Themed modal dialog with a single confirmation button. | `FinishDialog(parent, title, message, color)` |

Design choices worth knowing:

- **No `.ui` files.** Every widget is built in Python, which keeps the diff-friendly and dependency-free.
- **Styles are functions, not files.** `theme.py` builds QSS strings so the focus/break accent color can be swapped at runtime.
- **The ring paints itself.** No image assets, no SVG, no animation framework — just `QPainter` and `drawArc`.
- **Audio is generated.** The chime is written to the temp directory on first run, so the repository stays tiny.
- **Graceful audio degradation.** If `QtMultimedia` is unavailable, `HAS_AUDIO` is `False` and the app beeps instead of crashing.

---

## Customization

### Colors and typography

All design tokens live in [`focusflow/theme.py`](focusflow/theme.py):

| Token | Value | Used for |
|---|---|---|
| `BG` | `#FFF7F0` | Warm app background |
| `CARD` | `#FFFFFF` | Timer and settings cards |
| `BORDER` | `#FFE2CF` | Card and button borders |
| `TEXT` | `#2B2118` | Primary text |
| `MUTED` | `#9A8878` | Secondary text, units, hints |
| `TRACK` | `#FFE9DA` | Ring background arc |
| `FOCUS_COLOR` | `#FF6A1F` | Focus mode accent (orange) |
| `BREAK_COLOR` | `#F9A826` | Break mode accent (amber) |

To re-skin the app, change those constants — the stylesheets, ring, chips, dialogs, and main button all derive from them.

### Default durations

```python
# focusflow/theme.py
DEFAULT_FOCUS = 25
DEFAULT_BREAK = 5
```

These only apply on first launch (or after clearing saved settings); persisted user values take precedence.

### Persian fonts

The font stack is tried in order:

```
Vazirmatn → Noto Sans Arabic → Noto Naskh Arabic → DejaVu Sans
```

For the intended look, install [Vazirmatn](https://github.com/rastikerdar/vazirmatn):

```bash
# Debian/Ubuntu (if packaged) or download the TTFs and install locally
mkdir -p ~/.local/share/fonts
cp Vazirmatn-*.ttf ~/.local/share/fonts/
fc-cache -f -v
```

Without it, Qt falls back to any installed Arabic-capable font. Persian text still renders, but metrics and weight will differ slightly. On minimal Linux containers you may see `Failed to compute left/right minimum bearings` warnings — harmless, and fixed by installing a proper Arabic font.

---

## Data and persistence

Only two values are stored: **focus minutes** and **break minutes**.

| Platform | Location |
|---|---|
| Linux | `~/.config/FocusFlow/FocusFlow.conf` |
| Windows | Registry: `HKEY_CURRENT_USER\Software\FocusFlow\FocusFlow` |
| macOS | `~/Library/Preferences/` (Qt-managed plist) |

The bell chime is cached at `<system temp>/focusflow_bell.wav` (for example `/tmp/focusflow_bell.wav`) and regenerated automatically if deleted.

Reset stored preferences on Linux with:

```bash
rm ~/.config/FocusFlow/FocusFlow.conf
```

> The completed-session counter is **in-memory only** and resets when the app closes. Mode and remaining time are not persisted either — every launch starts at a fresh, idle focus timer.

---

## Troubleshooting

| Symptom | Cause / Fix |
|---|---|
| `ModuleNotFoundError: No module named 'PySide6'` | Activate the virtualenv and run `pip install -r requirements.txt`. |
| No sound, but the timer works | `QtMultimedia` is missing or no audio backend is available. The app falls back to the system beep. Install the Qt multimedia extras for your platform / ensure PipeWire or PulseAudio is running. |
| Bell doesn't play on Linux | Check that `libpulse`/PipeWire is reachable and that the temp WAV exists. Delete `/tmp/focusflow_bell.wav` to force regeneration. |
| Persian text looks cramped or uses the wrong font | Install Vazirmatn or Noto Sans Arabic (see [Persian fonts](#persian-fonts)). |
| `qt.qpa.plugin: Could not load the Qt platform plugin "xcb"` | Install the usual Qt 6 X11 libraries, e.g. `sudo apt install libxcb-cursor0 libxkbcommon-x11-0`. |
| Blank/black window on Wayland | Try `QT_QPA_PLATFORM=xcb python main.py`, or update your compositor/Qt build. |
| `Failed to compute left/right minimum bearings` | Font metric warning, not an error. Install a complete Arabic font to silence it. |
| Settings won't change | The steppers are disabled unless the timer is idle. Press **ریست** first. |
| Timer appears to jump | Expected: it is deadline-based and re-syncs to the monotonic clock on each 100 ms tick. |

---

## Development

The project has no packaging metadata or test suite yet; it runs directly from the source tree.

```bash
# Editable-ish workflow: just keep the venv active
source venv/bin/activate
python main.py
```

Conventions used in the codebase:

- `from __future__ import annotations` in every module.
- Type hints on public functions; short docstrings on modules and non-obvious methods.
- Persian user-facing strings live next to the widgets that show them; colors and shared styles live in `theme.py`.
- 4-space indentation, double quotes, ~88-column soft limit.

### Headless smoke test

Useful in CI or over SSH. It isolates settings with a temporary `XDG_CONFIG_HOME` so your real preferences are untouched:

```bash
XDG_CONFIG_HOME=$(mktemp -d) QT_QPA_PLATFORM=offscreen python - <<'PY'
from PySide6.QtWidgets import QApplication
from focusflow.window import FocusFlow

app = QApplication([])
w = FocusFlow()
w.show()
assert w.mode == "focus" and w.idle
assert w.total_ms == w.focus_min * 60_000

w.toggle()
assert w.running
w.toggle()
assert not w.running and not w.idle   # paused

w.reset()
assert w.idle

w.skip()
assert w.mode == "break" and w.idle
print("FocusFlow smoke test passed")
PY
```

### Packaging a standalone binary

PyInstaller can bundle the app; Qt multimedia plugins often need explicit collection:

```bash
pip install pyinstaller
pyinstaller --noconfirm --windowed --name FocusFlow \
    --collect-all PySide6 main.py
```

The result appears in `dist/FocusFlow/`. Test audio on the target OS, since codec/plugin bundling differs per platform.

---

## Known limitations

- The completed-session counter is not persisted.
- No system-tray icon, desktop notifications, or global (out-of-focus) hotkeys.
- No long-break cycle (e.g. 4 × 25 min → 15 min), task list, or statistics.
- Only one keyboard shortcut; durations cannot be typed directly.
- No automated tests, CI, or published package yet.
- Changing a duration always resets the current timer instead of applying at the next session.

---

## Roadmap

- [ ] Persist the completed-session counter and daily history
- [ ] Optional long-break cycle with configurable interval
- [ ] System-tray mode with minimize-to-tray
- [ ] Desktop notifications as an alternative to the modal dialog
- [ ] Editable duration fields (keyboard input)
- [ ] `pytest` + `pytest-qt` suite covering the state machine
- [ ] `pyproject.toml` and a `focusflow` console script
- [ ] Theme switch (light / dark / high contrast)

---

## Contributing

1. Fork the repository and create a branch: `git switch -c feature/long-breaks`.
2. Keep changes focused and match the existing module layout.
3. Verify the headless smoke test above still passes.
4. If you touch UI, check both focus and break modes, plus the paused and finished states.
5. Open a pull request describing the behavior change and, ideally, a screenshot.

Bug reports are most useful with: OS, Python version, PySide6 version, the exact command used, and any Qt warnings printed on startup.

> **Before your first commit:** this repository currently has no `.gitignore`, and `venv/` plus `__pycache__/` are untracked. Add them to `.gitignore` so the 600+ MB virtualenv never lands in history.

---

## License

No license file is included yet. Until one is added, the code is **all rights reserved** and cannot be reused, modified, or redistributed without the author's permission. If you intend to publish this project, add a `LICENSE` file (MIT is a good fit for a small desktop utility) and update this section.

---

## خلاصه فارسی

**فوکس‌فلو** یک تایمر پومودورو ساده و فارسی است که با Python و PySide6 ساخته شده است.

- اجرا: `pip install -r requirements.txt` سپس `python main.py` (یا `python -m focusflow`)
- کلید **فاصله** تایمر را شروع، متوقف یا ادامه می‌دهد.
- زمان تمرکز پیش‌فرض ۲۵ دقیقه و زمان استراحت ۵ دقیقه است و هر دو قابل تغییرند (تمرکز ۱ تا ۱۸۰، استراحت ۱ تا ۶۰ دقیقه).
- پس از پایان تمرکز، زنگ پخش می‌شود، گفت‌وگوی تبریک نمایش داده می‌شود و استراحت به‌صورت خودکار آغاز می‌گردد.
- تنظیمات زمان‌ها در `QSettings` ذخیره می‌شود؛ شمارندهٔ جلسه‌ها فقط تا زمان اجرای برنامه نگه داشته می‌شود.
- برای ظاهر بهتر، قلم **وزیرمتن** را نصب کنید.
