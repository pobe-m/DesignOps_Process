# Folded design skills — capability index

All 19 design skills from `shadcn-skills-design-starter` are now folded into this pipeline,
vendored so it stays standalone. Most were already wired (aesthetic, audit, critique, tokens);
this index covers the 6 that were added last and where each plugs in.

| Skill | Plugs into | Reference | Gate / verify |
|-------|-----------|-----------|---------------|
| **ux-writing** | Step 3.5 draft + Step 4 screens + Step 4.6 critique | `ux-writing/voice-tone.md`, `ux-writing/i18n-rtl.md` | `audit_prototype.py` gate 3 (`ux-writing/scripts/check_no_emoji.py`) — no emoji / em-dash in UI |
| **image-to-code** | Step 2.6 input path (infer aesthetic from a mockup) | `image-to-code.md` | `validate_aesthetic.py` (same gate) |
| **brandkit** | Step 2.6 deepening → full DTCG token foundation | `brandkit.md`, `tokens/` | `tokens/scripts/validate_tokens.py` + `validate_contrast.py` + `validate_theme_refs.py` |
| **migrate-design-system** | Step 2.6 alternative resolution target (external DS) | `migrate-design-system.md`, `aesthetics/design-systems/{interop-protocol,crosswalk}.md` | `aesthetics/scripts/contrast.py` |
| **performance** | optional Step 4.7 add-on (Core Web Vitals) | `performance.md` | Lighthouse / `tokens/scripts/measure_render.mjs` (needs a running build) |
| **governance** | repo-maintenance (not generation) — for when this becomes a living DS | `governance.md` | SemVer + changelog + `tokens/scripts/validate_tokens.py` |

## How they relate to the pipeline

```
TOR ──► brief ──► intelligence(2.5) ──► aesthetic(2.6) ──► flows ──► screens(3.5) ──► prototype(4) ──► critique(4.6) ──► audit(4.7) ──► [storybook 4.8] ──► Figma(5)
                                          ▲   ▲   ▲                      ▲                  ▲                ▲
                            image-to-code ┘   │   └ migrate-design-system │     ux-writing ─┤     ux-writing │ (gate 3: no emoji)
                                  brandkit ────┘                          └─ ux-writing copy ┘     anti-slop  │
                                  (DTCG foundation)                                                performance┘ (optional)
```

- **Generation-time (fold tightly):** ux-writing, image-to-code, brandkit — they directly shape the
  artifacts. Wired into the relevant steps + gates above.
- **Optional / situational:** performance (needs a running build; enable like Storybook),
  migrate-design-system (only when an external DS is mandated).
- **Out of the generation loop:** governance — it's about evolving a *living* design system
  (SemVer, deprecation, contribution) over time. Vendored as reference for when this repo graduates
  from a frozen vendored DS into a maintained one.
