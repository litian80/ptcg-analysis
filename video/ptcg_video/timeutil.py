"""Timestamp helpers shared by the pipeline."""

from __future__ import annotations


def parse_ts(value: str | float | int | None) -> float | None:
    """Parse '1:02:03', '62:03', '3723', '3723.5' or a number into seconds."""
    if value is None or value == "":
        return None
    if isinstance(value, (int, float)):
        return float(value)
    parts = value.strip().replace(",", ".").split(":")
    if len(parts) > 3:
        raise ValueError(f"bad timestamp: {value!r}")
    seconds = 0.0
    for part in parts:
        seconds = seconds * 60 + float(part)
    return seconds


def fmt_ts(seconds: float) -> str:
    """Format seconds as H:MM:SS (or M:SS under an hour)."""
    seconds = max(0, int(round(seconds)))
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"
