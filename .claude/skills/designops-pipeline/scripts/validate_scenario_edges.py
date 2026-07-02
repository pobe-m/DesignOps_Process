#!/usr/bin/env python3
"""Gate for scenario-edges.json (Step 2.5b — Scenario Edge Layer).

Structural + referential + the severity floors that keep scenario edges driven by the
intelligence dimensions (not taste). Sibling of validate_edgecases.py (3.7, screen altitude);
this is the product/requirement altitude. Mirrors validate_intelligence.py style.

Usage:  validate_scenario_edges.py <scenario-edges.json> [intelligence.json]
  - intelligence.json (optional) resolves user_type_ref / task_ref / compliance_ref and
    enforces the severity floors (error_tolerance, decision_criticality, mandatory compliance).
Exit 0 = valid (may print warnings). Exit 1 = blocked.
"""
import json
import sys

# the 10 Product Intelligence dimensions a scenario edge may rest on
DIMENSIONS = {
    "user_types", "user_expertise", "user_goals", "core_tasks", "workflow_complexity",
    "data_density", "error_tolerance", "accessibility_needs", "compliance_requirements",
    "decision_criticality",
}
SEVERITY = {"must", "should", "could"}
SOURCE = {"stated", "inferred"}
CONFIDENCE = {"high", "medium", "low"}


def _enum(val, allowed, path, errors):
    if val not in allowed:
        errors.append(f"{path}: {val!r} not in {sorted(allowed)}")


def validate(path, intel_path=None):
    errors, warnings = [], []
    try:
        with open(path) as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        return [f"cannot read {path}: {e}"], []

    # optional intelligence.json — ref resolution + severity floors
    ut_ids, task_ids, comp_ids = None, None, None
    et_overall, dc_overall, has_mandatory_comp = None, None, None
    if intel_path:
        try:
            with open(intel_path) as f:
                intel = json.load(f)
            ut_ids = {u.get("id") for u in intel.get("user_types", []) if u.get("id")}
            task_ids = {t.get("id") for t in intel.get("core_tasks", []) if t.get("id")}
            comp_ids = {c.get("id") for c in intel.get("compliance_requirements", []) if c.get("id")}
            et_overall = intel.get("error_tolerance", {}).get("overall")
            dc_overall = intel.get("decision_criticality", {}).get("overall")
            has_mandatory_comp = any(c.get("mandatory") for c in intel.get("compliance_requirements", []))
        except (OSError, json.JSONDecodeError):
            warnings.append(f"could not read intelligence.json at {intel_path} — skipping ref + floor checks")

    meta = data.get("meta", {})
    _enum(meta.get("overall_confidence"), CONFIDENCE, "meta.overall_confidence", errors)

    edges = data.get("scenario_edges", [])
    if not isinstance(edges, list) or not edges:
        errors.append("scenario_edges must have at least 1 entry")
        return errors, warnings

    ids = set()
    dims_seen = set()
    for i, e in enumerate(edges):
        p = f"scenario_edges[{i}]"
        eid = e.get("id", "")
        if not eid:
            errors.append(f"{p}.id: missing")
        elif eid in ids:
            errors.append(f"{p}.id: duplicate {eid!r}")
        else:
            ids.add(eid)
        dim = e.get("dimension")
        _enum(dim, DIMENSIONS, f"{p}.dimension", errors)
        dims_seen.add(dim)
        _enum(e.get("severity"), SEVERITY, f"{p}.severity", errors)
        _enum(e.get("source"), SOURCE, f"{p}.source", errors)
        _enum(e.get("confidence"), CONFIDENCE, f"{p}.confidence", errors)
        if not e.get("scenario"):
            errors.append(f"{p}.scenario: required")

        mif = e.get("may_inject_flow")
        if isinstance(mif, dict) and mif.get("inject") and not mif.get("flow_name"):
            errors.append(f"{p}.may_inject_flow.inject is true but flow_name is empty")

        # honesty: a must edge resting on a low-confidence inference needs an open_question
        if e.get("severity") == "must" and e.get("source") == "inferred" and e.get("confidence") == "low" \
                and not e.get("open_question"):
            errors.append(f"{p}: must-severity edge is inferred + low confidence but has no open_question")

        # referential (only when intelligence is loaded)
        if ut_ids is not None:
            for ref, pool, name in (("user_type_ref", ut_ids, "user_types"),
                                    ("task_ref", task_ids, "core_tasks"),
                                    ("compliance_ref", comp_ids, "compliance_requirements")):
                v = e.get(ref)
                if v and v not in pool:
                    errors.append(f"{p}.{ref} {v!r} does not resolve to intelligence.json {name}")

        # severity floors (driven by intelligence, not taste)
        if et_overall in {"low", "zero"} and dim == "error_tolerance":
            if e.get("severity") != "must":
                errors.append(f"{p}: error_tolerance is {et_overall} ⇒ this error_tolerance edge must be severity 'must'")
            if not e.get("suggested_handling"):
                errors.append(f"{p}: low/zero error_tolerance edge needs a recovery in suggested_handling")
        if dc_overall in {"high", "safety_critical"} and dim == "decision_criticality":
            if e.get("severity") != "must":
                errors.append(f"{p}: decision_criticality is {dc_overall} ⇒ this edge must be severity 'must'")

    # coverage floors + warnings (only meaningful with intelligence)
    if has_mandatory_comp:
        comp_edges = [e for e in edges if e.get("dimension") == "compliance_requirements" and e.get("severity") == "must"]
        if not comp_edges:
            errors.append("intelligence has a mandatory compliance requirement but no "
                          "compliance_requirements scenario edge at severity 'must'")
    if et_overall in {"low", "zero"} and "error_tolerance" not in dims_seen:
        warnings.append(f"error_tolerance is {et_overall} but no error_tolerance scenario edge — likely a coverage gap")
    if dc_overall in {"high", "safety_critical"} and "decision_criticality" not in dims_seen:
        warnings.append(f"decision_criticality is {dc_overall} but no decision_criticality scenario edge — likely a coverage gap")

    return errors, warnings


def main():
    if len(sys.argv) < 2:
        print("usage: validate_scenario_edges.py <scenario-edges.json> [intelligence.json]")
        sys.exit(2)
    errors, warnings = validate(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
    for w in warnings:
        print(f"  ⚠ {w}")
    if errors:
        print(f"\n✗ scenario-edges.json INVALID — {len(errors)} error(s):")
        for e in errors:
            print(f"  ✗ {e}")
        sys.exit(1)
    inject = sum(1 for e in json.load(open(sys.argv[1])).get("scenario_edges", [])
                 if isinstance(e.get("may_inject_flow"), dict) and e["may_inject_flow"].get("inject"))
    print(f"✓ scenario-edges.json valid ({inject} edge(s) inject a flow → Step 3)")
    sys.exit(0)


if __name__ == "__main__":
    main()
