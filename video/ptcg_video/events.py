"""Caption-only analysis: card mentions and game actions with timestamps.

This needs no API key and is cheap, so it always runs. It is also what lets
the vision step look at the right frames and gives it card-name hints.
"""

from __future__ import annotations

import re

from collections import Counter
from dataclasses import dataclass, field

from .captions import Segment
from .lexicon import CardMatcher, find_actions, is_definite


@dataclass
class Event:
    t: float
    kind: str  # "card" or an ACTION_PATTERNS key
    detail: str
    text: str
    # False for knockout/prize lines that are casters discussing a possibility.
    definite: bool = True

    def to_dict(self) -> dict:
        return {"t": round(self.t, 2), "kind": self.kind, "detail": self.detail, "text": self.text,
                "definite": self.definite}


@dataclass
class CaptionAnalysis:
    events: list[Event] = field(default_factory=list)
    card_counts: Counter = field(default_factory=Counter)
    # (start, end) guesses for each game in the video, from caster phrases.
    games: list[tuple[float, float | None]] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "events": [e.to_dict() for e in self.events],
            "card_counts": self.card_counts.most_common(),
            "games": [{"start": s, "end": e} for s, e in self.games],
        }

    def cards_between(self, start: float, end: float) -> list[str]:
        return sorted({e.detail for e in self.events if e.kind == "card" and start <= e.t < end})


def analyze_captions(segments: list[Segment], matcher: CardMatcher | None, year: int | None = None) -> CaptionAnalysis:
    """year: the video's year, so "your 2024 world champion" in a 2026 video reads as an intro."""
    result = CaptionAnalysis()
    cased = any(seg.text != seg.text.lower() for seg in segments)
    prev: Segment | None = None
    for seg in segments:
        if matcher is not None:
            for name, _matched, _score in matcher.find(seg.text, cased):
                result.events.append(Event(seg.start, "card", name, seg.text))
                result.card_counts[name] += 1
        # Auto-captions break sentences across lines: "if he finds the Boss" / "that's game".
        before = ""
        if prev is not None and seg.start - prev.start <= 6 and not prev.text.rstrip().endswith((".", "!", "?")):
            before = prev.text
        for kind, phrase in find_actions(seg.text):
            result.events.append(Event(seg.start, kind, phrase, seg.text, is_definite(kind, seg.text, before, year)))
        prev = seg
    result.games = _game_spans(result.events)
    return result


_NUMBERS = {"one": 1, "two": 2, "three": 3, "1": 1, "2": 2, "3": 3}


def _game_number(phrase: str) -> int | None:
    m = re.search(r"\bgame (one|two|three|1|2|3)\b", phrase)
    return _NUMBERS[m.group(1)] if m else None


def _game_spans(events: list[Event], min_gap: float = 120.0) -> list[tuple[float, float | None]]:
    """Split the timeline into games at 'game end' phrases.

    Casters say "that's game" / "concedes" at the end of each game; a new game
    starts at the next 'game start' cue (or right after the end).
    """
    ends = []
    for e in events:
        if e.kind == "game_end" and e.definite and (not ends or e.t - ends[-1] > min_gap):
            ends.append(e.t)
    if not events:
        return []
    spans = []
    start = events[0].t
    for k, end in enumerate(ends):
        spans.append((start, end))
        next_end = ends[k + 1] if k + 1 < len(ends) else float("inf")
        # "game one" after game one ended is a recap, not the start of game two.
        nxt = [
            e.t for e in events
            if e.kind == "game_start" and end < e.t < next_end and _game_number(e.detail) in (None, len(spans) + 1)
        ]
        start = nxt[0] if nxt else end
    after = [e for e in events if ends and e.t > ends[-1]]
    if not ends or any(e.kind == "game_start" for e in after) or (after and after[-1].t - start > min_gap):
        # The last game often ends without "that's game": a deck-out, or the
        # casters going straight to "your new world champion". Take the last
        # such call; earlier ones are hype ("one game away from being ...").
        calls = [e.t for e in events if e.kind == "match_end" and e.definite and e.t > start + min_gap]
        spans.append((start, calls[-1] if calls else None))
    return spans


def game_at(games: list[tuple[float, float | None]], t: float) -> int | None:
    """1-based number of the game span containing t, or None."""
    for i, (a, b) in enumerate(games, 1):
        if a <= t and (b is None or t <= b):
            return i
    return None


def split_at(games: list[tuple[float, float | None]], cuts: list[float]) -> list[tuple[float, float | None]]:
    """Split game spans at chapter starts: a game never runs across a chapter
    boundary (streams usually have one chapter per match)."""
    out = []
    for a, b in games:
        for c in sorted(cuts):
            if a < c and (b is None or c < b):
                out.append((a, c))
                a = c
        out.append((a, b))
    return out


def parse_games(spec: str) -> list[tuple[float, float | None]]:
    """'43:40-53:20,53:40-1:04:20' -> [(2620, 3200), (3220, 3860)]; an open end ('1:16:20-') is None."""
    from .timeutil import parse_ts

    games = []
    for part in spec.split(","):
        a, sep, b = part.strip().partition("-")
        if not sep or not a:
            raise ValueError(f"bad game range {part!r}: expected START-END, e.g. 43:40-53:20")
        start, end = parse_ts(a), parse_ts(b) if b else None
        if end is not None and end <= start:
            raise ValueError(f"game range {part!r} ends before it starts")
        games.append((start, end))
    return games
