import json
from pathlib import Path

from ptcg_video.events import CaptionAnalysis
from ptcg_video.report import write_outputs
from ptcg_video.vision import WindowResult


def test_outputs_are_utf8_even_with_a_legacy_locale(tmp_path, monkeypatch):
    # Windows defaults text files to the ANSI code page (e.g. cp1252), which cannot
    # encode the Chinese report text; every output must be written as UTF-8.
    orig_write, orig_read = Path.write_text, Path.read_text
    monkeypatch.setattr(Path, "write_text", lambda self, data, encoding=None, **kw: orig_write(self, data, encoding=encoding or "cp1252", **kw))
    monkeypatch.setattr(Path, "read_text", lambda self, encoding=None, **kw: orig_read(self, encoding=encoding or "cp1252", **kw))
    windows = [WindowResult(0, 60, [1.0], {"summary": "喷火龙击倒沙奈朵"})]
    write_outputs(tmp_path, {"video_id": "x", "title": "世界赛决赛"}, [], CaptionAnalysis(), [], windows, "## 对局概览")
    assert json.loads((tmp_path / "timeline.json").read_bytes().decode("utf-8"))[0]["summary"] == "喷火龙击倒沙奈朵"
    assert json.loads((tmp_path / "meta.json").read_bytes().decode("utf-8"))["title"] == "世界赛决赛"
    assert "对局概览" in (tmp_path / "report.md").read_bytes().decode("utf-8")
