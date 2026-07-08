# Phe-estimator — Peer-Review Matrix

*The structured review instrument the README calls **CRITICAL** before wider testing.*

The phe-estimator Skill now runs and is scored on the public benchmark. This matrix turns
"is it ready?" into specific, assignable review tasks tied to real test cases — so parents,
dietitians, clinicians, and AI developers each review the part they are qualified to judge,
and every finding lands on the record.

It is Layer 1 (cited, reviewer-of-record) of the [peer-review model](../docs/PEER-REVIEW.md)
applied to the estimator; the benchmark is Layer 2 (measured). This document connects them.

---

## Where the Skill stands today (test set `seed_v0`, 18 cases)

| Estimator | MAE (mg) | Within band | What it is |
|---|---:|---:|---|
| Deterministic rubric (`rubric_estimator`) | 12.76 | 83.3% | The rubric encoded in Python — the reproducible reference |
| **Claude Skill (`claude_skill`, live LLM)** | **23.57** | **50.0%** | The Skill following that rubric via the model |

The gap between the two is the review-and-optimization target: it is how much precision the
live model loses by applying the pinned rubric loosely. **The matrix below is how we close it
without adding confidence/band chatter.**

---

## Review dimensions × reviewer roles

Each cell is a concrete question for a specific reviewer, with the evidence to look at.

### 1. Methodology review — *parents, dietitians, clinicians*

Is the **rubric itself** right? (Not the code — the method.)

| # | Question | Evidence to review | Sign-off |
|---|---|---|---|
| M1 | Is the **≤ 2 g protein / serving** "countable" gate the right threshold and correctly framed as a parsing focus, not a suitability ruling? | `SKILL.md` step 1; README "Is this food potentially suitable" | ☐ |
| M2 | Is the **recipe-factor** procedure (weight shares from ingredient order + declared protein + cooking sense) how the clinic teaches parents to estimate? | `SKILL.md` step 4; `PLAN.md` rubric | ☐ |
| M3 | Is the **whole-food path** (no protein panel → estimate from each food's phe) a valid fallback, and does it match how a parent handles a fruit salad? | `SKILL.md` step 4-W | ☐ |
| M4 | Are the **protein-source classes** and their phe-per-gram values clinically sensible? | `phe_per_g_protein.json` (each row carries its basis) | ☐ |
| M5 | Is "**one number, no confidence bands**" the right output discipline for how counting is actually done at home/clinic? | `SKILL.md` hard rules | ☐ |

### 2. Output testing — *parents, dietitians*

Does the Skill produce **trustworthy numbers** on real labels?

| # | Question | Evidence to review | Sign-off |
|---|---|---|---|
| O1 | On single whole foods, are estimates close enough to be usable? Cases the Skill **missed**: **c05 strawberries** and **c09 tomato** (over-estimated), **c03 carrots** and **c06 broccoli** (under-estimated). Under-counts are the clinically riskier direction. | `results/claude_skill_v0.json`; table below | ☐ |
| O2 | On composite recipes, are estimates usable? Skill **missed** **c12, c14, c15** (under-estimated) and **c16** badly. | same | ☐ |
| O3 | Bring a **real label from your own pantry**, run it, and judge the number against what you'd count by hand. Report label + Skill output + your hand count. | your labels → new test cases | ☐ |
| O4 | Where the Skill and the deterministic rubric **disagree most** — by gap: **c16** (293 mg, the worst), **c14** (49), **c06** (45), **c12** (32), **c15** (27) — which estimator is closer to reality, and why? | table below | ☐ |

### 3. Reliability engineering — *AI developers*

Can the Skill be made to **follow the rubric precisely and repeatably**?

| # | Question | Evidence to review | Sign-off |
|---|---|---|---|
| R1 | **Determinism.** On this run one composite (**c11**) was *refused* while its siblings estimated — same rubric, different behavior. Reduce run-to-run variance. | `results/claude_skill_v0.json` (c11 error) | ☐ |
| R2 | **Rubric fidelity.** The Skill's 23.57 vs the rubric's 12.76 means the model deviates from the steps. Tighten the prompt so it applies step 4 as written — **without** adding hedging language. | both result JSONs; `SKILL.md` | ☐ |
| R3 | **The c16 failure** (rice+carrot bowl: rubric 332, Skill 39, truth 196) is the recipe-factor weight-share problem. Improve share estimation; this is where scale + food-list data plug in. | case c16 | ☐ |
| R4 | **Regression safety.** Confirm every change is gated: `run_benchmark.py --baseline results/baseline_v0.json` must fail the merge if MAE rises. | `run_benchmark.py`; CI | ☐ |
| R5 | **No answer-key leakage.** Confirm the adapter never reads `expected_phe_mg` / `ground_truth`. | `estimators/claude_skill.py`; `base.py` `label_view` | ☐ |

---

## Per-case evidence (both estimators, seed_v0)

`P` = within tolerance band `max(15 mg, 15% of truth)`; `F` = outside. Bold rows are where a
reviewer's eye is most useful.

| id | food | truth mg | rubric mg | R | Skill mg | S | note for reviewers |
|---|---|---:|---:|:--:|---:|:--:|---|
| c01 | Banana | 57.8 | 42.6 | F | 47.8 | P | class-avg vs banana's specific ratio |
| c02 | Apple | 12.6 | 16.2 | P | 24.5 | P | |
| **c03** | Carrots | 51.9 | 37.9 | P | 32.8 | **F** | Skill under-estimates |
| c04 | Cucumber | 31.0 | 28.3 | P | 32.5 | P | |
| **c05** | Strawberries | 27.4 | 31.7 | P | 48.0 | **F** | Skill over-estimates ~75% |
| **c06** | Broccoli | 106.5 | 123.4 | F | 78.5 | F | both miss; opposite directions |
| c07 | Cornstarch | 1.0 | 1.0 | P | 0.0 | P | |
| c08 | Tapioca | 1.2 | 2.7 | P | 0.3 | P | |
| **c09** | Tomato | 32.4 | 35.0 | P | 53.0 | **F** | Skill over-estimates |
| c10 | White rice | 158.8 | 149.5 | P | 148.5 | P | |
| **c11** | Fruit salad | 46.4 | 41.3 | P | ERR | **F** | Skill *refused* (determinism, R1) |
| **c12** | Carrot+cucumber | 69.0 | 76.5 | P | 45.0 | **F** | Skill under-estimates |
| c13 | Apple sauce | 9.7 | 10.4 | P | 16.0 | P | |
| **c14** | Tomato+broccoli | 102.6 | 102.6 | P | 54.0 | **F** | Skill under by half |
| **c15** | Banana-strawberry | 77.8 | 79.8 | P | 52.5 | **F** | Skill under-estimates |
| **c16** | Rice+carrot bowl | 196.1 | 332.4 | F | 39.0 | **F** | worst case; recipe-factor problem (R3) |
| c17 | Tapioca pudding | 18.1 | 11.0 | P | 17.0 | P | |
| c18 | Cucumber+tomato | 58.4 | 59.3 | P | 44.0 | P | |

---

## How to record a review (reviewer of record)

1. Pick a row (M/O/R item above). Put your name, role, and date on it.
2. File your finding as a GitHub issue labeled `peer-review` **or** submit via the feedback
   form on the [families](../docs/families.html) / [clinicians](../docs/clinicians.html) page.
3. A finding becomes a **test case** (new label + hand-counted phe), a **rubric change**
   (with clinician sign-off), or a **reliability fix** (with a benchmark delta). Each is
   linked back to this matrix so the audit trail is complete.

## Definition of "ready for wider testing"

- [ ] M1–M5 signed off by at least one clinician/dietitian **and** one parent.
- [ ] O3 done by ≥ 3 reviewers with their own labels (grows the test set beyond 18).
- [ ] R1 (determinism) and R4 (regression gate) verified by a developer.
- [ ] The Skill's within-band % on `seed_v0` beats the deterministic rubric's 83.3%, or the
      gap is understood and documented.
