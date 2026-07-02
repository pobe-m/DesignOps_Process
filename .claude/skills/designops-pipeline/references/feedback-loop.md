# Feedback Loop — Reference (Step 4.9, prototype → test → prototype N+1)

Read this when turning test feedback into `test-findings.json` — the artifact that decides what
changes in the **next** prototype. This is what makes the pipeline a loop, not a one-shot: build → test
→ score feedback → fix the ones that matter → build again, until it converges.

```
Prototype N ─test─► feedback ─► [de-solutionise] ─► score(severity × reach × confidence)
   ▲                                                        │
   │                        ┌── fix_now (top-N) ────────────┤
   └──── Prototype N+1 ◄────┘                               ├── backlog / won't_fix
                    ▲                                        └── grade prior hypotheses
                    └── converged? ─no─► loop / ─yes─► ship
```

**Real feedback is evidence — the one thing the synthetic front-end isn't.** A finding that comes from a
real user is the ground truth that upgrades an upstream hypothesis `inferred → evidence`. So this layer is
where the Discover/Define guesses (research 2.3, interview 2.3b, scenario edges 2.5b) finally get graded.

---

## Three rules

1. **Signal vs noise — a real problem is not one person's quirk.** Judge each finding on three signals,
   not a raw headcount: **convergence** (did several people hit it independently?), **breadth** (does it
   cross segments?), and **prior hypothesis** (does it confirm a pain we already guessed?). That yields a
   `verdict`: `systemic` (cross-segment) · `segment` (real but scoped to one segment) · `individual` (n=1).
2. **Observed beats stated; problem beats solution.** Behaviour ("I couldn't finish X") outranks opinion
   ("I'd prefer blue") — `type:"observed"` carries more weight than `type:"stated"`. And feedback usually
   arrives as a *solution* ("add a back button"); **de-solutionise** it into the underlying problem
   ("I lost track of where I was") before scoring — you fix the problem, not the user's guess at a fix.
3. **Fix to a budget, converge to an exit.** Don't fix everything: score, sort, take the top-N per round,
   backlog the rest. Stop the loop when the round's top findings are all cosmetic/minor, or when new
   findings dry up (`dry_rounds ≥ 2`) — endless polishing is its own failure.

---

## Scoring

```
priority_score = severity × reach × confidence_weight
```
| Factor | Scale |
|---|---|
| `severity` | blocker `3` · major `2` · minor `1` · cosmetic `0` (cosmetic → score 0 → never fix_now) |
| `reach` | number of distinct **segments** affected (≥1) — cross-segment scores higher than louder-but-narrower |
| `confidence_weight` | high `3` · med `2` · low `1` (an `observed` finding is usually high; `stated` rarely so) |

`decision` (`fix_now` / `backlog` / `wont_fix`) follows the score against the round's budget — high score
in-budget → `fix_now`; everything else waits. A `fix_now` names the `target_iteration` it lands in.

---

## `test-findings.json` shape

```jsonc
{
  "meta": { "iteration": 1, "prototype_ref": "output/prototype@v1", "generated_at": "ISO-8601",
            "schema_version": "1.0",
            "test_method": "real_user|simulated_4.8|hybrid",   // real_user feedback is EVIDENCE; simulated_4.8 stays a hypothesis
            "convergence": { "new_this_round": 4, "dry_rounds": 0 } },   // dry_rounds ≥ 2 ⇒ converged, stop

  "findings": [{
    "id": "FD01",
    "raw": "<what the tester said/did, verbatim>",
    "type": "observed|stated",                 // observed (behaviour) > stated (opinion)
    "problem_statement": "<de-solutionised: the underlying problem, not the user's proposed fix>",
    "maps_to": "PP01",                          // a prior hypothesis this confirms (research/interview id), or null
    "severity": 2, "reach": 2, "confidence": "high",
    "priority_score": 12,                       // = severity × reach × confidence_weight (validated)
    "verdict": "systemic|segment|individual",   // systemic ⇒ reach ≥ 2
    "decision": "fix_now|backlog|wont_fix",     // fix_now ⇒ target_iteration set
    "target_iteration": 2,
    "participant_ref": "R03" }]
}
```

`fix_now` findings feed the next round: they become `opportunities` / brief updates (progressive
enrichment) that Prototype N+1 is built from; a finding whose `maps_to` resolves to a prior hypothesis
**upgrades that item `inferred → evidence`** upstream (real contact finally grounds the guess).

---

## Honesty / structural invariants (hard fails)

| Rule |
|---|
| `type ∈ {observed, stated}`; `verdict ∈ {systemic, segment, individual}`; `decision ∈ {fix_now, backlog, wont_fix}`; `confidence ∈ {high, medium, low}` |
| `severity` ∈ 0..3; `reach` is an int ≥ 1 |
| `priority_score` == `severity × reach × confidence_weight` (high 3 / medium 2 / low 1) — the score can't be hand-waved |
| `verdict == "systemic"` ⇒ `reach ≥ 2` (a systemic problem crosses segments; a 1-segment claim isn't systemic) |
| `decision == "fix_now"` ⇒ `target_iteration` set and `> meta.iteration` |
| `problem_statement` non-empty (a finding with no stated problem can't be acted on) |
| `test_method == "simulated_4.8"` ⇒ findings are HYPOTHESES, not evidence — don't upgrade upstream confidence from them |

**Warnings (quality):** a `problem_statement` that reads like a solution ("add …", "make it …") —
de-solutionise it; a `verdict:"individual"` marked `fix_now` (fixing an n=1 quirk); a `severity:0`
(cosmetic) marked `fix_now`; `dry_rounds ≥ 2` (converged — consider shipping).

> Validated by `scripts/validate_test_findings.py` (pass `research.json` as the 2nd arg to resolve
> `maps_to` into a real pain/opportunity id and confirm the hypothesis actually exists).

---

## Generation prompt (agent reads test feedback [+ research.json] → writes test-findings.json)

```text
You are triaging test feedback into the next prototype's work-list. INPUT: raw test feedback (real-user
notes, or the 4.8 simulated usability output) + research.json. OUTPUT: test-findings.json per the shape.

1. DECLARE test_method. real_user = evidence; simulated_4.8 = hypothesis (don't upgrade upstream from it).
2. DE-SOLUTIONISE every item: write the underlying problem, not the user's proposed fix.
3. CLASSIFY observed vs stated (behaviour outranks opinion).
4. JUDGE signal: convergence + breadth + prior hypothesis → verdict (systemic needs reach ≥ 2).
5. SCORE: priority_score = severity × reach × confidence_weight. Sort; take the top-N in budget as
   fix_now (set target_iteration); backlog the rest. Never mark cosmetic or n=1 individual as fix_now.
6. GRADE HYPOTHESES: when a real-user finding maps_to a prior pain/opportunity, note it — that upgrades
   the upstream item inferred → evidence.
7. TRACK CONVERGENCE: new_this_round + dry_rounds; dry_rounds ≥ 2 ⇒ recommend shipping.

Process: de-solutionise → classify → judge verdict → score → decide fix_now/backlog against the budget →
set target_iteration → roll fix_now into the next brief/opportunities.
```
