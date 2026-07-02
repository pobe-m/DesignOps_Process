# Interview + Affinity Layer — Reference (Step 2.3b)

Read this when generating `interviews.json`. It sits **after Step 2.3 personas, before pain
synthesis** — it is the *documented reasoning trace* for how pains are derived. An AI role-plays each
persona through a tailored interview, the answers are clustered into an affinity map, and the map
feeds `pain_points` / `opportunities` back into `research.json`. It runs the **Empathize → Define**
move of the Double Diamond.

**Simulated by design — and it says so.** An AI pipeline cannot interview real people. Role-playing a
persona to "answer" questions is **not evidence** — the answers can contain no fact that wasn't already
in the brief/persona. Its value is *forced elaboration* (turning an abstract persona into concrete
behaviour), *surfacing implicit assumptions/contradictions*, and *producing a real interview script you
can later run on humans*. So the whole layer inherits the honesty discipline of the Usability Test layer
(Step 4.8): `meta.not_real_user_data` and every response's `simulated` **must be `true`**, and confidence
is capped at `medium` — never `high`.

**Three rules:**
1. **Never pass simulation off as research.** `not_real_user_data:true`, `simulated:true` on every
   response, `overall_confidence ∈ {low, medium}`, and `limitations` non-empty. The affinity insights
   are **hypotheses**, not findings.
2. **Trace or it doesn't count.** Every `simulated_responses[].traces_to` must name what the answer is
   grounded in (a persona field, a `pain_points`/`jobs_to_be_done` id, or a `brief` feature/flow id).
   An answer that traces to nothing is invention, not elaboration.
3. **Anti-circular gate.** An affinity insight that just restates one persona is a hall-of-mirrors echo.
   Each insight needs `supporting_quotes` from **≥2 distinct questions**, and every `pain_ref` it raises
   should map back to a real pain (or spawn a `research_question` to validate with humans).

> Validated by `scripts/validate_interviews.py` (pass `research.json` as the 2nd arg to resolve
> `persona_ref`/`pain_ref` across files). Feeds `research.json` — affinity `pain_ref` become
> `pain_points`, high-value insights become `opportunities`.

---

## `interviews.json` shape

```jsonc
{
  "meta": { "source_brief": "output/brief.json", "source_research": "output/research.json",
            "generated_at": "ISO-8601", "schema_version": "1.0",
            "evidence_mode": "inferred|hybrid|evidence_backed",
            "not_real_user_data": true,       // MUST be true
            "simulated": true,                // MUST be true
            "gate_rounds_used": 1,            // how many probe → reprobe rounds the quality gate ran (cap ~3)
            "overall_confidence": "low|medium",  // capped — simulated interviews never claim 'high'
            "limitations": ["no real participants — answers are role-played from the persona + brief"],
            "human_reviewed": false },

  // one script per persona — 6–10 questions, grouped by theme, marked universal vs role-specific
  "interview_scripts": [{ "persona_ref": "P01",
    "questions": [{ "id": "Q01", "theme": "motivation|pain|behavior|tools|goal",
                    "scope": "universal|role_specific", "text": "" }] }],

  // the AI, in character, answers each question — labelled simulated, traced to its grounding
  "simulated_responses": [{ "persona_ref": "P01", "question_ref": "Q01",
    "answer": "", "quote": "<one quotable line>",
    "traces_to": ["personas[0].frustrations", "PP01", "F03"],   // persona field / research id / brief id
    "simulated": true }],

  // cluster the quotes into themes — the affinity map
  "affinity_map": [{ "id": "AF01", "theme": "", "insight": "",
    "supporting_quotes": ["Q01", "Q07"],      // ≥2 distinct questions (anti-circular)
    "personas_covered": ["P01", "P02"],
    "pain_ref": ["PP01"],                     // pains this theme maps to (→ research.json)
    "confidence": "low|medium",               // capped — simulated
    "research_question": "" }],               // how a human would validate this insight

  // the quality gate's audit trail: each round either passes or re-probes with sharper questions
  "gate_log": [{ "round": 1, "verdict": "pass|reprobe", "reason": "" }]
}
```

The affinity map is the **seam** back into `research.json`: `pain_ref` → `pain_points`, high-signal
insights → `opportunities` (with the same honesty labels). Because everything here is simulated, it can
only *raise questions* and *shape hypotheses* — real evidence still arrives later, from the build → test
loop, and upgrades these items `inferred → evidence`.

---

## The quality gate (why the loop exists)

The gate checks the **right** thing — not "does the answer sound good" but:

| Gate check | Rejects |
|---|---|
| Every answer `traces_to` a persona field / research id / brief id | fabrication (answer from nowhere) |
| Each answer **decomposes** the persona into something concrete, not a paraphrase of it | circular / hall-of-mirrors |
| Each affinity insight has `supporting_quotes` from ≥2 distinct questions | a theme resting on one echo |
| No insight is 100% one persona when multiple personas exist | segment-biased insight |

**Loop:** answer → analyse insight → if (circular) or (not affinity-mappable) → **rewrite the questions
sharper / from another angle** → re-role-play → repeat. **Cap at ~3 rounds** (`gate_rounds_used`); if it
still won't converge, record the gap as a `research_question` instead of forcing it.

---

## Honesty invariants (hard fails)

| Invariant |
|---|
| `meta.not_real_user_data == true` **and** `meta.simulated == true` |
| every `simulated_responses[].simulated == true` |
| `meta.overall_confidence ∈ {low, medium}` and every `affinity_map[].confidence ∈ {low, medium}` — simulated never claims `high` |
| `meta.limitations` is non-empty |
| every `simulated_responses[].traces_to` is non-empty |
| every `question` id is unique; `theme`/`scope` are valid enums |
| every `simulated_responses[].question_ref` resolves to a question id |
| every `affinity_map[].supporting_quotes` entry resolves to a question id; `personas_covered` non-empty |
| when `research.json` is provided ⇒ every `persona_ref` resolves to a persona id, and **every primary persona has ≥1 interview_script** (you interview every user) |
| when `research.json` is provided ⇒ every `affinity_map[].pain_ref` resolves to a `pain_points` id |

**Warnings (quality, not blocking):** an insight with `supporting_quotes` from <2 questions; a script
with <6 questions; `gate_rounds_used > 3` (the gate never converged — treat the output as low-confidence).

---

## Generation prompt (agent reads `brief.json` + `research.json` → writes `interviews.json`)

```text
You are a Senior UX Researcher running a SIMULATED interview + affinity pass. You do not assume; you use
only what's in brief.json + research.json. You know this is role-play, not real research — label it so.

1. SCRIPT PER PERSONA. For each persona, write 6–10 open-ended, unbiased questions grouped by theme
   (motivation / pain / behavior / tools / goal). Mark each universal vs role-specific.
2. ROLE-PLAY, IN CHARACTER. Answer each question AS that persona, grounded in their fields + the brief.
   Give one quotable line. traces_to MUST name the persona field / research id / brief id it rests on.
   Never invent a fact that isn't implied by the inputs.
3. RUN THE GATE (before affinity). Re-read the answers: any answer that only paraphrases the persona
   (circular) or traces to nothing? Rewrite that question sharper / from another angle and re-answer.
   Log each round in gate_log. Cap at 3 rounds; unresolved → a research_question, not a forced answer.
4. AFFINITY MAP. Cluster the quotes into 5–7 themes. Each insight cites supporting_quotes from ≥2
   distinct questions and names the pains it maps to. Confidence ≤ medium (this is simulated).
5. BE HONEST. not_real_user_data:true, simulated:true, overall_confidence ≤ medium, fill limitations.

Process: scripts (per persona) → simulated_responses (in character, traced) → gate loop (until
affinity-mappable or capped) → affinity_map → hand pain_ref/insights back to research.json.
```

**Self-critique sub-prompt (run before writing the file):**
```text
Re-read the draft:
- Any answer that adds a fact not in brief.json/research.json? (fabrication — cut or trace it)
- Any insight that is one persona echoed back? (circular — needs a 2nd distinct quote or drop it)
- Any primary persona with no script? (coverage gap)
- Is overall_confidence honestly ≤ medium, limitations non-empty?
Fix, or move the uncertainty into a research_question and lower confidence.
```
