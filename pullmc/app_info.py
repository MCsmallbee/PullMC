"""Read-only application metadata exposed to QML."""

from __future__ import annotations

import platform

from PySide6.QtCore import QObject, Property

from . import (
    __version__,
    __version_codename__,
    __version_label__,
    __version_stage__,
)

APP_NAME = "PullMC"


class AppInfo(QObject):
    """Values that do not change while the application is running."""

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)

    @Property(str, constant=True)
    def name(self) -> str:
        return APP_NAME

    @Property(str, constant=True)
    def version(self) -> str:
        return __version_label__

    @Property(str, constant=True)
    def versionNumber(self) -> str:
        return __version__

    @Property(str, constant=True)
    def versionStage(self) -> str:
        return __version_stage__

    @Property(str, constant=True)
    def versionCodename(self) -> str:
        return __version_codename__

    @Property(int, constant=True)
    def disclaimerVersion(self) -> int:
        # Bump this whenever the text or meaning of the disclaimer changes.
        return 1

    @Property(int, constant=True)
    def onboardingVersion(self) -> int:
        # Bump this when the first-run setup should be shown again.
        return 1

    @Property(str, constant=True)
    def osName(self) -> str:
        return platform.system()
