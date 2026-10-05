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
RATE_LIMITED = "ERROR: Unable to download video subtitles for 'en': HTTP Error 429: Too Many Requests"


@pytest.fixture
def fake_ydl(monkeypatch):
    """yt_dlp.YoutubeDL stand-in whose caption downloads fail with HTTP 429 `fails` times."""
    fake = SimpleNamespace(fails=0, calls=[], waits=[])

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
            if self.opts.get("writesubtitles"):
                if fake.fails:
                    fake.fails -= 1
                    raise yt_dlp.utils.DownloadError(RATE_LIMITED)
                (out / f"{VID}.en.vtt").write_text("WEBVTT\n", encoding="utf-8")
            elif download and not self.opts.get("skip_download"):
                (out / f"{VID}.mp4").write_bytes(b"")
            return {"title": "Final"}

    monkeypatch.setattr(yt_dlp, "YoutubeDL", FakeYDL)
    monkeypatch.setattr(fetch, "_sleep", fake.waits.append)
    return fake


def test_captions_retried_when_rate_limited(tmp_path, fake_ydl):
    fake_ydl.fails = 2
    src = fetch.fetch_youtube(VID, tmp_path)
    assert fake_ydl.waits == [30.0, 60.0]
    assert (src.captions_path, src.video_path, src.captions_error) == (
        tmp_path / f"{VID}.en.vtt", tmp_path / f"{VID}.mp4", None)
    # The video pass asks for no captions, so a rate limit can't stop it.
    assert not fake_ydl.calls[-1].get("writesubtitles")


def test_video_downloaded_when_captions_keep_failing(tmp_path, fake_ydl):
    # Baltimore 2026 day 1 and the NAIC semis: YouTube refused captions for a while.
    fake_ydl.fails = 99
    src = fetch.fetch_youtube(VID, tmp_path, caption_attempts=3)
    assert fake_ydl.waits == [30.0, 60.0]
    assert (src.video_path, src.captions_path, src.title) == (tmp_path / f"{VID}.mp4", None, "Final")
    assert "429" in src.captions_error


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
