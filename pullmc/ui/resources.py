"""Locations of QML and translation resources inside the package."""

from __future__ import annotations

from pathlib import Path


def package_dir() -> Path:
    return Path(__file__).resolve().parent.parent


def qml_dir() -> Path:
    return package_dir() / "qml"


def i18n_dir() -> Path:
    return package_dir() / "i18n_data"
