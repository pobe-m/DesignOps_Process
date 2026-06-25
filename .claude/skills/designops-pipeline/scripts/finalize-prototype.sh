#!/usr/bin/env bash
# finalize-prototype.sh — the Step 5.6 quality gate, chained into one runnable check.
#
# After /generate-prototype builds the screens, this wraps the three quality gates so the
# audit can't be silently skipped:
#   1. validate_critique.py   — critique.json integrity (judge verdict caps score)   [if present]
#   2. audit_prototype.py     — the 11 objective gates (THE hard block)              [always]
#   3. validate_usability.py  — usability.json integrity (no fabricated testing)     [if present]
#
# The audit reads source files only — no build, no dev server, no GITHUB_TOKEN needed.
#
# By default it runs the audit with --strict (a skipped gate = a failure), which is correct on a
# COMPLETE full-pipeline build where every artifact (brand.config / intelligence / aesthetic /
# screen-inventory / edge-cases) sits in the output dir beside the prototype. On a partial run,
# pass --no-strict so legitimately-absent artifacts skip cleanly instead of blocking.
#
# Usage:
#   finalize-prototype.sh <prototype_dir> [--a11y AA|AAA] [--no-strict] [--report <path.md>]
#
# Exit 0 = all gates PASS · 1 = at least one gate BLOCKED.

set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

PROTO=""
A11Y=""
STRICT=1
REPORT=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --a11y)      A11Y="$2"; shift 2 ;;
    --no-strict) STRICT=0; shift ;;
    --strict)    STRICT=1; shift ;;
    --report)    REPORT="$2"; shift 2 ;;
    -h|--help)   sed -n '2,20p' "${BASH_SOURCE[0]}"; exit 0 ;;
    *)           PROTO="$1"; shift ;;
  esac
done

if [[ -z "$PROTO" || ! -d "$PROTO" ]]; then
  echo "[finalize] ✗ prototype dir not found: '${PROTO:-<none>}'" >&2
  echo "  usage: finalize-prototype.sh <prototype_dir> [--a11y AA|AAA] [--no-strict] [--report <path.md>]" >&2
  exit 1
fi

# OUT_DIR holds the upstream artifacts (output/) — it is the prototype's parent.
OUT_DIR="$(cd "$PROTO/.." && pwd)"
DOCS_DIR="$PROTO/docs"
[[ -z "$REPORT" ]] && REPORT="$DOCS_DIR/audit-report.md"

# a11y target: explicit flag wins, else read design_directives.a11y_target from the artifacts, else AA.
if [[ -z "$A11Y" ]]; then
  A11Y="$(python3 - "$OUT_DIR" <<'PY' 2>/dev/null || true
import json, sys
from pathlib import Path
out = Path(sys.argv[1])
for name in ("intelligence.json", "aesthetic.json"):
    p = out / name
    if not p.is_file():
        continue
    try:
        d = json.load(open(p))
    except Exception:
        continue
    # design_directives may sit at top level or nested under a key
    dd = d.get("design_directives") or d.get("directives") or {}
    t = (dd.get("a11y_target") or "").replace("AA_plus", "AAA").upper()
    if t in ("AA", "AAA"):
        print(t); break
PY
)"
  [[ -z "$A11Y" ]] && A11Y="AA"
fi

echo "════════════════════════════════════════"
echo "[finalize] Step 5.6 quality gate — prototype: $PROTO"
echo "[finalize] a11y=$A11Y · strict=$([[ $STRICT -eq 1 ]] && echo on || echo off) · artifacts: $OUT_DIR"
echo "════════════════════════════════════════"

FAIL=0

# ── 1. critique integrity (if the artifact exists) ────────────────────────────
CRITIQUE_JSON="$DOCS_DIR/critique.json"
if [[ -f "$CRITIQUE_JSON" ]]; then
  echo; echo "▶ 1/3 critique integrity (validate_critique.py)"
  if python3 "$SCRIPT_DIR/validate_critique.py" "$CRITIQUE_JSON"; then
    echo "  🟢 critique OK"
  else
    echo "  🔴 critique BLOCKED"; FAIL=1
  fi
else
  echo; echo "▶ 1/3 critique integrity — — skipped (no $CRITIQUE_JSON)"
fi

# ── 2. the audit gate (always — this is the hard block) ───────────────────────
echo; echo "▶ 2/3 audit gate (audit_prototype.py)"
AUDIT_ARGS=("$PROTO" --a11y "$A11Y" --report "$REPORT")
[[ $STRICT -eq 1 ]] && AUDIT_ARGS+=(--strict)
if python3 "$SCRIPT_DIR/audit_prototype.py" "${AUDIT_ARGS[@]}"; then
  echo "  🟢 audit PASS  → $REPORT"
else
  echo "  🔴 audit BLOCKED  → $REPORT"; FAIL=1
fi

# ── 3. usability integrity (if the artifact exists) ───────────────────────────
USABILITY_JSON="$OUT_DIR/usability.json"
RESEARCH_JSON="$OUT_DIR/research.json"
if [[ -f "$USABILITY_JSON" ]]; then
  echo; echo "▶ 3/3 usability integrity (validate_usability.py)"
  U_ARGS=("$USABILITY_JSON")
  [[ -f "$RESEARCH_JSON" ]] && U_ARGS+=("$RESEARCH_JSON")
  if python3 "$SCRIPT_DIR/validate_usability.py" "${U_ARGS[@]}"; then
    echo "  🟢 usability OK"
  else
    echo "  🔴 usability BLOCKED"; FAIL=1
  fi
else
  echo; echo "▶ 3/3 usability integrity — — skipped (no $USABILITY_JSON)"
fi

echo; echo "════════════════════════════════════════"
if [[ $FAIL -eq 0 ]]; then
  echo "[finalize] 🟢 ALL GATES PASS — ready for handoff"
else
  echo "[finalize] 🔴 BLOCKED — fix the gate(s) above, then re-run. (report: $REPORT)"
fi
echo "════════════════════════════════════════"
exit $FAIL
