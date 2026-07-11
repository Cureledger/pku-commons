# Contributing to PKU Commons

Thank you for helping make PKU tools reliable and for keeping them that way. This project is
infrastructure. Your contribution gets measured, cited, and outlives whoever wrote it.

If you are new here, start with [`docs/RELIABILITY.md`](docs/RELIABILITY.md). It breaks
phe-estimator reliability into four named gaps and tells you which component owns each fix. Pick
one.

## The two kinds of contribution

Each kind gets reviewed differently ([`docs/PEER-REVIEW.md`](docs/PEER-REVIEW.md)).

Layer 2 is improving an estimate. Prove it with a benchmark number. CI gates the merge, and your
run must not regress the baseline.

Layer 1 is adding or changing knowledge, such as a food-list row or a phe-per-gram rule. Cite an
authority. Every row needs a citation, a version, and a reviewer of record.

## Path A: improve an estimator (Layer 2)

The core task: beat the deterministic rubric on the benchmark.

1. Clone and run the benchmark once, so you know it works:
   ```bash
   git clone https://github.com/Cureledger/pku-commons && cd pku-commons/benchmark
   python run_benchmark.py --estimator estimators.stub_estimator
   ```
   No third-party dependencies. Standard-library Python 3.8+.

2. Copy the template and write your method:
   ```bash
   cp estimators/template_estimator.py estimators/my_estimator.py
   # edit estimators/my_estimator.py to implement estimate(case) returning mg phe
   ```
   You get the label: serving size, protein, ingredient text. You must not read
   `case["expected_phe_mg"]` or `case["ground_truth"]`. The shared, cited food list is available
   to you via `import foodlist`.

3. Score it against the baseline. This is exactly what CI runs:
   ```bash
   python run_benchmark.py --estimator estimators.my_estimator \
       --baseline results/baseline_v0.json \
       --out results/my_estimator_v0.json --report report.md
   ```
   The exit code is non-zero if you regress, meaning MAE went up or within-band percent went
   down. A green run means you are good.

4. Open a PR with your `estimators/my_estimator.py` and `results/my_estimator_v0.json`, and add a
   row to [`benchmark/leaderboard.md`](benchmark/leaderboard.md). CI re-runs to verify. A passing,
   non-regressing run lands you on the board.

### Which gap should I pick?

| If you are strong at | Attack gap | Where |
|---|---|---|
| retrieval and knowledge graphs | G1 and G2, look phe up instead of inferring it | food list and estimator |
| estimation and modeling | G3, better recipe-factor weight shares (biggest win) | `estimators/` |
| LLM engineering | G4, make the live Skill reproducible run to run | `phe-estimator/SKILL.md` |

Working on gap 4, reproducibility? Use the variance meter to check whether a prompt change
actually reduced run-to-run wobble:
```bash
python variance.py --estimator estimators.rubric_estimator --runs 5   # deterministic, range 0
```
It runs the benchmark scorer N times and reports the spread of MAE and within-band percent. A
deterministic estimator scores a range of 0. The distance from 0 is the gap-4 defect you are
closing. For the live Skill, set a model caller first; see the header of `variance.py`. The meter
reads estimator output only and changes no estimate.

---

## Path B: add or change knowledge (Layer 1)

### Add a food-list row

1. Add an entry to [`food-list/foods.json`](food-list/foods.json) that satisfies
   [`food-list/foods.schema.json`](food-list/foods.schema.json). Every row needs a citation (a
   USDA FDC id, an Open Food Facts code, or a named clinician or RD sign-off), a version
   (`"v0"`), and a reviewer of record.
2. Validate locally. This is what CI runs:
   ```bash
   python food-list/foodlist.py    # exits non-zero if any row is uncited
   ```
3. Run the benchmark to confirm no estimate that depends on the list regressed.
4. Open a PR. A **challenge** to an existing row is a GitHub issue. The resolution becomes part
   of the audit trail.

### Add a benchmark test case

Add a line to [`benchmark/low_protein_usda.jsonl`](benchmark/low_protein_usda.jsonl) (the
729-food single-ingredient corpus) conforming to [`benchmark/schema.json`](benchmark/schema.json),
with `ground_truth.components` citing the FDC ids and grams used so anyone can re-derive
`expected_phe_mg`. Use [`benchmark/fetch_fdc.py`](benchmark/fetch_fdc.py) to pull values, then
validate the file is arithmetically honest with `python benchmark/validate_cases.py
benchmark/low_protein_usda.jsonl` (must exit 0).

---

## What CI checks on your PR

The [`benchmark` workflow](.github/workflows/benchmark.yml) runs automatically on any PR touching
`benchmark/`, `phe-estimator/`, or `food-list/`:

1. Food-list Layer-1 validation: every row is cited, versioned, and has a reviewer.
2. Regression gate: the deterministic rubric gets re-scored against the baseline, and a
   regression fails the check.
3. The benchmark report is posted to the run summary.

---

## Ground rules

- No peeking. Estimators never read the answer key (`expected_phe_mg` or `ground_truth`).
- No hedging in the Skill. The phe-estimator returns one number and no confidence bands, see
  [`phe-estimator/SKILL.md`](phe-estimator/SKILL.md). Accuracy is measured externally, by the
  benchmark.
- Cite authority for knowledge, and cite measurement for accuracy. That is the model.

Have a question, or a failure case you cannot fix? Open an issue. A reproducible dispute becomes
a new benchmark case.
