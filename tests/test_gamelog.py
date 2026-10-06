"""ptcg.gamelog against three real TCG Live logs in data/gamelogs/logs."""
import pytest

from ptcg import gamelog
from ptcg.paths import DATA

RAW = DATA / "gamelogs" / "logs"


def load(name):
    return gamelog.parse((RAW / name).read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def g1():
    return load("2026-10-05_1_vs-dragapult-ex.txt")


@pytest.fixture(scope="module")
def g2():
    return load("2026-10-05_2_vs-lucario-hariyama.txt")


@pytest.fixture(scope="module")
def g3():
    return load("2026-10-05_3_vs-dragapult-ex.txt")


def test_players_order_and_perspective(g1, g2, g3):
    assert g1.players == ["Dakitigod", "Maxevil95"]
    assert g2.players == ["Maxevil95", "AkiraYoshioka"]
    # K3vlarUK won the toss and chose to go second.
    assert g3.players == ["Maxevil95", "K3vlarUK"]
    assert g3.coin_winner == "K3vlarUK"
    assert {g.perspective for g in (g1, g2, g3)} == {"Maxevil95"}
    assert g1.opening_hand[0] == "Rare Candy" and len(g1.opening_hand) == 7


def test_results(g1, g2, g3):
    assert (g1.winner, g1.end) == ("Maxevil95", "concede")
    assert (g2.winner, g2.end) == ("AkiraYoshioka", "concede")
    assert (g3.winner, g3.end) == ("Maxevil95", "prizes")
    assert g3.prizes_taken == {"K3vlarUK": 2, "Maxevil95": 6}
    assert g1.prizes_taken == {"Dakitigod": 3, "Maxevil95": 3}


def test_turns(g1, g3):
    assert len(g1.turns) == 12
    assert [t.player_turn for t in g1.turns[:4]] == [1, 1, 2, 2]
    assert g3.turns[0].player == "Maxevil95"


def test_counter_owner_is_resolved_from_the_board(g1, g3):
    # The client prints "Maxevil95 put 12 damage counters on Maxevil95's Drakloak".
    hs = gamelog.hand_sizes(g1)
    assert [(h["turn"], h["hand"], h["target_owner"], h["target"]) for h in hs] == [
        (6, 6, "Dakitigod", "Drakloak"), (10, 16, "Dakitigod", "Dragapult ex"), (12, 16, "Dakitigod", "Drakloak")]
    assert [h["hand"] for h in gamelog.hand_sizes(g3)] == [13, 12, 9, 20]
    # Phantom Dive's bench counters and Risky Ruins print the wrong owner too.
    dive = next(e for t in g3.turns for e in t.events if e.name == "Phantom Dive")
    assert [e["owner"] for e in dive.effects if "owner" in e] == ["Maxevil95", "Maxevil95"]
    ruins = next(e for t in g3.turns for e in t.events if e.kind == "activated" and e.card == "Risky Ruins"
                 and t.player == "Maxevil95")
    assert {e["owner"] for e in ruins.effects} == {"Maxevil95"}


def test_attacks_and_abilities(g1, g2):
    kinds = [(e.kind, e.card, e.name) for e in g1.turns[2].events if e.kind in ("used", "attack")]
    assert kinds == [("used", "Drakloak", "Recon Directive"), ("attack", "Budew", "Itchy Pollen")]
    last = [e for e in g2.turns[-1].events if e.kind in ("used", "attack")]
    # "Maxevil95 played Dudunsparce." is Run Away Draw, not an attack, even as the last action.
    assert [(e.kind, e.name) for e in last] == [("used", "Flip the Script"), ("used", "Run Away Draw")]
    assert not any(e.kind == "attack" for e in g2.turns[-1].events)


def test_seen_cards_are_attributed_to_their_owner(g2, g3):
    # Judge lists the cards Maxevil95 shuffled away; they are not AkiraYoshioka's.
    assert "Alakazam" not in g2.seen["AkiraYoshioka"]
    assert "Total damage: 100 damage" not in g2.seen["AkiraYoshioka"]
    assert "Special Red Card" in g3.seen["K3vlarUK"]
    assert "Battle Cage" in g3.seen["Maxevil95"]
    assert "Psychic Energy" in g3.seen["K3vlarUK"]  # printed "Basic Psychic Energy"


def test_archetype_guess(g1, g2, g3):
    assert gamelog.guess_archetype(g1.seen["Dakitigod"])[0][0] == "dragapult-ex"
    assert gamelog.guess_archetype(g2.seen["AkiraYoshioka"])[0][0] == "lucario-hariyama"
    assert gamelog.guess_archetype(g3.seen["K3vlarUK"])[0][0] == "dragapult-ex"
    assert gamelog.guess_archetype(g3.seen["Maxevil95"])[0][0] == "alakazam-dudunsparce"


def test_markdown_and_json(g3, tmp_path):
    md = gamelog.to_markdown(g3, "g3")
    assert "Powerful Hand 时手牌" in md and "| 11 | Maxevil95" in md
    assert '"winner": "Maxevil95"' in gamelog.to_json(g3)
    out = tmp_path / "out"
    assert gamelog.main([str(RAW / "2026-10-05_3_vs-dragapult-ex.txt"), "--out", str(out)]) == 0
    assert (out / "2026-10-05_3_vs-dragapult-ex.md").read_text(encoding="utf-8").startswith("# 2026-10-05_3")
