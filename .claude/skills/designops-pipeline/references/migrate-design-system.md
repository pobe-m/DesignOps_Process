# Migrate / Interop Design System (optional)

Bridge our shadcn token system **to or from** an external design system (Material 3, Apple HIG,
Fluent 2, Carbon, Ant, Radix, Chakra…) by mapping **roles**, not hex. Use when a TOR mandates a
specific external system, or when the prototype must build on someone else's foundation.

Vendored references (under `references/aesthetics/design-systems/`):
- `interop-protocol.md` — the Crosswalk Method (map by role/intent across 6 axes: color roles,
  type scale, spacing unit, radius, elevation, motion), the three directions, verification.
- `crosswalk.md` — curated role tables for Material 3 / Apple HIG / Fluent 2 / Carbon / shadcn / Radix.

## Directions

- **FROM** external → our tokens (adopt their look): re-point `semantic.*` to their color roles.
- **TO** external stack (our components on their foundation): theme their primitives with our tokens.
- **Migrate**: Audit → Map → Bridge (alias layer) → Verify, screen by screen.

## Verify

Every mapped color pair through `references/aesthetics/scripts/contrast.py` (light + dark); confirm
all 8 states + dark mode survive the mapping. Then `audit_prototype.py` on the built result.

> Where it fits the pipeline: this is an alternative resolution target for Step 2.6 — instead of
> resolving the chosen aesthetic to our neutral shadcn tokens, resolve it onto (or from) the
> external system named in the TOR. The `aesthetic.json` gate still applies.
