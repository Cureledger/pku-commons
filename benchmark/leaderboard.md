# PKU Commons — Phe-Estimator Leaderboard

*KPI #1: continually-improved performance for phe-reader apps, tracked over time.*

Every scored estimator (the Claude Skill, any app backend, any contributed model) lands here.
Lower MAE and higher within-band % are better. Runs are produced by `run_benchmark.py` on the
current public test set; the **test set version** column matters because scores are only
comparable within the same version.

## Current standings — test set `seed_v0` (18 cases)

| Rank | Estimator | Version | MAE (mg) ↓ | Within band ↑ | Bias (mg) | Date (UTC) | Run |
|-----:|-----------|---------|----------:|--------------:|----------:|------------|-----|
| 1 | `estimators.stub_estimator` (reference baseline) | v0 | 6.61 | 88.9% | +6.56 | 2026-07-07 | [json](results/stub_v0.json) |

> The stub is a deliberately crude baseline (equal-weight recipe factor). It is here to
> establish the floor; the goal is for real estimators — starting with the Claude Skill — to
> beat it, especially on the multi-ingredient composite cases where it fails.

## How to appear here

1. Implement the estimator interface (see [BENCHMARK.md](BENCHMARK.md)).
2. Run `python run_benchmark.py --estimator <you> --out results/<you>.json`.
3. Open a PR adding your `results/*.json` and a row above. CI re-runs to verify.

## Developer-participation metrics (KPI #2)

Tracked alongside performance for the hackathon:

| Metric | Value |
|---|---|
| Estimators submitted | 1 (reference stub) |
| External contributors | 0 |
| Test-set cases (with citations) | 18 |
| Food-reference rows (cited) | 11 |

*Update these counts as contributions arrive. Consider auto-generating this section from the
`results/` directory and merged PRs.*
