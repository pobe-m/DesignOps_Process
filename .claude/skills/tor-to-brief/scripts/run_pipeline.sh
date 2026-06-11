#!/usr/bin/env bash
# tor-to-brief pipeline runner
# Usage:
#   Full pipeline:  run_pipeline.sh --tor <path> --ds <path> [--out <dir>] [--handoff <path>] [--brand <name>]
#   Step 1+2 only:  run_pipeline.sh --tor <path> [--out <dir>]
#   Step 3 only:    run_pipeline.sh --brief <path> --ds <path> [--out <dir>]
#   With bridge:    run_pipeline.sh --tor <path> --handoff <path/to/Hand-off-test> [--brand <name>]
#
# Env vars:
#   TOR_OUTPUT_DIR    — output directory (default: ./tor-output)
#   TOR_DS_PATH       — design system path override (default: ../shadcn-skills-design-starter)
#   TOR_HANDOFF_PATH  — Hand-off-test repo path (if set, runs the bridge automatically)
#   TOR_BRAND_NAME    — brand name for brand.config.json (default: poc-brand)

set -euo pipefail

# ── defaults ──────────────────────────────────────────────────────────────────
TOR_FILE=""
TOR_TEXT=""
DS_PATH=""
# Auto-resolve shadcn-skills-design-starter as default DS
# Lookup order: env var → in-repo vendored DS → project-root sibling
_resolve_default_ds() {
  # 1. env var override
  [[ -n "${TOR_DS_PATH:-}" ]] && { echo "$TOR_DS_PATH"; return; }
  # 2. in-repo vendored DS (./design-system) — self-contained default
  local project_root in_repo
  project_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)"
  in_repo="$project_root/design-system"
  [[ -d "$in_repo" ]] && { echo "$in_repo"; return; }
  # 3. project-root sibling (../shadcn-skills-design-starter) — fallback
  local sibling
  sibling="$(cd "$project_root" && cd .. && pwd)/shadcn-skills-design-starter"
  [[ -d "$sibling" ]] && { echo "$sibling"; return; }
  echo ""
}
BRIEF_JSON=""
OUT_DIR="${TOR_OUTPUT_DIR:-./tor-output}"
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# ── parse args ────────────────────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
  case $1 in
    --tor)       TOR_FILE="$2";  shift 2 ;;
    --tor-text)  TOR_TEXT="$2";  shift 2 ;;
    --ds)        DS_PATH="$2";   shift 2 ;;
    --brief)     BRIEF_JSON="$2"; shift 2 ;;
    --out)       OUT_DIR="$2";   shift 2 ;;
    --handoff)   export TOR_HANDOFF_PATH="$2";  shift 2 ;;
    --brand)     export TOR_BRAND_NAME="$2";    shift 2 ;;
    *) echo "[tor-to-brief] ERROR: unknown flag $1"; exit 1 ;;
  esac
done

# ── helpers ───────────────────────────────────────────────────────────────────
log()  { echo "[tor-to-brief] $*"; }
err()  { echo "[tor-to-brief] ERROR: $*" >&2; exit 1; }
step() { echo ""; echo "[tor-to-brief] ▶ $*"; echo "────────────────────────────────"; }

# ── validate inputs ───────────────────────────────────────────────────────────
if [[ -z "$TOR_FILE" && -z "$TOR_TEXT" && -z "$BRIEF_JSON" ]]; then
  err "you must provide at least one input:
  --tor <path>        TOR file (PDF or DOCX)
  --tor-text \"<text>\" TOR text directly
  --brief <path>      skip steps 1+2, use an existing brief.json"
fi

if [[ -n "$TOR_FILE" && ! -f "$TOR_FILE" ]]; then
  err "file not found: $TOR_FILE"
fi

if [[ -n "$BRIEF_JSON" && ! -f "$BRIEF_JSON" ]]; then
  err "file not found: $BRIEF_JSON"
fi

# ── setup output dir ──────────────────────────────────────────────────────────
mkdir -p "$OUT_DIR"
log "Output directory: $OUT_DIR"

# ── step 1+2: TOR → brief ─────────────────────────────────────────────────────
if [[ -z "$BRIEF_JSON" ]]; then
  step "Step 1+2 — Reading TOR & generating brief"

  # Build claude prompt context
  TOR_CONTEXT=""
  if [[ -n "$TOR_FILE" ]]; then
    EXT="${TOR_FILE##*.}"
    case "${EXT,,}" in
      pdf)
        log "Extracting text from PDF: $TOR_FILE"
        if command -v pdftotext &>/dev/null; then
          TOR_CONTEXT=$(pdftotext -layout "$TOR_FILE" - 2>/dev/null || true)
        fi
        if [[ -z "$TOR_CONTEXT" ]]; then
          log "pdftotext empty or unavailable — will pass file path to Claude directly"
          TOR_CONTEXT="[PDF_FILE:$TOR_FILE]"
        fi
        ;;
      docx)
        log "Extracting text from DOCX: $TOR_FILE"
        if command -v python3 &>/dev/null; then
          TOR_CONTEXT=$(python3 -c "
import sys
try:
    from docx import Document
    doc = Document('$TOR_FILE')
    print('\n'.join(p.text for p in doc.paragraphs if p.text.strip()))
except Exception as e:
    print('[DOCX_FILE:$TOR_FILE]')
" 2>/dev/null || echo "[DOCX_FILE:$TOR_FILE]")
        else
          TOR_CONTEXT="[DOCX_FILE:$TOR_FILE]"
        fi
        ;;
      md|txt)
        TOR_CONTEXT=$(cat "$TOR_FILE")
        ;;
      *)
        err "unsupported format: .$EXT (supported: pdf, docx, md, txt)"
        ;;
    esac
  elif [[ -n "$TOR_TEXT" ]]; then
    TOR_CONTEXT="$TOR_TEXT"
  fi

  # Write prompt file for Claude Code to execute
  PROMPT_FILE="$OUT_DIR/.prompt_step1.txt"
  cat > "$PROMPT_FILE" << PROMPT
Read the TOR below and produce 2 output files per the tor-to-brief SKILL.md:

1. Save "$OUT_DIR/brief.md" — Markdown for humans to review
2. Save "$OUT_DIR/brief.json" — JSON schema for the AI to consume next

Use the 8 main categories: PROJECT_OVERVIEW, TARGET_USERS, CORE_FEATURES, USER_FLOWS,
CONSTRAINTS, DESIGN_DIRECTION, SUCCESS_METRICS, OPEN_QUESTIONS

If the TOR doesn't state a category → set null, don't make it up.
A feature with no priority → default to Should.

TOR content:
---
$TOR_CONTEXT
---
PROMPT

  log "Prompt ready → $PROMPT_FILE"
  log "Claude Code will read this prompt and produce brief.md + brief.json"

  # In a Claude Code environment, use claude -p
  # When run standalone, the prompt is saved for manual processing
  if command -v claude &>/dev/null; then
    claude -p "$(cat "$PROMPT_FILE")" --output-format text > /dev/null
    log "Claude finished step 1+2"
  else
    log "claude CLI not found — prompt saved to $PROMPT_FILE"
    log "Run inside Claude Code so the AI processes it automatically"
  fi

  BRIEF_JSON="$OUT_DIR/brief.json"
fi

# ── validate brief.json ───────────────────────────────────────────────────────
if [[ -f "$BRIEF_JSON" ]]; then
  step "Validating brief.json"
  python3 "$SKILL_DIR/scripts/validate_brief.py" "$BRIEF_JSON" || {
    err "brief.json validation failed — fix it first, or re-run steps 1+2"
  }
  log "✓ brief.json valid"
else
  log "brief.json doesn't exist yet — Claude Code will create it after steps 1+2"
fi

# ── step 3: brief + DS → design draft ────────────────────────────────────────
# Auto-resolve DS if not provided
if [[ -z "$DS_PATH" ]]; then
  DS_PATH="$(_resolve_default_ds)"
  if [[ -n "$DS_PATH" ]]; then
    log "ℹ  --ds not provided → using default: $DS_PATH"
  fi
fi

if [[ -n "$DS_PATH" ]]; then
  step "Step 3 — Reading design system & generating first draft"

  # resolve github URL → clone
  if [[ "$DS_PATH" =~ ^https://github.com ]]; then
    CLONE_DIR="/tmp/tor-ds-repo"
    if [[ ! -d "$CLONE_DIR/.git" ]]; then
      log "Cloning design system repo..."
      git clone --depth 1 "$DS_PATH" "$CLONE_DIR"
    else
      log "Using cached clone at $CLONE_DIR"
    fi
    DS_PATH="$CLONE_DIR"
  fi

  [[ -d "$DS_PATH" ]] || err "design system directory not found: $DS_PATH"

  # Inventory DS structure
  log "Scanning design system at: $DS_PATH"
  DS_INVENTORY=$(python3 - "$DS_PATH" << 'PYEOF'
import os, sys, json

ds_path = sys.argv[1]
result = {"components": [], "tokens": {}, "has_storybook": False, "readme": ""}

# Find components
for search_dir in ["components", "src/components", "lib/components", "packages"]:
    full = os.path.join(ds_path, search_dir)
    if os.path.isdir(full):
        for root, dirs, files in os.walk(full):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules']
            for f in files:
                if f.endswith(('.tsx', '.jsx', '.vue', '.svelte')) and not f.endswith(('.test.tsx', '.spec.tsx', '.stories.tsx')):
                    name = f.replace('.tsx','').replace('.jsx','').replace('.vue','').replace('.svelte','')
                    if name not in result["components"] and not name.startswith('index'):
                        result["components"].append(name)
        break

# Find token files
for token_dir in ["tokens", "design-tokens", "src/tokens", "styles"]:
    full = os.path.join(ds_path, token_dir)
    if os.path.isdir(full):
        result["tokens"]["dir"] = token_dir
        result["tokens"]["files"] = [f for f in os.listdir(full) if f.endswith(('.json','.ts','.css','.scss'))]
        break

# Check for storybook
result["has_storybook"] = any(
    os.path.exists(os.path.join(ds_path, p))
    for p in [".storybook", "stories", "src/stories"]
)

# Read README
for readme in ["README.md", "readme.md", "CONTRIBUTING.md"]:
    p = os.path.join(ds_path, readme)
    if os.path.isfile(p):
        with open(p) as f:
            result["readme"] = f.read()[:2000]
        break

print(json.dumps(result, ensure_ascii=False, indent=2))
PYEOF
)

  # Write step 3 prompt
  PROMPT3_FILE="$OUT_DIR/.prompt_step3.txt"
  BRIEF_CONTENT=""
  [[ -f "$BRIEF_JSON" ]] && BRIEF_CONTENT=$(cat "$BRIEF_JSON")

  cat > "$PROMPT3_FILE" << PROMPT
Read the brief.json and design system inventory below, then produce "$OUT_DIR/design-first-draft.md"

brief.json:
$BRIEF_CONTENT

design system path: $DS_PATH
design system inventory:
$DS_INVENTORY

Produce design-first-draft.md containing:
1. Screen Inventory — all screens with priority (from core_features)
2. Screen Breakdown — per screen: purpose, user flow, layout, component usage (JSX), design decisions
3. Component Gap Report — components present in the DS vs ones that must be built
4. Token Usage Guide — design tokens to use in each context

If the design system is shadcn-skills-design-starter, read its root CLAUDE.md first.
CLAUDE.md describes component patterns, the Figma→Tailwind token map, and naming conventions.
The component list is in components/ui/ (52 in total).
The token reference is in .claude/skills/shadcn-ui-design/references/DESIGN.md

rules:
- Use only components that actually exist in the inventory
- If a component is missing → record it in the gap report as "🔴 Missing"
- A partially available component → "🟡 Partial" with a recommendation
- Don't invent components
PROMPT

  log "Prompt ready → $PROMPT3_FILE"

  if command -v claude &>/dev/null; then
    claude -p "$(cat "$PROMPT3_FILE")" --output-format text > /dev/null
    log "Claude finished step 3"
  else
    log "claude CLI not found — prompt saved to $PROMPT3_FILE"
  fi

else
  log "--ds not provided → skipping step 3"
  log "Run step 3 later with: run_pipeline.sh --brief $BRIEF_JSON --ds <path> --out $OUT_DIR"
fi

# ── step 4.5: token bridge → hand-off repo ───────────────────────────────────
TOKENS_JSON="$OUT_DIR/poc-delivery/design-system/tokens.json"
HANDOFF_PATH="${TOR_HANDOFF_PATH:-}"

if [[ -f "$TOKENS_JSON" && -n "$HANDOFF_PATH" ]]; then
  step "Step 4.5 — Bridging tokens to Hand-off repo (hex → oklch)"

  [[ -d "$HANDOFF_PATH" ]] || err "handoff directory not found: $HANDOFF_PATH"

  BRIDGE_SCRIPT="$SKILL_DIR/scripts/bridge-tokens.mjs"
  [[ -f "$BRIDGE_SCRIPT" ]] || err "bridge-tokens.mjs not found — check the skill directory"

  # dry-run first to preview
  log "Preview token conversion:"
  node "$BRIDGE_SCRIPT" \
    --tokens  "$TOKENS_JSON" \
    --handoff "$HANDOFF_PATH" \
    --brand   "${TOR_BRAND_NAME:-poc-brand}" \
    --dry-run

  # confirm, then run
  read -r -p "[tor-to-brief] Confirm updating brand.config.json? [y/N] " CONFIRM
  if [[ "${CONFIRM,,}" == "y" ]]; then
    node "$BRIDGE_SCRIPT" \
      --tokens  "$TOKENS_JSON" \
      --handoff "$HANDOFF_PATH" \
      --brand   "${TOR_BRAND_NAME:-poc-brand}"

    log "Running brand:build in handoff repo..."
    (cd "$HANDOFF_PATH" && npm run brand:build)
    log "✓ brand.css regenerated"
  else
    log "Skipped — you can run it later with:"
    log "  node $BRIDGE_SCRIPT --tokens $TOKENS_JSON --handoff $HANDOFF_PATH"
  fi

elif [[ -f "$TOKENS_JSON" && -z "$HANDOFF_PATH" ]]; then
  log "ℹ  tokens.json is ready but --handoff was not provided"
  log "  Run the bridge later with:"
  log "  node $SKILL_DIR/scripts/bridge-tokens.mjs \\"
  log "    --tokens  $TOKENS_JSON \\"
  log "    --handoff <path/to/Hand-off-test>"
fi

# ── final summary ─────────────────────────────────────────────────────────────
echo ""
echo "════════════════════════════════════════"
log "✓ Pipeline complete → $OUT_DIR/"
echo ""
for f in brief.md brief.json design-first-draft.md; do
  if [[ -f "$OUT_DIR/$f" ]]; then
    SIZE=$(wc -c < "$OUT_DIR/$f" | tr -d ' ')
    echo "  ✓ $f ($SIZE bytes)"
  else
    echo "  – $f (not generated yet)"
  fi
done
echo "════════════════════════════════════════"
