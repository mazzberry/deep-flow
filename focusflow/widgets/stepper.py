"""Minus/plus numeric stepper widget."""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget

from ..theme import fa


class Stepper(QWidget):
    changed = Signal(int)

    def __init__(self, value: int, lo: int, hi: int) -> None:
        super().__init__()
        self.value, self.lo, self.hi = value, lo, hi
        self.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        self.minus = QPushButton("−")
        self.plus = QPushButton("+")
        self.label = QLabel(fa(value))
        self.label.setObjectName("stepValue")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setFixedWidth(48)

        for button, delta in ((self.minus, -1), (self.plus, 1)):
            button.setObjectName("step")
            button.setFixedSize(36, 36)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.setAutoRepeat(True)
            button.setAutoRepeatDelay(350)
            button.setAutoRepeatInterval(80)
            button.clicked.connect(lambda _=False, d=delta: self.add(d))

        layout.addWidget(self.minus)
        layout.addWidget(self.label)
        layout.addWidget(self.plus)

    def add(self, delta: int) -> None:
        new_value = max(self.lo, min(self.hi, self.value + delta))
        if new_value != self.value:
            self.value = new_value
            self.label.setText(fa(new_value))
            self.changed.emit(new_value)
