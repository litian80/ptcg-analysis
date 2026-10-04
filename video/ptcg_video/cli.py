"""Command line: ``python -m ptcg_video analyze <youtube-url | video-file> ...``"""

from __future__ import annotations

import argparse
import glob
import os
import sys
from pathlib import Path

from . import captions as cap
from .events import analyze_captions
from .fetch import chapter_range, fetch_metadata, fetch_youtube, from_local, is_youtube
from .cardpool import find_data_dir, load_pool, parse_date, season_for
from .frames import mark_keyframes, parse_regions, sample_frames
from .lexicon import CardMatcher, load_card_names
from .report import write_outputs, write_review_pack
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

    matcher = _card_matcher(args, meta)
    uploaded = _upload_date(meta)
    captions = analyze_captions(segments, matcher, year=uploaded.year if uploaded else None)

    frames = []
    if src.video_path:
        layout = parse_regions(args.hash_regions)
        _log(f"sampling a frame every {args.every:g}s (change detection: {args.hash_regions}) ...")
        frames = sample_frames(
            src.video_path, work / "frames", args.every, clip_start, clip_end, offset=src.offset, layout=layout
        )
        threshold = layout.threshold if args.change_threshold is None else args.change_threshold
        dead_band = layout.dead_band if args.dead_band is None else args.dead_band
        mark_keyframes(frames, threshold=threshold, dead_band=dead_band)
        _log(f"frames: {len(frames)} sampled, {sum(f.keyframe for f in frames)} keyframes")

    windows, summary = [], None
    if args.llm and frames:
        from .vision import analyze_windows, summarize

        def progress(w):
            _log(f"  window {fmt_ts(w.start)}: {w.data.get('summary', '')[:100]}")

        keys = [f for f in frames if f.keyframe]
        calls = len({int((f.t - keys[0].t) // args.window) for f in keys}) if keys else 0
        if args.max_windows:
            calls = min(calls, args.max_windows)
        _log(f"reading board state with {args.model}: {calls} vision calls, then 1 report call ...")
        windows = analyze_windows(
            frames, segments, captions, window=args.window, max_frames=args.frames_per_window,
            model=args.model, effort=args.effort, max_windows=args.max_windows, on_window=progress,
        )
        _log("writing match report ...")
        summary = summarize(meta, windows, captions, segments, model=args.model, language=args.lang)
    elif args.llm and not frames:
        _log("no video frames, so skipping the vision step (use --no-llm to silence this)")

    report = write_outputs(work, meta, segments, captions, frames, windows, summary)
    if frames and not windows:
        pack = write_review_pack(work, meta, segments, captions, frames, args.window, args.frames_per_window)
        _log(f"review pack (frames + commentary per window, for reading by eye): {pack}")
    print(report)
    return 0


def _upload_date(meta: dict):
    try:
        return parse_date(meta.get("upload_date"))
    except ValueError:
        return None


def _card_matcher(args, meta: dict) -> CardMatcher | None:
    """Card names to look for in captions: a file, or the season's legal pool."""
    # --format/--data-dir ask for the season pool, so they beat PTCG_CARD_NAMES.
    env = None if (args.format or args.data_dir) else os.environ.get("PTCG_CARD_NAMES")
    spec = args.cards or env or "auto"
    if spec == "none":
        return None
    try:
        if spec != "auto":
            matcher = CardMatcher(load_card_names(spec))
            _log(f"card names loaded from {spec}: {len(matcher)}")
            return matcher
        data_dir = Path(args.data_dir) if args.data_dir else find_data_dir(Path.cwd(), Path(__file__).parent)
        if data_dir is None:
            _log("card names: no data/formats/standard_rotations.json found; "
                 "pass --data-dir or --cards to match card names")
            return None
        uploaded = _upload_date(meta)
        season = args.format or season_for(data_dir, uploaded, live=args.live)
        pool = load_pool(data_dir, season)
    except (OSError, ValueError, KeyError) as e:  # JSONDecodeError is a ValueError
        _log(f"card names: skipped ({e})")
        return None
    why = "--format" if args.format else (f"uploaded {uploaded}" if uploaded else "upload date unknown, using today")
    _log(f"card names: {season} Standard pool, {len(pool.names)} names ({why})")
    meta["card_pool"] = season
    return CardMatcher(pool.names)


def _sibling_captions(video: Path) -> Path | None:
    stem = glob.escape(video.stem)
    for pattern in (f"{stem}*.vtt", f"{stem}*.srt"):
        found = sorted(video.parent.glob(pattern))
        if found:
            return found[0]
    return None


def _regions(spec: str) -> str:
    try:
        parse_regions(spec)
    except ValueError as e:
        raise argparse.ArgumentTypeError(str(e))
    return spec


def _positive_int(value: str) -> int:
    n = int(value)
    if n < 1:
        raise argparse.ArgumentTypeError("must be at least 1")
    return n


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
    a.add_argument("--cards", help="card name list (.txt/.json/.csv), 'auto' (default: the legal pool for the "
                   "video's season from the repo's data/), or 'none'; also PTCG_CARD_NAMES")
    a.add_argument("--data-dir", help="the repo's data/ directory, if not found automatically")
    a.add_argument("--format", help="Standard season for the card pool, e.g. 2026-27 (default: from upload date)")
    a.add_argument("--live", action="store_true", help="TCG Live video: use Live's rotation dates")
    a.add_argument("--hash-regions", default="full", type=_regions,
                   help="where to look for board changes: 'full', 'sides' (Play! Pokémon broadcast overlay), "
                        "or 'x,y,w,h;...' fractions of the frame")
    a.add_argument("--every", type=float, default=5.0, help="seconds between sampled frames (default 5)")
    a.add_argument("--change-threshold", type=float,
                   help="fraction of a region's pixels that must change to count as a board change "
                        "(default 0.05 for 'full', 0.02 for 'sides' and custom regions)")
    a.add_argument("--dead-band", type=int,
                   help="gray levels a pixel must change by to count (default 8 for 'full', 30 for 'sides' "
                        "and custom regions); raise it if static overlays still make keyframes")
    a.add_argument("--captions-only", action="store_true", help="skip video download and frames")
    a.add_argument("--max-height", type=int, default=720)
    a.add_argument("--no-llm", dest="llm", action="store_false", help="skip Claude (captions + frames only)")
    a.add_argument("--model", default="claude-opus-5-5")
    a.add_argument("--effort", default="low", help="effort for per-window frame reading (summary uses high)")
    a.add_argument("--window", type=float, default=60.0, help="seconds per vision window")
    a.add_argument("--frames-per-window", type=_positive_int, default=4,
                   help="frames per window sent to Claude, or listed in the review pack (default 4)")
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
