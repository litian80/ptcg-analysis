"""Card-count tuning for one deck: which counts went with more wins among comparable players.

    python -m ptcg.tuning dragapult-ex               # the latest two card pools
    python -m ptcg.tuning dragapult-ex TEF-PBL,TEF-30C

Only day 2 players are compared (every day 2 player's list is published), and only their day 2
games count, so everyone in the comparison is of similar strength and plays similar opponents.
For each card, players on the most common count are compared with players on each other count
(at least MIN_GAMES day 2 games). The difference is weighted to the forecast field (data/forecast,
ptcg.forecast): each opponent's games count by its forecast share over its share of these games.

Cards whose counts always move together (|correlation| >= PACKAGE) are reported as one package.
Every comparison gets a z-score and a Benjamini-Hochberg q-value over all comparisons for the
deck; q < Q_SUGGEST is a suggestion, the rest are leads to watch. For each suggestion the
opponents that drive the difference are listed, which says what the change is for. Still
correlation: a count can go with a stronger player group even inside day 2.
"""
from __future__ import annotations

import collections
import csv
import json
import math
import sys

from . import forecast as fc
from .paths import TOURNAMENTS

TIE = 1 / 3
MIN_GAMES = 40
MIN_PLAYERS = 10   # ...from at least this many players
MIN_LISTS = 0.10   # a card must be in this share of lists to be compared
PACKAGE = 0.8
Q_SUGGEST = 0.2


def parse(line: str) -> tuple[int, str]:
    t = line.split()
    return int(t[0]), " ".join(t[1:-2])


def _lists(e: dict, deck: str) -> dict[str, collections.Counter]:
    place = {s["placing"]: s for s in e["standings"]}
    out = {}
    path = TOURNAMENTS / e["dir"] / "decklists.jsonl"
    if not path.exists():
        return out
    with open(path, encoding="utf-8") as f:
        for x in map(json.loads, f):
            s = place.get(str(x["placing"]))
            if not s or s["archetype_slug"] != deck or s["day2"] != "True":
                continue
            c = collections.Counter()
            for sec in x["cards"].values():
                for line in sec:
                    n, name = parse(line)
                    c[name] += n
            out[s["labs_player_id"]] = c
    return out


def _day2_games(e: dict) -> dict[str, list[tuple[str, float]]]:
    with open(TOURNAMENTS / e["dir"] / "matches.csv", encoding="utf-8") as f:
        ms = [m for m in csv.DictReader(f) if m["round"].isdigit()]
    d2 = {s["labs_player_id"] for s in e["standings"] if s["day2"] == "True"}
    rounds = collections.defaultdict(set)
    for m in ms:
        rounds[int(m["round"])].update(i for i in (m["p1_id"], m["p2_id"]) if i)
    start = next((r for r in sorted(rounds) if rounds[r] and len(rounds[r] & d2) >= 0.9 * len(rounds[r])), None)
    g = collections.defaultdict(list)
    if start is None:
        return g
    for m in ms:
        r = m["result"]
        if int(m["round"]) < start or r not in ("p1", "p2", "tie"):
            continue
        a = {"p1": 1.0, "p2": 0.0, "tie": TIE}[r]
        g[m["p1_id"]].append((m["p2_archetype_slug"], a))
        g[m["p2_id"]].append((m["p1_archetype_slug"], TIE if r == "tie" else 1 - a))
    return g


def players(deck: str, pools: list[str]) -> list[tuple[collections.Counter, list]]:
    rows = []
    for e in fc.events():
        if e["format_code"] in pools:
            games = _day2_games(e)
            rows += [(c, games.get(pid, [])) for pid, c in _lists(e, deck).items()]
    return rows


def _clustered(players_games, weight) -> tuple[float, float]:
    """Weighted win rate over several players' games, and its variance with each player as one
    cluster: a player's games are not independent (same list, same skill), so the variance comes
    from how much players differ, not from the number of games."""
    sums = [(sum(weight(o) * a for o, a in gs), sum(weight(o) for o, _ in gs)) for gs in players_games]
    w = sum(n for _, n in sums)
    if not w:
        return float("nan"), 0.0
    m = sum(x for x, _ in sums) / w
    k = len(sums)
    var = sum((x - m * n) ** 2 for x, n in sums) / w ** 2 * (k / (k - 1) if k > 1 else 1)
    return m, var


def _bh(ps: list[float]) -> list[float]:
    order = sorted(range(len(ps)), key=lambda i: ps[i])
    q, best = [0.0] * len(ps), 1.0
    for rank, i in reversed(list(enumerate(order, 1))):
        best = min(best, ps[i] * len(ps) / rank)
        q[i] = best
    return q


def packages(rows, cards) -> dict[str, list[str]]:
    """card -> the other cards whose counts move with it."""
    vec = {c: [r[0].get(c, 0) for r in rows] for c in cards}

    def corr(x, y):
        mx, my = sum(x) / len(x), sum(y) / len(y)
        sx = math.sqrt(sum((a - mx) ** 2 for a in x))
        sy = math.sqrt(sum((b - my) ** 2 for b in y))
        return sum((a - mx) * (b - my) for a, b in zip(x, y)) / (sx * sy) if sx and sy else 0

    out = collections.defaultdict(list)
    cs = sorted(cards)
    for i, a in enumerate(cs):
        for b in cs[i + 1:]:
            if abs(corr(vec[a], vec[b])) >= PACKAGE:
                out[a].append(b)
                out[b].append(a)
    return out


def analyse(deck: str, pools: list[str], field: dict[str, float] | None = None) -> dict:
    rows = players(deck, pools)
    games_all = [g for _, gs in rows for g in gs]
    played = collections.Counter(o for o, _ in games_all)
    n_games = sum(played.values())
    if field:
        # opponents absent from the forecast still count a little, so no game is thrown away
        weight = lambda o: (field.get(o, 0.002) / (played[o] / n_games)) if played[o] else 0
    else:
        weight = lambda o: 1.0
    present = collections.Counter(c for r, _ in rows for c in r)
    cards = [c for c, k in present.items() if k >= MIN_LISTS * len(rows)]
    pk = packages(rows, cards)
    tests = []
    for card in cards:
        by = collections.defaultdict(list)          # count -> one list of games per player
        for c, gs in rows:
            if gs:
                by[c.get(card, 0)].append(gs)
        modal = max(by, key=lambda k: len(by[k]))
        base, vb = _clustered(by[modal], weight)
        for n in sorted(by):
            if n == modal or sum(map(len, by[n])) < MIN_GAMES or len(by[n]) < MIN_PLAYERS:
                continue
            alt, va = _clustered(by[n], weight)
            z = (alt - base) / math.sqrt(va + vb) if va + vb else 0.0
            flat_n = [g for gs in by[n] for g in gs]
            flat_m = [g for gs in by[modal] for g in gs]
            opp = []                                # which opponents carry the difference
            for o in {o for o, _ in flat_n}:
                a = [x for oo, x in flat_n if oo == o]
                b = [x for oo, x in flat_m if oo == o]
                if len(a) >= 8 and len(b) >= 8:
                    d = sum(a) / len(a) - sum(b) / len(b)
                    opp.append((d * weight(o) * min(len(a), len(b)), o, round(d, 3), len(a), len(b)))
            opp.sort(key=lambda t: -abs(t[0]))
            tests.append({"card": card, "from": modal, "to": n, "lists_from": len(by[modal]),
                          "lists_to": len(by[n]), "games_from": len(flat_m), "games_to": len(flat_n),
                          "win_from": round(base, 3), "win_to": round(alt, 3), "z": round(z, 2),
                          "p": math.erfc(abs(z) / math.sqrt(2)), "package": sorted(pk.get(card, [])),
                          "drivers": [{"vs": o, "diff": d, "games_to": ga, "games_from": gb}
                                      for _, o, d, ga, gb in opp[:3] if (d > 0) == (z > 0)]})
    for t, q in zip(tests, _bh([t["p"] for t in tests])):
        t["q"] = round(q, 3)
        t["p"] = round(t["p"], 4)
    tests.sort(key=lambda t: t["p"])
    # one line per package: keep the strongest member
    seen, out = set(), []
    for t in tests:
        key = (frozenset([t["card"], *t["package"]]), t["to"] - t["from"] > 0)
        if key in seen:
            continue
        seen.add(key)
        out.append(t)
    return {"deck": deck, "pools": pools, "lists": len(rows), "games": n_games,
            "field_weighted": bool(field), "tests": out}


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    deck = argv[0]
    pools = argv[1].split(",") if len(argv) > 1 else None
    if pools is None:
        seen = list(dict.fromkeys(e["format_code"] for e in reversed(fc.events())))
        pools = seen[:2]
    field = fc.next_event()["field"]
    r = analyse(deck, pools, field)
    print(f"{deck} {pools}: {r['lists']} day 2 lists, {r['games']} day 2 games, weighted to forecast field")
    for t in r["tests"][:15]:
        pk = f" (with {', '.join(t['package'])})" if t["package"] else ""
        dr = "; ".join(f"{d['vs']} {d['diff']:+.2f}" for d in t["drivers"])
        print(f"  q {t['q']:.2f} z {t['z']:+.2f}  {t['card']}{pk}: {t['from']} -> {t['to']}  "
              f"{t['win_from']:.3f} ({t['games_from']}) vs {t['win_to']:.3f} ({t['games_to']})  [{dr}]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
