"""Standard format seasons (rotations) from data/formats/standard_rotations.json."""
from __future__ import annotations

import datetime as dt
import json
from dataclasses import dataclass, field

from .paths import FORMATS


@dataclass
class Season:
    id: str
    tournament_start: dt.date
    tcg_live_start: dt.date
    legal_regulation_marks: list
    rotated_out: list
    banned: list = field(default_factory=list)
    sources: list = field(default_factory=list)


def load_seasons() -> list[Season]:
    raw = json.loads((FORMATS / "standard_rotations.json").read_text(encoding="utf-8"))
    out = []
    for s in raw["seasons"]:
        out.append(Season(
            id=s["id"],
            tournament_start=dt.date.fromisoformat(s["tournament_start"]),
            tcg_live_start=dt.date.fromisoformat(s["tcg_live_start"]),
            legal_regulation_marks=s["legal_regulation_marks"],
            rotated_out=s["rotated_out"],
            banned=s.get("banned", []),
            sources=s.get("sources", []),
        ))
    return sorted(out, key=lambda s: s.tournament_start)


def season_for(date: dt.date | str, *, live: bool = False) -> Season:
    """The Standard season in force on `date` (in-person by default, TCG Live if live=True)."""
    if isinstance(date, str):
        date = dt.date.fromisoformat(date)
    current = None
    for s in load_seasons():
        start = s.tcg_live_start if live else s.tournament_start
        if start <= date:
            current = s
    if current is None:
        raise ValueError(f"no Standard season on record for {date}")
    return current
