from conftest import FIXTURES

from ptcg_video.captions import load_captions, parse_captions
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


def test_short_names_need_case_and_words_are_not_glued():
    m = CardMatcher(["Will", "May", "Bea", "Gardevoir", "Gardevoir ex", "Abra"])
    assert m.find("Diego will start to sift through his deck") == []
    assert [n for n, *_ in m.find("He plays Will and flips")] == ["Will"]
    assert [n for n, *_ in m.find("he plays will and flips")] == ["Will"]  # caseless captions
    assert m.find("priority will be finding", cased=True) == []  # lowercase line in a cased track
    assert m.find("That would be a decent sacrificial") == []
    assert [n for n, *_ in m.find("knock out on the garde voir")] == ["Gardevoir"]


def test_game_split_ignores_deck_out_talk_and_recaps():
    segs = parse_captions(
        "00:00:20.000 --> 00:00:22.000\nDiego is going first\n\n"
        "00:28:36.000 --> 00:28:38.000\nand Andrew is going to take game number one\n\n"
        "00:29:06.000 --> 00:29:08.000\nlet's go back to the whole of game one\n\n"
        "00:30:49.000 --> 00:30:51.000\nhe has to take a mulligan\n\n"
        "00:52:02.000 --> 00:52:04.000\nto make sure he wasn't going to deck out\n\n"
        "00:54:30.000 --> 00:54:32.000\nDiego is counting his cards\n"
    )
    games = analyze_captions(segs, None).games
    assert games == [(20.0, 1716.0), (1849.0, None)]
