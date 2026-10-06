"""Goldfish Monte Carlo: how often a deck sets up on its own, with no opponent.

Only answers "the deck's own probability" questions (setup speed, hand size, energy,
prized cards, bench space). Interaction (item lock, hand disruption, knockouts) is out
of scope by design. Card effects follow the printed texts; each deck module plays a
simple greedy policy, not a strong player, so numbers lean conservative.

    python -m ptcg.goldfish <deck-slug|all> [games]

Results go to data/goldfish/<slug>.json (summary: data/goldfish/README.md).
"""
from __future__ import annotations

from .alakazam_dudunsparce import AlakazamDudunsparce
from .alakazam_dusknoir import AlakazamDusknoir
from .basic_box import BasicBox
from .core import Deck, Game, modified, simulate
from .crustle import Crustle
from .dragapult import Dragapult
from .slowking import Slowking

DECKS: dict[str, type[Deck]] = {d.SLUG: d for d in (
    AlakazamDudunsparce, BasicBox, AlakazamDusknoir, Crustle, Dragapult, Slowking,
)}


def variants(slug: str, **opts) -> list[Deck]:
    """Deck instances whose metrics are merged (Basic Box runs one policy per main attacker)."""
    cls = DECKS[slug]
    if cls is BasicBox:
        return [BasicBox(plan="Latias ex", **opts), BasicBox(plan="Mega Kangaskhan ex", **opts)]
    return [cls(**opts)]


def run_deck(slug: str, games: int, seed: int = 1, change: dict | None = None, opts: dict | None = None) -> dict:
    """{side: {metric: value}} for one deck (optionally with a list change / policy options)."""
    out: dict[str, dict] = {}
    for d in variants(slug, **(opts or {})):
        lst = modified(d.LIST, change) if change else None
        for side, rows in simulate(d, games, seed, lst).items():
            merged = out.setdefault(side, {})
            for k, v in rows.items():
                merged.setdefault(k, v)
    return out


def delta(base: dict, new: dict) -> dict:
    """Per side and metric: change in percentage points for rates, raw for means."""
    out = {}
    for side in base:
        out[side] = {}
        for k, v in base[side].items():
            w = new[side].get(k)
            if v is None or w is None:
                continue
            out[side][k] = round(w - v, 2) if "均值" in k else round((w - v) * 100, 1)
    return out


def report(slug: str, games: int, seed: int = 1) -> dict:
    cls = DECKS[slug]
    base = run_deck(slug, games, seed)
    tun = []
    for t in cls().tunings():
        res = run_deck(slug, games, seed, t.get("change"), t.get("opts"))
        tun.append({**t, "results": res, "delta_pp": delta(base, res)})
    return {
        "slug": slug, "name": cls.NAME, "list_source": cls.SOURCE, "games_per_side": games, "seed": seed,
        "list": cls.LIST, "modelled": (cls.__module__ and __import__(cls.__module__, fromlist=["x"]).__doc__ or "").strip(),
        "blanks": cls.BLANKS, "notes": cls.NOTES, "results": base, "tuning": tun,
    }
