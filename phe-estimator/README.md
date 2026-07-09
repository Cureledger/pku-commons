# Phe-estimator Skill

This Skill does the thinking a PKU parent does to read a food's nutrition label and
ingredients list and estimate the phenylalanine (phe) it contains. It is the second core
deliverable of PKU Commons, after the landing page.

## Objective

The Skill turns a nutrition label into a recipe factor: a phe estimate anchored to the label's
own serving, so phe scales accurately to any portion the user actually eats.

Once we have a defensible phe estimate for the panel's stated serving, any portion is
arithmetic (`phe = recipe_factor × portion`). The hard part is the human one the clinic trains
parents to do: estimating the relative weights of the phe-bearing ingredients in a recipe well
enough to compute that factor. This Skill encodes that method. It does not reinvent it.

Its scope is narrow on purpose:

- The Skill returns one number, the estimated phe for the requested portion, plus its working:
  the recipe factor and the per-ingredient breakdown that produced it.
- Its output carries no confidence bands, no probability ranges, and no hedging language. Bands
  and confidence levels invite the model to work harder, drift from the rubric, and introduce
  error. We measure accuracy externally, with the harness below, rather than asking the Skill to
  grade its own uncertainty.
- The Skill follows the rubric exactly and in order. It does not add steps, skip steps, or
  substitute its own method. When the rubric requires a judgment (the recipe factor), it makes
  that judgment by the documented procedure, not by free-form reasoning.
- Optimization comes after it works. Efficiency and devops cleverness are welcome, but they may
  never trade away precision, and the benchmark exists to prove they did not.

The build plan that turns this objective into a working Skill lives in [`PLAN.md`](PLAN.md).

## The rubric: how we attack a label

The general method follows.

### Is this food potentially suitable for my diet?

For label analysis, PKU patients are often taught that foods with 2 g of protein or less per
serving are potentially suitable for the diet. Those are the foods where we need to calculate
phe accurately. Higher-protein foods matter less here, because they are not usually relevant to
the diet.

So we set the Skill's initial parameter for label parsing to under 2 g of protein. This is not a
decision about whether any product is suitable for any person. It focuses the Skill and the label
parser on working well in the critical countable range.

### How do I count the phe in this food?

1. Once you determine a food is potentially suitable, read the label's ingredients list and find
   the items that contain phe.
2. Classify each ingredient by protein source, so you can apply a phe-per-gram calculation to it.
3. Estimate the recipe composition and the relative weight of the phe-bearing ingredients in the
   whole label recipe, using basic cooking science. We call this the recipe factor.
4. Multiply the recipe factor by the portion consumed.
5. Log it.

Testing showed that many factors affect the AI's performance. The Skill reduces the AI's
non-deterministic thinking, so it does not work as hard and introduce errors, and it sets
specific guidelines for foreseeable technical conditions such as weak grocery-store WiFi.

## Peer review requests

- Methodology review by parents, dietitians, and clinicians.
- Testing of phe-reader outputs by parents and dietitians.
- Building and improving the reliability of the phe-estimator Skill by AI developers.

The maintainer has tested the phe-estimation method in real life. The Skill that encodes it is
now built and scored against the benchmark, and its review instrument is
[PEER-REVIEW-MATRIX.md](PEER-REVIEW-MATRIX.md). It turns "is it ready?" into specific,
assignable review tasks across methodology, output testing, and reliability, each tied to real
benchmark cases and to a reviewer role.

## The harness (already built)

The accuracy of this Skill is measured, not asserted. It is scored against a public,
reproducible benchmark that already exists in [`../benchmark/`](../benchmark/):

- A seed test set (`testset/seed_v0.jsonl`, 18 cases) pairing food labels with an expected phe
  value in milligrams. Ground truth is computed from USDA FoodData Central (nutrient 508,
  Phenylalanine), so anyone can independently re-derive every answer.
- A pluggable harness (`run_benchmark.py`) that scores any estimator exposing one function,
  `estimate(case)` returning phe in mg, and reports MAE, median error, RMSE, bias, and the share
  of cases within a tolerance band.
- A regression gate: run against a saved baseline and the harness exits non-zero if accuracy
  dropped, ready to wire into CI as a merge gate.

The tolerance band (`max(15 mg, 15% of truth)`) is a scoring rule inside the harness. It decides
how close an estimate must be to count as correct. The Skill does not emit it. The Skill returns
a single number, and the harness decides whether that number was close enough. Keeping
uncertainty out of the Skill and inside the measuring stick is the separation that keeps the
Skill precise.

## How the harness helps us

It solves the problem you hit building your own estimator, where making a calculation more
efficient quietly cost precision and cycles got burned finding and fixing the regression.

- It catches precision loss automatically. Any change, whether a prompt tweak, a caching layer,
  or a food-list lookup, is scored before it merges. If MAE goes up or within-band percent goes
  down, the gate fails. The compromise gets caught by CI, not by a user three weeks later.
- It makes optimization safe. You can be aggressive about devops efficiency precisely because
  the harness proves each change is precision-neutral. Optimize freely; the gate is the
  seatbelt.
- It tells us whether the Skill actually follows the rubric. If the technical work all lands but
  the numbers are wrong, the benchmark says so in one run.
- It is the leaderboard (KPI #1). Every scored estimator gets a row, so improvement over time is
  visible to families, clinicians, and the community.

The Skill plugs in via a `benchmark/estimators/claude_skill.py` adapter that wraps its output in
`estimate(case)`. That adapter is the single integration point between the Skill and the harness.
