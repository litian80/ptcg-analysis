"""Command line: python -m ptcg <command>.

  cards         refresh data/cards from pokemon-tcg-data
  pools         rebuild data/formats/<season>/card_pool.csv and the current card-name list
  tournaments   collect new major Standard tournaments from Limitless
  windows       rebuild data/formats/limitless_formats.csv (set windows seen at events)
  check         warn when the rotation file looks out of date (exit code 1)
  all           cards, pools, tournaments, windows
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import sys

from . import cards, limitless
from .formats import load_seasons
from .paths import FORMATS


def windows() -> None:
    """One row per Limitless format code (first set - last legal set) seen at a collected event."""
    agg: dict[str, dict] = {}
    for r in limitless.load_index():
        code = r["format_code"]
        if not code:
            continue
        a = agg.setdefault(code, {"format_code": code, "first_event": r["date"], "last_event": r["date"],
                                  "events": 0})
        a["first_event"] = min(a["first_event"], r["date"])
        a["last_event"] = max(a["last_event"], r["date"])
        a["events"] += 1
    rows = sorted(agg.values(), key=lambda a: a["first_event"])
    with open(FORMATS / "limitless_formats.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["format_code", "first_event", "last_event", "events"],
                           lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print(f"windows: {len(rows)} format codes")


def check() -> list[str]:
    """Problems that mean data/formats/standard_rotations.json needs a human update."""
    problems = []
    seasons = load_seasons()
    current = seasons[-1]
    today = dt.date.today()
    known = set(current.legal_regulation_marks) | {m for s in seasons for m in s.rotated_out}
    for s in cards.load_sets():
        new = set(s["regulation_marks"]) - known
        for m in sorted(new):
            problems.append(f"Set {s['name']} ({s['code']}) has regulation mark {m}, which no season lists.")
    # Rotations happen every spring; by the following March the next one should be on record.
    if today >= dt.date(current.tournament_start.year + 1, 3, 1):
        problems.append(f"No Standard season after {current.id} is on record; the next rotation "
                        "is usually announced in the autumn and takes effect in April.")
    return problems


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="ptcg")
    ap.add_argument("command", choices=["cards", "pools", "tournaments", "windows", "check", "all"])
    ap.add_argument("--max", type=int, default=None, help="tournaments: at most N events this run")
    ap.add_argument("--refresh-days", type=int, default=14,
                    help="tournaments: re-collect events from the last N days")
    ap.add_argument("--seasons", default=",".join(limitless.SEASONS),
                    help="tournaments: Limitless season filters, e.g. 2526,2627")
    args = ap.parse_args(argv)

    if args.command in ("cards", "all"):
        cards.fetch()
    if args.command in ("pools", "all", "cards"):
        cards.write_pools()
    if args.command in ("tournaments", "all"):
        limitless.collect(args.max, args.refresh_days, args.seasons.split(","))
    if args.command in ("windows", "tournaments", "all"):
        windows()
    if args.command == "check":
        problems = check()
        for p in problems:
            print(p)
        return 1 if problems else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
