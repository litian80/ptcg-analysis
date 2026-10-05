from pathlib import Path
from types import SimpleNamespace

import pytest
import yt_dlp

from ptcg_video import cli, fetch
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


VID = "abcdefghijk"


@pytest.fixture
def fake_ydl(monkeypatch):
    """yt_dlp.YoutubeDL stand-in for a video with the given caption tracks.

    `manual` and `auto` name the uploaded and automatic tracks (by default an
    English stream: speech recognition "en-orig" and its "en" copy); a track
    listed in `fails` is refused with HTTP 429 that many times.
    """
    fake = SimpleNamespace(manual=set(), auto={"en-orig", "en"}, fails={}, calls=[], waits=[])

    class FakeYDL:
        def __init__(self, opts):
            self.opts = opts

        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

        def extract_info(self, url, download=True):
            fake.calls.append(self.opts)
            out = Path(self.opts["outtmpl"]).parent
            tracks = (fake.manual if self.opts.get("writesubtitles")
                      else fake.auto if self.opts.get("writeautomaticsub") else set())
            for lang in self.opts.get("subtitleslangs", []):
                if lang not in tracks:
                    continue
                if fake.fails.get(lang):
                    fake.fails[lang] -= 1
                    raise yt_dlp.utils.DownloadError(
                        f"ERROR: Unable to download video subtitles for {lang!r}: HTTP Error 429: Too Many Requests")
                (out / f"{VID}.{lang}.vtt").write_text("WEBVTT\n", encoding="utf-8")
            if download and not self.opts.get("skip_download"):
                (out / f"{VID}.mp4").write_bytes(b"")
            return {"title": "Final", "subtitles": dict.fromkeys(fake.manual, []),
                    "automatic_captions": dict.fromkeys(fake.auto, [])}

    monkeypatch.setattr(yt_dlp, "YoutubeDL", FakeYDL)
    monkeypatch.setattr(fetch, "_sleep", fake.waits.append)
    return fake


def _asked_for(calls):
    """The caption tracks each pass asked for, as (kind, langs)."""
    return [("manual" if c.get("writesubtitles") else "auto", c["subtitleslangs"])
            for c in calls if c.get("writesubtitles") or c.get("writeautomaticsub")]


def test_english_stream_uses_the_original_track(tmp_path, fake_ydl):
    # The Turin final: YouTube refused "en" for an hour while "en-orig" came at once.
    fake_ydl.fails = {"en": 99}
    src = fetch.fetch_youtube(VID, tmp_path)
    assert (src.captions_path, src.captions_error, fake_ydl.waits) == (tmp_path / f"{VID}.en-orig.vtt", None, [])
    assert _asked_for(fake_ydl.calls) == [("manual", ["en", "en-US", "en-GB"]), ("auto", ["en-orig"])]
    # The video pass asks for no captions, so a rate limit can't stop it.
    assert src.video_path == tmp_path / f"{VID}.mp4"
    assert _asked_for(fake_ydl.calls[-1:]) == []


def test_uploaded_subtitles_come_first(tmp_path, fake_ydl):
    fake_ydl.manual = {"en"}
    src = fetch.fetch_youtube(VID, tmp_path)
    assert src.captions_path == tmp_path / f"{VID}.en.vtt"
    assert _asked_for(fake_ydl.calls) == [("manual", ["en", "en-US", "en-GB"])]


def test_translation_retried_when_rate_limited(tmp_path, fake_ydl):
    # A stream in another language has only YouTube's translation into English.
    fake_ydl.auto = {"en"}
    fake_ydl.fails = {"en": 2}
    src = fetch.fetch_youtube(VID, tmp_path)
    assert fake_ydl.waits == [30.0, 60.0]
    assert (src.captions_path, src.video_path, src.captions_error) == (
        tmp_path / f"{VID}.en.vtt", tmp_path / f"{VID}.mp4", None)
    # Retries skip the tracks the video doesn't have.
    assert _asked_for(fake_ydl.calls) == [("manual", ["en", "en-US", "en-GB"])] + [("auto", ["en"])] * 3


def test_video_downloaded_when_captions_keep_failing(tmp_path, fake_ydl):
    # Baltimore 2026 day 1 and the NAIC semis: YouTube refused captions for a while.
    fake_ydl.fails = {"en-orig": 99, "en": 99}
    src = fetch.fetch_youtube(VID, tmp_path, caption_attempts=3)
    assert fake_ydl.waits == [30.0, 60.0]
    assert (src.video_path, src.captions_path, src.title) == (tmp_path / f"{VID}.mp4", None, "Final")
    assert "429" in src.captions_error


def test_video_without_captions(tmp_path, fake_ydl):
    fake_ydl.auto = set()
    src = fetch.fetch_youtube(VID, tmp_path)
    assert (src.captions_path, src.captions_error, fake_ydl.waits) == (None, None, [])
    assert src.video_path == tmp_path / f"{VID}.mp4"


def test_other_download_errors_still_raised(tmp_path, monkeypatch):
    class Unavailable:
        def __init__(self, opts):
            pass

        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

        def extract_info(self, url, download=True):
            raise yt_dlp.utils.DownloadError(f"ERROR: [youtube] {VID}: Video unavailable")

    monkeypatch.setattr(yt_dlp, "YoutubeDL", Unavailable)
    with pytest.raises(yt_dlp.utils.DownloadError):
        fetch.fetch_youtube(VID, tmp_path)
