"""Minecraft asset index handling and legacy virtual asset trees."""

from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Iterable


@dataclass(frozen=True)
class AssetIndexRef:
    id: str
    url: str
    sha1: str | None = None
    size: int | None = None
    total_size: int | None = None


def asset_index_ref(version_json: dict) -> AssetIndexRef | None:
    index = version_json.get("assetIndex")
    if not isinstance(index, dict):
        return None
    index_id = index.get("id")
    url = index.get("url")
    if not isinstance(index_id, str) or not isinstance(url, str):
        return None
    return AssetIndexRef(
        id=index_id,
        url=url,
        sha1=_optional_str(index.get("sha1")),
        size=_optional_int(index.get("size")),
        total_size=_optional_int(index.get("totalSize")),
    )


def asset_objects(index_json: dict) -> Iterable[tuple[str, int]]:
    objects = index_json.get("objects")
    if not isinstance(objects, dict):
        return
    seen: set[str] = set()
    for value in objects.values():
        if not isinstance(value, dict):
            continue
        digest = value.get("hash")
        size = value.get("size")
        if not isinstance(digest, str) or not isinstance(size, int):
            continue
        if digest in seen:
            continue
        seen.add(digest)
        yield digest, size


def virtual_asset_names(index_json: dict) -> dict[str, str]:
    objects = index_json.get("objects")
    if not isinstance(objects, dict):
        return {}
    result: dict[str, str] = {}
    for name in sorted(objects):
        value = objects[name]
        if not isinstance(value, dict):
            continue
        digest = value.get("hash")
        if isinstance(digest, str) and _safe_relative(name):
            result[name] = digest
    return result


def build_virtual_assets(root: Path, index_json: dict, index_id: str) -> int:
    """Copy objects into ``assets/virtual/<index_id>/`` and return misses."""
    root = Path(root)
    source_root = root / "assets" / "objects"
    target_root = root / "assets" / "virtual" / index_id
    missing = 0
    for name, digest in virtual_asset_names(index_json).items():
        source = source_root / digest[:2] / digest
        if not source.is_file():
            missing += 1
            continue
        target = target_root.joinpath(*PurePosixPath(name).parts)
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and target.stat().st_size == source.stat().st_size:
            continue
        shutil.copyfile(source, target)
    return missing


def _safe_relative(name: str) -> bool:
    path = PurePosixPath(name)
    return bool(path.parts) and not path.is_absolute() and ".." not in path.parts


def _optional_str(value) -> str | None:
    return value if isinstance(value, str) else None


def _optional_int(value) -> int | None:
    return value if isinstance(value, int) and value >= 0 else None
