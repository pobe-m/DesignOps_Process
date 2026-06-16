# Mobile Usability — UI & UX checklist

Most TORs here are **mobile-first**. A layout that merely *fits* a phone is not usable on one.
Apply this when generating screens (Step 3.5 / Step 4) and when scoring the **Responsiveness**
dimension in critique (Step 4.6). Pairs with `performance.md` (mobile is where slow UIs fail first),
`accessibility/wcag-checklist.md` (target size), and `ux-writing/voice-tone.md` (short copy).

## 1. Touch targets (the #1 mobile defect)

- **Minimum 44×44 px** tappable area for any control (Apple HIG 44pt, Material 48dp, WCAG 2.5.5 AAA;
  WCAG 2.5.8 AA floor is 24×24 with spacing). Icon-only buttons especially — pad the hit area, not
  just the glyph.
- **≥ 8 px gap** between adjacent targets so fat fingers don't mis-tap.
- Make the **whole row/card tappable**, not a tiny "›" chevron.
- Primary action buttons: full-width or near it on phones; don't shrink to content.

## 2. Thumb reachability

- Put the **primary action within thumb reach** — bottom third of the screen, not the top corners.
  Long forms: a sticky bottom CTA bar beats a button far above the fold.
- Top corners are the hardest to reach one-handed — reserve them for low-frequency actions (close, menu).
- Keep destructive and primary actions **far apart** to avoid mis-taps.

## 3. Input ergonomics (forms feel 2× slower on mobile)

- Use the **right input type** so the right keyboard appears: `type="tel|email|number|url|date"`,
  `inputMode="numeric|decimal"`, `autoComplete` (e.g. `one-time-code`, `name`, `tel`).
- **Body/input font ≥ 16 px** — smaller triggers iOS auto-zoom on focus (jarring).
- **Labels, not placeholder-only** (placeholder vanishes on type; fails recall + a11y).
- Minimize fields; split long forms into steps (a wizard) rather than one long scroll.
- Native pickers (date/select) beat custom dropdowns on touch unless you build them for touch.

## 4. Layout & viewport

- **No horizontal scroll at 320 px.** Single-column by default; reflow, don't shrink.
- Respect **safe-area insets** (notch / home indicator): `env(safe-area-inset-*)` for sticky bars.
- Fluid type and spacing; tap copy and numbers large enough to read outdoors (contrast matters more
  on a sunlit phone — keep to the a11y target).
- Sticky headers should be thin; don't eat the small viewport.

## 5. Gestures, hover & states

- **No hover-only affordances.** Touch has no hover — anything revealed on hover (tooltips, menus,
  "row actions") must be reachable by tap. Keep hover as enhancement only.
- Provide **visible tap feedback** (active/pressed state); avoid long-press-only or swipe-only actions
  without a visible alternative.
- Don't rely on right-click / hover context menus.

## 6. Performance (felt hardest on mobile)

- Above-the-fold first; lazy-load below-fold and behind interaction. Reserve image space
  (`aspect-ratio`) to avoid layout shift. See `performance.md` (LCP ≤ 2.5s, INP ≤ 200ms, CLS ≤ 0.1
  on a mid-tier phone).
- Respect `prefers-reduced-motion`; keep animation to transform/opacity.

## 7. Dev / testing note

- To test on a real phone over Wi-Fi, the dev server must allow the LAN origin. The scaffolded
  prototype's `next.config.ts` already computes `allowedDevOrigins` from the machine's LAN IPs
  (Next 16 blocks cross-origin dev HMR otherwise, which leaves the page un-hydrated and buttons
  dead). Open `http://<lan-ip>:3000` on the phone.

## Quick checklist (score Responsiveness against this)

```
□ Every control ≥ 44×44 px, ≥ 8px apart; whole row tappable
□ Primary action in thumb reach (bottom), destructive far from primary
□ Correct input type/keyboard; input font ≥ 16px; real labels
□ No horizontal scroll at 320px; single-column reflow; safe-area insets
□ No hover-only / long-press-only actions; visible tap feedback
□ Fast first paint, no layout shift, reduced-motion honored
□ Testable on a real device (LAN origin allowed)
```
