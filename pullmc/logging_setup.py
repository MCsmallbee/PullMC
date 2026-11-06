"""Per-launch log files and the optional debug console window."""

from __future__ import annotations

import logging
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

_LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
_OWNED = "_pullmc_owned_handlers"


def logs_dir(data_dir: Path | None = None) -> Path:
    from .paths import app_data_dir

    return (data_dir or app_data_dir()) / "logs"


def create_log_file(data_dir: Path | None = None) -> Path:
    """Create a fresh log file so every launch has its own history."""

    directory = logs_dir(data_dir)
    directory.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    path = directory / f"pullmc-{stamp}.log"
    path.touch(exist_ok=True)
    return path


def build_console_command(log_path: Path) -> list[str]:
    """Return the command for a console that tails the current log."""

    escaped = str(log_path).replace("'", "''")
    tail = (
        "title PullMC 控制台 & powershell -NoLogo -NoProfile "
        f'-Command "Get-Content -LiteralPath \'{escaped}\' -Wait -Tail 50"'
    )
    return ["cmd.exe", "/k", tail]


class ConsoleWindow:
    """A small wrapper around the separate command window."""

    def __init__(self, log_path: Path) -> None:
        self.log_path = log_path
        self.process: subprocess.Popen | None = None

    def start(self) -> bool:
        if os.name != "nt":
            return False
        if self.process is not None and self.process.poll() is None:
            return True
        try:
            flags = getattr(subprocess, "CREATE_NEW_CONSOLE", 0)
            self.process = subprocess.Popen(
                build_console_command(self.log_path),
                cwd=str(self.log_path.parent),
                creationflags=flags,
                close_fds=True,
            )
        except OSError:
            self.process = None
            return False
        time.sleep(0.2)
        if self.process.poll() is not None:
            self.process = None
            return False
        return True

    def stop(self) -> None:
        process = self.process
        self.process = None
        if process is None or process.poll() is not None:
            return
        try:
            process.terminate()
        except OSError:
            pass


class _Tee:
    def __init__(self, stream, logger: logging.Logger) -> None:
        self._stream = stream
        self._logger = logger

    def write(self, text: str) -> int:
        written = self._stream.write(text)
        message = text.rstrip("\r\n")
        if message:
            self._logger.info("%s", message)
        return written

    def flush(self) -> None:
        self._stream.flush()

    def __getattr__(self, name: str):
        return getattr(self._stream, name)


class LogSession:
    def __init__(
        self,
        path: Path,
        file_handler: logging.Handler,
        console_handler: logging.Handler | None,
        old_stdout,
        old_stderr,
        console: ConsoleWindow,
    ) -> None:
        self.path = path
        self.file_handler = file_handler
        self.console_handler = console_handler
        self._old_stdout = old_stdout
        self._old_stderr = old_stderr
        self._console = console
        self._closed = False

    def start_console(self) -> bool:
        return self._console.start()

    def stop_console(self) -> None:
        self._console.stop()

    def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        self.stop_console()
        root = logging.getLogger()
        for handler in (self.file_handler, self.console_handler):
            if handler is not None:
                handler.flush()
                root.removeHandler(handler)
                handler.close()
        owned = getattr(root, _OWNED, [])
        if isinstance(owned, list):
            for handler in (self.file_handler, self.console_handler):
                if handler in owned:
                    owned.remove(handler)
        if isinstance(sys.stdout, _Tee):
            sys.stdout = self._old_stdout
        if isinstance(sys.stderr, _Tee):
            sys.stderr = self._old_stderr


def setup_logging(data_dir: Path | None = None) -> LogSession:
    """Install file logging and mirror print/stdout/stderr into the log."""

    path = create_log_file(data_dir)
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    owned = getattr(root, _OWNED, None)
    if not isinstance(owned, list):
        owned = []
        setattr(root, _OWNED, owned)

    file_handler = logging.FileHandler(path, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(_LOG_FORMAT, _DATE_FORMAT))
    root.addHandler(file_handler)
    owned.append(file_handler)

    old_stdout, old_stderr = sys.stdout, sys.stderr
    console_handler = None
    if old_stderr is not None:
        console_handler = logging.StreamHandler(old_stderr)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter(_LOG_FORMAT, _DATE_FORMAT))
        root.addHandler(console_handler)
        owned.append(console_handler)

    if old_stdout is not None:
        sys.stdout = _Tee(old_stdout, logging.getLogger("stdout"))
    if old_stderr is not None:
        sys.stderr = _Tee(old_stderr, logging.getLogger("stderr"))

    session = LogSession(path, file_handler, console_handler, old_stdout, old_stderr, ConsoleWindow(path))
    logging.getLogger("pullmc").info("日志文件：%s", path)
    return session
