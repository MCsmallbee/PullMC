import logging
import subprocess
import sys
from pathlib import Path

from pullmc.logging_setup import ConsoleWindow, build_console_command, create_log_file, setup_logging


def test_create_log_file_is_unique_and_in_logs_dir(workdir):
    first = create_log_file(workdir)
    second = create_log_file(workdir)

    assert first.parent == workdir / "logs"
    assert second.parent == workdir / "logs"
    assert first.suffix == ".log"
    assert first != second
    assert first.exists()
    assert second.exists()


def test_setup_logging_captures_logging_and_print(workdir):
    session = setup_logging(workdir)
    try:
        logging.getLogger("pullmc.test").info("记录一条日志")
        print("打印一行调试信息", file=sys.stderr)
        session.file_handler.flush()
        text = session.path.read_text(encoding="utf-8")
    finally:
        session.close()

    assert "记录一条日志" in text
    assert "打印一行调试信息" in text
    assert session.path.parent == workdir / "logs"


def test_console_command_quotes_the_log_path(workdir):
    log_path = workdir / "logs" / "a b.log"
    command = build_console_command(log_path)

    joined = " ".join(command)
    assert "cmd.exe" in command[0].lower()
    assert "Get-Content" in joined
    assert "a b.log" in joined


def test_setup_logging_restores_streams(workdir):
    original_stdout = sys.stdout
    session = setup_logging(workdir)
    assert sys.stdout is not original_stdout
    session.close()
    assert sys.stdout is original_stdout


def test_console_start_reports_failure_when_process_exits(monkeypatch, workdir):
    class _ExitedProcess:
        def poll(self):
            return 1

    monkeypatch.setattr(subprocess, "Popen", lambda *args, **kwargs: _ExitedProcess())
    console = ConsoleWindow(workdir / "pullmc.log")

    assert console.start() is False
