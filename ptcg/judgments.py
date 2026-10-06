"""Key judgments in the playbooks, the evidence for and against them, and player feedback.

    python -m ptcg.judgments check            # validate files and playbook marks; exit 1 on errors
    python -m ptcg.judgments sync             # rewrite the confidence marks in the playbooks
    python -m ptcg.judgments stale            # judgments the format has moved under; exit 1 if any
    python -m ptcg.judgments calibration      # do judgments marked 70% hold about 70% of the time?
    python -m ptcg.judgments pending [deck] [vs]   # what a review of this matchup should look for

A judgment is one call a playbook makes that a game can prove right or wrong ("going second
is better in the Alakazam Dusknoir mirror"). Each lives in data/judgments/<deck>.yaml with the
confidence it was written with and how many games that confidence is worth (`weight`).
Every later game review, video review or piece of player feedback is a source file in
data/judgments/sources/ that records, per judgment, whether it held. The current confidence
is the written one updated by those results; feedback counts half as much as a game.

The playbooks carry the current confidence next to the judgment as （信心 70%，akd-mir-01）;
`sync` keeps those numbers equal to the computed ones. Card facts that can be checked against
card text are not judgments: they are checked, then written as fact.
"""
from __future__ import annotations

import csv
import functools
import json
import re
import sys
from pathlib import Path

import yaml

from .paths import CARDS, DATA, ROOT

JUDGMENTS = DATA / "judgments"
SOURCES = JUDGMENTS / "sources"
ARCHETYPES = DATA / "archetypes"
MARK = re.compile(r"（信心 (\d+)%，([a-z0-9]+(?:-[a-z0-9]+)+)）")
DEFAULT_WEIGHT = 4
SOURCE_KINDS = {"log": 1.0, "video": 1.0, "feedback": 0.5}
RESULTS = {"log": {"held": 1, "failed": 0}, "video": {"held": 1, "failed": 0},
           "feedback": {"agree": 1, "disagree": 0}}
CLAIM_TYPES = {"纠错", "新打法", "全局观", "备选路线", "玩家观点", "复盘盲点"}
CLAIM_STATUS = {"待验证", "已转正", "已否定", "观点", "已核对"}
CORE_FLOOR = 0.25   # meta files list a card in a deck's core only above this share
USAGE_SHIFT = 0.25  # a card's share of lists moving this much means the matchup changed


@functools.cache
def _card_names() -> frozenset[str]:
    with open(CARDS / "cards.csv", encoding="utf-8") as f:
        return frozenset(r["name"] for r in csv.DictReader(f))


@functools.cache
def _standard_names() -> frozenset[str]:
    return frozenset((CARDS / "standard_card_names.txt").read_text(encoding="utf-8").split("\n")) - {""}


@functools.cache
def _meta(window: str) -> dict | None:
    p = ARCHETYPES / f"meta_{window}.json"
    return json.loads(p.read_text(encoding="utf-8"))["archetypes"] if p.exists() else None


def load_judgments(root: Path = JUDGMENTS) -> dict[str, dict]:
    """Every judgment by id, with its deck filled in."""
    out = {}
    for p in sorted(root.glob("*.yaml")):
        doc = yaml.safe_load(p.read_text(encoding="utf-8"))
        for j in doc.get("judgments", []):
            out.setdefault(j["id"], []).append({**j, "deck": doc["deck"], "_file": p.name})
    return {k: v[0] if len(v) == 1 else {**v[0], "_dupes": len(v)} for k, v in out.items()}


def load_sources(root: Path = SOURCES) -> list[dict]:
    docs = []
    for p in sorted(root.glob("*.yaml")):
        doc = yaml.safe_load(p.read_text(encoding="utf-8"))
        docs.append({**doc, "_file": p.name})
    return sorted(docs, key=lambda d: (str(d.get("date")), d["_file"]))


def history(jid: str, judgment: dict, sources: list[dict]) -> list[tuple[dict, dict, float, int]]:
    """(source, observation, weight, success) for every result recorded on this judgment, oldest first."""
    rows = []
    for s in sources:
        for o in s.get("observations", []):
            if o.get("judgment") != jid:
                continue
            result = RESULTS.get(s["kind"], {}).get(o.get("result"))
            if result is not None:
                rows.append((s, o, SOURCE_KINDS[s["kind"]], result))
    return rows


def confidence(judgment: dict, rows) -> float:
    w = judgment.get("weight", DEFAULT_WEIGHT)
    num = judgment["confidence"] * w + sum(wt * ok for _, _, wt, ok in rows)
    return num / (w + sum(wt for _, _, wt, _ in rows))


def shown(p: float) -> int:
    """The percentage written in the playbooks: nearest 5."""
    return int(5 * round(p * 20))


def current(judgments: dict[str, dict], sources: list[dict]) -> dict[str, float]:
    return {jid: confidence(j, history(jid, j, sources)) for jid, j in judgments.items()}


def marks(path: Path) -> list[tuple[int, str]]:
    return [(int(m.group(1)), m.group(2)) for m in MARK.finditer(path.read_text(encoding="utf-8"))]


def check(judgments: dict[str, dict], sources: list[dict], root: Path = ROOT) -> tuple[list[str], list[str]]:
    errors, warnings = [], []
    names = _card_names()
    for jid, j in judgments.items():
        where = f"{j['_file']} {jid}"
        if j.get("_dupes"):
            errors.append(f"{where}: id used {j['_dupes']} times")
        for k in ("text", "confidence", "window", "where"):
            if k not in j:
                errors.append(f"{where}: missing {k}")
        c = j.get("confidence")
        if c is not None and not 0.5 <= c <= 0.99:
            errors.append(f"{where}: confidence {c} must be 0.5-0.99 (write the opposite call if it is below 0.5)")
        for card in j.get("depends_on", []):
            if card not in names:
                errors.append(f"{where}: depends_on {card!r} is not in data/cards/cards.csv")
        alt = j.get("alternative_to")
        if alt and alt not in judgments:
            errors.append(f"{where}: alternative_to {alt} is not a judgment")
        if "where" in j and not (root / j["where"]).exists():
            errors.append(f"{where}: where {j['where']} does not exist")

    claim_ids = set()
    for s in sources:
        f = s["_file"]
        if s.get("kind") not in SOURCE_KINDS:
            errors.append(f"{f}: kind must be one of {sorted(SOURCE_KINDS)}")
            continue
        for k in ("date", "ref", "window"):
            if k not in s:
                errors.append(f"{f}: missing {k}")
        if s["kind"] == "feedback" and not s.get("reviewer"):
            errors.append(f"{f}: feedback needs a reviewer alias")
        for o in s.get("observations", []):
            if o.get("judgment") not in judgments:
                errors.append(f"{f}: observation on unknown judgment {o.get('judgment')}")
            if o.get("result") not in set(RESULTS[s["kind"]]) | {"n/a"}:
                errors.append(f"{f}: {o.get('judgment')} result {o.get('result')!r}; "
                              f"{s['kind']} takes {sorted(RESULTS[s['kind']])} or n/a")
        for c in s.get("claims", []):
            cid = c.get("id")
            if cid in claim_ids:
                errors.append(f"{f}: claim id {cid} used twice")
            claim_ids.add(cid)
            if c.get("type") not in CLAIM_TYPES:
                errors.append(f"{f}: claim {cid} type {c.get('type')!r}; one of {sorted(CLAIM_TYPES)}")
            if c.get("status") not in CLAIM_STATUS:
                errors.append(f"{f}: claim {cid} status {c.get('status')!r}; one of {sorted(CLAIM_STATUS)}")
            if c.get("status") == "已转正" and c.get("promoted_to") not in judgments:
                errors.append(f"{f}: claim {cid} is 已转正 but promoted_to is not a judgment")
            for card in c.get("depends_on", []):
                if card not in names:
                    errors.append(f"{f}: claim {cid} depends_on {card!r} is not in data/cards/cards.csv")

    now = current(judgments, sources)
    seen: dict[str, set[str]] = {}
    for path in sorted({j["where"] for j in judgments.values() if "where" in j}):
        p = root / path
        if not p.exists():
            continue
        for pct, jid in marks(p):
            seen.setdefault(jid, set()).add(path)
            if jid not in judgments:
                errors.append(f"{path}: mark for unknown judgment {jid}")
            elif pct != shown(now[jid]):
                warnings.append(f"{path}: {jid} marked {pct}%, now {shown(now[jid])}% (run sync)")
    for jid, p in now.items():
        if p < 0.5:
            warnings.append(f"{jid}: confidence {shown(p)}%, below even: rewrite the playbook line or "
                            "write the opposite call as a new judgment")
    for jid, j in judgments.items():
        if "where" in j and j["where"] not in seen.get(jid, set()):
            errors.append(f"{j['where']}: no （信心 …，{jid}） mark")
    return errors, warnings


def sync(judgments: dict[str, dict], sources: list[dict], root: Path = ROOT) -> list[str]:
    now = current(judgments, sources)
    changed = []

    def repl(m):
        jid = m.group(2)
        return f"（信心 {shown(now[jid])}%，{jid}）" if jid in now else m.group(0)

    for path in sorted({j["where"] for j in judgments.values() if "where" in j}):
        p = root / path
        text = p.read_text(encoding="utf-8")
        new = MARK.sub(repl, text)
        if new != text:
            p.write_text(new, encoding="utf-8")
            changed.append(path)
    return changed


def _in_lists(window: str, slug: str) -> dict[str, float] | None:
    meta = _meta(window)
    if meta is None or slug not in meta:
        return None
    core = meta[slug].get("core", [])
    return {c["name"]: c["in_lists"] for c in core}


def stale(judgments: dict[str, dict], sources: list[dict], latest: str) -> list[str]:
    """Judgments to look at again: a card they depend on left Standard, or the window moved and
    the deck or the opponent changed how often it plays a card the judgment depends on."""
    out = []
    standard = _standard_names()
    items = [(jid, j) for jid, j in judgments.items()]
    for s in sources:
        for c in s.get("claims", []):
            if c.get("status") in {"待验证", "观点"}:
                items.append((c["id"], {**c, "window": s.get("window")}))
    for jid, j in items:
        why = [f"{card} 已不在 Standard" for card in j.get("depends_on", []) if card not in standard]
        window = j.get("window")
        if window and window != latest:
            for slug in dict.fromkeys(filter(None, [j.get("deck"), j.get("vs")])):
                old, new = _in_lists(window, slug), _in_lists(latest, slug)
                if old is None or new is None:
                    if old is not None:
                        why.append(f"{slug} 在 {latest} 已不是主流卡组")
                    continue
                for card in j.get("depends_on", []):
                    # core lists only keep cards in at least 25% of lists; call a missing one 12.5%
                    a, b = old.get(card, CORE_FLOOR / 2), new.get(card, CORE_FLOOR / 2)
                    if abs(a - b) >= USAGE_SHIFT:
                        pa, pb = (f"{x:.0%}" if card in d else "<25%" for x, d in ((a, old), (b, new)))
                        why.append(f"{slug} 的卡表带 {card} 的比例 {pa} → {pb}")
        if why:
            out.append(f"{jid}（{window}）：{j['text']} —— " + "；".join(why))
    return out


def calibration(judgments: dict[str, dict], sources: list[dict]) -> list[str]:
    """Game results only (logs, videos), each scored against the confidence the judgment had
    just before that game."""
    buckets: dict[int, list[int]] = {}
    brier = []
    for jid, j in judgments.items():
        rows = history(jid, j, sources)
        for i, (s, _, _, ok) in enumerate(rows):
            if s["kind"] == "feedback":
                continue
            p = confidence(j, rows[:i])
            buckets.setdefault(min(int(p * 10), 9), []).append(ok)
            brier.append((p - ok) ** 2)
    lines = ["| 当时的信心 | 局数 | 实际成立 |", "|---|---|---|"]
    for b in sorted(buckets):
        r = buckets[b]
        lines.append(f"| {b * 10}–{b * 10 + 9}% | {len(r)} | {sum(r) / len(r):.0%} |")
    if brier:
        lines.append(f"\nBrier 分数 {sum(brier) / len(brier):.3f}（{len(brier)} 次判定；越低越好，"
                     "全部写 50% 是 0.25）")
    else:
        lines.append("\n还没有对局结果。")
    return lines


def pending(judgments: dict[str, dict], sources: list[dict], deck: str | None, vs: str | None) -> list[str]:
    now = current(judgments, sources)
    lines = []
    for jid, j in sorted(judgments.items()):
        if (deck and deck not in (j["deck"], j.get("vs"))) or (vs and vs not in (j["deck"], j.get("vs"))):
            continue
        n = sum(1 for s, *_ in history(jid, j, sources) if s["kind"] != "feedback")
        lines.append(f"判断 {jid}（{shown(now[jid])}%，{n} 局）：{j['text']}")
    for s in sources:
        for c in s.get("claims", []):
            if c.get("status") != "待验证":
                continue
            if (deck and deck not in (c.get("deck"), c.get("vs"))) or (vs and vs not in (c.get("deck"), c.get("vs"))):
                continue
            lines.append(f"待验证 {c['id']}（{c['type']}，{s['_file']}）：{c['text']}"
                         + (f"；要找：{c['check']}" if c.get("check") else ""))
    return lines


def _latest_window() -> str:
    from .archetypes import latest_window
    return latest_window()


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    cmd = argv[0] if argv else "check"
    js, ss = load_judgments(), load_sources()
    if cmd == "check":
        errors, warnings = check(js, ss)
        for w in warnings:
            print(f"warning: {w}")
        for e in errors:
            print(f"ERROR: {e}")
        print(f"judgments: {len(js)} judgments, {len(ss)} sources, {len(errors)} errors")
        return 1 if errors else 0
    if cmd == "sync":
        for p in sync(js, ss):
            print(f"updated {p}")
        return 0
    if cmd == "stale":
        out = stale(js, ss, _latest_window())
        print("\n".join(f"- {x}" for x in out) or "no stale judgments")
        return 1 if out else 0
    if cmd == "calibration":
        print("\n".join(calibration(js, ss)))
        return 0
    if cmd == "pending":
        print("\n".join(pending(js, ss, *(argv[1:3] + [None, None])[:2])) or "nothing pending")
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
