"""Version catalogue model and the QML-facing library controller."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Iterable

from PySide6.QtCore import (
    QAbstractListModel,
    QModelIndex,
    QObject,
    Property,
    QRunnable,
    Qt,
    QThreadPool,
    Signal,
    Slot,
)

from ..core.http import HttpClient
from ..core.manifest import CATEGORY_ORDER, VersionSummary, categorize_version, fetch_manifest
from ..core.mirrors import Mirrors


ICONS = {
    "release": "ic_fluent_cube_20_regular",
    "snapshot": "ic_fluent_flash_sparkle_20_regular",
    "old": "ic_fluent_archive_clock_20_regular",
    "april_fools": "ic_fluent_gift_open_20_regular",
}


class VersionListModel(QAbstractListModel):
    """Flat, category-filtered view over Mojang's version manifest."""

    VersionIdRole = Qt.ItemDataRole.UserRole + 1
    CategoryRole = Qt.ItemDataRole.UserRole + 2
    ReleaseTextRole = Qt.ItemDataRole.UserRole + 3
    IconRole = Qt.ItemDataRole.UserRole + 4
    TypeRole = Qt.ItemDataRole.UserRole + 5

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._versions: list[VersionSummary] = []
        self._visible: list[VersionSummary] = []
        self._category = "release"

    def roleNames(self) -> dict[int, bytes]:
        return {
            self.VersionIdRole: b"versionId",
            self.CategoryRole: b"category",
            self.ReleaseTextRole: b"releaseText",
            self.IconRole: b"iconName",
            self.TypeRole: b"type",
        }

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        if parent.isValid():
            return 0
        return len(self._visible)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or not 0 <= index.row() < len(self._visible):
            return None
        version = self._visible[index.row()]
        category = categorize_version(version)
        if role in (Qt.ItemDataRole.DisplayRole, self.VersionIdRole):
            return version.id
        if role == self.CategoryRole:
            return category
        if role == self.ReleaseTextRole:
            return _release_text(version.release_time)
        if role == self.IconRole:
            return ICONS[category]
        if role == self.TypeRole:
            return version.type
        return None

    @property
    def category(self) -> str:
        return self._category

    def set_versions(self, versions: Iterable[VersionSummary]) -> None:
        self._versions = sorted(versions, key=_sort_key, reverse=True)
        self._rebuild()

    def set_category(self, category: str) -> None:
        if category not in CATEGORY_ORDER:
            raise ValueError(f"unknown library category: {category}")
        if category == self._category:
            return
        self._category = category
        self._rebuild()

    def _rebuild(self) -> None:
        self.beginResetModel()
        self._visible = [
            version
            for version in self._versions
            if categorize_version(version) == self._category
        ]
        self.endResetModel()


class _ManifestSignals(QObject):
    finished = Signal(object)
    failed = Signal(str)


class _ManifestJob(QRunnable):
    def __init__(self, mirror_mode: str = "auto", timeout: float = 20.0) -> None:
        super().__init__()
        self.signals = _ManifestSignals()
        self._mirror_mode = mirror_mode
        self._timeout = timeout

    def run(self) -> None:
        try:
            client = HttpClient(timeout=self._timeout)
            versions, _ = fetch_manifest(client, Mirrors(self._mirror_mode))
            self.signals.finished.emit(versions)
        except Exception as exc:  # The UI receives a concise, stable message.
            self.signals.failed.emit(str(exc))


def manifest_options(settings) -> tuple[str, float]:
    if settings is None:
        return "auto", 20.0
    mode = str(getattr(settings, "mirrorMode", "auto"))
    if mode not in ("auto", "mojang", "bmclapi"):
        mode = "auto"
    try:
        timeout = float(getattr(settings, "requestTimeout", 20))
    except (TypeError, ValueError):
        timeout = 20.0
    return mode, timeout


class LibraryController(QObject):
    stateChanged = Signal()
    errorChanged = Signal()
    categoryChanged = Signal()
    countChanged = Signal()

    def __init__(self, settings=None, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.model = VersionListModel(self)
        self._settings = settings
        self._state = "idle"
        self._error = ""
        self._busy = False
        if settings is not None:
            settings.mirrorModeChanged.connect(self._on_fetch_settings_changed)
            settings.requestTimeoutChanged.connect(self._on_fetch_settings_changed)

    @Property(str, notify=stateChanged)
    def state(self) -> str:
        return self._state

    @Property(str, notify=errorChanged)
    def error(self) -> str:
        return self._error

    @Property(str, notify=categoryChanged)
    def category(self) -> str:
        return self.model.category

    @Property(int, notify=countChanged)
    def count(self) -> int:
        return self.model.rowCount()

    @Slot()
    def refresh(self) -> None:
        if self._busy:
            return
        self._busy = True
        self._error = ""
        self._state = "loading"
        self.errorChanged.emit()
        self.stateChanged.emit()

        job = _ManifestJob(*manifest_options(self._settings))
        job.signals.finished.connect(self._on_finished)
        job.signals.failed.connect(self._on_failed)
        QThreadPool.globalInstance().start(job)

    @Slot()
    def _on_fetch_settings_changed(self) -> None:
        if self._state in ("ready", "error"):
            self.refresh()

    @Slot(str)
    def setCategory(self, category: str) -> None:
        if category not in CATEGORY_ORDER or category == self.model.category:
            return
        self.model.set_category(category)
        self.categoryChanged.emit()
        self.countChanged.emit()

    @Slot(object)
    def _on_finished(self, versions: object) -> None:
        self._busy = False
        self.model.set_versions(versions or [])  # type: ignore[arg-type]
        self._state = "ready"
        self.stateChanged.emit()
        self.countChanged.emit()

    @Slot(str)
    def _on_failed(self, message: str) -> None:
        self._busy = False
        self._error = message
        self._state = "error"
        self.errorChanged.emit()
        self.stateChanged.emit()


def _release_text(value: str) -> str:
    try:
        moment = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return moment.astimezone().strftime("%Y年%m月%d日 %H:%M")
    except (TypeError, ValueError):
        return ""


def _sort_key(version: VersionSummary) -> datetime:
    try:
        return datetime.fromisoformat(version.release_time.replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return datetime.min.replace(tzinfo=timezone.utc)
