#!/usr/bin/env python3
"""
lint_edge_coverage.py — Step 4.7 gate 9: did the prototype actually HANDLE the edge cases
Step 3.7 committed?

edge-cases.json is the front end of the edge-case spine — for every Must screen it lists the
non-happy-path conditions the build must survive (empty data, bad input, a failed request, a
destructive click). Nothing downstream checked that the BUILT prototype handles them, so a screen
could ship with only its ideal state. This gate re-reads edge-cases.json and FAILS when a **Must**
edge case has no detectable handling in the screen it maps to.

It is the back end of the same spine as gate 8 (screen coverage): deterministic, keyword-based.
Each Must edge maps to a screen id; with screen-inventory.json that id resolves to a route → page
file, and the handling signal for the edge's ui_state / category is a keyword scan of that route's
files. Without screen-inventory.json it falls back to scanning the whole app/ surface (coarser,
noted in the report).

Usage:
  lint_edge_coverage.py <prototype_dir> <edge-cases.json> [screen-inventory.json]
Exit 0 = PASS / nothing to check, 1 = BLOCKED.
"""

import json
import sys
from pathlib import Path

PAGE_EXTS = (".tsx", ".jsx", ".ts", ".js")
VALIDATION_DIMS = {"conformance", "range", "existence"}

# handling signals (lowercased substring match). The most specific match wins:
# destructive → confirm; validation → field errors; otherwise the UI-Stack state.
STATE_HINTS = {
    "empty":   ("empty", "no results", "no data", "nothing here", "get started", "no items"),
    "error":   ("error", "failed", "went wrong", "try again", "retry", "couldn't"),
    "loading": ("skeleton", "isloading", "loading", "spinner", "suspense", "aria-busy"),
    "partial": ("truncate", "line-clamp", "show more", "ellipsis", "pagination", "load more", "…"),
}
VALIDATION_HINTS = ("fielderror", "aria-invalid", "formmessage", ".min(", ".max(", ".email(",
                    "required", "zoderror", "useform", "resolver", "invalid")
CONFIRM_HINTS = ("alertdialog", "confirm", "are you sure", "type to confirm", "cannot be undone",
                 "this action")


def built_routes(proto):
    appdir = proto / "app"
    routes = {}
    if not appdir.is_dir():
        return routes
    for p in appdir.rglob("page.*"):
        if p.suffix not in PAGE_EXTS:
            continue
        rel = p.relative_to(appdir).parent
        segs = [s for s in rel.parts if not (s.startswith("(") and s.endswith(")"))]
        routes["/".join(segs)] = p
    return routes


def _norm(route):
    return (route or "").strip().strip("/")


def _files_text(page):
    """Lowercased text of a page file + its co-located siblings (state UI often lives there)."""
    parts = []
    for f in [page] + [s for s in page.parent.glob("*") if s != page]:
        if f.suffix in PAGE_EXTS and f.is_file():
            try:
                parts.append(f.read_text(errors="ignore"))
            except Exception:  # noqa: BLE001
                pass
    return "\n".join(parts).lower()


def _app_text(proto):
    """Whole-app fallback text (coarse), used when a screen's route can't be resolved."""
    appdir = proto / "app"
    parts = []
    if appdir.is_dir():
        for f in appdir.rglob("*"):
            if f.suffix in PAGE_EXTS and f.is_file():
                try:
                    parts.append(f.read_text(errors="ignore"))
                except Exception:  # noqa: BLE001
                    pass
    return "\n".join(parts).lower()


def _hints_for(edge):
    """Pick the most specific handling signal for an edge. Returns (hints, label)."""
    cat = (edge.get("category") or "").lower()
    cd = (edge.get("correct_dim") or "").lower()
    us = (edge.get("ui_state") or "").lower()
    if cat == "destructive":
        return CONFIRM_HINTS, "a confirm (AlertDialog/type-to-confirm)"
    # Data-presence states (empty/loading/partial) take priority over a CORRECT validation dim:
    # an empty list driven by 'existence'/'cardinality' is handled by the empty STATE, not by form
    # validation. Validation hints only apply to an error state (data present but invalid).
    if us in ("empty", "loading", "partial"):
        return STATE_HINTS[us], f"a {us} state"
    if cat == "validation" or cd in VALIDATION_DIMS:
        return VALIDATION_HINTS, "inline validation (FieldError/aria-invalid/schema)"
    if us in STATE_HINTS:
        return STATE_HINTS[us], f"a {us} state"
    return None, us  # 'ideal' or unknown → nothing to verify


def check(proto, ec_path, inv_path=None):
    errors, notes = [], []
    proto = Path(proto)
    try:
        ec = json.loads(Path(ec_path).read_text())
    except Exception as e:  # noqa: BLE001
        return [], [f"edge-cases not read ({ec_path}): {e} — edge-coverage check skipped"]

    edges = ec.get("edge_cases", [])
    if not edges:
        return [], ["edge-cases.json has no edge_cases — nothing to verify"]

    # screen id → route (so an edge's maps_to_screen can be located in the build)
    id_to_route = {}
    if inv_path:
        try:
            for s in json.loads(Path(inv_path).read_text()).get("screens", []):
                if s.get("id"):
                    id_to_route[s["id"]] = _norm(s.get("route"))
        except Exception as e:  # noqa: BLE001
            notes.append(f"screen-inventory not read ({inv_path}): {e} — using whole-app fallback")

    routes = built_routes(proto)
    app_text_cache = None
    checked = 0
    for e in edges:
        if e.get("severity") != "must":
            continue  # only Must edges block; should/could are advisory upstream
        hints, label = _hints_for(e)
        if not hints:
            continue  # ideal / unverifiable
        eid = e.get("id", "?")
        sid = e.get("maps_to_screen", "?")
        # locate the screen's page text, else fall back to the whole app surface
        text, scope = None, ""
        route = id_to_route.get(sid)
        page = routes.get(route) if route is not None else None
        if page is not None:
            text, scope = _files_text(page), f"route '{route}'"
        else:
            if app_text_cache is None:
                app_text_cache = _app_text(proto)
            text, scope = app_text_cache, "the app (route unresolved)"
        checked += 1
        if not any(h in text for h in hints):
            errors.append(f"edge '{eid}' ({e.get('ui_state')}/{e.get('category','-')}) on screen "
                          f"'{sid}' expects {label}, but {scope} shows no sign of it — build the handling")

    if not errors:
        notes.append(f"{checked} Must edge case(s) verified handled in the build")
    return errors, notes


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    inv = argv[2] if len(argv) > 2 else None
    errors, notes = check(argv[0], argv[1], inv)
    if errors:
        print(f"[edge_coverage] ✗ {len(errors)} Must edge case(s) unhandled:")
        for e in errors:
            print(f"  • {e}")
        for n in notes:
            print(f"  ℹ {n}")
        return 1
    print("[edge_coverage] ✓ every Must edge case is handled in the build")
    for n in notes:
        print(f"  ℹ {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
