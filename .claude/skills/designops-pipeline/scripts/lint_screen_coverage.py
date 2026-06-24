#!/usr/bin/env python3
"""
lint_screen_coverage.py — Step 4.7 gate 8: did the prototype actually build the screens
Step 3.5 committed?

screen-inventory.json is the build manifest (every Must screen + the data-states it must
render). Nothing downstream checked that the BUILT prototype contains them, so a Must screen
could silently never get built (or render only the happy path). This gate re-reads the manifest
and FAILS when a Must screen has no route page, or a declared state (loading/empty/error) is
nowhere in that route.

It is deterministic: each screen carries a `route`, mapped to Next.js app-router page files
(route groups `(x)` ignored), and state presence is a keyword scan of the route's files.

Usage:
  lint_screen_coverage.py <prototype_dir> <screen-inventory.json>
Exit 0 = PASS / nothing to check, 1 = BLOCKED.
"""

import json
import sys
from pathlib import Path

PAGE_EXTS = (".tsx", ".jsx", ".ts", ".js")
# keyword hints that a data-state is rendered (lowercased substring match)
STATE_HINTS = {
    "loading": ("skeleton", "isloading", "loading", "spinner", "suspense", "aria-busy"),
    "empty":   ("empty", "no results", "no data", "nothing here", "get started"),
    "error":   ("error", "failed", "went wrong", "try again", "retry"),
}


def built_routes(proto):
    """Map normalized route → page file for every app-router page (route groups stripped)."""
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


def _route_text(page):
    """Lowercased text of the route's page file + its co-located siblings (state UI often lives there)."""
    parts = []
    try:
        parts.append(page.read_text(errors="ignore"))
    except Exception:  # noqa: BLE001
        pass
    for sib in page.parent.glob("*"):
        if sib != page and sib.suffix in PAGE_EXTS and sib.is_file():
            try:
                parts.append(sib.read_text(errors="ignore"))
            except Exception:  # noqa: BLE001
                pass
    return "\n".join(parts).lower()


def check(proto, inv_path):
    errors, notes = [], []
    proto = Path(proto)
    inv, _ = (None, None)
    try:
        inv = json.loads(Path(inv_path).read_text())
    except Exception as e:  # noqa: BLE001
        return [], [f"screen-inventory not read ({inv_path}): {e} — coverage check skipped"]

    screens = inv.get("screens", [])
    if not screens:
        return [], ["screen-inventory has no screens — nothing to verify"]

    routes = built_routes(proto)
    built = 0
    for s in screens:
        must = s.get("priority") == "Must"
        raw = s.get("route")
        route = _norm(raw)        # a root route "/" normalizes to "" — that's the app/page.tsx root, NOT "missing"
        name = s.get("name", s.get("id", "?"))
        if not raw:               # only a truly absent/blank route field is "no route"
            if must:
                errors.append(f"Must screen '{name}' has no route in the manifest — cannot verify it was built")
            continue
        page = routes.get(route)
        if page is None:
            msg = f"screen '{name}' (route '{route}') has no app/{route}/page.* in the built prototype"
            (errors if must else notes).append(msg + ("" if must else " — Should/Could, advisory"))
            continue
        built += 1
        text = _route_text(page)
        for st in s.get("states", []) or []:
            hints = STATE_HINTS.get(st, ())
            if hints and not any(h in text for h in hints):
                errors.append(f"screen '{name}' (route '{route}') declares a '{st}' state but its page "
                              f"renders no sign of it ({'/'.join(hints[:3])}…) — build the {st} state")

    if not errors:
        notes.append(f"{built}/{len(screens)} screens built; declared states present")
    return errors, notes


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    errors, notes = check(argv[0], argv[1])
    if errors:
        print(f"[screen_coverage] ✗ {len(errors)} screen(s) not built / incomplete:")
        for e in errors:
            print(f"  • {e}")
        for n in notes:
            print(f"  ℹ {n}")
        return 1
    print("[screen_coverage] ✓ every Must screen is built with its declared states")
    for n in notes:
        print(f"  ℹ {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
