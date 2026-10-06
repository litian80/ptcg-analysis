"""The championship plan for the next major: who will be at the top, which deck, which list, which lines.

    python -m ptcg.plan                    # next event, all regions
    python -m ptcg.plan --region EU        # weight events from that region (EU, NA, LA, OC)

Writes data/plan/<date>[_<region>].md. Built from ptcg.forecast (field, deck scores, backtests),
ptcg.tuning (card counts, day 2 players only) and the hand-written matchup points in
data/brief/points and card notes in data/plan/notes.yaml.
"""
from __future__ import annotations

import collections
import sys

import yaml

from . import forecast as fc
from . import tuning
from .paths import DATA

OUT = DATA / "plan"
POINTS = DATA / "brief" / "points"
PICKS = 3
TOP_OPPONENTS = 6
MIN_LISTS = 40      # a deck needs this many day 2 lists before card suggestions are given
SMALL = 60          # fewer players than this in the latest two card pools: the numbers are thin


def pct(x: float) -> str:
    return f"{100 * x:.1f}%"


def names() -> dict[str, str]:
    out = {}
    for e in fc.events():
        for s in e["standings"]:
            out.setdefault(s["archetype_slug"], s["archetype"])
    return out


def recent_players(pools: list[str]) -> collections.Counter:
    return collections.Counter(s["archetype_slug"] for e in fc.events() if e["format_code"] in pools
                               for s in e["standings"])


def write(region: str | None = None) -> str:
    nm = names()
    n = lambda s: nm.get(s, s)
    nx = fc.next_event(region)
    field, decks = nx["field"], nx["decks"]
    pools = list(dict.fromkeys(e["format_code"] for e in reversed(fc.events())))[:2]
    seen = recent_players(pools)
    top32 = fc.normalize({a: d["field"] * d["conversion"] for a, d in decks.items()})
    order = sorted(decks, key=lambda a: -decks[a]["score"])
    picks = order[:PICKS]
    bp = fc.backtest_picks()
    notes = yaml.safe_load((OUT / "notes.yaml").read_text(encoding="utf-8")) or {}
    points = {p.stem: yaml.safe_load(p.read_text(encoding="utf-8")) for p in POINTS.glob("*.yaml")}
    evs = [e for e in fc.events() if e["format_code"] == pools[0]]

    L = [f"# 夺冠方案（{nx['day']} 前后的大赛{('，' + region + ' 地区') if region else ''}）", "",
         f"数据截至 {max(e['date'] for e in fc.events())}，卡池 {pools[0]}（{'、'.join(e['name'] for e in evs)}）。"
         "目标是进前 8 和夺冠，不是平均胜率。", ""]

    a, b = bp["after"]["model_top8"], bp["after"]["popular_top8"]
    L += ["## 结论", "",
          f"- 首选 **{n(picks[0])}**，备选 {'、'.join(n(p) for p in picks[1:])}。理由见第 2 节。"
          + ("" if all(seen[p] >= SMALL for p in picks) else
             f"其中 {'、'.join(n(p) for p in picks if seen[p] < SMALL)} 近期人数少，得分主要来自少数选手的好成绩，"
             f"样本最大的推荐是 {n(max(picks, key=lambda p: seen[p]))}。"),
          f"- 选卡组能给的优势有限：轮换后 {bp['after']['events']} 场大赛回测，按本方案选的卡组进前 8 的人数是"
          f"平均卡组的 {a['lift']} 倍，直接选最热门的卡组是 {b['lift']} 倍。夺冠主要还得靠打法和卡表。",
          "- 单卡调整和对局要点见第 3、4 节；只有样本够的卡组才给单卡建议。", ""]

    L += ["## 1. 前排会遇到谁", "",
          "预计份额 = 各卡组近期份额（按时间、地区加权，加上最近前 8 带来的跟风）；"
          "预计前 32 份额 = 预计份额 × 该卡组过去进前 32 的比例。单场前 32 的构成波动很大，只看大致排序。", "",
          "| 卡组 | 预计全场份额 | 预计前 32 份额 |", "|---|---|---|"]
    for s in sorted(top32, key=lambda k: -top32[k])[:10]:
        L.append(f"| {n(s)} | {pct(field.get(s, 0))} | {pct(top32[s])} |")
    L.append("")

    L += ["## 2. 带哪套", "",
          "得分 = 进前 32 的历史比例（权重 3/4）+ 对预计环境的期望胜率（权重 1/4），都换成标准分。"
          "进前 32 的比例同时反映卡组和选它的选手水平。", "",
          "| 卡组 | 得分 | 进前 32 比例（平均 = 1） | 对预计环境期望胜率 | 近两个卡池人数 |", "|---|---|---|---|---|"]
    for s in order[:8]:
        d = decks[s]
        small = "（样本小）" if seen[s] < SMALL else ""
        L.append(f"| {n(s)} | {d['score']:+.2f} | {d['conversion']:.2f} | {pct(d['expected'])} | {seen[s]}{small} |")
    L.append("")

    L += ["## 3. 单卡调整", "",
          "只比较进了 Day 2 的选手（他们的卡表全部公开，水平相近），只算 Day 2 的对局，"
          "按预计环境给各对手加权。q 值是多重比较校正后的错报概率，q < 0.2 才算建议。", ""]
    for s in picks:
        r = tuning.analyse(s, pools, field)
        sug = [t for t in r["tests"] if t["q"] < tuning.Q_SUGGEST] if r["lists"] >= MIN_LISTS else []
        L += [f"### {n(s)}（{r['lists']} 份 Day 2 卡表，{r['games']} 局）", ""]
        if not sug:
            leads = [t for t in r["tests"] if t["q"] < 0.6][:3]
            L.append("- 样本不够给出建议，按常见卡表带。" + (
                "值得留意：" + "；".join(f"{t['card']} {t['from']} → {t['to']} 张"
                                         f"（{pct(t['win_from'])} 对 {pct(t['win_to'])}）" for t in leads) if leads else ""))
        for t in sug:
            pk = f"（和 {'、'.join(t['package'])} 一起）" if t["package"] else ""
            dr = "、".join(f"{n(d['vs'])}" for d in t["drivers"])
            note = notes.get(s, {}).get(t["card"]) or "原因还没核实。"
            verdict = (f"改成 {t['to']} 张" if t["win_to"] > t["win_from"]
                       else f"保持 {t['from']} 张，别改成 {t['to']} 张")
            L.append(f"- **{t['card']}{pk}：{verdict}**。常见带法 {t['from']} 张胜率 {pct(t['win_from'])}"
                     f"（{t['games_from']} 局），{t['to']} 张 {pct(t['win_to'])}（{t['games_to']} 局），q = {t['q']}。"
                     + (f"差距主要来自对 {dr}。" if dr else "") + note)
        L.append("")

    L += ["## 4. 对前排卡组的要点", "",
          "按预计前 32 份额排，取自对局速查（data/brief）。没有速查的卡组还没写手册。", ""]
    opp = [s for s in sorted(top32, key=lambda k: -top32[k])][:TOP_OPPONENTS]
    for s in picks:
        pts = points.get(s)
        L += [f"### {n(s)}", ""]
        if not pts:
            L += ["- 这套还没有对局手册，需要的话下一步补。", ""]
            continue
        for o in opp:
            lines = pts.get("matchups", {}).get(o)
            if lines:
                L.append(f"**对 {n(o)}**" + ("（镜像）" if o == s else ""))
                L += [f"- {p['text']}" + ("（推断）" if p.get("inferred") else "") for p in lines[:3]]
                L.append("")
    return "\n".join(L).rstrip() + "\n"


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    region = argv[argv.index("--region") + 1] if "--region" in argv else None
    text = write(region)
    day = fc.next_event(region)["day"]
    OUT.mkdir(exist_ok=True)
    path = OUT / f"{day}{'_' + region if region else ''}.md"
    path.write_text(text, encoding="utf-8")
    print(f"wrote {path.relative_to(DATA.parent)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
