"""Application bootstrap."""

from __future__ import annotations

import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication

from .theme import FONTS
from .window import FocusFlow


def run() -> int:
    """Create the Qt application, show the window and enter the event loop."""
    app = QApplication(sys.argv)
    app.setApplicationName("FocusFlow")
    app.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
    app.setFont(QFont(FONTS, 11))
    window = FocusFlow()
    window.show()
    return app.exec()
