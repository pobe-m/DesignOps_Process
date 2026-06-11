# Design Tokens — Full Reference

> Auto-generated from `assets/variables-export.json` — 1804 variables.
> Regenerate with `python3 scripts/generate_tokens.py`. Do not edit by hand.

---

## Quick Reference

### QR-1  Colors by Use

Apply via Tailwind: `bg-<token>`, `text-<token>`, `border-<token>`, `ring-<token>`.

| Token | Class | Hex | When to use |
|---|---|---|---|
| foreground | `text-foreground` | `#0a0a0a` | Body text, headings |
| muted-foreground | `text-muted-foreground` | `#737373` | Helper text, placeholders |
| background | `bg-background` | `#ffffff` | Page surface |
| card | `bg-card` | `#ffffff` | Card / panel surface |
| muted | `bg-muted` | `#f5f5f5` | Disabled, code block, skeleton |
| accent | `bg-accent` | `#f5f5f5` | Hover highlight on nav items |
| primary | `bg-primary` | `#171717` | Primary button fill |
| secondary | `bg-secondary` | `#f5f5f5` | Secondary button fill |
| destructive | `text-destructive` | `#dc2626` | Errors, destructive actions |
| border | `border-border` | `#e5e5e5` | Dividers, outlines |
| ring | `ring-ring` | `#737373` | Focus ring |
| sidebar | `bg-sidebar` | `#fafafa` | Sidebar background |

### QR-2  Spacing (base unit = 4px)

| Class | px | Use |
|---|---|---|
| `p-1` `gap-1` | 4 | Icon-to-label gap |
| `p-2` `gap-2` | 8 | Compact padding |
| `p-4` `gap-4` | 16 | Standard card padding |
| `p-6` `gap-6` | 24 | Section spacing |
| `p-8` | 32 | Large gap |
| `max-w-sm` | 384 | Narrow dialog |
| `max-w-7xl` | 1280 | Page container |

### QR-3  Typography

Font: **Google Sans** (sans) · **Geist Mono** (mono).

| Role | Classes |
|---|---|
| H1 | `text-4xl font-bold leading-10 tracking-tight` |
| H2 | `text-2xl font-semibold leading-9 tracking-tight` |
| H3 | `text-xl font-semibold leading-8` |
| Body | `text-base font-normal leading-7` |
| Label | `text-sm font-medium leading-5` |
| Muted | `text-sm text-muted-foreground leading-6` |
| Code | `font-mono text-sm` |

### QR-4  Border Radius

| Class | px | Use |
|---|---|---|
| `rounded-sm` | 4 | Buttons, inputs |
| `rounded-md` | 6 | Tooltips |
| `rounded-lg` | 8 | Cards, panels |
| `rounded-xl` | 12 | Dialogs, sheets |
| `rounded-full` | 9999 | Avatars, pills |

---

## Appendix: Full Token Reference

All 1804 variables, organized by collection.

### A1  shadcn-ui Semantic Tokens (35 variables)

| Token | Alias | Hex | Alpha | Description |
|---|---|---|---|---|
| `backgrund` | white | `#ffffff` | 100% | The page shell, page sections, and default text. |
| `foreground` | neutral/950 | `#0a0a0a` | 100% | The page shell, page sections, and default text. |
| `Card` | white | `#ffffff` | 100% | Card, dashboard panels, settings panels. |
| `Card-foregrund` | neutral/950 | `#0a0a0a` | 100% | Card, dashboard panels, settings panels. |
| `popover` | white | `#ffffff` | 100% | Popover, DropdownMenu, ContextMenu, and other overlays. |
| `popover-foregrund` | neutral/950 | `#0a0a0a` | 100% | Popover, DropdownMenu, ContextMenu, and other overlays. |
| `primary` | neutral/900 | `#171717` | 100% | Default Button, selected states, badges, and active accents. |
| `primary-foregrund` | neutral/50 | `#fafafa` | 100% | Default Button, selected states, badges, and active accents. |
| `secondary` | neutral/100 | `#f5f5f5` | 100% | Secondary buttons, secondary badges, and supporting UI. |
| `secondary-foregrund` | neutral/950 | `#0a0a0a` | 100% | Secondary buttons, secondary badges, and supporting UI. |
| `muted` | neutral/100 | `#f5f5f5` | 100% |  |
| `muted-foregrund` | neutral/500 | `#737373` | 100% |  |
| `accent` | neutral/100 | `#f5f5f5` | 100% | Descriptions, placeholders, empty states, helper text, and subdued surfaces. |
| `accent-foregrund` | neutral/900 | `#171717` | 100% | Descriptions, placeholders, empty states, helper text, and subdued surfaces. |
| `destructive` | red/600 | `#dc2626` | 100% |  |
| `border` | neutral/200 | `#e5e5e5` | 100% |  |
| `input` | neutral/200 | `#e5e5e5` | 100% |  |
| `ring` | neutral/500 | `#737373` | 100% |  |
| `chart-1` | blue/8 | `#5eb1ef` | 100% |  |
| `chart-2` | blue/9 | `#0090ff` | 100% |  |
| `chart-3` | blue/10 | `#0588f0` | 100% |  |
| `chart-4` | blue/11 | `#0d74ce` | 100% |  |
| `chart-5` | blue/12 | `#113264` | 100% |  |
| `sidebar` | neutral/50 | `#fafafa` | 100% |  |
| `sidebar-foregrund` | neutral/950 | `#0a0a0a` | 100% |  |
| `sidebar-primary` | neutral/900 | `#171717` | 100% |  |
| `sidebar-primary-foregrund` | neutral/50 | `#fafafa` | 100% |  |
| `sidebar-accent` | neutral/100 | `#f5f5f5` | 100% |  |
| `sidebar-accent-foregrund` | neutral/900 | `#171717` | 100% |  |
| `sidebar-border` | neutral/300 | `#d4d4d4` | 100% |  |
| `sidebar-ring` | neutral/500 | `#737373` | 100% |  |
| `background-color` | black/5 | `#000000` | 30% |  |
| `semantic-background` | gray/500 | `#6b7280` | 100% |  |
| `semantic-border` | gray/600 | `#4b5563` | 100% |  |
| `semantic-foreground` | white | `#ffffff` | 100% |  |

### A2  Tailwind Color Palette — tw-colors (244 variables)

**slate**

| Token | Hex | Alpha |
|---|---|---|
| `slate/50` | `#f8fafc` | 100% |
| `slate/100` | `#f1f5f9` | 100% |
| `slate/200` | `#e2e8f0` | 100% |
| `slate/300` | `#cbd5e1` | 100% |
| `slate/400` | `#94a3b8` | 100% |
| `slate/500` | `#64748b` | 100% |
| `slate/600` | `#475569` | 100% |
| `slate/700` | `#334155` | 100% |
| `slate/800` | `#1e293b` | 100% |
| `slate/900` | `#0f172a` | 100% |
| `slate/950` | `#020617` | 100% |

**gray**

| Token | Hex | Alpha |
|---|---|---|
| `gray/50` | `#f9fafb` | 100% |
| `gray/100` | `#f3f4f6` | 100% |
| `gray/200` | `#e5e7eb` | 100% |
| `gray/300` | `#d1d5db` | 100% |
| `gray/400` | `#9ca3af` | 100% |
| `gray/500` | `#6b7280` | 100% |
| `gray/600` | `#4b5563` | 100% |
| `gray/700` | `#374151` | 100% |
| `gray/800` | `#1f2937` | 100% |
| `gray/900` | `#111827` | 100% |
| `gray/950` | `#030712` | 100% |

**zinc**

| Token | Hex | Alpha |
|---|---|---|
| `zinc/50` | `#fafafa` | 100% |
| `zinc/100` | `#f4f4f5` | 100% |
| `zinc/200` | `#e4e4e7` | 100% |
| `zinc/300` | `#d4d4d8` | 100% |
| `zinc/400` | `#a1a1aa` | 100% |
| `zinc/500` | `#71717a` | 100% |
| `zinc/600` | `#52525b` | 100% |
| `zinc/700` | `#3f3f46` | 100% |
| `zinc/800` | `#27272a` | 100% |
| `zinc/900` | `#18181b` | 100% |
| `zinc/950` | `#09090b` | 100% |

**neutral**

| Token | Hex | Alpha |
|---|---|---|
| `neutral/50` | `#fafafa` | 100% |
| `neutral/100` | `#f5f5f5` | 100% |
| `neutral/200` | `#e5e5e5` | 100% |
| `neutral/300` | `#d4d4d4` | 100% |
| `neutral/400` | `#a3a3a3` | 100% |
| `neutral/500` | `#737373` | 100% |
| `neutral/600` | `#525252` | 100% |
| `neutral/700` | `#404040` | 100% |
| `neutral/800` | `#262626` | 100% |
| `neutral/900` | `#171717` | 100% |
| `neutral/950` | `#0a0a0a` | 100% |

**stone**

| Token | Hex | Alpha |
|---|---|---|
| `stone/50` | `#fafaf9` | 100% |
| `stone/100` | `#f5f5f4` | 100% |
| `stone/200` | `#e7e5e4` | 100% |
| `stone/300` | `#d6d3d1` | 100% |
| `stone/400` | `#a8a29e` | 100% |
| `stone/500` | `#78716c` | 100% |
| `stone/600` | `#57534e` | 100% |
| `stone/700` | `#44403c` | 100% |
| `stone/800` | `#292524` | 100% |
| `stone/900` | `#1c1917` | 100% |
| `stone/950` | `#0c0a09` | 100% |

**red**

| Token | Hex | Alpha |
|---|---|---|
| `red/50` | `#fef2f2` | 100% |
| `red/100` | `#fee2e2` | 100% |
| `red/200` | `#fca5a5` | 100% |
| `red/300` | `#f87171` | 100% |
| `red/400` | `#f87171` | 100% |
| `red/500` | `#ef4444` | 100% |
| `red/600` | `#dc2626` | 100% |
| `red/700` | `#b91c1c` | 100% |
| `red/800` | `#991b1b` | 100% |
| `red/900` | `#7f1d1d` | 100% |
| `red/950` | `#450a0a` | 100% |

**orange**

| Token | Hex | Alpha |
|---|---|---|
| `orange/50` | `#fff7ed` | 100% |
| `orange/100` | `#ffedd5` | 100% |
| `orange/200` | `#fed7aa` | 100% |
| `orange/300` | `#fdba74` | 100% |
| `orange/400` | `#fb923c` | 100% |
| `orange/500` | `#f97316` | 100% |
| `orange/600` | `#ea580c` | 100% |
| `orange/700` | `#c2410c` | 100% |
| `orange/800` | `#9a3412` | 100% |
| `orange/900` | `#7c2d12` | 100% |
| `orange/950` | `#431407` | 100% |

**amber**

| Token | Hex | Alpha |
|---|---|---|
| `amber/50` | `#fffbeb` | 100% |
| `amber/100` | `#fef3c7` | 100% |
| `amber/200` | `#fde68a` | 100% |
| `amber/300` | `#fcd34d` | 100% |
| `amber/400` | `#fbbf24` | 100% |
| `amber/500` | `#f59e0b` | 100% |
| `amber/600` | `#d97706` | 100% |
| `amber/700` | `#b45309` | 100% |
| `amber/800` | `#92400e` | 100% |
| `amber/900` | `#78350f` | 100% |
| `amber/950` | `#451a03` | 100% |

**yellow**

| Token | Hex | Alpha |
|---|---|---|
| `yellow/50` | `#fefce8` | 100% |
| `yellow/100` | `#fef9c3` | 100% |
| `yellow/200` | `#fef08a` | 100% |
| `yellow/300` | `#fde047` | 100% |
| `yellow/400` | `#facc15` | 100% |
| `yellow/500` | `#eab308` | 100% |
| `yellow/600` | `#ca8a04` | 100% |
| `yellow/700` | `#a16207` | 100% |
| `yellow/800` | `#854d0e` | 100% |
| `yellow/900` | `#713f12` | 100% |
| `yellow/950` | `#422006` | 100% |

**lime**

| Token | Hex | Alpha |
|---|---|---|
| `lime/50` | `#f7fee7` | 100% |
| `lime/100` | `#ecfccb` | 100% |
| `lime/200` | `#d9f99d` | 100% |
| `lime/300` | `#bef264` | 100% |
| `lime/400` | `#a3e635` | 100% |
| `lime/500` | `#84cc16` | 100% |
| `lime/600` | `#65a30d` | 100% |
| `lime/700` | `#4d7c0f` | 100% |
| `lime/800` | `#3f6212` | 100% |
| `lime/900` | `#365314` | 100% |
| `lime/950` | `#1a2e05` | 100% |

**green**

| Token | Hex | Alpha |
|---|---|---|
| `green/50` | `#f0fdf4` | 100% |
| `green/100` | `#dcfce7` | 100% |
| `green/200` | `#bbf7d0` | 100% |
| `green/300` | `#86efac` | 100% |
| `green/400` | `#4ade80` | 100% |
| `green/500` | `#22c55e` | 100% |
| `green/600` | `#16a34a` | 100% |
| `green/700` | `#15803d` | 100% |
| `green/800` | `#166534` | 100% |
| `green/900` | `#14532d` | 100% |
| `green/950` | `#052e16` | 100% |

**emerald**

| Token | Hex | Alpha |
|---|---|---|
| `emerald/50` | `#ecfdf5` | 100% |
| `emerald/100` | `#d1fae5` | 100% |
| `emerald/200` | `#a7f3d0` | 100% |
| `emerald/300` | `#6ee7b7` | 100% |
| `emerald/400` | `#34d399` | 100% |
| `emerald/500` | `#10b981` | 100% |
| `emerald/600` | `#059669` | 100% |
| `emerald/700` | `#047857` | 100% |
| `emerald/800` | `#065f46` | 100% |
| `emerald/900` | `#064e3b` | 100% |
| `emerald/950` | `#022c22` | 100% |

**teal**

| Token | Hex | Alpha |
|---|---|---|
| `teal/50` | `#f0fdfa` | 100% |
| `teal/100` | `#ccfbf1` | 100% |
| `teal/200` | `#99f6e4` | 100% |
| `teal/300` | `#5eead4` | 100% |
| `teal/400` | `#2dd4bf` | 100% |
| `teal/500` | `#14b8a6` | 100% |
| `teal/600` | `#0d9488` | 100% |
| `teal/700` | `#0f766e` | 100% |
| `teal/800` | `#115e59` | 100% |
| `teal/900` | `#134e4a` | 100% |
| `teal/950` | `#042f2e` | 100% |

**cyan**

| Token | Hex | Alpha |
|---|---|---|
| `cyan/50` | `#ecfeff` | 100% |
| `cyan/100` | `#cffafe` | 100% |
| `cyan/200` | `#a5f3fc` | 100% |
| `cyan/300` | `#67e8f9` | 100% |
| `cyan/400` | `#22d3ee` | 100% |
| `cyan/500` | `#06b6d4` | 100% |
| `cyan/600` | `#0891b2` | 100% |
| `cyan/700` | `#0e7490` | 100% |
| `cyan/800` | `#155e75` | 100% |
| `cyan/900` | `#164e63` | 100% |
| `cyan/950` | `#083344` | 100% |

**sky**

| Token | Hex | Alpha |
|---|---|---|
| `sky/50` | `#f0f9ff` | 100% |
| `sky/100` | `#e0f2fe` | 100% |
| `sky/200` | `#bae6fd` | 100% |
| `sky/300` | `#7dd3fc` | 100% |
| `sky/400` | `#38bdf8` | 100% |
| `sky/500` | `#0ea5e9` | 100% |
| `sky/600` | `#0284c7` | 100% |
| `sky/700` | `#0369a1` | 100% |
| `sky/800` | `#075985` | 100% |
| `sky/900` | `#0c4a6e` | 100% |
| `sky/950` | `#082f49` | 100% |

**blue**

| Token | Hex | Alpha |
|---|---|---|
| `blue/50` | `#eff6ff` | 100% |
| `blue/100` | `#dbeafe` | 100% |
| `blue/200` | `#bfdbfe` | 100% |
| `blue/300` | `#93c5fd` | 100% |
| `blue/400` | `#60a5fa` | 100% |
| `blue/500` | `#3b82f6` | 100% |
| `blue/600` | `#2563eb` | 100% |
| `blue/700` | `#1d4ed8` | 100% |
| `blue/800` | `#1e40af` | 100% |
| `blue/900` | `#1e3a8a` | 100% |
| `blue/950` | `#172554` | 100% |

**indigo**

| Token | Hex | Alpha |
|---|---|---|
| `indigo/50` | `#eef2ff` | 100% |
| `indigo/100` | `#e0e7ff` | 100% |
| `indigo/200` | `#c7d2fe` | 100% |
| `indigo/300` | `#a5b4fc` | 100% |
| `indigo/400` | `#818cf8` | 100% |
| `indigo/500` | `#6366f1` | 100% |
| `indigo/600` | `#4f46e5` | 100% |
| `indigo/700` | `#4338ca` | 100% |
| `indigo/800` | `#3730a3` | 100% |
| `indigo/900` | `#312e81` | 100% |
| `indigo/950` | `#1e1b4b` | 100% |

**violet**

| Token | Hex | Alpha |
|---|---|---|
| `violet/50` | `#f5f3ff` | 100% |
| `violet/100` | `#ede9fe` | 100% |
| `violet/200` | `#ddd6fe` | 100% |
| `violet/300` | `#c4b5fd` | 100% |
| `violet/400` | `#a78bfa` | 100% |
| `violet/500` | `#8b5cf6` | 100% |
| `violet/600` | `#7c3aed` | 100% |
| `violet/700` | `#6d28d9` | 100% |
| `violet/800` | `#5b21b6` | 100% |
| `violet/900` | `#4c1d95` | 100% |
| `violet/950` | `#2e1065` | 100% |

**purple**

| Token | Hex | Alpha |
|---|---|---|
| `purple/50` | `#faf5ff` | 100% |
| `purple/100` | `#f3e8ff` | 100% |
| `purple/200` | `#e9d5ff` | 100% |
| `purple/300` | `#d8b4fe` | 100% |
| `purple/400` | `#c084fc` | 100% |
| `purple/500` | `#a855f7` | 100% |
| `purple/600` | `#9333ea` | 100% |
| `purple/700` | `#7e22ce` | 100% |
| `purple/800` | `#6b21a8` | 100% |
| `purple/900` | `#581c87` | 100% |
| `purple/950` | `#3b0764` | 100% |

**fuchsia**

| Token | Hex | Alpha |
|---|---|---|
| `fuchsia/50` | `#fdf4ff` | 100% |
| `fuchsia/100` | `#fae8ff` | 100% |
| `fuchsia/200` | `#f5d0fe` | 100% |
| `fuchsia/300` | `#f0abfc` | 100% |
| `fuchsia/400` | `#e879f9` | 100% |
| `fuchsia/500` | `#d946ef` | 100% |
| `fuchsia/600` | `#c026d3` | 100% |
| `fuchsia/700` | `#a21caf` | 100% |
| `fuchsia/800` | `#86198f` | 100% |
| `fuchsia/900` | `#701a75` | 100% |
| `fuchsia/950` | `#4a044e` | 100% |

**pink**

| Token | Hex | Alpha |
|---|---|---|
| `pink/50` | `#fdf2f8` | 100% |
| `pink/100` | `#fce7f3` | 100% |
| `pink/200` | `#fbcfe8` | 100% |
| `pink/300` | `#f9a8d4` | 100% |
| `pink/400` | `#f472b6` | 100% |
| `pink/500` | `#ec4899` | 100% |
| `pink/600` | `#db2777` | 100% |
| `pink/700` | `#be185d` | 100% |
| `pink/800` | `#9d174d` | 100% |
| `pink/900` | `#831843` | 100% |
| `pink/950` | `#500724` | 100% |

**rose**

| Token | Hex | Alpha |
|---|---|---|
| `rose/50` | `#fff1f2` | 100% |
| `rose/100` | `#ffe4e6` | 100% |
| `rose/200` | `#fecdd3` | 100% |
| `rose/300` | `#fda4af` | 100% |
| `rose/400` | `#fb7185` | 100% |
| `rose/500` | `#f43f5e` | 100% |
| `rose/600` | `#e11d48` | 100% |
| `rose/700` | `#be123c` | 100% |
| `rose/800` | `#9f1239` | 100% |
| `rose/900` | `#881337` | 100% |
| `rose/950` | `#4c0519` | 100% |

**white**

| Token | Hex | Alpha |
|---|---|---|
| `white` | `#ffffff` | 100% |

**black**

| Token | Hex | Alpha |
|---|---|---|
| `black` | `#000000` | 100% |

### A3  Radix Color Scale — rdx-colors (396 variables)

**gray**

| Token | Hex | Alpha |
|---|---|---|
| `gray/1` | `#fcfcfc` | 100% |
| `gray/2` | `#f9f9f9` | 100% |
| `gray/3` | `#f0f0f0` | 100% |
| `gray/4` | `#e8e8e8` | 100% |
| `gray/5` | `#e0e0e0` | 100% |
| `gray/6` | `#d9d9d9` | 100% |
| `gray/7` | `#cecece` | 100% |
| `gray/8` | `#bbbbbb` | 100% |
| `gray/9` | `#8d8d8d` | 100% |
| `gray/10` | `#838383` | 100% |
| `gray/11` | `#646464` | 100% |
| `gray/12` | `#202020` | 100% |

**mauve**

| Token | Hex | Alpha |
|---|---|---|
| `mauve/1` | `#fdfcfd` | 100% |
| `mauve/2` | `#faf9fb` | 100% |
| `mauve/3` | `#f2eff3` | 100% |
| `mauve/4` | `#eae7ec` | 100% |
| `mauve/5` | `#e3dfe6` | 100% |
| `mauve/6` | `#dbd8e0` | 100% |
| `mauve/7` | `#d0cdd7` | 100% |
| `mauve/8` | `#bcbac7` | 100% |
| `mauve/9` | `#8e8c99` | 100% |
| `mauve/10` | `#84828e` | 100% |
| `mauve/11` | `#65636d` | 100% |
| `mauve/12` | `#211f26` | 100% |

**slate**

| Token | Hex | Alpha |
|---|---|---|
| `slate/1` | `#fcfcfd` | 100% |
| `slate/2` | `#f9f9fb` | 100% |
| `slate/3` | `#f0f0f3` | 100% |
| `slate/4` | `#e8e8ec` | 100% |
| `slate/5` | `#e0e1e6` | 100% |
| `slate/6` | `#d9d9e0` | 100% |
| `slate/7` | `#cdced6` | 100% |
| `slate/8` | `#b9bbc6` | 100% |
| `slate/9` | `#8b8d98` | 100% |
| `slate/10` | `#80838d` | 100% |
| `slate/11` | `#60646c` | 100% |
| `slate/12` | `#1c2024` | 100% |

**sage**

| Token | Hex | Alpha |
|---|---|---|
| `sage/1` | `#fbfdfc` | 100% |
| `sage/2` | `#f7f9f8` | 100% |
| `sage/3` | `#eef1f0` | 100% |
| `sage/4` | `#e6e9e8` | 100% |
| `sage/5` | `#dfe2e0` | 100% |
| `sage/6` | `#d7dad9` | 100% |
| `sage/7` | `#cbcfcd` | 100% |
| `sage/8` | `#b8bcba` | 100% |
| `sage/9` | `#868e8b` | 100% |
| `sage/10` | `#7c8481` | 100% |
| `sage/11` | `#5f6563` | 100% |
| `sage/12` | `#1a211e` | 100% |

**olive**

| Token | Hex | Alpha |
|---|---|---|
| `olive/1` | `#fcfdfc` | 100% |
| `olive/2` | `#f8faf8` | 100% |
| `olive/3` | `#eff1ef` | 100% |
| `olive/4` | `#e7e9e7` | 100% |
| `olive/5` | `#dfe2df` | 100% |
| `olive/6` | `#d7dad7` | 100% |
| `olive/7` | `#cccfcc` | 100% |
| `olive/8` | `#b9bcb8` | 100% |
| `olive/9` | `#898e87` | 100% |
| `olive/10` | `#7f847d` | 100% |
| `olive/11` | `#60655f` | 100% |
| `olive/12` | `#1d211c` | 100% |

**sand**

| Token | Hex | Alpha |
|---|---|---|
| `sand/1` | `#fdfdfc` | 100% |
| `sand/2` | `#f9f9f8` | 100% |
| `sand/3` | `#f1f0ef` | 100% |
| `sand/4` | `#e9e8e6` | 100% |
| `sand/5` | `#e2e1de` | 100% |
| `sand/6` | `#dad9d6` | 100% |
| `sand/7` | `#cfceca` | 100% |
| `sand/8` | `#bcbbb5` | 100% |
| `sand/9` | `#8d8d86` | 100% |
| `sand/10` | `#82827c` | 100% |
| `sand/11` | `#63635e` | 100% |
| `sand/12` | `#21201c` | 100% |

**tomato**

| Token | Hex | Alpha |
|---|---|---|
| `tomato/1` | `#fffcfc` | 100% |
| `tomato/2` | `#fff8f7` | 100% |
| `tomato/3` | `#feebe7` | 100% |
| `tomato/4` | `#ffdcd3` | 100% |
| `tomato/5` | `#ffcdc2` | 100% |
| `tomato/6` | `#fdbdaf` | 100% |
| `tomato/7` | `#f5a898` | 100% |
| `tomato/8` | `#ec8e7b` | 100% |
| `tomato/9` | `#e54d2e` | 100% |
| `tomato/10` | `#dd4425` | 100% |
| `tomato/11` | `#d13415` | 100% |
| `tomato/12` | `#5c271f` | 100% |

**red**

| Token | Hex | Alpha |
|---|---|---|
| `red/1` | `#fffcfc` | 100% |
| `red/2` | `#fff7f7` | 100% |
| `red/3` | `#feebec` | 100% |
| `red/4` | `#ffdbdc` | 100% |
| `red/5` | `#ffcdce` | 100% |
| `red/6` | `#fdbdbe` | 100% |
| `red/7` | `#f4a9aa` | 100% |
| `red/8` | `#eb8e90` | 100% |
| `red/9` | `#e5484d` | 100% |
| `red/10` | `#dc3e42` | 100% |
| `red/11` | `#ce2c31` | 100% |
| `red/12` | `#641723` | 100% |

**ruby**

| Token | Hex | Alpha |
|---|---|---|
| `ruby/1` | `#fffcfd` | 100% |
| `ruby/2` | `#fff7f8` | 100% |
| `ruby/3` | `#feeaed` | 100% |
| `ruby/4` | `#ffdce1` | 100% |
| `ruby/5` | `#ffced6` | 100% |
| `ruby/6` | `#f8bfc8` | 100% |
| `ruby/7` | `#efacb8` | 100% |
| `ruby/8` | `#e592a3` | 100% |
| `ruby/9` | `#e54666` | 100% |
| `ruby/10` | `#dc3b5d` | 100% |
| `ruby/11` | `#ca244d` | 100% |
| `ruby/12` | `#64172b` | 100% |

**crimson**

| Token | Hex | Alpha |
|---|---|---|
| `crimson/1` | `#fffcfd` | 100% |
| `crimson/2` | `#fef7f9` | 100% |
| `crimson/3` | `#ffe9f0` | 100% |
| `crimson/4` | `#fedce7` | 100% |
| `crimson/5` | `#facedd` | 100% |
| `crimson/6` | `#f3bed1` | 100% |
| `crimson/7` | `#eaacc3` | 100% |
| `crimson/8` | `#e093b2` | 100% |
| `crimson/9` | `#e93d82` | 100% |
| `crimson/10` | `#df3478` | 100% |
| `crimson/11` | `#cb1d63` | 100% |
| `crimson/12` | `#621639` | 100% |

**pink**

| Token | Hex | Alpha |
|---|---|---|
| `pink/1` | `#fffcfe` | 100% |
| `pink/2` | `#fef7fb` | 100% |
| `pink/3` | `#fee9f5` | 100% |
| `pink/4` | `#fbdcef` | 100% |
| `pink/5` | `#f6cee7` | 100% |
| `pink/6` | `#efbfdd` | 100% |
| `pink/7` | `#e7acd0` | 100% |
| `pink/8` | `#dd93c2` | 100% |
| `pink/9` | `#d6409f` | 100% |
| `pink/10` | `#cf3897` | 100% |
| `pink/11` | `#c2298a` | 100% |
| `pink/12` | `#651249` | 100% |

**plum**

| Token | Hex | Alpha |
|---|---|---|
| `plum/1` | `#fefcff` | 100% |
| `plum/2` | `#fdf7fd` | 100% |
| `plum/3` | `#fbebfb` | 100% |
| `plum/4` | `#f7def8` | 100% |
| `plum/5` | `#f2d1f3` | 100% |
| `plum/6` | `#e9c2ec` | 100% |
| `plum/7` | `#deade3` | 100% |
| `plum/8` | `#cf91d8` | 100% |
| `plum/9` | `#ab4aba` | 100% |
| `plum/10` | `#a144af` | 100% |
| `plum/11` | `#953ea3` | 100% |
| `plum/12` | `#53195d` | 100% |

**purple**

| Token | Hex | Alpha |
|---|---|---|
| `purple/1` | `#fefcfe` | 100% |
| `purple/2` | `#fbf7fe` | 100% |
| `purple/3` | `#f7edfe` | 100% |
| `purple/4` | `#f2e2fc` | 100% |
| `purple/5` | `#ead5f9` | 100% |
| `purple/6` | `#e0c4f4` | 100% |
| `purple/7` | `#d1afec` | 100% |
| `purple/8` | `#be93e4` | 100% |
| `purple/9` | `#8e4ec6` | 100% |
| `purple/10` | `#8347b9` | 100% |
| `purple/11` | `#8145b5` | 100% |
| `purple/12` | `#402060` | 100% |

**violet**

| Token | Hex | Alpha |
|---|---|---|
| `violet/1` | `#fdfcfe` | 100% |
| `violet/2` | `#faf8ff` | 100% |
| `violet/3` | `#f4f0fe` | 100% |
| `violet/4` | `#ebe4ff` | 100% |
| `violet/5` | `#e1d9ff` | 100% |
| `violet/6` | `#d4cafe` | 100% |
| `violet/7` | `#c2b5f5` | 100% |
| `violet/8` | `#aa99ec` | 100% |
| `violet/9` | `#6e56cf` | 100% |
| `violet/10` | `#654dc4` | 100% |
| `violet/11` | `#6550b9` | 100% |
| `violet/12` | `#2f265f` | 100% |

**iris**

| Token | Hex | Alpha |
|---|---|---|
| `iris/1` | `#fdfdff` | 100% |
| `iris/2` | `#f8f8ff` | 100% |
| `iris/3` | `#f0f1fe` | 100% |
| `iris/4` | `#e6e7ff` | 100% |
| `iris/5` | `#dadcff` | 100% |
| `iris/6` | `#cbcdff` | 100% |
| `iris/7` | `#b8baf8` | 100% |
| `iris/8` | `#9b9ef0` | 100% |
| `iris/9` | `#5b5bd6` | 100% |
| `iris/10` | `#5151cd` | 100% |
| `iris/11` | `#5753c6` | 100% |
| `iris/12` | `#272962` | 100% |

**indigo**

| Token | Hex | Alpha |
|---|---|---|
| `indigo/1` | `#fdfdfe` | 100% |
| `indigo/2` | `#f7f9ff` | 100% |
| `indigo/3` | `#edf2fe` | 100% |
| `indigo/4` | `#e1e9ff` | 100% |
| `indigo/5` | `#d2deff` | 100% |
| `indigo/6` | `#c1d0ff` | 100% |
| `indigo/7` | `#abbdf9` | 100% |
| `indigo/8` | `#8da4ef` | 100% |
| `indigo/9` | `#3e63dd` | 100% |
| `indigo/10` | `#3358d4` | 100% |
| `indigo/11` | `#3a5bc7` | 100% |
| `indigo/12` | `#1f2d5c` | 100% |

**blue**

| Token | Hex | Alpha |
|---|---|---|
| `blue/1` | `#fbfdff` | 100% |
| `blue/2` | `#f4faff` | 100% |
| `blue/3` | `#e6f4fe` | 100% |
| `blue/4` | `#d5efff` | 100% |
| `blue/5` | `#c2e5ff` | 100% |
| `blue/6` | `#acd8fc` | 100% |
| `blue/7` | `#8ec8f6` | 100% |
| `blue/8` | `#5eb1ef` | 100% |
| `blue/9` | `#0090ff` | 100% |
| `blue/10` | `#0588f0` | 100% |
| `blue/11` | `#0d74ce` | 100% |
| `blue/12` | `#113264` | 100% |

**cyan**

| Token | Hex | Alpha |
|---|---|---|
| `cyan/1` | `#fafdfe` | 100% |
| `cyan/2` | `#f2fafb` | 100% |
| `cyan/3` | `#def7f9` | 100% |
| `cyan/4` | `#caf1f6` | 100% |
| `cyan/5` | `#b5e9f0` | 100% |
| `cyan/6` | `#9ddde7` | 100% |
| `cyan/7` | `#7dcedc` | 100% |
| `cyan/8` | `#3db9cf` | 100% |
| `cyan/9` | `#00a2c7` | 100% |
| `cyan/10` | `#0797b9` | 100% |
| `cyan/11` | `#107d98` | 100% |
| `cyan/12` | `#0d3c48` | 100% |

**teal**

| Token | Hex | Alpha |
|---|---|---|
| `teal/1` | `#fafefd` | 100% |
| `teal/2` | `#f3fbf9` | 100% |
| `teal/3` | `#e0f8f3` | 100% |
| `teal/4` | `#ccf3ea` | 100% |
| `teal/5` | `#b8eae0` | 100% |
| `teal/6` | `#a1ded2` | 100% |
| `teal/7` | `#83cdc1` | 100% |
| `teal/8` | `#53b9ab` | 100% |
| `teal/9` | `#12a594` | 100% |
| `teal/10` | `#0d9b8a` | 100% |
| `teal/11` | `#008573` | 100% |
| `teal/12` | `#0d3d38` | 100% |

**jade**

| Token | Hex | Alpha |
|---|---|---|
| `jade/1` | `#fbfefd` | 100% |
| `jade/2` | `#f4fbf7` | 100% |
| `jade/3` | `#e6f7ed` | 100% |
| `jade/4` | `#d6f1e3` | 100% |
| `jade/5` | `#c3e9d7` | 100% |
| `jade/6` | `#acdec8` | 100% |
| `jade/7` | `#8bceb6` | 100% |
| `jade/8` | `#56ba9f` | 100% |
| `jade/9` | `#29a383` | 100% |
| `jade/10` | `#26997b` | 100% |
| `jade/11` | `#208368` | 100% |
| `jade/12` | `#1d3b31` | 100% |

**green**

| Token | Hex | Alpha |
|---|---|---|
| `green/1` | `#fbfefc` | 100% |
| `green/2` | `#f4fbf6` | 100% |
| `green/3` | `#e6f6eb` | 100% |
| `green/4` | `#d6f1df` | 100% |
| `green/5` | `#c4e8d1` | 100% |
| `green/6` | `#adddc0` | 100% |
| `green/7` | `#8eceaa` | 100% |
| `green/8` | `#5bb98b` | 100% |
| `green/9` | `#30a46c` | 100% |
| `green/10` | `#2b9a66` | 100% |
| `green/11` | `#218358` | 100% |
| `green/12` | `#193b2d` | 100% |

**grass**

| Token | Hex | Alpha |
|---|---|---|
| `grass/1` | `#fbfefb` | 100% |
| `grass/2` | `#f5fbf5` | 100% |
| `grass/3` | `#e9f6e9` | 100% |
| `grass/4` | `#daf1db` | 100% |
| `grass/5` | `#c9e8ca` | 100% |
| `grass/6` | `#b2ddb5` | 100% |
| `grass/7` | `#94ce9a` | 100% |
| `grass/8` | `#65ba74` | 100% |
| `grass/9` | `#46a758` | 100% |
| `grass/10` | `#3e9b4f` | 100% |
| `grass/11` | `#2a7e3b` | 100% |
| `grass/12` | `#203c25` | 100% |

**bronze**

| Token | Hex | Alpha |
|---|---|---|
| `bronze/1` | `#fdfcfc` | 100% |
| `bronze/2` | `#fdf7f5` | 100% |
| `bronze/3` | `#f6edea` | 100% |
| `bronze/4` | `#efe4df` | 100% |
| `bronze/5` | `#e7d9d3` | 100% |
| `bronze/6` | `#dfcdc5` | 100% |
| `bronze/7` | `#d3bcb3` | 100% |
| `bronze/8` | `#c2a499` | 100% |
| `bronze/9` | `#a18072` | 100% |
| `bronze/10` | `#957468` | 100% |
| `bronze/11` | `#7d5e54` | 100% |
| `bronze/12` | `#43302b` | 100% |

**gold**

| Token | Hex | Alpha |
|---|---|---|
| `gold/1` | `#fdfdfc` | 100% |
| `gold/2` | `#faf9f2` | 100% |
| `gold/3` | `#f2f0e7` | 100% |
| `gold/4` | `#eae6db` | 100% |
| `gold/5` | `#e1dccf` | 100% |
| `gold/6` | `#d8d0bf` | 100% |
| `gold/7` | `#cbc0aa` | 100% |
| `gold/8` | `#b9a88d` | 100% |
| `gold/9` | `#978365` | 100% |
| `gold/10` | `#8c7a5e` | 100% |
| `gold/11` | `#71624b` | 100% |
| `gold/12` | `#3b352b` | 100% |

**brown**

| Token | Hex | Alpha |
|---|---|---|
| `brown/1` | `#fefdfc` | 100% |
| `brown/2` | `#fcf9f6` | 100% |
| `brown/3` | `#f6eee7` | 100% |
| `brown/4` | `#f0e4d9` | 100% |
| `brown/5` | `#ebdaca` | 100% |
| `brown/6` | `#e4cdb7` | 100% |
| `brown/7` | `#dcbc9f` | 100% |
| `brown/8` | `#cea37e` | 100% |
| `brown/9` | `#ad7f58` | 100% |
| `brown/10` | `#a07553` | 100% |
| `brown/11` | `#815e46` | 100% |
| `brown/12` | `#3e332e` | 100% |

**orange**

| Token | Hex | Alpha |
|---|---|---|
| `orange/1` | `#fefcfb` | 100% |
| `orange/2` | `#fff7ed` | 100% |
| `orange/3` | `#ffefd6` | 100% |
| `orange/4` | `#ffdfb5` | 100% |
| `orange/5` | `#ffd19a` | 100% |
| `orange/6` | `#ffc182` | 100% |
| `orange/7` | `#f5ae73` | 100% |
| `orange/8` | `#ec9455` | 100% |
| `orange/9` | `#f76b15` | 100% |
| `orange/10` | `#ef5f00` | 100% |
| `orange/11` | `#cc4e00` | 100% |
| `orange/12` | `#582d1d` | 100% |

**amber**

| Token | Hex | Alpha |
|---|---|---|
| `amber/1` | `#fefdfb` | 100% |
| `amber/2` | `#fefbe9` | 100% |
| `amber/3` | `#fff7c2` | 100% |
| `amber/4` | `#ffee9c` | 100% |
| `amber/5` | `#fbe577` | 100% |
| `amber/6` | `#f3d673` | 100% |
| `amber/7` | `#e9c162` | 100% |
| `amber/8` | `#e2a336` | 100% |
| `amber/9` | `#ffc53d` | 100% |
| `amber/10` | `#ffba18` | 100% |
| `amber/11` | `#ab6400` | 100% |
| `amber/12` | `#4f3422` | 100% |

**yellow**

| Token | Hex | Alpha |
|---|---|---|
| `yellow/1` | `#fdfdf9` | 100% |
| `yellow/2` | `#fefce9` | 100% |
| `yellow/3` | `#fffab8` | 100% |
| `yellow/4` | `#fff394` | 100% |
| `yellow/5` | `#ffe770` | 100% |
| `yellow/6` | `#f3d768` | 100% |
| `yellow/7` | `#e4c767` | 100% |
| `yellow/8` | `#d5ae39` | 100% |
| `yellow/9` | `#ffe629` | 100% |
| `yellow/10` | `#ffdc00` | 100% |
| `yellow/11` | `#9e6c00` | 100% |
| `yellow/12` | `#473b1f` | 100% |

**lime**

| Token | Hex | Alpha |
|---|---|---|
| `lime/1` | `#fcfdfa` | 100% |
| `lime/2` | `#f8faf3` | 100% |
| `lime/3` | `#eef6d6` | 100% |
| `lime/4` | `#e2f0bd` | 100% |
| `lime/5` | `#d3e7a6` | 100% |
| `lime/6` | `#c2da91` | 100% |
| `lime/7` | `#abc978` | 100% |
| `lime/8` | `#8db654` | 100% |
| `lime/9` | `#bdee63` | 100% |
| `lime/10` | `#b0e64c` | 100% |
| `lime/11` | `#5c7c2f` | 100% |
| `lime/12` | `#37401c` | 100% |

**mint**

| Token | Hex | Alpha |
|---|---|---|
| `mint/1` | `#f9fefd` | 100% |
| `mint/2` | `#f2fbf9` | 100% |
| `mint/3` | `#ddf9f2` | 100% |
| `mint/4` | `#c8f4e9` | 100% |
| `mint/5` | `#b3ecde` | 100% |
| `mint/6` | `#9ce0d0` | 100% |
| `mint/7` | `#7ecfbd` | 100% |
| `mint/8` | `#4cbba5` | 100% |
| `mint/9` | `#86ead4` | 100% |
| `mint/10` | `#7de0cb` | 100% |
| `mint/11` | `#027864` | 100% |
| `mint/12` | `#16433c` | 100% |

**sky**

| Token | Hex | Alpha |
|---|---|---|
| `sky/1` | `#f9feff` | 100% |
| `sky/2` | `#f1fafd` | 100% |
| `sky/3` | `#e1f6fd` | 100% |
| `sky/4` | `#d1f0fa` | 100% |
| `sky/5` | `#bee7f5` | 100% |
| `sky/6` | `#a9daed` | 100% |
| `sky/7` | `#8dcae3` | 100% |
| `sky/8` | `#60b3d7` | 100% |
| `sky/9` | `#7ce2fe` | 100% |
| `sky/10` | `#74daf8` | 100% |
| `sky/11` | `#00749e` | 100% |
| `sky/12` | `#1d3e56` | 100% |

**black**

| Token | Hex | Alpha |
|---|---|---|
| `black/1` | `#000000` | 5% |
| `black/2` | `#000000` | 10% |
| `black/3` | `#000000` | 15% |
| `black/4` | `#000000` | 20% |
| `black/5` | `#000000` | 30% |
| `black/6` | `#000000` | 40% |
| `black/7` | `#000000` | 50% |
| `black/8` | `#000000` | 60% |
| `black/9` | `#000000` | 70% |
| `black/10` | `#000000` | 80% |
| `black/11` | `#000000` | 90% |
| `black/12` | `#000000` | 95% |

**white**

| Token | Hex | Alpha |
|---|---|---|
| `white/1` | `#ffffff` | 5% |
| `white/2` | `#ffffff` | 10% |
| `white/3` | `#ffffff` | 15% |
| `white/4` | `#ffffff` | 20% |
| `white/5` | `#ffffff` | 30% |
| `white/6` | `#ffffff` | 40% |
| `white/7` | `#ffffff` | 50% |
| `white/8` | `#ffffff` | 60% |
| `white/9` | `#ffffff` | 70% |
| `white/10` | `#ffffff` | 80% |
| `white/11` | `#ffffff` | 90% |
| `white/12` | `#ffffff` | 95% |

### A4  Typography — font (45 variables)

**font/family** (2 variables)

| Token | Value |
|---|---|
| `family/sans` | `Google sans` |
| `family/mono` | `Geist Mono` |

**font/size** (13 variables)

| Token | Value |
|---|---|
| `size/xs` | `12` |
| `size/sm` | `14` |
| `size/base` | `16` |
| `size/lg` | `18` |
| `size/xl` | `20` |
| `size/2xl` | `24` |
| `size/3xl` | `30` |
| `size/4xl` | `36` |
| `size/5xl` | `48` |
| `size/6xl` | `60` |
| `size/7xl` | `72` |
| `size/8xl` | `96` |
| `size/9xl` | `128` |

**font/style** (2 variables)

| Token | Value |
|---|---|
| `style/italic` | `italic` |
| `style/not-italic` | `normal` |

**font/weight** (9 variables)

| Token | Value |
|---|---|
| `weight/thin` | `100` |
| `weight/extralight` | `200` |
| `weight/light` | `300` |
| `weight/normal` | `400` |
| `weight/medium` | `500` |
| `weight/semibold` | `600` |
| `weight/bold` | `700` |
| `weight/extrabold` | `800` |
| `weight/black` | `900` |

**font/leading** (13 variables)

| Token | Value |
|---|---|
| `leading/3` | `12` |
| `leading/4` | `16` |
| `leading/5` | `20` |
| `leading/6` | `24` |
| `leading/7` | `28` |
| `leading/8` | `32` |
| `leading/9` | `36` |
| `leading/10` | `40` |
| `leading/12` | `48` |
| `leading/15` | `60` |
| `leading/18` | `72` |
| `leading/24` | `96` |
| `leading/32` | `128` |

**font/tracking** (6 variables)

| Token | Value |
|---|---|
| `tracking/tighter` | `-0.800000011920929` |
| `tracking/tight` | `-0.4000000059604645` |
| `tracking/normal` | `0` |
| `tracking/wide` | `0.4000000059604645` |
| `tracking/wider` | `0.800000011920929` |
| `tracking/widest` | `1.600000023841858` |

### A5  Base Token Scale — tokens (87 variables)

| Token | Value (px) |
|---|---|
| `-0,8` | `-0.800000011920929` |
| `-0,4` | `-0.4000000059604645` |
| `0` | `0` |
| `0,4` | `0.4000000059604645` |
| `0,5` | `0.5` |
| `0,75` | `0.75` |
| `0,8` | `0.800000011920929` |
| `1` | `1` |
| `1,25` | `1.25` |
| `1,5` | `1.5` |
| `1,6` | `1.600000023841858` |
| `1,75` | `1.75` |
| `2` | `2` |
| `2,25` | `2.25` |
| `2,5` | `2.5` |
| `2,75` | `2.75` |
| `3` | `3` |
| `4` | `4` |
| `5` | `5` |
| `6` | `6` |
| `8` | `8` |
| `10` | `10` |
| `12` | `12` |
| `14` | `14` |
| `15` | `15` |
| `16` | `16` |
| `18` | `18` |
| `20` | `20` |
| `24` | `24` |
| `25` | `25` |
| `28` | `28` |
| `30` | `30` |
| `32` | `32` |
| `35` | `35` |
| `36` | `36` |
| `40` | `40` |
| `44` | `44` |
| `45` | `45` |
| `48` | `48` |
| `50` | `50` |
| `55` | `55` |
| `56` | `56` |
| `60` | `60` |
| `64` | `64` |
| `65` | `65` |
| `70` | `70` |
| `72` | `72` |
| `75` | `75` |
| `80` | `80` |
| `85` | `85` |
| `90` | `90` |
| `95` | `95` |
| `96` | `96` |
| `100` | `100` |
| `112` | `112` |
| `128` | `128` |
| `144` | `144` |
| `160` | `160` |
| `176` | `176` |
| `192` | `192` |
| `200` | `200` |
| `208` | `208` |
| `224` | `224` |
| `240` | `240` |
| `256` | `256` |
| `288` | `288` |
| `300` | `300` |
| `320` | `320` |
| `384` | `384` |
| `400` | `400` |
| `448` | `448` |
| `500` | `500` |
| `512` | `512` |
| `576` | `576` |
| `600` | `600` |
| `640` | `640` |
| `672` | `672` |
| `700` | `700` |
| `768` | `768` |
| `800` | `800` |
| `896` | `896` |
| `900` | `900` |
| `1024` | `1024` |
| `1152` | `1152` |
| `1280` | `1280` |
| `1536` | `1536` |
| `9999` | `9999` |

### A6  Space Utilities — space (68 variables)

| Token | Value (px) |
|---|---|
| `space-x-0` | `0` |
| `space-y-0` | `0` |
| `space-x-0,5` | `2` |
| `space-y-0,5` | `2` |
| `space-x-1` | `4` |
| `space-y-1` | `4` |
| `space-x-1,5` | `6` |
| `space-y-1,5` | `6` |
| `space-x-2` | `8` |
| `space-y-2` | `8` |
| `space-x-2,5` | `10` |
| `space-y-2,5` | `10` |
| `space-x-3` | `12` |
| `space-y-3` | `12` |
| `space-x-3,5` | `14` |
| `space-y-3,5` | `14` |
| `space-x-4` | `16` |
| `space-y-4` | `16` |
| `space-x-5` | `20` |
| `space-y-5` | `20` |
| `space-x-6` | `24` |
| `space-y-6` | `24` |
| `space-x-7` | `28` |
| `space-y-7` | `28` |
| `space-x-8` | `32` |
| `space-y-8` | `32` |
| `space-x-9` | `36` |
| `space-y-9` | `36` |
| `space-x-10` | `40` |
| `space-y-10` | `40` |
| `space-x-11` | `44` |
| `space-y-11` | `44` |
| `space-x-12` | `48` |
| `space-y-12` | `48` |
| `space-x-14` | `56` |
| `space-y-14` | `56` |
| `space-x-16` | `64` |
| `space-y-16` | `64` |
| `space-x-20` | `80` |
| `space-y-20` | `80` |
| `space-x-24` | `96` |
| `space-y-24` | `96` |
| `space-x-28` | `112` |
| `space-y-28` | `112` |
| `space-x-32` | `128` |
| `space-y-32` | `128` |
| `space-x-36` | `144` |
| `space-y-36` | `144` |
| `space-x-40` | `160` |
| `space-y-40` | `160` |
| `space-x-44` | `176` |
| `space-y-44` | `176` |
| `space-x-48` | `192` |
| `space-y-48` | `192` |
| `space-x-52` | `208` |
| `space-y-52` | `208` |
| `space-x-56` | `224` |
| `space-y-56` | `224` |
| `space-x-60` | `240` |
| `space-y-60` | `240` |
| `space-x-64` | `256` |
| `space-y-64` | `256` |
| `space-x-72` | `288` |
| `space-y-72` | `288` |
| `space-x-80` | `320` |
| `space-y-80` | `320` |
| `space-x-96` | `384` |
| `space-y-96` | `384` |

### A7  Gap Utilities — gap (102 variables)

| Token | Value (px) |
|---|---|
| `gap-0` | `0` |
| `gap-x-0` | `0` |
| `gap-y-0` | `0` |
| `gap-0,5` | `2` |
| `gap-x-0,5` | `2` |
| `gap-y-0,5` | `2` |
| `gap-1` | `4` |
| `gap-x-1` | `4` |
| `gap-y-1` | `4` |
| `gap-1,5` | `6` |
| `gap-x-1,5` | `6` |
| `gap-y-1,5` | `6` |
| `gap-2` | `8` |
| `gap-x-2` | `8` |
| `gap-y-2` | `8` |
| `gap-2,5` | `10` |
| `gap-x-2,5` | `10` |
| `gap-y-2,5` | `10` |
| `gap-3` | `12` |
| `gap-x-3` | `12` |
| `gap-y-3` | `12` |
| `gap-3,5` | `14` |
| `gap-x-3,5` | `14` |
| `gap-y-3,5` | `14` |
| `gap-4` | `16` |
| `gap-x-4` | `16` |
| `gap-y-4` | `16` |
| `gap-5` | `20` |
| `gap-x-5` | `20` |
| `gap-y-5` | `20` |
| `gap-6` | `24` |
| `gap-x-6` | `24` |
| `gap-y-6` | `24` |
| `gap-7` | `28` |
| `gap-x-7` | `28` |
| `gap-y-7` | `28` |
| `gap-8` | `32` |
| `gap-x-8` | `32` |
| `gap-y-8` | `32` |
| `gap-9` | `36` |
| `gap-x-9` | `36` |
| `gap-y-9` | `36` |
| `gap-10` | `40` |
| `gap-x-10` | `40` |
| `gap-y-10` | `40` |
| `gap-11` | `44` |
| `gap-x-11` | `44` |
| `gap-y-11` | `44` |
| `gap-12` | `48` |
| `gap-x-12` | `48` |
| `gap-y-12` | `48` |
| `gap-14` | `56` |
| `gap-x-14` | `56` |
| `gap-y-14` | `56` |
| `gap-16` | `64` |
| `gap-x-16` | `64` |
| `gap-y-16` | `64` |
| `gap-20` | `80` |
| `gap-x-20` | `80` |
| `gap-y-20` | `80` |
| `gap-24` | `96` |
| `gap-x-24` | `96` |
| `gap-y-24` | `96` |
| `gap-28` | `112` |
| `gap-x-28` | `112` |
| `gap-y-28` | `112` |
| `gap-32` | `128` |
| `gap-x-32` | `128` |
| `gap-y-32` | `128` |
| `gap-36` | `144` |
| `gap-x-36` | `144` |
| `gap-y-36` | `144` |
| `gap-40` | `160` |
| `gap-x-40` | `160` |
| `gap-y-40` | `160` |
| `gap-44` | `176` |
| `gap-x-44` | `176` |
| `gap-y-44` | `176` |
| `gap-48` | `192` |
| `gap-x-48` | `192` |
| `gap-y-48` | `192` |
| `gap-52` | `208` |
| `gap-x-52` | `208` |
| `gap-y-52` | `208` |
| `gap-56` | `224` |
| `gap-x-56` | `224` |
| `gap-y-56` | `224` |
| `gap-60` | `240` |
| `gap-x-60` | `240` |
| `gap-y-60` | `240` |
| `gap-64` | `256` |
| `gap-x-64` | `256` |
| `gap-y-64` | `256` |
| `gap-72` | `288` |
| `gap-x-72` | `288` |
| `gap-y-72` | `288` |
| `gap-80` | `320` |
| `gap-x-80` | `320` |
| `gap-y-80` | `320` |
| `gap-96` | `384` |
| `gap-x-96` | `384` |
| `gap-y-96` | `384` |

### A8  Margin Utilities — margin (245 variables)

| Token | Value (px) |
|---|---|
| `m-0` | `0` |
| `mx-0` | `0` |
| `my-0` | `0` |
| `mr-0` | `0` |
| `ml-0` | `0` |
| `mt-0` | `0` |
| `mb-0` | `0` |
| `m-px` | `1` |
| `mx-px` | `1` |
| `my-px` | `1` |
| `mr-px` | `1` |
| `ml-px` | `1` |
| `mt-px` | `1` |
| `mb-px` | `1` |
| `m-0,5` | `2` |
| `mx-0,5` | `2` |
| `my-0,5` | `2` |
| `mr-0,5` | `2` |
| `ml-0,5` | `2` |
| `mt-0,5` | `2` |
| `mb-0,5` | `2` |
| `m-1` | `4` |
| `mx-1` | `4` |
| `my-1` | `4` |
| `mr-1` | `4` |
| `ml-1` | `4` |
| `mt-1` | `4` |
| `mb-1` | `4` |
| `m-1,5` | `6` |
| `mx-1,5` | `6` |
| `my-1,5` | `6` |
| `mr-1,5` | `6` |
| `ml-1,5` | `6` |
| `mt-1,5` | `6` |
| `mb-1,5` | `6` |
| `m-2` | `8` |
| `mx-2` | `8` |
| `my-2` | `8` |
| `mr-2` | `8` |
| `ml-2` | `8` |
| `mt-2` | `8` |
| `mb-2` | `8` |
| `m-2,5` | `10` |
| `mx-2,5` | `10` |
| `my-2,5` | `10` |
| `mr-2,5` | `10` |
| `ml-2,5` | `10` |
| `mt-2,5` | `10` |
| `mb-2,5` | `10` |
| `m-3` | `12` |
| `mx-3` | `12` |
| `my-3` | `12` |
| `mr-3` | `12` |
| `ml-3` | `12` |
| `mt-3` | `12` |
| `mb-3` | `12` |
| `m-3,5` | `14` |
| `mx-3,5` | `14` |
| `my-3,5` | `14` |
| `mr-3,5` | `14` |
| `ml-3,5` | `14` |
| `mt-3,5` | `14` |
| `mb-3,5` | `14` |
| `m-4` | `16` |
| `mx-4` | `16` |
| `my-4` | `16` |
| `mr-4` | `16` |
| `ml-4` | `16` |
| `mt-4` | `16` |
| `mb-4` | `16` |
| `m-5` | `20` |
| `mx-5` | `20` |
| `my-5` | `20` |
| `mr-5` | `20` |
| `ml-5` | `20` |
| `mt-5` | `20` |
| `mb-5` | `20` |
| `m-6` | `24` |
| `mx-6` | `24` |
| `my-6` | `24` |
| `mr-6` | `24` |
| `ml-6` | `24` |
| `mt-6` | `24` |
| `mb-6` | `24` |
| `m-7` | `28` |
| `mx-7` | `28` |
| `my-7` | `28` |
| `mr-7` | `28` |
| `ml-7` | `28` |
| `mt-7` | `28` |
| `mb-7` | `28` |
| `m-8` | `32` |
| `mx-8` | `32` |
| `my-8` | `32` |
| `mr-8` | `32` |
| `ml-8` | `32` |
| `mt-8` | `32` |
| `mb-8` | `32` |
| `m-9` | `36` |
| `mx-9` | `36` |
| `my-9` | `36` |
| `mr-9` | `36` |
| `ml-9` | `36` |
| `mt-9` | `36` |
| `mb-9` | `36` |
| `m-10` | `40` |
| `mx-10` | `40` |
| `my-10` | `40` |
| `mr-10` | `40` |
| `ml-10` | `40` |
| `mt-10` | `40` |
| `mb-10` | `40` |
| `m-11` | `44` |
| `mx-11` | `44` |
| `my-11` | `44` |
| `mr-11` | `44` |
| `ml-11` | `44` |
| `mt-11` | `44` |
| `mb-11` | `44` |
| `m-12` | `48` |
| `mx-12` | `48` |
| `my-12` | `48` |
| `mr-12` | `48` |
| `ml-12` | `48` |
| `mt-12` | `48` |
| `mb-12` | `48` |
| `m-14` | `56` |
| `mx-14` | `56` |
| `my-14` | `56` |
| `mr-14` | `56` |
| `ml-14` | `56` |
| `mt-14` | `56` |
| `mb-14` | `56` |
| `m-16` | `64` |
| `mx-16` | `64` |
| `my-16` | `64` |
| `mr-16` | `64` |
| `ml-16` | `64` |
| `mt-16` | `64` |
| `mb-16` | `64` |
| `m-20` | `80` |
| `mx-20` | `80` |
| `my-20` | `80` |
| `mr-20` | `80` |
| `ml-20` | `80` |
| `mt-20` | `80` |
| `mb-20` | `80` |
| `m-24` | `96` |
| `mx-24` | `96` |
| `my-24` | `96` |
| `mr-24` | `96` |
| `ml-24` | `96` |
| `mt-24` | `96` |
| `mb-24` | `96` |
| `m-28` | `112` |
| `mx-28` | `112` |
| `my-28` | `112` |
| `mr-28` | `112` |
| `ml-28` | `112` |
| `mt-28` | `112` |
| `mb-28` | `112` |
| `m-32` | `128` |
| `mx-32` | `128` |
| `my-32` | `128` |
| `mr-32` | `128` |
| `ml-32` | `128` |
| `mt-32` | `128` |
| `mb-32` | `128` |
| `m-36` | `144` |
| `mx-36` | `144` |
| `my-36` | `144` |
| `mr-36` | `144` |
| `ml-36` | `144` |
| `mt-36` | `144` |
| `mb-36` | `144` |
| `m-40` | `160` |
| `mx-40` | `160` |
| `my-40` | `160` |
| `mr-40` | `160` |
| `ml-40` | `160` |
| `mt-40` | `160` |
| `mb-40` | `160` |
| `m-44` | `176` |
| `mx-44` | `176` |
| `my-44` | `176` |
| `mr-44` | `176` |
| `ml-44` | `176` |
| `mt-44` | `176` |
| `mb-44` | `176` |
| `m-48` | `192` |
| `mx-48` | `192` |
| `my-48` | `192` |
| `mr-48` | `192` |
| `ml-48` | `192` |
| `mt-48` | `192` |
| `mb-48` | `192` |
| `m-52` | `208` |
| `mx-52` | `208` |
| `my-52` | `208` |
| `mr-52` | `208` |
| `ml-52` | `208` |
| `mt-52` | `208` |
| `mb-52` | `208` |
| `m-56` | `224` |
| `mx-56` | `224` |
| `my-56` | `224` |
| `mr-56` | `224` |
| `ml-56` | `224` |
| `mt-56` | `224` |
| `mb-56` | `224` |
| `m-60` | `240` |
| `mx-60` | `240` |
| `my-60` | `240` |
| `mr-60` | `240` |
| `ml-60` | `240` |
| `mt-60` | `240` |
| `mb-60` | `240` |
| `m-64` | `256` |
| `mx-64` | `256` |
| `my-64` | `256` |
| `mr-64` | `256` |
| `ml-64` | `256` |
| `mt-64` | `256` |
| `mb-64` | `256` |
| `m-72` | `288` |
| `mx-72` | `288` |
| `my-72` | `288` |
| `mr-72` | `288` |
| `ml-72` | `288` |
| `mt-72` | `288` |
| `mb-72` | `288` |
| `m-80` | `320` |
| `mx-80` | `320` |
| `my-80` | `320` |
| `mr-80` | `320` |
| `ml-80` | `320` |
| `mt-80` | `320` |
| `mb-80` | `320` |
| `m-96` | `384` |
| `mx-96` | `384` |
| `my-96` | `384` |
| `mr-96` | `384` |
| `ml-96` | `384` |
| `mt-96` | `384` |
| `mb-96` | `384` |

### A9  Padding Utilities — padding (245 variables)

| Token | Value (px) |
|---|---|
| `p-0` | `0` |
| `px-0` | `0` |
| `py-0` | `0` |
| `pr-0` | `0` |
| `pl-0` | `0` |
| `pt-0` | `0` |
| `pb-0` | `0` |
| `p-px` | `1` |
| `px-px` | `1` |
| `py-px` | `1` |
| `pr-px` | `1` |
| `pl-px` | `1` |
| `pt-px` | `1` |
| `pb-px` | `1` |
| `p-0,5` | `2` |
| `px-0,5` | `2` |
| `py-0,5` | `2` |
| `pr-0,5` | `2` |
| `pl-0,5` | `2` |
| `pt-0,5` | `2` |
| `pb-0,5` | `2` |
| `p-1` | `4` |
| `px-1` | `4` |
| `py-1` | `4` |
| `pr-1` | `4` |
| `pl-1` | `4` |
| `pt-1` | `4` |
| `pb-1` | `4` |
| `p-1,5` | `6` |
| `px-1,5` | `6` |
| `py-1,5` | `6` |
| `pr-1,5` | `6` |
| `pl-1,5` | `6` |
| `pt-1,5` | `6` |
| `pb-1,5` | `6` |
| `p-2` | `8` |
| `px-2` | `8` |
| `py-2` | `8` |
| `pr-2` | `8` |
| `pl-2` | `8` |
| `pt-2` | `8` |
| `pb-2` | `8` |
| `p-2,5` | `10` |
| `px-2,5` | `10` |
| `py-2,5` | `10` |
| `pr-2,5` | `10` |
| `pl-2,5` | `10` |
| `pt-2,5` | `10` |
| `pb-2,5` | `10` |
| `p-3` | `12` |
| `px-3` | `12` |
| `py-3` | `12` |
| `pr-3` | `12` |
| `pl-3` | `12` |
| `pt-3` | `12` |
| `pb-3` | `12` |
| `p-3,5` | `14` |
| `px-3,5` | `14` |
| `py-3,5` | `14` |
| `pr-3,5` | `14` |
| `pl-3,5` | `14` |
| `pt-3,5` | `14` |
| `pb-3,5` | `14` |
| `p-4` | `16` |
| `px-4` | `16` |
| `py-4` | `16` |
| `pr-4` | `16` |
| `pl-4` | `16` |
| `pt-4` | `16` |
| `pb-4` | `16` |
| `p-5` | `20` |
| `px-5` | `20` |
| `py-5` | `20` |
| `pr-5` | `20` |
| `pl-5` | `20` |
| `pt-5` | `20` |
| `pb-5` | `20` |
| `p-6` | `24` |
| `px-6` | `24` |
| `py-6` | `24` |
| `pr-6` | `24` |
| `pl-6` | `24` |
| `pt-6` | `24` |
| `pb-6` | `24` |
| `p-7` | `28` |
| `px-7` | `28` |
| `py-7` | `28` |
| `pr-7` | `28` |
| `pl-7` | `28` |
| `pt-7` | `28` |
| `pb-7` | `28` |
| `p-8` | `32` |
| `px-8` | `32` |
| `py-8` | `32` |
| `pr-8` | `32` |
| `pl-8` | `32` |
| `pt-8` | `32` |
| `pb-8` | `32` |
| `p-9` | `36` |
| `px-9` | `36` |
| `py-9` | `36` |
| `pr-9` | `36` |
| `pl-9` | `36` |
| `pt-9` | `36` |
| `pb-9` | `36` |
| `p-10` | `40` |
| `px-10` | `40` |
| `py-10` | `40` |
| `pr-10` | `40` |
| `pl-10` | `40` |
| `pt-10` | `40` |
| `pb-10` | `40` |
| `p-11` | `44` |
| `px-11` | `44` |
| `py-11` | `44` |
| `pr-11` | `44` |
| `pl-11` | `44` |
| `pt-11` | `44` |
| `pb-11` | `44` |
| `p-12` | `48` |
| `px-12` | `48` |
| `py-12` | `48` |
| `pr-12` | `48` |
| `pl-12` | `48` |
| `pt-12` | `48` |
| `pb-12` | `48` |
| `p-14` | `56` |
| `px-14` | `56` |
| `py-14` | `56` |
| `pr-14` | `56` |
| `pl-14` | `56` |
| `pt-14` | `56` |
| `pb-14` | `56` |
| `p-16` | `64` |
| `px-16` | `64` |
| `py-16` | `64` |
| `pr-16` | `64` |
| `pl-16` | `64` |
| `pt-16` | `64` |
| `pb-16` | `64` |
| `p-20` | `80` |
| `px-20` | `80` |
| `py-20` | `80` |
| `pr-20` | `80` |
| `pl-20` | `80` |
| `pt-20` | `80` |
| `pb-20` | `80` |
| `p-24` | `96` |
| `px-24` | `96` |
| `py-24` | `96` |
| `pr-24` | `96` |
| `pl-24` | `96` |
| `pt-24` | `96` |
| `pb-24` | `96` |
| `p-28` | `112` |
| `px-28` | `112` |
| `py-28` | `112` |
| `pr-28` | `112` |
| `pl-28` | `112` |
| `pt-28` | `112` |
| `pb-28` | `112` |
| `p-32` | `128` |
| `px-32` | `128` |
| `py-32` | `128` |
| `pr-32` | `128` |
| `pl-32` | `128` |
| `pt-32` | `128` |
| `pb-32` | `128` |
| `p-36` | `144` |
| `px-36` | `144` |
| `py-36` | `144` |
| `pr-36` | `144` |
| `pl-36` | `144` |
| `pt-36` | `144` |
| `pb-36` | `144` |
| `p-40` | `160` |
| `px-40` | `160` |
| `py-40` | `160` |
| `pr-40` | `160` |
| `pl-40` | `160` |
| `pt-40` | `160` |
| `pb-40` | `160` |
| `p-44` | `176` |
| `px-44` | `176` |
| `py-44` | `176` |
| `pr-44` | `176` |
| `pl-44` | `176` |
| `pt-44` | `176` |
| `pb-44` | `176` |
| `p-48` | `192` |
| `px-48` | `192` |
| `py-48` | `192` |
| `pr-48` | `192` |
| `pl-48` | `192` |
| `pt-48` | `192` |
| `pb-48` | `192` |
| `p-52` | `208` |
| `px-52` | `208` |
| `py-52` | `208` |
| `pr-52` | `208` |
| `pl-52` | `208` |
| `pt-52` | `208` |
| `pb-52` | `208` |
| `p-56` | `224` |
| `px-56` | `224` |
| `py-56` | `224` |
| `pr-56` | `224` |
| `pl-56` | `224` |
| `pt-56` | `224` |
| `pb-56` | `224` |
| `p-60` | `240` |
| `px-60` | `240` |
| `py-60` | `240` |
| `pr-60` | `240` |
| `pl-60` | `240` |
| `pt-60` | `240` |
| `pb-60` | `240` |
| `p-64` | `256` |
| `px-64` | `256` |
| `py-64` | `256` |
| `pr-64` | `256` |
| `pl-64` | `256` |
| `pt-64` | `256` |
| `pb-64` | `256` |
| `p-72` | `288` |
| `px-72` | `288` |
| `py-72` | `288` |
| `pr-72` | `288` |
| `pl-72` | `288` |
| `pt-72` | `288` |
| `pb-72` | `288` |
| `p-80` | `320` |
| `px-80` | `320` |
| `py-80` | `320` |
| `pr-80` | `320` |
| `pl-80` | `320` |
| `pt-80` | `320` |
| `pb-80` | `320` |
| `p-96` | `384` |
| `px-96` | `384` |
| `py-96` | `384` |
| `pr-96` | `384` |
| `pl-96` | `384` |
| `pt-96` | `384` |
| `pb-96` | `384` |

### A10  Height Utilities — height (24 variables)

| Token | Value (px) |
|---|---|
| `h-0` | `0` |
| `h-px` | `1` |
| `h-0,5` | `2` |
| `h-1` | `4` |
| `h-2` | `8` |
| `h-2,5` | `10` |
| `h-3` | `12` |
| `h-3,5` | `14` |
| `h-4` | `16` |
| `h-5` | `20` |
| `h-6` | `24` |
| `h-7` | `28` |
| `h-8` | `32` |
| `h-9` | `36` |
| `h-10` | `40` |
| `h-12` | `48` |
| `h-14` | `56` |
| `h-16` | `64` |
| `h-18` | `72` |
| `h-20` | `80` |
| `h-24` | `96` |
| `h-48` | `192` |
| `h-72` | `288` |
| `h-96` | `384` |

### A11  Max Height Utilities — max-height (35 variables)

| Token | Value (px) |
|---|---|
| `max-h-0` | `0` |
| `max-h-px` | `1` |
| `max-h-0,5` | `2` |
| `max-h-1` | `4` |
| `max-h-1,5` | `6` |
| `max-h-2` | `8` |
| `max-h-2,5` | `10` |
| `max-h-3` | `12` |
| `max-h-3,5` | `14` |
| `max-h-4` | `16` |
| `max-h-5` | `20` |
| `max-h-6` | `24` |
| `max-h-7` | `28` |
| `max-h-8` | `32` |
| `max-h-9` | `36` |
| `max-h-10` | `40` |
| `max-h-11` | `44` |
| `max-h-12` | `48` |
| `max-h-14` | `56` |
| `max-h-16` | `64` |
| `max-h-20` | `80` |
| `max-h-24` | `96` |
| `max-h-28` | `112` |
| `max-h-32` | `128` |
| `max-h-36` | `144` |
| `max-h-40` | `160` |
| `max-h-44` | `176` |
| `max-h-48` | `192` |
| `max-h-52` | `208` |
| `max-h-56` | `224` |
| `max-h-60` | `240` |
| `max-h-64` | `256` |
| `max-h-72` | `288` |
| `max-h-80` | `320` |
| `max-h-96` | `384` |

### A12  Max Width Utilities — max-width (51 variables)

| Token | Value (px) |
|---|---|
| `max-w-0` | `0` |
| `max-w-px` | `1` |
| `max-w-0,5` | `2` |
| `max-w-1` | `4` |
| `max-w-1,5` | `6` |
| `max-w-2` | `8` |
| `max-w-2,5` | `10` |
| `max-w-3` | `12` |
| `max-w-4` | `16` |
| `max-w-5` | `20` |
| `max-w-6` | `24` |
| `max-w-7` | `28` |
| `max-w-8` | `32` |
| `max-w-9` | `36` |
| `max-w-10` | `40` |
| `max-w-11` | `44` |
| `max-w-12` | `48` |
| `max-w-14` | `56` |
| `max-w-16` | `64` |
| `max-w-20` | `80` |
| `max-w-24` | `96` |
| `max-w-28` | `112` |
| `max-w-32` | `128` |
| `max-w-36` | `144` |
| `max-w-40` | `160` |
| `max-w-44` | `176` |
| `max-w-48` | `192` |
| `max-w-52` | `208` |
| `max-w-56` | `224` |
| `max-w-60` | `240` |
| `max-w-64` | `256` |
| `max-w-72` | `288` |
| `max-w-80` | `320` |
| `max-w-96` | `384` |
| `max-w-xs` | `320` |
| `max-w-sm` | `384` |
| `max-w-md` | `448` |
| `max-w-lg` | `512` |
| `max-w-xl` | `576` |
| `max-w-2xl` | `672` |
| `max-w-3xl` | `768` |
| `max-w-4xl` | `896` |
| `max-w-5xl` | `1024` |
| `max-w-6xl` | `1152` |
| `max-w-7xl` | `1280` |
| `max-w-none` | `0` |
| `max-w-screen-sm` | `640` |
| `max-w-screen-md` | `768` |
| `max-w-screen-lg` | `1024` |
| `max-w-screen-xl` | `1280` |
| `max-w-screen-2xl` | `1536` |

### A13  Border Radius — border-radius (150 variables)

| Token | Value (px) | Alias |
|---|---|---|
| `rounded-xs` | `2` | 2 |
| `rounded-sm` | `4` | 4 |
| `rounded-md` | `6` | 6 |
| `rounded-lg` | `8` | 8 |
| `rounded-xl` | `12` | 12 |
| `rounded-2xl` | `16` | 16 |
| `rounded-3xl` | `24` | 24 |
| `rounded-4xl` | `32` | 32 |
| `rounded-none` | `0` | 0 |
| `rounded-full` | `9999` | 9999 |
| `rounded-s-xs` | `2` | 2 |
| `rounded-s-sm` | `4` | 4 |
| `rounded-s-md` | `6` | 6 |
| `rounded-s-lg` | `8` | 8 |
| `rounded-s-xl` | `12` | 12 |
| `rounded-s-2xl` | `16` | 16 |
| `rounded-s-3xl` | `24` | 24 |
| `rounded-s-4xl` | `32` | 32 |
| `rounded-s-none` | `0` | 0 |
| `rounded-s-full` | `9999` | 9999 |
| `rounded-e-xs` | `2` | 2 |
| `rounded-e-sm` | `4` | 4 |
| `rounded-e-md` | `6` | 6 |
| `rounded-e-lg` | `8` | 8 |
| `rounded-e-xl` | `12` | 12 |
| `rounded-e-2xl` | `16` | 16 |
| `rounded-e-3xl` | `24` | 24 |
| `rounded-e-4xl` | `32` | 32 |
| `rounded-e-none` | `0` | 0 |
| `rounded-e-full` | `9999` | 9999 |
| `rounded-t-xs` | `2` | 2 |
| `rounded-t-sm` | `4` | 4 |
| `rounded-t-md` | `6` | 6 |
| `rounded-t-lg` | `8` | 8 |
| `rounded-t-xl` | `12` | 12 |
| `rounded-t-2xl` | `16` | 16 |
| `rounded-t-3xl` | `24` | 24 |
| `rounded-t-4xl` | `32` | 32 |
| `rounded-t-none` | `0` | 0 |
| `rounded-t-full` | `9999` | 9999 |
| `rounded-r-xs` | `2` | 2 |
| `rounded-r-sm` | `4` | 4 |
| `rounded-r-md` | `6` | 6 |
| `rounded-r-lg` | `8` | 8 |
| `rounded-r-xl` | `12` | 12 |
| `rounded-r-2xl` | `16` | 16 |
| `rounded-r-3xl` | `24` | 24 |
| `rounded-r-4xl` | `32` | 32 |
| `rounded-r-none` | `0` | 0 |
| `rounded-r-full` | `9999` | 9999 |
| `rounded-b-xs` | `2` | 2 |
| `rounded-b-sm` | `4` | 4 |
| `rounded-b-md` | `6` | 6 |
| `rounded-b-lg` | `8` | 8 |
| `rounded-b-xl` | `12` | 12 |
| `rounded-b-2xl` | `16` | 16 |
| `rounded-b-3xl` | `24` | 24 |
| `rounded-b-4xl` | `32` | 32 |
| `rounded-b-none` | `0` | 0 |
| `rounded-b-full` | `9999` | 9999 |
| `rounded-l-xs` | `2` | 2 |
| `rounded-l-sm` | `4` | 4 |
| `rounded-l-md` | `6` | 6 |
| `rounded-l-lg` | `8` | 8 |
| `rounded-l-xl` | `12` | 12 |
| `rounded-l-2xl` | `16` | 16 |
| `rounded-l-3xl` | `24` | 24 |
| `rounded-l-4xl` | `32` | 32 |
| `rounded-l-none` | `0` | 0 |
| `rounded-l-full` | `9999` | 9999 |
| `rounded-ss-xs` | `2` | 2 |
| `rounded-ss-sm` | `4` | 4 |
| `rounded-ss-md` | `6` | 6 |
| `rounded-ss-lg` | `8` | 8 |
| `rounded-ss-xl` | `12` | 12 |
| `rounded-ss-2xl` | `16` | 16 |
| `rounded-ss-3xl` | `24` | 24 |
| `rounded-ss-4xl` | `32` | 32 |
| `rounded-ss-none` | `0` | 0 |
| `rounded-ss-full` | `9999` | 9999 |
| `rounded-se-xs` | `2` | 2 |
| `rounded-se-sm` | `4` | 4 |
| `rounded-se-md` | `6` | 6 |
| `rounded-se-lg` | `8` | 8 |
| `rounded-se-xl` | `12` | 12 |
| `rounded-se-2xl` | `16` | 16 |
| `rounded-se-3xl` | `24` | 24 |
| `rounded-se-4xl` | `32` | 32 |
| `rounded-se-none` | `0` | 0 |
| `rounded-se-full` | `9999` | 9999 |
| `rounded-ee-xs` | `2` | 2 |
| `rounded-ee-sm` | `4` | 4 |
| `rounded-ee-md` | `6` | 6 |
| `rounded-ee-lg` | `8` | 8 |
| `rounded-ee-xl` | `12` | 12 |
| `rounded-ee-2xl` | `16` | 16 |
| `rounded-ee-3xl` | `24` | 24 |
| `rounded-ee-4xl` | `32` | 32 |
| `rounded-ee-none` | `0` | 0 |
| `rounded-ee-full` | `9999` | 9999 |
| `rounded-es-xs` | `2` | 2 |
| `rounded-es-sm` | `4` | 4 |
| `rounded-es-md` | `6` | 6 |
| `rounded-es-lg` | `8` | 8 |
| `rounded-es-xl` | `12` | 12 |
| `rounded-es-2xl` | `16` | 16 |
| `rounded-es-3xl` | `24` | 24 |
| `rounded-es-4xl` | `32` | 32 |
| `rounded-es-none` | `0` | 0 |
| `rounded-es-full` | `9999` | 9999 |
| `rounded-tl-xs` | `2` | 2 |
| `rounded-tl-sm` | `4` | 4 |
| `rounded-tl-md` | `6` | 6 |
| `rounded-tl-lg` | `8` | 8 |
| `rounded-tl-xl` | `12` | 12 |
| `rounded-tl-2xl` | `16` | 16 |
| `rounded-tl-3xl` | `24` | 24 |
| `rounded-tl-4xl` | `32` | 32 |
| `rounded-tl-none` | `0` | 0 |
| `rounded-tl-full` | `9999` | 9999 |
| `rounded-tr-xs` | `2` | 2 |
| `rounded-tr-sm` | `4` | 4 |
| `rounded-tr-md` | `6` | 6 |
| `rounded-tr-lg` | `8` | 8 |
| `rounded-tr-xl` | `12` | 12 |
| `rounded-tr-2xl` | `16` | 16 |
| `rounded-tr-3xl` | `24` | 24 |
| `rounded-tr-4xl` | `32` | 32 |
| `rounded-tr-none` | `0` | 0 |
| `rounded-tr-full` | `9999` | 9999 |
| `rounded-br-xs` | `2` | 2 |
| `rounded-br-sm` | `4` | 4 |
| `rounded-br-md` | `6` | 6 |
| `rounded-br-lg` | `8` | 8 |
| `rounded-br-xl` | `12` | 12 |
| `rounded-br-2xl` | `16` | 16 |
| `rounded-br-3xl` | `24` | 24 |
| `rounded-br-4xl` | `32` | 32 |
| `rounded-br-none` | `0` | 0 |
| `rounded-br-full` | `9999` | 9999 |
| `rounded-bl-xs` | `2` | 2 |
| `rounded-bl-sm` | `4` | 4 |
| `rounded-bl-md` | `6` | 6 |
| `rounded-bl-lg` | `8` | 8 |
| `rounded-bl-xl` | `12` | 12 |
| `rounded-bl-2xl` | `16` | 16 |
| `rounded-bl-3xl` | `24` | 24 |
| `rounded-bl-4xl` | `32` | 32 |
| `rounded-bl-none` | `0` | 0 |
| `rounded-bl-full` | `9999` | 9999 |

### A14  Border Width — border-width (45 variables)

| Token | Value (px) |
|---|---|
| `border-0` | `0` |
| `border` | `1` |
| `border-2` | `2` |
| `border-4` | `4` |
| `border-8` | `8` |
| `border-x-0` | `0` |
| `border-x` | `1` |
| `border-x-2` | `2` |
| `border-x-4` | `4` |
| `border-x-8` | `8` |
| `border-y-0` | `0` |
| `border-y` | `1` |
| `border-y-2` | `2` |
| `border-y-4` | `4` |
| `border-y-8` | `8` |
| `border-s-0` | `0` |
| `border-s` | `1` |
| `border-s-2` | `2` |
| `border-s-4` | `4` |
| `border-s-8` | `8` |
| `border-e-0` | `0` |
| `border-e` | `1` |
| `border-e-2` | `2` |
| `border-e-4` | `4` |
| `border-e-8` | `8` |
| `border-t-0` | `0` |
| `border-t` | `1` |
| `border-t-2` | `2` |
| `border-t-4` | `4` |
| `border-t-8` | `8` |
| `border-r-0` | `0` |
| `border-r` | `1` |
| `border-r-2` | `2` |
| `border-r-4` | `4` |
| `border-r-8` | `8` |
| `border-b-0` | `0` |
| `border-b` | `1` |
| `border-b-2` | `2` |
| `border-b-4` | `4` |
| `border-b-8` | `8` |
| `border-l-0` | `0` |
| `border-l` | `1` |
| `border-l-2` | `2` |
| `border-l-4` | `4` |
| `border-l-8` | `8` |

### A15  Opacity — opacity (21 variables)

| Token | Value (%) |
|---|---|
| `opacity-0` | `0` |
| `opacity-5` | `5` |
| `opacity-10` | `10` |
| `opacity-15` | `15` |
| `opacity-20` | `20` |
| `opacity-25` | `25` |
| `opacity-30` | `30` |
| `opacity-35` | `35` |
| `opacity-40` | `40` |
| `opacity-45` | `45` |
| `opacity-50` | `50` |
| `opacity-55` | `55` |
| `opacity-60` | `60` |
| `opacity-65` | `65` |
| `opacity-70` | `70` |
| `opacity-75` | `75` |
| `opacity-80` | `80` |
| `opacity-85` | `85` |
| `opacity-90` | `90` |
| `opacity-95` | `95` |
| `opacity-100` | `100` |

### A16  Stroke Width — stroke-width (11 variables)

| Token | Value (value) |
|---|---|
| `stroke-0,5` | `0.5` |
| `stroke-0,75` | `0.75` |
| `stroke-1` | `1` |
| `stroke-1,25` | `1.25` |
| `stroke-1,5` | `1.5` |
| `stroke-1,75` | `1.75` |
| `stroke-2` | `2` |
| `stroke-2,25` | `2.25` |
| `stroke-2,5` | `2.5` |
| `stroke-2,75` | `2.75` |
| `stroke-3` | `3` |

### Token Count Verification

| Collection | Variables |
|---|---|
| shadcn-ui | 35 |
| tw-colors | 244 |
| tokens | 87 |
| border-radius | 150 |
| border-width | 45 |
| font | 45 |
| height | 24 |
| gap | 102 |
| max-height | 35 |
| max-width | 51 |
| margin | 245 |
| padding | 245 |
| opacity | 21 |
| space | 68 |
| stroke-width | 11 |
| rdx-colors | 396 |
| **TOTAL** | **1804** |

> Source: `variables-export.json` — 1804 variables total.