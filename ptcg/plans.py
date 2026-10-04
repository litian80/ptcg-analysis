"""Load and check the hand-written archetype game plans in data/archetypes/<slug>.yaml.

    python -m ptcg.plans          # check every plan; exit code 1 on errors

A plan says how a deck sets up, which Pokémon attack, and the order it takes Prize cards.
The checks keep the facts in a plan tied to the data: every card named exists in the card
database, the Prize count written next to each Pokémon matches its card type (Mega
Pokémon ex give 3, other ex and V give 2, everything else 1), every Prize route adds up to
the Prizes it claims, and slugs and matchup win rates match data/archetypes/meta_<window>.json.
Win rates that have drifted from the meta file are warnings, not errors: the meta file is
regenerated as new events come in, the plan text is not.
"""
from __future__ import annotations

import csv
import functools
import json
import sys

import yaml

from .paths import CARDS, DATA

ARCHETYPES = DATA / "archetypes"
REQUIRED = ["slug", "name", "window", "summary", "setup", "attackers", "prize_map", "matchups"]
DRIFT = 0.05


@functools.cache
def _cards() -> dict[str, list[dict]]:
    by_name: dict[str, list[dict]] = {}
    with open(CARDS / "cards.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            by_name.setdefault(r["name"], []).append(r)
    return by_name


@functools.cache
def _meta(window: str) -> dict:
    return json.loads((ARCHETYPES / f"meta_{window}.json").read_text(encoding="utf-8"))


def prizes_for(name: str) -> int | None:
    """Prize cards the opponent takes for knocking out this Pokémon (None if unknown)."""
    rows = [r for r in _cards().get(name, []) if r["supertype"] == "Pokémon"]
    if not rows:
        return None
    subtypes = set(rows[-1]["subtypes"].split("|"))
    if "MEGA" in subtypes:
        return 3
    if subtypes & {"ex", "V", "VSTAR", "GX", "EX"}:
        return 2
    if "VMAX" in subtypes:
        return 3
    return 1


def load(slug: str) -> dict:
    return yaml.safe_load((ARCHETYPES / f"{slug}.yaml").read_text(encoding="utf-8"))


def load_all() -> dict[str, dict]:
    return {p.stem: yaml.safe_load(p.read_text(encoding="utf-8"))
            for p in sorted(ARCHETYPES.glob("*.yaml"))}


def check(plan: dict) -> tuple[list[str], list[str]]:
    errors, warnings = [], []
    for k in REQUIRED:
        if k not in plan:
            errors.append(f"missing key {k}")
    if errors:
        return errors, warnings
    try:
        meta = _meta(plan["window"])["archetypes"]
    except FileNotFoundError:
        return [f"no meta file for window {plan['window']}"], warnings
    if plan["slug"] not in meta:
        errors.append(f"slug {plan['slug']} not in meta_{plan['window']}.json")

    pokemon = list(plan["attackers"]) + list(plan.get("support", []))
    for t in plan.get("copy_targets", []):
        pokemon.append({**t, "prizes": prizes_for(t["card"])})
    for p in pokemon:
        expected = prizes_for(p["card"])
        if expected is None:
            errors.append(f"{p['card']}: not a Pokémon in data/cards/cards.csv")
        elif p.get("prizes") != expected:
            errors.append(f"{p['card']}: prizes is {p.get('prizes')}, card type says {expected}")
        if "printing" in p:
            code, _, number = p["printing"].partition(" ")
            if not any(r["code"] == code and r["number"] == number for r in _cards().get(p["card"], [])):
                errors.append(f"{p['card']}: no printing {p['printing']} with that name")
    for name in plan["setup"].get("key_cards", []):
        if name not in _cards():
            errors.append(f"setup.key_cards: {name} not in data/cards/cards.csv")

    for route in plan["prize_map"].get("routes", []):
        total = sum(s["take"] for s in route["steps"])
        if total != route.get("total", 6):
            errors.append(f"prize route {route['name']!r} takes {total}, expected {route.get('total', 6)}")

    for m in plan["matchups"]:
        if m["vs"] not in meta:
            errors.append(f"matchup vs {m['vs']}: slug not in meta_{plan['window']}.json")
            continue
        actual = next((x for x in meta.get(plan["slug"], {}).get("matchups", []) if x["vs"] == m["vs"]), None)
        if actual is None:
            warnings.append(f"matchup vs {m['vs']}: too few matches in the meta file")
        elif abs(actual["win_rate"] - m["win_rate"]) > DRIFT:
            warnings.append(f"matchup vs {m['vs']}: plan says {m['win_rate']}, meta now {actual['win_rate']}")
    return errors, warnings


def main() -> int:
    bad = 0
    for slug, plan in load_all().items():
        errors, warnings = check(plan)
        for w in warnings:
            print(f"{slug}: warning: {w}")
        for e in errors:
            print(f"{slug}: ERROR: {e}")
        bad += bool(errors)
    print(f"plans: {len(load_all())} checked, {bad} with errors")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
