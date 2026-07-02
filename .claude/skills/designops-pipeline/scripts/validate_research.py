#!/usr/bin/env python3
"""Gate for research.json (Step 2.3 — User Research Layer).

Structural + referential + the *honesty invariants* that keep a hybrid
(infer-then-override) layer from passing AI hypotheses off as real research.

Usage:  validate_research.py <research.json> [brief.json]
Exit 0 = valid (may print warnings). Exit 1 = blocked.
"""
import json
import sys

EVIDENCE_MODE = {"inferred", "hybrid", "evidence_backed"}
CONFIDENCE = {"high", "medium", "low"}
SOURCE = {"inferred", "evidence"}
SEVERITY = {"low", "med", "high"}
RISK = {"low", "med", "high"}
PRIORITY = {"must", "should", "could"}
METHOD = {"interview", "survey", "analytics", "usability_test"}
STATUS = {"unvalidated", "validated", "invalidated"}
IMPACT_EFFORT = {"low", "med", "high"}
JOURNEY_MODE = {"existing_product", "workaround", "none"}


def _enum(val, allowed, path, errors):
    if val not in allowed:
        errors.append(f"{path}: {val!r} not in {sorted(allowed)}")


def validate(path, brief_path=None):
    errors, warnings = [], []
    try:
        with open(path) as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        return [f"cannot read {path}: {e}"], [], {}

    meta = data.get("meta", {})
    mode = meta.get("evidence_mode")
    _enum(mode, EVIDENCE_MODE, "meta.evidence_mode", errors)
    inputs = meta.get("inputs_provided", [])
    if not isinstance(inputs, list):
        errors.append("meta.inputs_provided must be a list")
        inputs = []
    inputs_set = set(inputs)
    _enum(meta.get("overall_confidence"), CONFIDENCE, "meta.overall_confidence", errors)

    no_inputs = len(inputs_set) == 0
    if no_inputs and mode != "inferred":
        errors.append("meta.inputs_provided is empty but evidence_mode != 'inferred' "
                      "(you cannot be evidence-backed with no inputs)")

    ids = {}

    def reg(idv, kind, path):
        if not idv:
            errors.append(f"{path}: missing id")
        elif idv in ids:
            errors.append(f"{path}: duplicate id {idv!r} (also {ids[idv]})")
        else:
            ids[idv] = kind

    def honesty(item, path):
        src = item.get("source")
        _enum(src, SOURCE, f"{path}.source", errors)
        conf = item.get("confidence")
        _enum(conf, CONFIDENCE, f"{path}.confidence", errors)
        ev = item.get("evidence", [])
        if src == "evidence":
            if not ev:
                errors.append(f"{path}: source 'evidence' but evidence is empty")
            for ref in ev:
                if ref not in inputs_set:
                    errors.append(f"{path}: evidence {ref!r} not declared in meta.inputs_provided "
                                  "(fabricated evidence)")
        if src == "inferred" and conf == "high":
            errors.append(f"{path}: inferred items may not claim confidence 'high'")
        if no_inputs and src != "inferred":
            errors.append(f"{path}: no inputs provided, so source must be 'inferred' (not {src!r})")

    personas = data.get("personas", [])
    if not any(p.get("primary") is True for p in personas):
        errors.append("personas: need ≥1 with primary=true")
    for i, p in enumerate(personas):
        path = f"personas[{i}]"
        reg(p.get("id"), "persona", path)
        _enum(p.get("tech_proficiency"), {"novice", "intermediate", "expert"}, f"{path}.tech_proficiency", errors)
        honesty(p, path)

    jtbd = data.get("jobs_to_be_done", [])
    for i, j in enumerate(jtbd):
        path = f"jobs_to_be_done[{i}]"
        reg(j.get("id"), "jtbd", path)
        _enum(j.get("priority"), PRIORITY, f"{path}.priority", errors)
        for fld in ("when", "want", "so_that"):
            if not j.get(fld):
                errors.append(f"{path}.{fld}: required (JTBD is situation+motivation+outcome)")
        honesty(j, path)

    pains = data.get("pain_points", [])
    for i, pp in enumerate(pains):
        path = f"pain_points[{i}]"
        reg(pp.get("id"), "pain", path)
        _enum(pp.get("severity"), SEVERITY, f"{path}.severity", errors)
        honesty(pp, path)

    assumptions = data.get("behavioral_assumptions", [])
    rqs = data.get("research_questions", [])
    tied = {q.get("tied_to") for q in rqs}
    for i, a in enumerate(assumptions):
        path = f"behavioral_assumptions[{i}]"
        reg(a.get("id"), "assumption", path)
        _enum(a.get("risk_if_wrong"), RISK, f"{path}.risk_if_wrong", errors)
        _enum(a.get("status"), STATUS, f"{path}.status", errors)
        honesty(a, path)
        if a.get("status") == "validated" and a.get("source") != "evidence":
            errors.append(f"{path}: status 'validated' requires source 'evidence'")
        if a.get("risk_if_wrong") == "high" and a.get("id") not in tied:
            errors.append(f"{path}: high-risk assumption has no research_question tied to {a.get('id')!r}")

    rq_ids = set()
    for i, q in enumerate(rqs):
        path = f"research_questions[{i}]"
        qid = q.get("id")
        if qid:
            rq_ids.add(qid)
        _enum(q.get("method"), METHOD, f"{path}.method", errors)
        _enum(q.get("priority"), {"blocker", "important", "nice_to_know"}, f"{path}.priority", errors)

    # opportunities — where the as-is breaks becomes a chance to improve. Register ids first so the
    # journey's opportunity_ref can resolve; honesty rules match every other item.
    opportunities = data.get("opportunities", [])
    for i, o in enumerate(opportunities):
        path = f"opportunities[{i}]"
        reg(o.get("id"), "opportunity", path)
        _enum(o.get("impact"), IMPACT_EFFORT, f"{path}.impact", errors)
        _enum(o.get("effort"), IMPACT_EFFORT, f"{path}.effort", errors)
        if not o.get("statement"):
            errors.append(f"{path}.statement: required (a 'how might we…' framing)")
        honesty(o, path)
        rq = o.get("research_question")
        if o.get("impact") == "high" and o.get("source") == "inferred" and not rq:
            errors.append(f"{path}: high-impact + inferred opportunity must carry a research_question "
                          "(don't rest a big bet on an unvalidated guess)")
        if rq and rq not in rq_ids:
            errors.append(f"{path}.research_question {rq!r} does not resolve to a research_questions id")

    # ref resolution
    def resolve(ref, kinds, path):
        if ref and ref not in ids:
            errors.append(f"{path}: ref {ref!r} does not resolve")
        elif ref and ids.get(ref) not in kinds:
            errors.append(f"{path}: ref {ref!r} is a {ids.get(ref)}, expected {kinds}")

    for i, p in enumerate(personas):
        for g in p.get("goals_ref", []):
            resolve(g, {"jtbd"}, f"personas[{i}].goals_ref")
    for i, j in enumerate(jtbd):
        resolve(j.get("persona_ref"), {"persona"}, f"jobs_to_be_done[{i}].persona_ref")
    for i, pp in enumerate(pains):
        resolve(pp.get("persona_ref"), {"persona"}, f"pain_points[{i}].persona_ref")
    for i, o in enumerate(opportunities):
        resolve(o.get("persona_ref"), {"persona"}, f"opportunities[{i}].persona_ref")
        for pr in o.get("pain_ref", []):
            resolve(pr, {"pain"}, f"opportunities[{i}].pain_ref")

    # current_state_journey — conditional (flow-shaped only); re-projects pains onto a timeline.
    for i, cj in enumerate(data.get("current_state_journey", [])):
        path = f"current_state_journey[{i}]"
        _enum(cj.get("mode"), JOURNEY_MODE, f"{path}.mode", errors)
        resolve(cj.get("persona_ref"), {"persona"}, f"{path}.persona_ref")
        if cj.get("mode") == "none" and cj.get("phases"):
            errors.append(f"{path}: mode 'none' means there is no as-is to map — omit the journey "
                          "rather than inventing phases")
        for k, ph in enumerate(cj.get("phases", [])):
            ppath = f"{path}.phases[{k}]"
            emo = ph.get("emotion")
            if not isinstance(emo, (int, float)) or not (-2 <= emo <= 2):
                errors.append(f"{ppath}.emotion must be a number in [-2, 2]")
            for pr in ph.get("pains_ref", []):
                resolve(pr, {"pain"}, f"{ppath}.pains_ref")
            for orf in ph.get("opportunity_ref", []):
                resolve(orf, {"opportunity"}, f"{ppath}.opportunity_ref")

    flags = {}
    if meta.get("overall_confidence") == "low":
        flags["constrain_downstream"] = True
        warnings.append("overall_confidence=low → constrain_downstream: Step 2.5 should treat hints as low-confidence")
    if mode == "inferred":
        warnings.append("evidence_mode=inferred → research is HYPOTHESES; gather real inputs to upgrade")
    return errors, warnings, flags


def main():
    if len(sys.argv) < 2:
        print("usage: validate_research.py <research.json> [brief.json]")
        sys.exit(2)
    errors, warnings, flags = validate(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
    for w in warnings:
        print(f"  ⚠ {w}")
    if errors:
        print(f"\n✗ research.json INVALID — {len(errors)} error(s):")
        for e in errors:
            print(f"  ✗ {e}")
        sys.exit(1)
    print(f"✓ research.json valid{' (flags: ' + ','.join(flags) + ')' if flags else ''}")
    sys.exit(0)


if __name__ == "__main__":
    main()
