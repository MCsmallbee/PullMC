"""Application entry point for the PullMC desktop UI."""

from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

from PySide6.QtCore import QTimer, Qt
from PySide6.QtWidgets import QApplication

from .app_info import AppInfo
from .i18n import I18nBackend
from .icon import build_icon
from .settings import AppSettings
from .ui.bridge import AppBridge
from .ui.home import HomeState
from .ui.resources import qml_dir


def _configure_console() -> None:
    """Keep RinUI's emoji startup log from crashing a GBK console."""

    for stream in (sys.stdout, sys.stderr):
        if stream is None or not hasattr(stream, "reconfigure"):
            continue
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (OSError, ValueError):
            pass


def _load_rinui():
    """Import RinUI from a harmless working directory.

    RinUI 0.4.x resolves its config directory from ``Path.cwd()`` at import
    time.  Importing it from the project root would create a stray ``RinUI``
    directory next to the source tree.  PullMC owns its own ``config/ui.json``
    instead, so RinUI's auto-save is disabled.
    """

    runtime_dir = Path(tempfile.gettempdir()) / "PullMC" / "rinui-runtime"
    runtime_dir.mkdir(parents=True, exist_ok=True)
    previous = Path.cwd()
    try:
        os.chdir(runtime_dir)
        from RinUI import RinUIWindow
        from RinUI.core.config import RinConfig

        RinConfig.save_config = lambda: False
    finally:
        os.chdir(previous)
    return RinUIWindow


def _capture_window(window, path: Path) -> None:
    image = window.grabWindow()
    if image.isNull():
        print(f"PullMC: could not capture window to {path}", file=sys.stderr)
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    if not image.save(str(path)):
        print(f"PullMC: could not save screenshot to {path}", file=sys.stderr)


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv if argv is None else argv)
    _configure_console()
    screenshot_path: Path | None = None
    if "--screenshot" in argv:
        index = argv.index("--screenshot")
        if index + 1 < len(argv):
            screenshot_path = Path(argv[index + 1])
    smoke = "--smoke" in argv

    rinui_window_class = _load_rinui()

    app = QApplication(argv)
    app.setApplicationName("PullMC")
    app.setOrganizationName("MCsmallbee")
    app.setApplicationDisplayName("PullMC")

    settings = AppSettings(app)
    app.setWindowIcon(build_icon(settings.effectiveAccentColor))
    i18n = I18nBackend(language=settings.language, parent=app)
    app_info = AppInfo(app)
    home = HomeState(settings, i18n, parent=app)
    bridge = AppBridge(settings, i18n, app_info, parent=app)
    app.applicationStateChanged.connect(
        lambda state: home.refresh()
        if state == Qt.ApplicationState.ApplicationActive
        else None
    )

    window = rinui_window_class(shared_engine=True)
    bridge.set_theme_manager(window.theme_manager)
    bridge.applyAppearance()
    window.engine.addImportPath(str(qml_dir()))
    context = window.engine.rootContext()
    context.setContextProperty("appInfo", app_info)
    context.setContextProperty("settings", settings)
    context.setContextProperty("i18nBackend", i18n)
    context.setContextProperty("home", home)
    context.setContextProperty("bridge", bridge)

    window.load(str(qml_dir() / "Main.qml"))
    root_window = window.root_window

    def refresh_icon() -> None:
        icon = build_icon(settings.effectiveAccentColor)
        app.setWindowIcon(icon)
        if root_window is not None:
            root_window.setIcon(icon)

    root_window.setIcon(build_icon(settings.effectiveAccentColor))
    bridge.appearanceChanged.connect(refresh_icon)

    try:
        window.theme_manager.apply_backdrop_effect(
            os.environ.get("PULLMC_BACKDROP") or settings.backdropEffect
        )
    except Exception as exc:  # Backdrop effects are best-effort.
        print(f"PullMC: backdrop effect unavailable: {exc}", file=sys.stderr)

    if screenshot_path is not None:
        root_window = window.root_window
        QTimer.singleShot(
            2_000,
            lambda: (_capture_window(root_window, screenshot_path), app.quit()),
        )
    elif smoke:
        QTimer.singleShot(2_000, app.quit)

    print("PullMC UI loaded", flush=True)
    return app.exec()
