from pullmc.i18n import I18nBackend


def test_translation_tables_have_the_same_keys() -> None:
    backend = I18nBackend()
    tables = backend._tables
    expected = set(tables["zh_CN"])
    assert expected
    for code, table in tables.items():
        assert set(table) == expected, f"{code} has a different key set"


def test_every_translation_is_non_empty() -> None:
    backend = I18nBackend()
    for code, table in backend._tables.items():
        for key, value in table.items():
            assert value.strip(), f"{code}:{key} is empty"


def test_formatting_and_language_switch() -> None:
    backend = I18nBackend()
    assert backend.tf("home.greeting.morning", "fallback {0}", ["Alex"]) == "早上好，Alex"
    assert backend.setLanguage("en") is True
    assert backend.language == "en"
    assert backend.tf("home.greeting.morning", "fallback {0}", ["Alex"]) == "Good morning, Alex"


def test_unknown_key_uses_fallback() -> None:
    backend = I18nBackend()
    assert backend.t("missing.key", "fallback") == "fallback"
