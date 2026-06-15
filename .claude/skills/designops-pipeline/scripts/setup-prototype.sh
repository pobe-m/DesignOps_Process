#!/usr/bin/env bash
# setup-prototype.sh — Step 4 base setup, fast + correct.
#
# Copies the design system into {OUT}/prototype and installs deps. Two speedups,
# both keeping a REAL node_modules (a symlinked/shared node_modules breaks tsc's
# @types/react resolution — proven, don't do it):
#   1. Reuse: if a prototype already has node_modules matching the current lockfile,
#      only the source is refreshed — no reinstall.
#   2. npm ci --prefer-offline: lockfile-exact, uses npm's own (~/.npm) cache, skips
#      audit/fund. The first install is the one-time cost; repeats are fast.
#
#   bash .claude/skills/designops-pipeline/scripts/setup-prototype.sh --out ./output [--ds ./design-system]
#
# bash 3.2 safe.

set -uo pipefail

DS="./design-system"
OUT="./output"
while [ $# -gt 0 ]; do
  case "$1" in
    --ds)  DS="$2"; shift 2 ;;
    --out) OUT="$2"; shift 2 ;;
    *) echo "[setup-prototype] ERROR: unknown flag $1" >&2; exit 1 ;;
  esac
done

log() { echo "[setup-prototype] $*"; }
err() { echo "[setup-prototype] ERROR: $*" >&2; exit 1; }

# resolve in-repo DS default if the given one is missing
if [ ! -d "$DS" ]; then
  SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
  ALT="$(cd "$SCRIPT_DIR/../../../.." && pwd)/design-system"
  [ -d "$ALT" ] && DS="$ALT" || err "design system not found: $DS"
fi
command -v rsync >/dev/null 2>&1 || err "rsync required"
command -v npm   >/dev/null 2>&1 || err "npm required"

PROTO="$OUT/prototype"
MARKER_REL="node_modules/.tor-lock-hash"

_lock_hash() {  # hash of the design-system lockfile (install fingerprint)
  local lock="$DS/package-lock.json"; [ -f "$lock" ] || lock="$DS/package.json"
  if command -v shasum >/dev/null 2>&1; then shasum "$lock" | awk '{print $1}'
  elif command -v sha1sum >/dev/null 2>&1; then sha1sum "$lock" | awk '{print $1}'
  else cksum "$lock" | awk '{print $1}'; fi
}

# Reusable only if it's a REAL dir (not a symlink) whose install fingerprint
# (marker we wrote) matches the current design-system lockfile.
_can_reuse() {
  [ -d "$PROTO/node_modules" ] || return 1
  [ -L "$PROTO/node_modules" ] && return 1   # never reuse a symlinked one
  [ -f "$PROTO/$MARKER_REL" ] || return 1
  [ "$(cat "$PROTO/$MARKER_REL" 2>/dev/null)" = "$(_lock_hash)" ]
}

if _can_reuse; then
  log "Reusing existing node_modules (lockfile matches) — refreshing source only ⚡"
  rsync -a --delete \
    --exclude node_modules --exclude .next --exclude out --exclude .git --exclude '.DS_Store' \
    "$DS"/ "$PROTO"/ || err "rsync failed"
else
  log "Copying design system → $PROTO"
  mkdir -p "$PROTO"
  rsync -a --delete-excluded \
    --exclude node_modules --exclude .next --exclude out --exclude .git --exclude '.DS_Store' \
    "$DS"/ "$PROTO"/ || err "rsync failed"

  log "Installing deps (npm ci --prefer-offline — first run is the slow one; repeats use npm's cache)…"
  if ! ( cd "$PROTO" && npm ci --prefer-offline --no-audit --no-fund ); then
    log "npm ci failed (lockfile out of sync?) — falling back to npm install"
    ( cd "$PROTO" && npm install --no-audit --no-fund ) || err "npm install failed"
  fi
  # fingerprint the install so the next run can reuse it
  _lock_hash > "$PROTO/$MARKER_REL"
fi

log "✓ prototype ready → $PROTO"
log "  cd $PROTO && npm run dev"
