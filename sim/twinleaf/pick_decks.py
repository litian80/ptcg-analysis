"""Pick one representative decklist per archetype for the Twinleaf battle sim.

For each slug: best-placing list at the most recent event that has one
(Frankfurt, then Brisbane, then Baltimore, then Worlds). Writes decks.json.

    python sim/twinleaf/pick_decks.py
"""
import csv, glob, json, os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
EVENTS = [
    "2026-09-26_579_regional-frankfurt",
    "2026-09-26_578_regional-brisbane",
    "2026-09-19_577_regional-baltimore-md",
    "2026-08-28_515_world-championships-2026",
]
RECOMMENDED = ["basic-box-m", "alakazam-dusknoir", "crustle-dri", "dragapult-ex", "slowking-scr"]


def opponents():
    return sorted(os.path.basename(p)[:-5] for p in glob.glob(os.path.join(ROOT, "data/archetypes/*.yaml")))


def load_event(ev):
    d = os.path.join(ROOT, "data/tournaments", ev)
    slug_by = {}
    with open(os.path.join(d, "standings.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["placing"]:
                slug_by[(int(r["placing"]), r["name"])] = r["archetype_slug"]
    lists = []
    with open(os.path.join(d, "decklists.jsonl"), encoding="utf-8") as f:
        for line in f:
            x = json.loads(line)
            x["slug"] = slug_by.get((x["placing"], x["player"]))
            x["event"] = ev
            lists.append(x)
    return lists


def main():
    want = list(dict.fromkeys(RECOMMENDED + opponents()))
    by_event = {ev: load_event(ev) for ev in EVENTS}
    out = {}
    for slug in want:
        for ev in EVENTS:
            cands = sorted((x for x in by_event[ev] if x["slug"] == slug), key=lambda x: x["placing"])
            if cands:
                x = cands[0]
                cards = x["cards"]["pokemon"] + x["cards"]["trainer"] + x["cards"]["energy"]
                assert sum(int(c.split(" ", 1)[0]) for c in cards) == 60, (slug, ev)
                out[slug] = {"event": ev, "placing": x["placing"], "player": x["player"],
                             "archetype": x["archetype"], "cards": cards}
                break
        else:
            print("no list for", slug)
    path = os.path.join(ROOT, "sim/twinleaf/decks.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"recommended": RECOMMENDED, "opponents": opponents(), "decks": out}, f, ensure_ascii=False, indent=1)
    for s, d in out.items():
        print(f"{s:28s} {d['event'][:30]:30s} #{d['placing']:<4d} {d['archetype']}")


if __name__ == "__main__":
    main()
