from ptcg_video.frames import hamming, mark_keyframes, sample_frames


def test_sample_and_keyframes(board_video, tmp_path):
    frames = sample_frames(board_video, tmp_path / "f", every=2.0, offset=1000)
    assert len(frames) == 15
    assert frames[0].t == 1000.0 and abs(frames[1].t - 1002.0) < 0.01
    keys = mark_keyframes(frames, threshold=4, max_gap=1e9)
    # One keyframe per board state.
    assert [round(k.t - 1000) for k in keys] == [0, 10, 20]
    assert hamming(frames[0].dhash, frames[1].dhash) == 0


def test_sample_range(board_video, tmp_path):
    frames = sample_frames(board_video, tmp_path / "f", every=5.0, start=10, end=20)
    assert [round(f.t) for f in frames] == [10, 15]
