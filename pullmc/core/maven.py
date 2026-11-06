"""Maven coordinates and forge-installer path rules."""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class MavenCoord:
    group: str
    artifact: str
    version: str
    classifier: str | None = None
    extension: str = "jar"

    @classmethod
    def parse(cls, value: str) -> "MavenCoord":
        raw = value.strip()
        if not raw:
            raise ValueError("empty maven coordinate")
        raw, extension = _split_extension(raw)
        parts = raw.split(":")
        if len(parts) not in (3, 4) or any(not part for part in parts):
            raise ValueError(f"invalid maven coordinate: {value!r}")
        group, artifact, version = parts[:3]
        classifier = parts[3] if len(parts) == 4 else None
        return cls(group, artifact, version, classifier, extension)

    @property
    def filename(self) -> str:
        suffix = f"-{self.classifier}" if self.classifier else ""
        return f"{self.artifact}-{self.version}{suffix}.{self.extension}"

    @property
    def path(self) -> str:
        return "/".join(
            part
            for part in (
                self.group.replace(".", "/"),
                self.artifact,
                self.version,
                self.filename,
            )
            if part
        )


def _split_extension(value: str) -> tuple[str, str]:
    if "@" not in value:
        return value, "jar"
    coordinate, _, extension = value.rpartition("@")
    if not extension or "/" in extension or ":" in extension:
        raise ValueError(f"invalid maven extension: {value!r}")
    return coordinate, extension


def _installer_version(version: str) -> str:
    return (
        f"net/minecraftforge/forge/{version}/"
        f"forge-{version}-installer.jar"
    )


def installer_path_candidates(minecraft: str, forge_version: str) -> list[str]:
    """Return likely Forge installer paths, newest naming scheme first.

    Forge 1.7.10 and older published the installer under a doubled version
    (``1.7.10-10.13.4.1614-1.7.10``); modern versions use the plain
    ``<mc>-<forge>`` coordinate.
    """

    combined = f"{minecraft}-{forge_version}"
    paths = [_installer_version(combined)]
    if _minecraft_key(minecraft) <= (1, 7, 10):
        suffixed = combined if combined.endswith(f"-{minecraft}") else f"{combined}-{minecraft}"
        if suffixed != combined:
            paths.append(_installer_version(suffixed))
    return paths


def _minecraft_key(version: str) -> tuple[int, ...]:
    match = re.match(r"^(\d+(?:\.\d+)*)", version)
    if not match:
        return (999,)
    return tuple(int(part) for part in match.group(1).split("."))
