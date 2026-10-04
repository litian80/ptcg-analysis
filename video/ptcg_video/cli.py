"""Command line: ``python -m ptcg_video analyze <youtube-url | video-file> ...``"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from . import captions as cap
from .events import analyze_captions
from .fetch import chapter_range, fetch_metadata, fetch_youtube, from_local, is_youtube
from .frames import mark_keyframes, sample_frames
from .lexicon import CardMatcher, load_card_names
from .report import write_outputs
from .timeutil import fmt_ts, parse_ts


def _log(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)


def cmd_chapters(args) -> int:
    info = fetch_metadata(args.target)
    print(info.get("title"))
    for i, ch in enumerate(info.get("chapters") or [], 1):
        print(f"{i:3d}  {fmt_ts(ch['start_time']):>8} - {fmt_ts(ch['end_time']):>8}  {ch.get('title')}")
    if not info.get("chapters"):
        print("(no chapters)")
    return 0


def cmd_analyze(args) -> int:
    start, end = parse_ts(args.start), parse_ts(args.end)
    out_root = Path(args.out)

    if is_youtube(args.target):
        if args.chapter:
            start, end = chapter_range(fetch_metadata(args.target).get("chapters") or [], args.chapter)
            _log(f"chapter {args.chapter}: {fmt_ts(start)} - {fmt_ts(end)}")
        from .fetch import video_id_from

        work = out_root / video_id_from(args.target)
        _log("downloading captions" + ("" if args.captions_only else " and video") + " ...")
        src = fetch_youtube(args.target, work / "source", start, end, args.max_height, not args.captions_only)
        # The downloaded clip already starts at `start`; frame times get the offset.
        clip_start, clip_end = None, None
    else:
        video = None if args.captions_only else args.target
        captions_file = args.captions or _sibling_captions(Path(args.target))
        src = from_local(video, captions_file)
        work = out_root / src.video_id
        clip_start, clip_end = start, end

    meta = src.to_dict() | {"range": [start, end]}

    segments = cap.load_captions(src.captions_path) if src.captions_path else []
    segments = cap.clip(segments, start, end)
    _log(f"captions: {len(segments)} lines" if segments else "captions: none found")

    matcher = None
    cards_path = args.cards or os.environ.get("PTCG_CARD_NAMES")
    if cards_path:
        matcher = CardMatcher(load_card_names(cards_path))
        _log(f"card names loaded: {len(matcher)}")
    captions = analyze_captions(segments, matcher)

    frames = []
    if src.video_path:
        _log(f"sampling a frame every {args.every:g}s ...")
        frames = sample_frames(src.video_path, work / "frames", args.every, clip_start, clip_end, offset=src.offset)
        mark_keyframes(frames, threshold=args.change_threshold)
        _log(f"frames: {len(frames)} sampled, {sum(f.keyframe for f in frames)} keyframes")

    windows, summary = [], None
    if args.llm and frames:
        from .vision import analyze_windows, summarize

        def progress(w):
            _log(f"  window {fmt_ts(w.start)}: {w.data.get('summary', '')[:100]}")

        _log(f"reading board state with {args.model} ...")
        windows = analyze_windows(
            frames, segments, captions, window=args.window, max_frames=args.frames_per_window,
            model=args.model, effort=args.effort, max_windows=args.max_windows, on_window=progress,
        )
        _log("writing match report ...")
        summary = summarize(meta, windows, captions, segments, model=args.model, language=args.lang)
    elif args.llm and not frames:
        _log("no video frames, so skipping the vision step (use --no-llm to silence this)")

    report = write_outputs(work, meta, segments, captions, frames, windows, summary)
    print(report)
    return 0


def _sibling_captions(video: Path) -> Path | None:
    for pattern in (f"{video.stem}*.vtt", f"{video.stem}*.srt"):
        found = sorted(video.parent.glob(pattern))
        if found:
            return found[0]
    return None


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="ptcg_video", description="Analyze Pokemon TCG match videos")
    sub = p.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("chapters", help="list a YouTube video's chapters (streams often have one per match)")
    c.add_argument("target")
    c.set_defaults(func=cmd_chapters)

    a = sub.add_parser("analyze", help="analyze one match")
    a.add_argument("target", help="YouTube URL/id, or a local video file")
    a.add_argument("--captions", help="caption file (.vtt/.srt) for a local video")
    a.add_argument("--start", help="start time, e.g. 1:02:30")
    a.add_argument("--end", help="end time")
    a.add_argument("--chapter", help="YouTube chapter number or title substring")
    a.add_argument("--cards", help="card name list (.txt/.json/.csv); or set PTCG_CARD_NAMES")
    a.add_argument("--every", type=float, default=5.0, help="seconds between sampled frames (default 5)")
    a.add_argument("--change-threshold", type=int, default=6, help="dHash bits that count as a board change")
    a.add_argument("--captions-only", action="store_true", help="skip video download and frames")
    a.add_argument("--max-height", type=int, default=720)
    a.add_argument("--no-llm", dest="llm", action="store_false", help="skip Claude (captions + frames only)")
    a.add_argument("--model", default="claude-opus-5-5")
    a.add_argument("--effort", default="low", help="effort for per-window frame reading (summary uses high)")
    a.add_argument("--window", type=float, default=60.0, help="seconds per vision window")
    a.add_argument("--frames-per-window", type=int, default=4)
    a.add_argument("--max-windows", type=int, help="cap vision calls (cost control)")
    a.add_argument("--lang", default="zh", help="report language: zh (default) or en")
    a.add_argument("--out", default="out", help="output root directory")
    a.set_defaults(func=cmd_analyze)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except Exception as e:  # yt-dlp download errors are long; show the first line
        if type(e).__name__ != "DownloadError":
            raise
        _log(f"YouTube download failed: {str(e).splitlines()[0]}")
        _log("If YouTube is unreachable from this machine, download the video and captions "
             "elsewhere and pass the local file with --captions.")
        return 2
