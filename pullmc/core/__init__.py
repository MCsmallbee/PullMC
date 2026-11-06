"""Platform-independent PullMC core.

Nothing in this package may import PySide6 or touch the UI.
"""

from .assets import (
    AssetIndexRef,
    asset_index_ref,
    asset_objects,
    build_virtual_assets,
    virtual_asset_names,
)
from .http import CancelToken, Cancelled, DownloadSpec, HttpClient
from .manifest import (
    APRIL_FOOLS_IDS,
    CATEGORY_ORDER,
    LibraryFile,
    VersionSummary,
    categorize_version,
    fetch_manifest,
    fetch_version_json,
    group_versions,
    library_files,
    rules_allow,
    version_java_major,
)
from .maven import MavenCoord, installer_path_candidates
from .mirrors import Mirrors

__all__ = [
    "APRIL_FOOLS_IDS",
    "CATEGORY_ORDER",
    "AssetIndexRef",
    "CancelToken",
    "Cancelled",
    "DownloadSpec",
    "HttpClient",
    "LibraryFile",
    "MavenCoord",
    "Mirrors",
    "VersionSummary",
    "asset_index_ref",
    "asset_objects",
    "build_virtual_assets",
    "categorize_version",
    "fetch_manifest",
    "fetch_version_json",
    "group_versions",
    "installer_path_candidates",
    "library_files",
    "rules_allow",
    "version_java_major",
    "virtual_asset_names",
]
