# Edge-Case Layer — Reference (Step 3.7)

Read this when generating `edge-cases.json`. It runs **after Step 3.5 Screen Inventory, before
Step 4 build** — once the flows and screens exist but before anything is coded — and enumerates the
**non-happy-path conditions every Must screen has to survive**: empty data, bad input, a failed
request, a destructive click. It is the **front end of the edge-case spine**: the contract that the
build must satisfy and that the Step 4.7 **gate 9** (`lint_edge_coverage.py`) verifies on the built
prototype. Same shape as the intent-traceability spine (`feature → task → flow → screen → route`),
with **edge case** as one more traceable contract.

It is **not** invented per-project. The taxonomy is the cross-product of two established frameworks,
so a reviewer can check the reasoning back to a source instead of trusting the agent's imagination.

**The two axes:**
- **The UI Stack** (Scott Hurff, *Designing Products People Love*) — every screen has **five states**:
  **Ideal · Empty · Error · Partial · Loading**. The happy path designs only *Ideal*; the other four
  are where products break. This axis answers *"what condition is the screen in?"* and maps directly
  onto `screen-inventory.json`'s declared `states` (`loading`/`empty`/`error`) — it just adds
  **Partial** (data arrived incomplete / truncated) and names **Ideal** explicitly.
- **CORRECT** (Hunt & Thomas, *Pragmatic Unit Testing*) — seven boundary dimensions for *input and
  data*: **C**onformance · **O**rdering · **R**ange · **R**eference · **E**xistence · **C**ardinality
  · **T**ime. This axis answers *"what about the data pushes the screen off the happy path?"*

**Three rules:**
1. **Trace or it doesn't count.** Every edge case names a real `maps_to_screen` (a `screen-inventory.json`
   id) and, when it's flow-driven, a real `maps_to_flow` (a `flows.json` id). An edge case that points
   nowhere is rejected — it can't be verified downstream.
2. **Severity is driven by intelligence, not taste.** `must`/`should`/`could` is set from
   `intelligence.json` → `design_directives` (see the matrix below), so a zero-error-tolerance product
   can't quietly mark its error states "could".
3. **Every declared screen state needs a reason.** If `screen-inventory.json` says a Must screen renders
   an `empty` or `error` state, there must be ≥1 edge case explaining *what triggers it* and *how it's
   handled* — otherwise the declared state is decoration.

> Validated by `scripts/validate_edgecases.py`. Verified end-to-end by Step 4.7 **gate 9**
> (`lint_edge_coverage.py`): every **Must** edge case must have detectable handling in the built screen.

---

## The taxonomy (UI Stack × CORRECT)

Use this grid to enumerate. Not every cell applies to every screen — pick the ones the screen's data
and flow make real. The **UI-state** column is what the screen shows; the **CORRECT** column is the
data condition that triggers it.

| UI state | When it happens | CORRECT dimensions that drive it | Typical handling to design |
|----------|-----------------|----------------------------------|----------------------------|
| **Empty** | no data yet, or a filter/search returns nothing | **E**xistence, **C**ardinality (the `0` of 0-1-n) | empty-state with value prop + primary action (not a blank box) |
| **Error** | request failed, server 4xx/5xx, validation rejected | **R**eference (external dep down), **C**onformance (bad format), **R**ange (out of bounds) | error state with *what → why → how to recover*; inline `FieldError` for input |
| **Partial** | some data loaded, some missing/truncated; long text, big numbers | **C**ardinality (the `n`, overflow), **O**rdering | truncate + "show more", skeleton for the missing part, no layout break at max volume |
| **Loading** | request in flight, slow network, optimistic update pending | **T**ime (latency, timeout) | skeleton/spinner with `aria-busy`; timeout + retry; never a frozen UI |
| **Ideal** | the happy path (already designed in Step 4) | — | baseline; edge cases are everything that deviates from it |

**Cross-cutting CORRECT cases that aren't a single UI state** (still enumerate them when the data
allows):
- **Conformance** — invalid email/phone/date format, wrong file type → inline validation.
- **Ordering** — list assumed sorted but isn't; steps done out of sequence → guard or re-sort.
- **Range** — min/max/length boundary, `min−1` / `max+1`, zero, negative → clamp + message (Boundary
  Value Analysis: test the boundary, not the middle).
- **Reference** — depends on an external thing it doesn't control (API, auth token, prior screen's
  selection) → handle the dependency being absent/expired (session expired, 401, stale ref).
- **Existence** — `null` / empty / absent / not-yet-loaded → the Empty state above, plus null-safety.
- **Cardinality** — the **0-1-n / fencepost** rule: design for zero items, exactly one, and many
  (overflow). Most "looks done" screens only handle the *many* case with tidy mock data.
- **Time** — timeout, slow response, **concurrency** (stale data, a conflicting edit), things arriving
  out of order → optimistic-update rollback, conflict warning, retry.

> The Step 4.7 audit recomputes the back side of this in *Right-BICEP* terms — **B**oundary, **E**rror,
> **R**eference (cross-check) — so the front taxonomy and the back gate speak the same language.

---

## Severity matrix — driven by `intelligence.json`

Set each edge case's `severity` from the product's directives. The agent does **not** free-choose;
`validate_edgecases.py` enforces the `must` floors below.

| Directive (from Step 2.5) | Effect on edge-case severity |
|---|---|
| `error_tolerance.overall` = `low` or `zero` | every Must screen needs ≥1 **Error** edge **and** ≥1 input-validation (Conformance/Range/Existence) edge at `must` |
| `decision_criticality.overall` = `high` or `safety_critical` | every destructive / irreversible action needs a **confirm** edge (Time/Reference) at `must`; safety_critical also needs an **undo / cascade-warning** edge |
| `data_density.overall_band` ≥ 4 | **Partial** (overflow / truncation / max-volume) edges are `must` for table/list/dashboard screens |
| `guidance_level` = `guided` | every Must screen needs an **Empty** edge at `must` (a guided product never shows a dead blank screen) |
| `safeguard_level` = `strict` or `maximal` | destructive confirms escalate to type-to-confirm; `must` |

Everything else (cosmetic truncation on a low-density consumer screen, a rare ordering case) is
`should` or `could` — real, logged, but not a build blocker.

---

## `edge-cases.json` shape

```jsonc
{
  "meta": {
    "source_flows": "output/flows.json",
    "source_screens": "output/screen-inventory.json",
    "intelligence_ref": "output/intelligence.json",
    "generated_at": "ISO-8601", "schema_version": "1.0",
    // snapshot of the directives that drove severity — makes the floors auditable
    "driven_by": { "error_tolerance": "low", "decision_criticality": "high",
                   "data_density_band": 5, "guidance_level": "guided", "safeguard_level": "strict" }
  },

  "edge_cases": [
    {
      "id": "EC01",
      "ui_state": "error",                  // ideal | empty | error | partial | loading
      "correct_dim": "reference",           // conformance|ordering|range|reference|existence|cardinality|time (optional for pure UI-state cases)
      "category": "network",                // free label: network | validation | data | permission | concurrency | destructive
      "trigger": "Booking submit while the appointments API is down (502)",
      "expected_handling": "Error state: 'Couldn't save your booking — the service is busy. Retry.' with a Retry action; the form keeps its values.",
      "severity": "must",                   // must | should | could
      "maps_to_screen": "SCR_BOOKING",      // a screen-inventory.json id
      "maps_to_flow": "FL_BOOK"             // a flows.json id (optional)
    },
    {
      "id": "EC02", "ui_state": "empty", "correct_dim": "existence", "category": "data",
      "trigger": "A new patient with no appointment history opens the dashboard",
      "expected_handling": "Empty state explaining the value + a 'Book first appointment' primary action.",
      "severity": "must", "maps_to_screen": "SCR_DASH", "maps_to_flow": "FL_BOOK"
    },
    {
      "id": "EC03", "ui_state": "error", "correct_dim": "conformance", "category": "validation",
      "trigger": "Phone number entered in the wrong format",
      "expected_handling": "Inline FieldError + aria-invalid; submit blocked until valid; not red colour alone.",
      "severity": "must", "maps_to_screen": "SCR_BOOKING", "maps_to_flow": "FL_BOOK"
    }
  ],

  "coverage": { "must": 0, "should": 0, "could": 0 }   // rollup (informational)
}
```

---

## Integrity invariants (hard fails — `validate_edgecases.py`)

| Invariant |
|---|
| `edge_cases` is a non-empty array; every `id` unique |
| every `ui_state` ∈ {`ideal`,`empty`,`error`,`partial`,`loading`} |
| `correct_dim`, when present, ∈ {`conformance`,`ordering`,`range`,`reference`,`existence`,`cardinality`,`time`} |
| every `severity` ∈ {`must`,`should`,`could`} |
| every `maps_to_screen` resolves to a `screen-inventory.json` screen id |
| every `maps_to_flow`, when present, resolves to a `flows.json` flow id |
| every `must` edge has a non-empty `expected_handling` (an unactionable blocker is not a contract) |
| every Must screen that declares an `empty`/`error` state in `screen-inventory.json` has ≥1 edge case of that `ui_state` mapped to it (declared states need a reason) |
| **directive floors** (only when `intelligence.json` resolves): the `error_tolerance` / `decision_criticality` / `guidance_level` floors from the severity matrix are satisfied |

> Advisory **warnings** (never block): a screen with Must edges of `ui_state:empty`/`error` that the
> screen-inventory does **not** declare (likely screen-inventory drift); `should`/`could` edges with no
> `expected_handling`; a destructive `category` with no confirm edge when criticality is only `medium`.

---

## Generation prompt (agent reads flows + screen-inventory + intelligence → writes `edge-cases.json`)

```text
You are a Quality Engineer enumerating the edge cases a build must survive, BEFORE it is built.
INPUT: flows.json (the happy paths), screen-inventory.json (the Must/Should/Could screens + their
declared states), intelligence.json (error_tolerance, decision_criticality, data_density,
guidance_level, safeguard_level).

OUTPUT: edge-cases.json per the shape above. Enumerate, don't free-associate:

1. WALK EVERY MUST SCREEN THROUGH THE UI STACK. For each, ask: what is its Empty / Error / Partial /
   Loading state? Ideal is already designed — skip it. Write an edge case for each non-ideal state
   that can really occur given the screen's data and flow.
2. WALK ITS DATA THROUGH CORRECT. For each input or data dependency on the screen, ask the seven:
   Conformance (bad format?), Ordering, Range (min/max/0/boundary — Boundary Value Analysis),
   Reference (external dep down/expired?), Existence (null/empty?), Cardinality (0-1-n / overflow?),
   Time (timeout / concurrency?). Write an edge case for each that applies.
3. SET SEVERITY FROM INTELLIGENCE, NOT TASTE. Apply the severity matrix: low/zero error_tolerance
   forces error + validation edges to `must`; high/safety_critical criticality forces destructive
   confirms (and undo) to `must`; dense data forces Partial/overflow to `must`; guided forces Empty
   to `must`. Snapshot those directives into meta.driven_by.
4. TRACE EVERYTHING. Each edge case maps_to_screen (a real screen id) and, when flow-driven,
   maps_to_flow (a real flow id). No orphans.
5. EXPLAIN EVERY DECLARED STATE. If a Must screen declares an empty/error state in screen-inventory,
   make sure ≥1 edge case explains its trigger + handling.
6. Roll up coverage. Keep handling concrete ("Retry action, form keeps values"), not "handle error".
```

---

## Frameworks referenced (so the taxonomy is auditable, not invented)

- **The UI Stack — the 5 states of a UI.** Scott Hurff, *Designing Products People Love* (2015). →
  the `ui_state` axis (Ideal/Empty/Error/Partial/Loading).
- **CORRECT boundary heuristic** + **Right-BICEP.** Andrew Hunt & David Thomas, *Pragmatic Unit
  Testing* (The Pragmatic Programmers). → the `correct_dim` axis (front) and the gate-9 framing (back).
- **Boundary Value Analysis** + **Equivalence Partitioning.** Glenford Myers, *The Art of Software
  Testing* (1979); codified by **ISTQB** Foundation black-box techniques. → the Range / Cardinality cases.
- **State Transition Testing** (ISTQB). → flow-driven edges (out-of-order steps, stale state).
- **Stress cases.** Eric Meyer & Sara Wachter-Boettcher, *Design for Real Life* (A Book Apart, 2016).
  → why severity is driven by `error_tolerance` (edges aren't rare "edges", they're users under stress).
- **Inclusive Design / Persona Spectrum** (Microsoft). → accessibility/situational edges, paired with
  the existing `accessibility/wcag-checklist.md`.
