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
                "board_visible": True, "game_number": 1, "turn_player": "p1",
                "players": [
                    {"name": "A", "active": "Charizard ex", "bench": ["Pidgeot ex"], "prizes_remaining": 6 - n,
                     "hand_size": None, "deck_guess": "Charizard ex"},
                    {"name": "B", "active": "Gardevoir ex", "bench": [], "prizes_remaining": 6,
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
    mark_keyframes(frames, threshold=4)
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
        "--cards", str(FIXTURES / "cards.txt"), "--every", "2", "--change-threshold", "4",
        "--window", "15", "--out", str(out),
    ])
    assert rc == 0
    report = (out / "match" / "report.md").read_text(encoding="utf-8")
    assert "## Match report" in report and "对局概览" in report
    assert "Charizard ex / Pidgeot ex / 5" in report
    assert "| Charizard ex | 1 |" in report
    timeline = json.loads((out / "match" / "timeline.json").read_text(encoding="utf-8"))
    assert timeline[0]["players"][1]["active"] == "Gardevoir ex"


def test_cli_no_llm(board_video, tmp_path):
    out = tmp_path / "out"
    assert cli.main(["analyze", str(board_video), "--captions", str(FIXTURES / "simple.srt"),
                     "--no-llm", "--out", str(out)]) == 0
    report = (out / "match" / "report.md").read_text(encoding="utf-8")
    assert "vision windows: 0" in report
