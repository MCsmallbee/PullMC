"""Filesystem locations used by PullMC.

The application keeps mutable state outside the installation directory:
``%LOCALAPPDATA%\\PullMC`` on Windows, and a hidden per-user directory
elsewhere.

All user-facing configuration lives in ``config``.  PullMC itself owns
``ui.json``; later download/version/mirror settings will get their own file
there instead of spreading state around the data directory.
"""

from __future__ import annotations

import os
from pathlib import Path

APP_DIR_NAME = "PullMC"


def app_data_dir() -> Path:
    """Return the per-user directory for PullMC state.

    ``PULLMC_DATA_DIR`` is an explicit escape hatch for portable installs and
    for running from a restricted development sandbox.
    """

    override = os.environ.get("PULLMC_DATA_DIR")
    if override:
        return Path(override)
    local_app_data = os.environ.get("LOCALAPPDATA")
    base = Path(local_app_data) if local_app_data else Path.home() / ".local" / "share"
    return base / APP_DIR_NAME


def config_dir() -> Path:
    return app_data_dir() / "config"


def settings_path() -> Path:
    """The single UI configuration file for now."""

    return config_dir() / "ui.json"


def legacy_settings_path() -> Path:
    return app_data_dir() / "settings.json"


def legacy_rinui_config_dir() -> Path:
    """Old RinUI auto-generated directory, kept only for one-time migration."""

    return app_data_dir() / "rinui"
