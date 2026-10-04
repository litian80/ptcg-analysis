from ptcg_video import cli
from ptcg_video.fetch import from_local


def test_local_info_json_with_dots_in_name(tmp_path):
    video = tmp_path / "Worlds 2026 vol.1.mp4"
    video.write_bytes(b"")
    (tmp_path / "Worlds 2026 vol.1.info.json").write_text(
        '{"id": "abc", "title": "Final", "upload_date": "20260830"}', encoding="utf-8")
    src = from_local(video, None)
    assert (src.video_id, src.title, src.upload_date) == ("abc", "Final", "20260830")


def test_local_captions_only_without_info(tmp_path):
    vtt = tmp_path / "match.en.vtt"
    vtt.write_text("WEBVTT\n", encoding="utf-8")
    assert from_local(None, vtt).video_id == "match"


def test_sibling_captions_with_glob_characters(tmp_path):
    video = tmp_path / "[Final] game 1.mp4"
    video.write_bytes(b"")
    vtt = tmp_path / "[Final] game 1.en.vtt"
    vtt.write_text("WEBVTT\n", encoding="utf-8")
    assert cli._sibling_captions(video) == vtt
