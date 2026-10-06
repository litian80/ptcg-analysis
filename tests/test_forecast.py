from ptcg import forecast as fc
from ptcg import plan, tuning


def test_backtest_never_sees_the_event_or_later():
    for e, past in fc.cases():
        assert past and all(x["day"] < e["day"] for x in past)


def test_forecast_is_a_distribution():
    nx = fc.next_event()
    assert abs(sum(nx["field"].values()) - 1) < 1e-9
    assert all(0 <= d["expected"] <= 1 for d in nx["decks"].values())


def test_bh_is_monotone_and_bounded():
    ps = [0.001, 0.04, 0.03, 0.5, 0.2]
    qs = tuning._bh(ps)
    order = sorted(range(len(ps)), key=lambda i: ps[i])
    assert all(qs[order[i]] <= qs[order[i + 1]] + 1e-12 for i in range(len(ps) - 1))
    assert all(p <= q <= 1 for p, q in zip(ps, qs))


def test_clustered_variance_grows_when_players_disagree():
    w = lambda o: 1.0
    same = [[("x", 1.0), ("x", 0.0)]] * 10
    split = [[("x", 1.0), ("x", 1.0)]] * 5 + [[("x", 0.0), ("x", 0.0)]] * 5
    assert tuning._clustered(same, w)[0] == tuning._clustered(split, w)[0] == 0.5
    assert tuning._clustered(split, w)[1] > tuning._clustered(same, w)[1]


def test_plan_renders():
    text = plan.write()
    for head in ("## 结论", "## 1.", "## 2.", "## 3.", "## 4."):
        assert head in text
