"""Sample frames from a match video and keep the ones where the board changed.

One ffmpeg pass writes a JPEG every ``every`` seconds and, alongside it, small
grayscale thumbnails of one or more regions of the frame. A frame is a
keyframe when enough thumbnail pixels changed (by more than a dead band, which
absorbs compression noise) since the last keyframe and the change is still there
in the next sample; frames that look the same (players thinking, commentary
over a static table) are skipped. Pixels that change in most samples (a glowing
panel border, an animated empty Bench slot) are ignored, and so are one-sample
pop-ups (a zoomed card, a "PRIZES" banner) because they do not persist.

Which regions to watch matters. Official Play! Pokémon streams draw each
player's board as a digital overlay down the sides of the screen, with a live
hand-cam in the middle that moves constantly. Watching only the side panels
(``--hash-regions sides``) keeps the frames where the board actually changed:
a prize taken, HP dropping, a new Pokémon benched.
"""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

_PTS = re.compile(r"pts_time:([0-9.]+)")

# (x, y, w, h) as fractions of the frame.
Region = tuple[float, float, float, float]

# Pixel differences at or below this many gray levels are compression noise.
DEAD_BAND = 8
# A pixel that changed in more than this share of consecutive samples is an
# animation, not the board.
ANIMATED = 0.4
# Sample pairs where more than this share of a region changed are cuts or
# pop-ups; they say nothing about which pixels animate.
CUT = 0.25


@dataclass(frozen=True)
class HashLayout:
    regions: tuple[Region, ...]
    thumb: tuple[int, int]  # (width, height) each region is shrunk to
    # Fraction of a region's thumbnail pixels that must change for a frame to
    # count as a board change; the whole-frame view must not fire on the
    # camera's normal movement.
    threshold: float = 0.05
    # Gray levels a pixel must move by to count as changed. Broadcast overlays
    # have fine text and glow that compress noisily, so they need more.
    dead_band: int = DEAD_BAND


REGION_PRESETS: dict[str, HashLayout] = {
    "full": HashLayout(((0.0, 0.0, 1.0, 1.0),), (64, 36), threshold=0.05),
    # Play! Pokémon broadcast overlay: one tall panel per player at each side.
    # Calibrated on the Worlds 2026 Masters final: real board changes move 7-65%
    # of a panel, a slow overlay animation that survives the steadiness check
    # about 1%, and 30 levels / 2% kept every change with the fewest frames.
    "sides": HashLayout(((0.0, 0.0, 0.21, 1.0), (0.79, 0.0, 0.21, 1.0)), (32, 96), threshold=0.02, dead_band=30),
}


def parse_regions(spec: str) -> HashLayout:
    """A preset name, or 'x,y,w,h;x,y,w,h' in fractions of the frame."""
    if spec in REGION_PRESETS:
        return REGION_PRESETS[spec]
    regions = []
    for part in spec.split(";"):
        try:
            x, y, w, h = (float(v) for v in part.split(","))
        except ValueError:
            raise ValueError(f"bad region {part!r}: expected x,y,w,h fractions or one of {sorted(REGION_PRESETS)}")
        if not (0 <= x < 1 and 0 <= y < 1 and 0 < w <= 1 - x + 1e-9 and 0 < h <= 1 - y + 1e-9):
            raise ValueError(f"region {part!r} is outside the frame")
        regions.append((x, y, w, h))
    tall = all(h / w >= 2 for _, _, w, h in regions)
    return HashLayout(tuple(regions), (32, 96) if tall else (64, 36), threshold=0.02, dead_band=30)


@dataclass
class Frame:
    t: float  # seconds in original-video time
    path: Path
    thumbs: tuple[np.ndarray, ...] = field(default=(), repr=False)  # one grayscale thumbnail per region
    keyframe: bool = False
    # Largest changed fraction of any region against the previous keyframe, to
    # help tune --change-threshold.
    change: float = 0.0

    def to_dict(self) -> dict:
        return {"t": round(self.t, 2), "path": str(self.path), "keyframe": self.keyframe,
                "change": round(self.change, 4)}


def _changed(a: np.ndarray, b: np.ndarray, dead_band: int = DEAD_BAND) -> np.ndarray:
    return np.abs(a.astype(np.int16) - b.astype(np.int16)) > dead_band


def changed_fraction(a: np.ndarray, b: np.ndarray, dead_band: int = DEAD_BAND, ignore: np.ndarray | None = None) -> float:
    """Share of pixels that differ by more than the noise dead band (minus ignored ones)."""
    changed = _changed(a, b, dead_band)
    if ignore is not None:
        changed &= ~ignore
    return float(np.mean(changed))


def animated_pixels(frames: list[Frame], dead_band: int = DEAD_BAND, min_pairs: int = 6) -> list[np.ndarray | None]:
    """Per region, the pixels that change between most consecutive samples."""
    if len(frames) < 2 or not frames[0].thumbs:
        return []
    masks: list[np.ndarray | None] = []
    for r in range(len(frames[0].thumbs)):
        counts = np.zeros(frames[0].thumbs[r].shape, dtype=np.int32)
        pairs = 0
        for a, b in zip(frames, frames[1:]):
            changed = _changed(a.thumbs[r], b.thumbs[r], dead_band)
            if changed.mean() <= CUT:
                counts += changed
                pairs += 1
        masks.append(counts > ANIMATED * pairs if pairs >= min_pairs else None)
    return masks


def _filter(every: float, width: int, layout: HashLayout) -> str:
    tw, th = layout.thumb
    n = len(layout.regions)
    labels = "".join(f"[r{i}]" for i in range(n))
    # select (not fps) so each output frame is the input frame at that time and
    # showinfo reports its real timestamp; fps would emit the frame nearest the
    # middle of each interval, about every/2 later than the reported time.
    pick = f"select='isnan(prev_selected_t)+gte(t-prev_selected_t\\,{every - 0.001:.3f})'"
    parts = [f"[0:v]{pick},showinfo,split={n + 1}[full]{labels}", f"[full]scale={width}:-2[out]"]
    for i, (x, y, w, h) in enumerate(layout.regions):
        parts.append(f"[r{i}]crop=iw*{w}:ih*{h}:iw*{x}:ih*{y},scale={tw}:{th}:flags=area,format=gray[h{i}]")
    if n == 1:
        parts.append("[h0]null[hash]")
    else:
        parts.append("".join(f"[h{i}]" for i in range(n)) + f"hstack=inputs={n}[hash]")
    return ";".join(parts)


def sample_frames(
    video: str | Path,
    out_dir: str | Path,
    every: float = 5.0,
    start: float | None = None,
    end: float | None = None,
    offset: float = 0.0,
    width: int = 1280,
    layout: HashLayout = REGION_PRESETS["full"],
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
        "-filter_complex", _filter(every, width, layout),
        "-map", "[out]", "-fps_mode", "passthrough", "-q:v", "3", str(out_dir / "frame_%05d.jpg"),
        "-map", "[hash]", "-fps_mode", "passthrough", "-f", "rawvideo", "-",
    ]
    proc = subprocess.run(cmd, capture_output=True)
    if proc.returncode != 0:
        raise RuntimeError(f"ffmpeg failed:\n{proc.stderr.decode(errors='replace')[-2000:]}")
    times = [float(m) for m in _PTS.findall(proc.stderr.decode(errors="replace"))]
    tw, th = layout.thumb
    n_regions = len(layout.regions)
    per_frame = tw * th * n_regions
    raw = np.frombuffer(proc.stdout, dtype=np.uint8)
    n = len(raw) // per_frame
    grays = raw[: n * per_frame].reshape(n, th, tw * n_regions)
    paths = sorted(out_dir.glob("frame_*.jpg"))
    count = min(len(paths), n, len(times)) if times else min(len(paths), n)
    base = (start or 0.0) + offset
    frames = []
    for i in range(count):
        # -ss before -i resets timestamps to 0, so pts_time is relative to start.
        t = times[i] if times else i * every
        thumbs = tuple(grays[i][:, r * tw : (r + 1) * tw].copy() for r in range(n_regions))
        frames.append(Frame(t=base + t, path=paths[i], thumbs=thumbs))
    return frames


def mark_keyframes(
    frames: list[Frame],
    threshold: float = 0.05,
    max_gap: float = 60.0,
    dead_band: int = DEAD_BAND,
    steady: bool = True,
) -> list[Frame]:
    """Flag frames where a watched region changed since the last kept frame.

    ``threshold`` is the fraction of a region's thumbnail pixels that must
    change (use the layout's ``threshold`` and ``dead_band`` unless tuning).
    With ``steady``, animated pixels are ignored and a region's change must
    still be there in the next sample, so one-sample pop-ups are skipped. A
    frame is also kept if ``max_gap`` seconds passed since the last keyframe,
    so a long static stretch still gets periodic coverage.
    """
    masks = animated_pixels(frames, dead_band) if steady else []

    def changes(f: Frame, ref: Frame) -> list[float]:
        return [
            changed_fraction(a, b, dead_band, masks[r] if r < len(masks) else None)
            for r, (a, b) in enumerate(zip(f.thumbs, ref.thumbs))
        ]

    last: Frame | None = None
    for i, f in enumerate(frames):
        f.keyframe, f.change = False, 0.0
        if last is None:
            f.keyframe = True
            last = f
            continue
        now = changes(f, last)
        f.change = max(now, default=0.0)
        moved = [c > threshold for c in now]
        if steady and any(moved) and i + 1 < len(frames):
            after = changes(frames[i + 1], last)
            moved = [m and c > threshold for m, c in zip(moved, after)]
        if any(moved) or f.t - last.t >= max_gap:
            f.keyframe = True
            last = f
    return [f for f in frames if f.keyframe]
