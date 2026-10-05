"""python -m ptcg.goldfish <deck-slug|all> [games]"""
from __future__ import annotations

import json
import sys

from ..paths import DATA
from . import DECKS, report

OUT = DATA / "goldfish"


def fmt(k: str, v) -> str:
    if v is None:
        return "-"
    return f"{v:.1f}" if "均值" in k else f"{v:.1%}"


def main(argv: list[str]) -> None:
    args = [a for a in argv if not a.startswith("-")]
    if not args or (args[0] not in DECKS and args[0] != "all"):
        print(__doc__.strip())
        print("decks:", ", ".join(DECKS), "| all")
        if args and args[0].isdigit():
            print("(the deck slug now comes first, e.g. `python -m ptcg.goldfish alakazam-dudunsparce 20000`)")
        sys.exit(2)
    slugs = list(DECKS) if args[0] == "all" else [args[0]]
    games = int(args[1]) if len(args) > 1 else 20000
    OUT.mkdir(parents=True, exist_ok=True)
    for slug in slugs:
        rep = report(slug, games)
        (OUT / f"{slug}.json").write_text(json.dumps(rep, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"== {rep['name']}（{rep['list_source']}，每边 {games} 局）")
        res = rep["results"]
        for k in res["先攻"]:
            print(f"  {k}: 先攻 {fmt(k, res['先攻'][k])} / 后攻 {fmt(k, res['后攻'][k])}")
        for t in rep["tuning"]:
            print(f"  -- {t['question']}")
            for side, rows in t["delta_pp"].items():
                moved = {k: v for k, v in rows.items() if abs(v) >= (0.2 if "均值" in k else 1.0)}
                if moved:
                    print(f"     {side}: " + "；".join(f"{k} {v:+}" + ("" if "均值" in k else "pp") for k, v in moved.items()))
        print(f"  -> {OUT / (slug + '.json')}")


if __name__ == "__main__":
    main(sys.argv[1:])
