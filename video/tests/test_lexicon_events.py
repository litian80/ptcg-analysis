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


def test_common_word_names_need_capitals_in_cased_captions():
    m = CardMatcher(["Judge", "Grant", "Iono", "Special Red Card", "Red"])
    assert [n for n, *_ in m.find("the judge ruled on it", cased=True)] == []
    assert [n for n, *_ in m.find("he plays Judge here", cased=True)] == ["Judge"]
    assert [n for n, *_ in m.find("he plays judge here", cased=False)] == ["Judge"]
    # Casters drop "Card"; the longest name wins over "Red".
    assert [n for n, *_ in m.find("Special Red on the Alakazam", cased=True)] == ["Special Red Card"]


def test_hedged_knockouts_are_not_definite():
    from ptcg_video.lexicon import is_definite

    assert not is_definite("knockout", "he needs 16 cards in hand to get a KO")
    assert not is_definite("knockout", "that's not going to be a KO")
    assert is_definite("knockout", "and that's the KO on Kadabra")
    assert is_definite("knockout", "Alakazam, energy, Boss's Orders, KO")
    assert is_definite("prize", "Diego takes two prizes, three away")
    assert not is_definite("prize", "if he can take two prizes here")
    assert is_definite("evolve", "if he can rare candy")  # only KO/prize/match end are filtered


def test_match_end_closes_final_game():
    from ptcg_video.captions import Segment

    segs = [
        Segment(10, 12, "welcome back, Andrew is your 2024 world champion"),
        Segment(20, 22, "game one is underway"),
        Segment(600, 602, "and that's game"),
        Segment(700, 702, "game two, shuffle up"),
        Segment(800, 802, "one prize away from being your world champion"),
        Segment(1500, 1502, "Andrew Hedrick is your 2026 world champion"),
        Segment(1600, 1602, "an interview with the champion"),
    ]
    result = analyze_captions(segs, None)
    assert result.games == [(10, 600), (700, 1500)]
    defs = {(e.t, e.kind): e.definite for e in result.events}
    assert defs[(800, "match_end")] is False and defs[(1500, "match_end")] is True


def test_hedged_game_end_does_not_split_games():
    from ptcg_video.captions import Segment

    segs = [
        Segment(0, 2, "game one, shuffle up"),
        Segment(300, 302, "if he hits this, that's game"),
        Segment(900, 902, "and that's game one for Andrew"),
        Segment(1000, 1002, "game two"),
    ]
    assert analyze_captions(segs, None).games == [(0, 900), (1000, None)]


def test_caption_aliases_only_when_not_a_card_themselves():
    m = CardMatcher(["Fezandipiti ex", "Drakloak", "Budew", "Dragalge"])
    found = [n for n, _, _ in m.find("Fessentipity draws three, Bidoof attacks, Dragalge is benched")]
    assert found == ["Fezandipiti ex", "Budew", "Dragalge"]
    # Not in the pool, so no alias: "fez" stays a word.
    assert CardMatcher(["Drakloak"]).find("he wears a fez") == []


def test_exact_shorter_name_beats_fuzzy_longer_gram():
    pytest = __import__("pytest")
    pytest.importorskip("rapidfuzz")
    m = CardMatcher(["Lillie's Determination", "Night Stretcher"])
    assert m.find("He plays Lillie's Determination and Night Stretcher") == [
        ("Lillie's Determination", "lillies determination", 100.0),
        ("Night Stretcher", "night stretcher", 100.0),
    ]


def test_split_games_at_chapters_and_parse_games():
    from ptcg_video.events import parse_games, split_at

    assert split_at([(10, 600), (700, None)], [0, 300, 900]) == [(10, 300), (300, 600), (700, 900), (900, None)]
    assert parse_games("43:40-53:20, 1:16:20-") == [(2620, 3200), (4580, None)]
    for bad in ("43:40", "53:20-43:40"):
        try:
            parse_games(bad)
        except ValueError:
            continue
        raise AssertionError(bad)


def test_player_shorthand_aliases():
    m = CardMatcher(["Dragapult ex", "Munkidori", "Toucannon", "Alakazam", "Budew"])
    found = [n for n, _, _ in m.find("pult takes two, monkey dory moves three, two cannon is scary, zam needs 16, beddo locks")]
    assert found == ["Dragapult ex", "Munkidori", "Toucannon", "Alakazam", "Budew"]
