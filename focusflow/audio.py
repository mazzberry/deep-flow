"""Bell chime generation and playback."""

from __future__ import annotations

import math
import struct
import tempfile
import wave
from pathlib import Path

from PySide6.QtCore import QObject, QUrl
from PySide6.QtWidgets import QApplication

try:
    from PySide6.QtMultimedia import QSoundEffect

    HAS_AUDIO = True
except ImportError:
    HAS_AUDIO = False


def make_bell_wav() -> Path:
    """Generate (once) and return the path to a bell chime WAV file."""
    path = Path(tempfile.gettempdir()) / "focusflow_bell.wav"
    if path.exists():
        return path

    rate, duration, base = 44100, 3.0, 660.0
    partials = [(1.0, 1.00, 1.6), (2.0, 0.60, 2.0), (2.76, 0.45, 2.6),
                (5.4, 0.25, 3.5), (8.93, 0.12, 5.0)]
    frames = bytearray()
    for i in range(int(rate * duration)):
        t = i / rate
        sample = sum(a * math.exp(-d * t) * math.sin(2 * math.pi * base * r * t)
                     for r, a, d in partials)
        sample *= min(1.0, t / 0.005) * 0.28
        frames += struct.pack("<h", int(max(-1.0, min(1.0, sample)) * 32767))

    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(bytes(frames))
    return path


class Bell(QObject):
    """Plays the bell chime, falling back to the system beep when unavailable."""

    def __init__(self, parent=None, volume: float = 0.9, loops: int = 3) -> None:
        super().__init__(parent)
        self._effect = None
        if HAS_AUDIO:
            try:
                self._effect = QSoundEffect(self)
                self._effect.setSource(QUrl.fromLocalFile(str(make_bell_wav())))
                self._effect.setVolume(volume)
                self._effect.setLoopCount(loops)
            except Exception:
                self._effect = None

    def play(self) -> None:
        if self._effect is not None:
            self._effect.play()
        else:
            QApplication.beep()

    def stop(self) -> None:
        if self._effect is not None:
            self._effect.stop()
