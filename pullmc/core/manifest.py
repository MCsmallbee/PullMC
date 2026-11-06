"""Version manifest, version JSON, rules and library parsing."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Iterable

from ..errors import PullMCError
from .mirrors import Manifest, Mirrors, VersionJson

CATEGORY_ORDER = ("release", "snapshot", "old", "april_fools")

# Curated Mojang April Fools versions.  Anything not in this set follows the
# manifest type, which keeps unknown future snapshots classified as snapshots
# instead of silently becoming "old".
APRIL_FOOLS_IDS = frozenset(
    {
        "2.0",
        "15w14a",
        "1.RV-Pre1",
        "3D Shareware v1.34",
        "20w14infinite",
        "22w13oneblockatatime",
        "23w13a_or_b",
        "24w14potato",
        "25w14craftmine",
    }
)


@dataclass(frozen=True)
class VersionSummary:
    id: str
    type: str
    url: str
    release_time: str
    sha1: str | None = None
    size: int | None = None


@dataclass(frozen=True)
class LibraryFile:
    path: str
    name: str = ""
    official_url: str | None = None
    sha1: str | None = None
    size: int | None = None


def fetch_manifest(client, mirrors: Mirrors) -> tuple[list[VersionSummary], dict[str, str]]:
    data = client.get_json(mirrors.candidates(Manifest()))
    raw_versions = data.get("versions")
    if not isinstance(raw_versions, list):
        raise PullMCError("bad_manifest", "版本清单格式不正确", "versions 不是数组")
    versions: list[VersionSummary] = []
    for entry in raw_versions:
        if not isinstance(entry, dict):
            continue
        version_id = entry.get("id")
        version_type = entry.get("type")
        url = entry.get("url")
        release_time = entry.get("releaseTime")
        if not (
            isinstance(version_id, str)
            and isinstance(version_type, str)
            and isinstance(url, str)
            and isinstance(release_time, str)
        ):
            continue
        versions.append(
            VersionSummary(
                id=version_id,
                type=version_type,
                url=url,
                release_time=release_time,
                sha1=_optional_str(entry.get("sha1")),
                size=_optional_int(entry.get("size")),
            )
        )
    latest = data.get("latest")
    return versions, latest if isinstance(latest, dict) else {}


def fetch_version_json(client, mirrors: Mirrors, version_id: str) -> dict:
    versions, _ = fetch_manifest(client, mirrors)
    summary = next((item for item in versions if item.id == version_id), None)
    if summary is None:
        raise PullMCError("unknown_version", f"找不到 Minecraft {version_id}", version_id)
    return client.get_json(mirrors.candidates(VersionJson(summary.id, summary.url)))


def categorize_version(version: VersionSummary) -> str:
    if version.id in APRIL_FOOLS_IDS:
        return "april_fools"
    if version.type == "release":
        return "release"
    if version.type == "snapshot":
        return "snapshot"
    return "old"


def group_versions(versions: Iterable[VersionSummary]) -> dict[str, list[VersionSummary]]:
    grouped: dict[str, list[VersionSummary]] = {key: [] for key in CATEGORY_ORDER}
    for version in versions:
        grouped[categorize_version(version)].append(version)
    for items in grouped.values():
        items.sort(key=_release_sort_key, reverse=True)
    return grouped


def rules_allow(
    rules: Iterable[dict] | None,
    *,
    os_name: str = "windows",
    os_arch: str = "x86_64",
    os_version: str = "",
    features: dict[str, bool] | None = None,
) -> bool:
    if rules is None:
        return True
    rules = list(rules)
    if not rules:
        return False
    features = features or {}
    allowed = False
    for rule in rules:
        if not isinstance(rule, dict):
            continue
        if not _rule_matches(rule, os_name, os_arch, os_version, features):
            continue
        allowed = rule.get("action") == "allow"
    return allowed


def library_files(
    version_json: dict,
    *,
    os_name: str = "windows",
    os_arch: str = "x86_64",
    features: dict[str, bool] | None = None,
) -> list[LibraryFile]:
    result: list[LibraryFile] = []
    seen: set[str] = set()
    for library in version_json.get("libraries", []):
        if not isinstance(library, dict):
            continue
        if not rules_allow(
            library.get("rules"),
            os_name=os_name,
            os_arch=os_arch,
            features=features,
        ):
            continue
        name = library.get("name") if isinstance(library.get("name"), str) else ""
        downloads = library.get("downloads")
        artifact = downloads.get("artifact") if isinstance(downloads, dict) else None
        if isinstance(artifact, dict):
            path = artifact.get("path")
            if isinstance(path, str) and path not in seen:
                seen.add(path)
                result.append(
                    LibraryFile(
                        path=path,
                        name=name,
                        official_url=_optional_str(artifact.get("url")),
                        sha1=_optional_str(artifact.get("sha1")),
                        size=_optional_int(artifact.get("size")),
                    )
                )

        natives = library.get("natives")
        if isinstance(natives, dict) and isinstance(downloads, dict):
            classifier = natives.get(os_name)
            classifiers = downloads.get("classifiers")
            if isinstance(classifier, str) and isinstance(classifiers, dict):
                entry = classifiers.get(classifier)
                if isinstance(entry, dict):
                    path = entry.get("path")
                    if isinstance(path, str) and path not in seen:
                        seen.add(path)
                        result.append(
                            LibraryFile(
                                path=path,
                                name=name,
                                official_url=_optional_str(entry.get("url")),
                                sha1=_optional_str(entry.get("sha1")),
                                size=_optional_int(entry.get("size")),
                            )
                        )
    return result


def version_java_major(version_json: dict) -> int | None:
    java = version_json.get("javaVersion")
    if not isinstance(java, dict):
        return None
    major = java.get("majorVersion")
    return major if isinstance(major, int) and major > 0 else None


def _rule_matches(
    rule: dict,
    os_name: str,
    os_arch: str,
    os_version: str,
    features: dict[str, bool],
) -> bool:
    conditions = rule.get("os")
    if isinstance(conditions, dict):
        expected_name = conditions.get("name")
        if isinstance(expected_name, str) and expected_name != os_name:
            return False
        expected_arch = conditions.get("arch")
        if isinstance(expected_arch, str) and not _arch_matches(expected_arch, os_arch):
            return False
        expected_version = conditions.get("version")
        if isinstance(expected_version, str) and not re.search(expected_version, os_version):
            return False
    rule_features = rule.get("features")
    if isinstance(rule_features, dict):
        for key, expected in rule_features.items():
            if bool(features.get(key, False)) != bool(expected):
                return False
    return True


def _arch_matches(expected: str, actual: str) -> bool:
    if expected == "x86":
        return actual in {"x86", "i386", "i686"}
    return expected == actual


def _release_sort_key(version: VersionSummary) -> datetime:
    try:
        return datetime.fromisoformat(version.release_time.replace("Z", "+00:00"))
    except ValueError:
        return datetime.min.replace(tzinfo=timezone.utc)


def _optional_str(value: Any) -> str | None:
    return value if isinstance(value, str) else None


def _optional_int(value: Any) -> int | None:
    return value if isinstance(value, int) and value >= 0 else None
