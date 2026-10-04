"""Download raw pages listed in tools/snapshot_urls.txt into raw/ (dev aid; runs in CI)."""
import hashlib, pathlib, re, sys, urllib.request

out = pathlib.Path("raw"); out.mkdir(exist_ok=True)
for url in pathlib.Path("tools/snapshot_urls.txt").read_text().split():
    name = re.sub(r"[^A-Za-z0-9]+", "_", url.split("//", 1)[1])[:120]
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (ptcg-analysis research bot)"})
    try:
        body = urllib.request.urlopen(req, timeout=60).read()
        (out / f"{name}.html").write_bytes(body)
        print("ok", len(body), url)
    except Exception as e:  # noqa: BLE001
        print("FAIL", url, e, file=sys.stderr)
