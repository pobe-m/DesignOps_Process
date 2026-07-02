# Intake Layer — Reference (Step 1.0, the hourglass waist)

Read this when turning **any product intent** into `brief.json`. Step 1+2 already reads a TOR; the
intake layer generalises the *input* so the pipeline body never changes. Everything downstream reads
`brief.json`, so as long as any intent normalises into it, the rest of the pipeline just works.

```
   TOR ─┐
   PRD ─┤
 one-line idea ─┤    ┌──────────────────────────────┐    ┌───────────────┐
 redesign target ─┼──►│ INTAKE: normalise → brief.json │ ─►│ pipeline body │ ─► prototype
 meeting notes ─┤    │  + set confidence floor        │    │  (unchanged)  │
 analytics ─┘        └──────────────────────────────┘    └───────────────┘
                          ↑ the ONLY place that generalises. Never fork the pipeline per input type.
```

**Intake stays THIN.** Its job is to *collect facts + name gaps*, not to synthesise. Personas, JTBD,
pains, and design directives are inferred **downstream** (2.3 / 2.5) where invariants guard the guessing.
If intake starts inventing JTBD, the hall-of-mirrors just moves upstream. Collect what's stated, infer
only what's safe, and mark the rest as an `open_question` — never fill a gap with a fabricated fact.

---

## Input taxonomy — richer input ⇒ higher confidence floor

Different intents arrive at different fidelity. Intake declares `meta.input_type` and sets
`meta.tor_confidence` (the brief's confidence floor) from how much is actually grounded:

| `input_type` | Fidelity | Pre-fills (as stated facts) | Confidence floor |
|---|---|---|---|
| `tor` / `prd` | high | features, flows, constraints, users, scoring | `high` if complete |
| `redesign` | high | + a real as-is (→ 2.3 `current_state_journey` can be evidence) | `high`/`medium` |
| `notes` | medium | fragments of goals/users/constraints | `medium` |
| `analytics` | medium | usage/priority signals (→ later test_findings evidence) | `medium` |
| `idea` (one line) | low | almost nothing — everything downstream is inference | **`low`** |
| `mixed` | varies | union of the above | lowest of its parts |

`meta.tor_confidence == "low"` ⇒ **`constrain_downstream`**: Steps 3/4 produce wireframe-level output
and force a human gate (don't mint an authoritative prototype from a one-line guess). This mirrors the
`constrain_downstream` flag in research (2.3) and intelligence (2.5).

> Naming note: the confidence field is `meta.tor_confidence` for back-compat even when the input isn't a
> TOR — read it as "brief confidence / intake confidence".

---

## The 4-way completeness gate (per required brief field)

"Ask before starting, skip if complete" is **not** binary. For every field `brief.json` needs, decide:

```
field required by brief.json:
  ├─ present in the input          → use it            (source: stated)          ✅ don't ask
  ├─ absent but safely inferable   → infer + open_question (mark it a guess)      ✅ don't ask
  ├─ absent + unguessable + PROTOTYPE-CRITICAL → 🙋 ASK (batch)                    ← ask only this bucket
  └─ absent + not critical (admin) → skip                                          ✅ don't ask
```

Result: intake asks **only** what is (a) needed to build a prototype **and** (b) can't be safely
inferred. A complete input → intake proceeds silently.

**Prototype-critical vs admin.** Only the first shapes a prototype — the second never does, so it's
dropped from the critical path (kept in `open_questions` if surfaced, never a blocking question):

| Prototype-critical (ask if unguessable) | Admin (never block on it) |
|---|---|
| the core problem / objective | budget · payment schedule |
| primary user segment(s) | file-format / deliverable checklist |
| the 1–2 must-do flows / features | contract milestones · sign-off process |
| platform (web/mobile) | ROI projections · procurement terms |
| accessibility target (if a duty applies) | team / committee structure |

(This is the Seven Peaks brief question bank, trimmed to what changes the prototype.)

---

## Batch clarifying protocol (fast path)

1. **Compute the gap set first** — run the 4-way gate over every required field; keep only the
   `ASK` bucket (critical + unguessable).
2. **Fire once, grouped** — present that bucket as a single batch, grouped by section (Foundation /
   Users / Platform-a11y). The user answers in one pass.
3. **Every question is skippable** — "skip / don't know" → the field becomes `null` + an
   `open_questions` entry (inferred downstream). Momentum over completeness.
4. **One follow-up round max** — if answers open a *new* critical gap, ask once more, then stop.
   This keeps a batch from degrading into an endless conversation.
5. **Ask to sufficiency, not completeness** — the moment the brief is buildable, proceed.

> Implementation: the batch maps cleanly onto the host's multi-question prompt (ask several, each
> selectable or free-text, answered in one pass).

---

## What intake writes into `brief.json`

Intake produces the same `brief.json` Step 1+2 always did, plus these honesty signals in `meta`:

```jsonc
"meta": {
  "project_name": "", "generated_at": "ISO-8601",
  "source_file": "",            // the intent's origin: a path, a URL, or "conversation"
  "input_type": "tor|prd|redesign|notes|analytics|idea|mixed",   // NEW — what came in
  "tor_confidence": "high|medium|low",   // the confidence floor (see taxonomy); low ⇒ constrain_downstream
  "intake": {                   // NEW — the audit trail of the gate (optional but recommended)
    "asked": ["primary user segment", "platform"],   // fields the user was asked
    "inferred": ["success_metrics"],                 // fields intake guessed (each has an open_question)
    "skipped": ["budget", "file_formats"]            // admin fields dropped from the critical path
  }
}
```

Every inferred field must have a matching `open_questions` entry (impact `blocker`/`important`/
`nice-to-know`). A `null` field is honest; a fabricated one is not.

---

## Honesty rules (carried by validate_brief.py where checkable)

| Rule |
|---|
| Never invent a fact to fill a gap — absent + unguessable + not asked ⇒ `null` + an `open_questions` entry |
| `meta.input_type` (when present) ∈ {tor, prd, redesign, notes, analytics, idea, mixed} |
| a thin input (`input_type: idea` / sparse) ⇒ `tor_confidence` must be `low` (→ `constrain_downstream`) — don't claim high confidence from one line |
| admin content (budget/procurement/committee) is dropped or parked in `open_questions`, never a blocking question |

---

## Generation prompt (agent reads *any* product intent → writes `brief.json`)

```text
You are running INTAKE — the hourglass waist. INPUT: any product intent (a TOR, a PRD, a one-line
idea, a redesign target, notes, analytics). OUTPUT: brief.json (facts) per Step 1+2's shape.

1. DETECT & DECLARE. Set meta.input_type and, from how much is actually grounded, meta.tor_confidence
   (see the taxonomy — a one-line idea is LOW → constrain_downstream). Set meta.source_file to the origin.
2. STAY THIN. Extract only stated facts. Do NOT synthesise personas/JTBD/pains — that is 2.3/2.5's job.
3. RUN THE 4-WAY GATE per required field: present → use; safely inferable → infer + an open_question;
   critical + unguessable → ASK (batch, grouped, skippable); admin → skip. Ask ONLY the critical+unguessable
   bucket, once (one follow-up round max). Ask to sufficiency, not completeness.
4. NEVER FABRICATE. An unknown critical field you didn't ask about is null + an open_question, not a guess.
5. DROP ADMIN. Budget / file formats / procurement / committee structure never block — omit or park them.
6. RECORD THE TRAIL in meta.intake { asked, inferred, skipped }.

Process: detect input_type → set confidence floor → gate every field → batch-ask the critical gaps →
write brief.json (facts + open_questions) → hand off to Step 2.3.
```
