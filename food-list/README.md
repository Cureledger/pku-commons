# Low-Protein Living PKU Foods List

## Why we supplement the model with a foods list

PKU food manufacturers and associations often maintain low-protein foods lists for the
community.

AI does not yet remove the need for these lists. The reliability of label-only ingredient
analysis is hard to gauge and harder to prove. To make the agent more reliable, we built a set
of food lists that act like knowledge graphs.

In testing, this improved performance across the very-low-protein range, the staples of the PKU
diet.

## TODO

We need a system for maintaining a living foods list that reduces the work the Claude Skill, or
any agent using the service, has to do.

Analogues exist from sources such as Open Food Facts, from whom we gratefully forked some
resources.

### Goal for the Claude Science hackathon

Get the USDA and Open Food Facts modules working well as a supplement to the label reader, and
build the technical foundation for the low-protein living foods list.

## The technical foundation (built for the hackathon)

The living list now has a concrete, cited data foundation that both the estimator and the
benchmark read from a single place:

| File | What it is |
|---|---|
| [`foods.json`](foods.json) | The canonical food-list data. Every row carries the Layer-1 fields the [peer-review model](../docs/PEER-REVIEW.md) requires: a citation to authority (a USDA FDC id, an Open Food Facts code, or a clinician sign-off), a version, and a reviewer of record. |
| [`foods.schema.json`](foods.schema.json) | JSON schema for a row, the contract a contributed row must satisfy. |
| [`foodlist.py`](foodlist.py) | The shared, dependency-free loader: `load()`, `lookup_phe_100g(name)`, and `validate()`. The rubric estimator imports this, so there is one source of truth for a food's phe value rather than an ad-hoc copy per consumer. |

The Layer-1 gate: `python foodlist.py` validates every row and exits non-zero if any row is
missing a citation, version, or reviewer of record, so an uncited row cannot silently enter the
knowledge base. This is the CI-enforceable version of "nothing enters without a citation."

Adding a food is a Layer-1 pull request. Add a row to `foods.json` that satisfies
`foods.schema.json` (cite an FDC id or OFF code, set the version and reviewer), run
`python foodlist.py` to confirm it validates, and run the benchmark to confirm it does not
regress any estimate that depends on it.

## How this narrows the reliability gaps

The food list is the component that owns two of the four reliability gaps named in
[`docs/RELIABILITY.md`](../docs/RELIABILITY.md):

- Gap 1 (source-dependent conversion): better per-food and per-class phe values here mean the
  estimator infers less and looks up more.
- Gap 2 (label rounding): for a recognizable food, a cited food-list row lets the estimator route
  around the rounded label entirely, the only way past the label's information ceiling.

Growing this list with cited rows is therefore a direct, measurable reliability contribution.

## Relationship to the benchmark

Ground truth for the phe-estimation [`benchmark/`](../benchmark/) is computed from
documented sources (USDA FoodData Central; Open Food Facts). The living foods list feeds
the same very-low-protein staple range the benchmark seed set covers. See
`benchmark/testset/food_reference.json`.

## Next (post-hackathon)

- Unify the two data files. `fetch_fdc.py` currently maintains the benchmark's ground-truth
  reference (`benchmark/testset/food_reference.json`), while the estimator now reads the cited
  `food-list/foods.json`. They overlap by design (ground truth against knowledge) but should
  share a fetch path so a new FDC pull updates both with one command.
- Open Food Facts module. Add branded and packaged rows (authority `OpenFoodFacts`, `off_code`)
  to exercise the label-lookup path (reliability gap 2).
