#!/usr/bin/env python3
"""lint_font_imports.py — catch the remote-font `@import` trap in CSS (Turbopack dev 500).

Loading a webfont via a CSS `@import url("https://fonts.googleapis.com/…")` in globals.css
**500s the Next.js dev server under Turbopack**: the design system's own `@import "…/styles.css"`
is inlined first, which pushes the font @import after other rules and violates the CSS rule that
`@import` must precede all other statements. (`next build` tolerates it; `next dev` does not.)

The fix is always the same — load fonts with `next/font` (self-hosted, no remote @import). This
turns that documented gotcha into a runnable gate so a forgetful run can't reintroduce it.

Flags a CSS `@import` that points at a remote font (googleapis / gstatic / typekit / bunny, or any
remote URL whose path mentions a font). Local/relative `@import` is fine and ignored.

Usage:
  python3 lint_font_imports.py app/globals.css            # files
  python3 lint_font_imports.py app components              # dirs (scans .css/.scss)
Exit 0 = clean, 1 = a remote-font @import was found.
"""
import re
import sys
from pathlib import Path

CSS_EXT = {".css", ".scss", ".sass", ".less"}

# @import  url("…")  |  @import "…"  →  capture the imported target
IMPORT = re.compile(r"""@import\s+(?:url\(\s*)?["']?\s*([^"')\s;]+)""", re.I)
# remote font sources
FONT_HOST = re.compile(
    r"^https?://(?:[\w.-]*\.)?(?:fonts\.googleapis\.com|fonts\.gstatic\.com|use\.typekit\.net|"
    r"fonts\.bunny\.net|fontlibrary\.org|use\.fontawesome\.com)", re.I)
REMOTE = re.compile(r"^https?://", re.I)
LOOKS_FONT = re.compile(r"font", re.I)


def is_remote_font(url):
    if FONT_HOST.match(url):
        return True
    # any other remote stylesheet whose URL mentions a font (e.g. a self-rolled CDN path)
    return bool(REMOTE.match(url) and LOOKS_FONT.search(url))


def iter_files(paths):
    for p in paths:
        pp = Path(p)
        if pp.is_dir():
            for f in pp.rglob("*"):
                if f.suffix in CSS_EXT and "node_modules" not in f.parts:
                    yield f
        elif pp.is_file() and pp.suffix in CSS_EXT:
            yield pp


def main(argv):
    if not argv:
        print(__doc__)
        return 0
    files = list(iter_files(argv))
    violations = 0
    for f in files:
        try:
            text = f.read_text()
        except (UnicodeDecodeError, OSError):
            continue
        for n, line in enumerate(text.splitlines(), 1):
            s = line.strip()
            if s.startswith(("/*", "*", "//")):
                continue
            for m in IMPORT.finditer(line):
                if is_remote_font(m.group(1)):
                    print(f"{f}:{n}: remote-font @import '{m.group(1)}' — load fonts with "
                          f"next/font (this 500s the Turbopack dev server)")
                    violations += 1

    print(f"\nScanned {len(files)} CSS file(s).")
    if violations:
        print(f"FAIL: {violations} remote-font @import(s). Replace with next/font/google or "
              f"next/font/local — never an @import in globals.css.")
        return 1
    print("OK: no remote-font @import found.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
