"""Persistent user preferences backed by QSettings."""

from __future__ import annotations

from PySide6.QtCore import QSettings

from .theme import DEFAULT_BREAK, DEFAULT_FOCUS


class AppSettings:
    """Thin wrapper around QSettings for the values FocusFlow persists."""

    def __init__(self) -> None:
        self._settings = QSettings("FocusFlow", "FocusFlow")

    @property
    def focus_min(self) -> int:
        return int(self._settings.value("focus_min", DEFAULT_FOCUS))

    @property
    def break_min(self) -> int:
        return int(self._settings.value("break_min", DEFAULT_BREAK))

    def save(self, focus_min: int, break_min: int) -> None:
        self._settings.setValue("focus_min", focus_min)
        self._settings.setValue("break_min", break_min)
