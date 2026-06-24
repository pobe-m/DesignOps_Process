#!/usr/bin/env python3
"""
lint_directive_fidelity.py — Step 4.7 gate 7: did the build honor design_directives?

Step 2.5 produces ~10 measurable directives, but only a11y_target was ever gated in the build
(via contrast). density/guidance/safeguard/nav stayed advisory prose → the prototype could
ignore them and regress to a generic UI. This gate machine-checks the directives that are
concretely verifiable, and is honest about the fuzzy ones (advisory, never fails):

  HARD 🔴
   - safeguard_level ∈ {standard,strict,maximal}: a destructive action (delete/remove, or a
     destructive-variant button) in a screen must be guarded by an AlertDialog / confirm.
   - guidance_level == "guided": at least one Empty / empty-state component must exist.
  ADVISORY (notes only)
   - density_target ≥ 4: expect a Table/DataTable somewhere (dense data ≠ loose cards).
   - navigation_model workspace/hub_spoke: expect a Sidebar/nav shell.

Usage:
  lint_directive_fidelity.py <prototype_dir> <intelligence.json>
Exit 0 = PASS / nothing to check, 1 = BLOCKED.
"""

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from audit_prototype import _collect_targets  # reuse the generated-surface file collector

# A destructive *action* — a destructive-variant Button, or delete/remove handlers — NOT a
# destructive-variant Badge/Alert (those colour a status/error message, they aren't an action that
# needs a confirm). `<Button[^>]*variant="destructive"` keeps the match scoped to the button tag
# ([^>]* spans props/newlines up to the tag's closing '>', so it won't reach a later Badge/Alert).
DESTRUCTIVE = re.compile(r'<Button[^>]*variant\s*=\s*["\']destructive|on(?:Delete|Remove)\b|handle(?:Delete|Remove)\b', re.I)
DESTRUCTIVE_TEXT = re.compile(r'>\s*(?:delete|remove|discard)\b', re.I)
CONFIRM = re.compile(r'AlertDialog|window\.confirm|\bconfirm\s*\(|role\s*=\s*["\']alertdialog', re.I)
EMPTY = re.compile(r'<Empty\b|EmptyHeader|EmptyTitle|empty-state', re.I)
TABLE = re.compile(r'<Table\b|<DataTable\b|<DataGrid\b|role\s*=\s*["\']table', re.I)
SHELL = re.compile(r'<Sidebar\b|<AppSidebar\b|<nav\b|role\s*=\s*["\']navigation', re.I)

SAFEGUARD_ON = {"standard", "strict", "maximal"}


def check(proto, intel_path):
    errors, notes = [], []
    proto = Path(proto)
    try:
        intel = json.loads(Path(intel_path).read_text())
    except Exception as e:  # noqa: BLE001
        return [], [f"intelligence.json not read ({intel_path}): {e} — directive check skipped"]

    dz = intel.get("design_directives") or {}
    if not dz:
        return [], ["no design_directives in intelligence.json — nothing to verify"]

    files = _collect_targets(proto, ["app", "components", "lib"], include_vendored=False)
    if not files:
        return [], ["no generated screens to scan"]
    texts = {}
    for f in files:
        try:
            texts[f] = Path(f).read_text(errors="ignore")
        except Exception:  # noqa: BLE001
            texts[f] = ""

    # HARD — safeguard: destructive action ⇒ a confirm in the same file
    safeguard = dz.get("safeguard_level")
    if safeguard in SAFEGUARD_ON:
        for f, t in texts.items():
            if (DESTRUCTIVE.search(t) or DESTRUCTIVE_TEXT.search(t)) and not CONFIRM.search(t):
                rel = Path(f).name
                errors.append(f"{rel}: a destructive action has no AlertDialog/confirm "
                              f"(safeguard_level={safeguard} requires one)")

    # HARD — guided ⇒ at least one empty-state component exists
    if dz.get("guidance_level") == "guided":
        if not any(EMPTY.search(t) for t in texts.values()):
            errors.append("guidance_level=guided but no Empty / empty-state component found in any screen "
                          "— guided products must teach the empty path")

    # ADVISORY — density / navigation (fuzzy, never fail)
    density = dz.get("density_target")
    if isinstance(density, int) and density >= 4 and not any(TABLE.search(t) for t in texts.values()):
        notes.append(f"advisory: density_target={density} (dense) but no Table/DataTable found — "
                     "verify dense data isn't rendered in loose cards")
    nav = dz.get("navigation_model")
    if nav in {"workspace", "hub_spoke"} and not any(SHELL.search(t) for t in texts.values()):
        notes.append(f"advisory: navigation_model={nav} but no Sidebar/nav shell found")

    if not errors:
        notes.append(f"safeguard={safeguard or '—'} · guidance={dz.get('guidance_level','—')} "
                     f"· density={density} · nav={nav or '—'} honored")
    return errors, notes


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    errors, notes = check(argv[0], argv[1])
    if errors:
        print(f"[directive_fidelity] ✗ {len(errors)} directive(s) not honored:")
        for e in errors:
            print(f"  • {e}")
        for n in notes:
            print(f"  ℹ {n}")
        return 1
    print("[directive_fidelity] ✓ verifiable directives are honored")
    for n in notes:
        print(f"  ℹ {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
