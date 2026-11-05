import sys
import types

from pullmc import system


def test_abgr_registry_value_is_converted_to_rgb() -> None:
    # AccentColorMenu stores 0xAABBGGRR on Windows.
    assert system.accent_from_abgr(0xFFD67A00) == "#007AD6"
    assert system.accent_from_abgr(-0x298600) == "#007AD6"


def test_argb_colorization_value_is_converted_to_rgb() -> None:
    # ColorizationColor stores 0xAARRGGBB.
    assert system.accent_from_argb(0xC4007AD6) == "#007AD6"


def test_registry_accent_prefers_accent_color_menu(monkeypatch) -> None:
    accent_path = r"Software\Microsoft\Windows\CurrentVersion\Explorer\Accent"
    dwm_path = r"Software\Microsoft\Windows\DWM"
    values = {
        (accent_path, "AccentColorMenu"): 0xFFD67A00,
        (dwm_path, "AccentColor"): 0xFF112233,
        (dwm_path, "ColorizationColor"): 0xC4000000,
    }
    calls = []

    def open_key(root, subkey, reserved, access):
        calls.append(subkey)
        return subkey

    def query_value(key, name):
        try:
            return values[(key, name)], 4
        except KeyError as exc:
            raise OSError("missing value") from exc

    fake_api = types.SimpleNamespace(
        RegOpenKeyEx=open_key,
        RegQueryValueEx=query_value,
        RegCloseKey=lambda key: None,
    )
    monkeypatch.setitem(sys.modules, "win32api", fake_api)
    monkeypatch.setitem(
        sys.modules,
        "win32con",
        types.SimpleNamespace(HKEY_CURRENT_USER=0, KEY_READ=1),
    )
    monkeypatch.setattr(system.sys, "platform", "win32")

    assert system.system_accent_color() == "#007AD6"
    assert calls[0] == accent_path


def test_registry_accent_falls_back_to_colorization_color(monkeypatch) -> None:
    dwm_path = r"Software\Microsoft\Windows\DWM"

    def open_key(root, subkey, reserved, access):
        return subkey

    def query_value(key, name):
        if key == dwm_path and name == "ColorizationColor":
            return 0xC4007AD6, 4
        raise OSError("missing value")

    fake_api = types.SimpleNamespace(
        RegOpenKeyEx=open_key,
        RegQueryValueEx=query_value,
        RegCloseKey=lambda key: None,
    )
    monkeypatch.setitem(sys.modules, "win32api", fake_api)
    monkeypatch.setitem(
        sys.modules,
        "win32con",
        types.SimpleNamespace(HKEY_CURRENT_USER=0, KEY_READ=1),
    )
    monkeypatch.setattr(system.sys, "platform", "win32")

    assert system.system_accent_color() == "#007AD6"


def test_system_accent_is_empty_off_windows(monkeypatch) -> None:
    monkeypatch.setattr(system.sys, "platform", "darwin")
    assert system.system_accent_color() == ""
