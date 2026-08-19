#!/usr/bin/env python3
"""
validate_flows.py — gate for Step C (User Flows).

Usage: validate_flows.py <flows.json> [intelligence.json] [brief.json] [scenario-edges.json]
Exit 0 = valid, Exit 1 = invalid. Zero-dependency, mirrors validate_brief.py.

flows.json refines the brief's raw user_flows using design_directives (navigation_model,
safeguard_level, mandatory_flows). This gate checks structure + that the refinement is
consistent with intelligence.json and the brief; when scenario-edges.json is provided
it also enforces that every flow the 2.5b layer said to inject actually exists.
"""

import json
import sys

REQUIRED_TOP_KEYS = ["meta", "navigation_model", "flows"]
NAV_MODEL = {"single", "wizard", "hub_spoke", "workspace"}


def _load(path):
    try:
        with open(path) as f:
            return json.load(f), None
    except json.JSONDecodeError as e:
        return None, f"JSON parse error in {path}: {e}"
    except FileNotFoundError:
        return None, f"file not found: {path}"


def _norm(s):
    return str(s or "").strip().lower().replace("-", " ").replace("_", " ")


def _name_pool_match(needle, name_pool):
    """True if needle equals (normalized) or is a normalized substring of any name in pool.
    Same semantics as the pre-existing mandatory_flows substring match, shared so the
    2.5b injection check and the mandatory_flows check agree on what 'the same flow' means."""
    n = _norm(needle)
    if not n:
        return False
    for name in name_pool:
        hn = _norm(name)
        if not hn:
            continue
        if n == hn or n in hn:
            return True
    return False


def validate(flows_path, intel_path=None, brief_path=None, edges_path=None):
    errors, warnings = [], []
    _empty_summary = {"injected_from_edges": 0, "tasks_covered": 0, "tasks_total": 0}
    d, err = _load(flows_path)
    if err:
        return [err], [], _empty_summary

    intel = brief = edges = None
    if intel_path:
        intel, e = _load(intel_path)
        if e:
            warnings.append(e + " — skipping intelligence checks")
    if brief_path:
        brief, e = _load(brief_path)
        if e:
            warnings.append(e + " — skipping brief checks")
    if edges_path:
        edges, e = _load(edges_path)
        if e:
            warnings.append(e + " — skipping scenario-edge injection checks")

    for k in REQUIRED_TOP_KEYS:
        if k not in d:
            errors.append(f"missing top-level key: '{k}'")
    if errors:
        return errors, warnings, _empty_summary

    if d["navigation_model"] not in NAV_MODEL:
        errors.append(f"navigation_model must be one of {sorted(NAV_MODEL)} (got: {d['navigation_model']!r})")

    flows = d["flows"]
    if not isinstance(flows, list) or not flows:
        errors.append("flows must have at least 1 entry")
        return errors, warnings, _empty_summary

    # reference sets from upstream artifacts
    ut_ids = {u.get("id") for u in (intel or {}).get("user_types", [])} if intel else None
    goal_ids = {g.get("id") for g in (intel or {}).get("user_goals", [])} if intel else None
    brief_flow_ids = {fl.get("id") for fl in (brief or {}).get("user_flows", [])} if brief else None

    flow_ids = set()
    for i, fl in enumerate(flows):
        fid = fl.get("id", "")
        if not fid or fid in flow_ids:
            errors.append(f"flows[{i}].id missing or duplicate ('{fid}')")
        else:
            flow_ids.add(fid)
        if not fl.get("name"):
            errors.append(f"flows[{i}].name must not be empty")
        steps = fl.get("steps", [])
        if not isinstance(steps, list) or not steps:
            errors.append(f"flows[{i}].steps must be a non-empty array")
        else:
            for j, s in enumerate(steps):
                if not s.get("action"):
                    errors.append(f"flows[{i}].steps[{j}].action must not be empty")
        if ut_ids is not None and fl.get("user_type_ref") not in ut_ids:
            errors.append(f"flows[{i}].user_type_ref '{fl.get('user_type_ref')}' not in intelligence.user_types")
        if goal_ids is not None and fl.get("goal_ref") not in goal_ids:
            errors.append(f"flows[{i}].goal_ref '{fl.get('goal_ref')}' not in intelligence.user_goals")
        # source_flow_ref may be null for injected (mandatory) flows
        src = fl.get("source_flow_ref")
        if brief_flow_ids is not None and src and src not in brief_flow_ids:
            errors.append(f"flows[{i}].source_flow_ref '{src}' not in brief.user_flows")

    # Shared name pool for both mandatory_flows and 2.5b injection matching (see _norm).
    flow_name_pool = [fl.get("id", "") for fl in flows] \
                   + [fl.get("name", "") for fl in flows] \
                   + [m.get("name", "") for m in d.get("mandatory_flows", [])]

    # navigation_model must echo the directive; every mandatory_flow must be present
    if intel is not None:
        dz = intel.get("design_directives", {})
        if dz.get("navigation_model") and d["navigation_model"] != dz["navigation_model"]:
            errors.append(f"navigation_model ({d['navigation_model']}) must equal design_directives.navigation_model ({dz['navigation_model']})")
        for mf in dz.get("mandatory_flows", []):
            if not _name_pool_match(mf, flow_name_pool):
                errors.append(f"design_directives mandatory_flow '{mf}' has no corresponding flow (must be injected)")

        # Phase 1.3 — reverse coverage: every primary user_type must have at least one flow.
        # `system` role_category is intentionally exempt: batch jobs / integrations don't get
        # UI flows and forcing them would push agents to invent fake flows to pass the gate.
        covered_ut = {fl.get("user_type_ref") for fl in flows}
        for u in intel.get("user_types", []):
            uid = u.get("id")
            rel = u.get("relationship")
            role = u.get("role_category")
            if not uid or uid in covered_ut:
                continue
            name = u.get("name") or ""
            label = f"'{uid}'" + (f" ({name})" if name else "")
            if rel == "primary" and role != "system":
                errors.append(f"primary user_type {label} has no flow in flows.json — a primary audience that never gets a flow is a dropped segment")
            elif rel in ("secondary", "occasional"):
                warnings.append(f"{rel} user_type {label} has no flow in flows.json")

        # Phase 2.2 — task_refs coverage: every user-triggered core_task must land in some flow.
        # `scheduled` / `system` triggers are exempt: those tasks run without a UI, so forcing
        # a flow would push agents to invent one just to pass (same reasoning as the `system`
        # role_category exemption above). Opt-in via the `any_*_refs` pattern: silence when the
        # field isn't used anywhere; enforce hard once anyone opts in.
        core_tasks = intel.get("core_tasks", []) or []
        task_ids_from_intel = {t.get("id") for t in core_tasks if t.get("id")}
        ui_task_ids = {t.get("id") for t in core_tasks
                       if t.get("id") and t.get("trigger") not in ("scheduled", "system")}
        any_task_refs = False
        task_refs_seen = set()
        for i, fl in enumerate(flows):
            refs = fl.get("task_refs")
            if refs is None:
                continue
            if not isinstance(refs, list):
                errors.append(f"flows[{i}].task_refs must be a list of core_tasks ids")
                continue
            for ref in refs:
                any_task_refs = True
                if ref in task_ids_from_intel:
                    task_refs_seen.add(ref)
                else:
                    errors.append(f"flows[{i}].task_refs '{ref}' does not resolve to any core_tasks id in intelligence.json")
        if any_task_refs:
            for task in core_tasks:
                tid = task.get("id")
                if tid and tid in ui_task_ids and tid not in task_refs_seen:
                    tname = task.get("name") or ""
                    label = f"'{tid}'" + (f" ({tname})" if tname else "")
                    errors.append(f"core_task {label} has no flow in flows.json — a task the user must perform but never gets a path")
        elif ui_task_ids:
            warnings.append("flows declare no task_refs — task→flow traceability not enforced; "
                            "add task_refs so every user-triggered core_task provably gets a path")
        tasks_covered = len(task_refs_seen & ui_task_ids)
        tasks_total = len(ui_task_ids)
    else:
        tasks_covered = 0
        tasks_total = 0

    # Phase 1.2 — 2.5b injection check: every scenario_edge that asked for a flow must have one.
    injected_from_edges = 0
    if edges is not None:
        for se in edges.get("scenario_edges", []) or []:
            mif = se.get("may_inject_flow") or {}
            if not mif.get("inject"):
                continue
            injected_from_edges += 1
            sid = se.get("id", "?")
            severity = (se.get("severity") or "").lower()
            flow_name = mif.get("flow_name") or ""
            if not flow_name.strip():
                errors.append(f"scenario_edges[{sid}].may_inject_flow.inject=true but flow_name is empty")
                continue
            if _name_pool_match(flow_name, flow_name_pool):
                continue
            msg = (f"scenario_edges[{sid!r}] requires injected flow '{flow_name}' "
                   f"but no flow in flows.json matches — Step 2.5b found a missing flow and Step 3 dropped it")
            if severity == "must":
                errors.append(f"(must) {msg}")
            elif severity in ("should", "could"):
                warnings.append(f"({severity}) {msg}")
            else:
                # unknown/empty severity → treat as should (advisory) so we don't silently block
                warnings.append(f"(should) {msg}")

    return errors, warnings, {
        "injected_from_edges": injected_from_edges,
        "tasks_covered": tasks_covered,
        "tasks_total": tasks_total,
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: validate_flows.py <flows.json> [intelligence.json] [brief.json] [scenario-edges.json]", file=sys.stderr)
        sys.exit(1)
    errors, warnings, summary = validate(*sys.argv[1:5])
    if errors:
        print(f"[validate_flows] ✗ Invalid — {len(errors)} error(s):", file=sys.stderr)
        for e in errors:
            print(f"  • {e}", file=sys.stderr)
        sys.exit(1)
    with open(sys.argv[1]) as f:
        d = json.load(f)
    print("[validate_flows] ✓ Valid")
    print(f"  Navigation : {d.get('navigation_model')}")
    print(f"  Flows      : {len(d.get('flows', []))} · mandatory/injected: {len(d.get('mandatory_flows', []))}")
    print(f"  Injected   : {len(d.get('mandatory_flows', []))} from directives · {summary['injected_from_edges']} from scenario edges (2.5b)")
    print(f"  Tasks      : {summary['tasks_covered']}/{summary['tasks_total']} user-triggered core_tasks covered by a flow")
    for w in warnings:
        print(f"  ⚠ {w}")
    sys.exit(0)


if __name__ == "__main__":
    main()
