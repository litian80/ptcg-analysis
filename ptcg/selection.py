"""Deck selection numbers: how well each archetype should do against the field you expect to face.

    python -m ptcg.selection                    # the latest window, matchups pooled with the one before
    python -m ptcg.selection TEF-30C TEF-PBL    # field from the first window, matchups from all listed

The field you will face is taken from the first window (the latest one by default): its share of
all players, and its share of day 2. Matchup win rates are pooled over every listed window, since
one weekend rarely has enough games for the smaller pairings, and shrunk toward the field average
so a 12-game matchup cannot dominate the result. A deck's expected win rate is then its matchup
win rate against each opponent, weighted by how often you meet that opponent.

Writes data/selection/selection_<window>.json. The written analysis lives next to it as
data/selection/<window>.md (hand-written from these numbers).
"""
from __future__ import annotations

import collections
import csv
import json
import sys

from .limitless import load_index
from .paths import DATA, TOURNAMENTS

OUT = DATA / "selection"
MIN_SHARE = 0.005  # archetypes below 0.5% of the latest field are left out
PRIOR = 20         # shrinkage: a matchup counts as if it had this many extra games at the field average
TIE = 1 / 3        # a tie is 1 match point of 3, the same convention as ptcg.archetypes


def _read_csv(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _windows_by_date() -> list[str]:
    first = {}
    for r in load_index():
        if r["format_code"]:
            first[r["format_code"]] = min(first.get(r["format_code"], r["date"]), r["date"])
    return sorted(first, key=first.get)


def _known(slug: str) -> bool:
    return bool(slug) and slug != "other" and not slug.startswith("?")


def _day2_start(matches: list[dict], day2: set[str]) -> int | None:
    """First round in which (nearly) every paired player made day 2. A few day 2 players lack the
    flag in the standings, so 90% is enough."""
    rounds = collections.defaultdict(set)
    for m in matches:
        rounds[int(m["round"])].update((m["p1_id"], m["p2_id"]))
    for r in sorted(rounds):
        ids = {i for i in rounds[r] if i}
        if ids and len(ids & day2) >= 0.9 * len(ids):
            return r
    return None


def _event(e: dict) -> dict:
    d = TOURNAMENTS / e["dir"]
    standings = _read_csv(d / "standings.csv")
    matches = _read_csv(d / "matches.csv")
    day2 = {r["labs_player_id"] for r in standings if r.get("day2") == "True"}
    start = _day2_start(matches, day2)
    return {"standings": standings, "matches": matches, "day2_start": start}


def _rate(w, l, t):
    n = w + l + t
    return (w + t * TIE) / n if n else None


def stats(windows: list[str]) -> dict:
    index = load_index()
    field_window = windows[0]
    events = {w: [e for e in index if e["format_code"] == w] for w in windows}
    for w, es in events.items():
        if not es:
            raise SystemExit(f"selection: no collected tournaments in window {w}")
    loaded = {e["dir"]: _event(e) for es in events.values() for e in es}

    # Field: who you meet, from the latest window only.
    players = collections.Counter()
    day2 = collections.Counter()
    top_cut = collections.Counter()
    names = {}
    n_players = n_day2 = 0
    for e in events[field_window]:
        for r in loaded[e["dir"]]["standings"]:
            n_players += 1
            n_day2 += r.get("day2") == "True"
            slug = r["archetype_slug"]
            if not _known(slug):
                continue
            names[slug] = r["archetype"]
            players[slug] += 1
            day2[slug] += r.get("day2") == "True"
            top_cut[slug] += r.get("top_cut") == "True"

    # Previous window's share, for the trend column.
    prev_share = {}
    if len(windows) > 1:
        c = collections.Counter()
        n = 0
        for e in events[windows[1]]:
            for r in loaded[e["dir"]]["standings"]:
                n += 1
                if _known(r["archetype_slug"]):
                    c[r["archetype_slug"]] += 1
        prev_share = {s: k / n for s, k in c.items()}

    # Matchups, pooled over all windows. "late" = rounds where both players are in day 2.
    vs = collections.defaultdict(lambda: collections.defaultdict(lambda: [0, 0, 0]))
    late = collections.defaultdict(lambda: [0, 0, 0])
    mirror = [0, 0]   # games, ties
    for ev in loaded.values():
        for m in ev["matches"]:
            a, b, res = m["p1_archetype_slug"], m["p2_archetype_slug"], m["result"]
            if res not in ("p1", "p2", "tie") or not _known(a) or not _known(b):
                continue
            if a == b:
                mirror[0] += 1
                mirror[1] += res == "tie"
                continue
            ra = {"p1": 0, "p2": 1, "tie": 2}[res]
            rb = {"p1": 1, "p2": 0, "tie": 2}[res]
            vs[a][b][ra] += 1
            vs[b][a][rb] += 1
            if ev["day2_start"] and int(m["round"]) >= ev["day2_start"]:
                late[a][ra] += 1
                late[b][rb] += 1

    # Average match points per game across all non-mirror games: with ties worth 1/3 this is
    # below 0.5, so it is the "neither good nor bad" line and the shrinkage target.
    late_tot = [sum(r[i] for r in late.values()) for i in range(3)]
    tot = [0, 0, 0]
    for a in vs:
        for b in vs[a]:
            for i in range(3):
                tot[i] += vs[a][b][i]
    baseline = _rate(*tot)
    mirror_rate = (0.5 * (mirror[0] - mirror[1]) + TIE * mirror[1]) / mirror[0] if mirror[0] else baseline

    kept = [s for s, k in players.most_common() if k / n_players >= MIN_SHARE]
    field = {s: players[s] / n_players for s in kept}
    field_d2 = {s: day2[s] / n_day2 for s in kept} if n_day2 else field

    def shrunk(a, b):
        w, l, t = vs[a][b]
        n = w + l + t
        return (w + t * TIE + PRIOR * baseline) / (n + PRIOR), n

    def overall(a):
        w = l = t = 0
        for b, (mw, ml, mt) in vs[a].items():
            w, l, t = w + mw, l + ml, t + mt
        return w, l, t

    def expected(a, shares):
        """Expected points rate against a field; opponents outside the kept list play like the
        deck's record against everything not kept."""
        covered = sum(shares.values())
        ew = 0.0
        for b, sh in shares.items():
            ew += sh * (mirror_rate if a == b else shrunk(a, b)[0])
        rest = [0, 0, 0]
        for b, rec in vs[a].items():
            if b not in shares:
                for i in range(3):
                    rest[i] += rec[i]
        n = sum(rest)
        rest_rate = (rest[0] + rest[2] * TIE + PRIOR * baseline) / (n + PRIOR)
        return ew + (1 - covered) * rest_rate

    out = {}
    for s in kept:
        w, l, t = overall(s)
        lw, ll, lt = late[s]
        out[s] = {
            "name": names[s],
            "players": players[s],
            "share": round(field[s], 4),
            "prev_share": round(prev_share.get(s, 0.0), 4) if prev_share else None,
            "day2_share": round(field_d2[s], 4),
            "day2_conversion": round(field_d2[s] / field[s], 2),
            "top_cut": top_cut[s],
            "record": {"wins": w, "losses": l, "ties": t, "win_rate": round(_rate(w, l, t), 3),
                       "tie_rate": round(t / (w + l + t), 3)},
            "day2_record": {"wins": lw, "losses": ll, "ties": lt,
                            "win_rate": round(_rate(lw, ll, lt), 3) if lw + ll + lt else None},
            "expected_vs_field": round(expected(s, field), 3),
            "expected_vs_day2": round(expected(s, field_d2), 3),
            "matchups": [
                {"vs": b, "games": shrunk(s, b)[1], "wins": vs[s][b][0], "losses": vs[s][b][1],
                 "ties": vs[s][b][2], "win_rate": round(_rate(*vs[s][b]), 3) if shrunk(s, b)[1] else None,
                 "shrunk": round(shrunk(s, b)[0], 3)}
                for b in kept if b != s
            ],
        }
    ranked = sorted(out, key=lambda s: -out[s]["expected_vs_day2"])
    return {
        "field_window": field_window,
        "matchup_windows": windows,
        "events": [{"window": w, "date": e["date"], "name": e["name"], "players": int(e["players"])}
                   for w in windows for e in events[w]],
        "players": n_players,
        "day2_players": n_day2,
        "baseline": round(baseline, 3),
        "day2_baseline": round(_rate(*late_tot), 3),
        "mirror_rate": round(mirror_rate, 3),
        "note": "win_rate = match points per game with a tie worth 1/3 of a win; baseline is the average "
                "over all non-mirror games, so above baseline is better than average. shrunk adds "
                f"{PRIOR} games at baseline to each matchup. expected_vs_field weights matchups by "
                "the latest window's share of all players, expected_vs_day2 by its share of day 2. "
                "day2_record counts only rounds in which both players had made day 2.",
        "ranking": ranked,
        "archetypes": out,
    }


def write(windows: list[str] | None = None) -> dict:
    if not windows:
        order = _windows_by_date()
        windows = list(reversed(order[-2:]))
    s = stats(windows)
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"selection_{windows[0]}.json"
    path.write_text(json.dumps(s, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"selection: {len(s['archetypes'])} archetypes, field {windows[0]}, "
          f"matchups {'+'.join(windows)} -> {path.relative_to(DATA.parent)}")
    return s


if __name__ == "__main__":
    write(sys.argv[1:] or None)
