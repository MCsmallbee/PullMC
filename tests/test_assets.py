from pullmc.core.assets import (
    asset_index_ref,
    asset_objects,
    build_virtual_assets,
    virtual_asset_names,
)

INDEX = {
    "objects": {
        "minecraft/sounds/a.ogg": {"hash": "h1", "size": 1},
        "minecraft/lang/zh_cn.json": {"hash": "h2", "size": 2},
        "README": {"hash": "h1", "size": 1},
    }
}


def test_asset_index_ref_has_url_and_id():
    ref = asset_index_ref(
        {
            "assetIndex": {
                "id": "5",
                "url": "https://piston-meta.mojang.com/v1/packages/x/5.json",
            }
        }
    )
    assert ref is not None
    assert ref.id == "5"
    assert ref.url.endswith("/5.json")


def test_asset_objects_dedupes_and_keeps_index_order():
    objects = list(asset_objects(INDEX))
    assert objects == [("h1", 1), ("h2", 2)]


def test_virtual_asset_names_maps_name_to_hash():
    assert virtual_asset_names(INDEX) == {
        "README": "h1",
        "minecraft/lang/zh_cn.json": "h2",
        "minecraft/sounds/a.ogg": "h1",
    }


def test_build_virtual_assets_copies_and_reports_missing(workdir):
    src = workdir / "assets" / "objects" / "h1" / "h1"
    src.parent.mkdir(parents=True)
    src.write_bytes(b"data")
    missing = build_virtual_assets(workdir, INDEX, "legacy")
    target = workdir / "assets" / "virtual" / "legacy" / "README"
    assert target.read_bytes() == b"data"
    # h2 has no object file in this fixture
    assert missing == 1
