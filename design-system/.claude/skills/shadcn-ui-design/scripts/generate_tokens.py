#!/usr/bin/env python3
"""
Generate references/DESIGN.md from assets/variables-export.json.

Guarantees the output contains every variable from the export — no more, no less.
The script asserts the total (1,804) before writing and counts the rendered
table rows after writing.

Usage:
    python3 scripts/generate_tokens.py
"""

import json
import sys
from pathlib import Path
from collections import defaultdict

SKILL_DIR = Path(__file__).resolve().parent.parent
JSON_PATH = SKILL_DIR / "assets" / "variables-export.json"
OUT_PATH  = SKILL_DIR / "references" / "DESIGN.md"

EXPECTED_TOTAL = 1804


def to_hex(r, g, b):
    return "#{:02x}{:02x}{:02x}".format(
        int(round(r * 255)), int(round(g * 255)), int(round(b * 255))
    )


def get_val(v):
    mode_key = list(v["valuesByMode"].keys())[0]
    return v["valuesByMode"][mode_key]


def fmt_alpha(a):
    return "100%" if abs(a - 1.0) < 0.001 else f"{round(a * 100)}%"


def main():
    data = json.loads(JSON_PATH.read_text())
    variables = data["variables"]

    total = len(variables)
    assert total == EXPECTED_TOTAL, f"Expected {EXPECTED_TOTAL}, got {total}"

    by_col = defaultdict(list)
    for v in variables:
        by_col[v["collectionName"]].append(v)

    lines = []
    lx = lines.append

    # ── Header ──────────────────────────────────────────────
    lx("# Design Tokens — Full Reference")
    lx("")
    lx(f"> Auto-generated from `assets/variables-export.json` — {total} variables.")
    lx("> Regenerate with `python3 scripts/generate_tokens.py`. Do not edit by hand.")
    lx("")
    lx("---")
    lx("")

    # ── Quick Reference ─────────────────────────────────────
    lx("## Quick Reference")
    lx("")
    lx("### QR-1  Colors by Use")
    lx("")
    lx("Apply via Tailwind: `bg-<token>`, `text-<token>`, `border-<token>`, `ring-<token>`.")
    lx("")
    lx("| Token | Class | Hex | When to use |")
    lx("|---|---|---|---|")
    lx("| foreground | `text-foreground` | `#0a0a0a` | Body text, headings |")
    lx("| muted-foreground | `text-muted-foreground` | `#737373` | Helper text, placeholders |")
    lx("| background | `bg-background` | `#ffffff` | Page surface |")
    lx("| card | `bg-card` | `#ffffff` | Card / panel surface |")
    lx("| muted | `bg-muted` | `#f5f5f5` | Disabled, code block, skeleton |")
    lx("| accent | `bg-accent` | `#f5f5f5` | Hover highlight on nav items |")
    lx("| primary | `bg-primary` | `#171717` | Primary button fill |")
    lx("| secondary | `bg-secondary` | `#f5f5f5` | Secondary button fill |")
    lx("| destructive | `text-destructive` | `#dc2626` | Errors, destructive actions |")
    lx("| border | `border-border` | `#e5e5e5` | Dividers, outlines |")
    lx("| ring | `ring-ring` | `#737373` | Focus ring |")
    lx("| sidebar | `bg-sidebar` | `#fafafa` | Sidebar background |")
    lx("")
    lx("### QR-2  Spacing (base unit = 4px)")
    lx("")
    lx("| Class | px | Use |")
    lx("|---|---|---|")
    lx("| `p-1` `gap-1` | 4 | Icon-to-label gap |")
    lx("| `p-2` `gap-2` | 8 | Compact padding |")
    lx("| `p-4` `gap-4` | 16 | Standard card padding |")
    lx("| `p-6` `gap-6` | 24 | Section spacing |")
    lx("| `p-8` | 32 | Large gap |")
    lx("| `max-w-sm` | 384 | Narrow dialog |")
    lx("| `max-w-7xl` | 1280 | Page container |")
    lx("")
    lx("### QR-3  Typography")
    lx("")
    lx("Font: **Google Sans** (sans) · **Geist Mono** (mono).")
    lx("")
    lx("| Role | Classes |")
    lx("|---|---|")
    lx("| H1 | `text-4xl font-bold leading-10 tracking-tight` |")
    lx("| H2 | `text-2xl font-semibold leading-9 tracking-tight` |")
    lx("| H3 | `text-xl font-semibold leading-8` |")
    lx("| Body | `text-base font-normal leading-7` |")
    lx("| Label | `text-sm font-medium leading-5` |")
    lx("| Muted | `text-sm text-muted-foreground leading-6` |")
    lx("| Code | `font-mono text-sm` |")
    lx("")
    lx("### QR-4  Border Radius")
    lx("")
    lx("| Class | px | Use |")
    lx("|---|---|---|")
    lx("| `rounded-sm` | 4 | Buttons, inputs |")
    lx("| `rounded-md` | 6 | Tooltips |")
    lx("| `rounded-lg` | 8 | Cards, panels |")
    lx("| `rounded-xl` | 12 | Dialogs, sheets |")
    lx("| `rounded-full` | 9999 | Avatars, pills |")
    lx("")
    lx("---")
    lx("")

    # ── Appendix helpers ────────────────────────────────────
    lx("## Appendix: Full Token Reference")
    lx("")
    lx(f"All {total} variables, organized by collection.")
    lx("")

    appendix_start = len(lines)

    def color_flat(col_vars):
        lx("| Token | Alias | Hex | Alpha | Description |")
        lx("|---|---|---|---|---|")
        for v in col_vars:
            val = get_val(v)
            c = val["value"]
            alias = val.get("alias", "")
            desc = v.get("description", "").replace("|", "\\|").strip()
            if isinstance(c, dict) and "r" in c:
                lx(f'| `{v["name"]}` | {alias} | `{to_hex(c["r"], c["g"], c["b"])}` '
                   f'| {fmt_alpha(c.get("a", 1))} | {desc} |')
        lx("")

    def color_grouped(col_vars):
        fams = defaultdict(list)
        for v in col_vars:
            fam = v["name"].split("/")[0] if "/" in v["name"] else v["name"]
            fams[fam].append(v)
        for fam, fvars in fams.items():
            lx(f"**{fam}**")
            lx("")
            lx("| Token | Hex | Alpha |")
            lx("|---|---|---|")
            for v in fvars:
                c = get_val(v)["value"]
                lx(f'| `{v["name"]}` | `{to_hex(c["r"], c["g"], c["b"])}` '
                   f'| {fmt_alpha(c.get("a", 1))} |')
            lx("")

    def number_table(col_vars, unit="px"):
        lx(f"| Token | Value ({unit}) |")
        lx("|---|---|")
        for v in col_vars:
            lx(f'| `{v["name"]}` | `{get_val(v)["value"]}` |')
        lx("")

    # A1 shadcn-ui
    lx("### A1  shadcn-ui Semantic Tokens (35 variables)")
    lx("")
    color_flat(by_col["shadcn-ui"])

    # A2 tw-colors
    lx("### A2  Tailwind Color Palette — tw-colors (244 variables)")
    lx("")
    color_grouped(by_col["tw-colors"])

    # A3 rdx-colors
    lx("### A3  Radix Color Scale — rdx-colors (396 variables)")
    lx("")
    color_grouped(by_col["rdx-colors"])

    # A4 font
    lx("### A4  Typography — font (45 variables)")
    lx("")
    font_groups = defaultdict(list)
    for v in by_col["font"]:
        parts = v["name"].split("/")
        font_groups[parts[0] if len(parts) > 1 else "other"].append(v)
    for group, gvars in font_groups.items():
        lx(f"**font/{group}** ({len(gvars)} variables)")
        lx("")
        lx("| Token | Value |")
        lx("|---|---|")
        for v in gvars:
            lx(f'| `{v["name"]}` | `{get_val(v)["value"]}` |')
        lx("")

    # A5–A12 numeric
    numeric_specs = [
        ("tokens",     "A5",  "Base Token Scale — tokens (87 variables)", "px"),
        ("space",      "A6",  "Space Utilities — space (68 variables)", "px"),
        ("gap",        "A7",  "Gap Utilities — gap (102 variables)", "px"),
        ("margin",     "A8",  "Margin Utilities — margin (245 variables)", "px"),
        ("padding",    "A9",  "Padding Utilities — padding (245 variables)", "px"),
        ("height",     "A10", "Height Utilities — height (24 variables)", "px"),
        ("max-height", "A11", "Max Height Utilities — max-height (35 variables)", "px"),
        ("max-width",  "A12", "Max Width Utilities — max-width (51 variables)", "px"),
    ]
    for col_name, ref, title, unit in numeric_specs:
        lx(f"### {ref}  {title}")
        lx("")
        number_table(by_col[col_name], unit)

    # A13 border-radius (alias column)
    lx("### A13  Border Radius — border-radius (150 variables)")
    lx("")
    lx("| Token | Value (px) | Alias |")
    lx("|---|---|---|")
    for v in by_col["border-radius"]:
        val = get_val(v)
        lx(f'| `{v["name"]}` | `{val["value"]}` | {val.get("alias", "")} |')
    lx("")

    # A14–A16
    numeric_specs2 = [
        ("border-width", "A14", "Border Width — border-width (45 variables)", "px"),
        ("opacity",      "A15", "Opacity — opacity (21 variables)", "%"),
        ("stroke-width", "A16", "Stroke Width — stroke-width (11 variables)", "value"),
    ]
    for col_name, ref, title, unit in numeric_specs2:
        lx(f"### {ref}  {title}")
        lx("")
        number_table(by_col[col_name], unit)

    # Count table
    lx("### Token Count Verification")
    lx("")
    lx("| Collection | Variables |")
    lx("|---|---|")
    grand = 0
    for col in data["collections"]:
        lx(f'| {col["name"]} | {col["variableCount"]} |')
        grand += col["variableCount"]
    lx(f"| **TOTAL** | **{grand}** |")
    lx("")
    lx(f"> Source: `variables-export.json` — {grand} variables total.")

    content = "\n".join(lines)
    OUT_PATH.write_text(content)

    # Verify
    appendix_rows = [l for l in lines[appendix_start:] if l.startswith("| `")]
    print(f"Wrote {OUT_PATH.relative_to(SKILL_DIR)} "
          f"({len(content):,} chars, {len(lines):,} lines)")
    print(f"Appendix token rows: {len(appendix_rows)} (expected {EXPECTED_TOTAL})")
    if len(appendix_rows) != EXPECTED_TOTAL:
        print("ERROR: token count mismatch", file=sys.stderr)
        sys.exit(1)
    print("OK — all variables present, none missing, none extra.")


if __name__ == "__main__":
    main()
