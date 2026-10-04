"""Caption-only analysis: card mentions and game actions with timestamps.

This needs no API key and is cheap, so it always runs. It is also what lets
the vision step look at the right frames and gives it card-name hints.
"""

from __future__ import annotations

import re

from collections import Counter
from dataclasses import dataclass, field

from .captions import Segment
from .lexicon import CardMatcher, find_actions


@dataclass
class Event:
    t: float
    kind: str  # "card" or an ACTION_PATTERNS key
    detail: str
    text: str

    def to_dict(self) -> dict:
        return {"t": round(self.t, 2), "kind": self.kind, "detail": self.detail, "text": self.text}


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


def analyze_captions(segments: list[Segment], matcher: CardMatcher | None) -> CaptionAnalysis:
    result = CaptionAnalysis()
    cased = any(seg.text != seg.text.lower() for seg in segments)
    for seg in segments:
        if matcher is not None:
            for name, _matched, _score in matcher.find(seg.text, cased):
                result.events.append(Event(seg.start, "card", name, seg.text))
                result.card_counts[name] += 1
        for kind, phrase in find_actions(seg.text):
            result.events.append(Event(seg.start, kind, phrase, seg.text))
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
        if e.kind == "game_end" and (not ends or e.t - ends[-1] > min_gap):
            ends.append(e.t)
    if not events:
        return []
    spans = []
    start = events[0].t
    for end in ends:
        spans.append((start, end))
        # "game one" after game one ended is a recap, not the start of game two.
        nxt = [e.t for e in events if e.kind == "game_start" and e.t > end and _game_number(e.detail) in (None, len(spans) + 1)]
        start = nxt[0] if nxt else end
    after = [e for e in events if ends and e.t > ends[-1]]
    if not ends or any(e.kind == "game_start" for e in after) or (after and after[-1].t - start > min_gap):
        spans.append((start, None))
    return spans
