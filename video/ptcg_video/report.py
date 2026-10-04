"""Write the analysis outputs: JSON for other tools, Markdown for people."""

from __future__ import annotations

import json
from pathlib import Path

from .captions import Segment
from .events import CaptionAnalysis
from .frames import Frame
from .timeutil import fmt_ts
from .vision import WindowResult


def _link(url: str | None, t: float) -> str:
    return f"[{fmt_ts(t)}]({url}&t={int(t)}s)" if url else f"[{fmt_ts(t)}]"


def write_outputs(
    out_dir: Path,
    meta: dict,
    segments: list[Segment],
    captions: CaptionAnalysis,
    frames: list[Frame],
    windows: list[WindowResult],
    summary: str | None,
) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "transcript.json").write_text(json.dumps([s.to_dict() for s in segments], ensure_ascii=False, indent=1))
    (out_dir / "caption_events.json").write_text(json.dumps(captions.to_dict(), ensure_ascii=False, indent=1))
    (out_dir / "frames.json").write_text(json.dumps([f.to_dict() for f in frames], indent=1))
    if windows:
        (out_dir / "timeline.json").write_text(
            json.dumps([w.to_dict() for w in windows], ensure_ascii=False, indent=1)
        )
    (out_dir / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1, default=str))

    url = meta.get("url")
    lines = [f"# {meta.get('title') or meta.get('video_id')}", ""]
    if url:
        lines.append(f"Source: {url}  ")
    if meta.get("channel"):
        lines.append(f"Channel: {meta['channel']}  ")
    if meta.get("range"):
        a, b = meta["range"]
        lines.append(f"Analyzed range: {fmt_ts(a or 0)} - {fmt_ts(b) if b else 'end'}  ")
    lines.append(
        f"Captions: {len(segments)} lines · frames sampled: {len(frames)} · keyframes: "
        f"{sum(f.keyframe for f in frames)} · vision windows: {len(windows)}"
    )
    lines.append("")

    if summary:
        lines += ["## Match report", "", summary.strip(), ""]

    if windows:
        lines += ["## Board timeline (from frames)", "", "| Time | Game | P1 active / bench / prizes | P2 active / bench / prizes | What happened |", "|---|---|---|---|---|"]
        for w in windows:
            players = (w.data.get("players") or []) + [{}, {}]

            def side(p: dict) -> str:
                bench = ", ".join(p.get("bench") or []) or "-"
                return f"{p.get('active') or '?'} / {bench} / {p.get('prizes_remaining') if p.get('prizes_remaining') is not None else '?'}"

            what = w.data.get("summary", "") if w.data.get("board_visible") else "_(no board on screen)_"
            lines.append(
                f"| {_link(url, w.start)} | {w.data.get('game_number') or ''} | {side(players[0])} | {side(players[1])} | {what.replace('|', '/')} |"
            )
        lines.append("")

    if captions.games:
        lines += ["## Games detected from commentary", ""]
        for i, (a, b) in enumerate(captions.games, 1):
            lines.append(f"- Game {i}: {_link(url, a)} - {_link(url, b) if b is not None else 'end'}")
        lines.append("")

    if captions.card_counts:
        lines += ["## Cards mentioned by casters", "", "| Card | Mentions |", "|---|---|"]
        for name, n in captions.card_counts.most_common(30):
            lines.append(f"| {name} | {n} |")
        lines.append("")

    key_events = [e for e in captions.events if e.kind in {"knockout", "prize", "game_start", "game_end", "turn"}]
    if key_events:
        lines += ["## Key moments from commentary", ""]
        for e in key_events[:200]:
            lines.append(f"- {_link(url, e.t)} **{e.kind}**: {e.text}")
        lines.append("")

    report = out_dir / "report.md"
    report.write_text("\n".join(lines), encoding="utf-8")
    return report
