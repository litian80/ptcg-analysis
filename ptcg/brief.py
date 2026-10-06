"""Pre-tournament brief: which deck to bring, how to tune the list, and what to do in each matchup.

    python -m ptcg.brief            # the latest window with selection numbers
    python -m ptcg.brief TEF-30C

Writes data/brief/<window>.md (the one-page overview) and data/brief/<window>/<deck>.md (one cheat
sheet per recommended deck). Everything numeric comes from data/selection/selection_<window>.json
and data/matchups/tech_<window>.json, so the brief follows the weekly data update. The hand-written
parts are data/brief/picks.yaml (tiers and who each deck suits) and data/brief/points/<deck>.yaml
(3-5 points per matchup, condensed from the playbooks in data/matchups/). A point that restates a
playbook judgment carries its id; the brief shows that judgment's current confidence.
"""
from __future__ import annotations

import json
import sys

import yaml

from . import judgments as jm
from .paths import DATA

BRIEF = DATA / "brief"
POINTS = BRIEF / "points"
FIELD_ROWS = 12      # opponents listed in the field table and cheat sheets
MIN_SIDE = 10        # tech: games needed on both the with and without side of a matchup
MIN_COVER = 0.25     # tech: the card must have data against this much of the day 2 field
MIN_DELTA = 0.04     # tech: weighted win-rate difference worth mentioning
PAIR_SIDE = 15       # per-matchup tech: games needed on both sides
PAIR_DELTA = 0.10    # per-matchup tech: difference worth a line in that matchup
TOP_N = 3            # a tier is backed while the deck ranks this high by expected day 2 win rate
MIN_GAMES = 300      # ...among decks with at least this many games


def pct(x: float) -> str:
    return f"{100 * x:.1f}%"


def latest_window() -> str | None:
    """The selection file whose field comes from the most recent events."""
    best = None
    for p in (DATA / "selection").glob("selection_*.json"):
        d = json.loads(p.read_text(encoding="utf-8"))
        date = max((e["date"] for e in d["events"] if e["window"] == d["field_window"]), default="")
        if best is None or date > best[0]:
            best = (date, d["field_window"])
    return best and best[1]


def load(window: str | None = None):
    picks = yaml.safe_load((BRIEF / "picks.yaml").read_text(encoding="utf-8"))
    if window is None:
        window = latest_window() or picks["window"]
    sel = json.loads((DATA / "selection" / f"selection_{window}.json").read_text(encoding="utf-8"))
    tech = json.loads((DATA / "matchups" / f"tech_{window}.json").read_text(encoding="utf-8"))
    points = {}
    for p in sorted(POINTS.glob("*.yaml")):
        d = yaml.safe_load(p.read_text(encoding="utf-8"))
        points[d["deck"]] = d
    return window, picks, sel, tech, points


def field(sel: dict) -> list[tuple[str, dict]]:
    """Opponents by share of day 2, the field a player aiming for the top has to beat."""
    arch = sel["archetypes"]
    return sorted(arch.items(), key=lambda kv: -kv[1]["day2_share"])[:FIELD_ROWS]


def name(sel: dict, slug: str) -> str:
    a = sel["archetypes"].get(slug)
    return a["name"] if a else slug


def matchup(sel: dict, deck: str, vs: str) -> dict | None:
    for m in sel["archetypes"].get(deck, {}).get("matchups", []):
        if m["vs"] == vs:
            return m
    return None


def tech(sel: dict, tech_json: dict, deck: str) -> list[dict]:
    """Cards whose presence in the deck's lists goes with a better or worse record against the
    day 2 field. Per matchup, the with/without difference counts when both sides have MIN_SIDE
    games; matchups are weighted by the opponent's day 2 share. Correlation, not proof."""
    arch = sel["archetypes"]
    cards: dict[str, dict] = {}
    for vs, pair in tech_json["pairs"].get(deck, {}).items():
        share = arch.get(vs, {}).get("day2_share", 0)
        if not share:
            continue
        for c in pair["cards"]:
            if c["with_games"] < MIN_SIDE or c["without_games"] < MIN_SIDE:
                continue
            e = cards.setdefault(c["card"], {"card": c["card"], "w": 0.0, "sum": 0.0, "in_lists": [],
                                             "rows": []})
            e["w"] += share
            e["sum"] += share * c["delta"]
            e["in_lists"].append(c["in_lists"])
            e["rows"].append((c["delta"], vs, c))
    total = sum(a["day2_share"] for a in arch.values())
    out = []
    for e in cards.values():
        cover = e["w"] / total
        delta = e["sum"] / e["w"]
        if cover < MIN_COVER or abs(delta) < MIN_DELTA:
            continue
        # the matchup that pulls hardest in the overall direction, so the example agrees with the verdict
        biggest = max(e["rows"], key=lambda r: r[0] if delta > 0 else -r[0])
        out.append({"card": e["card"], "delta": delta, "cover": cover,
                    "in_lists": sum(e["in_lists"]) / len(e["in_lists"]), "biggest": biggest})
    return sorted(out, key=lambda e: -e["delta"])


def pair_tech(tech_json: dict, deck: str, vs: str) -> list[str]:
    """At most two cards whose with/without difference in this one matchup is large."""
    pair = tech_json["pairs"].get(deck, {}).get(vs)
    if not pair:
        return []
    rows = [c for c in pair["cards"] if c["with_games"] >= PAIR_SIDE and c["without_games"] >= PAIR_SIDE
            and abs(c["delta"]) >= PAIR_DELTA]
    rows.sort(key=lambda c: -abs(c["delta"]))
    seen, out = set(), []
    for c in rows:  # cards that always travel together split the games the same way: show one
        split = frozenset((c["with_games"], c["without_games"]))
        if split not in seen:
            seen.add(split)
            out.append(c)
    return [f"- 卡表：带 {c['card']} {pct(c['with'])}（{c['with_games']} 局）对不带 {pct(c['without'])}"
            f"（{c['without_games']} 局）" for c in out[:2]]


def backed(sel: dict, deck: str) -> int | None:
    """The deck's rank by expected day 2 win rate among decks with MIN_GAMES games."""
    ranked = sorted((a for a in sel["archetypes"].items() if a[1]["record"]["wins"] + a[1]["record"]["losses"]
                     + a[1]["record"]["ties"] >= MIN_GAMES), key=lambda kv: -kv[1]["expected_vs_day2"])
    for i, (slug, _) in enumerate(ranked, 1):
        if slug == deck:
            return i
    return None


def games(a: dict) -> int:
    r = a["record"]
    return r["wins"] + r["losses"] + r["ties"]


def tech_lines(sel: dict, rows: list[dict]) -> list[str]:
    lines = []
    for e in rows:
        d, vs, c = e["biggest"]
        verb = "带上或多带" if e["delta"] > 0 else "考虑少带或不带"
        lines.append(
            f"- **{e['card']}**（{pct(e['in_lists'])} 的卡表带）：{verb}，对 Day 2 环境加权胜率差 "
            f"{100 * e['delta']:+.1f} 个百分点；差得最多的是对 {name(sel, vs)}，带 {pct(c['with'])}"
            f"（{c['with_games']} 局）对不带 {pct(c['without'])}（{c['without_games']} 局）")
    return lines


def overview(window, picks, sel, tech_json, points) -> str:
    arch = sel["archetypes"]
    ev = "、".join(f"{e['name'].replace('Regional ', '')}（{e['date']}）" for e in sel["events"]
                  if e["window"] == window)
    L = [f"# 赛前简报（{window}）", "",
         f"环境取自 {ev}，共 {sel['players']} 人、{sel['day2_players']} 人进 Day 2；对位胜率合并了"
         f" {'、'.join(sel['matchup_windows'])} 两个窗口。胜率里平局算 1/3 胜，全场平均 {pct(sel['baseline'])}，"
         "高于它就是赢面。数字随每周一的数据更新自动重算；推荐分档是人工判断，"
         f"定于 {picks['decided']}。", ""]

    L += ["## 1. 会遇到谁", "",
          "按 Day 2 份额排（想进前排一定会遇到的环境）。这是上一场的环境，不是对下一场的预测。", "",
          "| 卡组 | Day 2 份额 | 全场份额 | 上个窗口 | 走势 |", "|---|---|---|---|---|"]
    for slug, a in field(sel):
        trend = "↑" if a["share"] - a["prev_share"] > 0.005 else "↓" if a["prev_share"] - a["share"] > 0.005 else "→"
        L.append(f"| {a['name']} | {pct(a['day2_share'])} | {pct(a['share'])} | {pct(a['prev_share'])} | {trend} |")
    L += [""] + [f"- {n}" for n in picks.get("field_notes", [])] + [""]

    L += ["## 2. 带哪套", "",
          "| 档 | 卡组 | 对 Day 2 期望胜率 | 胜率（局数） | 理由 | 适合谁 |", "|---|---|---|---|---|---|"]
    warn = []
    if picks["window"] != window:
        warn.append(f"推荐分档是按 {picks['window']} 定的，这里的数字已经是 {window}")
    for p in picks["picks"]:
        a = arch[p["deck"]]
        L.append(f"| {p['tier']} | [{a['name']}]({window}/{p['deck']}.md) | {pct(a['expected_vs_day2'])} | "
                 f"{pct(a['record']['win_rate'])}（{games(a)}） | {p['why']} | {p['who']} |")
        rank = backed(sel, p["deck"])
        if p["tier"] in ("首选", "高上限") and (rank is None or rank > TOP_N):
            warn.append(f"{a['name']} 标为{p['tier']}，但现在按对 Day 2 期望胜率只排第 {rank or '—'}（局数 ≥ {MIN_GAMES} 的卡组里）")
    L += ["", "**避开**：" + "；".join(f"{name(sel, x['deck'])}（{x['why']}）" for x in picks.get("avoid", [])), ""]
    if warn:
        L += ["> 注意：最新数字和推荐分档不一致，`data/brief/picks.yaml` 需要重新看：", ">"]
        L += [f"> - {w}" for w in warn]
        L.append("")
    L += ["点卡组名看它的对局速查。", ""]

    L += ["## 3. 卡表怎么微调", "",
          "公开卡表里带和不带某张卡的胜率差，按对手的 Day 2 份额加权。只有成绩靠前的选手公开卡表，"
          "这是相关，不是证明：差值可能来自同一组一起出现的卡或选手水平。各卡组的速查页里有完整列表。", ""]
    for p in picks["picks"]:
        rows = tech(sel, tech_json, p["deck"])
        if not rows:
            L += [f"**{name(sel, p['deck'])}**：没有哪张卡的差值够明显（样本或差值太小），按常见卡表带。", ""]
            continue
        top = [r for r in rows if r["delta"] > 0][:2] + [r for r in rows if r["delta"] < 0][-2:]
        L += [f"**{name(sel, p['deck'])}**", ""] + tech_lines(sel, top) + [""]
    return "\n".join(L).rstrip() + "\n"


def sheet(window, picks, sel, tech_json, points, pick, conf) -> str:
    deck = pick["deck"]
    a = sel["archetypes"][deck]
    pts = points.get(deck, {})
    L = [f"# {a['name']} 对局速查（{window}）", "",
         f"{pick['tier']}：{pick['why']}。适合：{pick['who']}。", "",
         f"份额 {pct(a['share'])}，Day 2 份额 {pct(a['day2_share'])}；胜率 {pct(a['record']['win_rate'])}"
         f"（{games(a)} 局），对 Day 2 环境期望 {pct(a['expected_vs_day2'])}（平均 {pct(sel['day2_baseline'])}）。"
         f"完整打法和录像出处见长版手册 {deck}.md（matchups 目录）。要点后的（推断）表示没有卡牌文字或数据直接支撑，"
         "（信心 xx%）是这条判断经录像、对局记录和反馈修正后的当前信心。", ""]

    def line(pt):
        s = pt["text"]
        if pt.get("inferred"):
            s += "（推断）"
        if pt.get("judgment") in conf:
            s += f"（信心 {jm.shown(conf[pt['judgment']])}%）"
        return f"- {s}"

    if pts.get("general"):
        L += ["## 通用", ""] + [line(p) for p in pts["general"]] + [""]

    mus = pts.get("matchups", {})
    L += ["## 对手（按 Day 2 份额）", ""]
    order = [s for s, _ in field(sel)] + [s for s in mus if s not in dict(field(sel))]
    for vs in order:
        if vs not in mus and vs != deck:
            if vs in dict(field(sel)):
                m = matchup(sel, deck, vs)
                wr = f"（胜率 {pct(m['win_rate'])}，{m['games']} 局）" if m else ""
                L += [f"### {name(sel, vs)}{wr}", "", "- 手册里还没有这个对局。", ""]
            continue
        if vs not in mus:
            continue
        o = sel["archetypes"].get(vs)
        if vs == deck:
            head = f"### {name(sel, vs)}（镜像）"
        else:
            m = matchup(sel, deck, vs)
            share = f"Day 2 份额 {pct(o['day2_share'])}，" if o else ""
            wr = f"胜率 {pct(m['win_rate'])}，{m['games']} 局" if m else "没有对局数据"
            head = f"### {name(sel, vs)}（{share}{wr}）"
        L += [head, ""] + [line(p) for p in mus[vs]] + pair_tech(tech_json, deck, vs) + [""]

    rows = tech(sel, tech_json, deck)
    L += ["## 卡表微调", "",
          "带和不带的胜率差，按对手 Day 2 份额加权；相关不是证明，见简报首页说明。", ""]
    L += (tech_lines(sel, rows) or ["- 没有哪张卡的差值够明显（样本或差值太小），按常见卡表带。"]) + [""]
    return "\n".join(L).rstrip() + "\n"


def check(points: dict, sel: dict, judgments: dict) -> list[str]:
    errors = []
    for deck, d in points.items():
        if deck not in sel["archetypes"]:
            errors.append(f"points/{deck}.yaml: unknown deck")
        for p in d.get("general", []):
            if not p.get("text"):
                errors.append(f"points/{deck}.yaml: general point without text")
        for vs, pts in d.get("matchups", {}).items():
            if vs not in sel["archetypes"]:
                errors.append(f"points/{deck}.yaml: unknown opponent {vs}")
            for p in pts:
                if not p.get("text"):
                    errors.append(f"points/{deck}.yaml {vs}: point without text")
                j = p.get("judgment")
                if j and j not in judgments:
                    errors.append(f"points/{deck}.yaml {vs}: unknown judgment {j}")
    return errors


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    window, picks, sel, tech_json, points = load(argv[0] if argv else None)
    judgments = jm.load_judgments()
    errors = check(points, sel, judgments)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    conf = jm.current(judgments, jm.load_sources())
    (BRIEF / f"{window}.md").write_text(overview(window, picks, sel, tech_json, points), encoding="utf-8")
    out = BRIEF / window
    out.mkdir(exist_ok=True)
    for p in picks["picks"]:
        (out / f"{p['deck']}.md").write_text(sheet(window, picks, sel, tech_json, points, p, conf), encoding="utf-8")
    print(f"wrote data/brief/{window}.md and {len(picks['picks'])} cheat sheets")
    return 0


if __name__ == "__main__":
    sys.exit(main())
