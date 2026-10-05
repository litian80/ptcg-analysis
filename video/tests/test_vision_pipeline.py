import pytest
import json
from types import SimpleNamespace

from conftest import FIXTURES

from ptcg_video import cli, vision
from ptcg_video.captions import load_captions
from ptcg_video.events import analyze_captions
from ptcg_video.frames import mark_keyframes, sample_frames


class _Stream:
    def __init__(self, msg):
        self.msg = msg

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False

    def get_final_message(self):
        return self.msg


class FakeClient:
    """Stands in for anthropic.Anthropic(); records requests, returns canned JSON."""

    def __init__(self):
        self.requests = []
        self.messages = self

    def stream(self, **kwargs):
        self.requests.append(kwargs)
        if "format" in kwargs["output_config"]:
            n = len(self.requests)
            text = json.dumps({
                "board_visible": True, "game_number": 1, "turn_player": "p1", "stadium": "Battle Cage",
                "players": [
                    {"name": "A", "active": "Charizard ex", "active_hp": 330, "bench": ["Pidgeot ex"], "prizes_remaining": 6 - n,
                     "hand_size": None, "deck_guess": "Charizard ex"},
                    {"name": "B", "active": "Gardevoir ex", "active_hp": None, "bench": [], "prizes_remaining": 6,
                     "hand_size": None, "deck_guess": "Gardevoir ex"},
                ],
                "actions": [{"t": "0:10", "player": "p1", "action": "Knocks Out Kirlia", "cards": ["Charizard ex"]}],
                "summary": f"window {n}",
            })
        else:
            text = "## 对局概览\nCharizard ex vs Gardevoir ex"
        return _Stream(SimpleNamespace(stop_reason="end_turn", content=[SimpleNamespace(type="text", text=text)]))


def test_windows_send_frames_captions_and_schema(board_video, tmp_path):
    frames = sample_frames(board_video, tmp_path / "f", every=2.0)
    mark_keyframes(frames, threshold=0.05)
    segs = load_captions(FIXTURES / "rolling_auto.en.vtt")
    caps = analyze_captions(segs, None)
    client = FakeClient()
    results = vision.analyze_windows(frames, segs, caps, window=15, client=client)
    assert len(results) == 2  # keyframes at 0, 10 | 20
    first = client.requests[0]
    assert first["model"] == "claude-opus-5-5"
    assert first["extra_body"] == {"fallbacks": "default"}
    assert first["output_config"]["format"]["schema"] is vision.WINDOW_SCHEMA
    images = [b for b in first["messages"][0]["content"] if b["type"] == "image"]
    assert len(images) == 2
    assert "knock out" in first["messages"][0]["content"][0]["text"]
    # The second window carries the first window's state forward.
    assert '"prizes_remaining": 5' in client.requests[1]["messages"][0]["content"][0]["text"]


def test_cli_end_to_end_local(board_video, tmp_path, monkeypatch):
    client = FakeClient()
    monkeypatch.setattr(vision, "_client", lambda: client)
    out = tmp_path / "out"
    rc = cli.main([
        "analyze", str(board_video), "--captions", str(FIXTURES / "rolling_auto.en.vtt"),
        "--cards", str(FIXTURES / "cards.txt"), "--every", "2", "--change-threshold", "0.05",
        "--window", "15", "--out", str(out),
    ])
    assert rc == 0
    report = (out / "match" / "report.md").read_text(encoding="utf-8")
    assert "## Match report" in report and "对局概览" in report
    assert "Charizard ex (330 HP) / Pidgeot ex / 5" in report and "| Battle Cage |" in report
    assert "| Charizard ex | 1 |" in report
    timeline = json.loads((out / "match" / "timeline.json").read_text(encoding="utf-8"))
    assert timeline[0]["players"][1]["active"] == "Gardevoir ex"


def test_cli_no_llm(board_video, tmp_path):
    out = tmp_path / "out"
    assert cli.main(["analyze", str(board_video), "--captions", str(FIXTURES / "simple.srt"),
                     "--no-llm", "--out", str(out)]) == 0
    report = (out / "match" / "report.md").read_text(encoding="utf-8")
    assert "vision windows: 0" in report


def test_pick_frames_one_and_many(board_video, tmp_path):
    frames = sample_frames(board_video, tmp_path / "f", every=2.0)
    assert vision.pick_frames(frames, 1) == frames[-1:]
    picked = vision.pick_frames(frames, 3)
    assert picked[0] is frames[0] and picked[-1] is frames[-1] and len(picked) == 3


class _DeskClient(FakeClient):
    """Second window is the desk cam: board_visible false, nothing read."""

    def stream(self, **kwargs):
        if len(self.requests) == 1:
            self.requests.append(kwargs)
            text = json.dumps({"board_visible": False, "game_number": None, "turn_player": None, "stadium": None,
                               "players": [], "actions": [], "summary": "desk"})
            return _Stream(SimpleNamespace(stop_reason="end_turn", content=[SimpleNamespace(type="text", text=text)]))
        return super().stream(**kwargs)


def test_desk_window_keeps_board(board_video, tmp_path):
    frames = sample_frames(board_video, tmp_path / "f", every=2.0)
    mark_keyframes(frames, threshold=0.05)
    segs = load_captions(FIXTURES / "simple.srt")
    results = vision.analyze_windows(frames, segs, analyze_captions(segs, None), window=10, client=_DeskClient())
    desk = results[1].data
    assert desk["stadium"] == "Battle Cage" and desk["game_number"] == 1
    assert desk["players"][0]["active"] == "Charizard ex"


def test_no_llm_writes_review_pack(board_video, tmp_path):
    out = tmp_path / "out"
    assert cli.main(["analyze", str(board_video), "--captions", str(FIXTURES / "rolling_auto.en.vtt"),
                     "--cards", str(FIXTURES / "cards.txt"), "--every", "2", "--change-threshold", "0.05",
                     "--window", "15", "--frames-per-window", "1", "--no-llm", "--out", str(out)]) == 0
    pack = (out / "match" / "review_pack.md").read_text(encoding="utf-8")
    assert pack.count("## Window ") == 2
    # One frame per window, the last keyframe in it, as a path relative to the pack.
    assert "`frames/frame_00006.jpg`" in pack and "`frames/frame_00011.jpg`" in pack
    assert "Cards mentioned: Charizard, Charizard ex, Gardevoir, Rare Candy" in pack
    assert "Casters call **knockout** at 0:05" in pack
    assert "Commentary: " in pack


def test_youtube_downloads_whole_video_and_cuts_locally(board_video, tmp_path, monkeypatch):
    from ptcg_video.fetch import VideoSource

    calls = []

    def fake_fetch(url, out_dir, start, end, max_height, download_video):
        calls.append((start, end))
        return VideoSource("abcdefghijk", "t", board_video, FIXTURES / "simple.srt", url="https://youtu.be/x",
                           chapters=[{"start_time": 0, "end_time": 15}, {"start_time": 15, "end_time": 30}])

    monkeypatch.setattr(cli, "fetch_youtube", fake_fetch)
    out = tmp_path / "out"
    assert cli.main(["analyze", "abcdefghijk", "--start", "0:10", "--end", "0:20", "--every", "2",
                     "--cards", "none", "--no-llm", "--out", str(out)]) == 0
    assert calls == [(None, None)]
    frames = json.loads((out / "abcdefghijk" / "frames.json").read_text(encoding="utf-8"))
    assert [round(f["t"]) for f in frames] == [10, 12, 14, 16, 18]


def test_games_flag_overrides_commentary(board_video, tmp_path):
    out = tmp_path / "out"
    assert cli.main(["analyze", str(board_video), "--captions", str(FIXTURES / "rolling_auto.en.vtt"),
                     "--games", "0:00-0:12,0:12-", "--cards", "none", "--no-llm", "--out", str(out)]) == 0
    report = (out / "match" / "report.md").read_text(encoding="utf-8")
    assert "- Game 1: [0:00] - [0:12]" in report and "- Game 2: [0:12] - end" in report
    with pytest.raises(SystemExit):
        cli.build_parser().parse_args(["analyze", "x.mp4", "--games", "0:12"])
