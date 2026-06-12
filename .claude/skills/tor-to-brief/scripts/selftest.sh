#!/usr/bin/env bash
# selftest.sh — regression guard for the tor-to-brief scripts.
# Runs under macOS stock /bin/bash (3.2). Exits non-zero if any check fails.
#
#   bash .claude/skills/tor-to-brief/scripts/selftest.sh
#
# Covers the bugs we actually hit: bash-4-only syntax, the validate gate, and the
# agent-driven execution model (no claude -p recursion, --exec guard).

set -uo pipefail   # not -e: we want to run every check and tally failures

SCRIPTS_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(cd "$SCRIPTS_DIR/.." && pwd)"
RUN="$SCRIPTS_DIR/run_pipeline.sh"
VALIDATE="$SCRIPTS_DIR/validate_brief.py"
SAMPLE_TOR="$SKILL_DIR/references/sample-tor.md"

PASS=0 FAIL=0
ok()   { PASS=$((PASS+1)); echo "  ✓ $1"; }
bad()  { FAIL=$((FAIL+1)); echo "  ✗ $1"; }
TMP="$(mktemp -d -t tor-selftest.XXXXXX)"
trap 'rm -rf "$TMP"' EXIT

echo "── tor-to-brief selftest ─────────────────────────────"
echo "bash: $BASH_VERSION"

# ── T1. bash 3.2 compatibility ────────────────────────────────────────────────
echo "[T1] bash 3.2 compatibility"
for s in "$RUN" "$0"; do
  /bin/bash -n "$s" 2>/dev/null && ok "syntax: $(basename "$s")" || bad "syntax: $(basename "$s")"
done
# bash-4-only constructs that silently break on 3.2
if grep -nE '\$\{[A-Za-z_][A-Za-z_0-9]*(\^\^|,,)\}|\$\{![A-Za-z_]|(^|[^a-z])mapfile|readarray' "$RUN" >/dev/null 2>&1; then
  bad "bash-4-only syntax found in run_pipeline.sh:"; grep -nE '\$\{[A-Za-z_][A-Za-z_0-9]*(\^\^|,,)\}|\$\{![A-Za-z_]|mapfile|readarray' "$RUN" | sed 's/^/      /'
else
  ok "no bash-4-only syntax (\${,,}/\${^^}/\${!var}/mapfile)"
fi

# ── T2. validate_brief.py accepts a valid brief ───────────────────────────────
echo "[T2] validate gate — valid brief passes"
python3 - "$TMP/valid.json" <<'PY'
import json, sys
json.dump({
  "meta": {"project_name":"T","generated_at":"2026-06-12","source_file":"x","tor_confidence":"high"},
  "project_overview": {"objective":"o","scope":"s","out_of_scope":[]},
  "target_users": [{"persona":"p","context":"","pain_points":[]}],
  "core_features": [{"id":"F01","name":"f","description":"","priority":"Must","flows":[]}],
  "user_flows": [{"id":"UF01","name":"u","steps":[]}],
  "constraints": {"technical":[],"business":[],"regulatory":[],"timeline":""},
  "design_direction": {"context_preset":"consumer"},
  "success_metrics": [],
  "open_questions": [],
  "scoring_criteria": {"total_score":None,"passing_threshold":None,"categories":[],"minimum_viable":None},
}, open(sys.argv[1],"w"))
PY
python3 "$VALIDATE" "$TMP/valid.json" >/dev/null 2>&1 && ok "valid brief → exit 0" || bad "valid brief should pass but failed"

# ── T3. validate_brief.py rejects invalid briefs ──────────────────────────────
echo "[T3] validate gate — invalid briefs fail"
# missing a required top-level key
python3 -c "import json;d=json.load(open('$TMP/valid.json'));d.pop('core_features');json.dump(d,open('$TMP/no_features.json','w'))"
python3 "$VALIDATE" "$TMP/no_features.json" >/dev/null 2>&1 && bad "missing core_features should fail" || ok "missing required key → exit 1"
# bad preset
python3 -c "import json;d=json.load(open('$TMP/valid.json'));d['design_direction']['context_preset']='banana';json.dump(d,open('$TMP/bad_preset.json','w'))"
python3 "$VALIDATE" "$TMP/bad_preset.json" >/dev/null 2>&1 && bad "bad preset should fail" || ok "invalid context_preset → exit 1"
# bad priority
python3 -c "import json;d=json.load(open('$TMP/valid.json'));d['core_features'][0]['priority']='Urgent';json.dump(d,open('$TMP/bad_prio.json','w'))"
python3 "$VALIDATE" "$TMP/bad_prio.json" >/dev/null 2>&1 && bad "bad priority should fail" || ok "invalid priority → exit 1"
# placeholder preset from the schema template must NOT false-fail
python3 -c "import json;d=json.load(open('$TMP/valid.json'));d['design_direction']['context_preset']='government | healthcare | fintech | consumer';json.dump(d,open('$TMP/tmpl.json','w'))"
python3 "$VALIDATE" "$TMP/tmpl.json" >/dev/null 2>&1 && ok "schema-template placeholder preset → exit 0" || bad "placeholder preset should pass"

# ── T4. agent-driven prep mode: stages prompts, no recursion ──────────────────
echo "[T4] execution model — prep mode stages, no recursion"
if [ -f "$SAMPLE_TOR" ]; then
  OUT="$TMP/run"; mkdir -p "$OUT"
  CLAUDECODE=1 /bin/bash "$RUN" --tor "$SAMPLE_TOR" --out "$OUT" >"$OUT/log.txt" 2>&1
  rc=$?
  [ "$rc" = "0" ] && ok "prep run exit 0" || bad "prep run exit $rc"
  [ -f "$OUT/.prompt_step1.txt" ] && [ -f "$OUT/.prompt_step3.txt" ] && ok "both prompts staged" || bad "prompts not staged"
  grep -q "AGENT ACTIONS" "$OUT/log.txt" && ok "AGENT ACTIONS checklist printed" || bad "no AGENT ACTIONS block"
else
  bad "sample-tor.md missing — cannot run T4"
fi

# ── T5. --exec recursion guard refuses inside a session ───────────────────────
echo "[T5] execution model — --exec refused inside a session"
CLAUDECODE=1 /bin/bash "$RUN" --tor "$SAMPLE_TOR" --out "$TMP/run2" --exec >"$TMP/exec.log" 2>&1
rc=$?
{ [ "$rc" != "0" ] && grep -q "recursion" "$TMP/exec.log"; } && ok "--exec refused (exit $rc, recursion guard)" || bad "--exec should refuse inside CLAUDECODE session"

# ── result ────────────────────────────────────────────────────────────────────
echo "──────────────────────────────────────────────────────"
echo "PASS: $PASS   FAIL: $FAIL"
[ "$FAIL" = "0" ] && { echo "✓ selftest green"; exit 0; } || { echo "✗ selftest failed"; exit 1; }
