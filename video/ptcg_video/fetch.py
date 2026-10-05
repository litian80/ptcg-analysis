"""Get a match video and its captions, from YouTube (via yt-dlp) or from local files.

Tournament streams are often hours long, so a time range (or a chapter) can be
given to download only the match of interest.
"""

from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass, field
from pathlib import Path

CAPTION_LANGS = ["en", "en-US", "en-GB", "en-orig"]
# Where English captions come from, best first: subtitles someone uploaded;
# YouTube's speech recognition of an English stream ("en-orig"); YouTube's
# machine translation ("en"), the only English a stream in another language
# has. YouTube rate-limits the translated track (HTTP 429) while the original
# one still downloads, so "en" auto-captions are only asked for without
# "en-orig".
CAPTION_SOURCES = [
    ({"writesubtitles": True}, ["en", "en-US", "en-GB"]),
    ({"writeautomaticsub": True}, ["en-orig"]),
    ({"writeautomaticsub": True}, ["en"]),
]
_sleep = time.sleep  # replaced in tests
_YT_ID = re.compile(r"(?:v=|youtu\.be/|/live/|/shorts/|/embed/)([A-Za-z0-9_-]{11})")


@dataclass
class VideoSource:
    video_id: str
    title: str
    video_path: Path | None
    captions_path: Path | None
    # Offset (seconds) of video_path's t=0 inside the original video, when only
    # a range was downloaded. Caption and frame times are reported in original
    # video time so links like ?t=123 keep working.
    offset: float = 0.0
    url: str | None = None
    channel: str | None = None
    upload_date: str | None = None
    duration: float | None = None
    chapters: list[dict] = field(default_factory=list)
    description: str = ""
    # Why the captions are missing, when YouTube refused them.
    captions_error: str | None = None

    def to_dict(self) -> dict:
        d = self.__dict__.copy()
        d["video_path"] = str(self.video_path) if self.video_path else None
        d["captions_path"] = str(self.captions_path) if self.captions_path else None
        return d


def video_id_from(url_or_id: str) -> str:
    m = _YT_ID.search(url_or_id)
    if m:
        return m.group(1)
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", url_or_id):
        return url_or_id
    raise ValueError(f"not a YouTube URL or video id: {url_or_id!r}")


def is_youtube(target: str) -> bool:
    if Path(target).exists():
        return False
    try:
        video_id_from(target)
        return True
    except ValueError:
        return False


def _pick_captions(out_dir: Path, video_id: str) -> Path | None:
    candidates = sorted(out_dir.glob(f"{video_id}*.vtt"))
    if not candidates:
        return None
    # Prefer human-uploaded subtitles over auto-generated ones; yt-dlp names
    # both <id>.<lang>.vtt, so rank by language preference only.
    def rank(p: Path) -> int:
        lang = p.suffixes[-2].lstrip(".") if len(p.suffixes) >= 2 else ""
        return CAPTION_LANGS.index(lang) if lang in CAPTION_LANGS else len(CAPTION_LANGS)

    return min(candidates, key=rank)


def fetch_metadata(url_or_id: str) -> dict:
    """Return yt-dlp's info dict (title, chapters, duration, ...) without downloading."""
    import yt_dlp

    url = f"https://www.youtube.com/watch?v={video_id_from(url_or_id)}"
    with yt_dlp.YoutubeDL({"quiet": True, "no_warnings": True, "skip_download": True}) as ydl:
        return ydl.extract_info(url, download=False)


def _offers(info: dict, flags: dict, langs: list[str]) -> bool:
    tracks = info.get("subtitles" if flags.get("writesubtitles") else "automatic_captions") or {}
    return any(lang in tracks for lang in langs)


def _download_captions(
    url: str, base: dict, out_dir: Path, video_id: str, attempts: int, wait: float
) -> tuple[dict | None, str | None]:
    """Captions and the info JSON, without the video: (info, error or None).

    YouTube sometimes rate-limits caption downloads (HTTP 429), and yt-dlp then
    aborts the whole download, video included. So captions get their own
    passes, one per entry of CAPTION_SOURCES until one gives a file; a round
    that was rate-limited is retried with doubling waits, and a caption failure
    is returned rather than raised. Any other error (video unavailable,
    sign-in) is raised. info is None only when no pass got past the captions.
    """
    import yt_dlp

    info, error = None, None
    for attempt in range(attempts):
        if attempt:
            _sleep(wait * 2 ** (attempt - 1))
        limited = False
        for flags, langs in CAPTION_SOURCES:
            if info is not None and not _offers(info, flags, langs):
                continue
            opts = base | flags | {"skip_download": True, "subtitleslangs": langs, "subtitlesformat": "vtt"}
            try:
                with yt_dlp.YoutubeDL(opts) as ydl:
                    info = ydl.extract_info(url, download=True)
            except yt_dlp.utils.DownloadError as e:
                error = str(e)
                if "subtitles" not in error:
                    raise
                limited = limited or "429" in error
            if _pick_captions(out_dir, video_id):
                return info, None
        if not limited:
            break
    return info, error


def fetch_youtube(
    url_or_id: str,
    out_dir: Path,
    start: float | None = None,
    end: float | None = None,
    max_height: int = 720,
    download_video: bool = True,
    caption_attempts: int = 4,
    caption_wait: float = 30.0,
) -> VideoSource:
    """Download captions (manual, else auto-generated) and optionally the video.

    When YouTube keeps refusing the captions, the video is still downloaded and
    ``captions_error`` says why; running again later fetches the captions and
    reuses the video already on disk.
    """
    import yt_dlp
    from yt_dlp.utils import download_range_func

    video_id = video_id_from(url_or_id)
    url = f"https://www.youtube.com/watch?v={video_id}"
    out_dir.mkdir(parents=True, exist_ok=True)
    base = {
        "quiet": True,
        "no_warnings": True,
        "noprogress": True,  # as a library, quiet doesn't hide the progress bar
        "outtmpl": str(out_dir / "%(id)s.%(ext)s"),
        "writeinfojson": True,
        # Only the picture is used (captions come separately), so take the
        # video stream alone. Merging in an audio track also fails with HTTP
        # 403 on videos that carry auto-dubbed audio (NAIC 2026 final).
        "format": (
            f"bv*[height<={max_height}][ext=mp4]/bv*[height<={max_height}]/"
            f"b[height<={max_height}]/b"
        ),
    }
    info, captions_error = _download_captions(url, base, out_dir, video_id, caption_attempts, caption_wait)
    if download_video:
        opts = dict(base)
        if start is not None or end is not None:
            opts["download_ranges"] = download_range_func(None, [(start or 0, end or float("inf"))])
            opts["force_keyframes_at_cuts"] = True
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
    elif info is None:
        info = fetch_metadata(url)

    video_path = None
    if download_video:
        video_path = next(
            (p for ext in ("mp4", "mkv", "webm") if (p := out_dir / f"{video_id}.{ext}").exists()), None
        )
    return VideoSource(
        video_id=video_id,
        title=info.get("title") or video_id,
        video_path=video_path,
        captions_path=_pick_captions(out_dir, video_id),
        offset=float(start or 0) if download_video else 0.0,
        url=url,
        channel=info.get("channel") or info.get("uploader"),
        upload_date=info.get("upload_date"),
        duration=info.get("duration"),
        chapters=info.get("chapters") or [],
        description=info.get("description") or "",
        captions_error=captions_error,
    )


def from_local(video_path: str | Path | None, captions_path: str | Path | None, offset: float = 0.0) -> VideoSource:
    """Use a video file (and/or caption file) already on disk."""
    vp = Path(video_path) if video_path else None
    cp = Path(captions_path) if captions_path else None
    if vp is None and cp is None:
        raise ValueError("need a video file, a captions file, or both")
    first = vp or cp
    # yt-dlp writes <id>.info.json next to <id>.mp4 and <id>.en.vtt; ids and
    # titles may contain dots, so strip suffixes one at a time until it is found.
    stems = _stems(first.name)
    # Default id: the video's name, or the caption file's without ".en.vtt".
    stem, info = (vp.stem if vp else stems[min(1, len(stems) - 1)] if stems else first.name), {}
    for candidate in _stems(first.name):
        info_path = first.with_name(f"{candidate}.info.json")
        if info_path.exists():
            stem, info = candidate, json.loads(info_path.read_text(encoding="utf-8"))
            break
    return VideoSource(
        video_id=info.get("id", stem),
        title=info.get("title", stem),
        video_path=vp,
        captions_path=cp,
        offset=offset,
        url=info.get("webpage_url"),
        channel=info.get("channel"),
        upload_date=info.get("upload_date"),
        duration=info.get("duration"),
        chapters=info.get("chapters") or [],
        description=info.get("description") or "",
    )


def _stems(name: str) -> list[str]:
    """'a.b.en.vtt' -> ['a.b.en', 'a.b', 'a']."""
    out = []
    while "." in name:
        name = name.rsplit(".", 1)[0]
        out.append(name)
    return out


def chapter_range(chapters: list[dict], selector: str) -> tuple[float, float]:
    """Find a chapter by 1-based index or by case-insensitive title substring."""
    if not chapters:
        raise ValueError("this video has no chapters")
    if selector.isdigit():
        idx = int(selector) - 1
        if not 0 <= idx < len(chapters):
            raise ValueError(f"chapter {selector} out of range 1..{len(chapters)}")
        ch = chapters[idx]
    else:
        matches = [c for c in chapters if selector.lower() in (c.get("title") or "").lower()]
        if not matches:
            raise ValueError(f"no chapter title contains {selector!r}")
        ch = matches[0]
    return float(ch["start_time"]), float(ch["end_time"])
