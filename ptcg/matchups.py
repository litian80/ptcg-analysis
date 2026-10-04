"""Which cards move a specific matchup, from the published decklists and round-by-round results.

    python -m ptcg.matchups                      # latest two windows (e.g. TEF-30C + TEF-PBL)
    python -m ptcg.matchups TEF-30C TEF-PBL

For every pair of archetypes (A vs B) it compares A's match record when A's list plays a card
with A's record when it does not. Only players with a published list count, and Limitless
publishes lists for the top finishers, so the absolute rates are inflated; the difference
between "with" and "without" is the useful part, and only when both sides have enough games.

Writes data/matchups/tech_<window>.json. The hand-written matchup guides in data/matchups/<slug>.md
cite these numbers.
"""
from __future__ import annotations

import collections
import csv
import json
import sys

from .archetypes import _entries
from .limitless import load_index
from .paths import DATA, TOURNAMENTS
from .selection import TIE, _known, _windows_by_date

OUT = DATA / "matchups"
MIN_GAMES = 25      # pairs with fewer list-backed games are left out
MIN_SIDE = 10       # each of "with" and "without" needs at least this many games
LOW, HIGH = 0.12, 0.88   # cards in nearly every list (or almost none) can't be compared


def _rate(results):
    return (sum(r == "W" for r in results) + TIE * sum(r == "T" for r in results)) / len(results)


def _read_csv(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def stats(windows: list[str]) -> dict:
    lists = {}                                   # (event dir, labs player id) -> {card name: copies}
    games = collections.defaultdict(list)        # (a, b) -> [(player key, "W"/"L"/"T")]
    events = [e for e in load_index() if e["format_code"] in windows]
    for e in events:
        d = TOURNAMENTS / e["dir"]
        by_placing = {r["placing"]: r["labs_player_id"] for r in _read_csv(d / "standings.csv")}
        with open(d / "decklists.jsonl", encoding="utf-8") as f:
            for line in f:
                deck = json.loads(line)
                pid = by_placing.get(str(deck["placing"]))
                if pid:
                    cards = collections.Counter()
                    for c in _entries(deck):
                        cards[c["name"]] += c["count"]
                    lists[(e["dir"], pid)] = cards
        for m in _read_csv(d / "matches.csv"):
            a, b, res = m["p1_archetype_slug"], m["p2_archetype_slug"], m["result"]
            if res not in ("p1", "p2", "tie") or a == b or not _known(a) or not _known(b):
                continue
            ra = {"p1": "W", "p2": "L", "tie": "T"}[res]
            rb = {"W": "L", "L": "W", "T": "T"}[ra]
            games[(a, b)].append(((e["dir"], m["p1_id"]), ra))
            games[(b, a)].append(((e["dir"], m["p2_id"]), rb))

    pairs = {}
    for (a, b), gs in games.items():
        gs = [(k, r) for k, r in gs if k in lists]
        if len(gs) < MIN_GAMES:
            continue
        seen = collections.Counter(name for k, _ in gs for name in lists[k])
        cards = []
        for name, n in seen.items():
            if not LOW <= n / len(gs) <= HIGH:
                continue
            with_ = [r for k, r in gs if name in lists[k]]
            without = [r for k, r in gs if name not in lists[k]]
            if len(with_) < MIN_SIDE or len(without) < MIN_SIDE:
                continue
            cards.append({"card": name, "in_lists": round(n / len(gs), 2),
                          "with": round(_rate(with_), 3), "with_games": len(with_),
                          "without": round(_rate(without), 3), "without_games": len(without),
                          "delta": round(_rate(with_) - _rate(without), 3)})
        cards.sort(key=lambda c: -abs(c["delta"]))
        pairs.setdefault(a, {})[b] = {"games": len(gs), "win_rate": round(_rate([r for _, r in gs]), 3),
                                       "cards": cards}
    return {
        "windows": windows,
        "events": [{"date": e["date"], "name": e["name"]} for e in events],
        "note": "Per pair A vs B: A's record in games where A's decklist is published, and for each card "
                "in 12-88% of those lists, A's record with and without it. Tie = 1/3 win. Published lists "
                "are the top finishers', so absolute rates run high; compare with against without, and "
                "treat small game counts as noise.",
        "pairs": pairs,
    }


def write(windows: list[str] | None = None) -> dict:
    if not windows:
        windows = list(reversed(_windows_by_date()[-2:]))
    s = stats(windows)
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"tech_{windows[0]}.json"
    path.write_text(json.dumps(s, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    n = sum(len(v) for v in s["pairs"].values())
    print(f"matchups: {n} archetype pairs, windows {'+'.join(windows)} -> {path.relative_to(DATA.parent)}")
    return s


if __name__ == "__main__":
    write(sys.argv[1:] or None)
