import pytest

from ptcg_video.frames import REGION_PRESETS, changed_fraction, mark_keyframes, parse_regions, sample_frames


def test_sample_and_keyframes(board_video, tmp_path):
    frames = sample_frames(board_video, tmp_path / "f", every=2.0, offset=1000)
    assert len(frames) == 15
    assert [round(f.t - 1000, 2) for f in frames[:3]] == [0.0, 2.0, 4.0]
    keys = mark_keyframes(frames, threshold=REGION_PRESETS["full"].threshold, max_gap=1e9)
    # One keyframe per board state.
    assert [round(k.t - 1000) for k in keys] == [0, 10, 20]
    assert changed_fraction(frames[0].thumbs[0], frames[1].thumbs[0]) == 0


def test_sample_range(board_video, tmp_path):
    frames = sample_frames(board_video, tmp_path / "f", every=5.0, start=10, end=20)
    assert [round(f.t) for f in frames] == [10, 15]


def test_timestamps_match_content(board_video, tmp_path):
    # The board changes at exactly t=10 and t=20; the frame labelled 10 must show the new board.
    frames = sample_frames(board_video, tmp_path / "f", every=5.0)
    by_t = {round(f.t): f for f in frames}
    assert changed_fraction(by_t[5].thumbs[0], by_t[10].thumbs[0]) > 0.05
    assert changed_fraction(by_t[10].thumbs[0], by_t[15].thumbs[0]) == 0


def test_side_regions_ignore_handcam(broadcast_video, tmp_path):
    full = sample_frames(broadcast_video, tmp_path / "a", every=2.0)
    churn = mark_keyframes(full, threshold=REGION_PRESETS["full"].threshold, max_gap=1e9)
    assert len(churn) > 5  # the moving hand-cam makes most frames look new

    sides = REGION_PRESETS["sides"]
    frames = sample_frames(broadcast_video, tmp_path / "b", every=2.0, layout=sides)
    assert all(len(f.thumbs) == 2 for f in frames)
    keys = mark_keyframes(frames, threshold=sides.threshold, max_gap=1e9)
    assert [round(k.t) for k in keys] == [0, 20]


def test_sides_catch_small_overlay_changes_but_not_noise(overlay_video, tmp_path):
    sides = REGION_PRESETS["sides"]
    frames = sample_frames(overlay_video, tmp_path / "o", every=5.0, layout=sides)
    keys = mark_keyframes(frames, threshold=sides.threshold, max_gap=1e9, dead_band=sides.dead_band)
    assert [round(k.t) for k in keys] == [0, 20, 40]


def test_sides_ignore_glow_and_popups(live_overlay_video, tmp_path):
    sides = REGION_PRESETS["sides"]
    frames = sample_frames(live_overlay_video, tmp_path / "l", every=5.0, layout=sides)
    # Without the animation mask and the steadiness check, the glow and the
    # pop-up turn most samples into keyframes.
    noisy = mark_keyframes(frames, threshold=sides.threshold, max_gap=1e9, dead_band=sides.dead_band, steady=False)
    assert len(noisy) > 6
    keys = mark_keyframes(frames, threshold=sides.threshold, max_gap=1e9, dead_band=sides.dead_band)
    assert [round(k.t) for k in keys] == [0, 20, 40]
    assert max(f.change for f in frames) > 0


def test_max_gap_keeps_periodic_frames(broadcast_video, tmp_path):
    sides = REGION_PRESETS["sides"]
    frames = sample_frames(broadcast_video, tmp_path / "c", every=2.0, layout=sides)
    keys = mark_keyframes(frames, threshold=sides.threshold, max_gap=8)
    assert [round(k.t) for k in keys] == [0, 8, 16, 20, 28]


def test_parse_regions():
    assert parse_regions("sides") is REGION_PRESETS["sides"]
    assert len(parse_regions("regional").regions) == 2
    custom = parse_regions("0,0,0.2,1;0.8,0,0.2,1")
    assert custom.regions == ((0.0, 0.0, 0.2, 1.0), (0.8, 0.0, 0.2, 1.0)) and custom.thumb == (32, 96)
    assert parse_regions("0,0,0.5,0.5").thumb == (64, 36)
    with pytest.raises(ValueError):
        parse_regions("0.9,0,0.5,1")
    with pytest.raises(ValueError):
        parse_regions("bogus")
