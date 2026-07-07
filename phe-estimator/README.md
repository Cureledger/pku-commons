# Phe-estimator Skill

> **The most important job after the landing page.**

This Skill is intended to do the "thinking like a PKU parent" needed to parse and
estimate the phenylalanine (phe) contained in a food from its nutrition label and
ingredients list.

## Objective

**One job:** turn a nutrition label into a **recipe factor** — a phe estimate anchored to
the label's own serving — so that phe can be scaled accurately to *any* portion the user
actually eats.

That's the whole thing. The recipe factor is the point: once we have a defensible phe
estimate for the panel's stated serving, any portion is simple arithmetic
(`phe = recipe_factor × portion`). The hard, human part — the part the clinic trains
parents to do — is estimating the relative weights of the phe-bearing ingredients in a
recipe well enough to compute that factor. This Skill encodes that method; it does not
reinvent it.

**Scope discipline (this is deliberate, not a limitation):**

- The Skill returns **one number** — the estimated phe for the requested portion — plus its
  working (the recipe factor and the per-ingredient breakdown that produced it).
- **No confidence bands, no probability ranges, no hedging language** in the Skill's output.
  Bands and "confidence levels" are chatter that invite the model to work harder, drift from
  the rubric, and introduce error. We measure accuracy *externally* (see the harness below) —
  we do not ask the Skill to grade its own uncertainty.
- The Skill **follows the rubric exactly and in order.** It does not add steps, skip steps,
  or substitute its own method. When the rubric requires a judgment (the recipe factor), it
  makes that judgment by the documented procedure — not by free-form reasoning.
- Optimization comes *after* it works. Efficiency and devops cleverness are welcome, but they
  may never trade away precision — and the benchmark exists to prove they didn't.

> The build plan that turns this objective into a working Skill lives in [`PLAN.md`](PLAN.md).

## The rubric — how we attack a label

The general method:

## Is this food potentially suitable for my diet?

For purposes of label analysis, PKU patients are often taught that foods with **2 g of
protein or less per serving** are potentially suitable for the diet. For these foods we
need to accurately calculate phe. We're less concerned about calculating phe for
higher-protein foods, in general, because they aren't usually relevant to the diet.

Accordingly, we set the Claude Skill's initial parameter for label parsing to **under 2 g
of protein** — not to make a decision about a food product's suitability for any person,
but to focus on making the Skill and label parser work well at the critical "countable"
food range.

## How do I count the phe in this food?

1. Once you determine a food is potentially suitable, read the label's ingredients list,
   searching for items that contain phe.
2. Classify each ingredient by type of protein source, for a phe-per-gram calculation for
   that ingredient.
3. Make an educated guess about recipe composition and the relative weight of phe-bearing
   ingredients in the entire label recipe, based on basic cooking science. We call this
   the **"recipe factor."**
4. Multiply the recipe factor by the portion consumed.
5. Log it.

My experiments show that many factors affect the AI's performance. So we need to **reduce
non-deterministic thinking** by the AI — so it doesn't "work" as hard and potentially
introduce errors — and create specific guidelines for optimizing performance in
foreseeable technical conditions (for example, weak grocery-store WiFi).

## Peer review requests

- **Methodology review** by parents, dietitians, and clinicians.
- **Testing of phe-reader outputs** by parents and dietitians.
- **Creating and optimizing the reliability** of the phe-estimator Skill by AI developers.

I have tested the phe-estimator function in real life, but have not yet created a working
Skill.

> **CRITICAL:** We will have Claude Science create a peer-review matrix once we feel the
> Skill is ready to test.

## The harness (already built)

The accuracy of this Skill is not a matter of opinion — it is measured against a public,
reproducible benchmark that already exists in [`../benchmark/`](../benchmark/):

- **A seed test set** (`testset/seed_v0.jsonl`, 18 cases) pairing food labels with an
  expected phe value in milligrams. Ground truth is computed from **USDA FoodData Central**
  (nutrient 508, Phenylalanine) — so anyone can independently re-derive every answer.
- **A pluggable harness** (`run_benchmark.py`) that scores any estimator exposing one
  function, `estimate(case) -> phe_mg`, and reports **MAE**, median error, RMSE, bias, and
  the share of cases **within a tolerance band**.
- **A regression gate**: run against a saved baseline and the harness exits non-zero if
  accuracy dropped — ready to wire into CI as a merge gate.

> **Where the "band" lives — and where it doesn't.** The tolerance band
> (`max(15 mg, 15% of truth)`) is a *scoring* rule inside the harness: it decides how close
> an estimate must be to count as correct. It is **not** something the Skill emits. The Skill
> returns a single number; the harness decides whether that number was close enough. Keeping
> uncertainty *out* of the Skill and *in* the measuring stick is exactly the separation that
> keeps the Skill precise.

## How the harness helps us

This is the part that solves the problem you hit building your own estimator — where making
a calculation "more efficient" quietly cost precision, and cycles got burned finding and
fixing the regression.

- **It catches precision loss automatically.** Any change — a prompt tweak, a caching layer,
  a food-list lookup, a "cleverness" — is scored before it merges. If MAE goes up or
  within-band% goes down, the gate fails. The compromise gets caught by CI, not by a user
  three weeks later.
- **It makes optimization safe.** We *can* be aggressive about devops efficiency precisely
  because the harness proves each change is precision-neutral. Optimize freely; the gate is
  the seatbelt.
- **It tells us whether the Skill actually follows the rubric.** If all the technical work
  lands but the numbers are wrong, we lost the thread — and the benchmark says so in one run.
- **It is the leaderboard (KPI #1).** Every scored estimator gets a row, so improvement over
  time is visible to families, clinicians, and the community.

The Skill plugs in via a `benchmark/estimators/claude_skill.py` adapter that wraps its output
in `estimate(case)` — that adapter is the single integration point between the Skill and the
harness.
