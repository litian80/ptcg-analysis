"""Alakazam Dudunsparce: Diego Cassiraga, Worlds 2026 2nd (the original prototype list).

Modelled (printed text, MEG/PFL/WHT/POR/TEF/JTG): Dawn, Hilda, Poke Pad, Buddy-Buddy Poffin,
Rare Candy, Telepathic Psychic Energy, Kadabra/Alakazam Psychic Draw, Dudunsparce Run Away Draw.
"""
from __future__ import annotations

from .core import Deck, Game

LIST = {
    "Abra": 4, "Kadabra": 4, "Alakazam": 3, "Dunsparce": 3, "Dudunsparce": 3,
    "Genesect": 2, "Dedenne": 1, "Fezandipiti ex": 1, "Shaymin": 1,
    "Dawn": 4, "Hilda": 3, "Boss's Orders": 2, "Lana's Aid": 1, "Eri": 1,
    "Buddy-Buddy Poffin": 4, "Poke Pad": 4, "Rare Candy": 3, "Enhanced Hammer": 2,
    "Sacred Ash": 1, "Air Balloon": 2, "Lucky Helmet": 1, "Battle Cage": 4,
    "Telepathic Psychic Energy": 4, "Psychic Energy": 1, "Enriching Energy": 1,
}
LINE = ("Abra", "Kadabra", "Alakazam")


class AlakazamDudunsparce(Deck):
    SLUG = "alakazam-dudunsparce"
    NAME = "Alakazam Dudunsparce"
    SOURCE = "2026 世界赛亚军 Diego Cassiraga（原型卡表）"
    LIST = LIST
    TURNS = 3
    ACTIVE_PREF = ("Dunsparce", "Shaymin", "Genesect", "Dedenne", "Abra", "Fezandipiti ex")
    BLANKS = ["Genesect", "Dedenne", "Fezandipiti ex", "Shaymin", "Boss's Orders", "Lana's Aid",
              "Eri", "Enhanced Hammer", "Sacred Ash", "Air Balloon", "Lucky Helmet", "Battle Cage",
              "Psychic Energy", "Enriching Energy"]
    NOTES = ["与原型完全相同的贪心打法；手牌数 = 回合结束时手牌 - 1（攻击前手贴一个超能量）。"]

    def initial_bench(self, g: Game) -> None:
        for c in list(g.hand):
            if c in ("Abra", "Dunsparce") and g.bench_room() > 0:
                g.bench_from_hand(c)

    def wants(self, g: Game) -> list[str]:
        out = []
        h = g.hand
        if g.count(*LINE) < 3 and "Abra" not in h:
            out.append("Abra")
        if g.turn >= 2 and "Alakazam" not in h and g.count("Alakazam") < 2:
            if ("Rare Candy" in h and g.evolvable("Abra")) or g.evolvable("Kadabra"):
                out.append("Alakazam")
        if g.count("Dunsparce", "Dudunsparce") == 0 and "Dunsparce" not in h:
            out.append("Dunsparce")
        if g.turn >= 2 and g.evolvable("Dunsparce") and "Dudunsparce" not in h:
            out.append("Dudunsparce")
        if g.turn >= 2 and g.evolvable("Abra") and "Kadabra" not in h and "Rare Candy" not in h:
            out.append("Kadabra")
        return out

    def step(self, g: Game) -> bool:
        h = g.hand
        my_first = g.turn == 1
        for c in ("Abra", "Dunsparce"):
            if c in h and g.bench_room() > 0 and (c != "Dunsparce" or g.count("Dunsparce", "Dudunsparce") < 2):
                g.bench_from_hand(c)
                return True
        if "Buddy-Buddy Poffin" in h and g.bench_room() > 0:
            g.play("Buddy-Buddy Poffin")
            for _ in range(2):
                line = g.count(*LINE)
                duns = g.count("Dunsparce", "Dudunsparce")
                want = "Abra" if line < 3 else ("Dunsparce" if duns == 0 else None)
                if want:
                    g.bench_from_deck(want)
            g.shuffle()
            return True
        if not g.attached and "Telepathic Psychic Energy" in h and g.mons(*LINE):
            g.attach(g.mons(*LINE)[0], "Telepathic Psychic Energy")
            for _ in range(2):
                g.bench_from_deck("Abra")
            g.shuffle()
            return True
        if not my_first:
            if "Alakazam" in h:
                if g.evolvable("Kadabra"):
                    g.evolve(g.evolvable("Kadabra")[0], "Alakazam")
                    g.draw(3)
                    return True
                if "Rare Candy" in h and g.evolvable("Abra"):
                    g.play("Rare Candy")
                    g.evolve(g.evolvable("Abra")[0], "Alakazam")
                    g.draw(3)
                    return True
            if "Kadabra" in h and g.evolvable("Abra") and not ("Rare Candy" in h and "Alakazam" in h):
                g.evolve(g.evolvable("Abra")[0], "Kadabra")
                g.draw(2)
                return True
            if "Dudunsparce" in h and g.evolvable("Dunsparce"):
                m = g.evolvable("Dunsparce")[0]
                h.remove("Dudunsparce")
                g.board.remove(m)          # Run Away Draw: draw 3, shuffle it back
                if not g.board:
                    from .core import Mon
                    g.board.append(Mon("(none)", 0))
                g.draw(3)
                g.deck += ["Dudunsparce", "Dunsparce"]
                g.shuffle()
                return True
        if "Poke Pad" in h:
            for w in self.wants(g):
                if g.search(w):
                    g.play("Poke Pad")
                    g.shuffle()
                    return True
        if g.can_supporter():
            missing = self.wants(g)
            if "Dawn" in h and missing:
                g.play_supporter("Dawn")
                for w in LINE:
                    g.search(w)
                g.shuffle()
                return True
            if "Hilda" in h and ("Alakazam" in missing or g.turn >= 2):
                g.play_supporter("Hilda")
                g.search("Alakazam" if g.turn >= 2 else "Kadabra")
                g.search("Telepathic Psychic Energy")
                g.shuffle()
                return True
        return False

    def measure(self, g: Game, t: int) -> dict:
        if t == 1:
            return {}
        n = g.count("Alakazam")
        out = {f"第{t}回合有 Alakazam": n >= 1}
        if t == 3:
            out["第3回合有 2 只 Alakazam"] = n >= 2
        if t in (2, 3):
            hand = len(g.hand) - 1 if n else None
            out[f"第{t}回合打出时手牌（均值）"] = hand
            if t == 3:
                out["第3回合手牌≥16（一击 Dragapult ex）"] = (hand >= 16) if n else None
        return out

    def tunings(self) -> list[dict]:
        return [{
            "question": "第 4 张 Rare Candy（换 1 张 Enhanced Hammer）",
            "source": "project-files/advisor/2026-10-05_模拟对战可行性.md 原型问题",
            "change": {"Rare Candy": +1, "Enhanced Hammer": -1},
        }]
