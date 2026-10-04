import shutil
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
FIXTURES = Path(__file__).parent / "fixtures"


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
