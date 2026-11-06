from pullmc.core.manifest import (
    VersionSummary,
    categorize_version,
    fetch_manifest,
    fetch_version_json,
    group_versions,
    library_files,
    rules_allow,
)
from pullmc.core.mirrors import Manifest, Mirrors


class FakeClient:
    def __init__(self, *responses):
        self._responses = list(responses)
        self.calls: list[tuple[str, ...]] = []

    def get_json(self, urls):
        self.calls.append(tuple(urls))
        if not self._responses:
            raise AssertionError("unexpected get_json call")
        return self._responses.pop(0)


MANIFEST = {
    "latest": {"release": "1.21.1", "snapshot": "25w31a"},
    "versions": [
        {
            "id": "1.21.1",
            "type": "release",
            "url": "https://piston-meta.mojang.com/v1/packages/aa/1.21.1.json",
            "releaseTime": "2024-08-08T14:05:00+00:00",
            "sha1": "aa",
            "size": 123,
        },
        {
            "id": "25w31a",
            "type": "snapshot",
            "url": "https://piston-meta.mojang.com/v1/packages/bb/25w31a.json",
            "releaseTime": "2025-07-29T12:00:00+00:00",
        },
    ],
}


def test_fetch_manifest_via_mirrors():
    client = FakeClient(MANIFEST)
    versions, latest = fetch_manifest(client, Mirrors("bmclapi"))
    assert latest == {"release": "1.21.1", "snapshot": "25w31a"}
    assert [item.id for item in versions] == ["1.21.1", "25w31a"]
    assert versions[0].release_time == "2024-08-08T14:05:00+00:00"
    assert client.calls[0][0].endswith("/mc/game/version_manifest_v2.json")


def test_fetch_version_json_uses_official_url_after_manifest():
    client = FakeClient(MANIFEST, {"id": "1.21.1", "libraries": []})
    data = fetch_version_json(client, Mirrors("bmclapi"), "1.21.1")
    assert data["id"] == "1.21.1"
    assert len(client.calls) == 2
    assert client.calls[1][0].endswith("/version/1.21.1/json")


def test_rules_allow_defaults_and_conditions():
    rules = [
        {"action": "allow"},
        {"action": "disallow", "os": {"name": "osx"}},
    ]
    assert rules_allow(rules, os_name="windows")
    assert not rules_allow(rules, os_name="osx")
    assert not rules_allow([], os_name="windows")
    assert rules_allow(
        [{"action": "allow", "features": {"has_custom_resolution": True}}],
        os_name="windows",
        features={"has_custom_resolution": True},
    )
    assert not rules_allow(
        [{"action": "allow", "features": {"has_custom_resolution": True}}],
        os_name="windows",
        features={},
    )


def test_library_files_reads_artifact_download_metadata():
    version = {
        "libraries": [
            {
                "name": "com.example:demo:1.0",
                "downloads": {
                    "artifact": {
                        "path": "com/example/demo/1.0/demo-1.0.jar",
                        "url": "https://libraries.minecraft.net/com/example/demo/1.0/demo-1.0.jar",
                        "sha1": "cc",
                        "size": 10,
                    }
                },
            }
        ]
    }
    files = library_files(version, os_name="windows")
    assert len(files) == 1
    assert files[0].path == "com/example/demo/1.0/demo-1.0.jar"
    assert files[0].name == "com.example:demo:1.0"
    assert files[0].sha1 == "cc"


def test_library_files_adds_legacy_native_classifier():
    version = {
        "libraries": [
            {
                "name": "org.lwjgl.lwjgl:lwjgl-platform:2.9.4",
                "natives": {"windows": "natives-windows"},
                "downloads": {
                    "classifiers": {
                        "natives-windows": {
                            "path": "org/lwjgl/lwjgl/lwjgl-platform/2.9.4/lwjgl-platform-2.9.4-natives-windows.jar",
                            "url": "https://libraries.minecraft.net/natives.jar",
                            "sha1": "dd",
                            "size": 42,
                        }
                    }
                },
            }
        ]
    }
    files = library_files(version, os_name="windows")
    assert [item.path for item in files] == [
        "org/lwjgl/lwjgl/lwjgl-platform/2.9.4/lwjgl-platform-2.9.4-natives-windows.jar"
    ]


def test_categorize_and_group_versions():
    summary = VersionSummary
    versions = [
        summary("1.21.1", "release", "", "2024-08-08T14:05:00+00:00"),
        summary("25w31a", "snapshot", "", "2025-07-29T12:00:00+00:00"),
        summary("b1.7.3", "old_beta", "", "2011-07-08T00:00:00+00:00"),
        summary("24w14a", "snapshot", "", "2024-04-03T00:00:00+00:00"),
        summary("24w14potato", "snapshot", "", "2024-04-01T00:00:00+00:00"),
    ]
    assert categorize_version(versions[0]) == "release"
    assert categorize_version(versions[4]) == "april_fools"
    grouped = group_versions(versions)
    assert grouped["release"][0].id == "1.21.1"
    assert grouped["snapshot"][0].id == "25w31a"
    assert grouped["snapshot"][-1].id == "24w14a"
    assert grouped["old"][0].id == "b1.7.3"
    assert grouped["april_fools"][0].id == "24w14potato"
