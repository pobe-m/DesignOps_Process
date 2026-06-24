#!/usr/bin/env python3
"""
validate_edgecases.py — gate for Step 3.7 (Edge-Case Layer).

Usage: validate_edgecases.py <edge-cases.json> [screen-inventory.json] [flows.json] [intelligence.json]
Exit 0 = valid, Exit 1 = invalid. Zero-dependency, mirrors validate_screens.py.

The front end of the edge-case spine. Enforces:
  • structure — UI-Stack states + CORRECT dims + must/should/could severity
  • traceability — every edge maps to a real screen (and flow, when given); no orphans
  • "declared states need a reason" — a Must screen that declares an empty/error state in
    screen-inventory.json must have ≥1 edge case explaining it
  • directive floors (when intelligence.json resolves) — low/zero error_tolerance forces error +
    input-validation edges to `must`; guided forces an empty edge; dense data forces a partial edge;
    high/safety_critical criticality forces destructive confirms (and an undo/cascade) to `must`

Cross-file artifacts are optional: when absent the dependent checks are skipped with a warning, so
the gate runs standalone (same graceful pattern as validate_screens.py).
Spec + taxonomy + citations: references/edge-cases-layer.md.
"""

import json
import sys

UI_STATES = {"ideal", "empty", "error", "partial", "loading"}
CORRECT_DIMS = {"conformance", "ordering", "range", "reference", "existence", "cardinality", "time"}
SEVERITY = {"must", "should", "could"}
VALIDATION_DIMS = {"conformance", "range", "existence"}   # CORRECT dims that mean "input was bad"
INPUT_LAYOUTS = {"form", "wizard_step"}                    # screens that actually take input
DATA_LAYOUTS = {"table", "list", "dashboard", "hub", "card", "detail"}  # screens that can be empty
DENSE_LAYOUTS = {"table", "list", "dashboard"}            # screens that overflow when dense
UNDO_WORDS = ("undo", "cascade", "restore", "revert")


def _load(path):
    try:
        with open(path) as f:
            return json.load(f), None
    except json.JSONDecodeError as e:
        return None, f"JSON parse error in {path}: {e}"
    except FileNotFoundError:
        return None, f"file not found: {path}"


def validate(ec_path, screens_path=None, flows_path=None, intel_path=None):
    errors, warnings = [], []
    d, err = _load(ec_path)
    if err:
        return [err], []

    screens = flows = intel = None
    if screens_path:
        screens, e = _load(screens_path)
        if e:
            warnings.append(e + " — skipping screen traceability + declared-state + directive floors")
    if flows_path:
        flows, e = _load(flows_path)
        if e:
            warnings.append(e + " — skipping flow traceability")
    if intel_path:
        intel, e = _load(intel_path)
        if e:
            warnings.append(e + " — skipping directive floors")

    edges = d.get("edge_cases")
    if not isinstance(edges, list) or not edges:
        errors.append("edge_cases must be a non-empty array")
        return errors, warnings

    screen_ids = {s.get("id") for s in (screens or {}).get("screens", [])} if screens else None
    flow_ids = {fl.get("id") for fl in (flows or {}).get("flows", [])} if flows else None

    # ── per-edge structure + traceability ─────────────────────────────────────
    seen = set()
    by_screen = {}   # screen id → list of edge dicts mapped to it
    for i, e in enumerate(edges):
        eid = e.get("id", "")
        if not eid or eid in seen:
            errors.append(f"edge_cases[{i}].id missing or duplicate ('{eid}')")
        else:
            seen.add(eid)
        if e.get("ui_state") not in UI_STATES:
            errors.append(f"edge_cases[{i}].ui_state must be one of {sorted(UI_STATES)} (got: {e.get('ui_state')!r})")
        cd = e.get("correct_dim")
        if cd is not None and cd not in CORRECT_DIMS:
            errors.append(f"edge_cases[{i}].correct_dim must be one of {sorted(CORRECT_DIMS)} (got: {cd!r})")
        sev = e.get("severity")
        if sev not in SEVERITY:
            errors.append(f"edge_cases[{i}].severity must be one of {sorted(SEVERITY)} (got: {sev!r})")
        if sev == "must" and not (e.get("expected_handling") or "").strip():
            errors.append(f"edge_cases[{i}] ('{eid}') is must but has empty expected_handling "
                          "(a blocker contract must say how it's handled)")
        sref = e.get("maps_to_screen")
        if not sref:
            errors.append(f"edge_cases[{i}] ('{eid}') has no maps_to_screen (every edge traces to a screen)")
        else:
            by_screen.setdefault(sref, []).append(e)
            if screen_ids is not None and sref not in screen_ids:
                errors.append(f"edge_cases[{i}].maps_to_screen '{sref}' not in screen-inventory.json")
        fref = e.get("maps_to_flow")
        if fref and flow_ids is not None and fref not in flow_ids:
            errors.append(f"edge_cases[{i}].maps_to_flow '{fref}' not in flows.json")

    # ── declared states need a reason (needs screen-inventory) ────────────────
    must_screens = []
    if screens is not None:
        for s in screens.get("screens", []):
            if s.get("priority") != "Must":
                continue
            must_screens.append(s)
            sid = s.get("id")
            mapped = by_screen.get(sid, [])
            declared = {st for st in (s.get("states") or []) if st in ("empty", "error")}
            for st in sorted(declared):
                if not any(e.get("ui_state") == st for e in mapped):
                    errors.append(f"screen '{sid}' declares state '{st}' in screen-inventory but no "
                                  f"edge case explains it (declared states need a reason)")
            # drift: a must edge says empty/error but the screen never declared it
            for e in mapped:
                us = e.get("ui_state")
                if us in ("empty", "error") and e.get("severity") == "must" and us not in (s.get("states") or []):
                    warnings.append(f"screen '{sid}' has a must {us} edge but screen-inventory does not "
                                    f"declare that state — likely screen-inventory drift")

    # ── directive floors (needs intelligence + screens) ───────────────────────
    if intel is not None and screens is not None:
        et = (intel.get("error_tolerance") or {}).get("overall")
        dc = (intel.get("decision_criticality") or {}).get("overall")
        dz = intel.get("design_directives") or {}
        guidance = dz.get("guidance_level")
        band = (intel.get("data_density") or {}).get("overall_band")

        def has(sid, **cond):
            for e in by_screen.get(sid, []):
                if all(e.get(k) == v for k, v in cond.items() if k != "dim_in"):
                    if "dim_in" in cond and e.get("correct_dim") not in cond["dim_in"]:
                        continue
                    return True
            return False

        for s in must_screens:
            sid, lay = s.get("id"), s.get("layout_primitive")
            if et in ("low", "zero"):
                if not has(sid, ui_state="error", severity="must"):
                    errors.append(f"error_tolerance={et}: Must screen '{sid}' needs a must-severity "
                                  "error edge (low/zero tolerance can't leave failures undesigned)")
                if lay in INPUT_LAYOUTS and not any(
                        e.get("severity") == "must" and e.get("correct_dim") in VALIDATION_DIMS
                        for e in by_screen.get(sid, [])):
                    errors.append(f"error_tolerance={et}: input screen '{sid}' needs a must-severity "
                                  "input-validation edge (correct_dim conformance/range/existence)")
            if guidance == "guided" and lay in DATA_LAYOUTS:
                if not has(sid, ui_state="empty", severity="must"):
                    errors.append(f"guidance_level=guided: data screen '{sid}' needs a must-severity "
                                  "empty edge (a guided product never shows a dead blank screen)")
            if isinstance(band, int) and band >= 4 and lay in DENSE_LAYOUTS:
                if not has(sid, ui_state="partial", severity="must"):
                    errors.append(f"data_density band {band} (dense): screen '{sid}' needs a must-severity "
                                  "partial edge (overflow/truncation/max-volume)")

        # destructive floor — criticality forces confirms to must (+ undo for safety_critical)
        if dc in ("high", "safety_critical"):
            destructive = [e for e in edges if e.get("category") == "destructive"]
            if not destructive:
                warnings.append(f"decision_criticality={dc} but no destructive edge enumerated — "
                                "confirm there are no irreversible actions, or add their confirm edges")
            for e in destructive:
                if e.get("severity") != "must":
                    errors.append(f"decision_criticality={dc}: destructive edge '{e.get('id')}' must be "
                                  "severity must (irreversible actions need a guaranteed confirm)")
            if dc == "safety_critical" and destructive and not any(
                    any(w in (e.get("expected_handling") or "").lower() for w in UNDO_WORDS)
                    for e in destructive):
                errors.append("decision_criticality=safety_critical: at least one destructive edge must "
                              "provide an undo / cascade-warning (none mention undo/cascade/restore)")
    elif intel is not None and screens is None:
        warnings.append("intelligence.json given but screen-inventory.json was not — directive floors "
                        "need both; skipped")

    # ── advisory: should/could without handling ───────────────────────────────
    for i, e in enumerate(edges):
        if e.get("severity") in ("should", "could") and not (e.get("expected_handling") or "").strip():
            warnings.append(f"edge_cases[{i}] ('{e.get('id')}') has no expected_handling — "
                            "even should/could edges read better with a concrete fix")

    return errors, warnings


def main():
    if len(sys.argv) < 2:
        print("Usage: validate_edgecases.py <edge-cases.json> [screen-inventory.json] [flows.json] [intelligence.json]",
              file=sys.stderr)
        sys.exit(1)
    errors, warnings = validate(*sys.argv[1:5])
    if errors:
        print(f"[validate_edgecases] ✗ Invalid — {len(errors)} error(s):", file=sys.stderr)
        for e in errors:
            print(f"  • {e}", file=sys.stderr)
        for w in warnings:
            print(f"  ⚠ {w}", file=sys.stderr)
        sys.exit(1)
    with open(sys.argv[1]) as f:
        d = json.load(f)
    edges = d.get("edge_cases", [])
    by_sev = {s: sum(1 for e in edges if e.get("severity") == s) for s in SEVERITY}
    print("[validate_edgecases] ✓ Valid")
    print(f"  Edge cases : {len(edges)} ({by_sev['must']} must / {by_sev['should']} should / {by_sev['could']} could)")
    for w in warnings:
        print(f"  ⚠ {w}")
    sys.exit(0)


if __name__ == "__main__":
    main()
