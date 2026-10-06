"""Basic Box (Mega Kangaskhan ex): Niklaus Christen, Regional Frankfurt 2026-09-26, 37th
(best Basic Box list there).

Modelled (printed text): Teal Mask Ogerpon ex Teal Dance (TWM 25), Latias ex Skyliner
(SSP 76), Mega Kangaskhan ex Run Errand (MEG 104), Meowth ex Last-Ditch Catch (POR 62),
Crispin (SCR 133), Cyrano (SSP 170), Lillie's Determination (MEG 119), Energy Switch (MEG 115),
Glass Trumpet (SCR 135), Ultra Ball (MEG 131), Area Zero Underdepths (SCR 131).
The policy powers up one chosen attacker (Latias ex or Mega Kangaskhan ex) as fast as it can.
"""
from __future__ import annotations

from .core import Deck, Game, Mon, can_pay, card

LIST = {
    "Mega Kangaskhan ex": 4, "Meowth ex": 3, "Teal Mask Ogerpon ex": 2, "Latias ex": 2,
    "Lillie's Clefairy ex": 2, "Fezandipiti ex": 1, "Chien-Pao": 1, "Raging Bolt ex": 1,
    "Iron Leaves ex": 1, "Maractus": 1, "Wellspring Mask Ogerpon ex": 1,
    "Crispin": 4, "Boss's Orders": 2, "Cyrano": 2, "Ciphermaniac's Codebreaking": 1,
    "Xerosic's Machinations": 1, "Lillie's Determination": 1,
    "Energy Switch": 4, "Ultra Ball": 4, "Night Stretcher": 2, "Glass Trumpet": 2, "Unfair Stamp": 1,
    "Area Zero Underdepths": 4,
    "Grass Energy": 6, "Psychic Energy": 2, "Lightning Energy": 2, "Fighting Energy": 2, "Water Energy": 1,
}
COST = {"Latias ex": "PPC", "Mega Kangaskhan ex": "CCC", "Iron Leaves ex": "GGC",
        "Raging Bolt ex": "LF", "Teal Mask Ogerpon ex": "GGG", "Wellspring Mask Ogerpon ex": "WCC"}
BASIC_E = ("Grass Energy", "Psychic Energy", "Lightning Energy", "Fighting Energy", "Water Energy")
SYM = {"G": "Grass Energy", "P": "Psychic Energy", "L": "Lightning Energy", "F": "Fighting Energy", "W": "Water Energy"}
JUNK = ["Boss's Orders", "Unfair Stamp", "Xerosic's Machinations", "Ciphermaniac's Codebreaking",
        "Night Stretcher", "Maractus", "Chien-Pao", "Lillie's Clefairy ex", "Fezandipiti ex",
        "Wellspring Mask Ogerpon ex", "Raging Bolt ex", "Water Energy", "Fighting Energy", "Lightning Energy",
        "Iron Leaves ex", "Mega Kangaskhan ex", "Meowth ex", "Area Zero Underdepths", "Glass Trumpet"]


def short(energies: list[str], cost: str) -> list[str]:
    """Symbols of `cost` not yet covered (specific first, then C)."""
    have = [card(e).provides for e in energies]
    out = []
    for sym in sorted(cost, key=lambda s: s == "C"):
        if sym == "C":
            if have:
                have.pop()
            else:
                out.append("C")
        elif sym in have:
            have.remove(sym)
        else:
            out.append(sym)
    return out


class BasicBox(Deck):
    SLUG = "basic-box-m"
    NAME = "Basic Box"
    SOURCE = "Frankfurt 区域赛 2026-09-26 第 37 名 Niklaus Christen"
    LIST = LIST
    TURNS = 3
    BLANKS = ["Lillie's Clefairy ex", "Fezandipiti ex", "Chien-Pao", "Maractus", "Wellspring Mask Ogerpon ex（只算攻击费用）",
              "Raging Bolt ex / Iron Leaves ex（只算攻击费用，不用 Rapid Vernier）",
              "Boss's Orders", "Ciphermaniac's Codebreaking", "Xerosic's Machinations", "Night Stretcher", "Unfair Stamp"]
    NOTES = [
        "打法只给一个选定的主攻手充能（plan=Latias ex 或 Mega Kangaskhan ex），两种打法各跑一遍；其余指标取 Latias 打法。",
        "能量来源：手贴、Teal Dance（只能贴草给 Ogerpon 自己，抽 1）、Crispin（一个贴主攻手、一个进手）、Energy Switch（基本能量挪给主攻手）、Glass Trumpet（弃牌区基本能量给后备区无色宝可梦，弃牌区的能量来自 Ultra Ball）。",
        "Latias ex 在场时基础宝可梦撤退 0，换位免费；否则按撤退费。",
    ]

    def __init__(self, plan: str = "Latias ex", **opts):
        super().__init__(**opts)
        self.plan = plan
        self.cost = COST[plan]

    ACTIVE_PREF = ("Latias ex", "Maractus", "Teal Mask Ogerpon ex", "Fezandipiti ex", "Wellspring Mask Ogerpon ex",
                   "Raging Bolt ex", "Chien-Pao", "Lillie's Clefairy ex", "Iron Leaves ex", "Meowth ex",
                   "Mega Kangaskhan ex")

    def choose_active(self, g: Game) -> str:
        if self.plan in g.hand and self.plan != "Mega Kangaskhan ex":
            return self.plan
        return super().choose_active(g)

    def initial_bench(self, g: Game) -> None:
        for c in list(g.hand):
            if c in ("Teal Mask Ogerpon ex", "Latias ex", self.plan) and g.count(c) < (2 if c == "Teal Mask Ogerpon ex" else 1):
                g.bench_from_hand(c)

    # ---- helpers -------------------------------------------------------
    def target(self, g: Game) -> Mon | None:
        ms = g.mons(self.plan)
        if not ms:
            return None
        return max(ms, key=lambda m: (len(m.energy), m is g.active))

    def need(self, g: Game) -> list[str]:
        t = self.target(g)
        return short(t.energy, self.cost) if t else list(self.cost)

    def fits(self, e: str, g: Game) -> bool:
        need = self.need(g)
        return card(e).provides in need or ("C" in need)

    # ---- policy --------------------------------------------------------
    def step(self, g: Game) -> bool:
        h = g.hand
        room = g.bench_room()
        # Run Errand
        a = g.active
        if a.name == "Mega Kangaskhan ex" and not a.used:
            a.used = True
            g.draw(2)
            return True
        # bench the plan, Ogerpon and Latias (Skyliner)
        for c, cap in ((self.plan, 1), ("Teal Mask Ogerpon ex", 2), ("Latias ex", 1)):
            if c in h and g.count(c) < cap and room > 0:
                return bool(g.bench_from_hand(c))
        if "Area Zero Underdepths" in h and g.stadium != "Area Zero Underdepths" and \
                any(card(m.name).tera for m in g.board):
            return g.play_stadium("Area Zero Underdepths")
        # find the plan / Ogerpon
        missing = [c for c in (self.plan, "Teal Mask Ogerpon ex") if not g.count(c) and c not in h]
        if missing and "Ultra Ball" in h and room > 0:
            keep = {self.plan, "Teal Mask Ogerpon ex", "Energy Switch", "Crispin"} | \
                {e for e in BASIC_E if self.fits(e, g)}
            for w in missing:
                if g.ultra_ball(w, JUNK, keep):
                    return True
        # Teal Dance
        for m in g.mons("Teal Mask Ogerpon ex"):
            if not m.used and "Grass Energy" in h:
                m.used = True
                h.remove("Grass Energy")
                m.energy.append("Grass Energy")
                g.draw(1)
                return True
        t = self.target(g)
        need = self.need(g)
        if t and need:
            # manual attachment
            if not g.attached:
                for sym in need:
                    pref = [SYM[sym]] if sym != "C" else [e for e in ("Lightning Energy", "Fighting Energy", "Water Energy",
                                                                       "Psychic Energy", "Grass Energy") if e in h]
                    for e in pref:
                        if e in h:
                            return g.attach(t, e)
            # Energy Switch from another Pokemon
            if "Energy Switch" in h:
                for m in g.board:
                    if m is t:
                        continue
                    for e in m.energy:
                        if card(e).kind == "energy" and e in BASIC_E and (card(e).provides in need or "C" in need):
                            g.play("Energy Switch")
                            m.energy.remove(e)
                            t.energy.append(e)
                            return True
            # Glass Trumpet: Kangaskhan on the Bench
            if "Glass Trumpet" in h and t is not g.active and card(t.name).type == "C" and \
                    any(card(m.name).tera for m in g.board) and any(e in BASIC_E for e in g.discard):
                g.play("Glass Trumpet")
                e = next(e for e in BASIC_E if e in g.discard)
                g.discard.remove(e)
                t.energy.append(e)
                return True
        if g.can_supporter():
            return self.supporter(g, t, need, missing)
        return False

    def supporter(self, g: Game, t: Mon | None, need: list[str], missing: list[str]) -> bool:
        h = g.hand
        room = g.bench_room()
        useful = ("Cyrano" in h and missing) or ("Crispin" in h and t and need) or "Lillie's Determination" in h
        if not useful and "Meowth ex" in h and room > 0:
            g.bench_from_hand("Meowth ex")
            choice = "Cyrano" if missing else "Crispin"
            g.search(choice) or g.search("Crispin") or g.search("Lillie's Determination")
            g.shuffle()
            return True
        if "Cyrano" in h and missing:
            g.play_supporter("Cyrano")
            for c in missing + ["Latias ex", "Teal Mask Ogerpon ex"]:
                if c not in h:
                    g.search(c)
            g.shuffle()
            return True
        if "Crispin" in h and t and need:
            g.play_supporter("Crispin")
            got = []
            order = [SYM[s] for s in need if s != "C"] + ["Lightning Energy", "Fighting Energy", "Psychic Energy",
                                                           "Water Energy", "Grass Energy"]
            for e in order:
                if e not in got and e in g.deck and len(got) < 2:
                    got.append(e)
            for e in got:
                g.deck.remove(e)
            if got:
                # attach the one the target needs; Grass goes to hand for Teal Dance
                got.sort(key=lambda e: (not (card(e).provides in need), e == "Grass Energy"))
                t.energy.append(got[0])
                g.hand += got[1:]
            g.shuffle()
            return True
        if "Lillie's Determination" in h and (missing or need):
            return g.lillies()
        return False

    def end_turn(self, g: Game) -> None:
        t = self.target(g)
        g.flags["plan_ready"] = bool(t) and g.go(t, self.cost)
        # Iron Leaves ex from hand: Rapid Vernier switches it in and moves any Energy onto it
        g.flags["leaves"] = g.can_attack() and "Iron Leaves ex" in g.hand and g.bench_room() > 0 and \
            can_pay([e for m in g.board for e in m.energy], COST["Iron Leaves ex"])
        g.flags["any_ready"] = g.flags["plan_ready"] or g.flags["leaves"] or any(
            g.can_attack() and can_pay(m.energy, COST[m.name]) and g.can_pivot(m)
            for m in g.board if m.name in COST)

    def measure(self, g: Game, t: int) -> dict:
        p = self.plan
        out = {f"[{p}打法] 第{t}回合 {p} 能攻击": g.flags["plan_ready"]}
        if self.plan != "Latias ex":
            return out
        out[f"第{t}回合任一主攻手能攻击"] = g.flags["any_ready"]
        out[f"第{t}回合 Iron Leaves ex 能从手上放下攻击"] = g.flags["leaves"]
        if t <= 2:
            out[f"第{t}回合 Area Zero 在场（后备区 8 格）"] = g.bench_max() == 8
        if t == 1:
            psy = sum(1 for c in g.prizes if c == "Psychic Energy")
            usable = sum(1 for c in g.deck + g.hand if c == "Psychic Energy") + sum(
                m.energy.count("Psychic Energy") for m in g.board)
            out["Psychic Energy 至少 1 张在奖赏卡"] = psy >= 1
            out["奖赏卡外的 Psychic Energy 不到 2 张（拿奖前 Latias 打不出 Eon Blade）"] = usable < 2
            others = [c for c in g.opening if card(c).kind == "pokemon" and c != "Mega Kangaskhan ex"]
            out["起手只能放 Mega Kangaskhan ex 到战斗场"] = not others
        return out

    def tunings(self) -> list[dict]:
        return [
            {"question": "第 2 张 Iron Leaves ex（减 1 张 Night Stretcher）",
             "source": "data/matchups/basic-box-m.md:115、data/brief/TEF-30C.md（Iron Leaves +4.7）",
             "change": {"Iron Leaves ex": +1, "Night Stretcher": -1}},
            {"question": "Psychic Energy 2 → 3（减 1 张 Glass Trumpet）",
             "source": "data/matchups/basic-box-m.md:28（手册写的是 3 张）",
             "change": {"Psychic Energy": +1, "Glass Trumpet": -1}},
        ]
