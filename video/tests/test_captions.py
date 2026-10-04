from conftest import FIXTURES

from ptcg_video.captions import clip, load_captions, text_between


def test_rolling_auto_captions_are_deduplicated_and_timed_at_first_appearance():
    segs = load_captions(FIXTURES / "rolling_auto.en.vtt")
    texts = [s.text for s in segs]
    assert texts == [
        "welcome back to game one",
        "he's going first with charizard x",
        "rare candy into charizard and that's a knock out",
        "on the garde voir he takes two prizes",
        "and he concedes that's game",
        "game two boss's orders on pidgeot ex",
    ]
    assert segs[0].start == 0.0
    assert segs[4].start == 180.0
    assert all(a.end <= b.start for a, b in zip(segs, segs[1:]))


def test_srt_and_offset():
    segs = load_captions(FIXTURES / "simple.srt", offset=100)
    assert [s.text for s in segs] == ["Iono shuffles both hands.", "He attaches a Psychic Energy."]
    assert segs[0].start == 101.0


def test_clip_and_text_between():
    segs = load_captions(FIXTURES / "rolling_auto.en.vtt")
    assert [s.text for s in clip(segs, 170, None)][0] == "and he concedes that's game"
    assert "knock out" in text_between(segs, 5, 9)
