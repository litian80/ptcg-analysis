"""Goldfish Monte Carlo prototype: how often a deck sets up on its own, with no opponent.

Only answers "the deck's own probability" questions (opening hand, turn-2 Stage 2,
hand size when attacking). Interaction (opponent's item lock, hand disruption,
knockouts) is out of scope by design.

Prototype for one list: Alakazam Dudunsparce, Diego Cassiraga, Worlds 2026 2nd.
Card effects are the printed texts (MEG/PFL/WHT/POR/TEF/JTG); the play policy is a
simple greedy one written here, not a strong player.

    python -m ptcg.goldfish [games] [--candy N]
"""
from __future__ import annotations

import random
import sys
from collections import Counter

BASE_LIST = {
    # Pokemon
    "Abra": 4, "Kadabra": 4, "Alakazam": 3, "Dunsparce": 3, "Dudunsparce": 3,
    "Genesect": 2, "Dedenne": 1, "Fezandipiti ex": 1, "Shaymin": 1,
    # Supporters
    "Dawn": 4, "Hilda": 3, "Boss's Orders": 2, "Lana's Aid": 1, "Eri": 1,
    # Items / tools / stadium
    "Buddy-Buddy Poffin": 4, "Poke Pad": 4, "Rare Candy": 3, "Enhanced Hammer": 2,
    "Sacred Ash": 1, "Air Balloon": 2, "Lucky Helmet": 1, "Battle Cage": 4,
    # Energy
    "Telepathic Psychic Energy": 4, "Psychic Energy": 1, "Enriching Energy": 1,
}
BASICS = {"Abra", "Dunsparce", "Genesect", "Dedenne", "Fezandipiti ex", "Shaymin"}
SMALL_BASICS = {"Abra", "Dunsparce", "Dedenne", "Shaymin"}  # 70 HP or less (Poffin)
ENERGY = {"Telepathic Psychic Energy", "Psychic Energy", "Enriching Energy"}
BENCH_MAX = 5


class Game:
    def __init__(self, deck_list: dict[str, int], rng: random.Random, first: bool):
        self.rng = rng
        self.first = first
        self.deck = [c for c, n in deck_list.items() for _ in range(n)]
        assert len(self.deck) == 60, len(self.deck)
        self.mulligans = 0
        while True:
            rng.shuffle(self.deck)
            self.hand = self.deck[:7]
            if any(c in BASICS for c in self.hand):
                break
            self.mulligans += 1
        self.deck = self.deck[7:]
        self.prizes, self.deck = self.deck[:6], self.deck[6:]
        # board: list of [name, turn_put_in_play]; first entry is the Active
        active = self._pick_active()
        self.hand.remove(active)
        self.board = [[active, 0]]
        for c in [c for c in self.hand if c in SMALL_BASICS | {"Genesect"}]:
            if len(self.board) < 1 + BENCH_MAX and c in {"Abra", "Dunsparce"}:
                self.hand.remove(c)
                self.board.append([c, 0])
        self.turn = 0
        self.energy_attached = False

    def _pick_active(self) -> str:
        for pref in ("Dunsparce", "Shaymin", "Genesect", "Dedenne", "Abra", "Fezandipiti ex"):
            if pref in self.hand:
                return pref
        raise AssertionError

    # helpers
    def draw(self, n: int) -> None:
        for _ in range(n):
            if self.deck:
                self.hand.append(self.deck.pop())

    def search(self, wanted: str) -> bool:
        if wanted in self.deck:
            self.deck.remove(wanted)
            self.hand.append(wanted)
            return True
        return False

    def shuffle(self) -> None:
        self.rng.shuffle(self.deck)

    def count(self, name: str) -> int:
        return sum(1 for p in self.board if p[0] == name)

    def bench_room(self) -> int:
        return 1 + BENCH_MAX - len(self.board)

    def put(self, name: str) -> bool:
        if self.bench_room() > 0:
            self.board.append([name, self.turn])
            return True
        return False

    def evolvable(self, base: str) -> list[list]:
        return [p for p in self.board if p[0] == base and p[1] < self.turn]

    # one turn
    def play_turn(self) -> None:
        self.turn += 1
        my_first = self.turn == 1
        if not (my_first and self.first):
            self.draw(1)
        self.energy_attached = False
        self.supporter_used = my_first and self.first  # first player: no Supporter T1
        for _ in range(12):  # repeat until no progress
            if not self.step(my_first):
                break

    def wants(self) -> list[str]:
        """What the policy is missing, most important first."""
        out = []
        abras = self.count("Abra")
        if abras + self.count("Kadabra") + self.count("Alakazam") < 3 and "Abra" not in self.hand:
            out.append("Abra")
        if self.turn >= 2 and "Alakazam" not in self.hand and self.count("Alakazam") < 2:
            if ("Rare Candy" in self.hand and self.evolvable("Abra")) or self.evolvable("Kadabra"):
                out.append("Alakazam")
        if self.count("Dunsparce") + self.count("Dudunsparce") == 0 and "Dunsparce" not in self.hand:
            out.append("Dunsparce")
        if self.turn >= 2 and self.evolvable("Dunsparce") and "Dudunsparce" not in self.hand:
            out.append("Dudunsparce")
        if self.turn >= 2 and self.evolvable("Abra") and "Kadabra" not in self.hand and "Rare Candy" not in self.hand:
            out.append("Kadabra")
        return out

    def step(self, my_first: bool) -> bool:
        h = self.hand
        # 1. bench basics from hand
        for c in ("Abra", "Dunsparce"):
            if c in h and self.bench_room() > 0 and (c != "Dunsparce" or self.count("Dunsparce") + self.count("Dudunsparce") < 2):
                h.remove(c)
                self.put(c)
                return True
        # 2. Poffin
        if "Buddy-Buddy Poffin" in h and self.bench_room() > 0:
            h.remove("Buddy-Buddy Poffin")
            for _ in range(2):
                line = self.count("Abra") + self.count("Kadabra") + self.count("Alakazam")
                duns = self.count("Dunsparce") + self.count("Dudunsparce")
                want = "Abra" if line < 3 else ("Dunsparce" if duns == 0 else None)
                if want and want in self.deck and self.bench_room() > 0:
                    self.deck.remove(want)
                    self.put(want)
            self.shuffle()
            return True
        # 3. Telepathic energy on an Abra-line Pokemon (Psychic) -> bench up to 2 Abra
        if not self.energy_attached and "Telepathic Psychic Energy" in h and any(p[0] in ("Abra", "Kadabra", "Alakazam") for p in self.board):
            h.remove("Telepathic Psychic Energy")
            self.energy_attached = True
            for _ in range(2):
                if "Abra" in self.deck and self.bench_room() > 0:
                    self.deck.remove("Abra")
                    self.put("Abra")
            self.shuffle()
            return True
        # 4. Evolve (not on your first turn); each evolution draws
        if not my_first:
            if "Alakazam" in h:
                if self.evolvable("Kadabra"):
                    self.evolvable("Kadabra")[0][0] = "Alakazam"
                    h.remove("Alakazam"); self.draw(3); return True
                if "Rare Candy" in h and self.evolvable("Abra"):
                    p = self.evolvable("Abra")[0]
                    p[0] = "Alakazam"
                    h.remove("Alakazam"); h.remove("Rare Candy"); self.draw(3); return True
            if "Kadabra" in h and self.evolvable("Abra") and not ("Rare Candy" in h and "Alakazam" in h):
                p = self.evolvable("Abra")[0]
                p[0] = "Kadabra"; p[1] = self.turn
                h.remove("Kadabra"); self.draw(2); return True
            if "Dudunsparce" in h and self.evolvable("Dunsparce"):
                p = self.evolvable("Dunsparce")[0]
                h.remove("Dudunsparce")
                # Run Away Draw: draw 3, shuffle Dudunsparce back
                self.board.remove(p)
                if not self.board:
                    self.board.append(["(none)", 0])
                self.draw(3)
                self.deck += ["Dudunsparce", "Dunsparce"]
                self.shuffle()
                return True
        # 5. Poke Pad (non-rule-box Pokemon)
        if "Poke Pad" in h:
            for w in self.wants():
                if self.search(w):
                    h.remove("Poke Pad"); self.shuffle(); return True
        # 6. Supporter
        if not self.supporter_used:
            missing = self.wants()
            if "Dawn" in h and missing:
                h.remove("Dawn")
                self.supporter_used = True
                for w in ("Abra", "Kadabra", "Alakazam"):
                    self.search(w)
                self.shuffle()
                return True
            if "Hilda" in h and ("Alakazam" in missing or self.turn >= 2):
                h.remove("Hilda")
                self.supporter_used = True
                self.search("Alakazam" if self.turn >= 2 else "Kadabra")
                self.search("Telepathic Psychic Energy")
                self.shuffle()
                return True
        return False

    def alakazams(self) -> int:
        return self.count("Alakazam")


def run(games: int, deck_list: dict[str, int], seed: int = 1) -> dict:
    rng = random.Random(seed)
    res = {}
    for first in (True, False):
        c = Counter()
        hands = Counter()
        for _ in range(games):
            g = Game(deck_list, rng, first)
            c["mulligan"] += g.mulligans > 0
            for t in (1, 2, 3):
                g.play_turn()
                n = g.alakazams()
                c[f"t{t}_any"] += n >= 1
                c[f"t{t}_two"] += n >= 2
                if t in (2, 3) and n >= 1:
                    # hand after the turn's draws; a Psychic energy attaches from hand, so -1
                    hands[t] += len(g.hand) - 1
        res["先攻" if first else "后攻"] = {
            "第2回合有 Alakazam": c["t2_any"] / games,
            "第3回合有 Alakazam": c["t3_any"] / games,
            "第3回合有 2 只 Alakazam": c["t3_two"] / games,
            "第2回合打出时手牌（均值）": hands[2] / max(c["t2_any"], 1),
            "第3回合打出时手牌（均值）": hands[3] / max(c["t3_any"], 1),
            "起手重抽": c["mulligan"] / games,
        }
    return res


def main(argv: list[str]) -> None:
    games = int(argv[0]) if argv and argv[0].isdigit() else 20000
    deck = dict(BASE_LIST)
    if "--candy" in argv:
        n = int(argv[argv.index("--candy") + 1])
        deck["Rare Candy"] = n
        deck["Enhanced Hammer"] -= n - 3  # keep 60 cards
    for side, stats in run(games, deck).items():
        print(side)
        for k, v in stats.items():
            print(f"  {k}: {v:.1%}" if v <= 1 else f"  {k}: {v:.1f}")


if __name__ == "__main__":
    main(sys.argv[1:])
