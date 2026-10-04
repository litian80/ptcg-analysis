"""Parse WebVTT / SRT captions into clean, de-duplicated timed segments.

YouTube auto-generated captions are "rolling": each cue repeats the previous
line and adds a new one, with inline word timings like
``word<00:00:01.200><c> next</c>``. We strip the markup and keep every line
only once, timed at the cue where it first appeared.
"""

from __future__ import annotations

import html
import re
from dataclasses import dataclass
from pathlib import Path

from .timeutil import parse_ts

_TIMING = re.compile(r"(\d{1,2}:)?\d{1,2}:\d{2}[.,]\d{3}\s*-->\s*(\d{1,2}:)?\d{1,2}:\d{2}[.,]\d{3}")
_TAG = re.compile(r"<[^>]+>")
_SPEAKER_NOISE = re.compile(r"\[(music|applause|laughter|__)\]", re.I)


@dataclass
class Segment:
    start: float
    end: float
    text: str

    def to_dict(self) -> dict:
        return {"start": round(self.start, 2), "end": round(self.end, 2), "text": self.text}


def _clean(line: str) -> str:
    line = html.unescape(_TAG.sub("", line))
    line = _SPEAKER_NOISE.sub("", line)
    return re.sub(r"\s+", " ", line).strip()


def _cues(text: str):
    """Yield (start, end, [lines]) for each cue in a VTT or SRT document."""
    # Walk line by line rather than splitting on blank lines: YouTube's rolling
    # cues contain whitespace-only lines inside a cue.
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    cue = None
    for i, line in enumerate(lines):
        if _TIMING.search(line):
            if cue:
                yield cue
            a, b = line.split("-->")
            cue = (parse_ts(a.strip().split()[0]), parse_ts(b.strip().split()[0]), [])
        elif cue is not None:
            # SRT cue numbers sit on their own line right before the timing line.
            nxt = lines[i + 1] if i + 1 < len(lines) else ""
            if line.strip().isdigit() and _TIMING.search(nxt):
                continue
            cue[2].append(line)
    if cue:
        yield cue


def parse_captions(text: str, offset: float = 0.0) -> list[Segment]:
    segments: list[Segment] = []
    recent: list[str] = []  # last few emitted lines, for rolling-caption dedupe
    for start, end, lines in _cues(text):
        for raw in lines:
            line = _clean(raw)
            if not line or line in recent:
                continue
            # Some rolling cues re-emit the previous line with one word added;
            # replace instead of duplicating.
            if segments and recent and line.startswith(recent[-1]) and start - segments[-1].start < 1.0:
                segments[-1].text = line
                segments[-1].end = end + offset
                recent[-1] = line
                continue
            segments.append(Segment(start + offset, end + offset, line))
            recent = (recent + [line])[-3:]
    # Rolling cues give lines overlapping end times; make them end where the next starts.
    for cur, nxt in zip(segments, segments[1:]):
        if cur.end > nxt.start:
            cur.end = nxt.start
    return segments


def load_captions(path: str | Path, offset: float = 0.0) -> list[Segment]:
    return parse_captions(Path(path).read_text(encoding="utf-8-sig", errors="replace"), offset)


def clip(segments: list[Segment], start: float | None, end: float | None) -> list[Segment]:
    return [
        s for s in segments if (start is None or s.end >= start) and (end is None or s.start <= end)
    ]


def text_between(segments: list[Segment], start: float, end: float) -> str:
    return " ".join(s.text for s in segments if s.end >= start and s.start < end)


def windows(segments: list[Segment], size: float, start: float | None = None, end: float | None = None):
    """Yield (w_start, w_end) windows covering the captions (or the given range)."""
    if start is None:
        start = segments[0].start if segments else 0.0
    if end is None:
        end = segments[-1].end if segments else start
    t = start
    while t < end:
        yield t, min(t + size, end)
        t += size
