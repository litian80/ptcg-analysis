"""Crustle (DRI 12): Eemeli Reijonen, Regional Frankfurt 2026-09-26, 19th (best Crustle list there).

Modelled (printed text): Dwebble Ascension (DRI 11, attack: evolve from the deck), Crustle
(DRI 12, Superb Scissors G+C+C), Mega Kangaskhan ex Run Errand (MEG 104), Buddy-Buddy Poffin
(TEF 144), Ultra Ball (MEG 131), Team Rocket's Petrel (DRI 176), Team Rocket's Factory (DRI 173),
Hilda (WHT 84), Lillie's Determination (MEG 119), Pokégear 3.0 (SVI 186), Switch (MEG 130),
Lumiose City (POR 77, ends the turn), Growing Grass Energy (POR 86, Grass).
"""
from __future__ import annotations

from .core import Deck, Game, Mon, can_pay

LIST = {
    "Mega Kangaskhan ex": 4, "Dwebble": 3, "Crustle": 3,
    "Lillie's Determination": 4, "Boss's Orders": 4, "Team Rocket's Petrel": 4, "Hilda": 3,
    "Xerosic's Machinations": 2, "Eri": 2, "Pokémon Center Lady": 1, "Bianca's Devotion": 1,
    "Jumbo Ice Cream": 4, "Pokégear 3.0": 3, "Buddy-Buddy Poffin": 2, "Ultra Ball": 1, "Switch": 1,
    "Hero's Cape": 1, "Handheld Fan": 1, "Team Rocket's Factory": 1, "Lumiose City": 1, "Prism Tower": 1,
    "Spiky Energy": 4, "Growing Grass Energy": 4, "Mist Energy": 4, "Grass Energy": 1,
}
LINE = ("Dwebble", "Crustle")
JUNK = ["Boss's Orders", "Xerosic's Machinations", "Eri", "Pokémon Center Lady", "Bianca's Devotion",
        "Jumbo Ice Cream", "Hero's Cape", "Handheld Fan", "Prism Tower", "Spiky Energy", "Mega Kangaskhan ex"]
SUPPORTERS = ("Team Rocket's Petrel", "Hilda", "Lillie's Determination")


class Crustle(Deck):
    SLUG = "crustle-dri"
    NAME = "Crustle"
    SOURCE = "Frankfurt 区域赛 2026-09-26 第 19 名 Eemeli Reijonen"
    LIST = LIST
    TURNS = 4
    ACTIVE_PREF = ("Dwebble", "Mega Kangaskhan ex")
    BLANKS = ["Boss's Orders", "Xerosic's Machinations", "Eri", "Pokémon Center Lady", "Bianca's Devotion",
              "Jumbo Ice Cream", "Hero's Cape", "Handheld Fan", "Prism Tower",
              "Mist Energy / Spiky Energy（只当无色能量）"]
    NOTES = [
        "Ascension 是招式：要 Dwebble 在战斗场、身上 1 个能量、本回合能攻击（先攻第 1 回合不行），且这只 Dwebble 不是本回合才上场的。",
        "“后攻第 1 回合 Ascension”按允许计算（招式效果进化，手册 crustle-dri.md:22 也说以裁定为准）；规则问题里给出不允许时的数字。",
        "Superb Scissors 能打 = 一只 Crustle 身上有 Grass（Growing Grass 或基本草）+ 另 2 个能量，且在战斗场或能换上来。能量优先 Growing Grass，其次 Mist、Grass、Spiky。",
        "Kangaskhan 只当起手（没 Dwebble 时）和 Run Errand 抽 2；不主动放后备区。",
    ]

    def __init__(self, t1_ascension: bool = True, **opts):
        super().__init__(**opts)
        self.t1_ascension = t1_ascension

    def initial_bench(self, g: Game) -> None:
        for c in list(g.hand):
            if c == "Dwebble":
                g.bench_from_hand(c)

    # ---- helpers -------------------------------------------------------
    def attacker(self, g: Game) -> Mon | None:
        line = g.mons(*LINE)
        if not line:
            return None
        line.sort(key=lambda m: (m.name != "Crustle", m is not g.active, -len(m.energy)))
        if g.active.name in LINE and g.active.name == line[0].name:
            return g.active
        return line[0]

    def energy_pick(self, m: Mon, hand: list[str]) -> str | None:
        gg = m.energy.count("Growing Grass Energy")
        order = ["Growing Grass Energy"] if gg < 2 else []
        order += ["Mist Energy", "Growing Grass Energy", "Grass Energy", "Spiky Energy"]
        if not any(e in ("Growing Grass Energy", "Grass Energy") for e in m.energy) and len(m.energy) >= 2:
            order = ["Growing Grass Energy", "Grass Energy"] + order
        return next((e for e in order if e in hand), None)

    def can_ascend(self, g: Game) -> bool:
        a = g.active
        if a.name != "Dwebble" or not a.energy or not g.can_attack() or "Crustle" not in g.deck:
            return False
        if g.turn == 1 and not self.t1_ascension:
            return False
        return a.since < g.turn

    # ---- policy --------------------------------------------------------
    def step(self, g: Game) -> bool:
        h = g.hand
        room = g.bench_room()
        a = g.active
        if a.name == "Mega Kangaskhan ex" and not a.used:
            a.used = True
            g.draw(2)
            return True
        line = g.count(*LINE)
        if "Dwebble" in h and room > 0 and line < 3:
            return bool(g.bench_from_hand("Dwebble"))
        if "Buddy-Buddy Poffin" in h and room > 0 and line < 3 and "Dwebble" in g.deck:
            g.play("Buddy-Buddy Poffin")
            for _ in range(2):
                if g.count(*LINE) < 3:
                    g.bench_from_deck("Dwebble")
            g.shuffle()
            return True
        # evolve from hand
        if "Crustle" in h and g.evolvable("Dwebble"):
            ms = sorted(g.evolvable("Dwebble"), key=lambda m: (m is not g.active, -len(m.energy)))
            g.evolve(ms[0], "Crustle")
            return True
        need_crustle = not g.count("Crustle") and "Crustle" not in h and not self.can_ascend(g)
        if "Ultra Ball" in h and (not g.count(*LINE) and "Dwebble" not in h or need_crustle and g.turn >= 1):
            want = "Dwebble" if not g.count(*LINE) and "Dwebble" not in h else "Crustle"
            if g.ultra_ball(want, JUNK, {"Crustle", "Dwebble", "Growing Grass Energy", "Switch"}):
                return True
        # bring a Dwebble/Crustle to the Active spot when Kangaskhan is there
        if a.name not in LINE and g.mons(*LINE) and "Switch" in h:
            m = max(g.mons(*LINE), key=lambda m: (m.name == "Crustle", len(m.energy)))
            if m.energy or not g.attached:
                return g.pivot(m)
        # energy
        if not g.attached:
            m = self.attacker(g)
            if m:
                e = self.energy_pick(m, h)
                if e:
                    return g.attach(m, e)
        if "Pokégear 3.0" in h and g.can_supporter() and not any(s in h for s in SUPPORTERS):
            g.play("Pokégear 3.0")
            top = g.deck[-7:]
            for s in ("Team Rocket's Petrel", "Hilda", "Lillie's Determination"):
                if s in top:
                    g.deck.remove(s)
                    g.hand.append(s)
                    break
            g.shuffle()
            return True
        if g.can_supporter():
            return self.supporter(g)
        return False

    def petrel_target(self, g: Game) -> str | None:
        h = g.hand
        if not g.count(*LINE) and "Dwebble" not in h and "Buddy-Buddy Poffin" not in h:
            return "Buddy-Buddy Poffin"
        if g.active.name not in LINE and g.mons(*LINE) and "Switch" not in h:
            return "Switch"
        if not g.count("Crustle") and "Crustle" not in h and not self.can_ascend(g) and "Ultra Ball" not in h:
            return "Ultra Ball"
        if g.count(*LINE) < 2 and "Buddy-Buddy Poffin" not in h:
            return "Buddy-Buddy Poffin"
        return None

    def supporter(self, g: Game) -> bool:
        h = g.hand
        m = self.attacker(g)
        grass_missing = not any(e in h for e in ("Growing Grass Energy", "Grass Energy"))
        pt = self.petrel_target(g)
        if "Team Rocket's Petrel" in h and pt and pt in g.deck:
            if "Team Rocket's Factory" in h and g.stadium != "Team Rocket's Factory":
                g.play_stadium("Team Rocket's Factory")
            g.play_supporter("Team Rocket's Petrel")
            g.search(pt)
            g.shuffle()
            if g.stadium == "Team Rocket's Factory":
                g.draw(2)
            return True
        if "Hilda" in h and ((not g.count("Crustle") and "Crustle" not in h and not self.can_ascend(g)) or
                             (m and grass_missing)):
            g.play_supporter("Hilda")
            g.search("Crustle")
            g.search("Growing Grass Energy") or g.search("Grass Energy") or g.search("Mist Energy")
            g.shuffle()
            return True
        if "Lillie's Determination" in h and (pt or len(h) <= 4 or not m):
            return g.lillies()
        return False

    def end_turn(self, g: Game) -> None:
        g.flags["ascended"] = False
        # Superb Scissors if possible, else Ascension, else Lumiose City for a Dwebble
        for m in sorted(g.mons("Crustle"), key=lambda m: m is not g.active):
            if can_pay(m.energy, "GCC") and g.go(m, "GCC"):
                g.flags["scissors"] = True
                return
        g.flags["scissors"] = False
        if self.can_ascend(g):
            g.deck.remove("Crustle")
            g.evolve(g.active, "Crustle", from_hand=False)
            g.shuffle()
            g.attacked = True
            g.flags["ascended"] = True
            return
        if g.count(*LINE) < 2 and "Dwebble" in g.deck and g.bench_room() > 0 and (
                g.stadium == "Lumiose City" or ("Lumiose City" in g.hand and g.play_stadium("Lumiose City"))):
            g.bench_from_deck("Dwebble")
            g.shuffle()

    def measure(self, g: Game, t: int) -> dict:
        out = {}
        if t == 1:
            out["起手战斗场是 Mega Kangaskhan ex（没摸到 Dwebble）"] = "Dwebble" not in g.opening
        if t <= 3:
            out[f"第{t}回合场上有 Crustle"] = bool(g.count("Crustle"))
            out[f"第{t}回合 Crustle 在战斗场"] = g.active.name == "Crustle"
        if t == 1:
            out["第1回合用 Ascension 进化"] = g.flags.get("ascended", False)
        if t == 2:
            out["第2回合结束时有 Crustle 贴着 ≥2 张 Growing Grass"] = any(
                m.energy.count("Growing Grass Energy") >= 2 for m in g.mons(*LINE))
        if t >= 3:
            out[f"第{t}回合能用 Superb Scissors"] = g.flags.get("scissors", False)
            out[f"第{t}回合场上 ≥2 只 Crustle"] = g.count("Crustle") >= 2
        return out

    def tunings(self) -> list[dict]:
        return [
            {"question": "Growing Grass Energy 4 → 3（换 1 张基本 Grass Energy）",
             "source": "data/matchups/crustle-dri.md:435",
             "change": {"Growing Grass Energy": -1, "Grass Energy": +1}},
            {"question": "去掉 Bianca's Devotion，换第 3 张 Buddy-Buddy Poffin（换 Festival Grounds 在单人模拟里没有差别，两者都是空白卡）",
             "source": "data/brief/TEF-30C.md（Bianca's Devotion -5.4）",
             "change": {"Bianca's Devotion": -1, "Buddy-Buddy Poffin": +1}},
            {"question": "规则问题：后攻第 1 回合不允许用 Ascension 进化",
             "source": "data/matchups/crustle-dri.md:22",
             "change": {}, "opts": {"t1_ascension": False}},
        ]
