import pytest

from pullmc.core.mirrors import (
    AssetObject,
    FabricLoaderList,
    FabricProfile,
    Library,
    Manifest,
    Mirrors,
    OfficialUrl,
    VersionJson,
)


@pytest.mark.parametrize(
    "resource,expected",
    [
        (Manifest(), "https://bmclapi2.bangbang93.com/mc/game/version_manifest_v2.json"),
        (
            VersionJson("1.20.1", "https://piston-meta.mojang.com/v1/packages/x/1.20.1.json"),
            "https://bmclapi2.bangbang93.com/version/1.20.1/json",
        ),
        (
            Library("net/minecraft/client/1.20.1/client-1.20.1.jar", "https://libraries.minecraft.net/x.jar"),
            "https://bmclapi2.bangbang93.com/maven/net/minecraft/client/1.20.1/client-1.20.1.jar",
        ),
        (
            AssetObject("abcdef0123456789"),
            "https://bmclapi2.bangbang93.com/assets/ab/abcdef0123456789",
        ),
        (OfficialUrl("https://piston-meta.mojang.com/asset-index.json"), "https://piston-meta.mojang.com/asset-index.json"),
        (
            FabricLoaderList("1.21.1"),
            "https://bmclapi2.bangbang93.com/fabric-meta/v2/versions/loader/1.21.1",
        ),
        (
            FabricProfile("1.21.1", "0.16.0"),
            "https://bmclapi2.bangbang93.com/fabric-meta/v2/versions/loader/1.21.1/0.16.0/profile/json",
        ),
    ],
)
def test_bmclapi_candidates(resource, expected):
    assert Mirrors("bmclapi").candidates(resource) == [expected]


def test_mojang_candidates():
    mirrors = Mirrors("mojang")
    assert (
        mirrors.candidates(Manifest())[0]
        == "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"
    )
    assert mirrors.candidates(OfficialUrl("https://example/x")) == ["https://example/x"]


def test_auto_probes_once_then_uses_bmclapi():
    calls: list[str] = []

    def probe(base: str) -> bool:
        calls.append(base)
        return "bmclapi" in base

    mirrors = Mirrors("auto", client=None, probe=probe)
    assert mirrors.active_base() == "https://bmclapi2.bangbang93.com"
    assert mirrors.active_base() == "https://bmclapi2.bangbang93.com"
    assert len(calls) == 2
