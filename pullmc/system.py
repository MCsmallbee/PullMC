"""Small platform helpers used by settings and onboarding.

Everything in this module is deliberately best-effort: a missing Windows API
must never stop PullMC from starting.  Callers get a sensible fallback instead.
"""

from __future__ import annotations

import ctypes
import getpass
import os
import sys

FALLBACK_ACCENT = "#605ED2"
FALLBACK_LANGUAGE = "zh_CN"
FALLBACK_DISPLAY_NAME = "玩家"


def system_accent_color() -> str:
    """Return the Windows colorization color as ``#RRGGBB``.

    ``DwmGetColorizationColor`` has existed since Windows Vista, so it is a
    better fit than the undocumented registry layouts.  The returned value
    includes an alpha channel, which we deliberately drop.
    """

    if sys.platform != "win32":
        return ""

    try:
        color = ctypes.c_uint32()
        opaque = ctypes.c_int()
        result = ctypes.windll.dwmapi.DwmGetColorizationColor(
            ctypes.byref(color), ctypes.byref(opaque)
        )
        if result != 0:
            return ""
        value = int(color.value)
        red = (value >> 16) & 0xFF
        green = (value >> 8) & 0xFF
        blue = value & 0xFF
        return f"#{red:02X}{green:02X}{blue:02X}"
    except (AttributeError, OSError, ValueError):
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
