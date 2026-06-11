# Critique Framework Reference — DesignOps Loop

Read this file when entering CRITIQUE mode — especially for complex contexts (HIS, Dashboard, Multi-screen).

---

## Critique Principles

1. **Always state the context first** — critiquing a dashboard ≠ a landing page ≠ a mobile app
2. **Severity before aesthetics** — usability / a11y comes before visual preference
3. **Concrete over vague** — "adjust the spacing" isn't enough → "increase the gap between label and input from 4px to 8px"
4. **Preserve what works** — call out the good too, not just the problems
5. **Always quick wins** — point out fixes that take < 15 minutes with high impact

---

## Layer 1: Visual Hierarchy

### What to check

**Focal Point**
- Is there a clear primary focal point within the first 3 seconds?
- If several things attract attention equally → hierarchy is broken
- Is F-pattern / Z-pattern reading correct for the content type?

**Contrast Hierarchy**
- Are font sizes different enough between H1 / H2 / Body?
- Is the color contrast between primary / secondary content clear enough?
- Is visual weight (bold, color, size) used consistently with importance?

**Spacing Rhythm**
- Is whitespace consistent? Or are some sections too dense while others too sparse?
- Are section breaks clear?
- Is the gap between label and input correct? (label too close to the input, or too far)

### Dashboard-Specific Hierarchy Checks
- Does the most important KPI / key metric get the largest visual treatment?
- Do alert / warning statuses attract attention without scanning?
- Are trends (up/down) readable via color + icon (not color alone)?

---

## Layer 2: Information Architecture

### Flow Clarity
- Does the user know what to do next after viewing this screen?
- Is the primary action clear? Are there competing calls-to-action?
- Is breadcrumb / wayfinding complete for multi-level navigation?

### Content Grouping
- Is related content grouped together (proximity principle)?
- Do groups have a clear visual boundary (card, separator, whitespace)?
- Does the information order match the user's mental model?

### Label Quality
- Do labels clearly say what the data is (not just "Data" or "Value")?
- Is the unit stated in the label or near the value? (e.g. "Total (USD)" or "$1,234")
- Are abbreviations fully explained or intuitive enough?

### Healthcare / HIS IA Checks
- Is critical information (allergy, alert, override) at the top of the context?
- Is the patient identifier visible throughout the session?
- Does time-sensitive information have a timestamp?
- Is navigating between patient records safe (no accidental context switch)?

---

## Layer 3: Component Consistency

### Visual Consistency
- Do buttons of the same kind have the same size / style?
- A single icon set (no mixed icon families)?
- Is corner radius consistent across the page?
- Is color usage consistent (same semantic meaning = same color)?

### Behavioral Consistency
- Do all interactive elements have Hover / Focus states?
- Are loading states the same (spinner vs skeleton)?
- Do error states follow the same pattern?
- Are there empty states?

### Spacing Consistency
- Does spacing between elements use the token scale, not magic numbers?
- Is internal padding consistent across components of the same type?

---

## Layer 4: Context Fit

### Audience Fit Matrix

| Audience | Key concerns |
|---|---|
| Clinician / HIS user | Speed, error prevention, information density, trust |
| Admin / back office | Efficiency, batch operations, data completeness |
| Consumer / end user | Clarity, delight, onboarding, trust signals |
| Executive / dashboard viewer | KPI at-a-glance, trend clarity, drill-down |
| Government / public service | Accessibility, language clarity, trust, official tone |

### Density Check
- Is content density appropriate for the context?
  - Dashboard → density 6-8 (lots of data, but scannable)
  - Consumer app → density 3-5 (breathing room)
  - HIS → density 6-7 (must show complete data without overwhelming)

### Trust Signals
- Healthcare / Fintech: are there visual cues that data is current / verified?
- Do error states clearly state the next action? Not just "Error occurred"
- Do destructive actions have a confirmation step?

---

## Critique Output Templates

### Template A: Single Component

```markdown
## Critique: [Component Name]
**Context:** [screen / flow the component lives in]
**Summary:** [1-2 sentences]

### 🔴 Critical (fix before ship)
- **[Issue name]:** [explain why it's broken]
  → Fix: [concrete action]

### 🟡 High (should fix)
- **[Issue name]:** [explain]
  → Fix: [concrete action]

### 🔵 Low / Polish
- **[Issue name]:** [explain]
  → Fix: [concrete action]

### ✅ What's Working
- [call out the good — at least 2-3 things]

### ⚡ Quick Wins (< 15 min each)
- [fixes that are fast and high-impact]
```

### Template B: Full Screen / Flow

```markdown
## Critique: [Screen / Flow Name]
**Mode:** [Desktop / Mobile / Both]
**Context:** [user journey step]
**Summary:** [overall health assessment]

### Layer 1: Visual Hierarchy
[findings]

### Layer 2: Information Architecture
[findings]

### Layer 3: Component Consistency
[findings]

### Layer 4: Context Fit
[findings]

### Priority Matrix
| Issue | Severity | Effort | Priority |
|---|---|---|---|
| [issue] | 🔴 High | Low | Do first |
| [issue] | 🟡 Med | Low | Quick win |
| [issue] | 🔴 High | High | Plan sprint |
| [issue] | 🔵 Low | Low | Nice to have |

### Recommended Fix Order
1. [highest impact, lowest effort first]
```

---

## Critique Anti-Patterns (what good critique doesn't do)

- ❌ "Looks unprofessional" — no concrete detail → say exactly what makes it look unprofessional
- ❌ "Improve the spacing" — name the component + current value + recommended value
- ❌ Critiquing an aesthetic preference with no rationale — "I don't like the color" isn't a critique
- ❌ Listing every problem without prioritizing — always state severity
- ❌ Critiquing something the user already did correctly without acknowledging it
- ❌ Recommending a full redesign when a targeted fix is enough
