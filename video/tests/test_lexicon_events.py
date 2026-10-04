from conftest import FIXTURES

from ptcg_video.captions import load_captions
from ptcg_video.events import analyze_captions
from ptcg_video.lexicon import CardMatcher, find_actions, load_card_names, normalize


def matcher():
    return CardMatcher(load_card_names(FIXTURES / "cards.txt"))


def test_normalize():
    assert normalize("Boss’s Orders") == "bosss orders"
    assert normalize("Flabébé") == "flabebe"


def test_asr_variants_and_longest_match():
    m = matcher()
    assert [n for n, *_ in m.find("going first with charizard x")] == ["Charizard ex"]
    assert [n for n, *_ in m.find("charizard ex attacks")] == ["Charizard ex"]
    assert [n for n, *_ in m.find("knock out on the garde voir")] == ["Gardevoir"]
    assert [n for n, *_ in m.find("boss's orders on pidgeot ex")] == ["Boss's Orders", "Pidgeot ex"]


def test_load_json_formats(tmp_path):
    p = tmp_path / "c.json"
    p.write_text('{"data": [{"name": "Iono"}, {"name": "Pikachu ex"}]}')
    assert load_card_names(p) == ["Iono", "Pikachu ex"]


def test_actions():
    kinds = {k for k, _ in find_actions("rare candy into charizard and that's a knock out")}
    assert kinds == {"evolve", "knockout"}
    assert find_actions("and he concedes")[0][0] == "game_end"


def test_caption_analysis_games_and_counts():
    result = analyze_captions(load_captions(FIXTURES / "rolling_auto.en.vtt"), matcher())
    assert result.card_counts["Charizard ex"] == 1
    assert result.card_counts["Charizard"] == 1
    assert len(result.games) == 2
    assert result.games[0] == (0.0, 180.0)
    assert result.cards_between(0, 10) == ["Charizard", "Charizard ex", "Gardevoir", "Rare Candy"]
