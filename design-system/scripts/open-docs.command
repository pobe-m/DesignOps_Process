#!/usr/bin/env bash
#
# Serve the static component-docs export (out/) on a local port and open it in
# the browser. Fully offline — no internet required. Press Ctrl+C to stop.
#
# Double-click this file in Finder, or run `npm run docs:offline`.

set -e
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SITE="$ROOT/out"
PORT="${PORT:-4321}"

if [ ! -f "$SITE/index.html" ]; then
  echo "Static export not found — building it now (npm run build)…"
  (cd "$ROOT" && npm run build)
fi

echo ""
echo "  Component docs (offline) → http://localhost:$PORT/docs/"
echo "  Keep this window open while viewing. Press Ctrl+C to stop."
echo ""

( sleep 1; open "http://localhost:$PORT/docs/" >/dev/null 2>&1 || true ) &
exec python3 -m http.server "$PORT" --directory "$SITE"
