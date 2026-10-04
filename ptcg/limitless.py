"""Major-tournament results from Limitless TCG (limitlesstcg.com and labs.limitlesstcg.com).

Per tournament we write data/tournaments/<date>_<limitless id>_<slug>/:
  meta.json       name, date, players, format code (e.g. TEF-30C), RK9 / Labs ids
  standings.csv   every player Labs lists: placing, record, points, archetype
  decklists.jsonl full 60-card lists Limitless publishes (usually Day 2 / top finishers)
  matches.csv     every Swiss and top-cut match with both archetypes and the result
and data/tournaments/index.csv lists all collected tournaments.
"""
from __future__ import annotations

import csv
import json
import re
from collections import defaultdict

from bs4 import BeautifulSoup

from . import http
from .paths import TOURNAMENTS

SITE = "https://limitlesstcg.com"
LABS = "https://labs.limitlesstcg.com"

# Limitless season filter values (season = Aug..Aug). 2324 is the first Scarlet & Violet season.
SEASONS = ["2324", "2425", "2526", "2627"]
TYPES = ["regional", "international", "special", "worlds"]

INDEX_FIELDS = ["limitless_id", "date", "name", "type", "country", "players", "format_code",
                "winner", "labs_id", "rk9_id", "dir"]


def _soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "lxml")


def _icons(node) -> tuple[str, ...]:
    return tuple(img["alt"] for img in node.select("img.pokemon"))


# --------------------------------------------------------------------------- listing

def list_tournaments(seasons=SEASONS, types=TYPES) -> list[dict]:
    """All Standard tournaments of the given seasons and types, oldest first."""
    found = {}
    for season in seasons:
        for typ in types:
            page = 1
            while True:
                url = (f"{SITE}/tournaments?time={season}&type={typ}&format=standard"
                       f"&region=all&show=100&page={page}")
                rows = parse_tournament_list(http.get(url, cache=False))
                for r in rows:
                    r["type"] = typ
                    found[r["limitless_id"]] = r
                if len(rows) < 100:
                    break
                page += 1
    return sorted(found.values(), key=lambda r: (r["date"], int(r["limitless_id"])))


def parse_tournament_list(html: str) -> list[dict]:
    out = []
    for tr in _soup(html).select("table.completed-tournaments tr[data-date]"):
        link = tr.select_one('a[href^="/tournaments/"]')
        out.append({
            "limitless_id": link["href"].rsplit("/", 1)[1],
            "date": tr["data-date"],
            "name": tr["data-name"],
            "country": tr.get("data-country", ""),
            "players": int(tr.get("data-players") or 0),
            "format": tr.get("data-format", ""),
            "winner": (tr.get("data-winner") or "").split("-", 1)[-1],
        })
    return out


# --------------------------------------------------------------------------- tournament page

def parse_tournament_page(html: str) -> dict:
    """Format code, RK9 and Labs ids, and the Limitless standings (placing, deck, list id)."""
    soup = _soup(html)
    info = soup.select_one(".infobox")
    fmt = info.select_one('a[href*="format="]') if info else None
    rk9 = soup.select_one('a[href*="rk9.gg/pairings/"]')
    labs = soup.find("a", href=re.compile(r"labs\.limitlesstcg\.com/\d+/"))
    standings = []
    for tr in soup.select("table.data-table tr[data-rank]"):
        deck_a = tr.select_one('a[href^="/decks/"]:not([href^="/decks/list"])')
        list_a = tr.select_one('a[href^="/decks/list/"]')
        player_a = tr.select_one('a[href^="/players/"]')
        standings.append({
            "placing": int(tr["data-rank"]),
            "name": tr["data-name"],
            "country": tr.get("data-country", ""),
            "archetype": tr.get("data-deck", ""),
            "archetype_id": deck_a["href"].split("/decks/")[1] if deck_a else "",
            "limitless_player_id": player_a["href"].rsplit("/", 1)[1] if player_a else "",
            "list_id": list_a["href"].rsplit("/", 1)[1] if list_a else "",
        })
    return {
        "format_code": fmt["href"].split("format=")[1] if fmt else "",
        "format_name": fmt.get_text(strip=True) if fmt else "",
        "rk9_id": rk9["href"].rsplit("/", 1)[1] if rk9 else "",
        "labs_id": re.search(r"labs\.limitlesstcg\.com/(\d+)/", labs["href"]).group(1) if labs else "",
        "standings": standings,
    }


def parse_decklists(html: str) -> list[dict]:
    """Every decklist on /tournaments/<id>/decklists, in placing order."""
    out = []
    soup = _soup(html)
    for block in soup.select("div.tournament-decklist"):
        title = block.select_one(".decklist-toggle").get_text(" ", strip=True)
        m = re.match(r"(\d+)\w*\s+(.*)", title)
        deck = block.select_one("div.decklist")
        cards = []
        for col in deck.select(".decklist-column"):
            section = col.select_one(".decklist-column-heading").get_text(strip=True).split(" (")[0]
            for c in col.select(".decklist-card"):
                cards.append({
                    "section": section,
                    "count": int(c.select_one(".card-count").get_text(strip=True)),
                    "name": c.select_one(".card-name").get_text(strip=True),
                    "set": c.get("data-set", ""),
                    "number": c.get("data-number", ""),
                })
        archetype = deck.select_one(".decklist-title")
        out.append({
            "placing": int(m.group(1)) if m else None,
            "player": m.group(2) if m else title,
            "archetype": archetype.find(string=True, recursive=False).strip() if archetype else "",
            "cards": cards,
        })
    return out


# --------------------------------------------------------------------------- labs

def parse_labs_decks(html: str) -> dict[tuple, dict]:
    """Archetype lookup from /<labs id>/decks: icon tuple -> {slug, name}; ambiguous icons map to None."""
    out: dict[tuple, dict | None] = {}
    soup = _soup(html)
    for tr in soup.select("table.data-table tbody tr"):
        a = tr.select_one('a[href*="/decks/"]')
        if not a:
            continue
        icons = _icons(tr)
        entry = {"slug": a["href"].rsplit("/", 1)[1], "name": a.get_text(strip=True)}
        out[icons] = None if icons in out else entry
    return out


def parse_labs_standings(html: str) -> list[dict]:
    rows = []
    soup = _soup(html)
    for tr in soup.select("table.data-table tbody tr"):
        tds = tr.find_all("td", recursive=False)
        player = tr.select_one('a[href*="/player/"]')
        if len(tds) < 8 or not player:
            continue
        deck = tr.select_one('a[href*="/decks/"]')
        rec = re.findall(r"\d+", tds[4].get_text(" ", strip=True))
        rows.append({
            "placing": int(tds[0].get_text(strip=True)),
            "labs_player_id": player["href"].split("/player/")[1].split("/")[0],
            "name": player.get_text(strip=True),
            "country": (tr.select_one("img[title]") or {}).get("title", ""),
            "points": int(tds[3].get_text(strip=True) or 0),
            "wins": int(rec[0]), "losses": int(rec[1]), "ties": int(rec[2]),
            "phase": " ".join(tr.get("class", [])),
            "archetype_slug": deck["href"].rsplit("/", 1)[1] if deck else "",
            "icons": "|".join(_icons(tr)),
        })
    return rows


def parse_labs_rounds(html: str) -> list[int]:
    return sorted({int(r) for r in re.findall(r"pairings\?round=(\d+)", html)} | {1})


def parse_labs_pairings(html: str) -> list[dict]:
    """One round of pairings: both players, their deck icons and the result."""
    out = []
    soup = _soup(html)
    for tr in soup.select("table.data-table tbody tr"):
        tds = tr.find_all("td", recursive=False)
        if len(tds) != 3:
            continue
        sides = []
        for td in tds[1:]:
            a = td.select_one('a[href*="/player/"]')
            if not a:
                sides.append(None)
                continue
            name = a.select_one("span.text-center")
            flag = a.select_one("img[title]")
            sides.append({
                "country": flag["title"] if flag else "",
                "id": a["href"].split("/player/")[1].split("/")[0],
                "name": name.get_text(strip=True) if name else "",
                "icons": "|".join(_icons(a)),
                "win": "winner" in td.get("class", []),
                "tie": "tie" in td.get("class", []),
            })
        p1, p2 = sides
        if p1 is None:
            continue
        if p2 is None:
            result = "bye" if p1["win"] else "unpaired"
        elif p1["tie"] or p2["tie"]:
            result = "tie"
        elif p1["win"]:
            result = "p1"
        elif p2["win"]:
            result = "p2"
        else:
            result = "double_loss"
        out.append({"table": tds[0].get_text(strip=True), "p1": p1, "p2": p2, "result": result})
    return out


# --------------------------------------------------------------------------- collect

def _slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def tournament_dir(t: dict):
    return TOURNAMENTS / f"{t['date']}_{t['limitless_id']}_{_slug(t['name'])}"


def collect_tournament(t: dict) -> dict:
    """Fetch and write one tournament. Returns its index row."""
    out = tournament_dir(t)
    out.mkdir(parents=True, exist_ok=True)
    page = parse_tournament_page(http.get(f"{SITE}/tournaments/{t['limitless_id']}"))
    decklists = parse_decklists(http.get(f"{SITE}/tournaments/{t['limitless_id']}/decklists"))
    with open(out / "decklists.jsonl", "w", encoding="utf-8") as f:
        by_place = {s["placing"]: s for s in page["standings"]}
        for d in decklists:
            s = by_place.get(d["placing"], {})
            d.update({"country": s.get("country", ""), "limitless_archetype_id": s.get("archetype_id", ""),
                      "list_id": s.get("list_id", "")})
            if s.get("archetype"):
                d["archetype"] = s["archetype"]
            f.write(json.dumps(d, ensure_ascii=False) + "\n")

    n_matches = n_standings = 0
    if page["labs_id"]:
        lid = page["labs_id"]
        archetypes = parse_labs_decks(http.get(f"{LABS}/{lid}/decks"))
        slug_name = {v["slug"]: v["name"] for v in archetypes.values() if v}
        standings = parse_labs_standings(http.get(f"{LABS}/{lid}/standings"))
        players = {s["labs_player_id"]: s for s in standings}

        def archetype(pid: str, icons: str) -> tuple[str, str]:
            s = players.get(pid)
            if s and s["archetype_slug"]:
                return s["archetype_slug"], slug_name.get(s["archetype_slug"], s["archetype_slug"])
            hit = archetypes.get(tuple(icons.split("|")) if icons else ())
            return (hit["slug"], hit["name"]) if hit else ("", " ".join(icons.split("|")) or "unknown")

        first = http.get(f"{LABS}/{lid}/pairings?round=1")
        matches = []
        for rnd in parse_labs_rounds(first):
            html = first if rnd == 1 else http.get(f"{LABS}/{lid}/pairings?round={rnd}")
            for m in parse_labs_pairings(html):
                row = {"round": rnd, "table": m["table"], "result": m["result"]}
                for side in ("p1", "p2"):
                    p = m[side] or {"id": "", "name": "", "icons": "", "country": ""}
                    slug, name = archetype(p["id"], p["icons"]) if p["id"] else ("", "")
                    row.update({f"{side}_id": p["id"], f"{side}_name": p["name"],
                                f"{side}_country": p["country"],
                                f"{side}_archetype": name, f"{side}_archetype_slug": slug,
                                f"{side}_icons": p["icons"]})
                matches.append(row)
        full = full_standings(standings, matches)
        _write_csv(out / "standings.csv", full)
        _write_csv(out / "matches.csv", matches)
        n_matches, n_standings = len(matches), len(full)

    meta = {**{k: t[k] for k in ("limitless_id", "date", "name", "type", "country", "players", "winner")},
            "format_code": page["format_code"], "format_name": page["format_name"],
            "rk9_id": page["rk9_id"], "labs_id": page["labs_id"],
            "counts": {"decklists": len(decklists), "standings": n_standings, "matches": n_matches},
            "sources": [f"{SITE}/tournaments/{t['limitless_id']}"]
            + ([f"{LABS}/{page['labs_id']}/standings"] if page["labs_id"] else [])
            + ([f"https://rk9.gg/pairings/{page['rk9_id']}"] if page["rk9_id"] else [])}
    (out / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"  {t['date']} {t['name']}: {len(decklists)} lists, {n_standings} standings, {n_matches} matches")
    return {**{k: meta[k] for k in INDEX_FIELDS if k in meta}, "dir": out.name}


def full_standings(labs: list[dict], matches: list[dict]) -> list[dict]:
    """Every player in the event. Labs only lists the top 512 with placings, so the rest get
    their record from the match results and no placing."""
    top = {s["labs_player_id"]: s for s in labs}
    players: dict[str, dict] = {}
    for m in matches:
        for side, other in (("p1", "p2"), ("p2", "p1")):
            pid = m[f"{side}_id"]
            if not pid:
                continue
            p = players.setdefault(pid, {
                "labs_player_id": pid, "name": m[f"{side}_name"], "country": m[f"{side}_country"],
                "archetype": m[f"{side}_archetype"], "archetype_slug": m[f"{side}_archetype_slug"],
                "icons": m[f"{side}_icons"], "wins": 0, "losses": 0, "ties": 0, "rounds": 0})
            res = m["result"]
            p["rounds"] += 1
            if res == "tie":
                p["ties"] += 1
            elif res == side or res == "bye":
                p["wins"] += 1
            elif res in (other, "double_loss", "unpaired"):
                p["losses"] += 1
    rows = []
    for pid, p in players.items():
        t = top.get(pid)
        if t:  # Labs' own record is Swiss-only, which is what points and placings use
            p.update({k: t[k] for k in ("wins", "losses", "ties")})
        rows.append({
            "placing": t["placing"] if t else "", "labs_player_id": pid, "name": p["name"],
            "country": p["country"], "wins": p["wins"], "losses": p["losses"], "ties": p["ties"],
            "points": t["points"] if t else 3 * p["wins"] + p["ties"], "day2": "day2" in (t or {}).get("phase", ""),
            "top_cut": "topcut" in (t or {}).get("phase", ""),
            "archetype": p["archetype"], "archetype_slug": p["archetype_slug"], "icons": p["icons"],
        })
    rows.sort(key=lambda r: (r["placing"] == "", r["placing"] or 0, -r["points"], r["name"]))
    return rows


def _write_csv(path, rows):
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def load_index() -> list[dict]:
    path = TOURNAMENTS / "index.csv"
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def collect(max_new: int | None = None, refresh_days: int = 0, seasons=SEASONS) -> int:
    """Collect up to max_new tournaments not yet in the index (newest first). Returns how many.

    refresh_days re-collects already indexed events from the last N days, since Limitless
    sometimes fills in lists and Labs data a few days after an event.
    """
    import datetime as dt

    TOURNAMENTS.mkdir(parents=True, exist_ok=True)
    index = {r["limitless_id"]: r for r in load_index()}
    cutoff = (dt.date.today() - dt.timedelta(days=refresh_days)).isoformat()
    listed = sorted(list_tournaments(seasons), key=lambda t: t["date"], reverse=True)
    new = [t for t in listed if t["limitless_id"] not in index]
    if max_new is not None:
        new = new[:max_new]
    recent = [t for t in listed if t["limitless_id"] in index and refresh_days and t["date"] >= cutoff]
    todo = new + recent
    print(f"tournaments: {len(index)} indexed, collecting {len(new)} new, refreshing {len(recent)}")
    for t in todo:
        try:
            index[t["limitless_id"]] = collect_tournament(t)
        except Exception as e:  # keep going; the event is retried next run
            print(f"  FAILED {t['date']} {t['name']}: {e!r}")
            continue
        _write_index(index)
    return len(new)


def _write_index(index: dict) -> None:
    rows = sorted(index.values(), key=lambda r: (r["date"], int(r["limitless_id"])))
    with open(TOURNAMENTS / "index.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=INDEX_FIELDS, lineterminator="\n")
        w.writeheader()
        w.writerows({k: r.get(k, "") for k in INDEX_FIELDS} for r in rows)
