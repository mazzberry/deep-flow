"""Modal dialog shown when a focus/break session ends."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout

from ..theme import CARD, TEXT, darker


class FinishDialog(QDialog):
    def __init__(self, parent, title: str, message: str, color: str) -> None:
        super().__init__(parent)
        self.setWindowTitle("فوکس‌فلو")
        self.setModal(True)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
        self.setMinimumWidth(360)
        self.setStyleSheet(f"""
            QDialog {{ background: {CARD}; }}
            QLabel {{ background: transparent; }}
            QLabel#title {{ color: {color}; font-size: 20px; font-weight: 700; }}
            QLabel#msg {{ color: {TEXT}; font-size: 14px; }}
            QPushButton {{ background: {color}; color: white; border: none;
                           border-radius: 14px; padding: 12px 28px;
                           font-size: 15px; font-weight: 700; }}
            QPushButton:hover {{ background: {darker(color)}; }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 28, 30, 24)
        layout.setSpacing(12)

        title_label = QLabel(title)
        title_label.setObjectName("title")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        message_label = QLabel(message)
        message_label.setObjectName("msg")
        message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        message_label.setWordWrap(True)

        ok = QPushButton("تأیید")
        ok.setCursor(Qt.CursorShape.PointingHandCursor)
        ok.setDefault(True)
        ok.clicked.connect(self.accept)

        layout.addWidget(title_label)
        layout.addWidget(message_label)
        layout.addSpacing(8)
        layout.addWidget(ok)
