"""Shared goldfish core: deck, mulligan, prizes, draw/search, board and turn rules.

A goldfish game has no opponent. Rules enforced here:
- mulligan until the opening 7 has a Basic Pokemon; 6 prize cards;
- the player going first draws no card and can't play a Supporter or attack on turn 1;
- no evolution on a player's first turn, nor on a Pokemon put into play (or evolved)
  this turn; the same for Rare Candy (Deck.policies call ``can_evolve``);
- one manual Energy attachment, one Supporter, one Stadium and one retreat per turn;
- Bench of 5 (8 with Area Zero Underdepths and a Tera Pokemon in play).

The top of the deck is the END of ``Game.deck`` (``deck.pop()`` draws).
Card effects live in the deck modules; cards a deck doesn't model are blanks.
"""
from __future__ import annotations

import random
from collections import Counter
from dataclasses import dataclass


@dataclass(frozen=True)
class Card:
    name: str
    kind: str                 # pokemon / item / supporter / tool / stadium / energy
    stage: int = 0            # Pokemon: 0 basic, 1, 2
    evolves_from: str = ""
    hp: int = 0
    type: str = ""            # R fire, P psychic, D darkness, G grass, W water, L lightning, F fighting, M metal, N dragon, C colorless
    rulebox: bool = False
    tera: bool = False
    retreat: int = 0
    provides: str = ""        # Energy: type letter it provides
    basic_energy: bool = False


CARDS: dict[str, Card] = {}


def _pk(name, stage, hp, type_, retreat, evolves_from="", rulebox=False, tera=False):
    CARDS[name] = Card(name, "pokemon", stage, evolves_from, hp, type_, rulebox, tera, retreat)


def _tr(kind, *names):
    for n in names:
        CARDS[n] = Card(n, kind)


def _en(name, provides, basic=False):
    CARDS[name] = Card(name, "energy", provides=provides, basic_energy=basic)


# Pokemon (HP, type, retreat, evolution from the printed cards)
_pk("Abra", 0, 50, "P", 1)
_pk("Kadabra", 1, 80, "P", 1, "Abra")
_pk("Alakazam", 2, 140, "P", 1, "Kadabra")
_pk("Dunsparce", 0, 70, "C", 1)
_pk("Dudunsparce", 1, 140, "C", 3, "Dunsparce")
_pk("Genesect", 0, 110, "M", 2)          # SFA 40 (not re-fetched; Poffin can't take it)
_pk("Dedenne", 0, 70, "L", 1)
_pk("Fezandipiti ex", 0, 210, "D", 1, rulebox=True)
_pk("Shaymin", 0, 80, "G", 1)
_pk("Duskull", 0, 60, "P", 1)
_pk("Dusclops", 1, 90, "P", 2, "Duskull")
_pk("Dusknoir", 2, 160, "P", 3, "Dusclops")
_pk("Budew", 0, 30, "G", 0)
_pk("Dreepy", 0, 70, "N", 1)
_pk("Drakloak", 1, 90, "N", 1, "Dreepy")
_pk("Dragapult ex", 2, 320, "N", 1, "Drakloak", rulebox=True, tera=True)
_pk("Munkidori", 0, 110, "P", 1)
_pk("Meowth ex", 0, 170, "C", 1, rulebox=True)
_pk("Moltres", 0, 120, "R", 1)
_pk("Mega Kangaskhan ex", 0, 300, "C", 3, rulebox=True)
_pk("Teal Mask Ogerpon ex", 0, 210, "G", 1, rulebox=True, tera=True)
_pk("Wellspring Mask Ogerpon ex", 0, 210, "W", 1, rulebox=True, tera=True)
_pk("Latias ex", 0, 210, "P", 2, rulebox=True)
_pk("Lillie's Clefairy ex", 0, 190, "P", 1, rulebox=True)
_pk("Chien-Pao", 0, 120, "W", 1)
_pk("Raging Bolt ex", 0, 240, "N", 3, rulebox=True)
_pk("Iron Leaves ex", 0, 220, "G", 1, rulebox=True)
_pk("Maractus", 0, 110, "G", 2)
_pk("Dwebble", 0, 70, "G", 2)
_pk("Crustle", 1, 150, "G", 3, "Dwebble")
_pk("Slowpoke", 0, 80, "P", 2)
_pk("Slowking", 1, 120, "P", 3, "Slowpoke")
_pk("Kyurem", 0, 130, "N", 2)
_pk("Zeraora", 0, 100, "L", 1)
_pk("Metagross", 2, 180, "M", 3, "Metang")
_pk("Annihilape", 2, 150, "P", 2, "Primeape")
_pk("Pawmot", 2, 140, "L", 1, "Pawmo")
_pk("Mew ex", 0, 160, "P", 0, rulebox=True)

_tr("supporter", "Dawn", "Hilda", "Boss's Orders", "Lana's Aid", "Eri", "Gwynn",
    "Lillie's Determination", "Crispin", "Judge", "Rosa's Encouragement", "Cyrano",
    "Ciphermaniac's Codebreaking", "Xerosic's Machinations", "Team Rocket's Petrel",
    "Pokémon Center Lady", "Bianca's Devotion")
_tr("item", "Buddy-Buddy Poffin", "Poke Pad", "Rare Candy", "Enhanced Hammer", "Sacred Ash",
    "Strange Timepiece", "Special Red Card", "Night Stretcher", "Prime Catcher",
    "Crushing Hammer", "Ultra Ball", "Unfair Stamp", "Energy Switch", "Glass Trumpet",
    "Jumbo Ice Cream", "Pokégear 3.0", "Switch", "Wondrous Patch", "Secret Box")
_tr("tool", "Air Balloon", "Lucky Helmet", "Handheld Fan", "Hero's Cape")
_tr("stadium", "Battle Cage", "Team Rocket's Watchtower", "Risky Ruins", "Area Zero Underdepths",
    "Team Rocket's Factory", "Lumiose City", "Prism Tower", "Academy at Night", "Festival Grounds")
_en("Telepathic Psychic Energy", "P")
_en("Enriching Energy", "C")
_en("Psychic Energy", "P", True)
_en("Fire Energy", "R", True)
_en("Darkness Energy", "D", True)
_en("Grass Energy", "G", True)
_en("Lightning Energy", "L", True)
_en("Fighting Energy", "F", True)
_en("Water Energy", "W", True)
_en("Growing Grass Energy", "G")
_en("Mist Energy", "C")
_en("Spiky Energy", "C")
_en("Boomerang Energy", "C")


def card(name: str) -> Card:
    return CARDS[name]


def is_basic(name: str) -> bool:
    c = CARDS[name]
    return c.kind == "pokemon" and c.stage == 0


def can_pay(energies: list[str], cost: str) -> bool:
    """cost like 'PPC': specific letters first, then any energy for each C."""
    have = Counter(CARDS[e].provides for e in energies)
    need_c = 0
    for sym in cost:
        if sym == "C":
            need_c += 1
        elif have[sym] > 0:
            have[sym] -= 1
        else:
            return False
    return sum(have.values()) >= need_c


class Mon:
    __slots__ = ("name", "cards", "since", "energy", "tool", "used")

    def __init__(self, name: str, turn: int):
        self.name = name
        self.cards = [name]
        self.since = turn          # turn put into play or last evolved
        self.energy: list[str] = []
        self.tool: str | None = None
        self.used = False          # once-per-turn ability, reset each turn

    def __repr__(self):
        return f"{self.name}{self.energy or ''}"


class Game:
    def __init__(self, deck: "Deck", rng: random.Random, first: bool, deck_list: dict[str, int] | None = None):
        self.d = deck
        self.rng = rng
        self.first = first
        lst = deck_list if deck_list is not None else deck.LIST
        self.deck = [c for c, n in lst.items() for _ in range(n)]
        assert len(self.deck) == 60, (deck.SLUG, len(self.deck))
        self.mulligans = 0
        while True:
            rng.shuffle(self.deck)
            self.hand = self.deck[:7]
            if any(is_basic(c) for c in self.hand):
                break
            self.mulligans += 1
        self.deck = self.deck[7:]
        self.prizes, self.deck = self.deck[:6], self.deck[6:]
        self.opening = list(self.hand)
        self.discard: list[str] = []
        self.stadium: str | None = None
        self.turn = 0
        self.board: list[Mon] = []
        self.flags: dict = {}
        self.attached = self.supporter_used = self.retreated = self.stadium_played = False
        self.attacked = False
        active = deck.choose_active(self)
        self.hand.remove(active)
        self.board.append(Mon(active, 0))
        deck.initial_bench(self)

    # ---- board -------------------------------------------------------
    @property
    def active(self) -> Mon:
        return self.board[0]

    @property
    def bench(self) -> list[Mon]:
        return self.board[1:]

    def bench_max(self) -> int:
        if self.stadium == "Area Zero Underdepths" and any(CARDS[m.name].tera for m in self.board):
            return 8
        return 5

    def bench_room(self) -> int:
        return 1 + self.bench_max() - len(self.board)

    def mons(self, *names: str) -> list[Mon]:
        return [m for m in self.board if m.name in names]

    def count(self, *names: str) -> int:
        return sum(1 for m in self.board if m.name in names)

    def put(self, name: str) -> Mon | None:
        """Put a Basic onto the Bench (the card must already be out of hand/deck)."""
        if self.bench_room() <= 0:
            return None
        m = Mon(name, self.turn)
        self.board.append(m)
        return m

    def bench_from_hand(self, name: str) -> Mon | None:
        if name in self.hand and self.bench_room() > 0:
            self.hand.remove(name)
            return self.put(name)
        return None

    def bench_from_deck(self, name: str) -> Mon | None:
        if name in self.deck and self.bench_room() > 0:
            self.deck.remove(name)
            return self.put(name)
        return None

    def can_evolve(self, m: Mon) -> bool:
        return self.turn > 1 and m.since < self.turn

    def evolvable(self, base: str) -> list[Mon]:
        return [m for m in self.board if m.name == base and self.can_evolve(m)]

    def evolve(self, m: Mon, into: str, from_hand: bool = True) -> None:
        if from_hand:
            self.hand.remove(into)
        m.name = into
        m.cards.append(into)
        m.since = self.turn

    # ---- cards -------------------------------------------------------
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

    def play(self, name: str) -> None:
        """Play an Item/Supporter from hand to the discard pile."""
        self.hand.remove(name)
        self.discard.append(name)

    def can_supporter(self) -> bool:
        return not self.supporter_used and not (self.first and self.turn == 1)

    def play_supporter(self, name: str) -> bool:
        if name not in self.hand or not self.can_supporter():
            return False
        self.play(name)
        self.supporter_used = True
        return True

    def play_stadium(self, name: str) -> bool:
        if name not in self.hand or self.stadium_played or self.stadium == name:
            return False
        self.hand.remove(name)
        if self.stadium:
            self.discard.append(self.stadium)
        self.stadium = name
        self.stadium_played = True
        return True

    def attach(self, m: Mon, energy: str) -> bool:
        """Manual attachment from hand (once per turn)."""
        if self.attached or energy not in self.hand:
            return False
        self.hand.remove(energy)
        m.energy.append(energy)
        self.attached = True
        return True

    def can_attack(self) -> bool:
        return not (self.first and self.turn == 1) and not self.attacked

    def retreat_cost(self, m: Mon) -> int:
        c = CARDS[m.name]
        if c.stage == 0 and self.count("Latias ex"):
            return 0
        cost = c.retreat
        if m.tool == "Air Balloon":
            cost -= 2
        return max(cost, 0)

    def can_pivot(self, m: Mon) -> bool:
        if m is self.active:
            return True
        if any(c in self.hand for c in self.d.PIVOTS):
            return True
        return not self.retreated and len(self.active.energy) >= self.retreat_cost(self.active)

    def pivot(self, m: Mon) -> bool:
        """Make m the Active: free retreat, else a switching card, else pay the retreat."""
        if m is self.active:
            return True
        i = self.board.index(m)
        cost = self.retreat_cost(self.active)
        item = next((c for c in self.d.PIVOTS if c in self.hand), None)
        if not self.retreated and cost == 0:
            self.retreated = True
        elif item:
            self.play(item)
        elif not self.retreated and len(self.active.energy) >= cost:
            for _ in range(cost):
                self.discard.append(self.active.energy.pop())
            self.retreated = True
        else:
            return False
        self.board[0], self.board[i] = self.board[i], self.board[0]
        return True

    def ready(self, m: Mon, cost: str) -> bool:
        """m could attack now with an attack costing `cost`."""
        return self.can_attack() and can_pay(m.energy, cost) and self.can_pivot(m)

    def can_go(self, m: Mon, cost: str) -> bool:
        """Like go() but without changing anything."""
        if not self.can_attack() or not can_pay(m.energy, cost):
            return False
        if self.can_pivot(m):
            return True
        return not self.attached and not self.retreated and \
            self.retreat_cost(self.active) - len(self.active.energy) == 1 and \
            any(CARDS[c].kind == "energy" for c in self.hand)

    def go(self, m: Mon, cost: str) -> bool:
        """End of turn: if m can pay `cost`, get it Active (attaching an Energy to the Active to
        pay its retreat if that's the only thing missing) and mark the attack. Returns success."""
        if not self.can_attack() or not can_pay(m.energy, cost):
            return False
        if not self.can_pivot(m) and not self.attached and not self.retreated:
            short = self.retreat_cost(self.active) - len(self.active.energy)
            e = next((c for c in self.hand if CARDS[c].kind == "energy"), None)
            if short == 1 and e:
                self.attach(self.active, e)
        if not self.pivot(m):
            return False
        self.attacked = True
        return True

    def take_discards(self, n: int, junk: list[str], keep: set[str] = frozenset()) -> list[str] | None:
        """Pick n cards to discard from hand following `junk` order (then any card not in keep)."""
        pool = list(self.hand)
        out = []
        for j in junk:
            while j in pool and len(out) < n:
                pool.remove(j)
                out.append(j)
        for c in list(pool):
            if len(out) >= n:
                break
            if c not in keep:
                pool.remove(c)
                out.append(c)
        return out if len(out) == n else None

    def ultra_ball(self, target: str, junk: list[str], keep: set[str] = frozenset()) -> bool:
        """Ultra Ball (MEG 131): discard 2 other cards, search a Pokemon."""
        if "Ultra Ball" not in self.hand or target not in self.deck:
            return False
        self.hand.remove("Ultra Ball")
        disc = self.take_discards(2, junk, keep | {target})
        if disc is None:
            self.hand.append("Ultra Ball")
            return False
        self.discard.append("Ultra Ball")
        for c in disc:
            self.hand.remove(c)
            self.discard.append(c)
        self.search(target)
        self.shuffle()
        return True

    def poke_pad(self, wants: list[str]) -> bool:
        """Poke Pad (POR 81): a Pokemon without a Rule Box."""
        if "Poke Pad" not in self.hand:
            return False
        for w in wants:
            if not CARDS[w].rulebox and self.search(w):
                self.play("Poke Pad")
                self.shuffle()
                return True
        return False

    def lillies(self) -> bool:
        """Lillie's Determination (MEG 119): shuffle hand in, draw 8 (6 prizes left in a goldfish)."""
        if not self.play_supporter("Lillie's Determination"):
            return False
        self.deck += self.hand
        self.hand.clear()
        self.shuffle()
        self.draw(8 if len(self.prizes) == 6 else 6)
        return True

    # ---- turn --------------------------------------------------------
    def play_turn(self) -> None:
        self.turn += 1
        if not (self.first and self.turn == 1):
            self.draw(1)
        self.attached = self.supporter_used = self.retreated = self.stadium_played = False
        self.attacked = False
        for m in self.board:
            m.used = False
        self.d.turn(self)


class Deck:
    """One deck: its list, the effects that matter for setup, a greedy policy and metrics."""
    SLUG = ""
    NAME = ""
    SOURCE = ""               # where the list comes from
    LIST: dict[str, int] = {}
    TURNS = 4                 # own turns simulated
    BLANKS: list[str] = []    # cards in the list whose effects aren't modelled
    NOTES: list[str] = []
    STEP_LIMIT = 30
    PIVOTS: tuple[str, ...] = ("Switch",)   # cards that switch your Active for free

    def __init__(self, **opts):
        self.opts = opts

    # policy hooks
    def choose_active(self, g: Game) -> str:
        for pref in self.ACTIVE_PREF:
            if pref in g.hand:
                return pref
        return next(c for c in g.hand if is_basic(c))

    ACTIVE_PREF: tuple[str, ...] = ()

    def initial_bench(self, g: Game) -> None:
        pass

    def turn(self, g: Game) -> None:
        for _ in range(self.STEP_LIMIT):
            if g.flags.get("turn_over") or not self.step(g):
                break
        if not g.flags.pop("turn_over", False):
            self.end_turn(g)

    def step(self, g: Game) -> bool:
        return False

    def end_turn(self, g: Game) -> None:
        pass

    def measure(self, g: Game, t: int) -> dict:
        return {}

    def tunings(self) -> list[dict]:
        """List-tuning questions: [{"question", "source", "change": {card: +/-n}}]."""
        return []


def modified(base: dict[str, int], change: dict[str, int]) -> dict[str, int]:
    out = dict(base)
    for c, n in change.items():
        out[c] = out.get(c, 0) + n
        if out[c] <= 0:
            del out[c]
    assert sum(out.values()) == 60, change
    return out


def simulate(deck: Deck, games: int, seed: int = 1, deck_list: dict[str, int] | None = None) -> dict:
    """Run `games` goldfish games going first and second; return {side: {metric: value}}."""
    res = {}
    for first in (True, False):
        # one RNG per game (common random numbers): list variants start from comparable shuffles
        base = seed * 10_000_000 + (0 if first else 5_000_000)
        sums: dict[str, float] = {}
        cnts: dict[str, int] = {}
        for i in range(games):
            g = Game(deck, random.Random(base + i), first, deck_list)
            rows = {"起手重抽": g.mulligans > 0}
            for t in range(1, deck.TURNS + 1):
                g.play_turn()
                rows.update(deck.measure(g, t))
            for k, v in rows.items():
                if k not in sums:
                    sums[k], cnts[k] = 0.0, 0
                if v is None:
                    continue
                sums[k] += float(v)
                cnts[k] += 1
        out = {}
        for k in sums:
            if k == "起手重抽":
                continue
            out[k] = round(sums[k] / cnts[k], 4) if cnts[k] else None
        out["起手重抽"] = round(sums["起手重抽"] / games, 4)
        res["先攻" if first else "后攻"] = out
    return res
