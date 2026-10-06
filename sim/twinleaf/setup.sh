#!/usr/bin/env bash
# Clone Twinleaf at a pinned commit next to this script and compile it (no server, no DB needed).
# Usage: bash sim/twinleaf/setup.sh [target-dir]      (default: sim/twinleaf/.twinleaf)
set -euo pipefail
COMMIT=7bb457367c3431c18bbb53d1eef2f29591221ed8   # twinleafgg/twinleafgg main, 2026-10
DIR="${1:-$(cd "$(dirname "$0")" && pwd)/.twinleaf}"
if [ ! -d "$DIR/.git" ]; then
  git clone --filter=blob:limit=2m https://github.com/twinleafgg/twinleafgg.git "$DIR"
fi
git -C "$DIR" fetch --quiet origin "$COMMIT" || true
git -C "$DIR" checkout --quiet "$COMMIT"
cd "$DIR/ptcg-server"
npm install --ignore-scripts --no-audit --no-fund      # native modules (sqlite3) are not needed
node --max-old-space-size=8192 ./node_modules/typescript/bin/tsc   # ~2-3 min, writes ./output
echo "Twinleaf ready at $DIR (set TWINLEAF_DIR or pass --twinleaf if you moved it)"
