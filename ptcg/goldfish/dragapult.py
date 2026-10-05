"""Dragapult ex: Owyn Kamerman, Regional Frankfurt 2026-09-26, 7th (best Dragapult list there).

Modelled (printed text): Dreepy/Drakloak/Dragapult ex (TWM 128-130; Recon Directive look 2
take 1), Buddy-Buddy Poffin (TEF 144), Poke Pad (POR 81), Ultra Ball (MEG 131), Lillie's
Determination (MEG 119; always 8 cards, a goldfish never takes prizes), Crispin (SCR 133),
Judge (POR 76), Meowth ex Last-Ditch Catch (POR 62), Munkidori (TWM 95, only "has Darkness").
Tuning variant adds Dunsparce (JTG 120) / Dudunsparce (TEF 129, Run Away Draw).
"""
from __future__ import annotations

from .core import Deck, Game, Mon

LIST = {
    "Dreepy": 4, "Drakloak": 4, "Dragapult ex": 3, "Budew": 2, "Munkidori": 2,
    "Meowth ex": 1, "Fezandipiti ex": 1,
    "Lillie's Determination": 4, "Crispin": 3, "Boss's Orders": 3, "Judge": 1,
    "Crushing Hammer": 4, "Buddy-Buddy Poffin": 4, "Poke Pad": 4, "Ultra Ball": 4,
    "Night Stretcher": 2, "Unfair Stamp": 1, "Special Red Card": 1, "Handheld Fan": 1,
    "Team Rocket's Watchtower": 2,
    "Fire Energy": 3, "Psychic Energy": 3, "Darkness Energy": 3,
}
LINE = ("Dreepy", "Drakloak", "Dragapult ex")
JUNK = ["Crushing Hammer", "Special Red Card", "Unfair Stamp", "Handheld Fan", "Team Rocket's Watchtower",
        "Boss's Orders", "Judge", "Night Stretcher", "Fezandipiti ex", "Budew"]
ENERGY_OF = {"R": "Fire Energy", "P": "Psychic Energy", "D": "Darkness Energy"}


class Dragapult(Deck):
    SLUG = "dragapult-ex"
    NAME = "Dragapult ex"
    SOURCE = "Frankfurt 区域赛 2026-09-26 第 7 名 Owyn Kamerman"
    LIST = LIST
    TURNS = 4
    ACTIVE_PREF = ("Budew", "Dreepy", "Munkidori", "Fezandipiti ex", "Dunsparce", "Meowth ex")
    BLANKS = ["Budew", "Fezandipiti ex", "Boss's Orders", "Crushing Hammer", "Night Stretcher",
              "Unfair Stamp", "Special Red Card", "Handheld Fan", "Team Rocket's Watchtower",
              "Munkidori 的 Adrena-Brain（只统计是否贴上 Darkness）"]
    NOTES = [
        "Phantom Dive 能打 = 场上一只 Dragapult ex 身上有 Fire + Psychic，且在战斗场或能换上来（撤退费由战斗场身上的能量支付，Budew 撤退 0）。",
        "能量优先贴给最早能进化成 Dragapult ex 的那只（Fire、Psychic 各一个），其次给 Munkidori 贴 Darkness。",
        "Ultra Ball 弃牌顺序：Crushing Hammer、Special Red Card、Unfair Stamp、Handheld Fan、Watchtower、Boss、Judge、Night Stretcher…",
    ]

    def initial_bench(self, g: Game) -> None:
        for c in list(g.hand):
            if c == "Dreepy" and g.count(*LINE) < 3:
                g.bench_from_hand(c)
            elif c == "Munkidori" and not g.count("Munkidori"):
                g.bench_from_hand(c)
            elif c == "Dunsparce" and not g.count("Dunsparce", "Dudunsparce"):
                g.bench_from_hand(c)

    # ---- helpers -------------------------------------------------------
    def candidate(self, g: Game) -> Mon | None:
        """The Pokemon we're building into the attacking Dragapult ex."""
        line = [m for m in g.board if m.name in LINE]
        if not line:
            return None
        rank = {"Dragapult ex": 0, "Drakloak": 1, "Dreepy": 2}
        line.sort(key=lambda m: (rank[m.name], -len(m.energy), m.since, m is not g.active))
        return line[0]

    def missing_energy(self, g: Game) -> list[str]:
        m = self.candidate(g)
        out = []
        if m:
            have = [e for e in m.energy]
            for sym in "RP":
                if ENERGY_OF[sym] in have:
                    have.remove(ENERGY_OF[sym])
                else:
                    out.append(sym)
        return out

    def munki_needs_dark(self, g: Game) -> bool:
        return bool(g.count("Munkidori")) and not any("Darkness Energy" in m.energy for m in g.mons("Munkidori"))

    def wants(self, g: Game) -> list[str]:
        h = g.hand
        out = []
        if g.count(*LINE) + h.count("Dreepy") < 2:
            out.append("Dreepy")
        if g.evolvable("Drakloak") and "Dragapult ex" not in h:
            out.append("Dragapult ex")
        if g.turn >= 2 and g.evolvable("Dreepy") and "Drakloak" not in h:
            out.append("Drakloak")
        if g.turn >= 1 and g.count(*LINE) + h.count("Dreepy") < 3:
            out.append("Dreepy")
        # next turn's Dragapult: a Drakloak that can't evolve yet
        if g.mons("Drakloak") and not g.evolvable("Drakloak") and "Dragapult ex" not in h:
            out.append("Dragapult ex")
        if not g.count("Munkidori") and "Munkidori" not in h:
            out.append("Munkidori")
        return out

    def recon_pick(self, g: Game, cards: list[str]) -> str:
        ws = self.wants(g)
        miss = [ENERGY_OF[s] for s in self.missing_energy(g)]
        if self.munki_needs_dark(g):
            miss.append("Darkness Energy")
        has_sup = any(c in g.hand for c in ("Lillie's Determination", "Crispin"))

        def score(c):
            if c in ws:
                return 10 - ws.index(c)
            if c in miss and c not in g.hand:
                return 4
            if c in ("Lillie's Determination", "Crispin") and not has_sup:
                return 3
            if c in ("Ultra Ball", "Buddy-Buddy Poffin", "Poke Pad"):
                return 2
            return 0
        return max(cards, key=score)

    # ---- policy --------------------------------------------------------
    def step(self, g: Game) -> bool:
        h = g.hand
        line = g.count(*LINE)
        room = g.bench_room()
        if "Dreepy" in h and line < 4 and room > 0:
            return bool(g.bench_from_hand("Dreepy"))
        if "Munkidori" in h and room > 0 and (g.count("Munkidori") < 1 or (g.count("Munkidori") < 2 and line >= 3)):
            return bool(g.bench_from_hand("Munkidori"))
        if "Dunsparce" in h and room > 1 and not g.count("Dunsparce", "Dudunsparce"):
            return bool(g.bench_from_hand("Dunsparce"))
        if "Buddy-Buddy Poffin" in h and room > 0 and line < 4 and "Dreepy" in g.deck:
            g.play("Buddy-Buddy Poffin")
            for _ in range(2):
                if g.count(*LINE) < 4:
                    g.bench_from_deck("Dreepy")
            g.shuffle()
            return True
        # evolve
        if "Dragapult ex" in h and g.evolvable("Drakloak"):
            ms = sorted(g.evolvable("Drakloak"), key=lambda m: (-len(m.energy), m is not g.active))
            g.evolve(ms[0], "Dragapult ex")
            return True
        if "Drakloak" in h and g.evolvable("Dreepy"):
            ms = sorted(g.evolvable("Dreepy"), key=lambda m: (-len(m.energy), m is not g.active))
            g.evolve(ms[0], "Drakloak")
            return True
        if "Dudunsparce" in h and g.evolvable("Dunsparce"):
            m = g.evolvable("Dunsparce")[0]
            g.evolve(m, "Dudunsparce")
            return True
        for m in g.mons("Dudunsparce"):     # Run Away Draw: draw 3, shuffle it back
            if not m.used and len(g.board) > 1:
                g.board.remove(m)
                g.draw(3)
                g.deck += m.cards + m.energy
                g.shuffle()
                return True
        # Recon Directive
        for m in g.mons("Drakloak"):
            if not m.used and g.deck:
                m.used = True
                top = [g.deck.pop() for _ in range(min(2, len(g.deck)))]
                pick = self.recon_pick(g, top)
                top.remove(pick)
                g.hand.append(pick)
                g.deck[0:0] = top          # the other card to the bottom
                return True
        ws = self.wants(g)
        if g.poke_pad(ws):
            return True
        if ws and "Ultra Ball" in h:
            keep = {"Dragapult ex", "Drakloak", "Dreepy"} | {ENERGY_OF[x] for x in self.missing_energy(g)}
            for w in ws:
                if w not in ("Dragapult ex", "Drakloak") and not (w == "Dreepy" and line < 2):
                    continue
                if g.ultra_ball(w, JUNK, keep):
                    return True
        # energy
        if not g.attached:
            cand = self.candidate(g)
            for sym in self.missing_energy(g):
                if ENERGY_OF[sym] in h and cand:
                    return g.attach(cand, ENERGY_OF[sym])
            if self.munki_needs_dark(g) and "Darkness Energy" in h:
                m = g.mons("Munkidori")[0]
                return g.attach(m, "Darkness Energy")
        # supporter
        if g.can_supporter():
            useful = "Lillie's Determination" in h or ("Crispin" in h and self.missing_energy(g))
            if not useful and "Meowth ex" in h and room > 0:
                g.bench_from_hand("Meowth ex")
                choice = "Crispin" if self.missing_energy(g) and g.turn >= 2 else "Lillie's Determination"
                g.search(choice) or g.search("Lillie's Determination") or g.search("Crispin")
                g.shuffle()
                return True
            return self.supporter(g)
        return False

    def supporter(self, g: Game) -> bool:
        h = g.hand
        miss = self.missing_energy(g)
        ws = self.wants(g)
        if "Crispin" in h and miss and (g.turn >= 2 or not ws):
            return self._crispin(g)
        if "Lillie's Determination" in h and (ws or len(h) <= 5):
            return g.lillies()
        if "Crispin" in h and (miss or self.munki_needs_dark(g)):
            return self._crispin(g)
        if "Judge" in h and len(h) <= 3:
            g.play_supporter("Judge")
            g.deck += g.hand
            g.hand.clear()
            g.shuffle()
            g.draw(4)
            return True
        return False

    def _crispin(self, g: Game) -> bool:
        g.play_supporter("Crispin")
        miss = self.missing_energy(g)
        order = [ENERGY_OF[s] for s in miss] + ["Darkness Energy", "Fire Energy", "Psychic Energy"]
        got = []
        for e in order:
            if e not in got and e in g.deck and len(got) < 2:
                g.deck.remove(e)
                got.append(e)
        if got:
            cand = self.candidate(g)
            first = got[0]
            if cand and first in [ENERGY_OF[s] for s in miss]:
                cand.energy.append(first)
            elif first == "Darkness Energy" and g.count("Munkidori"):
                g.mons("Munkidori")[0].energy.append(first)
            elif cand:
                cand.energy.append(first)
            else:
                g.hand.append(first)
            g.hand += got[1:]
        g.shuffle()
        return True

    def end_turn(self, g: Game) -> None:
        g.flags["dive"] = any(g.go(m, "RP") for m in g.mons("Dragapult ex"))

    def measure(self, g: Game, t: int) -> dict:
        out = {}
        if t == 1:
            out["第1回合结束时场上 ≥2 只 Dreepy 线"] = g.count(*LINE) >= 2
            return out
        if t >= 2:
            out[f"第{t}回合场上有 Dragapult ex"] = bool(g.count("Dragapult ex"))
        if t >= 3:
            out[f"第{t}回合能用 Phantom Dive"] = g.flags.get("dive", False)
            out[f"第{t}回合 Munkidori 贴着 Darkness"] = not self.munki_needs_dark(g) and bool(g.count("Munkidori"))
        if t == 3:
            out["第3回合 Phantom Dive + Munkidori 都就绪"] = g.flags.get("dive", False) and \
                bool(g.count("Munkidori")) and not self.munki_needs_dark(g)
        if t == 4:
            out["第4回合场上 ≥2 只 Dragapult ex"] = g.count("Dragapult ex") >= 2
            out["第4回合有第二只攻击手（第 2 只 Dragapult ex 或可进化的 Drakloak）"] = \
                g.count("Dragapult ex") >= 2 or (g.count("Dragapult ex") >= 1 and bool(g.mons("Drakloak")))
        return out

    def tunings(self) -> list[dict]:
        return [
            {"question": "Darkness 能量 3 → 2（多 1 张 Judge）",
             "source": "data/matchups/dragapult-ex.md:31、data/matchups/dragapult-ex.md:612",
             "change": {"Darkness Energy": -1, "Judge": +1}},
            {"question": "加 Dunsparce + Dudunsparce（减 1 张 Crushing Hammer、1 张 Boss's Orders）",
             "source": "data/matchups/dragapult-ex.md:83",
             "change": {"Dunsparce": +1, "Dudunsparce": +1, "Crushing Hammer": -1, "Boss's Orders": -1}},
        ]
