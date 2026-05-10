"""
Shared helpers for the GUI application.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class StatusMessage:
    """Represents a UI status message."""

    text: str
    kind: str = "info"  # info | success | warning | error


def normalize_key_26_upper(key: str) -> str:
    """Normalize a monoalphabetic key and validate it is 26 letters A-Z."""
    key = (key or "").strip().upper()
    return key


def safe_int(value: str, default: int | None = None) -> int | None:
    """Parse an int from a string, returning default on failure."""
    try:
        return int(str(value).strip())
    except Exception:
        return default

