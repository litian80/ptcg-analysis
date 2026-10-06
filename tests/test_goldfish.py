import random

import pytest

from ptcg import goldfish
from ptcg.goldfish import DECKS, core, run_deck


@pytest.mark.parametrize("slug", list(DECKS))
def test_lists_are_60_and_cards_known(slug):
    deck = DECKS[slug]
    assert sum(deck.LIST.values()) == 60
    assert all(c in core.CARDS for c in deck.LIST)
    for t in deck().tunings():
        core.modified(deck.LIST, t.get("change") or {})  # still 60 cards


@pytest.mark.parametrize("slug", list(DECKS))
def test_rates_are_sane(slug):
    res = run_deck(slug, 150, seed=3)
    for side in res.values():
        for k, v in side.items():
            if v is not None and "均值" not in k:
                assert 0 <= v <= 1, (k, v)


def test_alakazam_dudunsparce_matches_prototype_shape():
    res = run_deck("alakazam-dudunsparce", 400, seed=3)
    for side in res.values():
        assert 0 < side["第2回合有 Alakazam"] <= side["第3回合有 Alakazam"] <= 1
    # going second gets an extra card and a turn-1 Supporter
    assert res["后攻"]["第3回合有 Alakazam"] > res["先攻"]["第3回合有 Alakazam"]


def test_turn_rules():
    deck = DECKS["alakazam-dusknoir"]()
    g = core.Game(deck, random.Random(1), first=True)
    hand0 = len(g.hand)
    g.turn = 1
    assert not g.can_supporter() and not g.can_attack()  # going first, turn 1
    m = g.board[0]
    assert not g.can_evolve(m)                          # nobody evolves on turn 1
    g.turn = 2
    assert g.can_evolve(m)
    fresh = core.Mon("Abra", 2)
    assert not g.can_evolve(fresh)                      # put into play this turn
    assert len(g.hand) == hand0
    g2 = core.Game(deck, random.Random(1), first=False)
    g2.play_turn()
    assert g2.turn == 1 and g2.can_attack() or g2.attacked  # going second may attack turn 1


def test_bench_limit_and_area_zero():
    deck = DECKS["basic-box-m"]()
    g = core.Game(deck, random.Random(2), first=True)
    g.board = [core.Mon("Latias ex", 0)] + [core.Mon("Meowth ex", 0) for _ in range(5)]
    assert g.bench_room() == 0
    g.board.append(core.Mon("Teal Mask Ogerpon ex", 0))   # pretend; Area Zero needs a Tera in play
    g.stadium = "Area Zero Underdepths"
    assert g.bench_max() == 8


def test_can_pay():
    assert core.can_pay(["Psychic Energy", "Psychic Energy", "Grass Energy"], "PPC")
    assert not core.can_pay(["Psychic Energy", "Grass Energy", "Grass Energy"], "PPC")
    assert core.can_pay(["Fire Energy", "Telepathic Psychic Energy"], "RP")
    assert core.can_pay(["Growing Grass Energy", "Mist Energy", "Spiky Energy"], "GCC")


def test_cli_lists_decks():
    assert {"basic-box-m", "alakazam-dusknoir", "crustle-dri", "dragapult-ex", "slowking-scr"} <= set(goldfish.DECKS)
