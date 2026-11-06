"""Shared fixtures for the PullMC core test-suite."""

from __future__ import annotations

import threading
import time
import uuid
from dataclasses import dataclass, field
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest


@dataclass
class Route:
    body: bytes
    status: int = 200
    headers: dict[str, str] = field(default_factory=dict)
    ignore_range: bool = False
    slow_chunk_delay: float = 0.0


class _Handler(BaseHTTPRequestHandler):
    def log_message(self, *args) -> None:  # keep pytest output clean
        pass

    @property
    def local(self):
        return self.server.local  # type: ignore[attr-defined]

    def do_HEAD(self) -> None:  # noqa: N802
        self.local.requests.append((self.path, dict(self.headers)))
        route = self.local.routes.get(self.path)
        if route is None:
            self.send_error(404)
            return
        self.send_response(route.status)
        for key, value in route.headers.items():
            self.send_header(key, value)
        self.send_header("Content-Length", str(len(route.body)))
        self.end_headers()

    def do_GET(self) -> None:  # noqa: N802
        self.local.requests.append((self.path, dict(self.headers)))
        route = self.local.routes.get(self.path)
        if route is None:
            self.send_error(404)
            return

        body = route.body
        status = route.status
        extra_headers: dict[str, str] = {}
        range_header = self.headers.get("Range")
        if range_header and not route.ignore_range and status == 200:
            try:
                start = int(range_header.split("=", 1)[1].split("-", 1)[0])
            except (IndexError, ValueError):
                start = 0
            if start >= len(body):
                self.send_response(416)
                self.send_header("Content-Range", f"bytes */{len(body)}")
                self.end_headers()
                return
            extra_headers["Content-Range"] = f"bytes {start}-{len(body) - 1}/{len(body)}"
            body = body[start:]
            status = 206

        self.send_response(status)
        for key, value in route.headers.items():
            self.send_header(key, value)
        for key, value in extra_headers.items():
            self.send_header(key, value)
        if "Content-Type" not in route.headers:
            self.send_header("Content-Type", "application/octet-stream")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()

        if self.command == "HEAD":
            return
        try:
            if route.slow_chunk_delay:
                for offset in range(0, len(body), 4):
                    self.wfile.write(body[offset : offset + 4])
                    self.wfile.flush()
                    time.sleep(route.slow_chunk_delay)
            else:
                self.wfile.write(body)
        except (BrokenPipeError, ConnectionResetError):
            pass


class LocalServer:
    def __init__(self) -> None:
        self.routes: dict[str, Route] = {}
        self.requests: list[tuple[str, dict[str, str]]] = []
        self._httpd = ThreadingHTTPServer(("127.0.0.1", 0), _Handler)
        self._httpd.local = self  # type: ignore[attr-defined]
        self._httpd.daemon_threads = True
        self._thread = threading.Thread(target=self._httpd.serve_forever, daemon=True)
        self._thread.start()

    @property
    def port(self) -> int:
        return int(self._httpd.server_address[1])

    def route(self, path: str, body: bytes, **kwargs) -> None:
        self.routes[path] = Route(body=body, **kwargs)

    def url(self, path: str) -> str:
        return f"http://127.0.0.1:{self.port}{path}"

    def close(self) -> None:
        self._httpd.shutdown()
        self._httpd.server_close()
        self._thread.join(timeout=3)


@pytest.fixture
def server():
    local = LocalServer()
    try:
        yield local
    finally:
        local.close()


@pytest.fixture
def workdir():
    """A scratch directory that avoids pytest's restricted base temp ACL."""
    path = Path.cwd() / ".tmp" / "tests" / uuid.uuid4().hex
    path.mkdir(parents=True, exist_ok=True)
    try:
        yield path
    finally:
        try:
            for child in sorted(path.rglob("*"), reverse=True):
                if child.is_file():
                    child.unlink(missing_ok=True)
                elif child.is_dir():
                    child.rmdir()
            path.rmdir()
        except OSError:
            pass
