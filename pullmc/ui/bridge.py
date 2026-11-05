"""Slots and signals that the QML shell may call."""

from __future__ import annotations

from PySide6.QtCore import QObject, Signal, Slot


class AppBridge(QObject):
    openLibraryRequested = Signal()
    pong = Signal(str)
    appearanceChanged = Signal()

    def __init__(self, settings, i18n, app_info, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._settings = settings
        self._i18n = i18n
        self._app_info = app_info
        self._theme_manager = None
        self._settings.effectiveAccentColorChanged.connect(self.applyAppearance)

    def set_theme_manager(self, manager) -> None:
        self._theme_manager = manager

    @Slot(result=str)
    def currentAccent(self) -> str:
        return self._settings.effectiveAccentColor

    @Slot()
    def applyAppearance(self) -> None:
        if self._theme_manager is None:
            return
        try:
            self._theme_manager.toggle_theme(self._settings.themeMode)
            self._theme_manager.set_theme_color(self._settings.effectiveAccentColor)
            self.appearanceChanged.emit()
        except Exception:
            # Theme integration is best-effort; the UI still works with defaults.
            pass

    @Slot()
    def ping(self) -> None:
        self.pong.emit("pong")

    @Slot()
    def requestLibrary(self) -> None:
        self.openLibraryRequested.emit()

    @Slot(str, result=bool)
    def setLanguage(self, code: str) -> bool:
        # Persist first so a languageChanged signal cannot observe the old
        # value while the translation model is being rebuilt.
        if not self._settings.setLanguage(code):
            return False
        return bool(self._i18n.setLanguage(code))

    @Slot(str, result=bool)
    def setDisplayName(self, name: str) -> bool:
        return bool(self._settings.setDisplayName(name))

    @Slot(bool, result=bool)
    def setUseSystemDisplayName(self, enabled: bool) -> bool:
        return bool(self._settings.setUseSystemDisplayName(enabled))

    @Slot(str, result=bool)
    def setThemeMode(self, mode: str) -> bool:
        if not self._settings.setThemeMode(mode):
            return False
        self.applyAppearance()
        return True

    @Slot(str, result=bool)
    def setAccentMode(self, mode: str) -> bool:
        if not self._settings.setAccentMode(mode):
            return False
        self.applyAppearance()
        return True

    @Slot(str, result=bool)
    def setAccentColor(self, color: str) -> bool:
        if not self._settings.setAccentColor(color):
            return False
        self.applyAppearance()
        return True

    @Slot(str, result=bool)
    def setBackdropEffect(self, effect: str) -> bool:
        if not self._settings.setBackdropEffect(effect):
            return False
        if self._theme_manager is not None:
            try:
                self._theme_manager.apply_backdrop_effect(effect)
            except Exception:
                pass
        return True

    @Slot(result=bool)
    def completeOnboarding(self) -> bool:
        return bool(self._settings.setOnboardingCompletedVersion(1))

    @Slot(int, result=bool)
    def acceptDisclaimer(self, version: int) -> bool:
        if version != self._app_info.disclaimerVersion:
            return False
        return bool(self._settings.setDisclaimerAcceptedVersion(version))
