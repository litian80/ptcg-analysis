from ptcg import goldfish


def test_list_is_60_and_rates_are_sane():
    assert sum(goldfish.BASE_LIST.values()) == 60
    res = goldfish.run(500, goldfish.BASE_LIST, seed=3)
    for side in res.values():
        assert 0 < side["第2回合有 Alakazam"] <= side["第3回合有 Alakazam"] <= 1
    # going second gets an extra card and a turn-1 Supporter
    assert res["后攻"]["第3回合有 Alakazam"] > res["先攻"]["第3回合有 Alakazam"]
