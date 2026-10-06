"""Aggregate Twinleaf sim games and compare with real matchup win rates.

    python sim/twinleaf/summarize.py            # reads data/sim/games/*.jsonl
writes data/sim/twinleaf_TEF-30C.json and prints the calibration tables.

Real numbers: data/selection/selection_TEF-30C.json (windows TEF-30C + TEF-PBL, match records)
with data/archetypes/meta_TEF-30C.json (TEF-30C only) as a second view. Real win rate here is
W/(W+L) on matches (ties dropped) and, as in the selection file, (W + T/3)/games. Sim win rate is
per game, draws/errors dropped. A Bo3 conversion of the sim game rate p, p^2(3-2p), is also shown
because real records are matches.
"""
import glob, json, math, os, sys
from collections import defaultdict

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MIN_REAL = 20


def load_games():
    rows = []
    for f in sorted(glob.glob(os.path.join(ROOT, "data/sim/games/*.jsonl"))):
        with open(f, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    rows.append(json.loads(line))
    return rows


def real_tables():
    sel = json.load(open(os.path.join(ROOT, "data/selection/selection_TEF-30C.json"), encoding="utf-8"))
    meta = json.load(open(os.path.join(ROOT, "data/archetypes/meta_TEF-30C.json"), encoding="utf-8"))
    out = {}
    for name, src in (("selection", sel), ("meta", meta)):
        t = {}
        for a, d in src["archetypes"].items():
            for m in d.get("matchups", []):
                w, l, ti = m["wins"], m["losses"], m["ties"]
                t[(a, m["vs"])] = {"games": w + l + ti, "wins": w, "losses": l, "ties": ti,
                                   "wr_no_ties": w / (w + l) if w + l else None,
                                   "wr_pts": (w + ti / 3) / (w + l + ti) if w + l + ti else None}
        out[name] = t
    return out


def bo3(p):
    return p * p * (3 - 2 * p)


def pearson(xs, ys):
    n = len(xs)
    if n < 3:
        return None
    mx, my = sum(xs) / n, sum(ys) / n
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    return sxy / math.sqrt(sxx * syy) if sxx > 0 and syy > 0 else None


def aggregate(rows):
    agg = defaultdict(lambda: {"games": 0, "wins": 0, "losses": 0, "draws": 0, "errors": 0,
                               "first_games": 0, "first_wins": 0, "second_games": 0, "second_wins": 0,
                               "turns": 0, "ms": 0, "ends": defaultdict(int)})
    for r in rows:
        k = (r.get("bot", "advanced"), r["a"], r["b"])
        g = agg[k]
        g["games"] += 1
        g["turns"] += r["turns"]
        g["ms"] += r["ms"]
        g["ends"][r["end"]] += 1
        w = r["winner"]
        if r["end"] not in ("finished",):
            g["errors"] += 1
            continue
        if w == "draw" or w not in ("a", "b"):
            g["draws"] += 1
            continue
        first = r.get("firstActual") or r["first"]
        won = w == "a"
        g["wins" if won else "losses"] += 1
        if first == "a":
            g["first_games"] += 1
            g["first_wins"] += won
        else:
            g["second_games"] += 1
            g["second_wins"] += won
    return agg


def main():
    rows = load_games()
    if not rows:
        sys.exit("no games found in data/sim/games")
    real = real_tables()
    agg = aggregate(rows)
    bots = sorted({k[0] for k in agg})
    out = {"window": "TEF-30C", "engine": "Twinleaf (github.com/twinleafgg/twinleafgg)",
           "note": "win_rate = wins/(wins+losses) per game for deck a; draws = finished without a winner; "
                   "errors = turn limit, time limit, stuck or exception. real_* from selection_TEF-30C.json "
                   "(TEF-30C + TEF-PBL match records): real_wr_no_ties = W/(W+L), real_wr_pts = (W+T/3)/games.",
           "bots": {}}
    for bot in bots:
        pairs = []
        tot = defaultdict(int)
        for (b, a, o), g in sorted(agg.items()):
            if b != bot:
                continue
            dec = g["wins"] + g["losses"]
            wr = g["wins"] / dec if dec else None
            rs = real["selection"].get((a, o))
            rm = real["meta"].get((a, o))
            p = {"a": a, "b": o, "games": g["games"], "wins": g["wins"], "losses": g["losses"],
                 "draws": g["draws"], "errors": g["errors"],
                 "win_rate": round(wr, 3) if wr is not None else None,
                 "win_rate_first": round(g["first_wins"] / g["first_games"], 3) if g["first_games"] else None,
                 "win_rate_second": round(g["second_wins"] / g["second_games"], 3) if g["second_games"] else None,
                 "avg_turns": round(g["turns"] / g["games"], 1), "avg_ms": round(g["ms"] / g["games"]),
                 "ends": dict(g["ends"])}
            if rs:
                p.update(real_games=rs["games"], real_wr_no_ties=round(rs["wr_no_ties"], 3),
                         real_wr_pts=round(rs["wr_pts"], 3))
            if rm:
                p.update(real_games_30c=rm["games"], real_wr_no_ties_30c=round(rm["wr_no_ties"], 3))
            pairs.append(p)
            for k2 in ("games", "wins", "losses", "draws", "errors", "first_games", "first_wins",
                       "second_games", "second_wins", "ms"):
                tot[k2] += g[k2]
        # calibration
        cal = [p for p in pairs if p.get("real_games", 0) >= MIN_REAL and p["win_rate"] is not None and p["a"] != p["b"]]
        xs = [p["real_wr_no_ties"] for p in cal]
        ys = [p["win_rate"] for p in cal]
        y3 = [bo3(y) for y in ys]
        diffs = [abs(x - y) for x, y in zip(xs, ys)]
        diffs3 = [abs(x - y) for x, y in zip(xs, y3)]
        summary = {
            "games": tot["games"], "errors": tot["errors"], "draws": tot["draws"],
            "error_rate": round(tot["errors"] / tot["games"], 4),
            "games_per_sec_per_core": round(tot["games"] / (tot["ms"] / 1000), 3) if tot["ms"] else None,
            "first_player_win_rate": round(tot["first_wins"] / tot["first_games"], 3) if tot["first_games"] else None,
            "first_games": tot["first_games"],
            "calibration_pairs": len(cal),
            "mean_abs_diff": round(sum(diffs) / len(diffs), 3) if diffs else None,
            "mean_abs_diff_bo3": round(sum(diffs3) / len(diffs3), 3) if diffs3 else None,
            "pearson": round(pearson(xs, ys), 3) if pearson(xs, ys) is not None else None,
            "within_10pp": sum(d <= 0.10 for d in diffs),
            "within_10pp_bo3": sum(d <= 0.10 for d in diffs3),
            "sign_agreement": sum((x - 0.5) * (y - 0.5) > 0 for x, y in zip(xs, ys)),
        }
        big = [(p["real_wr_no_ties"], p["win_rate"]) for p in cal if p["real_games"] >= 100]
        if len(big) >= 3:
            summary["pairs_ge100_real"] = len(big)
            summary["pearson_ge100"] = round(pearson([b[0] for b in big], [b[1] for b in big]), 3)
            summary["mean_abs_diff_ge100"] = round(sum(abs(a - b) for a, b in big) / len(big), 3)
        out["bots"][bot] = {"summary": summary, "pairs": pairs}
        print(f"\n=== bot={bot}: {json.dumps(summary)}")
        print(f"{'pair':48s} {'n':>4s} {'sim':>5s} {'1st':>5s} {'2nd':>5s} {'err':>4s} | {'real':>5s} {'nReal':>5s} {'diff':>6s}")
        for p in pairs:
            rr = p.get("real_wr_no_ties")
            d = (p["win_rate"] - rr) if (rr is not None and p["win_rate"] is not None) else None
            f = lambda v: f"{v:5.2f}" if v is not None else "  -  "
            print(f"{p['a'] + ' v ' + p['b']:48s} {p['games']:4d} {f(p['win_rate'])} {f(p['win_rate_first'])} "
                  f"{f(p['win_rate_second'])} {p['errors']:4d} | {f(rr)} {p.get('real_games', 0):5d} "
                  f"{(f'{d:+6.2f}' if d is not None else '   -  ')}")
    path = os.path.join(ROOT, "data/sim/twinleaf_TEF-30C.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)
    print("\nwrote", os.path.relpath(path, ROOT))


if __name__ == "__main__":
    main()
