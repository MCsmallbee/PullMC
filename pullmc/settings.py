"""Persistent UI settings for PullMC.

The UI currently owns one configuration file, ``config/ui.json``.  Download
paths, version folders and mirror preferences will get a separate file later,
so this module must not grow into a catch-all store.
"""

from __future__ import annotations

import json
import logging
import os
import re
import shutil
from typing import Any

from PySide6.QtCore import Property, QObject, Signal, Slot

from .paths import (
    config_dir,
    legacy_rinui_config_dir,
    legacy_settings_path,
    settings_path,
)
from .system import FALLBACK_ACCENT, system_accent_color, system_display_name

log = logging.getLogger(__name__)

_DEFAULT_DATA: dict[str, Any] = {
    "schemaVersion": 1,
    "onboardingCompletedVersion": 0,
    "disclaimerAcceptedVersion": 0,
    "displayName": "",
    "useSystemDisplayName": True,
    "language": "system",
    "themeMode": "Auto",
    "accentMode": "system",
    "accentColor": FALLBACK_ACCENT,
    "backdropEffect": "mica",
    "mirrorMode": "auto",
    "requestTimeout": 20,
    "consoleEnabled": False,
}

_SUPPORTED_LANGUAGES = {"system", "zh_CN", "zh_TW", "en", "ja"}
_THEME_MODES = {"Auto", "Light", "Dark"}
_ACCENT_MODES = {"system", "custom"}
_BACKDROP_EFFECTS = {"mica", "tabbed", "acrylic", "none"}
_COLOR_PATTERN = re.compile(r"^#[0-9A-Fa-f]{6}$")
_MIRROR_MODES = {"auto", "mojang", "bmclapi"}


class AppSettings(QObject):
    disclaimerAcceptedVersionChanged = Signal()
    onboardingCompletedVersionChanged = Signal()
    displayNameChanged = Signal()
    useSystemDisplayNameChanged = Signal()
    languageChanged = Signal()
    themeModeChanged = Signal()
    accentModeChanged = Signal()
    accentColorChanged = Signal()
    effectiveAccentColorChanged = Signal()
    systemAccentColorChanged = Signal()
    backdropEffectChanged = Signal()
    mirrorModeChanged = Signal()
    requestTimeoutChanged = Signal()
    consoleEnabledChanged = Signal()

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._path = settings_path()
        self._data = dict(_DEFAULT_DATA)
        self._system_accent = system_accent_color()
        self._system_display_name = system_display_name()
        self._load()

    # ------------------------------------------------------------------ load

    def _load(self) -> None:
        legacy = None
        if self._path.exists():
            try:
                with self._path.open("r", encoding="utf-8") as handle:
                    raw = json.load(handle)
                if isinstance(raw, dict):
                    for key in _DEFAULT_DATA:
                        if key in raw:
                            self._data[key] = raw[key]
            except (OSError, ValueError) as exc:
                log.warning("could not read settings from %s: %s", self._path, exc)
        else:
            legacy = self._read_legacy()
            if legacy:
                self._data.update(legacy)

        self._normalize()

        if legacy is not None:
            if self._save():
                self._remove_legacy()
            else:
                log.warning("legacy settings could not be migrated yet")

    def _read_legacy(self) -> dict[str, Any] | None:
        """Read the old flat settings and RinUI config, if either exists."""

        legacy: dict[str, Any] = {}
        old_settings = legacy_settings_path()
        if old_settings.exists():
            try:
                with old_settings.open("r", encoding="utf-8") as handle:
                    raw = json.load(handle)
                if isinstance(raw, dict):
                    for key in (
                        "disclaimerAcceptedVersion",
                        "displayName",
                        "language",
                    ):
                        if key in raw:
                            legacy[key] = raw[key]
            except (OSError, ValueError) as exc:
                log.warning("could not read legacy settings %s: %s", old_settings, exc)

        old_rinui = legacy_rinui_config_dir() / "RinUI" / "config" / "rin_ui.json"
        if old_rinui.exists():
            try:
                with old_rinui.open("r", encoding="utf-8") as handle:
                    raw = json.load(handle)
                if isinstance(raw, dict):
                    theme = raw.get("theme")
                    if isinstance(theme, dict) and theme.get("current_theme"):
                        legacy["themeMode"] = theme["current_theme"]
                    color = raw.get("theme_color")
                    if isinstance(color, str) and _COLOR_PATTERN.fullmatch(color):
                        legacy["accentColor"] = color
                        if color.upper() != FALLBACK_ACCENT:
                            legacy["accentMode"] = "custom"
                    effect = raw.get("backdrop_effect")
                    if isinstance(effect, str) and effect in _BACKDROP_EFFECTS:
                        legacy["backdropEffect"] = effect
            except (OSError, ValueError) as exc:
                log.warning("could not read legacy RinUI config %s: %s", old_rinui, exc)

        return legacy or None

    def _remove_legacy(self) -> None:
        old_settings = legacy_settings_path()
        try:
            if old_settings.exists():
                old_settings.unlink()
        except OSError as exc:
            log.warning("could not remove legacy settings %s: %s", old_settings, exc)

        old_dir = legacy_rinui_config_dir()
        try:
            if old_dir.exists():
                shutil.rmtree(old_dir)
        except OSError as exc:
            log.warning("could not remove legacy RinUI directory %s: %s", old_dir, exc)

    def _normalize(self) -> None:
        self._data["schemaVersion"] = 1
        for key in ("onboardingCompletedVersion", "disclaimerAcceptedVersion"):
            try:
                self._data[key] = max(0, int(self._data.get(key, 0) or 0))
            except (TypeError, ValueError):
                self._data[key] = 0

        name = self._data.get("displayName")
        self._data["displayName"] = str(name or "").strip()
        self._data["useSystemDisplayName"] = bool(
            self._data.get("useSystemDisplayName", True)
        )

        if self._data.get("language") not in _SUPPORTED_LANGUAGES:
            self._data["language"] = "system"
        if self._data.get("themeMode") not in _THEME_MODES:
            self._data["themeMode"] = "Auto"
        if self._data.get("accentMode") not in _ACCENT_MODES:
            self._data["accentMode"] = "system"
        if self._data.get("backdropEffect") not in _BACKDROP_EFFECTS:
            self._data["backdropEffect"] = "mica"
        if self._data.get("mirrorMode") not in _MIRROR_MODES:
            self._data["mirrorMode"] = "auto"
        try:
            timeout = int(self._data.get("requestTimeout", 20))
        except (TypeError, ValueError):
            timeout = 20
        self._data["requestTimeout"] = min(60, max(5, timeout))
        self._data["consoleEnabled"] = bool(self._data.get("consoleEnabled", False))

        color = str(self._data.get("accentColor") or "")
        self._data["accentColor"] = (
            color.upper() if _COLOR_PATTERN.fullmatch(color) else FALLBACK_ACCENT
        )

    # ------------------------------------------------------------------ save

    def _save(self) -> bool:
        try:
            config_dir().mkdir(parents=True, exist_ok=True)
            temporary = self._path.with_suffix(".json.tmp")
            with temporary.open("w", encoding="utf-8") as handle:
                json.dump(self._data, handle, ensure_ascii=False, indent=2)
                handle.write("\n")
            os.replace(temporary, self._path)
            return True
        except OSError as exc:
            log.warning("could not save settings to %s: %s", self._path, exc)
            return False

    def _set(self, key: str, value: Any, signal: Signal) -> bool:
        if self._data.get(key) == value:
            return True
        previous = self._data.get(key)
        self._data[key] = value
        if not self._save():
            self._data[key] = previous
            return False
        signal.emit()
        return True

    # ------------------------------------------------------------- properties

    @Property(int, notify=onboardingCompletedVersionChanged)
    def onboardingCompletedVersion(self) -> int:
        return int(self._data["onboardingCompletedVersion"])

    @Slot(int, result=bool)
    def setOnboardingCompletedVersion(self, version: int) -> bool:
        return self._set(
            "onboardingCompletedVersion",
            max(0, int(version)),
            self.onboardingCompletedVersionChanged,
        )

    @Property(int, notify=disclaimerAcceptedVersionChanged)
    def disclaimerAcceptedVersion(self) -> int:
        return int(self._data["disclaimerAcceptedVersion"])

    @Slot(int, result=bool)
    def setDisclaimerAcceptedVersion(self, version: int) -> bool:
        return self._set(
            "disclaimerAcceptedVersion",
            max(0, int(version)),
            self.disclaimerAcceptedVersionChanged,
        )

    @Property(str, notify=displayNameChanged)
    def displayName(self) -> str:
        return str(self._data["displayName"])

    @Slot(str, result=bool)
    def setDisplayName(self, name: str) -> bool:
        clean = str(name or "").strip()
        if not self._set("displayName", clean, self.displayNameChanged):
            return False
        if clean and not self.useSystemDisplayName:
            return True
        if clean:
            return self.setUseSystemDisplayName(False)
        return True

    @Property(bool, notify=useSystemDisplayNameChanged)
    def useSystemDisplayName(self) -> bool:
        return bool(self._data["useSystemDisplayName"])

    @Slot(bool, result=bool)
    def setUseSystemDisplayName(self, enabled: bool) -> bool:
        return self._set(
            "useSystemDisplayName",
            bool(enabled),
            self.useSystemDisplayNameChanged,
        )

    @Property(str, notify=languageChanged)
    def language(self) -> str:
        return str(self._data["language"])

    @Slot(str, result=bool)
    def setLanguage(self, code: str) -> bool:
        if code not in _SUPPORTED_LANGUAGES:
            return False
        return self._set("language", code, self.languageChanged)

    @Property(str, notify=themeModeChanged)
    def themeMode(self) -> str:
        return str(self._data["themeMode"])

    @Slot(str, result=bool)
    def setThemeMode(self, mode: str) -> bool:
        if mode not in _THEME_MODES:
            return False
        return self._set("themeMode", mode, self.themeModeChanged)

    @Property(str, notify=accentModeChanged)
    def accentMode(self) -> str:
        return str(self._data["accentMode"])

    @Slot(str, result=bool)
    def setAccentMode(self, mode: str) -> bool:
        if mode not in _ACCENT_MODES:
            return False
        changed = self._set("accentMode", mode, self.accentModeChanged)
        if changed:
            self.effectiveAccentColorChanged.emit()
        return changed

    @Property(str, notify=accentColorChanged)
    def accentColor(self) -> str:
        return str(self._data["accentColor"])

    @Slot(str, result=bool)
    def setAccentColor(self, color: str) -> bool:
        normalized = str(color or "").upper()
        if not _COLOR_PATTERN.fullmatch(normalized):
            return False
        changed = self._set("accentColor", normalized, self.accentColorChanged)
        if changed:
            self.effectiveAccentColorChanged.emit()
        return changed

    @Property(str, notify=backdropEffectChanged)
    def backdropEffect(self) -> str:
        return str(self._data["backdropEffect"])

    @Slot(str, result=bool)
    def setBackdropEffect(self, effect: str) -> bool:
        if effect not in _BACKDROP_EFFECTS:
            return False
        return self._set("backdropEffect", effect, self.backdropEffectChanged)

    @Property(str, notify=mirrorModeChanged)
    def mirrorMode(self) -> str:
        return str(self._data["mirrorMode"])

    @Slot(str, result=bool)
    def setMirrorMode(self, mode: str) -> bool:
        if mode not in _MIRROR_MODES:
            return False
        return self._set("mirrorMode", mode, self.mirrorModeChanged)

    @Property(int, notify=requestTimeoutChanged)
    def requestTimeout(self) -> int:
        return int(self._data["requestTimeout"])

    @Slot(int, result=bool)
    def setRequestTimeout(self, seconds: int) -> bool:
        if not 5 <= int(seconds) <= 60:
            return False
        return self._set("requestTimeout", int(seconds), self.requestTimeoutChanged)

    @Property(bool, notify=consoleEnabledChanged)
    def consoleEnabled(self) -> bool:
        return bool(self._data["consoleEnabled"])

    @Slot(bool, result=bool)
    def setConsoleEnabled(self, enabled: bool) -> bool:
        return self._set("consoleEnabled", bool(enabled), self.consoleEnabledChanged)

    @Slot(result=bool)
    def refreshSystemAccent(self) -> bool:
        """Re-read the Windows accent after a theme change."""

        accent = system_accent_color()
        if not accent or accent.upper() == self._system_accent.upper():
            return False
        self._system_accent = accent.upper()
        self.systemAccentColorChanged.emit()
        if self.accentMode == "system":
            self.effectiveAccentColorChanged.emit()
        return True

    @Property(str, notify=effectiveAccentColorChanged)
    def effectiveAccentColor(self) -> str:
        if self.accentMode == "custom":
            return self.accentColor
        return self._system_accent or FALLBACK_ACCENT

    @Property(str, notify=systemAccentColorChanged)
    def systemAccentColor(self) -> str:
        return self._system_accent

    @Property(str, constant=True)
    def systemDisplayName(self) -> str:
        return self._system_display_name
