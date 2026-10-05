"""Read each player's prizes left from the broadcast overlay's prize markers.

Play! Pokémon's side-panel overlay draws a column of six small balls next to
each player's name. A ball is lit for each prize card still to take, filling
from the top, so the bottom ball goes dark first. Counting lit balls in every
sampled frame gives an exact prize timeline, which is the most reliable signal
for who knocked out what, and when.

Frames that are not the board (a zoomed card, the "PRIZES" banner, a desk shot,
a break screen) fail the check below and read as unknown. Replays carry a
REPLAY banner and are skipped too. Other older board states shown again can
only raise a count, so a count may only go down, unless the higher count holds
long enough to be a new game.

The balls are set by hand: on the Frankfurt final they changed 20-30 seconds
after the knockout.
"""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from .frames import Frame


@dataclass(frozen=True)
class ReplayTag:
    """The broadcast's REPLAY banner: plain patches inside it and the colour their means fall in."""

    patches: tuple[tuple[int, int, int, int], ...]  # (x0, x1, y0, y1); all the same height
    rgb: tuple[tuple[float, float], tuple[float, float], tuple[float, float]]  # mean R, G, B ranges
    max_std: float = 25.0  # a flat banner, not a busy picture that happens to average the same


@dataclass(frozen=True)
class PrizeLayout:
    """Prize-ball geometry in pixels of a ``ref``-sized frame."""

    columns: tuple[tuple[int, int], tuple[int, int]]  # (x0, x1) of the left and right panel's balls
    y0: int  # top of the first ball
    pitch: int  # vertical distance between balls
    ball: int  # ball height
    ref: tuple[int, int] = (1280, 720)
    on: float = 100.0  # mean gray above this = ball lit
    lit: tuple[float, float] = (105.0, 200.0)  # every lit ball must read in this range ...
    dark: tuple[float, float] = (30.0, 80.0)  # ... and every dark slot in this one, or the frame is not the board
    replay: ReplayTag | None = None

    @property
    def height(self) -> int:
        return self.y0 + self.pitch * 5 + self.ball


PRIZE_PRESETS: dict[str, PrizeLayout] = {
    # Measured on the Frankfurt 2026 regional Day 2 stream (the same overlay as
    # Worlds): lit balls (white ring) read 115-165, empty slots (dark navy) 38-65.
    # The REPLAY banner (x 552-727, y 26-53) is light blue, about (109, 174, 223),
    # with white text in the middle; the patches sit either side of the text.
    # On the final it matched every replay frame and nothing else.
    "sides": PrizeLayout(
        columns=((276, 300), (980, 1004)), y0=4, pitch=19, ball=17,
        replay=ReplayTag(patches=((565, 605, 32, 50), (680, 715, 32, 50)),
                         rgb=((10.0, 120.0), (135.0, 180.0), (205.0, 230.0))),
    ),
}


def count_column(column: np.ndarray, layout: PrizeLayout) -> int | None:
    """Lit balls in one panel's column (gray, ``layout.height`` rows), or None if it isn't the board."""
    means = [
        float(column[layout.y0 + layout.pitch * k + 2 : layout.y0 + layout.pitch * k + layout.ball - 1].mean())
        for k in range(6)
    ]
    lit = [m > layout.on for m in means]
    n = sum(lit)
    if lit != [True] * n + [False] * (6 - n):
        return None
    if any(not layout.lit[0] <= m <= layout.lit[1] for m in means[:n]):
        return None
    if any(not layout.dark[0] <= m <= layout.dark[1] for m in means[n:]):
        return None
    return n


def read_prizes(frames: list[Frame], layout: PrizeLayout) -> None:
    """Set ``frame.prizes`` to (left, right) prizes left, or None where the overlay isn't readable.

    Frames showing the REPLAY banner get ``frame.replay`` and no prizes.
    """
    if not frames:
        return
    if not shutil.which("ffmpeg"):
        raise RuntimeError("ffmpeg is needed to read prize markers")
    (lx0, lx1), (rx0, rx1) = layout.columns
    lw = lx1 - lx0
    strips = _crops(frames, layout, "gray", [(lx0, lx1, 0, layout.height), (rx0, rx1, 0, layout.height)])
    tags = _crops(frames, layout, "rgb24", layout.replay.patches) if layout.replay else None
    for i, (f, strip) in enumerate(zip(frames, strips)):
        f.replay = tags is not None and _is_replay(tags[i], layout.replay)
        left, right = count_column(strip[:, :lw], layout), count_column(strip[:, lw:], layout)
        # Both columns dark is a dark screen, not a 0-0 board.
        f.prizes = None if f.replay or left is None or right is None or (left, right) == (0, 0) else (left, right)


def _crops(frames: list[Frame], layout: PrizeLayout, pix_fmt: str, boxes) -> np.ndarray:
    """The boxes (x0, x1, y0, y1; all the same height) of every frame, side by side: (frames, h, w[, 3])."""
    w, h = layout.ref
    n = len(boxes)
    height = boxes[0][3] - boxes[0][2]
    width = sum(x1 - x0 for x0, x1, _, _ in boxes)
    filt = f"scale={w}:{h},format={pix_fmt},split={n}" + "".join(f"[s{i}]" for i in range(n)) + ";"
    filt += "".join(f"[s{i}]crop={x1 - x0}:{y1 - y0}:{x0}:{y0}[c{i}];" for i, (x0, x1, y0, y1) in enumerate(boxes))
    filt += ("".join(f"[c{i}]" for i in range(n)) + f"hstack=inputs={n}") if n > 1 else "[c0]null"
    # One ffmpeg pass over the sampled JPEGs, listed in a concat file so any file names work.
    with tempfile.TemporaryDirectory() as tmp:
        listing = Path(tmp) / "frames.txt"
        listing.write_text(
            "".join(f"file '{_quote(Path(f.path).resolve().as_posix())}'\nduration 1\n" for f in frames),
            encoding="utf-8",
        )
        proc = subprocess.run(
            ["ffmpeg", "-hide_banner", "-nostdin", "-loglevel", "error", "-f", "concat", "-safe", "0",
             "-i", str(listing), "-filter_complex", filt, "-fps_mode", "passthrough", "-f", "rawvideo", "-"],
            capture_output=True,
        )
    if proc.returncode != 0:
        raise RuntimeError(f"ffmpeg failed reading prize markers:\n{proc.stderr.decode(errors='replace')[-2000:]}")
    channels = 3 if pix_fmt == "rgb24" else 1
    size = width * height * channels
    raw = np.frombuffer(proc.stdout, dtype=np.uint8)
    out = raw[: len(raw) // size * size].reshape((-1, height, width) + ((3,) if channels == 3 else ()))
    if len(out) != len(frames):
        raise RuntimeError(f"ffmpeg returned {len(out)} images for {len(frames)} frames")
    return out


def _is_replay(tag: np.ndarray, replay: ReplayTag) -> bool:
    """True if every patch is a flat area in the banner's colour."""
    x = 0
    for x0, x1, _, _ in replay.patches:
        patch = tag[:, x : x + x1 - x0].reshape(-1, 3).astype(float)
        x += x1 - x0
        if patch.std(axis=0).max() >= replay.max_std:
            return False
        if any(not lo <= m <= hi for m, (lo, hi) in zip(patch.mean(axis=0), replay.rgb)):
            return False
    return True


def _quote(path: str) -> str:
    """Escape a path for an ffmpeg concat list entry in single quotes."""
    return path.replace("'", "'\\''")


@dataclass
class PrizeChange:
    t: float  # first sample showing the new count
    left: int
    right: int
    game: int = 1  # counted from the prize readings: a new game starts when the counts go back up
    # Last sample that still showed the previous count: the change happened
    # between ``after`` and ``t``. Pop-ups and banners often cover the panel
    # right after a knockout, so the gap can be most of a minute.
    after: float | None = None

    def to_dict(self) -> dict:
        d = {"t": round(self.t, 2), "left": self.left, "right": self.right, "game": self.game}
        if self.after is not None:
            d["after"] = round(self.after, 2)
        return d


def prize_timeline(
    frames: list[Frame], hold: int = 2, new_game_hold: float = 60.0, reset_hold: float = 20.0
) -> list[PrizeChange]:
    """Confirmed prize counts over time, one entry per change.

    A count is kept once ``hold`` readable samples in a row agree. Prizes are
    never given back, so a count that goes up is a replay of an earlier board
    and is ignored, unless it holds long enough to be a new game: ``reset_hold``
    seconds for a fresh 6-6 board (short sudden-death games included),
    ``new_game_hold`` for any other count. Caption-based game spans are not
    used; on long streams they miss games.
    """
    out: list[PrizeChange] = []
    run_value, run_start, run_len = None, 0.0, 0
    state_seen = None  # last sample showing the current confirmed count
    for f in frames:
        if f.prizes is None:
            continue
        if out and f.prizes == (out[-1].left, out[-1].right):
            state_seen = f.t
        if f.prizes == run_value:
            run_len += 1
        else:
            run_value, run_start, run_len = f.prizes, f.t, 1
        if run_len < hold:
            continue
        last = out[-1] if out else None
        left, right = run_value
        if last is None:
            out.append(PrizeChange(run_start, left, right))
        elif (left, right) == (last.left, last.right):
            continue
        elif left <= last.left and right <= last.right:
            out.append(PrizeChange(run_start, left, right, last.game, state_seen))
        elif f.t - run_start >= (reset_hold if run_value == (6, 6) else new_game_hold):
            out.append(PrizeChange(run_start, left, right, last.game + 1, state_seen))
        else:
            continue
        state_seen = f.t
    return out


def prize_games(changes: list[PrizeChange]) -> list[tuple[float, float | None]]:
    """Game spans from the prize timeline: each game runs until the next one's first reading."""
    firsts = [c.t for i, c in enumerate(changes) if i == 0 or c.game != changes[i - 1].game]
    return [(a, firsts[i + 1] if i + 1 < len(firsts) else None) for i, a in enumerate(firsts)]


def describe(change: PrizeChange, before: PrizeChange | None) -> str:
    """'left took 2' style note for a change; 'new game' when the counts went back up."""
    if before is None:
        return ""
    if change.game != before.game:
        return "new game"
    took = []
    if change.left < before.left:
        took.append(f"left took {before.left - change.left}")
    if change.right < before.right:
        took.append(f"right took {before.right - change.right}")
    return ", ".join(took)
