# Phe-estimator Skill — build plan

**Goal:** a working Claude Skill that applies the label rubric exactly and returns a single
phe estimate for a portion, scored on the public benchmark. Working *first*; optimized
*after*.

This plan is deliberately narrow. The failure mode we are designing against is the one the
maintainer hit building her own estimator: efficiency changes silently trading away
precision, and confidence/band "chatter" pulling the model off the rubric. Every decision
below serves **precision + rubric-fidelity first**.

---

## The contract (what the Skill does — and does not do)

**Input:** a nutrition label — serving size (g), protein per serving (g), ingredients list
(text) — and a portion the user actually ate (g, or "1 serving").

**Output:** exactly one object:

```json
{
  "phe_mg": 42.0,
  "recipe_factor_mg_per_serving": 30.0,
  "portion_g": 168,
  "serving_size_g": 120,
  "ingredients_considered": [
    {"name": "wheat flour", "phe_source_class": "cereal protein", "est_share": 0.7},
    {"name": "sugar", "phe_source_class": "none", "est_share": 0.0}
  ]
}
```

- `phe_mg` = `recipe_factor_mg_per_serving × (portion_g / serving_size_g)`.
- The breakdown is the Skill's **working shown**, so a human reviewer can check the recipe
  factor. It is transparency, not hedging.

**The Skill does NOT:**

- emit confidence intervals, probability ranges, error bars, or "±" values;
- soften the answer with qualifier language ("roughly", "about", "hard to say");
- add, skip, or reorder rubric steps, or invent an alternative method;
- decide whether a food is *safe for a person* (that is a clinical decision, not ours);
- read or infer the benchmark's ground-truth answer.

If a label genuinely can't be parsed (missing ingredients list, unreadable panel), the Skill
says so plainly and stops — it does not guess a number to appear helpful.

---

## The rubric (pinned — implementations must not alter it)

Trained-by-the-clinic method, in strict order:

1. **Countable?** Is protein **≤ 2 g per serving**? This gates label parsing so we optimize
   the "countable" range that matters to the diet. (Not a suitability ruling for any person.)
2. **Find phe-bearing ingredients.** Read the ingredients list; identify items that carry phe.
3. **Classify each by protein source** for a phe-per-gram basis (cereal, dairy, legume,
   vegetable, etc.). This is where the food list / knowledge graph raises reliability.
4. **Estimate the recipe factor.** Judge the relative weights of the phe-bearing ingredients
   across the whole labeled recipe, using ingredient order, declared protein total, and basic
   cooking science. This is the irreducible estimation step — the goal of the technical work
   (food list, scale data) is to *narrow this guesswork*, never to remove the step.
5. **Scale to the panel serving** → `recipe_factor_mg_per_serving`.
6. **Scale to the portion eaten** → `phe_mg`.
7. **Return the number and the working.** Log it.

> Any implementation, optimization, or prompt revision is measured against this rubric. If a
> change makes the Skill deviate from these steps, it is wrong — even if it is faster.

---

## Build steps

- [x] **1. Author `SKILL.md`.** Encode the contract + rubric above as the Skill instructions.
  Bias the wording toward determinism: explicit ordered steps, explicit output schema, an
  explicit "do not emit confidence/bands" instruction. Keep reasoning bounded so the model
  does the rubric, not free-form analysis.
- [x] **2. Minimal phe-per-gram reference.** A small, cited table of phe-per-gram by protein
  source class (seeded from the [food list](../food-list/) work and USDA nutrient 508), so
  step 3 is a lookup, not a recollection. Start with the classes the seed test set exercises.
- [x] **3. Recipe-factor procedure.** Write the concrete heuristic for step 4 (how ingredient
  order + declared protein + cooking sense combine into relative weights). Document its
  assumptions so it is reviewable by dietitians.
- [x] **4. Harness adapter** (`../benchmark/estimators/claude_skill.py`). Wrap the Skill's
  output in `estimate(case) -> {"phe_mg": ...}`. Single integration point; no benchmark peeking.
- [x] **5. Score & baseline.** Run against `seed_v0.jsonl`; record MAE / within-band% as the
  Skill's first leaderboard row and save the run JSON as the regression baseline.
- [ ] **6. Peer-review matrix.** Once it scores, generate the review matrix (methodology /
  output-testing / reliability) for parents, dietitians, clinicians, and AI devs — the
  maintainer's explicit "CRITICAL" gate before wider testing.

## Only after it works: optimization (separate phase)

Efficiency, caching, offline/low-bandwidth handling (weak grocery-store WiFi), token cost.
**Every optimization is gated by the benchmark** (`run_benchmark.py --baseline`): if it moves
MAE up or within-band% down, it does not merge. That is how we get to be clever without
paying in precision.

---

## Definition of done (v1)

1. `SKILL.md` encodes the contract + rubric; output is one number + working, no bands.
2. The adapter scores the Skill on `seed_v0.jsonl` and it lands a leaderboard row.
3. A baseline run JSON is saved so every later change is regression-gated.
4. The peer-review matrix is generated for clinician/dietitian/parent/dev review.
