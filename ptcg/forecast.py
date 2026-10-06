"""Forecast the next major's field and which decks give the best shot at the top cut, with backtests.

    python -m ptcg.forecast                 # backtest, then forecast the next event
    python -m ptcg.forecast --region EU     # weight events from that region (EU, NA, LA, OC)

Writes data/forecast/forecast.json. Every past event is predicted from the events played
strictly before it, so a backtest never sees the future. Tuning uses only events before the
April 2026 rotation (SPLIT); results are reported separately for the events after it.

Two questions, two models:

1. Who registers (the whole field). Shares from all earlier events, weighted by recency
   (exp(-age / TAU), and by sqrt(players)), events in the same region counted REGION times,
   plus momentum: archetypes that took more of the latest top 8s than of their fields grow by
   BETA times the gap. Scored by total variation distance (TVD) against the actual field.
   Predicting the archetype mix of a single event's top 32 is mostly noise: even knowing the
   exact field, the top 32 sits ~0.35 TVD away from it (32 players is a small sample). So the
   forecast targets the field, and the top is handled by question 2.

2. Which deck converts (makes the top). Per archetype: its expected win rate against the
   forecast field (matchups from earlier events in the latest card pool, shrunk toward the
   average) and its past top-32 conversion (share of its players who finished top 32, divided by
   32 / players, shrunk toward 1). The score blends the two as z-scores, W_MATCHUP on matchups.
   Backtest: for each event, take the top PICKS archetypes and compare how many of their
   players made the top 8 / top 32 with how many an average deck would have put there (lift).
   Conversion carries the skill of the players who choose a deck as well as the deck itself.
"""
from __future__ import annotations

import collections
import csv
import datetime as dt
import functools
import json
import math
import statistics
import sys

from .paths import DATA, TOURNAMENTS

OUT = DATA / "forecast"
SPLIT = "2026-04-10"   # Standard rotation: tune on events before, report on events after
MIN_PLAYERS = 300      # smaller events are used as evidence but not scored
UNKNOWN = {"", "other"}
TIE = 1 / 3
TAU = 7                # field: recency in days
BETA = 0.1             # field: momentum from the latest top 8s
REGION = 2.0           # field: weight of same-region events
TAU_PERF = 14          # matchups and conversion: recency in days
PRIOR_GAMES = 20       # matchup shrinkage toward the average
PRIOR_PLAYERS = 20      # conversion shrinkage toward 1 (an average deck)
OTHER_POOL = 0.3       # conversion evidence from an older card pool counts this much
W_MATCHUP = 0.25       # pick score: weight on matchups, the rest on conversion
PICKS = 3
MIN_FIELD = 0.01       # candidates: forecast share at least this
REGIONS = {"EU": {"DE", "FR", "PL", "GB", "IT", "NL", "ES", "CZ", "PT", "BE", "AT", "SE", "DK", "CH", "ZA"},
           "NA": {"US", "CA", "PR"}, "LA": {"MX", "BR", "CL", "PE", "AR", "CO"}, "OC": {"AU", "NZ"}}


def region_of(country: str) -> str | None:
    return next((r for r, cs in REGIONS.items() if country in cs), None)


@functools.cache
def events() -> tuple[dict, ...]:
    with open(TOURNAMENTS / "index.csv", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    out = []
    for r in rows:
        p = TOURNAMENTS / r["dir"] / "standings.csv"
        if not p.exists():
            continue
        with open(p, encoding="utf-8") as f:
            st = sorted((s for s in csv.DictReader(f) if s["placing"]), key=lambda s: int(s["placing"]))
        if st:
            out.append({**r, "standings": st, "day": dt.date.fromisoformat(r["date"])})
    return tuple(sorted(out, key=lambda e: (e["date"], e["name"])))


def shares(standings: list[dict], top: int | None = None) -> dict[str, float]:
    c = collections.Counter(s["archetype_slug"] for s in (standings[:top] if top else standings)
                            if s["archetype_slug"] not in UNKNOWN)
    n = sum(c.values())
    return {k: v / n for k, v in c.items()} if n else {}


def normalize(d: dict[str, float]) -> dict[str, float]:
    d = {k: max(v, 0.0) for k, v in d.items()}
    n = sum(d.values())
    return {k: v / n for k, v in d.items() if v > 0} if n else {}


def tvd(p: dict[str, float], q: dict[str, float]) -> float:
    return 0.5 * sum(abs(p.get(k, 0) - q.get(k, 0)) for k in set(p) | set(q))


# 1. the field

def field_last(past, day, region=None) -> dict[str, float]:
    """Baseline: the latest weekend's fields pooled."""
    last = max(e["day"] for e in past)
    c = collections.Counter()
    for e in past:
        if e["day"] == last:
            for k, v in shares(e["standings"]).items():
                c[k] += v * int(e["players"])
    return normalize(c)


def field_forecast(past, day, region=None, tau=TAU, beta=BETA, same_region=REGION) -> dict[str, float]:
    acc, w_sum = collections.Counter(), 0.0
    mom, g_sum = collections.Counter(), 0.0
    last = max(e["day"] for e in past)
    for e in past:
        w = math.exp(-(day - e["day"]).days / tau) * math.sqrt(int(e["players"]))
        if region and region_of(e["country"]) == region:
            w *= same_region
        w_sum += w
        f = shares(e["standings"])
        for k, v in f.items():
            acc[k] += w * v
        if (last - e["day"]).days <= 14:
            g = math.sqrt(int(e["players"]))
            g_sum += g
            t8 = shares(e["standings"], 8)
            for k in set(t8) | set(f):
                mom[k] += g * (t8.get(k, 0) - f.get(k, 0))
    pred = {k: v / w_sum for k, v in acc.items()}
    for k, v in mom.items():
        pred[k] = pred.get(k, 0) + beta * v / g_sum
    return normalize(pred)


# 2. which deck converts

@functools.cache
def _matchups(event_dir: str) -> dict[tuple[str, str], tuple[float, int]]:
    c = collections.defaultdict(lambda: [0.0, 0])
    with open(TOURNAMENTS / event_dir / "matches.csv", encoding="utf-8") as f:
        for m in csv.DictReader(f):
            a, b, r = m["p1_archetype_slug"], m["p2_archetype_slug"], m["result"]
            if r not in ("p1", "p2", "tie") or a in UNKNOWN or b in UNKNOWN or a == b:
                continue
            pa = {"p1": 1.0, "p2": 0.0, "tie": TIE}[r]
            pb = TIE if r == "tie" else 1 - pa
            c[(a, b)][0] += pa
            c[(a, b)][1] += 1
            c[(b, a)][0] += pb
            c[(b, a)][1] += 1
    return {k: (v[0], v[1]) for k, v in c.items()}


def deck_scores(past, day, field: dict[str, float], top: int = 32) -> dict[str, dict]:
    pool = max(past, key=lambda e: e["day"])["format_code"]
    mu = collections.defaultdict(lambda: [0.0, 0.0])
    played, topped = collections.Counter(), collections.Counter()
    for e in past:
        w = math.exp(-(day - e["day"]).days / TAU_PERF)
        same = e["format_code"] == pool
        if same:
            for k, (pt, g) in _matchups(e["dir"]).items():
                mu[k][0] += w * pt
                mu[k][1] += w * g
        n = len(e["standings"])
        wc = w * (1 if same else OTHER_POOL)
        for s in e["standings"]:
            played[s["archetype_slug"]] += wc
        for s in e["standings"][:top]:
            topped[s["archetype_slug"]] += wc * n / top
    games = sum(v[1] for v in mu.values())
    avg = sum(v[0] for v in mu.values()) / games if games else 0.476

    def wr(a, b):
        pt, g = mu.get((a, b), (0, 0))
        return (pt + PRIOR_GAMES * avg) / (g + PRIOR_GAMES)

    cands = [a for a, v in field.items() if v >= MIN_FIELD]
    out = {}
    for a in cands:
        opp = {b: v for b, v in field.items() if b != a}
        tot = sum(opp.values())
        out[a] = {"field": field[a],
                  "expected": sum(v * wr(a, b) for b, v in opp.items()) / tot,
                  "conversion": (topped[a] + PRIOR_PLAYERS) / (played[a] + PRIOR_PLAYERS),
                  "games": sum(mu.get((a, b), (0, 0))[1] for b in opp)}

    def z(key):
        vals = [d[key] for d in out.values()]
        m, s = statistics.mean(vals), statistics.pstdev(vals) or 1
        return {a: (d[key] - m) / s for a, d in out.items()}

    ze, zc = z("expected"), z("conversion")
    for a, d in out.items():
        d["score"] = W_MATCHUP * ze[a] + (1 - W_MATCHUP) * zc[a]
    return out


# backtests

def cases():
    evs = events()
    return [(e, [x for x in evs if x["day"] < e["day"]]) for e in evs
            if int(e["players"]) >= MIN_PLAYERS and sum(x["day"] < e["day"] for x in evs) >= 2]


def backtest_field() -> dict:
    out = {}
    for split, cs in (("before", [c for c in cases() if c[0]["date"] < SPLIT]),
                      ("after", [c for c in cases() if c[0]["date"] >= SPLIT])):
        r = {}
        for name, model in (("forecast", field_forecast), ("last", field_last)):
            d = [tvd(model(p, e["day"], region_of(e["country"])), shares(e["standings"])) for e, p in cs]
            r[name] = round(sum(d) / len(d), 3)
        floor = [tvd(shares(e["standings"]), shares(e["standings"], 32)) for e, _ in cs]
        r["exact_field_vs_top32"] = round(sum(floor) / len(floor), 3)
        r["events"] = len(cs)
        out[split] = r
    return out


def backtest_picks() -> dict:
    out = {}
    for split, cs in (("before", [c for c in cases() if c[0]["date"] < SPLIT]),
                      ("after", [c for c in cases() if c[0]["date"] >= SPLIT])):
        tally = collections.defaultdict(lambda: [0, 0.0, 0])
        for e, past in cs:
            field = field_forecast(past, e["day"], region_of(e["country"]))
            sc = deck_scores(past, e["day"], field)
            last = max(x["day"] for x in past)
            strategies = {
                "model": sorted(sc, key=lambda a: -sc[a]["score"])[:PICKS],
                "popular": sorted(field, key=lambda a: -field[a])[:PICKS],
                "last_winners": list(dict.fromkeys(x["standings"][0]["archetype_slug"]
                                                   for x in past if x["day"] == last)),
            }
            st = e["standings"]
            n = collections.Counter(s["archetype_slug"] for s in st)
            for top in (8, 32):
                t = collections.Counter(s["archetype_slug"] for s in st[:top])
                for name, picks in strategies.items():
                    for a in picks:
                        tally[(name, top)][0] += t[a]
                        tally[(name, top)][1] += n[a] * top / len(st)
                        tally[(name, top)][2] += n[a]
        out[split] = {f"{name}_top{top}": {"made_it": h, "average_deck": round(x, 1),
                                           "lift": round(h / x, 2) if x else None, "players": p}
                      for (name, top), (h, x, p) in tally.items()}
        out[split]["events"] = len(cs)
    return out


def next_event(region: str | None = None, day: dt.date | None = None) -> dict:
    evs = events()
    day = day or (max(e["day"] for e in evs) + dt.timedelta(days=7))
    past = [e for e in evs if e["day"] < day]
    field = field_forecast(past, day, region)
    return {"day": day.isoformat(), "region": region, "field": field, "decks": deck_scores(past, day, field)}


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    region = argv[argv.index("--region") + 1] if "--region" in argv else None
    bf, bp = backtest_field(), backtest_picks()
    for split in ("before", "after"):
        print(f"{split} the rotation: field TVD {bf[split]}")
        for k, v in sorted(bp[split].items()):
            if k != "events":
                print(f"  {k:22} {v}")
    nx = next_event(region)
    print(f"next event ({nx['day']}, region {region}): field forecast and pick score")
    for a, d in sorted(nx["decks"].items(), key=lambda kv: -kv[1]["score"]):
        print(f"  {a:30} field {d['field']:.3f}  expected {d['expected']:.3f}  "
              f"conversion {d['conversion']:.2f}  score {d['score']:+.2f}")
    OUT.mkdir(exist_ok=True)
    nx["field"] = {k: round(v, 4) for k, v in sorted(nx["field"].items(), key=lambda kv: -kv[1])}
    nx["decks"] = {a: {k: round(v, 4) if isinstance(v, float) else v for k, v in d.items()}
                   for a, d in sorted(nx["decks"].items(), key=lambda kv: -kv[1]["score"])}
    (OUT / f"forecast{'_' + region if region else ''}.json").write_text(json.dumps(
        {"backtest": {"field": bf, "picks": bp}, "next": nx}, ensure_ascii=False, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
