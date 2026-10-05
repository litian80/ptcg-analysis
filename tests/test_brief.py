from ptcg import brief
from ptcg import judgments as jm


def test_points_reference_known_decks_and_judgments():
    window, picks, sel, tech_json, points = brief.load()
    assert brief.check(points, sel, jm.load_judgments()) == []
    for p in picks["picks"] + picks.get("avoid", []):
        assert p["deck"] in sel["archetypes"]


def test_tech_example_agrees_with_verdict():
    window, picks, sel, tech_json, points = brief.load()
    for p in picks["picks"]:
        for row in brief.tech(sel, tech_json, p["deck"]):
            assert (row["biggest"][0] > 0) == (row["delta"] > 0)


def test_renders_every_pick():
    window, picks, sel, tech_json, points = brief.load()
    assert "## 2. 带哪套" in brief.overview(window, picks, sel, tech_json, points)
    for p in picks["picks"]:
        assert brief.sheet(window, picks, sel, tech_json, points, p, {}).startswith("# ")
