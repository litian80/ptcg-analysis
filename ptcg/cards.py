"""Card database and Standard card pools.

Source: https://github.com/PokemonTCG/pokemon-tcg-data (the data behind pokemontcg.io),
which carries each card's regulation mark. Only sets from Sword & Shield onwards are kept,
since regulation marks start there.
"""
from __future__ import annotations

import csv
import hashlib
import json
from dataclasses import dataclass

from . import http
from .formats import Season, load_seasons
from .paths import CARDS, FORMATS

RAW = "https://raw.githubusercontent.com/PokemonTCG/pokemon-tcg-data/master"
SINCE = "2020/01/01"

# pokemon-tcg-data ptcgoCode -> code used by Limitless / TCG Live deck exports.
CODE_ALIASES = {"PR-SV": "SVP", "PR-ME": "MEP"}

SET_FIELDS = ["set_id", "code", "name", "series", "release_date", "total", "regulation_marks"]
CARD_FIELDS = [
    "card_id", "set_id", "code", "number", "name", "supertype", "subtypes", "regulation_mark",
    "hp", "types", "evolves_from", "rarity", "functional_id",
]


def functional_id(card: dict) -> str:
    """Identity of a card for legality purposes: equal across reprints.

    Trainers and Energy are identified by name and subtype (reprints often get re-templated
    wording, e.g. Boss's Orders). Pokémon by name, HP, and ability and attack names/damage.
    """
    if card["supertype"] == "Pokémon":
        keep = [card["name"], card.get("hp"),
                [a["name"] for a in card.get("abilities") or []],
                [(a["name"], a.get("damage", "")) for a in card.get("attacks") or []]]
    else:
        keep = [card["name"], card["supertype"], sorted(card.get("subtypes") or [])]
    blob = json.dumps(keep, sort_keys=True, ensure_ascii=False)
    return hashlib.sha1(blob.encode()).hexdigest()[:12]


def is_basic_energy(card: dict) -> bool:
    return card["supertype"] == "Energy" and "Basic" in (card.get("subtypes") or [])


def fetch() -> None:
    """Download sets and cards and write data/cards/sets.csv and cards.csv."""
    sets = json.loads(http.get(f"{RAW}/sets/en.json", cache=False))
    sets = sorted((s for s in sets if s["releaseDate"] >= SINCE), key=lambda s: (s["releaseDate"], s["id"]))
    set_rows, card_rows = [], []
    for s in sets:
        cards = json.loads(http.get(f"{RAW}/cards/en/{s['id']}.json", cache=False))
        code = CODE_ALIASES.get(s.get("ptcgoCode"), s.get("ptcgoCode") or "")
        marks = sorted({c.get("regulationMark") or "" for c in cards} - {""})
        set_rows.append({
            "set_id": s["id"], "code": code, "name": s["name"], "series": s["series"],
            "release_date": s["releaseDate"].replace("/", "-"), "total": s["total"],
            "regulation_marks": "".join(marks),
        })
        for c in cards:
            card_rows.append({
                "card_id": c["id"], "set_id": s["id"], "code": code, "number": c["number"],
                "name": c["name"], "supertype": c["supertype"],
                "subtypes": "|".join(c.get("subtypes") or []),
                "regulation_mark": c.get("regulationMark") or "",
                "hp": c.get("hp") or "", "types": "|".join(c.get("types") or []),
                "evolves_from": c.get("evolvesFrom") or "", "rarity": c.get("rarity") or "",
                "functional_id": functional_id(c),
            })
    CARDS.mkdir(parents=True, exist_ok=True)
    _write(CARDS / "sets.csv", SET_FIELDS, set_rows)
    _write(CARDS / "cards.csv", CARD_FIELDS, card_rows)
    print(f"cards: {len(set_rows)} sets, {len(card_rows)} printings")


def _write(path, fields, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def load_sets() -> list[dict]:
    with open(CARDS / "sets.csv", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_cards() -> list[dict]:
    with open(CARDS / "cards.csv", encoding="utf-8") as f:
        return list(csv.DictReader(f))


@dataclass
class PoolCard:
    name: str
    functional_id: str
    supertype: str
    subtypes: str
    regulation_marks: set
    printings: list  # "CODE NUMBER" strings


def pool(season: Season, last_set: str | None = None, cards: list[dict] | None = None,
         sets: list[dict] | None = None) -> list[PoolCard]:
    """Distinct Standard-legal cards for a season, optionally only sets up to `last_set` (a code).

    A card (by functional_id) is legal when any printing of it carries a legal regulation mark;
    then all of its printings may be played. Basic Energy is always legal.
    """
    cards = cards if cards is not None else load_cards()
    sets = sets if sets is not None else load_sets()
    release = {s["set_id"]: s["release_date"] for s in sets}
    cutoff = None
    if last_set:
        dates = [s["release_date"] for s in sets if s["code"] == last_set]
        if not dates:
            raise KeyError(f"unknown set code {last_set}")
        cutoff = max(dates)
    by_fid: dict[str, PoolCard] = {}
    legal_fids = set()
    for c in cards:
        if cutoff and release[c["set_id"]] > cutoff:
            continue
        p = by_fid.setdefault(c["functional_id"], PoolCard(
            c["name"], c["functional_id"], c["supertype"], c["subtypes"], set(), []))
        p.printings.append(f"{c['code']} {c['number']}")
        if c["regulation_mark"]:
            p.regulation_marks.add(c["regulation_mark"])
        basic_energy = c["supertype"] == "Energy" and "Basic" in c["subtypes"].split("|")
        if basic_energy or c["regulation_mark"] in season.legal_regulation_marks:
            if c["name"] not in season.banned:
                legal_fids.add(c["functional_id"])
    return sorted((by_fid[f] for f in legal_fids), key=lambda p: (p.supertype, p.name, p.functional_id))


def write_pools() -> None:
    """Write data/formats/<season>/card_pool.csv for every season, plus the current name list."""
    cards, sets = load_cards(), load_sets()
    seasons = load_seasons()
    for season in seasons:
        rows = pool(season, cards=cards, sets=sets)
        out = FORMATS / season.id
        out.mkdir(parents=True, exist_ok=True)
        _write(out / "card_pool.csv",
               ["name", "supertype", "subtypes", "regulation_marks", "functional_id", "printings"],
               [{"name": p.name, "supertype": p.supertype, "subtypes": p.subtypes,
                 "regulation_marks": "".join(sorted(p.regulation_marks)),
                 "functional_id": p.functional_id, "printings": "; ".join(p.printings)} for p in rows])
        print(f"pool {season.id}: {len(rows)} distinct cards, {len({p.name for p in rows})} names")
    current = seasons[-1]
    names = sorted({p.name for p in pool(current, cards=cards, sets=sets)})
    (CARDS / "standard_card_names.txt").write_text("\n".join(names) + "\n", encoding="utf-8")
