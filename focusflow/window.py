"""The main FocusFlow window and its timer state machine."""

from __future__ import annotations

import time

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget,
)

from . import theme
from .audio import Bell
from .storage import AppSettings
from .widgets import FinishDialog, Ring, Stepper


class FocusFlow(QWidget):
    FOCUS, BREAK = "focus", "break"

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("root")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setWindowTitle("فوکس‌فلو")
        self.setMinimumSize(430, 760)

        self.settings = AppSettings()
        self.focus_min = self.settings.focus_min
        self.break_min = self.settings.break_min

        self.mode = self.FOCUS
        self.running = False
        self.completed = 0
        self.total_ms = self.focus_min * 60_000
        self.remaining_ms = self.total_ms
        self.end_time = 0.0

        self.ticker = QTimer(self)
        self.ticker.setInterval(100)
        self.ticker.timeout.connect(self.tick)

        self.bell = Bell(self)

        self.build_ui()
        self.refresh()
        QShortcut(QKeySequence(Qt.Key.Key_Space), self, activated=self.toggle)

    # ---------- UI ----------
    def build_ui(self) -> None:
        self.setStyleSheet(theme.app_stylesheet())

        root = QVBoxLayout(self)
        root.setContentsMargins(26, 22, 26, 20)
        root.setSpacing(14)

        title = QLabel("🍅  فوکس‌فلو")
        title.setObjectName("appTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addWidget(title)

        root.addLayout(self.build_chips())
        root.addWidget(self.build_timer_card(), 1)
        root.addWidget(self.build_main_button())
        root.addLayout(self.build_action_row())
        root.addWidget(self.build_settings_card())

        hint = QLabel("کلید فاصله: شروع / توقف")
        hint.setObjectName("note")
        hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addWidget(hint)

    def build_chips(self) -> QHBoxLayout:
        chips = QHBoxLayout()
        chips.setSpacing(10)
        chips.addStretch()
        self.chip_focus = QLabel("تمرکز")
        self.chip_break = QLabel("استراحت")
        for chip in (self.chip_focus, self.chip_break):
            chip.setAlignment(Qt.AlignmentFlag.AlignCenter)
            chips.addWidget(chip)
        chips.addStretch()
        return chips

    def build_timer_card(self) -> QFrame:
        card = QFrame()
        card.setObjectName("card")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(16, 16, 16, 12)

        self.ring = Ring()
        layout.addWidget(self.ring, 1)

        self.count_label = QLabel()
        self.count_label.setObjectName("count")
        self.count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.count_label)
        return card

    def build_main_button(self) -> QPushButton:
        self.main_btn = QPushButton()
        self.main_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.main_btn.setMinimumHeight(56)
        self.main_btn.clicked.connect(self.toggle)
        return self.main_btn

    def build_action_row(self) -> QHBoxLayout:
        row = QHBoxLayout()
        row.setSpacing(12)
        self.reset_btn = QPushButton("ریست")
        self.skip_btn = QPushButton("رد کردن")
        for button in (self.reset_btn, self.skip_btn):
            button.setObjectName("secondary")
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            row.addWidget(button)
        self.reset_btn.clicked.connect(self.reset)
        self.skip_btn.clicked.connect(self.skip)
        return row

    def build_settings_card(self) -> QFrame:
        card = QFrame()
        card.setObjectName("card")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 14, 20, 12)
        layout.setSpacing(10)

        self.focus_step = Stepper(self.focus_min, 1, 180)
        self.break_step = Stepper(self.break_min, 1, 60)
        self.focus_step.changed.connect(self.on_setting_changed)
        self.break_step.changed.connect(self.on_setting_changed)
        layout.addLayout(self.setting_row("زمان تمرکز", self.focus_step))
        layout.addLayout(self.setting_row("زمان استراحت", self.break_step))

        self.note = QLabel("برای تغییر زمان‌ها، تایمر را ریست کنید.")
        self.note.setObjectName("note")
        self.note.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.note)
        return card

    @staticmethod
    def setting_row(text: str, stepper: Stepper) -> QHBoxLayout:
        row = QHBoxLayout()
        label = QLabel(text)
        label.setObjectName("rowLabel")
        unit = QLabel("دقیقه")
        unit.setObjectName("unit")
        row.addWidget(label)
        row.addStretch()
        row.addWidget(stepper)
        row.addWidget(unit)
        return row

    # ---------- State ----------
    @property
    def color(self) -> str:
        return theme.FOCUS_COLOR if self.mode == self.FOCUS else theme.BREAK_COLOR

    @property
    def idle(self) -> bool:
        return (not self.running) and self.remaining_ms == self.total_ms

    def set_mode(self, mode: str) -> None:
        self.mode = mode
        minutes = self.focus_min if mode == self.FOCUS else self.break_min
        self.total_ms = minutes * 60_000
        self.remaining_ms = self.total_ms
        self.running = False
        self.ticker.stop()
        self.refresh()

    def on_setting_changed(self, _value=None) -> None:
        self.focus_min = self.focus_step.value
        self.break_min = self.break_step.value
        self.settings.save(self.focus_min, self.break_min)
        self.set_mode(self.mode)

    def refresh(self) -> None:
        secs = (self.remaining_ms + 999) // 1000
        text = f"{theme.fa(f'{secs // 60:02d}')}:{theme.fa(f'{secs % 60:02d}')}"
        progress = self.remaining_ms / self.total_ms if self.total_ms else 0
        label = "تمرکز" if self.mode == self.FOCUS else "استراحت"
        if self.running:
            sub = label
        elif self.idle:
            sub = f"آماده · {label}"
        else:
            sub = f"متوقف · {label}"
        self.ring.update_state(progress, self.color, text, sub)

        self.setWindowTitle(f"{text} · فوکس‌فلو")
        self.count_label.setText(f"🍅 جلسه‌های تکمیل‌شده: {theme.fa(self.completed)}")

        self.chip_focus.setStyleSheet(
            theme.chip_style(self.color, self.mode == self.FOCUS))
        self.chip_break.setStyleSheet(
            theme.chip_style(self.color, self.mode == self.BREAK))

        if self.running:
            self.main_btn.setText("توقف")
        elif self.idle:
            self.main_btn.setText("شروع")
        else:
            self.main_btn.setText("ادامه")
        self.main_btn.setStyleSheet(theme.main_button_style(self.color))

        can_edit = self.idle
        self.focus_step.setEnabled(can_edit)
        self.break_step.setEnabled(can_edit)
        self.note.setVisible(not can_edit)

    # ---------- Actions ----------
    def toggle(self) -> None:
        if self.running:
            self.running = False
            self.ticker.stop()
        else:
            self.running = True
            self.end_time = time.monotonic() + self.remaining_ms / 1000
            self.ticker.start()
        self.refresh()

    def reset(self) -> None:
        self.set_mode(self.mode)

    def skip(self) -> None:
        self.set_mode(self.BREAK if self.mode == self.FOCUS else self.FOCUS)

    def tick(self) -> None:
        self.remaining_ms = max(0, int((self.end_time - time.monotonic()) * 1000))
        self.refresh()
        if self.remaining_ms <= 0:
            self.finished()

    def finished(self) -> None:
        self.ticker.stop()
        self.running = False
        self.remaining_ms = 0
        self.refresh()
        self.bell.play()
        self.raise_()
        self.activateWindow()

        if self.mode == self.FOCUS:
            self.completed += 1
            FinishDialog(
                self, "جلسه تمرکز تمام شد 🎉",
                f"آفرین! وقت یک استراحت {theme.fa(self.break_min)} دقیقه‌ای است.",
                theme.FOCUS_COLOR,
            ).exec()
            self.bell.stop()
            self.set_mode(self.BREAK)
            self.toggle()  # break starts automatically
        else:
            FinishDialog(
                self, "استراحت تمام شد ☕",
                "آماده‌ای برای یک جلسه تمرکز دیگر؟",
                theme.BREAK_COLOR,
            ).exec()
            self.bell.stop()
            self.set_mode(self.FOCUS)
