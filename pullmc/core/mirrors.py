"""Mirror selection and URL building for Mojang and BMCLAPI."""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Callable, Literal

import requests

MirrorMode = Literal["auto", "mojang", "bmclapi"]

BMCL_BASE = "https://bmclapi2.bangbang93.com"
MOJANG_META = "https://piston-meta.mojang.com"
MOJANG_LIBRARIES = "https://libraries.minecraft.net"
MOJANG_RESOURCES = "https://resources.download.minecraft.net"
FABRIC_OFFICIAL = "https://meta.fabricmc.net"
QUILT_OFFICIAL = "https://meta.quiltmc.org"
FORGE_MAVEN = "https://maven.minecraftforge.net"
NEOFORGE_MAVEN = "https://maven.neoforged.net"


@dataclass(frozen=True)
class Manifest:
    pass


@dataclass(frozen=True)
class VersionJson:
    version_id: str
    official_url: str | None = None


@dataclass(frozen=True)
class ClientJar:
    version_id: str
    official_url: str | None = None


@dataclass(frozen=True)
class Library:
    path: str
    official_url: str | None = None


@dataclass(frozen=True)
class AssetObject:
    hash: str


@dataclass(frozen=True)
class OfficialUrl:
    url: str


@dataclass(frozen=True)
class FabricLoaderList:
    game_version: str


@dataclass(frozen=True)
class FabricProfile:
    game_version: str
    loader_version: str


@dataclass(frozen=True)
class QuiltLoaderList:
    pass


@dataclass(frozen=True)
class QuiltGameList:
    pass


@dataclass(frozen=True)
class QuiltProfile:
    game_version: str
    loader_version: str


@dataclass(frozen=True)
class ForgeVersionList:
    minecraft_version: str


@dataclass(frozen=True)
class NeoForgeVersionList:
    minecraft_version: str


@dataclass(frozen=True)
class Installer:
    path: str
    official_base: str | None = None


class Mirrors:
    def __init__(
        self,
        mode: MirrorMode = "auto",
        *,
        client=None,
        probe: Callable[[str], bool] | None = None,
        cache_seconds: float = 600.0,
    ) -> None:
        if mode not in ("auto", "mojang", "bmclapi"):
            raise ValueError(f"unknown mirror mode: {mode}")
        self.mode: MirrorMode = mode
        self.client = client
        self._probe = probe or self._default_probe
        self._cache_seconds = cache_seconds
        self._active: str | None = None
        self._expires_at = 0.0

    def active_base(self) -> str:
        if self.mode == "bmclapi":
            return BMCL_BASE
        if self.mode == "mojang":
            return MOJANG_META
        now = time.monotonic()
        if self._active is not None and now < self._expires_at:
            return self._active
        bases = [BMCL_BASE, MOJANG_META]
        reachable: list[str] = []
        for base in bases:
            try:
                if self._probe(base):
                    reachable.append(base)
            except Exception:
                pass
        self._active = reachable[0] if reachable else BMCL_BASE
        self._expires_at = now + self._cache_seconds
        return self._active

    def candidates(self, resource) -> list[str]:
        if isinstance(resource, OfficialUrl):
            return [resource.url]
        pairs = self._pairs(resource)
        if self.mode == "bmclapi":
            return [bmcl for bmcl, _ in pairs if bmcl]
        if self.mode == "mojang":
            return [official for _, official in pairs if official]
        chosen = self.active_base()
        ordered = [chosen] + [
            base for base in (BMCL_BASE, MOJANG_META) if base != chosen
        ]
        urls: list[str] = []
        for base in ordered:
            for bmcl, official in pairs:
                if base == BMCL_BASE and bmcl:
                    urls.append(bmcl)
                elif base == MOJANG_META and official:
                    urls.append(official)
        return urls

    # ------------------------------------------------------------- URL rules

    def _pairs(self, resource) -> list[tuple[str | None, str | None]]:
        if isinstance(resource, Manifest):
            return [(
                f"{BMCL_BASE}/mc/game/version_manifest_v2.json",
                f"{MOJANG_META}/mc/game/version_manifest_v2.json",
            )]
        if isinstance(resource, VersionJson):
            return [(
                f"{BMCL_BASE}/version/{resource.version_id}/json",
                resource.official_url,
            )]
        if isinstance(resource, ClientJar):
            return [(
                f"{BMCL_BASE}/version/{resource.version_id}/client",
                resource.official_url,
            )]
        if isinstance(resource, Library):
            official = resource.official_url or f"{MOJANG_LIBRARIES}/{resource.path}"
            return [(f"{BMCL_BASE}/maven/{resource.path}", official)]
        if isinstance(resource, AssetObject):
            prefix = resource.hash[:2]
            return [(
                f"{BMCL_BASE}/assets/{prefix}/{resource.hash}",
                f"{MOJANG_RESOURCES}/{prefix}/{resource.hash}",
            )]
        if isinstance(resource, FabricLoaderList):
            return [(
                f"{BMCL_BASE}/fabric-meta/v2/versions/loader/{resource.game_version}",
                f"{FABRIC_OFFICIAL}/v2/versions/loader/{resource.game_version}",
            )]
        if isinstance(resource, FabricProfile):
            suffix = f"/v2/versions/loader/{resource.game_version}/{resource.loader_version}/profile/json"
            return [(f"{BMCL_BASE}/fabric-meta{suffix}", f"{FABRIC_OFFICIAL}{suffix}")]
        if isinstance(resource, QuiltLoaderList):
            return [(
                f"{BMCL_BASE}/quilt-meta/v3/versions/loader",
                f"{QUILT_OFFICIAL}/v3/versions/loader",
            )]
        if isinstance(resource, QuiltGameList):
            return [(
                f"{BMCL_BASE}/quilt-meta/v3/versions/game",
                f"{QUILT_OFFICIAL}/v3/versions/game",
            )]
        if isinstance(resource, QuiltProfile):
            suffix = f"/v3/versions/loader/{resource.game_version}/{resource.loader_version}/profile/json"
            return [(f"{BMCL_BASE}/quilt-meta{suffix}", f"{QUILT_OFFICIAL}{suffix}")]
        if isinstance(resource, ForgeVersionList):
            return [(
                f"{BMCL_BASE}/forge/minecraft/{resource.minecraft_version}",
                f"{FORGE_MAVEN}/net/minecraftforge/forge/maven-metadata.xml",
            )]
        if isinstance(resource, NeoForgeVersionList):
            return [(
                f"{BMCL_BASE}/neoforge/list/{resource.minecraft_version}",
                f"{NEOFORGE_MAVEN}/net/neoforged/neoforge/maven-metadata.xml",
            )]
        if isinstance(resource, Installer):
            official_base = resource.official_base
            official = (
                f"{official_base.rstrip('/')}/{resource.path}"
                if official_base and resource.path
                else None
            )
            return [(f"{BMCL_BASE}/maven/{resource.path}", official)]
        raise TypeError(f"unsupported mirror resource: {resource!r}")

    def _default_probe(self, base: str) -> bool:
        url = f"{base}/mc/game/version_manifest_v2.json"
        try:
            if self.client is not None and hasattr(self.client, "session"):
                response = self.client.session.head(url, timeout=3)
            else:
                response = requests.head(url, timeout=3)
            response.close()
            return response.status_code < 500
        except Exception:
            return False
