"""HTTP client with retries, Range resume and mirror fallback."""

from __future__ import annotations

import hashlib
import json
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Sequence

import requests

from ..errors import PullMCError

CHUNK_SIZE = 64 * 1024


class Cancelled(Exception):
    """Raised when a running download is cancelled."""


class CancelToken:
    """Small cooperative cancellation token shared with the UI layer."""

    def __init__(self) -> None:
        self._cancelled = False

    @property
    def cancelled(self) -> bool:
        return self._cancelled

    def cancel(self) -> None:
        self._cancelled = True

    def raise_if_cancelled(self) -> None:
        if self._cancelled:
            raise Cancelled()


@dataclass(frozen=True)
class DownloadSpec:
    urls: tuple[str, ...]
    dest: Path
    sha1: str | None = None
    size: int | None = None


class _Retryable(Exception):
    pass


class _SkipSource(Exception):
    pass


class _BadData(Exception):
    pass


class HttpClient:
    def __init__(self, timeout: float = 20.0, retries: int = 3) -> None:
        self.timeout = timeout
        self.retries = max(1, retries)
        self.session = requests.Session()
        self.session.headers["User-Agent"] = "PullMC/0.1"

    # ------------------------------------------------------------- JSON API

    def get_json(self, urls: Sequence[str]) -> dict:
        last_detail = "没有可用的下载地址"
        for url in urls:
            try:
                data = self.get_bytes((url,))
                parsed = json.loads(data.decode("utf-8"))
            except (PullMCError, UnicodeDecodeError, json.JSONDecodeError) as exc:
                last_detail = f"{url}: {exc}"
                continue
            if not isinstance(parsed, dict):
                last_detail = f"{url}: JSON 根节点不是对象"
                continue
            return parsed
        raise PullMCError("bad_json", "获取的 JSON 无效", last_detail)

    def get_bytes(self, urls: Sequence[str]) -> bytes:
        last_detail = "没有可用的下载地址"
        for url in urls:
            for attempt in range(self.retries):
                try:
                    response = self.session.get(
                        url,
                        timeout=(5, self.timeout),
                    )
                    status = response.status_code
                    if status in (408, 429) or status >= 500:
                        last_detail = f"{url}: HTTP {status}"
                        self._backoff(attempt)
                        continue
                    if status >= 400:
                        last_detail = f"{url}: HTTP {status}"
                        break
                    data = response.content
                    if _is_html(response, data):
                        last_detail = f"{url}: 返回了 HTML 页面"
                        break
                    return data
                except requests.RequestException as exc:
                    last_detail = f"{url}: {exc}"
                    self._backoff(attempt)
            # move on to the next mirror
        raise PullMCError("download_failed", "网络请求失败", last_detail)

    # --------------------------------------------------------- file download

    def download(
        self,
        urls: Sequence[str],
        dest: Path,
        sha1: str | None = None,
        size: int | None = None,
        on_bytes: Callable[[int], None] | None = None,
        cancel: CancelToken | None = None,
    ) -> bool:
        dest = Path(dest)
        dest.parent.mkdir(parents=True, exist_ok=True)
        part = dest.with_name(dest.name + ".part")

        if dest.exists() and self._matches(dest, sha1, size, allow_unverified=False):
            return False

        last_detail = "没有可用的下载地址"
        for url in urls:
            retried_bad = False
            retried_416 = False
            attempt = 0
            while attempt < self.retries:
                if cancel is not None:
                    cancel.raise_if_cancelled()
                try:
                    if not part.exists():
                        part.touch()
                    current = part.stat().st_size
                    if size is not None and current > size:
                        part.unlink(missing_ok=True)
                        current = 0
                    self._stream_to_part(
                        url,
                        part,
                        current,
                        on_bytes=on_bytes,
                        cancel=cancel,
                    )
                    if not self._matches(part, sha1, size, allow_unverified=True):
                        part.unlink(missing_ok=True)
                        if not retried_bad:
                            retried_bad = True
                            continue
                        last_detail = f"{url}: 校验失败"
                        break
                    os.replace(part, dest)
                    return True
                except Cancelled:
                    raise
                except _Retryable as exc:
                    last_detail = f"{url}: {exc}"
                    attempt += 1
                    self._backoff(attempt - 1)
                except _SkipSource as exc:
                    last_detail = f"{url}: {exc}"
                    break
                except _BadData as exc:
                    part.unlink(missing_ok=True)
                    if not retried_bad:
                        retried_bad = True
                        continue
                    last_detail = f"{url}: {exc}"
                    break
            # try the next mirror
        raise PullMCError("download_failed", f"下载失败：{dest.name}", last_detail)

    def _stream_to_part(
        self,
        url: str,
        part: Path,
        offset: int,
        *,
        on_bytes: Callable[[int], None] | None,
        cancel: CancelToken | None,
    ) -> None:
        headers = {"Range": f"bytes={offset}-"} if offset else {}
        try:
            response = self.session.get(
                url,
                headers=headers,
                timeout=(5, self.timeout),
                stream=True,
            )
        except requests.RequestException as exc:
            raise _Retryable(str(exc)) from exc

        with response:
            status = response.status_code
            if status == 416:
                raise _SkipSource("服务器拒绝续传范围")
            if status in (408, 429) or status >= 500:
                raise _Retryable(f"HTTP {status}")
            if status >= 400:
                raise _SkipSource(f"HTTP {status}")
            if status == 200:
                mode = "wb"
            elif status == 206:
                mode = "ab" if offset else "wb"
            else:
                raise _SkipSource(f"意外的 HTTP {status}")

            try:
                with part.open(mode) as handle:
                    for chunk in response.iter_content(CHUNK_SIZE):
                        if cancel is not None:
                            cancel.raise_if_cancelled()
                        if not chunk:
                            continue
                        handle.write(chunk)
                        if on_bytes is not None:
                            on_bytes(len(chunk))
            except requests.RequestException as exc:
                raise _Retryable(str(exc)) from exc

    # --------------------------------------------------------------- helpers

    @staticmethod
    def _matches(
        path: Path,
        sha1: str | None,
        size: int | None,
        *,
        allow_unverified: bool,
    ) -> bool:
        try:
            if size is not None and path.stat().st_size != size:
                return False
            if sha1:
                return _sha1(path) == sha1.lower()
            return allow_unverified
        except OSError:
            return False

    @staticmethod
    def _backoff(attempt: int) -> None:
        if attempt > 0:
            time.sleep(min(2.0, 0.25 * (2 ** (attempt - 1))))


def _sha1(path: Path) -> str:
    digest = hashlib.sha1()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(CHUNK_SIZE), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _is_html(response: requests.Response, data: bytes) -> bool:
    content_type = response.headers.get("Content-Type", "").lower()
    if "text/html" in content_type:
        return True
    return data.lstrip().startswith(b"<")
