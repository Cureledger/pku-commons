# Work log ,  Day 2 (2026-07-08)

What we did this session, in order, and why. This is the audit trail behind the Day-2 artifacts.
It lets a reviewer or future maintainer reconstruct the reasoning without reading the chat. Every
number here is reproducible from `benchmark/` on the public seed set.

## The question we started with

Day 1 built the skeleton: a phe-estimator Skill, a benchmark harness, a food list, a two-layer
peer-review model. The Day-2 question was whether there is a reliability problem that every
phe-estimator app shares, and whether we can state it cleanly enough for an experienced AI
developer to act on it. A pharmaceutical company has declined to ship its phe estimator over
precision. Small developers ship anyway because families have nothing else. We wanted to name the
shared problem plainly, without pointing fingers at any one company or developer.

## What we found, and the reframe

The first framing, "the gap between an LLM Skill and a deterministic version of the same method,"
is real. It is one of several reliability problems. The root cause runs deeper, in a structural
fact:

> **Phenylalanine never appears on a nutrition label. Protein does.** Every estimator infers phe
> from protein. The phe-per-gram-of-protein ratio varies about threefold by food source, and the
> label rounds protein exactly in the very-low-protein range where PKU management happens. For
> all 9 single-ingredient seed foods, the band of phe values consistent with the label alone is
> wider than the clinical tolerance band.

That limit turns out to be useful. The label ceiling functions as an engineering map. It marks
exactly where precision has to come from something besides the label, which is what the food list
(cited external lookup) and a connected scale (measured weight) are for. What remains after those
two routes is the one genuinely open problem.

## The decomposition: four reliability gaps

We split "the app feels unreliable" into four named, independently measurable gaps, each owned by
a specific repo component, each with a concrete ask. (Full detail: `docs/RELIABILITY.md`.)

| Gap | Plain statement | Known route to a fix? | Owner |
|---|---|---|---|
| G1 conversion | phe-per-protein ratio varies by food | **yes**, cited class table / food list | `phe_per_g_protein.json` + food list |
| G2 label rounding | label rounds protein in PKU's range | **yes**, look phe up in the food list instead | food list as external lookup |
| G3 recipe-factor | guess ingredient weight-shares in a mixed food | **no known route**, this is the ask | estimator heuristic |
| G4 execution variance | same model, same food, different answer | **yes**, prompt/method discipline | `SKILL.md` |

**G3 is the marquee ask.** G1 and G2 have known routes through the food list. G4 is prompt
discipline. Portion weight is a scale. G3, inferring hidden proportions from a short, rounded
description, is the largest error source and has no known method that beats a naive baseline. It
is also the most transferable: the same shape recurs far beyond PKU, so a method that measurably
wins here is reusable anywhere.

## What we measured (all on `seed_v0`, 18 cases, USDA FDC ground truth)

- **Deterministic rubric** (`rubric_estimator`, the 7-step method as plain Python): MAE **12.76
  mg**, 83.3% within tolerance, identical every run. This is the reproducible reference point and
  floor.
- **Live Claude Skill** (`claude_skill`, `claude-opus-4-8`, same rubric applied by the model):
  five runs on identical inputs scored MAE **25.2 / … / 34.2 (mean 27.7, stdev 3.3)**, within-band
  **38.9% to 55.6%**. This spread is what G4 measures.
- **Mean live-Skill error by gap:** G2 ~11 mg, G1 ~22 mg, **G3 ~53 mg (dominant)**.
- The run-to-run instability concentrates mostly, though not only, in the G3 multi-ingredient
  cases. The tomato-broccoli medley swung from 5 mg to 49 mg across identical runs.

## What we built this session

1. **Benchmark integrity pass.** The old `claude_skill` result file was hand-assembled and did not
   conform to the harness schema. We regenerated it live through `run_benchmark.py` with the real
   model id recorded. The headline number is now reproducible rather than asserted.
2. **The gap decomposition + figure** (`docs/RELIABILITY.md`, `docs/assets/reliability_gaps.png`,
   `benchmark/results/gap_analysis.json`).
3. **Food-list foundation:** `food-list/foods.json` (11 cited rows), `foods.schema.json`, and a
   shared dependency-free loader `foodlist.py` with a Layer-1 validation gate. The rubric
   estimator now reads from this single source. We verified the output is numerically identical,
   MAE still 12.76.
4. **Contributor on-ramp:** `CONTRIBUTING.md` (pick a gap, improve it, prove it, open a PR), a
   copy-me template `benchmark/estimators/template_estimator.py`, and a CI workflow
   (`.github/workflows/benchmark.yml`) that runs the food-list validation and a regression gate on
   every relevant PR.
5. **Reproducibility meter:** `benchmark/variance.py` is a standalone tool that runs any estimator
   N times and reports the spread of its score. This is how G4 is measured. It reads estimator
   output only and changes no estimate. Deterministic estimators report a range of 0.

## Decisions worth remembering

- **Terminology:** We use "reliability gap" instead of "seam," which reads as jargon. The
  vocabulary throughout is reproducible, harness-generated, cited, and measured. We avoid
  "honest," since it implies the alternative is dishonest.
- **Leaderboard ranking:** Generalizing estimators are ranked by MAE. The memorizing stub is
  listed unranked, as a floor, because its score does not generalize to unseen labels. The
  deterministic rubric is therefore the estimator to beat.
- **No confidence bands.** The Skill contract forbids hedging or confidence language.
  Reproducibility fixes G4. Accuracy is measured externally by the benchmark, never self-graded.
- **Scope we deliberately left alone:** food labels themselves, since changing them isn't ours to
  do; regulatory classification, which belongs in its own proper sphere; and the estimator's
  internal packaging, a separate and larger task if pursued.

## Open threads

- **G3 is the community ask.** No known method beats naive weight-shares from the label alone.
- Expand the seed set beyond 18 cases. The gap magnitudes are directionally solid now and will
  firm up with more data.
- Unify the two food-data files (`benchmark/testset/food_reference.json` ground truth vs
  `food-list/foods.json` knowledge) behind one fetch path.
- Add Open Food Facts branded rows to exercise the G2 lookup path.
