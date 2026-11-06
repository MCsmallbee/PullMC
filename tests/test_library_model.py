from pullmc.core.manifest import VersionSummary
from pullmc.ui.library import VersionListModel


def _version(version_id: str, version_type: str, released: str) -> VersionSummary:
    return VersionSummary(
        id=version_id,
        type=version_type,
        url=f"https://example.invalid/{version_id}.json",
        release_time=released,
    )


def test_model_filters_categories_and_sorts_newest_first():
    model = VersionListModel()
    model.set_versions(
        [
            _version("1.20.1", "release", "2023-06-12T10:00:00+00:00"),
            _version("1.21", "release", "2024-06-13T10:00:00+00:00"),
            _version("24w14potato", "snapshot", "2024-04-01T10:00:00+00:00"),
            _version("b1.7.3", "old_beta", "2011-07-08T10:00:00+00:00"),
        ]
    )

    assert model.rowCount() == 2
    assert model.data(model.index(0, 0), model.VersionIdRole) == "1.21"
    assert model.data(model.index(1, 0), model.VersionIdRole) == "1.20.1"
    assert "2024年06月13日" in model.data(model.index(0, 0), model.ReleaseTextRole)

    model.set_category("april_fools")
    assert model.rowCount() == 1
    assert model.data(model.index(0, 0), model.VersionIdRole) == "24w14potato"
    assert model.data(model.index(0, 0), model.IconRole) == "ic_fluent_gift_open_20_regular"

    model.set_category("old")
    assert model.rowCount() == 1
    assert model.data(model.index(0, 0), model.VersionIdRole) == "b1.7.3"


def test_model_ignores_invalid_category():
    model = VersionListModel()
    model.set_versions([])
    model.set_category("release")
    try:
        model.set_category("unknown")
    except ValueError as exc:
        assert "unknown" in str(exc)
    else:
        raise AssertionError("unknown category should be rejected")
