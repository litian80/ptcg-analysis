"""Pick the card names that were legal when a match was played.

The repo's data directory (built by the data pipeline) holds, per Standard
season, the legal card pool and the dates each season started:

* ``data/formats/standard_rotations.json`` with ``seasons[].id``,
  ``tournament_start`` and ``tcg_live_start``
* ``data/formats/<season id>/card_pool.csv`` with ``name`` and ``supertype``

Matching captions against only the cards legal at the time removes most
false matches against old cards ("Dragapult V" for "Dragapult ex").
"""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path

ROTATIONS = Path("formats") / "standard_rotations.json"


@dataclass
class CardPool:
    season: str
    names: list[str]
    supertypes: dict[str, str]  # name -> "Pokémon" / "Trainer" / "Energy"
    path: Path


def find_data_dir(*starts: Path) -> Path | None:
    """Walk up from each start directory looking for data/formats/standard_rotations.json."""
    for start in starts:
        for d in [start.resolve(), *start.resolve().parents]:
            if (d / "data" / ROTATIONS).exists():
                return d / "data"
    return None


def parse_date(value: str | date | None) -> date | None:
    """Accept yt-dlp's '20260830', ISO '2026-08-30', or a date."""
    if value is None or value == "":
        return None
    if isinstance(value, date):
        return value
    s = str(value).strip()
    if len(s) == 8 and s.isdigit():
        return date(int(s[:4]), int(s[4:6]), int(s[6:]))
    return date.fromisoformat(s[:10])


def season_for(data_dir: Path, when: date | None, live: bool = False) -> str:
    """The season in effect on `when` (today when `when` is unknown).

    TCG Live rotates a couple of weeks before in-person events, so Live videos
    use tcg_live_start as the cutoff.
    """
    seasons = json.loads((data_dir / ROTATIONS).read_text(encoding="utf-8-sig"))["seasons"]
    key = "tcg_live_start" if live else "tournament_start"
    dated = sorted(
        ((parse_date(s.get(key) or s.get("tournament_start")), s["id"]) for s in seasons),
        key=lambda x: x[0],
    )
    if not dated:
        raise ValueError(f"no seasons in {data_dir / ROTATIONS}")
    when = when or date.today()
    started = [sid for start, sid in dated if start <= when]
    if not started:
        raise ValueError(f"{when} is before the first season on record ({dated[0][1]})")
    return started[-1]


def load_pool(data_dir: Path, season: str) -> CardPool:
    path = data_dir / "formats" / season / "card_pool.csv"
    if not path.exists():
        raise FileNotFoundError(f"no card pool for season {season}: {path}")
    supertypes: dict[str, str] = {}
    with path.open(newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            name = (row.get("name") or "").strip()
            if name:
                supertypes.setdefault(name, (row.get("supertype") or "").strip())
    return CardPool(season, sorted(supertypes), supertypes, path)
