import shutil
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture(autouse=True)
def _no_card_env(monkeypatch):
    """A PTCG_CARD_NAMES set on the developer's machine must not leak into tests."""
    monkeypatch.delenv("PTCG_CARD_NAMES", raising=False)


@pytest.fixture(scope="session")
def board_video(tmp_path_factory):
    """30 s video with three 'board states': a box on the left, right, then left again."""
    if not shutil.which("ffmpeg"):
        pytest.skip("ffmpeg not installed")
    path = tmp_path_factory.mktemp("video") / "match.mp4"
    filt = (
        "[0:v]drawbox=x=40:y=60:w=200:h=240:color=white:t=fill[a];"
        "[1:v]drawbox=x=400:y=60:w=200:h=240:color=white:t=fill[b];"
        "[2:v]drawbox=x=40:y=60:w=200:h=240:color=white:t=fill,"
        "drawbox=x=300:y=200:w=100:h=100:color=yellow:t=fill[c];"
        "[a][b][c]concat=n=3:v=1:a=0[v]"
    )
    src = ["-f", "lavfi", "-i", "color=c=darkgreen:s=640x360:d=10:r=10"]
    subprocess.run(
        ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *src, *src, *src,
         "-filter_complex", filt, "-map", "[v]", "-pix_fmt", "yuv420p", str(path)],
        check=True,
    )
    return path


@pytest.fixture(scope="session")
def broadcast_video(tmp_path_factory):
    """30 s 'broadcast': static side panels, a hand-cam bar in the middle that
    moves every 2 s, and one change in the left panel at t=20."""
    if not shutil.which("ffmpeg"):
        pytest.skip("ffmpeg not installed")
    path = tmp_path_factory.mktemp("video") / "broadcast.mp4"
    filt = (
        "[0:v]drawbox=x=10:y=40:w=110:h=60:color=white:t=fill,"
        "drawbox=x=520:y=200:w=110:h=60:color=white:t=fill,"
        "drawbox=x=10:y=220:w=110:h=90:color=red:t=fill:enable='gte(t,20)'[base];"
        "[base][1:v]overlay=x='150+mod(floor(t/2),3)*110':y=0:eval=frame[v]"
    )
    subprocess.run(
        ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
         "-f", "lavfi", "-i", "color=c=darkblue:s=640x360:d=30:r=10",
         "-f", "lavfi", "-i", "color=c=yellow:s=120x360:d=30:r=10",
         "-filter_complex", filt, "-map", "[v]", "-pix_fmt", "yuv420p", str(path)],
        check=True,
    )
    return path


def _overlay_video(path: Path, extra: str = "") -> Path:
    first = path.with_name(path.stem + "_first.mp4")
    filt = (
        "[0:v]format=gray,geq=lum='30+4*X/W+3*sin(Y/40)+2*cos(X/90)',format=yuv420p,"
        # HP bar: 60 px wide until t=20, then 20 px.
        "drawbox=x=20:y=60:w=60:h=8:color=green:t=fill:enable='lt(t,20)',"
        "drawbox=x=20:y=60:w=20:h=8:color=green:t=fill:enable='gte(t,20)',"
        # Six prize icons on the right panel; the last two go at t=40.
        "drawbox=x=520:y=250:w=16:h=22:color=white:t=fill,drawbox=x=540:y=250:w=16:h=22:color=white:t=fill,"
        "drawbox=x=560:y=250:w=16:h=22:color=white:t=fill,drawbox=x=580:y=250:w=16:h=22:color=white:t=fill,"
        "drawbox=x=520:y=276:w=16:h=22:color=white:t=fill:enable='lt(t,40)',"
        "drawbox=x=540:y=276:w=16:h=22:color=white:t=fill:enable='lt(t,40)'"
        + extra + "[base];"
        "[base][1:v]overlay=x='150+mod(floor(t/2),3)*110':y=0:eval=frame[v]"
    )
    subprocess.run(
        ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
         "-f", "lavfi", "-i", "color=c=black:s=640x360:d=60:r=10",
         "-f", "lavfi", "-i", "testsrc2=s=120x360:d=60:r=10",
         "-filter_complex", filt, "-map", "[v]", "-c:v", "libx264", "-crf", "23", "-pix_fmt", "yuv420p", str(first)],
        check=True,
    )
    subprocess.run(
        ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(first),
         "-vf", "scale=1280:720", "-c:v", "libx264", "-crf", "32", "-pix_fmt", "yuv420p", str(path)],
        check=True,
    )
    return path


@pytest.fixture(scope="session")
def overlay_video(tmp_path_factory):
    """60 s 'broadcast' with noisy, gradient side panels (re-encoded twice, like
    YouTube) and small overlay changes: an HP bar shrinks at t=20, two prize
    icons disappear at t=40. A hand-cam bar moves in the middle every 2 s."""
    if not shutil.which("ffmpeg"):
        pytest.skip("ffmpeg not installed")
    return _overlay_video(tmp_path_factory.mktemp("video") / "overlay.mp4")


@pytest.fixture(scope="session")
def live_overlay_video(tmp_path_factory):
    """overlay_video plus what real Worlds overlays do: both panel borders glow
    on and off (period 3.4 s), and a zoomed card pops up over the left panel
    from 33 s to 37 s."""
    if not shutil.which("ffmpeg"):
        pytest.skip("ffmpeg not installed")
    glow = "enable='lt(mod(t,3.4),1.7)'"
    extra = (
        f",drawbox=x=4:y=4:w=124:h=352:color=white:t=4:{glow}"
        f",drawbox=x=510:y=4:w=124:h=352:color=white:t=4:{glow}"
        ",drawbox=x=10:y=40:w=110:h=260:color=orange:t=fill:enable='between(t,33,37)'"
    )
    return _overlay_video(tmp_path_factory.mktemp("video") / "live.mp4", extra)


@pytest.fixture
def data_dir(tmp_path):
    """A minimal copy of the repo's data/ layout: two seasons and their pools."""
    root = tmp_path / "data"
    (root / "formats" / "2025-26").mkdir(parents=True)
    (root / "formats" / "2026-27").mkdir(parents=True)
    (root / "formats" / "standard_rotations.json").write_text(
        '{"seasons": ['
        '{"id": "2025-26", "tournament_start": "2025-04-11", "tcg_live_start": "2025-03-27"},'
        '{"id": "2026-27", "tournament_start": "2026-04-10", "tcg_live_start": "2026-03-26"}]}',
        encoding="utf-8",
    )
    (root / "formats" / "2025-26" / "card_pool.csv").write_text(
        "name,supertype\nCharizard ex,Pokémon\nCharizard ex,Pokémon\nIono,Trainer\nJudge,Trainer\n", encoding="utf-8"
    )
    (root / "formats" / "2026-27" / "card_pool.csv").write_text(
        "name,supertype\nDragapult ex,Pokémon\nAlakazam,Pokémon\nJudge,Trainer\nSpecial Red Card,Trainer\n",
        encoding="utf-8",
    )
    return root
