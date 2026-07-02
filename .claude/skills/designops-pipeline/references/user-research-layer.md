# User Research Layer — Reference (Step 2.3)

Read this when generating `research.json`. It sits **after the brief, before Product Intelligence
(2.5)** and turns the brief's stated audience into structured research artifacts — personas,
jobs-to-be-done, pain points, behavioral assumptions — that become *evidence* for the
intelligence layer instead of raw guesses.

**Hybrid by design.** An AI pipeline cannot run real interviews. So this layer operates in one
of three modes, declared in `meta.evidence_mode`:
- `inferred` — no real inputs; everything is a **hypothesis** derived from the TOR. Caps confidence at `medium`.
- `hybrid` — some real inputs provided (interview notes, analytics, surveys); those items are `evidence`, the rest stay `inferred`.
- `evidence_backed` — all items grounded in provided inputs.

**Three rules:**
1. **Never fabricate evidence.** If `meta.inputs_provided` is empty, every item is `source:"inferred"`. You may not mark anything `evidence` without a matching ref in `inputs_provided`.
2. **Inferred ≠ confident.** `source:"inferred"` may never claim `confidence:"high"` — an unvalidated guess is medium at best, and every high-risk assumption needs a `research_question`.
3. **Outcomes, not features.** JTBD are situations + motivations ("when I…, I want…, so that…"), never UI.

> Validated by `scripts/validate_research.py` — schema + ref resolution + the **honesty invariants** below. Feeds `intelligence.json` via `feeds_intelligence`.
> Worked example + how to upgrade inferred→hybrid by providing real inputs: `examples/research.example.json` + `examples/README.md`.

---

## `research.json` shape

```jsonc
{
  "meta": { "source_brief": "output/brief.json", "generated_at": "ISO-8601", "schema_version": "1.0",
            "evidence_mode": "inferred|hybrid|evidence_backed",
            "inputs_provided": [],            // e.g. ["interview:notes-2026-06.md","analytics:ga4-export"]; [] = pure inference
            "overall_confidence": "high|medium|low", "human_reviewed": false },

  "personas": [{ "id": "P01", "name": "", "archetype": "", "primary": true,
    "context": "", "tech_proficiency": "novice|intermediate|expert", "environment": "",
    "goals_ref": ["JTBD01"], "frustrations": [],
    "source": "inferred|evidence", "evidence": [], "confidence": "high|medium|low" }],

  "jobs_to_be_done": [{ "id": "JTBD01", "persona_ref": "P01",
    "when": "<situation>", "want": "<motivation>", "so_that": "<outcome>",
    "priority": "must|should|could", "source": "inferred|evidence", "evidence": [], "confidence": "high|medium|low" }],

  "pain_points": [{ "id": "PP01", "persona_ref": "P01", "statement": "",
    "severity": "low|med|high", "frequency": "rare|occasional|frequent",
    "source": "inferred|evidence", "evidence": [], "confidence": "high|medium|low" }],

  "behavioral_assumptions": [{ "id": "A01", "statement": "", "risk_if_wrong": "low|med|high",
    "validation_method": "interview|survey|analytics|usability_test",
    "status": "unvalidated|validated|invalidated",
    "source": "inferred|evidence", "evidence": [], "confidence": "high|medium|low" }],

  "research_questions": [{ "id": "RQ01", "question": "", "tied_to": "A01",
    "method": "interview|survey|analytics|usability_test", "priority": "blocker|important|nice_to_know" }],

  // OPTIONAL — the as-is experience, sequenced. Produce ONLY when the product is flow-shaped
  // (a redesign, or a multi-step task users already do today by hand / with a workaround).
  // `mode` is honest about what the journey maps: an existing product, a manual workaround, or none.
  // Non-flow tools (a dashboard, a reference app) skip this — affinity/pains cover them.
  "current_state_journey": [{ "persona_ref": "P01", "mode": "existing_product|workaround|none",
    "phases": [{ "name": "", "actions": [], "pains_ref": ["PP01"],
                 "emotion": 0,                      // -2..+2 emotional low/high at this phase
                 "opportunity_ref": ["OPP01"] }] }],

  // OPTIONAL — where the as-is breaks becomes a chance to improve. Each ties to the pain it relieves
  // and (when journey-driven) the phase it sits in. Feeds design_directives via feeds_intelligence.
  "opportunities": [{ "id": "OPP01", "persona_ref": "P01", "pain_ref": ["PP01"],
    "statement": "<how might we…>", "impact": "low|med|high", "effort": "low|med|high",
    "source": "inferred|evidence", "evidence": [], "confidence": "high|medium|low",
    "research_question": "RQ01" }],   // required when a high-impact opportunity rests on a low-confidence inference

  "feeds_intelligence": { "user_types_hint": [], "user_goals_hint": [], "error_tolerance_hint": "",
    "opportunity_hints": [] }         // high-impact OPP ids → Step 2.5 may promote to mandatory_flows / features
}
```

`feeds_intelligence` is the **seam** Step 2.5 reads: personas → `user_types`, JTBD → `user_goals`,
pain points + assumptions → `error_tolerance` / `open_questions`, **`opportunity_hints` → `design_directives`
(a high-impact opportunity can become a `mandatory_flow` or a promoted feature)**. Evidence-backed hints
let the intelligence layer raise its own confidence; inferred hints stay hypotheses.

`current_state_journey` is **conditional, not mandatory** — it earns its place only when the product is
flow-shaped (a redesign, or a task users already perform via a manual workaround). It is the near-free
re-projection of the same pains along a timeline: it does not add new facts, it *locates* them and turns
each breakpoint into an `opportunity`. When there is no existing experience or workaround to map
(`mode: "none"`), don't invent one — omit the journey and let pains/opportunities stand alone.

---

## Honesty invariants (hard fails)

| Invariant |
|---|
| `meta.inputs_provided == []` ⇒ every item `source == "inferred"` **and** `evidence_mode == "inferred"` |
| `source == "evidence"` ⇒ `evidence` non-empty **and** every ref ∈ `meta.inputs_provided` |
| `source == "inferred"` ⇒ `confidence != "high"` |
| `behavioral_assumptions[].status == "validated"` ⇒ `source == "evidence"` |
| every `risk_if_wrong == "high"` assumption ⇒ ≥1 `research_questions` with `tied_to` = its id |
| ≥1 persona with `primary == true`; all ids unique; every `*_ref` resolves |
| `overall_confidence == "low"` ⇒ emits `constrain_downstream=true` (Step 2.5 treats hints as low-confidence) |
| `opportunities[]` obey the same honesty rules as every other item (`source`/`confidence`; inferred ≠ high; evidence refs ∈ `inputs_provided`) |
| every `opportunities[].pain_ref` resolves to a `pain_points` id; `persona_ref` resolves to a persona; `research_question` (when set) resolves to a `research_questions` id |
| a **high-impact** opportunity that is `source:"inferred"` ⇒ must carry a `research_question` (don't build a big bet on a guess without flagging it for validation) |
| `current_state_journey[].phases[].emotion` ∈ `[-2, 2]`; every `pains_ref` → a pain id; every `opportunity_ref` → an opportunity id; `persona_ref` resolves |
| `current_state_journey` present ⇒ `mode ∈ {existing_product, workaround, none}`; `mode == "none"` ⇒ the journey should be omitted, not filled with invention |

---

## Generation prompt (agent reads `brief.json` [+ any provided inputs] → writes `research.json`)

```text
You are a UX Researcher building the User Research Layer.
INPUT: brief.json (facts) + any provided research inputs. OUTPUT: research.json per the shape above.

1. DECLARE THE MODE FIRST. List every real input in meta.inputs_provided. If there are none,
   evidence_mode="inferred" and EVERYTHING is source:"inferred" — you are writing hypotheses, label them so.
2. NEVER FABRICATE EVIDENCE. Only mark source:"evidence" when you can cite a ref that is in inputs_provided.
3. INFERRED CAPS AT MEDIUM. Any inferred item is confidence ≤ medium; every high-risk assumption gets a research_question.
4. JTBD ARE SITUATIONS, not features ("when I…, I want…, so that…").
5. Fill feeds_intelligence so Step 2.5 can consume personas/JTBD/pains as evidence.
6. CURRENT-STATE JOURNEY IS CONDITIONAL. Only map it when the product is flow-shaped and there is an
   existing experience or a manual workaround to map. It re-projects the pains you already found onto a
   timeline — it invents no new facts. If there's nothing real to map (mode:"none"), OMIT it.
7. TURN BREAKPOINTS INTO OPPORTUNITIES. Each journey low / pain becomes ≤1 opportunity tied to its pain_ref;
   score impact × effort. A high-impact opportunity resting on an inferred guess MUST carry a research_question.
   Roll high-impact OPP ids into feeds_intelligence.opportunity_hints for Step 2.5.

Process: personas → JTBD (per persona) → pain_points → behavioral_assumptions (+ risk) →
research_questions (cover every high-risk assumption) → [if flow-shaped] current_state_journey →
opportunities (per breakpoint) → feeds_intelligence rollup (incl. opportunity_hints).
```
