"""Build the PullMC window icon from the SVG template."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QByteArray, QRectF, Qt
from PySide6.QtGui import QIcon, QPainter, QPixmap
from PySide6.QtSvg import QSvgRenderer

_LOGO = Path(__file__).resolve().parent / "res" / "logo.svg"
_ICON_SIZES = (16, 20, 24, 32, 40, 48, 64, 128, 256)


def build_icon(accent: str) -> QIcon:
    """Return the logo rendered in *accent*, at common Windows icon sizes."""

    svg = _LOGO.read_text(encoding="utf-8")
    svg = svg.replace('style="color: #000000;"', f'style="color: {accent};"')
    svg = svg.replace("<path ", f'<path fill="{accent}" ', 1)

    renderer = QSvgRenderer(QByteArray(svg.encode("utf-8")))
    icon = QIcon()
    for size in _ICON_SIZES:
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        renderer.render(painter, QRectF(0, 0, size, size))
        painter.end()
        icon.addPixmap(pixmap)
    return icon
