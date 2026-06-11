# Component Audit — DESIGN.md / SKILL.md ↔ Figma ↔ Docs

> Generated: 2026-05-30 · Figma file `aZs8dlgg9wlcmEM0lFd3Zw` · 55 component pages

## Sources (4 dimensions)

| Dimension | Source |
|---|---|
| **Doc** | `SKILL.md` → `references/components.md` catalogue |
| **Figma** | Figma file component pages (first contiguous `↳` run) |
| **Built** | `components/ui/*.tsx` |
| **Docs** | `components/docs/registry.tsx` (docs site) |

> `references/DESIGN.md` is the token reference (1,804 tokens) — no component catalogue.

## Summary

| Metric | First audit | Latest |
|---|---|---|
| Documented (catalogue) | 48 | 56 |
| Figma component pages | 55 | 55 |
| Built (`components/ui`) | 18 | 52 |
| In docs site (registry) | 16 entries | 55 components + 4 design-token pages |
| Documented ∩ Figma | 47 | 55 |
| Figma but undocumented | 8 | 0 |
| Figma but not in docs | — | 0 |

## Status

- ✅ **Every Figma component is documented, built, and in the docs site.**
- ✅ Composition patterns `combobox` · `data-table` · `date-picker` are documented as composed
  examples in the docs site (no standalone `components/ui` file — they compose Popover/Command/
  Calendar/Table). Shown as **Built —** but **Docs ✅**.
- ⚪ `resizable` — valid shadcn component, absent from this Figma file; kept in the catalogue.

## Data-quality findings (Figma file)

Misspelled page names, normalized by the audit — fix in Figma for Code Connect:

| Figma page | Correct slug |
|---|---|
| `↳ Contex Menu` | context-menu |
| `↳ Seperator` | separator |
| `↳ Aspect Radio` | aspect-ratio |
| `↳ KPD` | kbd |

## Coverage Matrix

| Component | Group | Doc | Figma | Built | Docs |
|---|---|:---:|:---:|:---:|:---:|
| `accordion` | Data | ✅ | ✅ | ✅ | ✅ |
| `alert` | Feedback | ✅ | ✅ | ✅ | ✅ |
| `alert-dialog` | Overlay | ✅ | ✅ | ✅ | ✅ |
| `aspect-ratio` | Utility | ✅ | ✅ | ✅ | ✅ |
| `avatar` | Display | ✅ | ✅ | ✅ | ✅ |
| `badge` | Display | ✅ | ✅ | ✅ | ✅ |
| `breadcrumb` | Navigation | ✅ | ✅ | ✅ | ✅ |
| `button` | Form & Input | ✅ | ✅ | ✅ | ✅ |
| `button-group` | Form & Input | ✅ | ✅ | ✅ | ✅ |
| `calendar` | Utility | ✅ | ✅ | ✅ | ✅ |
| `card` | Display | ✅ | ✅ | ✅ | ✅ |
| `carousel` | Display | ✅ | ✅ | ✅ | ✅ |
| `chart` | Display | ✅ | ✅ | ✅ | ✅ |
| `checkbox` | Form & Input | ✅ | ✅ | ✅ | ✅ |
| `collapsible` | Data | ✅ | ✅ | ✅ | ✅ |
| `combobox` *(pattern)* | Form & Input | ✅ | ✅ | — | ✅ |
| `command` | Data | ✅ | ✅ | ✅ | ✅ |
| `context-menu` | Overlay | ✅ | ✅ | ✅ | ✅ |
| `data-table` *(pattern)* | Data | ✅ | ✅ | — | ✅ |
| `date-picker` *(pattern)* | Utility | ✅ | ✅ | — | ✅ |
| `dialog` | Overlay | ✅ | ✅ | ✅ | ✅ |
| `drawer` | Overlay | ✅ | ✅ | ✅ | ✅ |
| `dropdown-menu` | Overlay | ✅ | ✅ | ✅ | ✅ |
| `empty` | Display | ✅ | ✅ | ✅ | ✅ |
| `field` | Form & Input | ✅ | ✅ | ✅ | ✅ |
| `hover-card` | Overlay | ✅ | ✅ | ✅ | ✅ |
| `input` | Form & Input | ✅ | ✅ | ✅ | ✅ |
| `input-group` | Form & Input | ✅ | ✅ | ✅ | ✅ |
| `input-otp` | Form & Input | ✅ | ✅ | ✅ | ✅ |
| `item` | Display | ✅ | ✅ | ✅ | ✅ |
| `kbd` | Display | ✅ | ✅ | ✅ | ✅ |
| `label` | Form & Input | ✅ | ✅ | ✅ | ✅ |
| `menubar` | Navigation | ✅ | ✅ | ✅ | ✅ |
| `native-select` | Form & Input | ✅ | ✅ | ✅ | ✅ |
| `navigation-menu` | Navigation | ✅ | ✅ | ✅ | ✅ |
| `pagination` | Navigation | ✅ | ✅ | ✅ | ✅ |
| `popover` | Overlay | ✅ | ✅ | ✅ | ✅ |
| `progress` | Display | ✅ | ✅ | ✅ | ✅ |
| `radio-group` | Form & Input | ✅ | ✅ | ✅ | ✅ |
| `resizable` | Utility | ✅ | — | — | — |
| `scroll-area` | Utility | ✅ | ✅ | ✅ | ✅ |
| `select` | Form & Input | ✅ | ✅ | ✅ | ✅ |
| `separator` | Data | ✅ | ✅ | ✅ | ✅ |
| `sheet` | Overlay | ✅ | ✅ | ✅ | ✅ |
| `sidebar` | Navigation | ✅ | ✅ | ✅ | ✅ |
| `skeleton` | Display | ✅ | ✅ | ✅ | ✅ |
| `slider` | Form & Input | ✅ | ✅ | ✅ | ✅ |
| `sonner` | Feedback | ✅ | ✅ | ✅ | ✅ |
| `spinner` | Display | ✅ | ✅ | ✅ | ✅ |
| `switch` | Form & Input | ✅ | ✅ | ✅ | ✅ |
| `table` | Display | ✅ | ✅ | ✅ | ✅ |
| `tabs` | Navigation | ✅ | ✅ | ✅ | ✅ |
| `textarea` | Form & Input | ✅ | ✅ | ✅ | ✅ |
| `toggle` | Form & Input | ✅ | ✅ | ✅ | ✅ |
| `toggle-group` | Form & Input | ✅ | ✅ | ✅ | ✅ |
| `tooltip` | Overlay | ✅ | ✅ | ✅ | ✅ |

_56 components audited · 55 fully covered (documented + Figma + built/composed + in docs). Plus 4 design-token pages._
