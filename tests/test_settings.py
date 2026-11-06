import re
import shutil
import uuid
from pathlib import Path

import pytest

from pullmc.settings import AppSettings


@pytest.fixture
def settings_home(monkeypatch):
    root = Path.cwd() / ".tmp" / f"test-settings-{uuid.uuid4().hex}"
    root.mkdir(parents=True)
    monkeypatch.setenv("PULLMC_DATA_DIR", str(root))
    try:
        yield root
    finally:
        shutil.rmtree(root, ignore_errors=True)


def test_defaults_follow_the_system(settings_home) -> None:
    settings = AppSettings()

    assert settings.onboardingCompletedVersion == 0
    assert settings.disclaimerAcceptedVersion == 0
    assert settings.displayName == ""
    assert settings.useSystemDisplayName is True
    assert settings.language == "system"
    assert settings.themeMode == "Auto"
    assert settings.accentMode == "system"
    assert re.fullmatch(r"#[0-9A-F]{6}", settings.effectiveAccentColor)


def test_changes_are_persisted(settings_home) -> None:
    settings = AppSettings()

    assert settings.setOnboardingCompletedVersion(1)
    assert settings.setDisclaimerAcceptedVersion(1)
    assert settings.setUseSystemDisplayName(False)
    assert settings.setDisplayName("Alex")
    assert settings.setLanguage("en")
    assert settings.setThemeMode("Dark")
    assert settings.setAccentMode("custom")
    assert settings.setAccentColor("#112233")

    config = settings_home / "config" / "ui.json"
    assert config.exists()

    reloaded = AppSettings()
    assert reloaded.onboardingCompletedVersion == 1
    assert reloaded.disclaimerAcceptedVersion == 1
    assert reloaded.useSystemDisplayName is False
    assert reloaded.displayName == "Alex"
    assert reloaded.language == "en"
    assert reloaded.themeMode == "Dark"
    assert reloaded.accentMode == "custom"
    assert reloaded.accentColor == "#112233"
    assert reloaded.effectiveAccentColor == "#112233"


def test_invalid_values_are_rejected(settings_home) -> None:
    settings = AppSettings()

    assert not settings.setLanguage("fr")
    assert not settings.setThemeMode("Neon")
    assert not settings.setAccentMode("rainbow")
    assert not settings.setAccentColor("red")
    assert not settings.setAccentColor("#12345")


def test_system_accent_can_be_refreshed(settings_home, monkeypatch) -> None:
    import pullmc.settings as settings_module

    monkeypatch.setattr(settings_module, "system_accent_color", lambda: "#123456")
    settings = AppSettings()
    assert settings.effectiveAccentColor == "#123456"

    monkeypatch.setattr(settings_module, "system_accent_color", lambda: "#654321")
    assert settings.refreshSystemAccent() is True
    assert settings.systemAccentColor == "#654321"
    assert settings.effectiveAccentColor == "#654321"


def test_system_accent_refresh_keeps_custom_color(settings_home, monkeypatch) -> None:
    import pullmc.settings as settings_module

    monkeypatch.setattr(settings_module, "system_accent_color", lambda: "#123456")
    settings = AppSettings()
    assert settings.setAccentMode("custom")
    assert settings.setAccentColor("#000000")

    monkeypatch.setattr(settings_module, "system_accent_color", lambda: "#654321")
    assert settings.refreshSystemAccent() is True
    assert settings.systemAccentColor == "#654321"
    assert settings.effectiveAccentColor == "#000000"


def test_version_fetch_and_console_defaults(settings_home):
    settings = AppSettings()

    assert settings.mirrorMode == "auto"
    assert settings.requestTimeout == 20
    assert settings.consoleEnabled is False


def test_version_fetch_and_console_settings_persist(settings_home):
    settings = AppSettings()

    assert settings.setMirrorMode("mojang")
    assert settings.setRequestTimeout(45)
    assert settings.setConsoleEnabled(True)

    reloaded = AppSettings()
    assert reloaded.mirrorMode == "mojang"
    assert reloaded.requestTimeout == 45
    assert reloaded.consoleEnabled is True


def test_invalid_version_fetch_settings_are_rejected(settings_home):
    settings = AppSettings()

    assert not settings.setMirrorMode("curseforge")
    assert not settings.setRequestTimeout(4)
    assert not settings.setRequestTimeout(61)
