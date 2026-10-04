"""Small polite HTTP helper with an on-disk cache."""
from __future__ import annotations

import hashlib
import os
import pathlib
import time
import urllib.error
import urllib.request

USER_AGENT = "ptcg-analysis/0.1 (+https://github.com/litian80/ptcg-analysis)"
CACHE_DIR = pathlib.Path(os.environ.get("PTCG_CACHE", ".cache/http"))
DELAY = float(os.environ.get("PTCG_DELAY", "1.0"))

_last = 0.0


def get(url: str, *, cache: bool = True, retries: int = 4) -> str:
    """GET a URL and return the decoded body. Cached by URL under CACHE_DIR."""
    global _last
    path = CACHE_DIR / hashlib.sha1(url.encode()).hexdigest()
    if cache and path.exists():
        return path.read_text(encoding="utf-8")
    for attempt in range(retries):
        wait = _last + DELAY - time.monotonic()
        if wait > 0:
            time.sleep(wait)
        _last = time.monotonic()
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=120) as resp:
                body = resp.read().decode("utf-8", errors="replace")
            break
        except urllib.error.HTTPError as e:
            if e.code == 404 or attempt == retries - 1:
                raise
        except (urllib.error.URLError, TimeoutError):
            if attempt == retries - 1:
                raise
        time.sleep(2 ** (attempt + 1))
    if cache:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body, encoding="utf-8")
    return body
