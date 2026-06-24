#!/usr/bin/env python3
"""
audit_prototype.py — the Step 4.7 audit GATE, as a real runnable check (not agent judgment).

Ten objective, deterministic gates over the BUILT prototype:
  1. Token compliance — runs lint_hardcodes.py over the generated screens; any raw hex / px /
     ms / raw Tailwind palette utility (bg-gray-500 …) that isn't a token = a violation.
  2. WCAG contrast — parses the prototype's globals.css :root + .dark token blocks, converts
     each oklch value to sRGB itself, and checks the essential foreground/background pairs at
     the a11y target (AA 4.5:1 / AAA 7:1 normal text; 3:1 for UI borders). Light AND dark.
  3. UX copy — runs check_no_emoji.py: no emoji / em-dash in product UI (ux-writing).
  4. Component contracts — runs lint_component_contracts.py: enforces the Button/Dialog/Field
     usage contracts (icon-button accessible name, DialogTitle present, Input↔FieldLabel).
  5. Font loading — runs lint_font_imports.py: no remote-font @import in CSS (a Turbopack dev
     500 trap; load fonts with next/font instead).
  6. Theme fidelity — runs lint_theme_fidelity.py: the identity theme Step 2.6 committed
     (brand.config.json / aesthetic.json) must actually be applied in globals.css. Catches the
     "brand colour slapped on a neutral skeleton" regression where card/secondary/muted/border
     silently stay at the shadcn-neutral default.
  7. Directive fidelity — runs lint_directive_fidelity.py: the build must honor design_directives
     (Step 2.5) — destructive actions guarded when safeguard_level is on, an empty-state when
     guidance_level is guided (density/nav are advisory). Reads intelligence.json.
  8. Screen coverage — runs lint_screen_coverage.py: every Must screen in screen-inventory.json
     (Step 3.5) was actually built as an app route, rendering its declared loading/empty/error states.
  9. Edge-case coverage — runs lint_edge_coverage.py: every Must edge case in edge-cases.json
     (Step 3.7) is actually handled in the screen it maps to (empty/error/loading/partial state,
     inline validation, or a destructive confirm). The back end of the edge-case spine.
 10. Font fidelity — runs lint_font_fidelity.py: the font_sans Step 2.6 committed in
     brand.config.json must actually be applied in app/layout.* / globals.css (not left at the
     scaffold default). Catches the silent font no-op that gate 5/6 don't.
Gates 3-10 skip cleanly (—) if their checker / source artifact is missing.

By default it audits the GENERATED surface only — `components/ui` (vendored shadcn primitives),
any `docs/` dir (DS demos + these reports), and node_modules/.next/out are auto-excluded, so you
can point it at the whole prototype without it tripping over vendored code. Use --include-vendored
to audit everything.

Usage:
  python3 audit_prototype.py <prototype_dir> [--a11y AA|AAA] [--scan app,components,lib]
                             [--include-vendored] [--report path.md] [--theme brand.config.json]
                             [--intel intelligence.json] [--screens screen-inventory.json]
                             [--edges edge-cases.json]
Exit 0 = PASS, 1 = BLOCKED. Zero-dependency (imports vendored contrast.py + lint_hardcodes.py).
"""

import math
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "references" / "aesthetics" / "scripts"))
import contrast as _contrast  # vendored WCAG checker (ratio from hex)

# ux-writing emoji/dash checker (vendored under references/ux-writing/scripts)
_EMOJI_CHECK = HERE.parent / "references" / "ux-writing" / "scripts" / "check_no_emoji.py"

# component-usage contract checker (Button/Dialog/Field — references/component-contracts.md)
_CONTRACT_CHECK = HERE / "lint_component_contracts.py"

# remote-font @import checker (Turbopack dev 500 trap)
_FONT_CHECK = HERE / "lint_font_imports.py"

# theme-fidelity checker (did the committed Step 2.6 identity theme actually get applied?)
_FIDELITY_CHECK = HERE / "lint_theme_fidelity.py"

# font-fidelity checker (did the committed Step 2.6 font_sans actually get applied?)
_FONT_FIDELITY_CHECK = HERE / "lint_font_fidelity.py"

# directive-fidelity (gate 7) + screen-coverage (gate 8) + edge-coverage (gate 9) —
# did the build honor the upstream intent?
_DIRECTIVE_CHECK = HERE / "lint_directive_fidelity.py"
_SCREEN_CHECK = HERE / "lint_screen_coverage.py"
_EDGE_CHECK = HERE / "lint_edge_coverage.py"

# Required pairs FAIL the gate; advisory pairs are reported only. shadcn/ui token names.
REQUIRED_PAIRS = [
    ("foreground", "background", "body text on page"),
    ("card-foreground", "card", "text on card"),
    ("primary-foreground", "primary", "text on primary action"),
    ("secondary-foreground", "secondary", "text on secondary"),
    ("destructive-foreground", "destructive", "text on destructive"),
]
ADVISORY_PAIRS = [
    ("muted-foreground", "background", "muted/secondary text", 4.5),
    ("accent-foreground", "accent", "text on accent", 4.5),
    ("border", "background", "control border (WCAG 1.4.11)", 3.0),
    ("ring", "background", "focus ring", 3.0),
]
WCAG_NORMAL = {"A": 4.5, "AA": 4.5, "AAA": 7.0}


# ── oklch → sRGB hex (Björn Ottosson's OKLab matrices) ────────────────────────
def _srgb_gamma(c):
    c = max(0.0, min(1.0, c))
    return 12.92 * c if c <= 0.0031308 else 1.055 * (c ** (1 / 2.4)) - 0.055


def oklch_to_hex(L, C, h_deg):
    h = math.radians(h_deg)
    a, b = C * math.cos(h), C * math.sin(h)
    l_ = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m_ = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s_ = (L - 0.0894841775 * a - 1.2914855480 * b) ** 3
    r = 4.0767416621 * l_ - 3.3077115913 * m_ + 0.2309699292 * s_
    g = -1.2684380046 * l_ + 2.6097574011 * m_ - 0.3413193965 * s_
    bl = -0.0041960863 * l_ - 0.7034186147 * m_ + 1.7076147010 * s_
    return "#" + "".join(f"{round(_srgb_gamma(x) * 255):02x}" for x in (r, g, bl))


_OKLCH = re.compile(r"oklch\(\s*([0-9.]+%?)\s+([0-9.]+%?)\s+([0-9.]+)", re.I)
_DEF = re.compile(r"--([a-z0-9-]+)\s*:\s*(oklch\([^)]*\)|#[0-9a-fA-F]{3,8})", re.I)


def _num(tok):
    return float(tok[:-1]) / 100 if tok.endswith("%") else float(tok)


def _to_hex(value):
    """A token value (oklch(...) or #hex) → #rrggbb, or None if unparseable."""
    value = value.strip()
    if value.startswith("#"):
        return value
    m = _OKLCH.search(value)
    if not m:
        return None
    L, C, h = _num(m.group(1)), _num(m.group(2)), float(m.group(3))
    if L > 1:  # tolerate 0..100 lightness
        L /= 100
    return oklch_to_hex(L, C, h)


def _parse_blocks(css_text):
    """Return {block_name: {token: hex}} for :root and .dark."""
    blocks = {}
    for name, sel in (("light", r":root"), ("dark", r"\.dark")):
        m = re.search(sel + r"\s*\{(.*?)\}", css_text, re.S)
        if not m:
            continue
        toks = {}
        for d in _DEF.finditer(m.group(1)):
            hexv = _to_hex(d.group(2))
            if hexv:
                toks[d.group(1).lower()] = hexv
        blocks[name] = toks
    return blocks


# Vendored / non-UI paths the audit should not blame on the generated screens.
_SKIP_SEGMENTS = {"node_modules", ".next", "out", "docs"}


def _is_vendored(rel_posix):
    """True if a prototype-relative path is vendored DS / build / report (not generated)."""
    if "components/ui/" in rel_posix + "/":
        return True
    return any(seg in rel_posix.split("/") for seg in _SKIP_SEGMENTS)


def _collect_targets(proto, scan_dirs, include_vendored):
    """Files under the scan dirs, minus vendored DS internals (unless include_vendored)."""
    files = []
    for d in scan_dirs:
        base = proto / d
        if not base.is_dir():
            continue
        for f in base.rglob("*"):
            if not f.is_file():
                continue
            rel = f.relative_to(proto).as_posix()
            if not include_vendored and _is_vendored(rel):
                continue
            files.append(str(f))
    return files


# ── gate 1: token compliance (hardcoded values) ───────────────────────────────
def lint_gate(proto, scan_dirs, include_vendored):
    targets = _collect_targets(proto, scan_dirs, include_vendored)
    if not targets:
        return None, "no scan targets found"
    proc = subprocess.run([sys.executable, str(HERE / "lint_hardcodes.py"), *targets],
                          capture_output=True, text=True)
    return proc.returncode == 0, proc.stdout.strip()


# ── gate 3: UX copy — no emoji / no em-dash in product UI (ux-writing) ─────────
def emoji_gate(proto, scan_dirs, include_vendored):
    targets = _collect_targets(proto, scan_dirs, include_vendored)
    if not targets or not _EMOJI_CHECK.is_file():
        return None, "skipped (no targets or checker missing)"
    proc = subprocess.run([sys.executable, str(_EMOJI_CHECK), *targets],
                          capture_output=True, text=True)
    return proc.returncode == 0, proc.stdout.strip()


# ── gate 4: component usage contracts (Button/Dialog/Field a11y) ───────────────
def contract_gate(proto, scan_dirs, include_vendored):
    targets = _collect_targets(proto, scan_dirs, include_vendored)
    if not targets or not _CONTRACT_CHECK.is_file():
        return None, "skipped (no targets or checker missing)"
    proc = subprocess.run([sys.executable, str(_CONTRACT_CHECK), *targets],
                          capture_output=True, text=True)
    return proc.returncode == 0, proc.stdout.strip()


# ── gate 5: font loading — no remote-font @import (Turbopack dev 500 trap) ──────
def font_gate(proto, scan_dirs, include_vendored):
    targets = _collect_targets(proto, scan_dirs, include_vendored)
    if not targets or not _FONT_CHECK.is_file():
        return None, "skipped (no targets or checker missing)"
    proc = subprocess.run([sys.executable, str(_FONT_CHECK), *targets],
                          capture_output=True, text=True)
    return proc.returncode == 0, proc.stdout.strip()


# ── gate 6: theme fidelity — committed Step 2.6 theme must be applied in globals.css ──
def _find_theme(proto, explicit=None):
    """The committed theme json. Explicit --theme wins; else the canonical brand.config.json
    written by Step 2.6 right beside the prototype (output/brand.config.json → proto.parent).
    Deliberately narrow (brand.config.json only, no cwd walk) so an unrelated theme file in a
    sibling/temp dir can't bind to the wrong prototype."""
    if explicit:
        p = Path(explicit)
        return p if p.is_file() else None
    for base in (proto.parent, proto):
        c = base / "brand.config.json"
        if c.is_file():
            return c
    return None


def fidelity_gate(proto, theme_path=None):
    css = proto / "app" / "globals.css"
    theme = _find_theme(proto, theme_path)
    if not theme or not css.is_file() or not _FIDELITY_CHECK.is_file():
        return None, "skipped (no brand.config.json beside prototype, or checker missing)"
    proc = subprocess.run([sys.executable, str(_FIDELITY_CHECK), str(css), str(theme)],
                          capture_output=True, text=True)
    return proc.returncode == 0, (proc.stdout.strip() or proc.stderr.strip())


# ── gates 7 + 8: did the build honor the upstream intent? (auto-discover the artifact) ──
def _find_artifact(proto, names, explicit=None):
    if explicit:
        p = Path(explicit)
        return p if p.is_file() else None
    for base in (proto.parent, proto):
        for name in names:
            c = base / name
            if c.is_file():
                return c
    return None


def directive_gate(proto, intel_path=None):
    intel = _find_artifact(proto, ("intelligence.json",), intel_path)
    if not intel or not _DIRECTIVE_CHECK.is_file():
        return None, "skipped (no intelligence.json beside prototype, or checker missing)"
    proc = subprocess.run([sys.executable, str(_DIRECTIVE_CHECK), str(proto), str(intel)],
                          capture_output=True, text=True)
    return proc.returncode == 0, (proc.stdout.strip() or proc.stderr.strip())


def screen_gate(proto, screens_path=None):
    inv = _find_artifact(proto, ("screen-inventory.json",), screens_path)
    if not inv or not _SCREEN_CHECK.is_file():
        return None, "skipped (no screen-inventory.json beside prototype, or checker missing)"
    proc = subprocess.run([sys.executable, str(_SCREEN_CHECK), str(proto), str(inv)],
                          capture_output=True, text=True)
    return proc.returncode == 0, (proc.stdout.strip() or proc.stderr.strip())


def font_fidelity_gate(proto, theme_path=None):
    theme = _find_theme(proto, theme_path)
    if not theme or not _FONT_FIDELITY_CHECK.is_file():
        return None, "skipped (no brand.config.json/aesthetic.json beside prototype, or checker missing)"
    proc = subprocess.run([sys.executable, str(_FONT_FIDELITY_CHECK), str(proto), str(theme)],
                          capture_output=True, text=True)
    return proc.returncode == 0, (proc.stdout.strip() or proc.stderr.strip())


def edge_gate(proto, edges_path=None, screens_path=None):
    ec = _find_artifact(proto, ("edge-cases.json",), edges_path)
    if not ec or not _EDGE_CHECK.is_file():
        return None, "skipped (no edge-cases.json beside prototype, or checker missing)"
    inv = _find_artifact(proto, ("screen-inventory.json",), screens_path)
    cmd = [sys.executable, str(_EDGE_CHECK), str(proto), str(ec)]
    if inv:  # lets each edge resolve to its screen's route; without it the check is whole-app
        cmd.append(str(inv))
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return proc.returncode == 0, (proc.stdout.strip() or proc.stderr.strip())


# ── gate 2: WCAG contrast over the actual theme ───────────────────────────────
def contrast_gate(css_path, a11y):
    text = css_path.read_text(errors="ignore")
    blocks = _parse_blocks(text)
    threshold = WCAG_NORMAL.get(a11y, 4.5)
    failures, lines = [], []
    if not blocks:
        return False, ["no :root/.dark token block parsed from globals.css"]
    for mode, toks in blocks.items():
        for fg, bg, label in REQUIRED_PAIRS:
            if fg not in toks or bg not in toks:
                continue  # token not in theme (e.g. no destructive-foreground) — skip
            r = _contrast.ratio(toks[fg], toks[bg])
            ok = r + 1e-9 >= threshold
            lines.append(f"  [{mode}] {label:28} {toks[fg]} on {toks[bg]} = {r:.2f}:1  {'PASS' if ok else 'FAIL'} (≥{threshold})")
            if not ok:
                failures.append(f"[{mode}] {label}: {r:.2f}:1 < {threshold}:1 — adjust the token")
        for fg, bg, label, req in ADVISORY_PAIRS:
            if fg in toks and bg in toks:
                r = _contrast.ratio(toks[fg], toks[bg])
                lines.append(f"  [{mode}] {label:28} {toks[fg]} on {toks[bg]} = {r:.2f}:1  {'ok' if r >= req else 'advisory<'+str(req)}")
    return len(failures) == 0, lines, failures


def main(argv):
    args, a11y, scan, report, include_vendored, theme = [], "AA", ["app", "components", "lib"], None, False, None
    intel, screens_path, edges_path = None, None, None
    i = 0
    while i < len(argv):
        if argv[i] == "--a11y" and i + 1 < len(argv):
            a11y = argv[i + 1].replace("AA_plus", "AAA").upper(); i += 2
        elif argv[i] == "--scan" and i + 1 < len(argv):
            scan = argv[i + 1].split(","); i += 2
        elif argv[i] == "--include-vendored":
            include_vendored = True; i += 1
        elif argv[i] == "--report" and i + 1 < len(argv):
            report = argv[i + 1]; i += 2
        elif argv[i] == "--theme" and i + 1 < len(argv):
            theme = argv[i + 1]; i += 2
        elif argv[i] == "--intel" and i + 1 < len(argv):
            intel = argv[i + 1]; i += 2
        elif argv[i] == "--screens" and i + 1 < len(argv):
            screens_path = argv[i + 1]; i += 2
        elif argv[i] == "--edges" and i + 1 < len(argv):
            edges_path = argv[i + 1]; i += 2
        else:
            args.append(argv[i]); i += 1
    if not args:
        print(__doc__); return 2
    proto = Path(args[0])
    if not proto.is_dir():
        print(f"[audit_prototype] ✗ prototype dir not found: {proto}", file=sys.stderr); return 1

    out = [f"# Audit Report — Step 4.7 (a11y target: {a11y})", ""]

    # gate 1
    lint_ok, lint_out = lint_gate(proto, scan, include_vendored)
    out += ["## 1. Token compliance (no hardcoded values)",
            "```", lint_out or "(nothing scanned)", "```", ""]

    # gate 3 (UX copy: no emoji / em-dash in product UI)
    emoji_ok, emoji_out = emoji_gate(proto, scan, include_vendored)
    out += ["## 3. UX copy — no emoji / em-dash in UI (ux-writing)",
            "```", emoji_out or "(skipped)", "```", ""]

    # gate 4 (component usage contracts: Button/Dialog/Field a11y)
    contract_ok, contract_out = contract_gate(proto, scan, include_vendored)
    out += ["## 4. Component contracts (Button/Dialog/Field usage)",
            "```", contract_out or "(skipped)", "```", ""]

    # gate 5 (font loading: no remote-font @import — Turbopack dev 500 trap)
    font_ok, font_out = font_gate(proto, scan, include_vendored)
    out += ["## 5. Font loading (Turbopack-safe — no remote @import)",
            "```", font_out or "(skipped)", "```", ""]

    # gate 6 (theme fidelity: committed Step 2.6 identity theme actually applied)
    fidelity_ok, fidelity_out = fidelity_gate(proto, theme)
    out += ["## 6. Theme fidelity (committed Step 2.6 theme applied, not regressed to neutral)",
            "```", fidelity_out or "(skipped)", "```", ""]

    # gate 7 (directive fidelity: build honors design_directives — safeguard/guidance)
    directive_ok, directive_out = directive_gate(proto, intel)
    out += ["## 7. Directive fidelity (design_directives honored: safeguards, guidance)",
            "```", directive_out or "(skipped)", "```", ""]

    # gate 8 (screen coverage: every Must screen in the inventory was actually built)
    screen_ok, screen_out = screen_gate(proto, screens_path)
    out += ["## 8. Screen coverage (every Must screen built with its declared states)",
            "```", screen_out or "(skipped)", "```", ""]

    # gate 9 (edge-case coverage: every Must edge case is handled in the build)
    edge_ok, edge_out = edge_gate(proto, edges_path, screens_path)
    out += ["## 9. Edge-case coverage (every Must edge case handled in its screen)",
            "```", edge_out or "(skipped)", "```", ""]

    # gate 10 (font fidelity: committed Step 2.6 font_sans actually applied)
    font_fid_ok, font_fid_out = font_fidelity_gate(proto, theme)
    out += ["## 10. Font fidelity (committed Step 2.6 font applied, not the scaffold default)",
            "```", font_fid_out or "(skipped)", "```", ""]

    # gate 2
    css = proto / "app" / "globals.css"
    if css.is_file():
        cg = contrast_gate(css, a11y)
        contrast_ok, clines = cg[0], cg[1]
        cfails = cg[2] if len(cg) > 2 else []
        out += [f"## 2. WCAG contrast — {a11y} (from globals.css, light + dark)", "```", *clines, "```", ""]
    else:
        contrast_ok, cfails = False, [f"globals.css not found at {css}"]
        out += ["## 2. WCAG contrast", "globals.css not found — cannot verify.", ""]

    # gates that may be None (skipped) only fail when explicitly False
    blocked = not (lint_ok and contrast_ok and emoji_ok is not False
                   and contract_ok is not False and font_ok is not False
                   and fidelity_ok is not False and directive_ok is not False
                   and screen_ok is not False and edge_ok is not False
                   and font_fid_ok is not False)
    verdict = "🔴 BLOCKED" if blocked else "🟢 PASS"
    out += ["## Verdict", f"- Token compliance: {'🟢' if lint_ok else '🔴'}",
            f"- WCAG {a11y} contrast: {'🟢' if contrast_ok else '🔴'}",
            f"- UX copy (no emoji/dash): {'🟢' if emoji_ok else ('—' if emoji_ok is None else '🔴')}",
            f"- Component contracts: {'🟢' if contract_ok else ('—' if contract_ok is None else '🔴')}",
            f"- Font loading (no remote @import): {'🟢' if font_ok else ('—' if font_ok is None else '🔴')}",
            f"- Theme fidelity (no neutral regression): {'🟢' if fidelity_ok else ('—' if fidelity_ok is None else '🔴')}",
            f"- Directive fidelity (safeguards/guidance): {'🟢' if directive_ok else ('—' if directive_ok is None else '🔴')}",
            f"- Screen coverage (Must screens built): {'🟢' if screen_ok else ('—' if screen_ok is None else '🔴')}",
            f"- Edge-case coverage (Must edges handled): {'🟢' if edge_ok else ('—' if edge_ok is None else '🔴')}",
            f"- Font fidelity (committed font applied): {'🟢' if font_fid_ok else ('—' if font_fid_ok is None else '🔴')}",
            "", f"**{verdict}**"]
    if cfails:
        out += ["", "### Contrast failures", *[f"- {f}" for f in cfails]]

    report_text = "\n".join(out)
    if report:
        Path(report).parent.mkdir(parents=True, exist_ok=True)
        Path(report).write_text(report_text + "\n")

    # console summary
    print(f"[audit_prototype] {verdict} — token={'PASS' if lint_ok else 'FAIL'} · "
          f"WCAG {a11y}={'PASS' if contrast_ok else 'FAIL'} · "
          f"copy={'PASS' if emoji_ok else ('—' if emoji_ok is None else 'FAIL')} · "
          f"contracts={'PASS' if contract_ok else ('—' if contract_ok is None else 'FAIL')} · "
          f"font={'PASS' if font_ok else ('—' if font_ok is None else 'FAIL')} · "
          f"fidelity={'PASS' if fidelity_ok else ('—' if fidelity_ok is None else 'FAIL')} · "
          f"directive={'PASS' if directive_ok else ('—' if directive_ok is None else 'FAIL')} · "
          f"screens={'PASS' if screen_ok else ('—' if screen_ok is None else 'FAIL')} · "
          f"edges={'PASS' if edge_ok else ('—' if edge_ok is None else 'FAIL')} · "
          f"fontfid={'PASS' if font_fid_ok else ('—' if font_fid_ok is None else 'FAIL')}")
    if report:
        print(f"  → {report}")
    for f in cfails:
        print(f"  • {f}", file=sys.stderr)
    return 1 if blocked else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
