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
| 2 | `estimators.rubric_estimator` (deterministic rubric) | v0 | 12.76 | 83.3% | +6.83 | 2026-07-07 | [json](results/rubric_v0.json) |
| 3 | `estimators.claude_skill` (Skill via LLM) | v0 | 23.57 | 50.0% | −16.41 | 2026-07-07 | [json](results/claude_skill_v0.json) |

> **Read these ranks with the method in mind — MAE alone is misleading here:**
>
> - The **stub** posts the lowest MAE but is not a generalizing estimator: it looks up phe
>   from a built-in table keyed to these exact seed foods, so it effectively memorizes the
>   single-ingredient answers and only its crude equal-weight recipe factor is ever tested.
>   It is the floor, not a real competitor.
> - The **deterministic rubric** (`rubric_estimator`) is the faithful, reproducible encoding
>   of the [SKILL.md](../phe-estimator/SKILL.md) rubric: it derives phe from label protein ×
>   a cited phe-per-g-protein class table (protein-panel path) or the food-list phe-per-100g
>   (whole-food path). It generalizes to unseen labels — which is why it is the estimator to
>   actually beat.
> - The **Claude Skill** row is the *live model* applying that same rubric. The gap between it
>   (23.57) and the deterministic rubric (12.76) is the **optimization target**: it measures
>   how much precision the model loses by following the rubric loosely. Closing that gap —
>   without adding confidence/band chatter — is the week's devops work. Its worst miss (c16,
>   a rice+carrot bowl) is the recipe-factor weight-share problem the scale + food-list work
>   exists to narrow.

## How to appear here

1. Implement the estimator interface (see [BENCHMARK.md](BENCHMARK.md)).
2. Run `python run_benchmark.py --estimator <you> --out results/<you>.json`.
3. Open a PR adding your `results/*.json` and a row above. CI re-runs to verify.

## Developer-participation metrics (KPI #2)

Tracked alongside performance for the hackathon:

| Metric | Value |
|---|---|
| Estimators submitted | 3 (stub, deterministic rubric, Claude Skill) |
| External contributors | 0 |
| Test-set cases (with citations) | 18 |
| Food-reference rows (cited) | 11 |

*Update these counts as contributions arrive. Consider auto-generating this section from the
`results/` directory and merged PRs.*
