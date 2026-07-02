# Image Sourcing — Reference (Step 3.5 detect · Step 4 source)

Read this to decide **whether a screen needs imagery** and to **place free-license images** without
breaking the build. Two moves, two steps:

- **Step 3.5 (detect):** while building `screen-inventory.json`, add `image_needs[]` per screen from the
  screen type + the chosen aesthetic (`aesthetic.json`). Some directions are image-heavy (editorial,
  storytelling, marketing hero); many are flat/utility (dashboard, table tool) and need **no** imagery —
  don't add images a system wouldn't use.
- **Step 4 (source):** for each need, fetch a **free-license** image, place it via `next/image`, and
  record provenance. A placed asset that can't prove its licence or lacks `alt` does not ship.

---

## Does the screen need an image? (detect at 3.5)

| Screen / context | Likely `image_needs` |
|---|---|
| marketing / landing / hero | `hero`, `background` |
| empty state (0 records) | `empty_state_art` (an illustration, not a blank box) |
| profile / people / comments | `avatar` |
| catalog / gallery / cards | `thumbnail` |
| editorial / story / onboarding | `illustration` |
| dense tool / dashboard / table | usually **none** — chrome + data, not photography |

Drive it from the aesthetic: `aesthetic.json.brief_inference.mood_adjective` + `direction` say whether
the look is photographic/editorial (needs imagery) or flat/utility (doesn't). Match the system — a
Linear/utility direction with stock heroes reads as off-brand slop.

`image_needs[]` shape on a screen:
```jsonc
"image_needs": [{
  "kind": "hero|illustration|avatar|thumbnail|background|empty_state_art|icon_spot",
  "purpose": "<why this screen needs it>",
  "required": true,
  "sourced": {                       // added at Step 4, once an image is actually placed
    "source_url": "https://unsplash.com/photos/…",
    "license": "Unsplash License",   // or CC0 / Pexels License — must be a real free licence
    "attribution": "Photo by Jane Doe on Unsplash",
    "alt": "<meaningful alt text>"
  }
}]
```

---

## Source at Step 4 — free-license only, provenance always

1. **Free-license sources.** Unsplash / Pexels / Openverse (CC0) via their APIs, matched to the
   aesthetic's mood. Prefer real free-license stock over generated images (licensing is unambiguous).
2. **Record provenance on every placed asset** — `source_url`, `license`, `attribution`, `alt`. The gate
   (`validate_screens.py`) blocks a `sourced` need missing any of these: free-license still needs
   attribution, and `alt` is mandatory for accessibility (audit gate 4.7 also requires `alt` on `<Image>`).
3. **Never claim a licence you can't cite.** No provable free licence → don't place it; leave the need
   unsourced and log it. (Same evidence-or-silence discipline as the rest of the pipeline.)

## ⚠️ Build caveat — binary assets break Tailwind v4

Images are binary; Tailwind v4 scans the tree for content and reads `*.webp`/`*.png` as text → emits
garbage classes → **Turbopack/Lightning CSS 500s on every route** (`Unexpected token Delim`). `setup-prototype.sh`
scaffolds the guard (`@source not "../public"` + `@source not "../.next"` in `globals.css`). When adding
images:
- keep them in `public/` (already guarded) and load via `next/font`-style `next/image` (writes optimised
  binaries to `.next/cache/images`, also guarded);
- always give `<Image>` an `alt`;
- a nested git root means a local `.gitignore` alone isn't consulted by Tailwind — the `@source not`
  lines are the robust fix.

---

## Seam

`3.5 image_needs` → `Step 4 asset-prep` (fetch + place + record `sourced`) → the built screen. The gate
verifies provenance + alt; the taste/geometry audits verify the image doesn't wreck layout.
