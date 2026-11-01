"""Translation backend exposed to QML."""

from __future__ import annotations

import json
import re
from pathlib import Path

from PySide6.QtCore import Property, QObject, Signal, Slot

from .system import system_language
from .ui.resources import i18n_dir

_FALLBACK_LANGUAGE = "zh_CN"
_PLACEHOLDER = re.compile(r"\{(\d+)\}")


class I18nBackend(QObject):
    """Loads JSON translation tables and answers ``t``/``tf`` calls from QML."""

    languageChanged = Signal(str)
    revisionChanged = Signal(int)

    def __init__(
        self,
        language: str = "system",
        data_dir: Path | None = None,
        parent: QObject | None = None,
    ) -> None:
        super().__init__(parent)
        self._data_dir = data_dir or i18n_dir()
        self._tables: dict[str, dict[str, str]] = {}
        self._revision = 0
        self._load_tables()
        if language == "system":
            language = system_language()
        if language not in self._tables:
            language = _FALLBACK_LANGUAGE
        if language not in self._tables and self._tables:
            language = next(iter(self._tables))
        self._language = language

    def _load_tables(self) -> None:
        if not self._data_dir.is_dir():
            raise FileNotFoundError(f"translation directory not found: {self._data_dir}")
        for path in sorted(self._data_dir.glob("*.json")):
            with path.open("r", encoding="utf-8") as handle:
                table = json.load(handle)
            if not isinstance(table, dict):
                raise ValueError(f"translation table must be an object: {path}")
            self._tables[path.stem] = {
                str(key): str(value) for key, value in table.items()
            }
        if not self._tables:
            raise FileNotFoundError(f"no translation tables in {self._data_dir}")

    @Property(str, notify=languageChanged)
    def language(self) -> str:
        return self._language

    @Property(int, notify=revisionChanged)
    def revision(self) -> int:
        return self._revision

    @Slot(str, result=bool)
    def setLanguage(self, code: str) -> bool:
        if code == "system":
            code = system_language()
        if code not in self._tables or code == self._language:
            return code in self._tables
        self._language = code
        self._revision += 1
        self.languageChanged.emit(code)
        self.revisionChanged.emit(self._revision)
        return True

    @Slot(str, str, result=str)
    def t(self, key: str, fallback: str = "") -> str:
        for table in (
            self._tables.get(self._language, {}),
            self._tables.get(_FALLBACK_LANGUAGE, {}),
        ):
            value = table.get(key)
            if value:
                return value
        return fallback

    @Slot(str, str, "QVariantList", result=str)
    def tf(self, key: str, fallback: str, args: list[object]) -> str:
        template = self.t(key, fallback)

        def replace(match: re.Match[str]) -> str:
            index = int(match.group(1))
            if 0 <= index < len(args):
                return str(args[index])
            return match.group(0)

        return _PLACEHOLDER.sub(replace, template)
