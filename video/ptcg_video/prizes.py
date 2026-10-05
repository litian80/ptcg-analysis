"""Read each player's prizes left from the broadcast overlay's prize markers.

Play! Pokémon's side-panel overlay draws a column of six small balls next to
each player's name. A ball is lit for each prize card still to take, filling
from the top, so the bottom ball goes dark first. Counting lit balls in every
sampled frame gives an exact prize timeline, which is the most reliable signal
for who knocked out what, and when.

Frames that are not the board (a zoomed card, the "PRIZES" banner, a desk shot,
a break screen) fail the check below and read as unknown. Post-game replays
show older board states, so a count may only go down, unless the higher count
holds long enough to be a new game.
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

    @property
    def height(self) -> int:
        return self.y0 + self.pitch * 5 + self.ball


PRIZE_PRESETS: dict[str, PrizeLayout] = {
    # Measured on the Frankfurt 2026 regional Day 2 stream (the same overlay as
    # Worlds): lit balls (white ring) read 115-165, empty slots (dark navy) 38-65.
    "sides": PrizeLayout(columns=((276, 300), (980, 1004)), y0=4, pitch=19, ball=17),
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
    """Set ``frame.prizes`` to (left, right) prizes left, or None where the overlay isn't readable."""
    if not frames:
        return
    if not shutil.which("ffmpeg"):
        raise RuntimeError("ffmpeg is needed to read prize markers")
    (lx0, lx1), (rx0, rx1) = layout.columns
    w, h = layout.ref
    filt = (
        f"scale={w}:{h},format=gray,split=2[a][b];"
        f"[a]crop={lx1 - lx0}:{layout.height}:{lx0}:0[l];"
        f"[b]crop={rx1 - rx0}:{layout.height}:{rx0}:0[r];"
        "[l][r]hstack=inputs=2"
    )
    # One ffmpeg pass over the sampled JPEGs, listed in a concat file so any file names work.
    lw, rw = lx1 - lx0, rx1 - rx0
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
    size = (lw + rw) * layout.height
    raw = np.frombuffer(proc.stdout, dtype=np.uint8)
    strips = raw[: len(raw) // size * size].reshape(-1, layout.height, lw + rw)
    if len(strips) != len(frames):
        raise RuntimeError(f"ffmpeg returned {len(strips)} images for {len(frames)} frames")
    for f, strip in zip(frames, strips):
        left, right = count_column(strip[:, :lw], layout), count_column(strip[:, lw:], layout)
        # Both columns dark is a dark screen, not a 0-0 board.
        f.prizes = None if left is None or right is None or (left, right) == (0, 0) else (left, right)


def _quote(path: str) -> str:
    """Escape a path for an ffmpeg concat list entry in single quotes."""
    return path.replace("'", "'\\''")


@dataclass
class PrizeChange:
    t: float  # first sample showing the new count
    left: int
    right: int
    game: int = 1  # counted from the prize readings: a new game starts when the counts go back up

    def to_dict(self) -> dict:
        return {"t": round(self.t, 2), "left": self.left, "right": self.right, "game": self.game}


def prize_timeline(frames: list[Frame], hold: int = 2, new_game_hold: float = 60.0) -> list[PrizeChange]:
    """Confirmed prize counts over time, one entry per change.

    A count is kept once ``hold`` readable samples in a row agree. Prizes are
    never given back, so a count that goes up is a replay of an earlier board
    and is ignored, unless it holds for ``new_game_hold`` seconds: then a new
    game has started. Caption-based game spans are not used; on long streams
    they miss games.
    """
    out: list[PrizeChange] = []
    run_value, run_start, run_len = None, 0.0, 0
    for f in frames:
        if f.prizes is None:
            continue
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
            out.append(PrizeChange(run_start, left, right, last.game))
        elif f.t - run_start >= new_game_hold:
            out.append(PrizeChange(run_start, left, right, last.game + 1))
    return out


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
