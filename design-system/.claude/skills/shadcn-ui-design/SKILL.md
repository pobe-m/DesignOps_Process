---
name: shadcn-ui-design
description: >-
  Build UI for this Next.js + Tailwind CSS v4 + shadcn/ui project using the
  project's design tokens. Use when creating or editing pages, components,
  layouts, forms, dialogs, tables, or any UI; when choosing colors, spacing,
  typography, or radius; or when setting up globals.css, fonts, or theming.
  Enforces semantic design tokens (neutral theme) over raw values.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash(npx shadcn*), Bash(python3*)
---

# shadcn/ui Design System

Build consistent UI for a **Next.js (App Router) · Tailwind CSS v4 · shadcn/ui** project.
Components are owned by the project in `components/ui/` and edited directly.

## Core Rules

**Always:**
- Use semantic token classes for color — `text-muted-foreground`, `bg-card`, `border-border` (see `references/DESIGN.md` QR-1)
- Use `cn()` from `@/lib/utils` for every conditional className
- Default new components to **Server Components** — add `"use client"` only when interactivity/hooks/browser APIs are needed (see `references/nextjs.md`)
- Use `size-4` not `w-4 h-4` (Tailwind v4)
- Use `next/font` for fonts, `next/image` for images
- Spacing on the 4px scale: `p-4` `gap-6` etc.

**Never:**
- Raw hex/rgb colors or `text-gray-500` — always a semantic token
- `tailwindcss-animate` — use `tw-animate-css`
- `React.forwardRef()` — use `React.ComponentProps<>` (React 19)
- Wrap a shadcn component to add a class — edit `components/ui/*.tsx` directly
- Extend colors in `tailwind.config.js` — use CSS variables in `globals.css`

## Token Quick Reference

| Need | Use | Detail |
|---|---|---|
| Colors | semantic token classes | `references/DESIGN.md` §QR-1, §A1 |
| Spacing | 4px scale (`p-4`, `gap-6`) | §QR-2 |
| Typography | Google Sans / Geist Mono | §QR-3 |
| Radius | `rounded-sm` btn, `rounded-lg` card | §QR-4 |
| Full token list (1,804) | exact values by collection | §A1–A16 |

The neutral theme: `primary` = `#171717`, `background` = `#ffffff`, `muted-foreground` = `#737373`,
`destructive` = `#dc2626`, `border` = `#e5e5e5`. Chart tokens use a Radix blue scale.

## Project Setup

Copy these into a new project (paths assume `@/*` → project root or `src/`):

| Asset | Destination | Purpose |
|---|---|---|
| `assets/globals.css` | `app/globals.css` | `@theme inline` tokens + light/dark `:root` |
| `assets/utils.ts` | `lib/utils.ts` | `cn()` helper |
| `assets/fonts.ts` | `lib/fonts.ts` | Google Sans + Geist Mono via `next/font` |

Then in `app/layout.tsx` wire fonts onto `<body>` and wrap with `next-themes`
`ThemeProvider` (full example in `references/nextjs.md` → Font Setup).

Initialize shadcn and add components:
```bash
npx shadcn@latest init -t next
npx shadcn@latest add button card dialog form table
```

## References

- **`references/DESIGN.md`** — all 1,804 design tokens (Quick Reference + full Appendix A1–A16). Consult for any exact color/spacing/size value.
- **`references/nextjs.md`** — App Router conventions: file roles, Server vs Client components, route groups, params, metadata, images, fonts.
- **`references/components.md`** — copy-paste shadcn/ui patterns: Button, Card, Form, Dialog, Table, Toast, Dropdown, plus page-shell / section-header / empty-state / skeleton compositions.

## Regenerating Tokens

The token reference is generated from the Figma export — never hand-edit it.
When `assets/variables-export.json` changes:
```bash
python3 scripts/generate_tokens.py
```
The script asserts the total (1,804) and verifies every variable is rendered.

## Accessibility (non-negotiable)

- Icon-only buttons need `aria-label`
- Form fields use `<FormLabel>` via `<FormField>`
- Dialogs include `<DialogTitle>` + `<DialogDescription>`
- Never remove the focus ring: `focus-visible:ring-2 focus-visible:ring-ring`
- Color is never the only signal — pair with text or icon

## Decision: where does a component go?

```
In shadcn catalogue?  → npx shadcn add <name>, then use/edit
Needs style change?   → className prop
Needs logic/variant?  → edit components/ui/*.tsx directly
Used across features? → components/shared/
Feature-specific?     → components/[feature]/
App chrome?           → components/layout/
```
