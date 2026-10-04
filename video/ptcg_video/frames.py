"""Sample frames from a match video and keep the ones where the board changed.

One ffmpeg pass writes a JPEG every ``every`` seconds and, alongside it, a tiny
9x8 grayscale copy used for a difference hash (dHash). Consecutive frames whose
hashes are close are the same board state (players thinking, commentary over
a static table), so only frames that differ from the last kept one are kept.
"""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

import numpy as np

_PTS = re.compile(r"pts_time:([0-9.]+)")
_HASH_W, _HASH_H = 9, 8


@dataclass
class Frame:
    t: float  # seconds in original-video time
    path: Path
    dhash: int
    keyframe: bool = False

    def to_dict(self) -> dict:
        return {"t": round(self.t, 2), "path": str(self.path), "keyframe": self.keyframe}


def _dhash(gray: np.ndarray) -> int:
    diff = gray[:, 1:] > gray[:, :-1]
    return int("".join("1" if b else "0" for b in diff.flatten()), 2)


def hamming(a: int, b: int) -> int:
    return (a ^ b).bit_count()


def sample_frames(
    video: str | Path,
    out_dir: str | Path,
    every: float = 5.0,
    start: float | None = None,
    end: float | None = None,
    offset: float = 0.0,
    width: int = 1280,
) -> list[Frame]:
    """Write frame_XXXXX.jpg files to out_dir and return them with timestamps.

    ``start``/``end`` are positions inside ``video``; ``offset`` is added to
    every timestamp (use it when ``video`` is a clip cut from a longer stream).
    """
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    for old in out_dir.glob("frame_*.jpg"):
        old.unlink()
    cmd = ["ffmpeg", "-hide_banner", "-nostdin", "-y"]
    if start:
        cmd += ["-ss", f"{start:.3f}"]
    if end is not None:
        cmd += ["-to", f"{end:.3f}"]
    cmd += [
        "-i", str(video),
        "-filter_complex",
        f"[0:v]fps=1/{every},showinfo,split=2[full][small];"
        f"[full]scale={width}:-2[out];"
        f"[small]scale={_HASH_W}:{_HASH_H}:flags=area,format=gray[hash]",
        "-map", "[out]", "-q:v", "3", str(out_dir / "frame_%05d.jpg"),
        "-map", "[hash]", "-f", "rawvideo", "-",
    ]
    proc = subprocess.run(cmd, capture_output=True)
    if proc.returncode != 0:
        raise RuntimeError(f"ffmpeg failed:\n{proc.stderr.decode(errors='replace')[-2000:]}")
    times = [float(m) for m in _PTS.findall(proc.stderr.decode(errors="replace"))]
    raw = np.frombuffer(proc.stdout, dtype=np.uint8)
    n = len(raw) // (_HASH_W * _HASH_H)
    grays = raw[: n * _HASH_W * _HASH_H].reshape(n, _HASH_H, _HASH_W)
    paths = sorted(out_dir.glob("frame_*.jpg"))
    count = min(len(paths), n, len(times)) if times else min(len(paths), n)
    base = (start or 0.0) + offset
    frames = []
    for i in range(count):
        # -ss before -i resets timestamps to 0, so pts_time is relative to start.
        t = times[i] if times else i * every
        frames.append(Frame(t=base + t, path=paths[i], dhash=_dhash(grays[i].astype(np.int16))))
    return frames


def mark_keyframes(frames: list[Frame], threshold: int = 6, max_gap: float = 60.0) -> list[Frame]:
    """Flag frames that differ from the last kept frame by > threshold bits.

    A frame is also kept if ``max_gap`` seconds passed since the last keyframe,
    so a long static stretch still gets periodic coverage.
    """
    last: Frame | None = None
    for f in frames:
        if last is None or hamming(f.dhash, last.dhash) > threshold or f.t - last.t >= max_gap:
            f.keyframe = True
            last = f
    return [f for f in frames if f.keyframe]
