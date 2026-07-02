# Scenario Edge Layer — Reference (Step 2.5b)

Read this when generating `scenario-edges.json`. It runs **after Step 2.5 Product Intelligence, in
parallel with Step 2.6 Aesthetic** (the two share no data), and enumerates the **scenario / requirement
edge cases** a product must handle — the messy real-world situations that decide *what flows and screens
must exist*, discovered from the intelligence dimensions.

## Why this is not Step 3.7

3.7 (Edge-Case Analysis) and 2.5b are two **altitudes** of the same spine — they do not overlap:

| | **2.5b Scenario Edge** (this) | **3.7 Screen Edge** |
|---|---|---|
| Asks | "what **situations** must the product handle?" | "what **states** must this screen survive?" |
| Altitude | product / requirement | UI / screen + data boundary |
| Reads | `intelligence.json` (the 10 dims) | `screen-inventory.json` + `flows.json` |
| Output | discovers **missing flows / screens** | hardens **existing** screens |
| Runs | after 2.5, before flows (Step 3) | after 3.5, before build (Step 4) |

2.5b sits **upstream** and *feeds* 3.7: a scenario edge can inject a whole new flow (`may_inject_flow`),
and 3.7 then enumerates that flow's UI states. If you only run 3.7, you design states for the screens you
already have — you never discover you're **missing** a flow (e.g. "reverse a transaction",
"withdraw consent") because nobody asked the scenario question.

---

## The taxonomy — the 10 dimensions pushed to their edge

Grounded like 3.7's UI-Stack × CORRECT: **not invented per project**. Every scenario edge names the
`intelligence.json` **dimension** it derives from, so a reviewer can trace it back instead of trusting
the agent's imagination. Enumerate the ones the product's dimensions make real:

| `dimension` | The edge it surfaces |
|---|---|
| `user_types` | conflicting actors · an unauthorized actor · delegation / handoff between roles |
| `user_expertise` | the total novice's first run · the power user at scale (bulk / keyboard) |
| `user_goals` | the goal blocked mid-way · two goals in tension for one user |
| `core_tasks` | a task abandoned part-done · a task that must resume elsewhere |
| `workflow_complexity` | interrupted / resumed on another device · **two users acting on one entity** (concurrency) |
| `data_density` | the empty account (0 records) · the overloaded one (10k rows, overflow) |
| `error_tolerance` | the **irreversible** mistake + its recovery / undo path |
| `accessibility_needs` | situational impairment (one-handed, bright sun, noisy) · assistive tech |
| `compliance_requirements` | consent withdrawn · a minor detected · a jurisdiction boundary crossed |
| `decision_criticality` | a wrong high-stakes decision · the audit / review-after-the-fact path |

---

## `scenario-edges.json` shape

```jsonc
{
  "meta": { "source_intelligence": "output/intelligence.json", "generated_at": "ISO-8601",
            "schema_version": "1.0",
            "driven_by": { "error_tolerance": "", "decision_criticality": "",
                           "compliance_mandatory": false },   // snapshot the directive floors used
            "overall_confidence": "high|medium|low" },

  "scenario_edges": [{
    "id": "SE01",
    "dimension": "workflow_complexity",     // which of the 10 intelligence dimensions this rests on
    "scenario": "<the real-world situation, one sentence>",
    "trigger": "<what causes it>",
    "impact": "<what breaks / who is hurt if unhandled>",
    "severity": "must|should|could",        // driven by directives, NOT taste (see floors)
    "suggested_handling": "<the flow/screen/guard that would handle it>",
    "may_inject_flow": { "inject": true, "flow_name": "withdraw-consent" },  // → Step 3 adds it
    "user_type_ref": "UT01",                // optional refs into intelligence.json (resolve when provided)
    "task_ref": "T03",
    "compliance_ref": "C01",
    "source": "stated|inferred", "confidence": "high|medium|low",
    "open_question": "" }]                    // required when a must-severity edge rests on a low-confidence inference
}
```

`may_inject_flow.inject == true` is the **seam** into Step 3: each becomes a mandatory/injected flow
(`source_flow_ref: null`), which then flows to 3.5 screens and 3.7 UI-state edges. That is how a scenario
question ("what if consent is withdrawn?") becomes a real screen instead of a silent gap.

---

## Severity floors (hard fails — severity from intelligence, not taste)

Mirrors 3.7 rule 2: a high-stakes product can't quietly mark its scenario edges "could".

| Floor |
|---|
| `error_tolerance ∈ {low, zero}` ⇒ every `dimension:"error_tolerance"` edge is `severity:"must"` **and** its `suggested_handling` names a recovery / undo / confirm |
| `decision_criticality ∈ {high, safety_critical}` ⇒ every `dimension:"decision_criticality"` edge is `severity:"must"` |
| a **mandatory** compliance requirement in intelligence ⇒ ≥1 `dimension:"compliance_requirements"` edge, `severity:"must"` |
| every `severity:"must"` edge that is `source:"inferred"` + `confidence:"low"` ⇒ carries an `open_question` (don't silently mandate a flow off a guess) |

## Structural / referential (hard fails)

| Rule |
|---|
| every `dimension` ∈ the 10 intelligence dimensions |
| ids unique; `severity` ∈ {must, should, could}; `source`/`confidence` valid enums |
| when `intelligence.json` is provided ⇒ `user_type_ref` → `user_types`, `task_ref` → `core_tasks`, `compliance_ref` → `compliance_requirements` all resolve |
| `may_inject_flow.inject == true` ⇒ non-empty `flow_name` |

**Warnings (quality):** a high-signal dimension with no edge (`error_tolerance ∈ {low,zero}` /
`decision_criticality ∈ {high,safety_critical}` / any mandatory compliance) — likely a coverage gap.

> Validated by `scripts/validate_scenario_edges.py` (pass `intelligence.json` as the 2nd arg to
> resolve refs + enforce the severity floors).

---

## Generation prompt (agent reads `intelligence.json` [+ `brief.json`] → writes `scenario-edges.json`)

```text
You are enumerating SCENARIO edge cases — the real-world situations the product must handle, one
altitude ABOVE screen states. INPUT: intelligence.json (the 10 dimensions + design_directives).
OUTPUT: scenario-edges.json per the shape above.

1. WALK THE 10 DIMENSIONS. For each, ask "what is its boundary / failure scenario?" (see the taxonomy).
   Write an edge only where the product's dimensions make it real — don't pad.
2. GROUND EVERY EDGE. Name the dimension it rests on; add user_type_ref/task_ref/compliance_ref that
   resolve into intelligence.json. An edge that traces to nothing is invention.
3. SEVERITY FROM INTELLIGENCE, NOT TASTE. Apply the floors: low/zero error_tolerance → its edges are
   must (+ a recovery in suggested_handling); high/safety decision_criticality → must; mandatory
   compliance → a must edge. Snapshot the floors used into meta.driven_by.
4. FEED STEP 3. When an edge implies a whole flow that doesn't exist yet (withdraw consent, reverse a
   transaction, resume-on-another-device), set may_inject_flow.inject=true + a flow_name.
5. BE HONEST. A must-severity edge resting on a low-confidence inference carries an open_question.

Process: for each of the 10 dimensions → derive its edge(s) → set severity from the floors → mark
may_inject_flow where a new flow is implied → open_question for every low-confidence must.
```
