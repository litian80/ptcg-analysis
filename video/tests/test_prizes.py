import json
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pytest

from ptcg_video import cli
from ptcg_video.frames import Frame
from ptcg_video.prizes import (PRIZE_FAMILIES, PRIZE_PRESETS, count_column, describe, prize_games, prize_timeline,
                                read_prizes, read_prizes_auto)

SIDES = PRIZE_PRESETS["sides"]
BALTIMORE = PRIZE_PRESETS["sides-baltimore"]
LIT, DARK = 140, 50  # mean gray of a lit ball and an empty slot on the real overlay: 115-165 and 38-65


def column(n: int, lit: int = LIT, dark: int = DARK, gap: int | None = None, layout=SIDES) -> np.ndarray:
    """One panel's prize column with n lit balls from the top (gap: ball index left dark)."""
    col = np.full((layout.height, 24), dark, dtype=np.uint8)
    for k in range(n):
        if k != gap:
            y = layout.y0 + layout.pitch * k
            col[y : y + layout.ball] = lit
    return col


def test_count_column():
    assert [count_column(column(n), SIDES) for n in range(7)] == [0, 1, 2, 3, 4, 5, 6]


def test_count_column_rejects_what_is_not_the_board():
    assert count_column(column(4, gap=1), SIDES) is None  # lit balls must fill from the top
    assert count_column(column(6, lit=235), SIDES) is None  # a white pop-up card over the column
    assert count_column(column(2, dark=10), SIDES) is None  # black break screen
    assert count_column(column(3, dark=95), SIDES) is None  # a lighter background, e.g. a desk shot
    mixed = column(3, lit=190, dark=107)  # the Baltimore overlay read with the Frankfurt preset:
    assert count_column(mixed, SIDES) is None  # its empty slots pass as balls, but far darker than the lit ones
    assert count_column(column(3, lit=185, dark=107, layout=BALTIMORE), BALTIMORE) == 3
    # NAIC 2026 uses the Baltimore overlay with darker empty slots (76-97).
    assert count_column(column(2, lit=170, dark=76, layout=BALTIMORE), BALTIMORE) == 2


def frames_with(readings, every=5.0):
    return [Frame(t=i * every, path=Path(f"f{i}.jpg"), prizes=r) for i, r in enumerate(readings)]


def test_timeline_needs_two_samples_and_ignores_replays():
    readings = [(6, 6), (6, 6), (5, 6), (6, 4),  # a one-sample misread changes nothing
                (5, 6), (5, 6), None, (5, 4), (5, 4),
                (6, 6), (6, 6), (6, 6),  # a short replay of the opening board
                (5, 4), (3, 4), (3, 4)]
    changes = prize_timeline(frames_with(readings))
    assert [(c.left, c.right) for c in changes] == [(6, 6), (5, 6), (5, 4), (3, 4)]
    assert [c.t for c in changes] == [0, 20, 35, 65]
    assert [describe(c, changes[i - 1] if i else None) for i, c in enumerate(changes)] == [
        "", "left took 1", "right took 2", "left took 2"]
    assert {c.game for c in changes} == {1}


def test_timeline_new_game_when_counts_hold_high():
    readings = [(2, 1)] * 3 + [(6, 6)] * 14 + [(6, 5)] * 2
    changes = prize_timeline(frames_with(readings))
    assert [(c.left, c.right, c.game) for c in changes] == [(2, 1, 1), (6, 6, 2), (6, 5, 2)]
    assert changes[1].t == 15  # first sample of the new game, not when it was confirmed
    assert describe(changes[1], changes[0]) == "new game"
    assert prize_games(changes) == [(0, 15), (15, None)]


def test_timeline_short_fresh_board_is_a_new_game_but_other_rises_are_not():
    # A 30 s replay of an earlier mid-game count is not a game; a fresh 6-6 board for 20 s
    # (a sudden-death game) is.
    readings = [(1, 1)] * 2 + [(4, 4)] * 7 + [None] * 3 + [(6, 6)] * 5 + [(5, 6)] * 2
    changes = prize_timeline(frames_with(readings))
    assert [(c.left, c.right, c.game) for c in changes] == [(1, 1, 1), (6, 6, 2), (5, 6, 2)]


def test_timeline_never_opens_a_game_on_a_zero():
    # NAIC 2026 final: the pre-match player cam read as 0-2 for a minute before the first board.
    readings = [(0, 2)] * 12 + [None] * 4 + [(6, 6)] * 5 + [(5, 6)] * 2
    changes = prize_timeline(frames_with(readings))
    assert [(c.left, c.right, c.game) for c in changes] == [(6, 6, 1), (5, 6, 1)]
    # Mid-game, a count reaching 0 still ends the game as before.
    changes = prize_timeline(frames_with([(2, 1)] * 2 + [(2, 0)] * 2 + [(6, 6)] * 5))
    assert [(c.left, c.right, c.game) for c in changes] == [(2, 1, 1), (2, 0, 1), (6, 6, 2)]


def test_timeline_change_time_range_when_the_panel_was_hidden():
    # A knockout at about 0:20, then a pop-up covers the panel until 0:45.
    readings = [(3, 2)] * 4 + [None] * 5 + [(1, 2)] * 3
    changes = prize_timeline(frames_with(readings))
    assert [(c.after, c.t) for c in changes] == [(None, 0), (15, 45)]
    assert changes[1].to_dict()["after"] == 15


REPLAY_BLUE = (109, 174, 223)  # the REPLAY banner on the Frankfurt stream


def _jpeg(img: np.ndarray, path: Path) -> Path:
    subprocess.run(
        ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
         "-s", "1280x720", "-i", "-", "-q:v", "3", str(path)],
        input=img.tobytes(), check=True,
    )
    return path


@pytest.fixture
def overlay_frames(tmp_path):
    """1280x720 JPEGs of the sides overlay: prize columns at 6-6, then 4-5, then a white pop-up over them,
    then 2-3 under the REPLAY banner, then a stadium banner of another colour in the same place, then a
    full-screen transition in the banner's blue."""
    if not shutil.which("ffmpeg"):
        pytest.skip("ffmpeg not installed")
    paths = []
    for i, (left, right) in enumerate([(6, 6), (4, 5), (6, 6), (2, 3), (4, 5), (4, 5)]):
        img = np.full((720, 1280, 3), 70, dtype=np.uint8)  # the hand-cam and panels around the columns
        for (x0, x1), n in zip(SIDES.columns, (left, right)):
            img[: SIDES.height, x0 - 4 : x1 + 4] = DARK
            img[: SIDES.height, x0:x1] = column(n)[:, : x1 - x0, None]
        if i == 2:
            img[:300, 200:420] = 240
        if i == 3:
            img[26:53, 552:727] = REPLAY_BLUE
            img[32:48, 610:672] = 250  # the white "REPLAY" text
        if i == 4:
            img[26:53, 552:727] = (150, 90, 160)
        if i == 5:
            img[:, :] = REPLAY_BLUE
        paths.append(_jpeg(img, tmp_path / f"frame_{i + 1:05d}.jpg"))
    return [Frame(t=i * 5.0, path=p) for i, p in enumerate(paths)]


def test_read_prizes_from_jpegs(overlay_frames, tmp_path):
    read_prizes(overlay_frames, SIDES)
    assert [f.prizes for f in overlay_frames] == [(6, 6), (4, 5), None, None, (4, 5), None]
    assert [f.replay for f in overlay_frames] == [False, False, False, True, False, False]
    assert overlay_frames[1].to_dict()["prizes"] == [4, 5]
    assert overlay_frames[3].to_dict()["replay"] is True and "replay" not in overlay_frames[1].to_dict()

    from ptcg_video.events import CaptionAnalysis
    from ptcg_video.report import write_review_pack

    for f in overlay_frames:
        f.keyframe = True
    pack = write_review_pack(tmp_path, {"title": "t"}, [], CaptionAnalysis(), overlay_frames, window=60,
                             max_frames=10).read_text(encoding="utf-8")
    assert "frame_00004.jpg` (replay)" in pack and "frame_00002.jpg` (replay)" not in pack


def test_auto_keeps_the_preset_that_reads_the_overlay(overlay_frames, tmp_path):
    presets = {n: PRIZE_PRESETS[n] for n in PRIZE_FAMILIES["sides"]}
    assert read_prizes_auto(overlay_frames, presets) == "sides"
    assert [f.prizes for f in overlay_frames] == [(6, 6), (4, 5), None, None, (4, 5), None]
    assert [f.replay for f in overlay_frames] == [False, False, False, True, False, False]

    frames = []  # the Baltimore Day 1 overlay: smaller balls on a lighter panel
    for i, (left, right) in enumerate([(6, 6), (5, 6), (3, 4)]):
        img = np.full((720, 1280, 3), 70, dtype=np.uint8)
        for (x0, x1), n in zip(BALTIMORE.columns, (left, right)):
            img[: BALTIMORE.height, x0 - 4 : x1 + 4] = 107
            img[: BALTIMORE.height, x0:x1] = column(n, lit=185, dark=107, layout=BALTIMORE)[:, : x1 - x0, None]
        frames.append(Frame(t=i * 5.0, path=_jpeg(img, tmp_path / f"baltimore_{i}.jpg")))
    assert read_prizes_auto(frames, presets) == "sides-baltimore"
    assert [f.prizes for f in frames] == [(6, 6), (5, 6), (3, 4)]

    frames = []  # NAIC 2026: the Baltimore overlay with darker empty slots, 76-97
    for i, (left, right) in enumerate([(6, 6), (5, 6), (3, 4), (1, 2)]):
        img = np.full((720, 1280, 3), 70, dtype=np.uint8)
        for (x0, x1), n, dark in zip(BALTIMORE.columns, (left, right), (76, 97)):
            img[: BALTIMORE.height, x0 - 4 : x1 + 4] = dark
            img[: BALTIMORE.height, x0:x1] = column(n, lit=170, dark=dark, layout=BALTIMORE)[:, : x1 - x0, None]
        frames.append(Frame(t=i * 5.0, path=_jpeg(img, tmp_path / f"naic_{i}.jpg")))
    assert read_prizes_auto(frames, presets) == "sides-baltimore"
    assert [f.prizes for f in frames] == [(6, 6), (5, 6), (3, 4), (1, 2)]


def _box(x: int, y: int, w: int, h: int, gray: int, when: str = "") -> str:
    color = f"0x{gray:02x}{gray:02x}{gray:02x}"
    return f"drawbox=x={x}:y={y}:w={w}:h={h}:color={color}:t=fill" + (f":enable='{when}'" if when else "")


def test_cli_reads_prizes_on_sides_overlay(tmp_path):
    """40 s of a sides overlay: the left player takes 2 prizes at 15 s, the right player 1 at 30 s."""
    if not shutil.which("ffmpeg"):
        pytest.skip("ffmpeg not installed")
    boxes = []
    for (x0, x1), dark_after in zip(SIDES.columns, ({4: 15, 5: 15}, {5: 30})):
        boxes.append(_box(x0 - 4, 0, x1 - x0 + 8, SIDES.height, DARK))
        for k in range(6):
            y = SIDES.y0 + SIDES.pitch * k
            boxes.append(_box(x0, y, x1 - x0, SIDES.ball, LIT, f"lt(t,{dark_after[k]})" if k in dark_after else ""))
    video = tmp_path / "overlay.mp4"
    subprocess.run(
        ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi", "-i", "color=c=0x464646:s=1280x720:d=40:r=5",
         "-vf", ",".join(boxes), "-c:v", "libx264", "-crf", "23", "-pix_fmt", "yuv420p", str(video)],
        check=True,
    )
    out = tmp_path / "out"
    assert cli.main(["analyze", str(video), "--captions", str(Path(__file__).parent / "fixtures" / "simple.srt"),
                     "--hash-regions", "sides", "--every", "5", "--no-llm", "--out", str(out)]) == 0
    prizes = json.loads((out / "overlay" / "prizes.json").read_text(encoding="utf-8"))
    assert [(c["t"], c["left"], c["right"]) for c in prizes] == [(0, 6, 6), (15, 4, 6), (30, 4, 5)]
    report = (out / "overlay" / "report.md").read_text(encoding="utf-8")
    assert "## Prizes left (from the overlay)" in report and "left took 2" in report
    pack = (out / "overlay" / "review_pack.md").read_text(encoding="utf-8")
    assert "Prizes left → 4 / 5 at 0:30 (right took 1)" in pack

    off = tmp_path / "off"
    assert cli.main(["analyze", str(video), "--captions", str(Path(__file__).parent / "fixtures" / "simple.srt"),
                     "--hash-regions", "sides", "--prizes", "off", "--no-llm", "--out", str(off)]) == 0
    assert not (off / "overlay" / "prizes.json").exists()


def test_report_games_from_prizes_and_time_ranges(tmp_path):
    from ptcg_video.events import CaptionAnalysis
    from ptcg_video.report import write_outputs, write_review_pack

    readings = [(6, 6)] * 4 + [None] * 4 + [(4, 6)] * 4 + [(6, 6)] * 6 + [(6, 5)] * 3
    frames = frames_with(readings)
    for f in frames:
        f.keyframe = True
    captions = CaptionAnalysis(games=[(0.0, None)])  # the commentary found one game; the prizes find two
    meta = {"title": "t", "url": "https://youtu.be/x?v=1"}
    report = write_outputs(tmp_path, meta, [], captions, frames, [], None).read_text(encoding="utf-8")
    assert "## Games (from prize markers)" in report
    assert "- Game 2: [1:00]" in report
    assert "| [0:15](https://youtu.be/x?v=1&t=15s) - 0:40 | 1 | 4 | 6 | left took 2 |" in report
    pack = write_review_pack(tmp_path, meta, [], captions, frames, window=30).read_text(encoding="utf-8")
    assert "Prizes left → 4 / 6 between 0:15 and 0:40 (left took 2)" in pack
    assert "(game 2)" in pack

    meta["games_from"] = "--games"
    report = write_outputs(tmp_path, meta, [], captions, frames, [], None).read_text(encoding="utf-8")
    assert "## Games (from --games)" in report and "Game 2" not in report
