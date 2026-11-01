"""Home-page greeting state.

This module is deliberately free of QML and network assumptions so the
time-bucket and display-name rules can be tested without a running window.
"""

from __future__ import annotations

import getpass
import os
from datetime import datetime

from PySide6.QtCore import Property, QObject, QTimer, Signal, Slot

# (first hour, greeting id, Chinese default)
_GREETING_BUCKETS: tuple[tuple[int, str, str], ...] = (
    (5, "home.greeting.morning", "早上好，{0}"),
    (9, "home.greeting.forenoon", "上午好，{0}"),
    (12, "home.greeting.noon", "中午好，{0}"),
    (14, "home.greeting.afternoon", "下午好，{0}"),
    (18, "home.greeting.evening", "晚上好，{0}"),
    (23, "home.greeting.latenight", "夜深了，{0}"),
)


def title_for(now: datetime | None = None) -> tuple[str, str]:
    """Return ``(translation key, Chinese fallback)`` for *now*."""

    hour = (now or datetime.now()).hour
    selected = _GREETING_BUCKETS[0]
    for bucket in _GREETING_BUCKETS:
        if hour >= bucket[0]:
            selected = bucket
        else:
            break
    if hour < _GREETING_BUCKETS[0][0]:
        selected = _GREETING_BUCKETS[-1]
    return selected[1], selected[2]


def resolve_display_name(configured: str, fallback: str = "玩家") -> str:
    """Use an explicit name, then the OS account name, then *fallback*."""

    name = (configured or "").strip()
    if name:
        return name
    for variable in ("USERNAME", "USER"):
        value = os.environ.get(variable, "").strip()
        if value:
            return value
    try:
        value = getpass.getuser().strip()
    except (KeyError, OSError):
        value = ""
    return value or fallback


class HomeState(QObject):
    titleIdChanged = Signal()
    titleDefaultChanged = Signal()
    displayNameChanged = Signal()

    def __init__(self, settings, i18n, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._settings = settings
        self._i18n = i18n
        self._title_id = ""
        self._title_default = ""
        self._display_name = ""
        self._timer = QTimer(self)
        self._timer.setInterval(30_000)
        self._timer.timeout.connect(self.refresh)
        self._timer.start()
        if hasattr(i18n, "languageChanged"):
            i18n.languageChanged.connect(lambda _code: self.refresh())
        if hasattr(settings, "displayNameChanged"):
            settings.displayNameChanged.connect(self.refresh)
        if hasattr(settings, "useSystemDisplayNameChanged"):
            settings.useSystemDisplayNameChanged.connect(self.refresh)
        self.refresh()

    @Property(str, notify=titleIdChanged)
    def titleId(self) -> str:
        return self._title_id

    @Property(str, notify=titleDefaultChanged)
    def titleDefault(self) -> str:
        return self._title_default

    @Property(str, notify=displayNameChanged)
    def displayName(self) -> str:
        return self._display_name

    @Slot()
    def refresh(self) -> None:
        title_id, title_default = title_for()
        fallback_name = self._i18n.t("home.display_name.fallback", "玩家")
        configured = "" if self._settings.useSystemDisplayName else self._settings.displayName
        display_name = resolve_display_name(configured, fallback_name)
        if title_id != self._title_id:
            self._title_id = title_id
            self.titleIdChanged.emit()
        if title_default != self._title_default:
            self._title_default = title_default
            self.titleDefaultChanged.emit()
        if display_name != self._display_name:
            self._display_name = display_name
            self.displayNameChanged.emit()
