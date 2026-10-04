"""Per-archetype numbers for one card-pool window, from the collected tournaments.

    python -m ptcg.archetypes            # latest window (e.g. TEF-30C)
    python -m ptcg.archetypes TEF-PBL    # a specific window

Writes data/archetypes/meta_<window>.json: for every archetype, its share of the field and of
day 2, its overall and per-matchup match record, and its core list (cards most of its lists
play, with the usual count). The hand-written game plans in data/archetypes/<slug>.yaml
reference these numbers; plans.py checks the plans against this file.

Archetype names and slugs are Limitless's (the same ones in standings.csv and matches.csv).
"""
from __future__ import annotations

import collections
import csv
import json
import statistics
import sys

from .limitless import load_index
from .paths import DATA, TOURNAMENTS

ARCHETYPES = DATA / "archetypes"
MIN_SHARE = 0.01        # archetypes below 1% of the field are left out
MIN_MATCHUP_GAMES = 20  # matchup rows need at least this many matches


def _events(window: str) -> list[dict]:
    return [r for r in load_index() if r["format_code"] == window]


def latest_window() -> str:
    rows = [r for r in load_index() if r["format_code"]]
    if not rows:
        raise SystemExit("archetypes: no tournaments collected yet (data/tournaments/index.csv)")
    return max(rows, key=lambda r: r["date"])["format_code"]


def _read_csv(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def stats(window: str) -> dict:
    events = _events(window)
    if not events:
        raise SystemExit(f"archetypes: no collected tournaments in window {window}")
    players = collections.Counter()
    day2 = collections.Counter()
    names: dict[str, str] = {}
    n_players = n_day2 = 0
    record = collections.defaultdict(lambda: [0, 0, 0])               # slug -> W/L/T
    vs = collections.defaultdict(lambda: collections.defaultdict(lambda: [0, 0, 0]))
    lists = collections.defaultdict(list)

    for e in events:
        d = TOURNAMENTS / e["dir"]
        by_placing = {}
        for r in _read_csv(d / "standings.csv"):
            slug = r["archetype_slug"]
            if r["placing"]:
                by_placing[r["placing"]] = slug
            n_players += 1
            n_day2 += r.get("day2") == "True"
            if not slug or slug == "other" or slug.startswith("?"):   # "?icons" = unresolved
                continue
            names[slug] = r["archetype"]
            players[slug] += 1
            day2[slug] += r.get("day2") == "True"
        for m in _read_csv(d / "matches.csv"):
            a, b, res = m["p1_archetype_slug"], m["p2_archetype_slug"], m["result"]
            if (res not in ("p1", "p2", "tie") or not a or not b or a == b
                    or a.startswith("?") or b.startswith("?")):
                continue
            ra = {"p1": 0, "p2": 1, "tie": 2}[res]
            rb = {"p1": 1, "p2": 0, "tie": 2}[res]
            record[a][ra] += 1
            record[b][rb] += 1
            vs[a][b][ra] += 1
            vs[b][a][rb] += 1
        # Decklists carry Limitless's own archetype names, which differ from Labs's; join on placing.
        with open(d / "decklists.jsonl", encoding="utf-8") as f:
            for line in f:
                deck = json.loads(line)
                slug = by_placing.get(str(deck["placing"]))
                if slug:
                    lists[slug].append(deck)

    def win_rate(w, l, t):
        n = w + l + t
        return round((w + t / 3) / n, 3) if n else None   # a tie counts as a third of a win (1 of 3 points)

    out = {}
    for slug, n in players.most_common():
        if n / n_players < MIN_SHARE:
            break
        w, l, t = record[slug]
        matchups = []
        for other, (mw, ml, mt) in sorted(vs[slug].items(), key=lambda kv: -players[kv[0]]):
            if mw + ml + mt >= MIN_MATCHUP_GAMES and players[other] / n_players >= MIN_SHARE:
                matchups.append({"vs": other, "wins": mw, "losses": ml, "ties": mt,
                                 "win_rate": win_rate(mw, ml, mt)})
        out[slug] = {
            "name": names[slug],
            "players": n,
            "share": round(n / n_players, 3),
            "day2_share": round(day2[slug] / n_day2, 3) if n_day2 else None,
            "record": {"wins": w, "losses": l, "ties": t, "win_rate": win_rate(w, l, t)},
            "lists": len(lists[slug]),
            "core": _core(lists[slug]),
            "matchups": matchups,
        }
    return {
        "window": window,
        "events": [{"date": e["date"], "name": e["name"], "players": int(e["players"]), "dir": e["dir"]}
                   for e in events],
        "players": n_players,
        "note": "win_rate counts a tie as 1/3 of a win; mirrors, byes and double losses are excluded. "
                "core lists every card in at least 25% of the archetype's lists: in_lists is that "
                "fraction, count the median copies among lists that play it, printing the most played set and number (cards with the same name can differ between sets).",
        "archetypes": out,
    }


def _num(x):
    return int(x) if x == int(x) else x


SECTIONS = {"pokemon": "Pokémon", "trainer": "Trainer", "energy": "Energy"}


def _entries(deck: dict) -> list[dict]:
    """A deck's cards as dicts, from either the list-of-dicts or the {section: ["4 Name SET 12"]} layout."""
    cards = deck["cards"]
    if isinstance(cards, list):
        return cards
    out = []
    for key, lines in cards.items():
        for line in lines:
            tokens = line.split()
            out.append({"count": int(tokens[0]), "name": " ".join(tokens[1:-2]), "set": tokens[-2],
                        "number": tokens[-1], "section": SECTIONS.get(key, key)})
    return out


def _core(decks: list[dict]) -> list[dict]:
    if not decks:
        return []
    counts = collections.defaultdict(list)
    section = {}
    printing = collections.defaultdict(collections.Counter)
    for deck in decks:
        per = collections.Counter()
        for c in _entries(deck):
            per[c["name"]] += c["count"]
            section[c["name"]] = c["section"]
            printing[c["name"]][f'{c["set"]} {c["number"]}'] += c["count"]
        for name, k in per.items():
            counts[name].append(k)
    rows = [{"name": name, "section": section[name], "in_lists": round(len(ks) / len(decks), 2),
             "count": _num(statistics.median(ks)),
             "printing": printing[name].most_common(1)[0][0]}
            for name, ks in counts.items() if len(ks) / len(decks) >= 0.25]
    order = {"Pokémon": 0, "Trainer": 1, "Energy": 2}
    return sorted(rows, key=lambda r: (order.get(r["section"], 3), -r["in_lists"], r["name"]))


def write(window: str | None = None) -> dict:
    window = window or latest_window()
    s = stats(window)
    ARCHETYPES.mkdir(parents=True, exist_ok=True)
    path = ARCHETYPES / f"meta_{window}.json"
    path.write_text(json.dumps(s, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"archetypes: {len(s['archetypes'])} archetypes in {window} -> {path.relative_to(DATA.parent)}")
    return s


if __name__ == "__main__":
    write(sys.argv[1] if len(sys.argv) > 1 else None)
