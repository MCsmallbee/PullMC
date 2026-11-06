"""Unified, UI-safe error type for PullMC."""

from __future__ import annotations


class PullMCError(Exception):
    """An expected failure with a stable code and a human-readable message.

    ``detail`` carries diagnostic context that is useful in logs but not
    necessarily suitable for the primary UI message (URLs, paths, status).
    """

    def __init__(self, code: str, message: str, detail: str = "") -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.detail = detail

    def __str__(self) -> str:
        return self.message
