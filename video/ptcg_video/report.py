"""Write the analysis outputs: JSON for other tools, Markdown for people."""

from __future__ import annotations

import json
import os
from pathlib import Path

from .captions import Segment, text_between
from .events import CaptionAnalysis, game_at
from .frames import Frame
from .prizes import PrizeChange, describe, prize_games, prize_timeline
from .timeutil import fmt_ts
from .vision import WindowResult, pick_frames, windows_of


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
    (out_dir / "transcript.json").write_text(json.dumps([s.to_dict() for s in segments], ensure_ascii=False, indent=1), encoding="utf-8")
    (out_dir / "caption_events.json").write_text(json.dumps(captions.to_dict(), ensure_ascii=False, indent=1), encoding="utf-8")
    (out_dir / "frames.json").write_text(json.dumps([f.to_dict() for f in frames], indent=1), encoding="utf-8")
    if windows:
        (out_dir / "timeline.json").write_text(
            json.dumps([w.to_dict() for w in windows], ensure_ascii=False, indent=1), encoding="utf-8"
        )
    (out_dir / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    prize_log = prize_timeline(frames)
    if prize_log:
        (out_dir / "prizes.json").write_text(json.dumps([c.to_dict() for c in prize_log], indent=1), encoding="utf-8")

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
        lines += ["## Board timeline (from frames)", "", "| Time | Game | P1 active / bench / prizes left | P2 active / bench / prizes left | Stadium | What happened |", "|---|---|---|---|---|---|"]
        for w in windows:
            players = (w.data.get("players") or []) + [{}, {}]

            def side(p: dict) -> str:
                bench = ", ".join(p.get("bench") or []) or "-"
                active = p.get("active") or "?"
                if p.get("active_hp") is not None:
                    active += f" ({p['active_hp']} HP)"
                prizes = p.get("prizes_remaining")
                return f"{active} / {bench} / {prizes if prizes is not None else '?'}"

            what = w.data.get("summary", "") if w.data.get("board_visible") else "_(no board on screen)_"
            lines.append(
                f"| {_link(url, w.start)} | {w.data.get('game_number') or ''} | {side(players[0])} | {side(players[1])} | {w.data.get('stadium') or ''} | {what.replace('|', '/')} |"
            )
        lines.append("")

    if prize_log:
        lines += _prize_table(prize_log, url)

    games, source = _games(meta, captions, prize_log)
    if games:
        lines += [f"## Games (from {source})", ""]
        for i, (a, b) in enumerate(games, 1):
            lines.append(f"- Game {i}: {_link(url, a)} - {_link(url, b) if b is not None else 'end'}")
        lines.append("")

    if captions.card_counts:
        lines += ["## Cards mentioned by casters", "", "| Card | Mentions |", "|---|---|"]
        for name, n in captions.card_counts.most_common(30):
            lines.append(f"| {name} | {n} |")
        lines.append("")

    # Only what happened: knockouts/prizes the casters called as done, game ends,
    # and the "world champion" call that closed the final game (not intros).
    final_end = captions.games[-1][1] if captions.games else None
    key_events = [
        e for e in captions.events
        if e.definite and (e.kind in {"knockout", "prize", "game_end"} or (e.kind == "match_end" and e.t == final_end))
    ]
    hedged = len({(e.t, e.text) for e in captions.events if e.kind in {"knockout", "prize"} and not e.definite})
    if key_events or hedged:
        lines += ["## Key moments from commentary", ""]
        for e in key_events[:200]:
            lines.append(f"- {_link(url, e.t)} **{e.kind}**: {e.text}")
        if len(key_events) > 200:
            lines.append(f"- _... {len(key_events) - 200} more in caption_events.json_")
        if not key_events:
            lines.append("_No knockout or prize was called as done in the commentary._")
        if hedged:
            lines.append(f"\n_{hedged} caption lines about knockouts/prizes were casters discussing a "
                         "possibility; they are in caption_events.json with definite=false._")
        lines.append("")

    report = out_dir / "report.md"
    report.write_text("\n".join(lines), encoding="utf-8")
    return report


PRIZE_NOTE = ("Prizes left, read from the overlay's six prize markers per player (left panel / right panel). "
              "A count is kept once two samples in a row agree. Counts only go down, so replays are ignored; "
              "a count that goes back up starts a new game once it holds (20 s for a fresh 6-6 board, a minute "
              "otherwise). A time range means a pop-up or banner hid the panel and the knockout happened inside "
              "it. The last prize of a game is often missing because the broadcast cuts away on the winning "
              "knockout, and a sudden-death game can merge into the next one.")


def _games(meta: dict, captions: CaptionAnalysis, prizes: list[PrizeChange]):
    """Game spans and where they came from: --games, else the prize markers when they
    found at least as many games as the commentary, else the commentary."""
    if meta.get("games_from") == "--games":
        return captions.games, "--games"
    from_prizes = prize_games(prizes)
    if from_prizes and len(from_prizes) >= len(captions.games):
        return from_prizes, "prize markers"
    return captions.games, "commentary"


def _when(c: PrizeChange, url: str | None) -> str:
    """When a prize change happened: a range when pop-ups hid the panel for a while."""
    if c.after is not None and c.t - c.after > 10:
        return f"{_link(url, c.after)} - {fmt_ts(c.t)}"
    return _link(url, c.t)


def _prize_table(prizes: list[PrizeChange], url: str | None) -> list[str]:
    lines = ["## Prizes left (from the overlay)", "", PRIZE_NOTE, "",
             "| Time | Game | Left | Right | Change |", "|---|---|---|---|---|"]
    for i, c in enumerate(prizes):
        lines.append(f"| {_when(c, url)} | {c.game} | {c.left} | {c.right} | "
                     f"{describe(c, prizes[i - 1] if i else None)} |")
    lines.append("")
    return lines


PACK_INTRO = """Everything needed to read this match by eye, without an API key: for each \
window, the frames where the board changed, what the casters said, and the card \
names they mentioned. Open the frames in order. On Play! Pokémon streams the side \
overlays carry the board: the LEFT panel is P1 and the RIGHT panel is P2, each with \
player name, a column of six small prize markers, the Active Pokémon and its HP, the \
Bench, and the Stadium. The large number beside the name is games won in the match, \
not prizes. The middle camera shows what is being played. Regional streams have no \
side panels: read games won and the six prize markers per player from the scorebar \
at the top, and played cards from the callout that pops up on the left. Commentary is auto-captioned, so card \
names can be misspelled; trust the overlay over the captions."""


def write_review_pack(
    out_dir: Path,
    meta: dict,
    segments: list[Segment],
    captions: CaptionAnalysis,
    frames: list[Frame],
    window: float = 60.0,
    max_frames: int = 4,
) -> Path:
    """review_pack.md: per-window keyframes, commentary and cards, for reading by eye."""
    url = meta.get("url")
    lines = [f"# Review pack: {meta.get('title') or meta.get('video_id')}", ""]
    if url:
        lines.append(f"Source: {url}  ")
    if meta.get("card_pool"):
        lines.append(f"Card names matched against the {meta['card_pool']} Standard pool.  ")
    if lines[-1]:
        lines.append("")
    lines += [PACK_INTRO, ""]
    prizes = prize_timeline(frames)
    if prizes:
        lines += [PRIZE_NOTE, ""]
    games, source = _games(meta, captions, prizes)
    if games:
        lines += [f"## Games (from {source})", ""]
        for i, (a, b) in enumerate(games, 1):
            lines.append(f"- Game {i}: {_link(url, a)} - {_link(url, b) if b is not None else 'end'}")
        lines.append("")
    for n, (t, w_end, in_window) in enumerate(windows_of(frames, window), 1):
        game = game_at(games, t)
        lines += [f"## Window {n}: {_link(url, t)} - {fmt_ts(w_end)}" + (f" (game {game})" if game else ""), ""]
        for f in pick_frames(in_window, max_frames):
            lines.append(f"- {fmt_ts(f.t)}: `{Path(os.path.relpath(f.path, out_dir)).as_posix()}`")
        if prizes:
            lines.append("")
            lines += _prize_lines(prizes, t, w_end)
        cards = captions.cards_between(t, w_end)
        if cards:
            lines.append(f"\nCards mentioned: {', '.join(cards)}")
        calls = [e for e in captions.events if t <= e.t < w_end and e.kind != "card" and e.definite
                 and e.kind in {"knockout", "prize", "game_end", "match_end"}]
        for e in calls:
            lines.append(f"\nCasters call **{e.kind}** at {fmt_ts(e.t)}: {e.text}")
        lines.append(f"\nCommentary: {text_between(segments, t, w_end) or '(none)'}")
        lines.append("")
    pack = out_dir / "review_pack.md"
    pack.write_text("\n".join(lines), encoding="utf-8")
    return pack


def _prize_lines(prizes: list[PrizeChange], start: float, end: float) -> list[str]:
    """Prizes left at a window's start, then each change inside it."""
    before = [c for c in prizes if c.t <= start]
    lines = []
    if before:
        lines.append(f"Prizes left (left / right): {before[-1].left} / {before[-1].right}")
    for i, c in enumerate(prizes):
        if start < c.t < end:
            note = describe(c, prizes[i - 1] if i else None)
            when = (f"between {fmt_ts(c.after)} and {fmt_ts(c.t)}" if c.after is not None and c.t - c.after > 10
                    else f"at {fmt_ts(c.t)}")
            lines.append(f"Prizes left → {c.left} / {c.right} {when}" + (f" ({note})" if note else ""))
    return lines
