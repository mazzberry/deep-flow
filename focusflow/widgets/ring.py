"""Circular countdown progress indicator."""

from __future__ import annotations

from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QColor, QFont, QPainter, QPen
from PySide6.QtWidgets import QWidget

from ..theme import FOCUS_COLOR, TEXT, TRACK


class Ring(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.progress = 1.0
        self.color = QColor(FOCUS_COLOR)
        self.text = ""
        self.subtext = ""
        self.setMinimumSize(260, 260)

    def update_state(self, progress: float, color: str, text: str, subtext: str) -> None:
        self.progress, self.color = progress, QColor(color)
        self.text, self.subtext = text, subtext
        self.update()

    def paintEvent(self, _event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        side = min(self.width(), self.height())
        pen_w = 16
        margin = pen_w + 4
        rect = QRectF((self.width() - side) / 2 + margin,
                      (self.height() - side) / 2 + margin,
                      side - 2 * margin, side - 2 * margin)

        track = QPen(QColor(TRACK), pen_w)
        track.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(track)
        painter.drawArc(rect, 0, 360 * 16)

        if self.progress > 0:
            pen = QPen(self.color, pen_w)
            pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)
            painter.drawArc(rect, 90 * 16, int(-self.progress * 360 * 16))

        painter.setPen(QColor(TEXT))
        font = QFont()
        font.setPointSize(44)
        font.setWeight(QFont.Weight.Bold)
        painter.setFont(font)
        painter.drawText(rect.adjusted(0, -14, 0, -14), Qt.AlignmentFlag.AlignCenter,
                         "\u200e" + self.text + "\u200e")

        painter.setPen(self.color)
        sub_font = QFont()
        sub_font.setPointSize(12)
        sub_font.setWeight(QFont.Weight.DemiBold)
        painter.setFont(sub_font)
        painter.drawText(rect.adjusted(0, 66, 0, 66), Qt.AlignmentFlag.AlignCenter,
                         self.subtext)
