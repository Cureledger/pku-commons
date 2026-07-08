# Contributing to PKU Commons

Thank you for helping make PKU tools reliable and keep them reliable. This project is
infrastructure: your contribution is measured, cited, and outlives whoever wrote it.

**New here? Start with [`docs/RELIABILITY.md`](docs/RELIABILITY.md)** — it decomposes phe-estimator
reliability into four named gaps. Pick one; it tells you which component owns the fix.

---

## The 60-second mental model

There are two kinds of contribution, and they're reviewed differently
([`docs/PEER-REVIEW.md`](docs/PEER-REVIEW.md)):

- **Layer 2 — you're improving an estimate.** Prove it with a benchmark number. Merges are
  gated by CI: your run must not regress the baseline.
- **Layer 1 — you're adding/changing knowledge** (a food-list row, a phe-per-gram rule). Cite an
  authority. Every row needs a citation, a version, and a reviewer of record.

---

## Path A — improve an estimator (Layer 2)

This is the headline ask: beat the deterministic rubric on the benchmark.

1. **Clone and run the benchmark once**, so you know it works:
   ```bash
   git clone https://github.com/Cureledger/pku-commons && cd pku-commons/benchmark
   python run_benchmark.py --estimator estimators.stub_estimator
   ```
   No third-party dependencies — standard-library Python 3.8+.

2. **Copy the template** and write your method:
   ```bash
   cp estimators/template_estimator.py estimators/my_estimator.py
   # edit estimators/my_estimator.py — implement estimate(case) -> mg phe
   ```
   You get the label (serving size, protein, ingredient text). You must **not** read
   `case["expected_phe_mg"]` or `case["ground_truth"]`. The shared, cited food list is available
   to you via `import foodlist`.

3. **Score it against the baseline** (this is exactly what CI runs):
   ```bash
   python run_benchmark.py --estimator estimators.my_estimator \
       --baseline results/baseline_v0.json \
       --out results/my_estimator_v0.json --report report.md
   ```
   Exit code is non-zero if you regress (MAE up or within-band % down). Green = you're good.

4. **Open a PR** with your `estimators/my_estimator.py` and `results/my_estimator_v0.json`, and
   add a row to [`benchmark/leaderboard.md`](benchmark/leaderboard.md). CI re-runs to verify. A
   passing, non-regressing run lands you on the board.

### Which gap should I pick?

| If you're strong at… | Attack gap | Where |
|---|---|---|
| retrieval / knowledge graphs | **G1/G2** — look phe up instead of inferring it | food list + estimator |
| estimation / modeling | **G3** — better recipe-factor weight shares (biggest win) | `estimators/` |
| LLM engineering | **G4** — make the live Skill reproducible run-to-run | `phe-estimator/SKILL.md` |

**Working on gap #4 (reproducibility)?** Use the variance meter to check whether a prompt change
actually reduced run-to-run wobble:
```bash
python variance.py --estimator estimators.rubric_estimator --runs 5   # deterministic → range 0
```
It runs the benchmark scorer N times and reports the spread of MAE / within-band %. A
deterministic estimator scores 0 range; the gap from 0 is the gap-4 defect you're closing. (For
the live Skill, set a model caller first — see the header of `variance.py`.) It reads estimator
output only; it changes no estimate.

---

## Path B — add or change knowledge (Layer 1)

### Add a food-list row

1. Add an entry to [`food-list/foods.json`](food-list/foods.json) that satisfies
   [`food-list/foods.schema.json`](food-list/foods.schema.json). Every row needs:
   - a **citation** — a USDA FDC id, an Open Food Facts code, or a named clinician/RD sign-off;
   - a **version** (`"v0"`); and a **reviewer of record**.
2. Validate locally — this is what CI runs:
   ```bash
   python food-list/foodlist.py    # exits non-zero if any row is uncited
   ```
3. Run the benchmark to confirm no estimate that depends on the list regressed.
4. Open a PR. A **challenge** to an existing row is a GitHub issue; the resolution becomes part
   of the audit trail.

### Add a benchmark test case

Add a line to [`benchmark/testset/seed_v0.jsonl`](benchmark/testset/seed_v0.jsonl) conforming to
[`benchmark/schema.json`](benchmark/schema.json), with `ground_truth.components` citing the FDC
ids and grams used so anyone can re-derive `expected_phe_mg`. Use
[`benchmark/fetch_fdc.py`](benchmark/fetch_fdc.py) to pull values.

---

## What CI checks on your PR

The [`benchmark` workflow](.github/workflows/benchmark.yml) runs automatically on any PR touching
`benchmark/`, `phe-estimator/`, or `food-list/`:

1. **Food-list Layer-1 validation** — every row is cited, versioned, has a reviewer.
2. **Regression gate** — the deterministic rubric is re-scored against the baseline; a regression
   fails the check.
3. The benchmark report is posted to the run summary.

---

## Ground rules

- **No peeking.** Estimators never read the answer key (`expected_phe_mg` / `ground_truth`).
- **No hedging in the Skill.** The phe-estimator returns one number, no confidence bands — see
  [`phe-estimator/SKILL.md`](phe-estimator/SKILL.md). Accuracy is measured externally, by the
  benchmark, not self-graded.
- **Cite authority for knowledge; cite measurement for accuracy.** That's the whole model.

Questions or a failure case you can't fix? Open an issue — a reproducible dispute becomes a new
benchmark case.
