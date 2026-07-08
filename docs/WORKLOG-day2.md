# Work log — Day 2 (2026-07-08)

What we did this session, in order, and why. This is the audit trail behind the Day-2 artifacts;
it exists so a reviewer (or future maintainer) can reconstruct the reasoning without reading the
chat. Every number here is reproducible from `benchmark/` on the public seed set.

## The question we started with

Day 1 built the skeleton — a phe-estimator Skill, a benchmark harness, a food list, a two-layer
peer-review model. The Day-2 question was **not** "is it done?" It was: *is there a reliability
problem that every phe-estimator app shares, and can we state it cleanly enough that an
experienced AI developer can act on it?* A pharmaceutical company has declined to ship its phe
estimator over precision; small developers ship anyway because families have nothing else. We
wanted to name the shared problem, not shame anyone.

## What we found, and the reframe

The first framing — "the gap between an LLM Skill and a deterministic version of the same
method" — is real but is only **one** of the reliability problems, not the root. Pushing on it
surfaced a structural fact:

> **Phenylalanine is never on a nutrition label. Protein is.** Every estimator infers phe from
> protein, and (a) the phe-per-gram-of-protein ratio varies ~3× by food source, while (b) the
> label rounds protein exactly in the very-low-protein range PKU lives in. For all 9
> single-ingredient seed foods, the band of phe values *consistent with the label alone* is wider
> than the clinical tolerance band.

The important move was to **not** treat that as a dead end. The label ceiling is not a tombstone;
it is an engineering map. It says precisely where precision has to come from something *other than
the label* — which is what the food list (cited external lookup) and a connected scale (measured
weight) are for. What remains after those two routes is the one genuinely open problem.

## The decomposition: four reliability gaps

We split "the app feels unreliable" into four named, independently-measurable gaps, each owned by
a specific repo component, each with a concrete ask. (Full detail: `docs/RELIABILITY.md`.)

| Gap | Plain statement | Known route to a fix? | Owner |
|---|---|---|---|
| G1 conversion | phe-per-protein ratio varies by food | **yes** — cited class table / food list | `phe_per_g_protein.json` + food list |
| G2 label rounding | label rounds protein in PKU's range | **yes** — look phe up in the food list instead | food list as external lookup |
| G3 recipe-factor | guess ingredient weight-shares in a mixed food | **no known route** — this is the ask | estimator heuristic |
| G4 execution variance | same model, same food, different answer | **yes** — prompt/method discipline | `SKILL.md` |

**G3 is the marquee ask.** G1 and G2 have known routes (food list); G4 is prompt discipline;
portion weight is a scale. G3 — inferring hidden proportions from a short, rounded description — is
the largest error source *and* has no known method that beats a naive baseline. It is also the
most transferable: the same shape recurs far beyond PKU, so a method that measurably wins here is
reusable anywhere.

## What we measured (all on `seed_v0`, 18 cases, USDA FDC ground truth)

- **Deterministic rubric** (`rubric_estimator`, the 7-step method as plain Python): MAE **12.76
  mg**, 83.3% within tolerance, identical every run. This is the reproducible reference/floor.
- **Live Claude Skill** (`claude_skill`, `claude-opus-4-8`, same rubric applied by the model):
  five runs on identical inputs scored MAE **25.2 / … / 34.2 (mean 27.7, stdev 3.3)**, within-band
  **38.9–55.6%**. The spread *is* G4.
- **Mean live-Skill error by gap:** G2 ~11 mg, G1 ~22 mg, **G3 ~53 mg (dominant)**.
- The run-to-run instability is concentrated in (but not exclusive to) the G3 multi-ingredient
  cases — the tomato-broccoli medley swung 5→49 mg across identical runs.

## What we built this session

1. **Benchmark integrity pass.** The old `claude_skill` result file was hand-assembled and did not
   conform to the harness schema. Regenerated it live through `run_benchmark.py` with the real
   model id recorded, so the headline number is reproducible rather than asserted.
2. **The gap decomposition + figure** (`docs/RELIABILITY.md`, `docs/assets/reliability_gaps.png`,
   `benchmark/results/gap_analysis.json`).
3. **Food-list foundation** — `food-list/foods.json` (11 cited rows) + `foods.schema.json` +
   a shared dependency-free loader `foodlist.py` with a Layer-1 validation gate. The rubric
   estimator now reads from this single source; verified numerically identical (MAE still 12.76).
4. **Contributor on-ramp** — `CONTRIBUTING.md` (pick a gap → improve → prove → PR), a copy-me
   `benchmark/estimators/template_estimator.py`, and a CI workflow
   (`.github/workflows/benchmark.yml`) that runs the food-list validation + a regression gate on
   every relevant PR.
5. **Reproducibility meter** — `benchmark/variance.py`, a standalone tool that runs any estimator
   N times and reports the spread of its score (this is how G4 is measured). It reads estimator
   output only; it changes no estimate. Deterministic estimators report range 0.

## Decisions worth remembering

- **Terminology:** "reliability gap," not "seam" (jargon). The vocabulary throughout is
  reproducible / harness-generated / cited / measured — never "honest" (which implies the
  alternative).
- **Leaderboard ranking:** generalizing estimators are ranked by MAE; the memorizing stub is
  listed *unranked* as a floor because its score does not generalize to unseen labels. The
  deterministic rubric is therefore the estimator to beat.
- **No confidence bands.** The Skill contract forbids hedging/confidence language; the fix for G4
  is reproducibility, not caveats. Accuracy is measured externally by the benchmark, never
  self-graded.
- **Scope we deliberately did not touch:** food labels themselves (not ours to change), regulatory
  classification (addressed in its proper sphere), and the estimator's internal packaging
  (a separate, larger task if pursued).

## Open threads

- **G3 is the community ask.** No known method beats naive weight-shares from the label alone.
- Expand the seed set beyond 18 cases; the gap magnitudes are directionally solid but will firm up.
- Unify the two food-data files (`benchmark/testset/food_reference.json` ground truth vs
  `food-list/foods.json` knowledge) behind one fetch path.
- Add Open Food Facts branded rows to exercise the G2 lookup path.
