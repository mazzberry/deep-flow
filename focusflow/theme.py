"""Colors, fonts and shared style helpers for FocusFlow."""

from __future__ import annotations

# ----- Palette -----
BG = "#FFF7F0"             # warm white background
CARD = "#FFFFFF"
BORDER = "#FFE2CF"
TEXT = "#2B2118"
MUTED = "#9A8878"
TRACK = "#FFE9DA"
FOCUS_COLOR = "#FF6A1F"    # orange
BREAK_COLOR = "#F9A826"    # amber

HOVER_BG = "#FFF0E5"
STEP_BG = "#FFF0E5"
STEP_HOVER_BG = "#FFE0CA"
STEP_DISABLED_BG = "#F5EFEA"
STEP_DISABLED_TEXT = "#CFC4BA"

FONTS = ["Vazirmatn", "Noto Sans Arabic", "Noto Naskh Arabic", "DejaVu Sans"]

DEFAULT_FOCUS = 25
DEFAULT_BREAK = 5

_FA_DIGITS = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")


def fa(value) -> str:
    """Convert ASCII digits in *value* to Persian digits."""
    return str(value).translate(_FA_DIGITS)


def darker(color: str, factor: int = 112) -> str:
    """Return a hex color darkened by *factor* percent."""
    from PySide6.QtGui import QColor

    return QColor(color).darker(factor).name()


def app_stylesheet() -> str:
    """Stylesheet applied to the main window root widget."""
    return f"""
        QWidget#root {{ background: {BG}; }}
        QLabel {{ background: transparent; color: {TEXT}; }}
        QFrame#card {{ background: {CARD}; border: 1px solid {BORDER};
                       border-radius: 24px; }}
        QLabel#appTitle {{ font-size: 22px; font-weight: 800; color: {FOCUS_COLOR}; }}
        QLabel#count {{ color: {MUTED}; font-size: 14px; }}
        QLabel#rowLabel {{ font-size: 14px; font-weight: 600; }}
        QLabel#unit {{ color: {MUTED}; font-size: 13px; }}
        QLabel#stepValue {{ font-size: 18px; font-weight: 800; }}
        QLabel#note {{ color: {MUTED}; font-size: 12px; }}
        QPushButton#secondary {{
            background: {CARD}; color: {TEXT}; border: 1px solid {BORDER};
            border-radius: 14px; padding: 13px 22px;
            font-size: 14px; font-weight: 600; }}
        QPushButton#secondary:hover {{ background: {HOVER_BG}; }}
        QPushButton#step {{
            background: {STEP_BG}; color: {FOCUS_COLOR}; border: none;
            border-radius: 18px; font-size: 20px; font-weight: 800; }}
        QPushButton#step:hover {{ background: {STEP_HOVER_BG}; }}
        QPushButton#step:disabled {{ background: {STEP_DISABLED_BG};
                                     color: {STEP_DISABLED_TEXT}; }}
    """


def main_button_style(color: str) -> str:
    return f"""
        QPushButton {{ background: {color}; color: white; border: none;
                       border-radius: 18px; font-size: 18px; font-weight: 800; }}
        QPushButton:hover {{ background: {darker(color)}; }}
    """


def chip_style(color: str, active: bool) -> str:
    if active:
        return (f"padding:8px 22px; border-radius:17px; font-size:13px; "
                f"font-weight:700; background:{color}; color:white; "
                f"border:1px solid {color};")
    return (f"padding:8px 22px; border-radius:17px; font-size:13px; "
            f"font-weight:600; background:{CARD}; color:{MUTED}; "
            f"border:1px solid {BORDER};")
