#!/usr/bin/env python3
"""
validate_brief.py — validate brief.json before passing it to Step 3
Usage: python3 validate_brief.py <path/to/brief.json>
Exit 0 = valid, Exit 1 = invalid (with an error message)
"""

import json
import sys
from pathlib import Path

REQUIRED_TOP_KEYS = [
    "meta",
    "project_overview",
    "target_users",
    "core_features",
    "user_flows",
    "constraints",
    "open_questions",
    "scoring_criteria",
]

VALID_CRITERIA_TYPES = {"functional", "technical", "process", "document"}

REQUIRED_META_KEYS = ["project_name", "generated_at", "source_file"]

VALID_PRIORITIES = {"Must", "Should", "Could"}
VALID_IMPACTS    = {"blocker", "important", "nice-to-know"}
VALID_CONFIDENCE = {"high", "medium", "low"}
VALID_PRESETS    = {"government", "healthcare", "fintech", "consumer"}


def validate(path: str) -> list[str]:
    """Return list of error strings. Empty = valid."""
    errors = []

    # ── load ──────────────────────────────────────────────────────────────────
    try:
        with open(path) as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return [f"JSON parse error: {e}"]
    except FileNotFoundError:
        return [f"file not found: {path}"]

    # ── top-level keys ────────────────────────────────────────────────────────
    for key in REQUIRED_TOP_KEYS:
        if key not in data:
            errors.append(f"missing top-level key: '{key}'")

    if errors:
        return errors  # stop if a top-level key is missing

    # ── meta ──────────────────────────────────────────────────────────────────
    meta = data["meta"]
    for k in REQUIRED_META_KEYS:
        if not meta.get(k):
            errors.append(f"meta.{k} must not be empty")

    conf = meta.get("tor_confidence", "")
    if conf and conf not in VALID_CONFIDENCE:
        errors.append(f"meta.tor_confidence must be one of: {VALID_CONFIDENCE} (got: '{conf}')")

    # ── project_overview ──────────────────────────────────────────────────────
    po = data["project_overview"]
    if not po.get("objective"):
        errors.append("project_overview.objective must not be empty")

    # ── target_users ──────────────────────────────────────────────────────────
    users = data["target_users"]
    if not isinstance(users, list) or len(users) == 0:
        errors.append("target_users must have at least 1 persona")
    else:
        for i, u in enumerate(users):
            if not u.get("persona"):
                errors.append(f"target_users[{i}].persona must not be empty")

    # ── core_features ─────────────────────────────────────────────────────────
    features = data["core_features"]
    if not isinstance(features, list) or len(features) == 0:
        errors.append("core_features must have at least 1 feature")
    else:
        ids_seen = set()
        for i, f in enumerate(features):
            fid = f.get("id", "")
            if not fid:
                errors.append(f"core_features[{i}].id must not be empty")
            elif fid in ids_seen:
                errors.append(f"core_features: duplicate id '{fid}'")
            else:
                ids_seen.add(fid)

            if not f.get("name"):
                errors.append(f"core_features[{i}].name must not be empty")

            priority = f.get("priority", "")
            if priority not in VALID_PRIORITIES:
                errors.append(
                    f"core_features[{i}].priority must be one of {VALID_PRIORITIES} "
                    f"(got: '{priority}')"
                )

    # ── user_flows ────────────────────────────────────────────────────────────
    flows = data["user_flows"]
    if not isinstance(flows, list):
        errors.append("user_flows must be an array")
    else:
        for i, fl in enumerate(flows):
            if not fl.get("id"):
                errors.append(f"user_flows[{i}].id must not be empty")
            if not fl.get("name"):
                errors.append(f"user_flows[{i}].name must not be empty")

    # ── open_questions ────────────────────────────────────────────────────────
    oq = data["open_questions"]
    if not isinstance(oq, list):
        errors.append("open_questions must be an array")
    else:
        for i, q in enumerate(oq):
            impact = q.get("impact", "")
            if impact and impact not in VALID_IMPACTS:
                errors.append(
                    f"open_questions[{i}].impact must be one of {VALID_IMPACTS} "
                    f"(got: '{impact}')"
                )

    # ── design_direction.context_preset (optional, but must be valid if present) ─
    dd = data.get("design_direction") or {}
    preset = dd.get("context_preset", "")
    # skip the not-yet-chosen placeholder (contains "|" in the schema template)
    if preset and "|" not in preset and preset not in VALID_PRESETS:
        errors.append(f"design_direction.context_preset must be one of {VALID_PRESETS} (got: '{preset}')")

    # ── scoring_criteria ──────────────────────────────────────────────────────
    sc = data.get("scoring_criteria")
    if sc is None:
        errors.append("scoring_criteria key must exist (if the TOR has no scoring table, use {} and minimum_viable: null)")
    elif isinstance(sc, dict):
        feature_ids = {f.get("id") for f in data.get("core_features", [])}
        feature_priority = {f.get("id"): f.get("priority") for f in data.get("core_features", [])}

        categories = sc.get("categories", [])
        if not isinstance(categories, list):
            errors.append("scoring_criteria.categories must be an array")
        else:
            for ci, cat in enumerate(categories):
                if not cat.get("id"):
                    errors.append(f"scoring_criteria.categories[{ci}].id must not be empty")
                for ii, item in enumerate(cat.get("items", [])):
                    t = item.get("type", "")
                    if t and t not in VALID_CRITERIA_TYPES:
                        errors.append(
                            f"scoring_criteria.categories[{ci}].items[{ii}].type "
                            f"must be one of {VALID_CRITERIA_TYPES} (got: '{t}')"
                        )
                    # cross-check: a functional criterion mapped to a feature must exist
                    fid = item.get("maps_to_feature")
                    if t == "functional" and fid and fid not in feature_ids:
                        errors.append(
                            f"scoring_criteria: '{item.get('name','')}' "
                            f"maps to feature '{fid}' which doesn't exist in core_features"
                        )

        mv = sc.get("minimum_viable")
        if mv and isinstance(mv, dict):
            for fid in mv.get("must_have_features", []):
                if fid not in feature_ids:
                    errors.append(
                        f"scoring_criteria.minimum_viable: must_have_feature '{fid}' "
                        f"not found in core_features"
                    )
                elif feature_priority.get(fid) != "Must":
                    errors.append(
                        f"scoring_criteria: feature '{fid}' is in must_have_features "
                        f"but its priority isn't Must (got: '{feature_priority.get(fid)}')"
                    )

    return errors


def main():
    if len(sys.argv) < 2:
        print("Usage: validate_brief.py <path/to/brief.json>", file=sys.stderr)
        sys.exit(1)

    path = sys.argv[1]
    errors = validate(path)

    if not errors:
        # summary stats
        with open(path) as f:
            data = json.load(f)
        features = data.get("core_features", [])
        must    = sum(1 for f in features if f.get("priority") == "Must")
        should  = sum(1 for f in features if f.get("priority") == "Should")
        could   = sum(1 for f in features if f.get("priority") == "Could")
        oq_count = len(data.get("open_questions", []))
        users    = len(data.get("target_users", []))
        flows    = len(data.get("user_flows", []))

        sc = data.get("scoring_criteria") or {}
        sc_items = sum(len(cat.get("items", [])) for cat in sc.get("categories", []))
        mv = sc.get("minimum_viable") or {}
        must_score_features = len(mv.get("must_have_features", []))

        preset = (data.get("design_direction") or {}).get("context_preset", "-")
        if preset and "|" in str(preset):
            preset = "- (not chosen yet)"

        print(f"[validate_brief] ✓ Valid")
        print(f"  Project   : {data['meta'].get('project_name', '-')}")
        print(f"  Confidence: {data['meta'].get('tor_confidence', '-')}")
        print(f"  Preset    : {preset}")
        print(f"  Users     : {users} personas")
        print(f"  Features  : {must} Must / {should} Should / {could} Could")
        print(f"  Flows     : {flows}")
        print(f"  Open Q    : {oq_count} items")
        print(f"  Scoring   : {sc_items} criteria · {must_score_features} must-have features")
        sys.exit(0)
    else:
        print(f"[validate_brief] ✗ Invalid — {len(errors)} error(s):", file=sys.stderr)
        for e in errors:
            print(f"  • {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
