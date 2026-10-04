"""Read board state from frames with Claude, then write a match summary.

Each window (default 60 s) sends Claude the keyframes in that window, the
commentary said during it, card names the casters mentioned, and the state at
the end of the previous window, and gets back structured JSON: who is active,
what is benched, prizes left, and what happened. A final call turns the whole
timeline into a written match report.

Needs ANTHROPIC_API_KEY (or another credential the Anthropic SDK picks up).
"""

from __future__ import annotations

import base64
import json
from dataclasses import dataclass
from pathlib import Path

from .captions import Segment, text_between
from .events import CaptionAnalysis
from .frames import Frame
from .timeutil import fmt_ts

DEFAULT_MODEL = "claude-opus-5-5"
FALLBACK_BETA = "server-side-fallback-2026-07-01"

_PLAYER = {
    "type": "object",
    "additionalProperties": False,
    "required": ["name", "active", "bench", "prizes_remaining", "hand_size", "deck_guess"],
    "properties": {
        "name": {"type": ["string", "null"], "description": "Player name if shown on the overlay or said by casters"},
        "active": {"type": ["string", "null"], "description": "Active Pokemon card name"},
        "bench": {"type": "array", "items": {"type": "string"}},
        "prizes_remaining": {"type": ["integer", "null"]},
        "hand_size": {"type": ["integer", "null"]},
        "deck_guess": {"type": ["string", "null"], "description": "Deck archetype, e.g. 'Gardevoir ex'"},
    },
}

WINDOW_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["board_visible", "game_number", "turn_player", "players", "actions", "summary"],
    "properties": {
        "board_visible": {"type": "boolean", "description": "False for desk cam, ads, interviews, brackets"},
        "game_number": {"type": ["integer", "null"]},
        "turn_player": {"type": ["string", "null"], "description": "'p1', 'p2' or null if unclear"},
        "players": {
            "type": "array",
            "description": "Exactly two entries: p1 = bottom/left of the screen, p2 = top/right",
            "items": _PLAYER,
        },
        "actions": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["t", "player", "action", "cards"],
                "properties": {
                    "t": {"type": "string", "description": "Timestamp label of the closest frame, e.g. '12:35'"},
                    "player": {"type": ["string", "null"], "description": "'p1' or 'p2'"},
                    "action": {"type": "string", "description": "What happened, one short sentence"},
                    "cards": {"type": "array", "items": {"type": "string"}},
                },
            },
        },
        "summary": {"type": "string", "description": "One or two sentences on this window"},
    },
}

SYSTEM = """You analyze broadcast footage of Pokemon Trading Card Game matches \
(Worlds, International Championships, Regionals, and similar streams).

You get a few frames from a short window of the video, the casters' commentary \
from the same window (auto-generated captions, so card names may be misspelled), \
card names that were matched in that commentary, and the board state you reported \
for the previous window.

Report the board state at the END of the window and the plays that happened \
during it. Conventions:
- p1 is the player whose side of the table is at the bottom (or left) of the \
screen; p2 is top (or right). Keep this assignment stable across windows.
- Use official English card names. Prefer names from the matched-cards hint when \
the frame is ambiguous; never invent a card you cannot see or that is not said.
- Prize count: read the prize cards or overlay; if unreadable, carry the previous \
value forward unless a Knock Out clearly happened.
- If the frames show no game board (desk, interview, ads, bracket), set \
board_visible false, keep players from the previous state, and leave actions empty.
- Use null for anything you cannot determine. Do not guess hand sizes."""


@dataclass
class WindowResult:
    start: float
    end: float
    frames: list[float]
    data: dict

    def to_dict(self) -> dict:
        return {"start": round(self.start, 2), "end": round(self.end, 2), "frames": self.frames, **self.data}


def _client():
    import anthropic

    return anthropic.Anthropic()


def _image_block(path: Path) -> dict:
    data = base64.standard_b64encode(Path(path).read_bytes()).decode()
    return {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": data}}


def _pick(frames: list[Frame], n: int) -> list[Frame]:
    if len(frames) <= n:
        return frames
    step = (len(frames) - 1) / (n - 1)
    return [frames[round(i * step)] for i in range(n)]


def _call(client, model: str, effort: str, system, content, schema: dict | None, max_tokens: int):
    kwargs = dict(
        model=model,
        max_tokens=max_tokens,
        system=system,
        thinking={"type": "adaptive"},
        messages=[{"role": "user", "content": content}],
        # On a safety-classifier decline, re-run on Anthropic's recommended model.
        extra_headers={"anthropic-beta": FALLBACK_BETA},
        extra_body={"fallbacks": "default"},
    )
    output_config = {"effort": effort}
    if schema is not None:
        output_config["format"] = {"type": "json_schema", "schema": schema}
    kwargs["output_config"] = output_config
    with client.messages.stream(**kwargs) as stream:
        msg = stream.get_final_message()
    if msg.stop_reason == "refusal":
        raise RuntimeError("model declined the request")
    if msg.stop_reason == "max_tokens":
        raise RuntimeError("response hit max_tokens")
    return "".join(b.text for b in msg.content if b.type == "text")


def analyze_windows(
    frames: list[Frame],
    segments: list[Segment],
    captions: CaptionAnalysis,
    window: float = 60.0,
    max_frames: int = 4,
    model: str = DEFAULT_MODEL,
    effort: str = "low",
    max_windows: int | None = None,
    client=None,
    on_window=None,
) -> list[WindowResult]:
    """Run the per-window board-state extraction over the keyframes."""
    client = client or _client()
    keyframes = [f for f in frames if f.keyframe] or frames
    if not keyframes:
        return []
    results: list[WindowResult] = []
    prev: dict | None = None
    t, end = keyframes[0].t, keyframes[-1].t + 1e-6
    system = [{"type": "text", "text": SYSTEM, "cache_control": {"type": "ephemeral"}}]
    while t < end:
        w_end = t + window
        in_window = [f for f in keyframes if t <= f.t < w_end]
        if in_window:
            chosen = _pick(in_window, max_frames)
            content: list[dict] = [
                {
                    "type": "text",
                    "text": (
                        f"Window {fmt_ts(t)}-{fmt_ts(w_end)}.\n\n"
                        f"Previous state: {json.dumps(prev) if prev else 'none (start of analysis)'}\n\n"
                        f"Commentary: {text_between(segments, t, w_end) or '(none)'}\n\n"
                        f"Cards mentioned: {', '.join(captions.cards_between(t - window, w_end)) or '(none)'}"
                    ),
                }
            ]
            for f in chosen:
                content.append({"type": "text", "text": f"Frame at {fmt_ts(f.t)}:"})
                content.append(_image_block(f.path))
            raw = _call(client, model, effort, system, content, WINDOW_SCHEMA, max_tokens=8000)
            data = json.loads(raw)
            if not data.get("board_visible") and prev:
                data["players"] = prev.get("players", data.get("players"))
            results.append(WindowResult(t, w_end, [round(f.t, 2) for f in chosen], data))
            prev = {k: data.get(k) for k in ("game_number", "turn_player", "players")}
            if on_window:
                on_window(results[-1])
            if max_windows and len(results) >= max_windows:
                break
        t = w_end
    return results


SUMMARY_SYSTEM = """You are a Pokemon TCG coach reviewing a recorded tournament match. \
You get a timeline built from the broadcast: per-window board states and plays read \
from video frames, plus caption-based events and the commentary itself. The timeline \
is machine-extracted and can contain mistakes; when sources disagree, say so rather \
than picking one silently.

Write a match report in Markdown with these sections:
1. Match overview: players, the two decks (archetype and key cards seen), result of \
each game and of the match, if known.
2. Game by game: the flow of each game turn by turn at a high level, prize trades, \
and the turning point.
3. Key decisions: plays that decided the game, and what the alternatives were.
4. Takeaways for deck selection and for playing this matchup.
Cite timestamps like [12:35] so the reader can jump to them. Keep it tight."""


def summarize(
    meta: dict,
    windows: list[WindowResult],
    captions: CaptionAnalysis,
    segments: list[Segment],
    model: str = DEFAULT_MODEL,
    effort: str = "high",
    language: str = "zh",
    client=None,
) -> str:
    client = client or _client()
    lang_line = {"zh": "Write the report in Simplified Chinese; keep card names in English.",
                 "en": "Write the report in English."}.get(language, f"Write the report in {language}.")
    transcript = "\n".join(f"[{fmt_ts(s.start)}] {s.text}" for s in segments)
    payload = {
        "video": {k: meta.get(k) for k in ("title", "channel", "upload_date", "url")},
        "caption_games": captions.to_dict()["games"],
        "cards_mentioned": captions.card_counts.most_common(40),
        "windows": [w.to_dict() for w in windows],
    }
    content = [
        {"type": "text", "text": f"Timeline (JSON):\n{json.dumps(payload, ensure_ascii=False)}"},
        {"type": "text", "text": f"Commentary transcript:\n{transcript}"},
        {"type": "text", "text": lang_line},
    ]
    return _call(client, model, effort, SUMMARY_SYSTEM, content, None, max_tokens=32000)
