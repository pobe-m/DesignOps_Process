#!/usr/bin/env python3
"""Gate for interviews.json (Step 2.3b — Interview + Affinity Layer).

Structural + referential + the *honesty invariants* that keep a SIMULATED interview
(AI role-playing a persona) from being passed off as real research. Mirrors the shape of
validate_research.py / validate_usability.py.

Usage:  validate_interviews.py <interviews.json> [research.json]
  - research.json (optional) resolves persona_ref / pain_ref across files and enforces
    that every primary persona has an interview script.
Exit 0 = valid (may print warnings). Exit 1 = blocked.
"""
import json
import sys

EVIDENCE_MODE = {"inferred", "hybrid", "evidence_backed"}
CONFIDENCE = {"high", "medium", "low"}
SIM_CONFIDENCE = {"medium", "low"}          # simulated → never 'high'
THEME = {"motivation", "pain", "behavior", "tools", "goal"}
SCOPE = {"universal", "role_specific"}
VERDICT = {"pass", "reprobe"}


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

    # optional research.json — cross-file persona / pain resolution + primary coverage
    persona_ids, primary_persona_ids, pain_ids = None, set(), None
    if research_path:
        try:
            with open(research_path) as f:
                research = json.load(f)
            persona_ids, pain_ids = set(), set()
            for p in research.get("personas", []):
                pid = p.get("id")
                if pid:
                    persona_ids.add(pid)
                    if p.get("primary") is True:
                        primary_persona_ids.add(pid)
            for pp in research.get("pain_points", []):
                if pp.get("id"):
                    pain_ids.add(pp.get("id"))
        except (OSError, json.JSONDecodeError):
            warnings.append(f"could not read research.json at {research_path} — skipping cross-file checks")

    # ── meta / honesty ──────────────────────────────────────────────────────────
    meta = data.get("meta", {})
    _enum(meta.get("evidence_mode"), EVIDENCE_MODE, "meta.evidence_mode", errors)
    if meta.get("not_real_user_data") is not True:
        errors.append("meta.not_real_user_data must be true — this is a simulated interview, not real research")
    if meta.get("simulated") is not True:
        errors.append("meta.simulated must be true")
    _enum(meta.get("overall_confidence"), SIM_CONFIDENCE, "meta.overall_confidence", errors)
    if not meta.get("limitations"):
        errors.append("meta.limitations must be non-empty (state that answers are role-played, not real)")
    rounds = meta.get("gate_rounds_used")
    if isinstance(rounds, int) and rounds > 3:
        warnings.append(f"meta.gate_rounds_used={rounds} (>3) — the quality gate never converged; treat as low-confidence")

    # ── interview_scripts + questions ───────────────────────────────────────────
    q_ids = set()
    scripted_personas = set()
    scripts = data.get("interview_scripts", [])
    for i, s in enumerate(scripts):
        path_s = f"interview_scripts[{i}]"
        pref = s.get("persona_ref")
        if not pref:
            errors.append(f"{path_s}.persona_ref: required")
        else:
            scripted_personas.add(pref)
            if persona_ids is not None and pref not in persona_ids:
                errors.append(f"{path_s}.persona_ref {pref!r} does not resolve to a research.json persona")
        questions = s.get("questions", [])
        if len(questions) < 6:
            warnings.append(f"{path_s} has {len(questions)} questions (<6) — thin script")
        for k, q in enumerate(questions):
            qpath = f"{path_s}.questions[{k}]"
            qid = q.get("id")
            if not qid:
                errors.append(f"{qpath}.id: missing")
            elif qid in q_ids:
                errors.append(f"{qpath}.id: duplicate {qid!r}")
            else:
                q_ids.add(qid)
            _enum(q.get("theme"), THEME, f"{qpath}.theme", errors)
            _enum(q.get("scope"), SCOPE, f"{qpath}.scope", errors)
            if not q.get("text"):
                errors.append(f"{qpath}.text: required")

    # every primary persona must be interviewed (when research is known)
    if persona_ids is not None:
        for pid in sorted(primary_persona_ids - scripted_personas):
            errors.append(f"primary persona {pid!r} has no interview_script — every user must be interviewed")

    # ── simulated_responses ─────────────────────────────────────────────────────
    for i, r in enumerate(data.get("simulated_responses", [])):
        rpath = f"simulated_responses[{i}]"
        if r.get("simulated") is not True:
            errors.append(f"{rpath}.simulated must be true")
        qref = r.get("question_ref")
        if qref not in q_ids:
            errors.append(f"{rpath}.question_ref {qref!r} does not resolve to a question id")
        if not r.get("traces_to"):
            errors.append(f"{rpath}.traces_to must be non-empty (an answer grounded in nothing is invention)")
        pref = r.get("persona_ref")
        if persona_ids is not None and pref is not None and pref not in persona_ids:
            errors.append(f"{rpath}.persona_ref {pref!r} does not resolve to a research.json persona")

    # ── affinity_map ────────────────────────────────────────────────────────────
    af = data.get("affinity_map", [])
    if not af:
        warnings.append("affinity_map is empty — the interview produced no clustered insight")
    af_ids = set()
    for i, a in enumerate(af):
        apath = f"affinity_map[{i}]"
        aid = a.get("id")
        if aid and aid in af_ids:
            errors.append(f"{apath}.id: duplicate {aid!r}")
        elif aid:
            af_ids.add(aid)
        _enum(a.get("confidence"), SIM_CONFIDENCE, f"{apath}.confidence", errors)
        quotes = a.get("supporting_quotes", [])
        if not quotes:
            errors.append(f"{apath}.supporting_quotes: required (an insight must cite the quotes it rests on)")
        for qref in quotes:
            if qref not in q_ids:
                errors.append(f"{apath}.supporting_quotes {qref!r} does not resolve to a question id")
        if len(set(quotes)) < 2:
            warnings.append(f"{apath} rests on <2 distinct questions — possible circular/echo insight")
        if not a.get("personas_covered"):
            errors.append(f"{apath}.personas_covered: required")
        if pain_ids is not None:
            for pr in a.get("pain_ref", []):
                if pr not in pain_ids:
                    errors.append(f"{apath}.pain_ref {pr!r} does not resolve to a research.json pain_points id")

    # ── gate_log ────────────────────────────────────────────────────────────────
    for i, g in enumerate(data.get("gate_log", [])):
        _enum(g.get("verdict"), VERDICT, f"gate_log[{i}].verdict", errors)

    return errors, warnings


def main():
    if len(sys.argv) < 2:
        print("usage: validate_interviews.py <interviews.json> [research.json]")
        sys.exit(2)
    errors, warnings = validate(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
    for w in warnings:
        print(f"  ⚠ {w}")
    if errors:
        print(f"\n✗ interviews.json INVALID — {len(errors)} error(s):")
        for e in errors:
            print(f"  ✗ {e}")
        sys.exit(1)
    print("✓ interviews.json valid (simulated — hypotheses, not real-user findings)")
    sys.exit(0)


if __name__ == "__main__":
    main()
