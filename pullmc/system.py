"""Small platform helpers used by settings and onboarding.

Everything in this module is deliberately best-effort: a missing Windows API
must never stop PullMC from starting.  Callers get a sensible fallback instead.
"""

from __future__ import annotations

import getpass
import os
import sys

FALLBACK_ACCENT = "#605ED2"
FALLBACK_LANGUAGE = "zh_CN"
FALLBACK_DISPLAY_NAME = "玩家"


def accent_from_abgr(value: int) -> str:
    """Convert a Windows ``AABBGGRR`` color to ``#RRGGBB``."""

    value = int(value) & 0xFFFFFFFF
    red = value & 0xFF
    green = (value >> 8) & 0xFF
    blue = (value >> 16) & 0xFF
    return f"#{red:02X}{green:02X}{blue:02X}"


def accent_from_argb(value: int) -> str:
    """Convert a Windows ``AARRGGBB`` color to ``#RRGGBB``."""

    value = int(value) & 0xFFFFFFFF
    red = (value >> 16) & 0xFF
    green = (value >> 8) & 0xFF
    blue = value & 0xFF
    return f"#{red:02X}{green:02X}{blue:02X}"


def _read_registry_value(subkey: str, name: str) -> int | None:
    """Read one integer value below HKCU with win32api, or return None."""

    try:
        import win32api
        import win32con
    except ImportError:
        return None

    key = None
    try:
        key = win32api.RegOpenKeyEx(
            win32con.HKEY_CURRENT_USER, subkey, 0, win32con.KEY_READ
        )
        value, _kind = win32api.RegQueryValueEx(key, name)
        return int(value) if isinstance(value, int) else None
    except Exception:
        return None
    finally:
        if key is not None:
            try:
                win32api.RegCloseKey(key)
            except Exception:
                pass


def system_accent_color() -> str:
    """Return the user's Windows accent color as ``#RRGGBB``.

    The per-user registry is the source Windows itself uses for accent-aware
    UI.  ``AccentColorMenu`` is stored as ABGR; the DWM ``ColorizationColor``
    value is the ARGB fallback.  win32api is imported lazily so non-Windows
    builds do not need pywin32 installed.
    """

    if sys.platform != "win32":
        return ""

    candidates = (
        (
            r"Software\Microsoft\Windows\CurrentVersion\Explorer\Accent",
            "AccentColorMenu",
            accent_from_abgr,
        ),
        (r"Software\Microsoft\Windows\DWM", "AccentColor", accent_from_abgr),
        (r"Software\Microsoft\Windows\DWM", "ColorizationColor", accent_from_argb),
    )
    for subkey, name, convert in candidates:
        value = _read_registry_value(subkey, name)
        if value is not None:
            return convert(value)
    return ""


def system_language() -> str:
    """Map the Windows UI language to one of PullMC's translation tables."""

    try:
        from PySide6.QtCore import QLocale

        code = QLocale.system().name()
    except Exception:
        code = ""

    code = (code or "").replace("-", "_")
    lower = code.lower()
    if lower.startswith("zh"):
        if any(part in lower for part in ("tw", "hk", "mo", "hant")):
            return "zh_TW"
        return "zh_CN"
    if lower.startswith("ja"):
        return "ja"
    if lower.startswith("en"):
        return "en"
    return FALLBACK_LANGUAGE


def system_display_name() -> str:
    """Return the current OS account name, or a neutral fallback."""

    for variable in ("USERNAME", "USER"):
        value = os.environ.get(variable, "").strip()
        if value:
            return value
    try:
        value = getpass.getuser().strip()
    except (KeyError, OSError):
        value = ""
    return value or FALLBACK_DISPLAY_NAME
