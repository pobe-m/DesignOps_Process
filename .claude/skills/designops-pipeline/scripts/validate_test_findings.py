#!/usr/bin/env python3
"""Gate for test-findings.json (Step 4.9 — Feedback Loop).

Turns test feedback into the next prototype's scored work-list. Enforces the scoring math,
the signal-vs-noise verdict rules, and the honesty split between real-user evidence and
simulated hypotheses. Mirrors validate_research.py style.

Usage:  validate_test_findings.py <test-findings.json> [research.json]
  - research.json (optional) resolves maps_to into a real pain/opportunity id.
Exit 0 = valid (may print warnings). Exit 1 = blocked.
"""
import json
import sys

TYPE = {"observed", "stated"}
VERDICT = {"systemic", "segment", "individual"}
DECISION = {"fix_now", "backlog", "wont_fix"}
CONFIDENCE = {"high", "medium", "low"}
TEST_METHOD = {"real_user", "simulated_4.8", "hybrid"}
CONF_WEIGHT = {"high": 3, "medium": 2, "low": 1}
SOLUTION_TELLS = ("add ", "make it ", "put a ", "use a ", "change the color", "move the ")


def _enum(val, allowed, path, errors):
    if val not in allowed:
        errors.append(f"{path}: {val!r} not in {sorted(allowed)}")


def validate(path, research_path=None):
    errors, warnings = [], []
    try:
        with open(path) as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        return [f"cannot read {path}: {e}"], []

    # optional research.json — resolve maps_to into a real pain/opportunity id
    hypo_ids = None
    if research_path:
        try:
            with open(research_path) as f:
                research = json.load(f)
            hypo_ids = set()
            for key in ("pain_points", "opportunities", "jobs_to_be_done"):
                for item in research.get(key, []):
                    if item.get("id"):
                        hypo_ids.add(item["id"])
        except (OSError, json.JSONDecodeError):
            warnings.append(f"could not read research.json at {research_path} — skipping maps_to resolution")

    meta = data.get("meta", {})
    it = meta.get("iteration")
    if not isinstance(it, int) or it < 1:
        errors.append("meta.iteration must be an int ≥ 1")
        it = None
    method = meta.get("test_method")
    _enum(method, TEST_METHOD, "meta.test_method", errors)
    conv = meta.get("convergence", {})
    if isinstance(conv, dict) and isinstance(conv.get("dry_rounds"), int) and conv["dry_rounds"] >= 2:
        warnings.append("meta.convergence.dry_rounds ≥ 2 — the loop has converged; consider shipping")

    findings = data.get("findings", [])
    if not isinstance(findings, list) or not findings:
        errors.append("findings must have at least 1 entry")
        return errors, warnings

    ids = set()
    for i, fnd in enumerate(findings):
        p = f"findings[{i}]"
        fid = fnd.get("id", "")
        if not fid:
            errors.append(f"{p}.id: missing")
        elif fid in ids:
            errors.append(f"{p}.id: duplicate {fid!r}")
        else:
            ids.add(fid)

        _enum(fnd.get("type"), TYPE, f"{p}.type", errors)
        _enum(fnd.get("verdict"), VERDICT, f"{p}.verdict", errors)
        _enum(fnd.get("decision"), DECISION, f"{p}.decision", errors)
        conf = fnd.get("confidence")
        _enum(conf, CONFIDENCE, f"{p}.confidence", errors)

        sev = fnd.get("severity")
        if not isinstance(sev, int) or not (0 <= sev <= 3):
            errors.append(f"{p}.severity must be an int 0..3 (blocker3/major2/minor1/cosmetic0)")
        reach = fnd.get("reach")
        if not isinstance(reach, int) or reach < 1:
            errors.append(f"{p}.reach must be an int ≥ 1 (distinct segments affected)")

        # the scoring math can't be hand-waved
        if isinstance(sev, int) and isinstance(reach, int) and conf in CONF_WEIGHT:
            expected = sev * reach * CONF_WEIGHT[conf]
            if fnd.get("priority_score") != expected:
                errors.append(f"{p}.priority_score must equal severity×reach×confidence_weight "
                              f"({sev}×{reach}×{CONF_WEIGHT[conf]} = {expected}), got {fnd.get('priority_score')!r}")

        if not fnd.get("problem_statement"):
            errors.append(f"{p}.problem_statement is required (a finding with no problem can't be acted on)")
        else:
            ps = fnd["problem_statement"].strip().lower()
            if ps.startswith(SOLUTION_TELLS):
                warnings.append(f"{p}.problem_statement reads like a solution — de-solutionise it into the underlying problem")

        # signal-vs-noise: systemic must cross segments
        if fnd.get("verdict") == "systemic" and isinstance(reach, int) and reach < 2:
            errors.append(f"{p}: verdict 'systemic' requires reach ≥ 2 (a systemic problem crosses segments)")

        # fix_now must target a future iteration
        if fnd.get("decision") == "fix_now":
            ti = fnd.get("target_iteration")
            if not isinstance(ti, int) or (it is not None and ti <= it):
                errors.append(f"{p}: decision 'fix_now' needs target_iteration > meta.iteration ({it})")
            if fnd.get("verdict") == "individual":
                warnings.append(f"{p}: fixing an 'individual' (n=1) finding — confirm it's not one person's quirk")
            if sev == 0:
                warnings.append(f"{p}: cosmetic (severity 0) marked fix_now — usually backlog")

        # honesty: simulated findings are hypotheses, not evidence
        if method == "simulated_4.8" and fnd.get("type") == "observed":
            warnings.append(f"{p}: simulated_4.8 test but type 'observed' — simulated behaviour is still a hypothesis, not real evidence")

        # maps_to resolution
        mt = fnd.get("maps_to")
        if mt and hypo_ids is not None and mt not in hypo_ids:
            errors.append(f"{p}.maps_to {mt!r} does not resolve to a research.json pain/opportunity/JTBD id")

    return errors, warnings


def main():
    if len(sys.argv) < 2:
        print("usage: validate_test_findings.py <test-findings.json> [research.json]")
        sys.exit(2)
    errors, warnings = validate(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
    for w in warnings:
        print(f"  ⚠ {w}")
    if errors:
        print(f"\n✗ test-findings.json INVALID — {len(errors)} error(s):")
        for e in errors:
            print(f"  ✗ {e}")
        sys.exit(1)
    d = json.load(open(sys.argv[1]))
    fix = sum(1 for f in d.get("findings", []) if f.get("decision") == "fix_now")
    print(f"✓ test-findings.json valid ({fix} fix_now → next prototype)")
    sys.exit(0)


if __name__ == "__main__":
    main()
