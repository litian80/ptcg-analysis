"""Slowking (SCR 58): Tomás Malaca, Regional Frankfurt 2026-09-26, 6th (best Slowking list there).

Modelled (printed text): Slowpoke/Slowking (SCR 57-58; Seek Inspiration P+C discards the top
card and copies it if it's a Pokemon without a Rule Box), Telepathic Psychic Energy (POR 88),
Academy at Night (SFA 54, a hand card on top of the deck), Ciphermaniac's Codebreaking
(TEF 145), Poke Pad (POR 81), Ultra Ball (MEG 131), Lillie's Determination (MEG 119),
Meowth ex (POR 62), Secret Box (TWM 163), Wondrous Patch (PFL 94), Switch (MEG 130),
Boomerang Energy (TWM 166), Latias ex Skyliner (SSP 76).
Copy sources: Kyurem SFA 47 Trifrost and Zeraora DRI 78 Thunder Raid (both discard all Energy
from the attacker; Boomerang comes back), Metagross CRI 61 Metallic Hammer, Annihilape PBL 41,
Pawmot PFL 34 (tuning).
"""
from __future__ import annotations

from .core import CARDS, Deck, Game, Mon, can_pay

LIST = {
    "Slowpoke": 4, "Slowking": 3, "Mega Kangaskhan ex": 3, "Latias ex": 2, "Metagross": 2,
    "Kyurem": 2, "Annihilape": 1, "Zeraora": 1, "Meowth ex": 1, "Fezandipiti ex": 1, "Mew ex": 1,
    "Lillie's Clefairy ex": 1,
    "Ciphermaniac's Codebreaking": 4, "Lillie's Determination": 4, "Poke Pad": 4, "Ultra Ball": 4,
    "Wondrous Patch": 3, "Night Stretcher": 3, "Secret Box": 1, "Switch": 1, "Academy at Night": 4,
    "Telepathic Psychic Energy": 4, "Psychic Energy": 4, "Boomerang Energy": 2,
}
LINE = ("Slowpoke", "Slowking")
SOURCES = ("Kyurem", "Metagross", "Annihilape", "Zeraora", "Pawmot")   # preference order
DISCARDS_ENERGY = ("Kyurem", "Zeraora")
PSY_BASICS = ("Slowpoke", "Latias ex", "Mew ex", "Lillie's Clefairy ex")
JUNK = ["Night Stretcher", "Mega Kangaskhan ex", "Lillie's Clefairy ex", "Fezandipiti ex", "Mew ex",
        "Wondrous Patch", "Latias ex", "Meowth ex"]
ENERGY = ("Telepathic Psychic Energy", "Psychic Energy", "Boomerang Energy")


class Slowking(Deck):
    SLUG = "slowking-scr"
    NAME = "Slowking"
    SOURCE = "Frankfurt 区域赛 2026-09-26 第 6 名 Tomás Malaca"
    LIST = LIST
    TURNS = 4
    ACTIVE_PREF = ("Slowpoke", "Latias ex", "Mew ex", "Fezandipiti ex", "Lillie's Clefairy ex", "Meowth ex",
                   "Mega Kangaskhan ex", "Zeraora", "Kyurem")
    BLANKS = ["Mega Kangaskhan ex（Run Errand 也没算）", "Fezandipiti ex", "Mew ex", "Lillie's Clefairy ex",
              "Night Stretcher", "Slowpoke 的 Dangle Tail"]
    NOTES = [
        "Slowking 能攻击 = 身上 Psychic + 另 1 个能量，在战斗场或能换上来（Switch、Latias ex 让基础宝可梦撤退 0 只帮 Latias 自己下场）。",
        "“指定复制”= 攻击前用 Academy at Night 把手上的复制来源放到牌库顶（手上没有就先用 Poké Pad 拿），或用 Ciphermaniac's Codebreaking 直接叠到牌库顶；做不到就盲翻。",
        "复制 Kyurem / Zeraora 会弃掉 Slowking 身上全部能量（Boomerang 回来），下回合要重新补能量。",
        "复制来源（Kyurem、Zeraora）起手能不放就不放。",
    ]

    def initial_bench(self, g: Game) -> None:
        for c in list(g.hand):
            if c == "Slowpoke" and g.count(*LINE) < 3:
                g.bench_from_hand(c)

    # ---- helpers -------------------------------------------------------
    def attacker(self, g: Game) -> Mon | None:
        ks = g.mons("Slowking")
        if not ks:
            return None
        ks.sort(key=lambda m: (m is not g.active, -len(m.energy)))
        return ks[0]

    def builder(self, g: Game) -> Mon | None:
        """The Slowpoke/Slowking that gets the energy: the Active one first."""
        line = g.mons(*LINE)
        if not line:
            return None
        line.sort(key=lambda m: (m is not g.active, m.name != "Slowking", -len(m.energy)))
        return line[0]

    def need(self, m: Mon | None) -> list[str]:
        if not m:
            return []
        if can_pay(m.energy, "PC"):
            return []
        if not can_pay(m.energy, "P"):
            return ["P"] + ([] if m.energy else ["C"])
        return ["C"]

    def wants(self, g: Game) -> list[str]:
        h = g.hand
        out = []
        if g.count(*LINE) + h.count("Slowpoke") < 2:
            out.append("Slowpoke")
        if g.evolvable("Slowpoke") and not g.count("Slowking") and "Slowking" not in h:
            out.append("Slowking")
        if g.turn >= 1 and g.mons("Slowpoke") and g.count("Slowking") + h.count("Slowking") < 2:
            out.append("Slowking")
        if g.count(*LINE) + h.count("Slowpoke") < 3:
            out.append("Slowpoke")
        return out

    def academy_ok(self, g: Game) -> bool:
        return g.stadium == "Academy at Night" or ("Academy at Night" in g.hand and not g.stadium_played)

    # ---- policy --------------------------------------------------------
    def step(self, g: Game) -> bool:
        h = g.hand
        room = g.bench_room()
        line = g.count(*LINE)
        if "Slowpoke" in h and room > 1 and line < 3:
            return bool(g.bench_from_hand("Slowpoke"))
        if "Latias ex" in h and room > 2 and not g.count("Latias ex") and g.active.name not in LINE:
            return bool(g.bench_from_hand("Latias ex"))
        if "Academy at Night" in h and g.stadium != "Academy at Night":
            return g.play_stadium("Academy at Night")
        # evolve
        if "Slowking" in h and g.evolvable("Slowpoke"):
            ms = sorted(g.evolvable("Slowpoke"), key=lambda m: (m is not g.active, -len(m.energy)))
            g.evolve(ms[0], "Slowking")
            return True
        # energy
        b = self.builder(g)
        if b and not self.need(b):        # pre-load the next Slowking/Slowpoke
            b = next((m for m in g.mons(*LINE) if self.need(m)), b)
        if not g.attached:
            need = self.need(b)
            if b and need:
                if "P" in need:
                    for e in ("Telepathic Psychic Energy", "Psychic Energy"):
                        if e in h:
                            return self.attach(g, b, e)
                else:
                    for e in ("Boomerang Energy", "Psychic Energy", "Telepathic Psychic Energy"):
                        if e in h:
                            return self.attach(g, b, e)
            elif not b and "Telepathic Psychic Energy" in h and CARDS[g.active.name].type == "P":
                return self.attach(g, g.active, "Telepathic Psychic Energy")
        # Wondrous Patch: Psychic from the discard to a Benched Psychic Pokemon
        if "Wondrous Patch" in h and "Psychic Energy" in g.discard:
            ms = [m for m in g.bench if m.name in LINE and self.need(m)]
            if ms:
                g.play("Wondrous Patch")
                g.discard.remove("Psychic Energy")
                ms[0].energy.append("Psychic Energy")
                return True
        ws = self.wants(g)
        if g.poke_pad(ws):
            return True
        if ws and ws[0] in ("Slowking", "Slowpoke") and "Ultra Ball" in h and (g.count(*LINE) < 1 or ws[0] == "Slowking"):
            if g.ultra_ball(ws[0], JUNK, set(SOURCES) | {"Slowking", "Academy at Night"} | set(ENERGY)):
                return True
        if "Secret Box" in h and not self.academy_ok(g) and len(h) >= 4:
            disc = None
            h.remove("Secret Box")
            disc = g.take_discards(3, JUNK + ["Ultra Ball", "Lillie's Determination"],
                                   set(SOURCES) | {"Slowking", "Slowpoke", "Telepathic Psychic Energy"})
            if disc:
                g.discard.append("Secret Box")
                for c in disc:
                    h.remove(c)
                    g.discard.append(c)
                for c in ("Poke Pad", "Ciphermaniac's Codebreaking", "Academy at Night"):
                    g.search(c)
                g.shuffle()
                return True
            h.append("Secret Box")
        if g.can_supporter():
            return self.supporter(g)
        return False

    def attach(self, g: Game, m: Mon, e: str) -> bool:
        g.attach(m, e)
        if e == "Telepathic Psychic Energy" and CARDS[m.name].type == "P":
            for _ in range(2):
                if g.count(*LINE) < 3 and g.bench_room() > 1:
                    g.bench_from_deck("Slowpoke")
            g.shuffle()
        return True

    def will_attack(self, g: Game) -> bool:
        k = self.attacker(g)
        if k and can_pay(k.energy, "PC"):
            return True
        return "Slowking" in g.hand and bool(g.evolvable("Slowpoke"))

    def supporter(self, g: Game) -> bool:
        h = g.hand
        ws = self.wants(g)
        # keep Codebreaking for the attack when Academy can't place the target
        reserve = self.will_attack(g) and not self.academy_ok(g) and "Ciphermaniac's Codebreaking" in h
        b = self.builder(g)
        no_energy = bool(b and self.need(b)) and not any(e in h for e in ENERGY)
        if "Lillie's Determination" in h and not reserve and (
                ws and ws[0] in ("Slowpoke", "Slowking") or len(h) <= 4 or no_energy):
            return g.lillies()
        if not any(s in h for s in ("Lillie's Determination", "Ciphermaniac's Codebreaking")) and "Meowth ex" in h \
                and g.bench_room() > 1:
            g.bench_from_hand("Meowth ex")
            g.search("Lillie's Determination") or g.search("Ciphermaniac's Codebreaking")
            g.shuffle()
            return True
        return False

    def end_turn(self, g: Game) -> None:
        g.flags["seek"] = g.flags["controlled"] = False
        g.flags["blind_useful"] = None
        k = self.attacker(g)
        if not k or not g.can_go(k, "PC"):
            return
        # place a copy source on top
        # own turn 2: Trifrost first (spread); later prefer copies that keep the Energy
        sources = SOURCES if g.turn == 2 else ("Metagross", "Annihilape", "Pawmot", "Kyurem", "Zeraora")
        target = next((s for s in sources if s in g.hand), None)
        if self.academy_ok(g) and not target and "Poke Pad" in g.hand:
            for s in sources:
                if g.search(s):
                    g.play("Poke Pad")
                    g.shuffle()
                    target = s
                    break
        if target and self.academy_ok(g):
            if g.stadium != "Academy at Night":
                g.play_stadium("Academy at Night")
            g.hand.remove(target)
            g.deck.append(target)
            g.flags["controlled"] = True
        elif g.can_supporter() and "Ciphermaniac's Codebreaking" in g.hand and any(s in g.deck for s in SOURCES):
            g.play_supporter("Ciphermaniac's Codebreaking")
            s = next(s for s in sources if s in g.deck)
            g.deck.remove(s)
            g.shuffle()
            g.deck.append(s)
            g.flags["controlled"] = True
        else:
            g.flags["blind_useful"] = sum(1 for c in g.deck if c in SOURCES) / max(len(g.deck), 1)
        if not g.go(k, "PC"):
            g.flags["controlled"] = False
            return
        g.flags["seek"] = True
        top = g.deck.pop() if g.deck else None
        if top:
            g.discard.append(top)
        if top in DISCARDS_ENERGY:
            for e in list(k.energy):
                if e != "Boomerang Energy":
                    k.energy.remove(e)
                    g.discard.append(e)

    def measure(self, g: Game, t: int) -> dict:
        out = {}
        if t == 1:
            basics = [c for c in g.opening if CARDS[c].kind == "pokemon" and CARDS[c].stage == 0]
            out["起手只能把复制来源（Kyurem/Zeraora）放战斗场"] = all(c in ("Kyurem", "Zeraora") for c in basics)
            out["第1回合结束后场上 ≥2 只 Slowpoke 线"] = g.count(*LINE) >= 2
            return out
        out[f"第{t}回合场上有 Slowking"] = bool(g.count("Slowking"))
        out[f"第{t}回合 Slowking 能攻击"] = g.flags["seek"]
        out[f"第{t}回合攻击且指定了复制目标"] = g.flags["controlled"] and g.flags["seek"]
        if t in (2, 3):
            out[f"第{t}回合只能盲翻时翻到复制来源的概率"] = g.flags["blind_useful"] if g.flags["seek"] else None
        return out

    def tunings(self) -> list[dict]:
        return [
            {"question": "加 1 只 Pawmot（减 1 张 Night Stretcher）",
             "source": "data/brief/TEF-30C.md（Pawmot +6.6）",
             "change": {"Pawmot": +1, "Night Stretcher": -1}},
            {"question": "加 1 张 Lana's Aid、Academy at Night 4 → 3",
             "source": "data/brief/TEF-30C.md（Lana's Aid +5.1；Lana's Aid 在单人模拟里是空白卡，这里量的是少 1 张 Academy 的代价）",
             "change": {"Lana's Aid": +1, "Academy at Night": -1}},
        ]
