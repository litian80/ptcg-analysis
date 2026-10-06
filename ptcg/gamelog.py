"""Parse Pokémon TCG Live game logs (the text the client copies with "Copy game log").

    python -m ptcg.gamelog LOG [LOG ...]            # markdown timeline of each game
    python -m ptcg.gamelog LOG --json               # the parsed game as JSON
    python -m ptcg.gamelog LOG --out DIR            # write <DIR>/<log name>.md instead

A log is a "Setup" block followed by one "<player>'s Turn" block per turn. Inside a block,
lines at the top level are actions, "- " lines are what the action above did, and "   • "
lines list the cards those effects revealed. Only the player who copied the log sees their
own hidden cards (opening hand, card names they drew), so that player is the log's
"perspective"; for the opponent the log says only "drew a card".

Known quirks of the client's text, which the parser works around:
- Lines that place damage counters name the wrong owner: Alakazam's Powerful Hand prints
  "Maxevil95 put 12 damage counters on Maxevil95's Drakloak" when the Drakloak is the
  opponent's. The owner is resolved from the Pokémon each player has in play.
- "X's Turn" uses an ASCII apostrophe, "on X’s Psyduck" a typographic one.
- Dudunsparce's Run Away Draw sometimes prints as a bare "X played Dudunsparce."
- Basic Energy is printed "Basic Psychic Energy"; data/cards calls it "Psychic Energy".
"""
from __future__ import annotations

import argparse
import collections
import dataclasses
import functools
import json
import pathlib
import re
import sys

from .paths import DATA

TURN_RE = re.compile(r"^(?P<p>.+)'s Turn$")
# Pokémon whose "played X." line is an Ability rather than playing a card.
ABILITY_PLAYED = {"Dudunsparce": "Run Away Draw"}


@dataclasses.dataclass
class Event:
    kind: str                     # see _classify for the list
    player: str | None            # who acted (None for "Handheld Fan was activated." etc.)
    text: str                     # the top-level line
    card: str | None = None       # the card played / the Pokémon that used something
    name: str | None = None       # attack or Ability name; evolution target
    target: str | None = None     # the Pokémon hit / switched in
    target_owner: str | None = None
    damage: int | None = None
    counters: int | None = None   # damage counters placed by this event's effects
    cards: list[str] = dataclasses.field(default_factory=list)   # all cards revealed under it
    effects: list[dict] = dataclasses.field(default_factory=list)  # its "- " lines: {text, cards}


@dataclasses.dataclass
class Turn:
    number: int        # 1, 2, 3 ... across both players
    player: str
    player_turn: int   # that player's 1st, 2nd ... turn
    events: list[Event] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class Game:
    players: list[str]             # [first, second]
    perspective: str | None        # the player who copied the log
    coin_winner: str | None
    opening_hand: list[str]        # perspective player's, if shown
    setup: list[Event]
    turns: list[Turn]
    winner: str | None
    end: str | None                # "prizes", "concede", "deck-out", "no-pokemon" or the raw line
    prizes_taken: dict[str, int]
    knockouts: list[dict]          # {turn, player (owner), card, by}
    seen: dict[str, list[str]]     # every card name seen for each player, in order, deduplicated

    def opponent(self, player: str | None = None) -> str | None:
        p = player or self.perspective
        others = [x for x in self.players if x != p]
        return others[0] if others else None


def card_name(s: str) -> str:
    s = s.strip().rstrip(".")
    m = re.fullmatch(r"Basic (\w+) Energy", s)
    return f"{m.group(1)} Energy" if m else s


def _norm(line: str) -> str:
    return line.replace("’", "'").rstrip()


def _blocks(text: str) -> list[tuple[str, list[tuple[str, list[str]]]]]:
    """[(header, [(action line, [sub lines incl. bullets])])]; header is "Setup" or a turn line."""
    blocks: list = []
    for raw in text.splitlines():
        line = _norm(raw)
        if not line.strip():
            continue
        if line == "Setup" or TURN_RE.match(line):
            blocks.append((line, []))
            continue
        if not blocks:
            blocks.append(("Setup", []))
        actions = blocks[-1][1]
        if line.startswith("- ") or line.lstrip().startswith("•"):
            if actions:
                actions[-1][1].append(line)
            continue
        actions.append((line, []))
    return blocks


def _effects(sub: list[str]) -> list[dict]:
    """The "- " lines under an action, each with the cards its "•" lines listed."""
    out: list[dict] = []
    for s in sub:
        s = s.strip()
        if s.startswith("- "):
            out.append({"text": s[2:], "cards": []})
        elif s.startswith("•") and out and not out[-1]["text"].startswith("Damage breakdown"):
            out[-1]["cards"].extend(card_name(c) for c in s.lstrip("• ").split(", ") if c)
    return out


class _Board:
    """Names of the Pokémon each player has in play; only used to resolve owners."""

    def __init__(self):
        self.inplay: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)

    def add(self, p, card):
        self.inplay[p][card] += 1

    def remove(self, p, card):
        if self.inplay[p][card] > 0:
            self.inplay[p][card] -= 1

    def evolve(self, p, frm, to):
        self.remove(p, frm)
        self.add(p, to)

    def owner(self, card, printed, actor, players, attack: bool) -> str:
        have = [p for p in players if self.inplay[p][card] > 0]
        if len(have) == 1:
            return have[0]
        if attack and actor in players:
            return next((p for p in players if p != actor), printed)
        return printed


_P = r"(?P<p>.+?)"
_C = r"(?P<card>.+?)"
PATTERNS = [
    ("coin_call", re.compile(rf"^{_P} chose (heads|tails) for the opening coin flip\.$")),
    ("coin_win", re.compile(rf"^{_P} won the coin toss\.$")),
    ("choose_order", re.compile(rf"^{_P} decided to go (?P<name>first|second)\.$")),
    ("opening_hand", re.compile(rf"^{_P} drew 7 cards for the opening hand\.$")),
    ("mulligan", re.compile(rf"^{_P} took a mulligan.*$")),
    ("draw", re.compile(rf"^{_P} drew (?P<card>a card|.+?)\.$")),
    ("play_pokemon", re.compile(rf"^{_P} played {_C} to the (?P<name>Active Spot|Bench)\.$")),
    ("stadium", re.compile(rf"^{_P} played {_C} to the Stadium spot\.$")),
    ("evolve", re.compile(rf"^{_P} evolved {_C} to (?P<name>.+?) (?:in the Active Spot|on the Bench)\.$")),
    ("attach", re.compile(rf"^{_P} attached {_C} to (?P<target>.+?) (?:in the Active Spot|on the Bench)\.$")),
    ("retreat", re.compile(rf"^{_P} retreated {_C} to the Bench\.$")),
    ("promote", re.compile(rf"^{_P}'s {_C} is now in the Active Spot\.$")),
    ("attack_hit", re.compile(rf"^{_P}'s {_C} used (?P<name>.+?) on (?P<owner>.+?)'s (?P<target>.+?) "
                              r"for (?P<damage>\d+) damage\..*$")),
    ("used", re.compile(rf"^{_P}'s {_C} used (?P<name>.+?)\.$")),
    ("knockout", re.compile(rf"^{_P}'s {_C} was Knocked Out!$")),
    ("prize", re.compile(rf"^{_P} took (?P<damage>a|\d+) Prize cards?\.$")),
    ("prize_card", re.compile(rf"^(?:A card|{_C}) was added to (?P<p>.+?)'s hand\.$")),
    ("activated", re.compile(rf"^{_C} was activated\.$")),
    ("discard_from", re.compile(rf"^{_C} was discarded from (?P<p>.+?)'s (?P<target>.+?)\.$")),
    ("end_turn", re.compile(rf"^{_P} ended their turn\.$")),
    ("play", re.compile(rf"^{_P} played {_C}\.$")),
]
END_RES = [
    ("prizes", re.compile(r"^All Prize cards taken\. (?P<w>.+) wins\.$")),
    ("concede", re.compile(r"^(?:Opponent|You) conceded\. (?P<w>.+) wins\.$")),
    ("deck-out", re.compile(r"^.*(?:deck|cards to draw).* (?P<w>.+) wins\.$")),
    ("no-pokemon", re.compile(r"^.*no Pokémon.* (?P<w>.+) wins\.$")),
    ("other", re.compile(r"^.* (?P<w>\S+) wins\.$")),
]
COUNTERS_RE = re.compile(r"^- (?P<p>.+?) put (?P<n>\d+|a) damage counters? on (?P<owner>.+?)'s (?P<card>.+?)\.$")


def _classify(line: str) -> tuple[str, dict]:
    for kind, rx in PATTERNS:
        m = rx.match(line)
        if m:
            return kind, m.groupdict()
    return "other", {}


def parse(text: str) -> Game:
    blocks = _blocks(text)
    board = _Board()
    players: list[str] = []
    first = coin = winner = end = perspective = None
    opening: list[str] = []
    setup: list[Event] = []
    turns: list[Turn] = []
    prizes: dict[str, int] = collections.Counter()
    kos: list[dict] = []
    seen: dict[str, dict[str, None]] = collections.defaultdict(dict)

    def see(p, *names):
        if p:
            for n in names:
                if n and n != "a card":
                    seen[p].setdefault(card_name(n), None)

    def player(p):
        if p and p not in players and len(players) < 2:
            players.append(p)

    per_player = collections.Counter()
    for header, actions in blocks:
        turn = None
        if header != "Setup":
            tp = TURN_RE.match(header).group("p")
            player(tp)
            per_player[tp] += 1
            turn = Turn(len(turns) + 1, tp, per_player[tp])
            turns.append(turn)
        for line, sub in actions:
            done = next(((k, rx.match(line)) for k, rx in END_RES if rx.match(line)), None)
            if done:
                end, winner = done[0], done[1].group("w")
                if line.startswith("You conceded"):
                    perspective = perspective or next((p for p in players if p != winner), None)
                ev = Event("game_end", None, line, name=end)
                (turn.events if turn else setup).append(ev)
                continue
            kind, g = _classify(line)
            p = g.get("p")
            if kind not in ("prize_card", "activated", "discard_from"):
                player(p)
            card = card_name(g["card"]) if g.get("card") else None
            effects = _effects(sub)
            ev = Event(kind, p, line, card=card, effects=effects, cards=[c for e in effects for c in e["cards"]])
            if kind == "coin_win":
                coin = p
            elif kind == "choose_order":
                first = p if g["name"] == "first" else None
                if g["name"] == "second":
                    first = ("second", p)
            elif kind == "opening_hand":
                if ev.cards:
                    perspective, opening = p, ev.cards
            elif kind == "draw" and card and card != "a card" and card != "7 cards for the opening hand":
                if turn and p == turn.player and line.endswith(f"drew {g['card']}."):
                    perspective = perspective or p
            elif kind == "play_pokemon":
                board.add(p, card)
                ev.name = g["name"]
            elif kind == "evolve":
                ev.name = card_name(g["name"])
                board.evolve(p, card, ev.name)
            elif kind == "attach":
                ev.target = card_name(g["target"])
            elif kind == "promote":
                ev.target = card
            elif kind == "knockout":
                board.remove(p, card)
                kos.append({"turn": turn.number if turn else 0, "player": p, "card": card,
                            "by": turn.player if turn else None})
            elif kind == "prize":
                n = 1 if g["damage"] == "a" else int(g["damage"])
                prizes[p] += n
                ev.damage = n
            elif kind == "prize_card":
                ev.player = g["p"]
                ev.card = card  # None when hidden
            elif kind == "discard_from":
                ev.player = g["p"]
                ev.target = card_name(g["target"])
            elif kind == "play" and card in ABILITY_PLAYED:
                kind = ev.kind = "used"
                ev.name = ABILITY_PLAYED[card]
            elif kind in ("attack_hit", "used"):
                ev.name = g["name"]
                if kind == "attack_hit":
                    ev.damage = int(g["damage"])
                    ev.target = card_name(g["target"])
                    ev.target_owner = board.owner(ev.target, g["owner"], p, players, attack=True)

            # Sub-lines: Pokémon that came into play, evolutions under Rare Candy, counters placed,
            # Run Away Draw / Switch effects that take a Pokémon off the board.
            for eff in effects:
                s = "- " + eff["text"]
                m = re.match(r"^- (.+?) drew (?:(\d+) cards|(.+?)) and played (?:them|it) to the Bench\.$", s)
                if m:
                    names = eff["cards"] if m.group(2) else [card_name(m.group(3))]
                    for n in names:
                        board.add(m.group(1), n)
                    continue
                m = re.match(r"^- (.+?) evolved (.+?) to (.+?) (?:in the Active Spot|on the Bench)\.$", s)
                if m:
                    board.evolve(m.group(1), card_name(m.group(2)), card_name(m.group(3)))
                    ev.name = ev.name or card_name(m.group(3))
                    see(m.group(1), m.group(2), m.group(3))
                    continue
                m = COUNTERS_RE.match(s)
                if m:
                    n = 1 if m.group("n") == "a" else int(m.group("n"))
                    ev.counters = (ev.counters or 0) + n
                    is_attack = kind in ("attack_hit", "used")
                    owner = board.owner(card_name(m.group("card")), m.group("owner"), m.group("p"), players,
                                        attack=is_attack)
                    eff["text"] = (f"{m.group('p')} put {n} damage counter{'s' if n > 1 else ''} on "
                                   f"{owner}'s {card_name(m.group('card'))}.")
                    eff["owner"] = owner
                    if kind == "used" and ev.target is None:
                        ev.target, ev.target_owner = card_name(m.group("card")), owner
            if kind == "used" and ev.name == "Run Away Draw" and "Dudunsparce" in ev.cards:
                board.remove(p, "Dudunsparce")

            # Card names this event shows for each player.
            if kind in ("play_pokemon", "stadium", "evolve", "attach", "play", "used", "attack_hit",
                        "retreat", "promote"):
                see(p, card, ev.name if kind == "evolve" else None, ev.target if kind == "attach" else None)
            if kind == "draw" and card and not card.startswith("7 cards"):
                see(p, card)
            if kind in ("discard_from", "knockout"):
                see(ev.player, card, ev.target)
            if kind == "prize_card" and card:
                see(g["p"], card)
            for eff in effects:
                if eff["cards"]:
                    m = re.match(r"^(.+?) (?:drew|discarded|shuffled|moved|put)\b", eff["text"])
                    see(m.group(1) if m and m.group(1) in players else (ev.player or p), *eff["cards"])
            (turn.events if turn else setup).append(ev)

    # The last "used" in a turn is an attack when nothing but its results follows it.
    for t in turns:
        for i in range(len(t.events) - 1, -1, -1):
            ev = t.events[i]
            if ev.kind in ("attack_hit",):
                break
            if ev.kind in ("end_turn", "play", "play_pokemon", "attach", "evolve", "retreat", "stadium"):
                break
            if ev.kind == "used" and ev.player == t.player and "'s " in ev.text:
                ev.kind = "attack"
                break
        for ev in t.events:
            if ev.kind == "attack_hit":
                ev.kind = "attack"

    if isinstance(first, tuple):
        first = next((p for p in players if p != first[1]), None)
    first = first or (turns[0].player if turns else None)
    if first and players and players[0] != first:
        players.reverse()
    if perspective is None and turns:
        for t in turns:
            for ev in t.events:
                if ev.kind == "draw" and ev.card not in (None, "a card") and ev.player == t.player:
                    perspective = ev.player
                    break
            if perspective:
                break
    return Game(players, perspective, coin, opening, setup, turns, winner, end, dict(prizes), kos,
                {p: list(v) for p, v in seen.items()})


# ---------------------------------------------------------------------------------------------
# Deck guess and summaries

@functools.cache
def _meta(window: str) -> dict:
    return json.loads((DATA / "archetypes" / f"meta_{window}.json").read_text(encoding="utf-8"))


def guess_archetype(cards: list[str], window: str = "TEF-30C") -> list[tuple[str, float]]:
    """Archetypes ranked by how well the seen cards match their core lists.

    Each core card scores in_lists / (number of archetypes whose core has it), so signature
    cards (Makuhita, Dreepy) count far more than staples (Boss's Orders, Meowth ex).
    """
    arch = _meta(window)["archetypes"]
    holders = collections.Counter(c["name"] for a in arch.values() for c in a.get("core", []))
    seen = set(cards)
    scores = []
    for slug, a in arch.items():
        core = a.get("core", [])
        total = sum(c["in_lists"] / holders[c["name"]] for c in core) or 1
        hit = sum(c["in_lists"] / holders[c["name"]] for c in core if c["name"] in seen)
        scores.append((slug, round(hit / total, 3)))
    return sorted(scores, key=lambda x: -x[1])


def hand_sizes(game: Game, card: str = "Alakazam", attack: str = "Powerful Hand") -> list[dict]:
    """Hand size at each Powerful Hand: it places 2 counters per card in hand."""
    out = []
    for t in game.turns:
        for ev in t.events:
            if ev.card == card and ev.name == attack and ev.counters:
                out.append({"turn": t.number, "player": ev.player, "hand": ev.counters // 2,
                            "target": ev.target, "target_owner": ev.target_owner})
    return out


SKIP = {"draw", "end_turn", "prize_card", "activated", "discard_from", "other", "promote"}


def _short(ev: Event) -> str | None:
    k = ev.kind
    if k in SKIP:
        return None
    if k == "play_pokemon":
        return f"{ev.card} 上{'场' if ev.name == 'Active Spot' else '后备区'}"
    first = next((e["cards"] for e in ev.effects if e["cards"]), [])
    if k == "play":
        extra = f"（{', '.join(first)}）" if first else ""
        return f"{ev.card}{extra}"
    if k == "stadium":
        return f"场地 {ev.card}"
    if k == "evolve":
        return f"{ev.card} → {ev.name}"
    if k == "attach":
        return f"{ev.card} 贴 {ev.target}"
    if k == "retreat":
        return f"{ev.card} 撤退"
    if k == "used":
        return f"{ev.card} 特性 {ev.name}" + (f"（{', '.join(first)}）" if first else "")
    if k == "attack":
        s = f"**{ev.card} {ev.name}**"
        if ev.target:
            s += f" → {ev.target}"
        if ev.damage is not None:
            s += f" {ev.damage}"
        if ev.counters:
            s += f"（放 {ev.counters} 个指示物）"
        return s
    if k == "knockout":
        return f"**{ev.player} 的 {ev.card} 被击倒**"
    if k == "prize":
        return f"{ev.player} 拿 {ev.damage} 张奖赏卡"
    if k == "game_end":
        return f"**{ev.text}**"
    if k in ("coin_call", "coin_win", "choose_order", "opening_hand", "mulligan"):
        return ev.text
    return ev.text


def to_markdown(game: Game, title: str = "") -> str:
    me = game.perspective
    opp = game.opponent()
    lines = [f"# {title or 'Game log'}", ""]
    lines.append(f"- 先攻：{game.players[0] if game.players else '?'}；"
                 f"视角：{me or '未知'}；胜者：{game.winner or '未结束'}（{game.end or '-'}）")
    lines.append(f"- 奖赏卡：" + "，".join(f"{p} 拿 {game.prizes_taken.get(p, 0)}" for p in game.players))
    if opp and game.seen.get(opp):
        top = guess_archetype(game.seen[opp])[:3]
        lines.append(f"- 对手卡组推测：" + "，".join(f"{s}（{v:.0%}）" for s, v in top))
        lines.append(f"- 对手亮出的牌：{', '.join(game.seen[opp])}")
    if game.opening_hand:
        lines.append(f"- {me} 起手：{', '.join(game.opening_hand)}")
    hs = hand_sizes(game)
    if hs:
        lines.append("- Powerful Hand 时手牌：" + "，".join(
            f"T{h['turn']} {h['player']} {h['hand']} 张 → {h['target_owner']} 的 {h['target']}" for h in hs))
    lines += ["", "| 回合 | 玩家 | 关键动作 |", "|---|---|---|"]
    for t in game.turns:
        acts = [s for s in (_short(e) for e in t.events) if s]
        lines.append(f"| {t.number} | {t.player}（第 {t.player_turn} 回合） | {'；'.join(acts) or '-'} |")
    lines.append("")
    return "\n".join(lines)


def to_json(game: Game) -> str:
    return json.dumps(dataclasses.asdict(game), ensure_ascii=False, indent=1)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python -m ptcg.gamelog")
    ap.add_argument("logs", nargs="+", type=pathlib.Path)
    ap.add_argument("--json", action="store_true", help="print the parsed game as JSON")
    ap.add_argument("--out", type=pathlib.Path, help="write one <name>.md (or .json) per log here")
    args = ap.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    for path in args.logs:
        game = parse(path.read_text(encoding="utf-8-sig"))
        text = to_json(game) if args.json else to_markdown(game, path.stem)
        if args.out:
            args.out.mkdir(parents=True, exist_ok=True)
            dest = args.out / f"{path.stem}.{'json' if args.json else 'md'}"
            dest.write_text(text, encoding="utf-8")
            print(dest)
        else:
            print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
