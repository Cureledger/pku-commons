# PKU Commons Phe-Estimation Benchmark

*The accuracy standard for phenylalanine-estimator tools.*

This benchmark is the scientific spine of PKU Commons. It lets **anyone** — a family, a
clinician, a researcher, or a maintainer's CI — score a phe-estimator against a public,
reproducible answer key. It is Layer 2 of the [peer-review model](../docs/PEER-REVIEW.md).

> **What it is:** a way to *measure* whether an estimate is accurate.
> **What it is not:** a food-suitability judgment or medical advice. It scores numeric phe
> estimation against database-derived ground truth.

---

## Why this exists

Phe-estimator apps are multiplying, but there has been **no standard** by which a user can
judge accuracy or a clinician can trust output. Without a shared measuring stick, "accurate"
is just a marketing word, and apps that decay after their author leaves take families' trust
down with them. A public benchmark fixes all three problems at once — it is the standard, the
CI quality gate, and the KPI-#1 leaderboard.

---

## How ground truth is computed (reproducibility statement)

Every test case pairs a **food label** with an **expected phe value in milligrams**, computed
as:

```
expected_phe_mg = Σ  (FDC phe_mg_per_100g[ingredient] × grams[ingredient] / 100)
```

- Per-ingredient phe comes from **USDA FoodData Central (SR Legacy)**, nutrient **508
  (Phenylalanine)**, cross-referenced with nutrient 203 (Protein).
- Each component records its **FDC id**, the grams used, and the phe contribution — see
  `ground_truth.components` in every case and the consolidated `testset/food_reference.json`.
- Because the inputs are public FDC records and the arithmetic is documented, **anyone can
  re-derive any expected value independently.** That reproducibility is the whole point:
  ground truth answers to a citable authority, not to us.

The seed set (`testset/seed_v0.jsonl`, 18 cases) deliberately spans the diet-relevant range:
near-zero staples (cornstarch, tapioca), common very-low-protein fruits and vegetables, a
couple of higher-phe items to test over-estimation control, and multi-ingredient recipes where
the "recipe factor" judgment matters.

---

## Metrics

For each estimator run we report:

| Metric | Meaning |
|---|---|
| **MAE (mg)** | Mean absolute error — the headline accuracy number. |
| **Median AE (mg)** | Median absolute error — robust to a few hard cases. |
| **RMSE (mg)** | Root-mean-square error — penalizes large misses. |
| **Bias (mg)** | Mean signed error; **+** means the estimator systematically **over**-estimates. |
| **Within band %** | Share of cases inside the tolerance band (below). |
| **Crashed** | Cases where the estimator raised an error (counts as a fail, not a crashed run). |

### Tolerance band

An estimate **passes** a case if its absolute error is within
`max(ABS_TOL_MG, REL_TOL × truth)`. Defaults: **15 mg or 15 %, whichever is larger.**

The absolute floor keeps near-zero foods (e.g. 1 mg cornstarch) from being judged on relative
error alone. The band is a **tunable, clinically-motivated parameter** — dietitians and
clinicians are explicitly invited to propose the right numbers via the review process; changing
it is a Layer-1 (citation + reviewer-of-record) decision.

---

## Running the benchmark

```bash
cd benchmark

# Score the bundled reference stub estimator
python run_benchmark.py --estimator estimators.stub_estimator

# Save a run + a markdown report
python run_benchmark.py --estimator estimators.stub_estimator \
    --out results/my_run.json --report report.md

# Use it as a CI merge gate: fail if this run regresses vs a saved baseline
python run_benchmark.py --estimator estimators.my_estimator \
    --baseline results/previous_best.json
# exit code 1 if MAE went up or within-band% went down beyond --tolerance
```

No third-party dependencies — standard-library Python 3.8+.

### Expanding the test set (USDA FDC key)

Ground truth is fetched from USDA FoodData Central. Set your key once:

```bash
cp .env.example .env          # then edit .env and set FDC_API_KEY=<your key>
# free key (instant): https://fdc.nal.usda.gov/api-key-signup.html
```

`.env` is git-ignored; `config.py` resolves the key from the process environment first,
then `.env`, then falls back to the rate-limited `DEMO_KEY`. Add foods with:

```bash
python fetch_fdc.py --update-reference testset/food_reference.json "spinach raw" "peas green raw"
```


---

## Implementing an estimator (for developers)

Expose one function in a module (see `estimators/base.py` for the contract and
`estimators/stub_estimator.py` for a worked example):

```python
def estimate(case: dict) -> float | dict:
    label = case["label"]          # serving_size_g, protein_g_per_serving, ingredients (text)
    # ... your logic ...            # DO NOT read case["expected_phe_mg"] / case["ground_truth"]
    return {"phe_mg": 42.0, "meta": {...}}   # or just: return 42.0
```

Then run `python run_benchmark.py --estimator your_pkg.your_module`. To score the **Claude
phe-estimator Skill**, wrap its output in an `estimate(case)` adapter — that adapter is the
integration point between the Skill and this benchmark.

---

## How contributions are gated

1. A PR that changes an estimator must not regress the benchmark (CI runs `run_benchmark.py
   --baseline <current best>`).
2. A PR that changes **ground truth** (a case, a food-reference row, or the tolerance band) is a
   Layer-1 change: it needs a citation to authority and a reviewer of record (see
   [PEER-REVIEW.md](../docs/PEER-REVIEW.md)).
3. Accepted improvements are recorded on the [leaderboard](leaderboard.md).

---

## Roadmap

- [x] Seed test set (v0) with FDC-computed ground truth and full provenance
- [x] Pluggable harness + metrics + regression gate
- [x] Reference stub estimator
- [ ] Claude Skill adapter (`estimators/claude_skill.py`) — wire the Skill to the harness
- [ ] Expand test set: branded/packaged labels (Open Food Facts codes), more composites
- [ ] Clinician-defined tolerance bands per phe range
- [ ] GitHub Actions workflow that posts benchmark deltas on every PR
