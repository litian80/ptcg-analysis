"""Alakazam Dusknoir: Tomasz Chałupka, Regional Frankfurt 2026-09-26, 1st.

Modelled (printed text): Abra/Kadabra/Alakazam (MEG 54-56, Psychic Draw 2/3), Duskull/
Dusclops/Dusknoir (PRE 35-37, only as "Cursed Blast available"), Dawn (PFL 87), Hilda (WHT 84),
Gwynn (PBL 78), Rare Candy (MEG 125), Poke Pad (POR 81), Buddy-Buddy Poffin (TEF 144),
Telepathic Psychic Energy (POR 88), Prime Catcher (TEF 157, only as a free switch).
Abra TWM 80 (Teleporter) is counted as a plain Abra.
"""
from __future__ import annotations

from .core import Deck, Game, Mon, modified  # noqa: F401

LIST = {
    "Duskull": 4, "Dusclops": 2, "Dusknoir": 2, "Abra": 4, "Kadabra": 4, "Alakazam": 3,
    "Budew": 2, "Shaymin": 1, "Fezandipiti ex": 1,
    "Hilda": 4, "Dawn": 4, "Gwynn": 3, "Boss's Orders": 1,
    "Rare Candy": 4, "Poke Pad": 4, "Buddy-Buddy Poffin": 3, "Strange Timepiece": 3,
    "Special Red Card": 2, "Night Stretcher": 2, "Sacred Ash": 1, "Prime Catcher": 1,
    "Telepathic Psychic Energy": 4, "Psychic Energy": 1,
}
LINE = ("Abra", "Kadabra", "Alakazam")
DUSK = ("Duskull", "Dusclops", "Dusknoir")
ENERGY = ("Telepathic Psychic Energy", "Psychic Energy")


class AlakazamDusknoir(Deck):
    SLUG = "alakazam-dusknoir"
    NAME = "Alakazam Dusknoir"
    SOURCE = "Frankfurt 区域赛 2026-09-26 冠军 Tomasz Chałupka"
    LIST = LIST
    TURNS = 4
    PIVOTS = ("Prime Catcher",)
    ACTIVE_PREF = ("Budew", "Abra", "Duskull", "Shaymin", "Fezandipiti ex")
    BLANKS = ["Budew", "Shaymin", "Fezandipiti ex", "Boss's Orders", "Strange Timepiece",
              "Special Red Card", "Night Stretcher", "Sacred Ash", "Abra TWM 80 的 Teleporter"]
    NOTES = [
        "攻击 = Alakazam 身上有超能量且在战斗场或能换上来（Budew 撤退 0；Prime Catcher 当免费换位；其他按撤退费弃能量）。",
        "手牌数 = 攻击时的手牌（手贴能量后）。打法先打完所有能进化抽牌的牌，Poffin 等会减手牌的牌也照打（贪心，偏保守）。",
        "Dusknoir 只统计“当回合能用 Cursed Blast”：场上有 Dusknoir，或手上有 Dusknoir 且有 Rare Candy+可进化的 Duskull / 可进化的 Dusclops（或 Poké Pad 能拿到 Dusknoir）。打法本身不进化 Dusknoir（会减 2 张手牌）。",
    ]

    def initial_bench(self, g: Game) -> None:
        for c in list(g.hand):
            if c == "Abra" and g.count(*LINE) < 3:
                g.bench_from_hand(c)
            elif c == "Duskull" and g.count(*DUSK) < 2:
                g.bench_from_hand(c)

    # ---- helpers -------------------------------------------------------
    def attacker(self, g: Game) -> Mon | None:
        zams = g.mons("Alakazam")
        if not zams:
            return None
        zams.sort(key=lambda m: (not m.energy, m is not g.active))
        return zams[0]

    def path_ok(self, g: Game) -> bool:
        h = g.hand
        if g.count("Alakazam"):
            return True
        return "Alakazam" in h and (bool(g.evolvable("Kadabra")) or ("Rare Candy" in h and bool(g.evolvable("Abra"))))

    def discardable(self, g: Game) -> list[str]:
        """Non-rule-box Pokemon in hand that Gwynn can throw away."""
        h = list(g.hand)
        out = []
        for c in ("Budew", "Shaymin", "Dusclops"):
            out += [c] * h.count(c)
        extra = h.count("Duskull") - (1 if g.count(*DUSK) < 2 and g.bench_room() > 0 else 0)
        out += ["Duskull"] * max(extra, 0)
        extra = h.count("Abra") - (1 if g.count(*LINE) < 3 and g.bench_room() > 0 else 0)
        out += ["Abra"] * max(extra, 0)
        extra = h.count("Kadabra") - len(g.mons("Abra"))
        out += ["Kadabra"] * max(extra, 0)
        out += ["Dusknoir"] * max(h.count("Dusknoir") - 1, 0)
        return out

    def wants(self, g: Game) -> list[str]:
        h = g.hand
        out = []
        if g.count(*LINE) < 2 and "Abra" not in h:
            out.append("Abra")
        if g.turn >= 2 and "Alakazam" not in h and (
                ("Rare Candy" in h and g.evolvable("Abra")) or g.evolvable("Kadabra")):
            out.append("Alakazam")
        if g.turn >= 2 and g.evolvable("Abra") and "Kadabra" not in h and "Rare Candy" not in h:
            out.append("Kadabra")
        if g.count(*DUSK) == 0 and "Duskull" not in h:
            out.append("Duskull")
        if g.count(*LINE) < 3 and "Abra" not in h and "Abra" not in out:
            out.append("Abra")
        return out

    # ---- policy --------------------------------------------------------
    def step(self, g: Game) -> bool:
        h = g.hand
        line, dusk = g.count(*LINE), g.count(*DUSK)
        if "Abra" in h and line < 3 and g.bench_room() > 0:
            return bool(g.bench_from_hand("Abra"))
        if "Duskull" in h and dusk < 2 and g.bench_room() > 0:
            return bool(g.bench_from_hand("Duskull"))
        if "Buddy-Buddy Poffin" in h and g.bench_room() > 0 and (line < 3 or dusk < 2):
            g.play("Buddy-Buddy Poffin")
            for _ in range(2):
                want = "Abra" if g.count(*LINE) < 3 else ("Duskull" if g.count(*DUSK) < 2 else None)
                if want:
                    g.bench_from_deck(want)
            g.shuffle()
            return True
        # energy
        if not g.attached:
            zam = next((m for m in g.mons("Alakazam") if not m.energy), None)
            target = None
            if zam and not any(m.energy for m in g.mons("Alakazam")):
                target = zam
            elif not any(m.energy for m in g.board) and "Telepathic Psychic Energy" in h:
                # active Abra/Duskull first (attacker, or energy to pay its retreat later)
                psy = [m for m in g.board if m.name in LINE + DUSK]
                psy.sort(key=lambda m: (m is not g.active, m.name != "Abra"))
                target = psy[0] if psy else None
            if target:
                e = "Telepathic Psychic Energy" if "Telepathic Psychic Energy" in h else (
                    "Psychic Energy" if "Psychic Energy" in h else None)
                if e:
                    g.attach(target, e)
                    if e == "Telepathic Psychic Energy":
                        for _ in range(2):
                            want = "Abra" if g.count(*LINE) < 3 else ("Duskull" if g.count(*DUSK) < 2 else None)
                            if want:
                                g.bench_from_deck(want)
                        g.shuffle()
                    return True
        # evolve
        if g.turn >= 2:
            if "Alakazam" in h:
                if g.evolvable("Kadabra"):
                    g.evolve(self._pick(g, g.evolvable("Kadabra")), "Alakazam")
                    g.draw(3)
                    return True
                if "Rare Candy" in h and g.evolvable("Abra"):
                    g.play("Rare Candy")
                    g.evolve(self._pick(g, g.evolvable("Abra")), "Alakazam")
                    g.draw(3)
                    return True
            if "Kadabra" in h and g.evolvable("Abra") and not ("Rare Candy" in h and "Alakazam" in h):
                g.evolve(self._pick(g, g.evolvable("Abra")), "Kadabra")
                g.draw(2)
                return True
        if "Poke Pad" in h:
            ws = self.wants(g)
            if g.turn >= 2 and g.evolvable("Abra") and "Kadabra" not in h:
                ws.append("Kadabra")
            for w in ws:
                if g.search(w):
                    g.play("Poke Pad")
                    g.shuffle()
                    return True
        if g.can_supporter():
            return self.supporter(g)
        return False

    @staticmethod
    def _pick(g: Game, ms: list[Mon]) -> Mon:
        ms = sorted(ms, key=lambda m: (m is not g.active, not m.energy))
        return ms[0]

    def supporter(self, g: Game) -> bool:
        h = g.hand
        need_energy = g.count("Alakazam") and not any(e in h for e in ENERGY) and \
            not any(m.energy for m in g.mons("Alakazam"))
        disc = self.discardable(g)
        if need_energy and "Hilda" in h:
            return self._hilda(g)
        if g.turn >= 2 and not self.path_ok(g):
            if "Dawn" in h:
                return self._dawn(g)
            if "Hilda" in h:
                return self._hilda(g)
            if "Gwynn" in h and disc:
                return self._gwynn(g, disc)
            return False
        if g.turn == 1 and self.wants(g) and "Dawn" in h:
            return self._dawn(g)
        if "Gwynn" in h and len(disc) >= 2:
            return self._gwynn(g, disc)
        if "Dawn" in h:
            return self._dawn(g)
        if "Hilda" in h:
            return self._hilda(g)
        if "Gwynn" in h and disc:
            return self._gwynn(g, disc)
        return False

    def _dawn(self, g: Game) -> bool:
        g.play_supporter("Dawn")
        basic = "Abra" if g.count(*LINE) + g.hand.count("Abra") < 3 else "Duskull"
        g.search(basic) or g.search("Abra") or g.search("Duskull")
        g.search("Kadabra") or g.search("Dusclops")
        g.search("Alakazam") or g.search("Dusknoir")
        g.shuffle()
        return True

    def _hilda(self, g: Game) -> bool:
        g.play_supporter("Hilda")
        g.search("Alakazam" if g.turn >= 2 else "Kadabra") or g.search("Kadabra") or g.search("Dusknoir")
        g.search("Telepathic Psychic Energy") or g.search("Psychic Energy")
        g.shuffle()
        return True

    def _gwynn(self, g: Game, disc: list[str]) -> bool:
        g.play_supporter("Gwynn")
        for c in disc[:2]:
            g.hand.remove(c)
            g.discard.append(c)
            g.draw(3)
        return True

    def end_turn(self, g: Game) -> None:
        m = self.attacker(g)
        if m and g.go(m, "P"):
            g.flags["attack_hand"] = len(g.hand)
        else:
            g.flags["attack_hand"] = None

    def blast(self, g: Game) -> bool:
        h = g.hand
        if g.count("Dusknoir"):
            return True
        has = "Dusknoir" in h or ("Poke Pad" in h and "Dusknoir" in g.deck)
        return has and (("Rare Candy" in h and bool(g.evolvable("Duskull"))) or bool(g.evolvable("Dusclops")))

    def measure(self, g: Game, t: int) -> dict:
        out = {}
        hand = g.flags.get("attack_hand")
        if t == 1:
            energy_prized = sum(1 for c in g.prizes if c in ENERGY)
            out["5 个能量里≥2 个在奖赏卡"] = energy_prized >= 2
            out["起手只有 Fezandipiti ex 能放战斗场"] = not any(
                c in g.opening for c in ("Abra", "Duskull", "Budew", "Shaymin"))
            return out
        out[f"第{t}回合 Alakazam 能攻击"] = hand is not None
        if t in (2, 3):
            out[f"第{t}回合攻击时手牌（均值）"] = hand
            out[f"第{t}回合能用 Cursed Blast"] = self.blast(g)
        if t == 3:
            out["第3回合攻击且手牌≥10（+Dusknoir 一击 Dragapult ex）"] = hand is not None and hand >= 10
        if t in (3, 4):
            out[f"第{t}回合攻击且手牌≥16（单靠 Powerful Hand 一击 Dragapult ex）"] = hand is not None and hand >= 16
        return out

    def tunings(self) -> list[dict]:
        return [
            {"question": "Dawn 4 张 → 3 张（多 1 张 Gwynn，22 份卡表中位数的配法）",
             "source": "data/matchups/alakazam-dusknoir.md:38",
             "change": {"Dawn": -1, "Gwynn": +1}},
            {"question": "第 3 张 Dusknoir（换 1 张 Special Red Card）",
             "source": "data/matchups/alakazam-dusknoir.md:179",
             "change": {"Dusknoir": +1, "Special Red Card": -1}},
        ]
