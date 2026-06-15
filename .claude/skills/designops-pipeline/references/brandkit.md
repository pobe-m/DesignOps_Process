# Brand Kit — full token foundation (optional deepening of Step 2.6)

Step 2.6 produces a `brand.config.json` (a handful of resolved tokens — enough to theme the
shadcn prototype). **Brand Kit** is the heavier option: a verified, themeable **DTCG 3-tier
token foundation** (primitive → semantic → component), light + dark, that everything renders
from. Use it when the deliverable is a *design foundation*, not just a POC theme — or when the
output must build to multiple platforms.

The DTCG source-of-truth + validators are vendored at `references/tokens/`.

## Steps

1. **Brief Inference** (same as Step 2.6) — industry, audience, the one mood adjective, motion
   depth; anchor to an archetype/named system (`aesthetics/taste/`).
2. **Primitives** — brand color ramp in **OKLCH** (11 shades, consistent chroma) + a neutral ramp.
   The 500 shade must hit ≥ 4.5:1 on white (text), 600 ≥ 3:1 (UI). See
   `references/tokens/KIT-CONVENTIONS.md` → Color Generation.
3. **Semantic layer** — map roles to primitives: `action.primary`/`-hover`/`destructive`,
   `text.{primary,secondary,on-action,link}`, `surface.{page,card,raised}`,
   `border.{default,strong}`, `feedback.{success,warning,error,info}` + **designed dark overrides**
   (not inverted).
4. **Scales** — Major-Third type scale, 4px spacing scale, radius tiers, elevation, motion
   durations/easings (`references/tokens/tokens/*.json` are the shape to follow).
5. **Emit** the DTCG `tokens/*.json` (edit the vendored set) + build one `theme.css`. To regenerate
   platform artifacts: `node references/tokens/scripts/build_tokens.mjs` (`token-build.md`).

## Verify (definition of done — all gate-able)

```bash
python3 references/tokens/scripts/validate_tokens.py      # valid JSON + every {alias} resolves
python3 references/tokens/scripts/validate_contrast.py     # required text/action/border pairs pass AA, light AND dark
python3 references/tokens/scripts/validate_theme_refs.py   # every theme var(--…) resolves (needs the built theme.css)
```
- One theme, no per-page palettes; `destructive` = danger token (never primary); zero hardcoded values.
- Feed `audit_prototype.py` (Step 4.7) on the built prototype to re-verify contrast + no-hardcodes end-to-end.

> Relationship to Step 2.6: the aesthetic direction (named system / mood) is the *input*; Brand Kit
> turns it into a full token system. `brand.config.json` is the thin slice of that system the
> shadcn prototype consumes.
