# Image → Aesthetic (optional input path for Step 2.6)

When the TOR (or the user) provides a **reference image, screenshot, or mockup**, don't pick a
direction blind from the brand library — *infer* it from the reference, then anchor it to a known
system so the decisions stay stable. The output is still a normal `aesthetic.json` (same schema,
same `validate_aesthetic.py` gate). Match the design **system**, never copy logos/photos/copy.

## Method (read the reference like a designer)

1. **Palette** — one dominant surface family, the text colors, one primary action + at most one
   accent. Sample the actual hues; don't guess random hex.
2. **Type** — family feel (geometric / grotesk / serif), the scale jumps, display-vs-body contrast,
   weights.
3. **Spacing & density** — base unit, section rhythm, card padding; airy vs. compact → maps to
   `design_directives.density_target`.
4. **Radius & depth** — radius language (sharp / soft / pill); shadow vs. hairline separation.
5. **Layout archetype + sequence** — full-bleed hero / asymmetric split / bento / editorial stack
   (`aesthetics/taste/design-taste.md` → Variance Mandate).

## Anchor + resolve (reuse the vendored kit)

6. **Anchor to a known system** if the reference is close to one — it stabilizes the tokens:
   ```bash
   python3 .claude/skills/designops-pipeline/references/aesthetics/scripts/design_systems.py search <term>
   ```
   Set `direction.type` = `named_system` (the closest match) or `archetype`. The reference image
   informs the token *values*; the anchor keeps them coherent.
7. **Resolve tokens** exactly as Step 2.6 does: oklch primary/background/foreground/radius/font_sans
   + `fg_hex`/`bg_hex` for every contrast pair. A sampled brand color that fails the WCAG floor
   gets adjusted — **taste never overrides POUR**.
8. Record the inference in `aesthetic.json.brief_inference.rationale` ("inferred from reference: …")
   and note the source in `direction.why_fit`.

## Verify (same gate as Step 2.6)

`validate_aesthetic.py` recomputes contrast from your hex and checks the anchor resolves in the
library. At build time, `audit_prototype.py` (Step 4.7) re-verifies the built screens
(tokens + contrast + no emoji). The result matches the reference's *design language*, not a
pixel-perfect copy.
