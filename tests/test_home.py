from datetime import datetime

from pullmc.ui.home import resolve_display_name, title_for


def test_title_buckets_cover_the_day() -> None:
    expected = {
        4: "home.greeting.latenight",
        5: "home.greeting.morning",
        8: "home.greeting.morning",
        9: "home.greeting.forenoon",
        11: "home.greeting.forenoon",
        12: "home.greeting.noon",
        13: "home.greeting.noon",
        14: "home.greeting.afternoon",
        17: "home.greeting.afternoon",
        18: "home.greeting.evening",
        22: "home.greeting.evening",
        23: "home.greeting.latenight",
        0: "home.greeting.latenight",
    }
    for hour, key in expected.items():
        assert title_for(datetime(2026, 1, 1, hour, 0))[0] == key


def test_title_includes_placeholder() -> None:
    key, default = title_for(datetime(2026, 1, 1, 9, 0))
    assert key == "home.greeting.forenoon"
    assert "{0}" in default


def test_configured_name_wins(monkeypatch) -> None:
    monkeypatch.setenv("USERNAME", "os-user")
    assert resolve_display_name("  Alex  ", "fallback") == "Alex"


def test_environment_name_is_used(monkeypatch) -> None:
    monkeypatch.setenv("USERNAME", "os-user")
    assert resolve_display_name("", "fallback") == "os-user"


def test_fallback_name_is_used(monkeypatch) -> None:
    monkeypatch.delenv("USERNAME", raising=False)
    monkeypatch.delenv("USER", raising=False)
    monkeypatch.setattr("pullmc.ui.home.getpass.getuser", lambda: "")
    assert resolve_display_name("", "fallback") == "fallback"
