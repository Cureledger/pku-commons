# PKU Commons — Phe-Estimator Leaderboard

*KPI #1: continually-improved performance for phe-reader apps, tracked over time.*

Every scored estimator (the Claude Skill, any app backend, any contributed model) lands here.
Lower MAE and higher within-band % are better. Runs are produced by `run_benchmark.py` on the
current public test set; the **test set version** column matters because scores are only
comparable within the same version.

## Current standings — test set `seed_v0` (18 cases)

| Rank | Estimator | Version | MAE (mg) ↓ | Within band ↑ | Bias (mg) | Date (UTC) | Run |
|-----:|-----------|---------|----------:|--------------:|----------:|------------|-----|
| — | `estimators.stub_estimator` (reference floor — memorizes seed answers, does not generalize) | v0 | 6.61 | 88.9% | +6.56 | 2026-07-08 | [json](results/stub_v0.json) |
| **1** | `estimators.rubric_estimator` (deterministic rubric — **the one to beat**) | v0 | **12.76** | 83.3% | +6.83 | 2026-07-08 | [json](results/rubric_v0.json) |
| 2 | `estimators.claude_skill` (Skill via LLM, `claude-opus-4-8`) | v0 | 33.73 | 33.3% | −1.36 | 2026-07-08 | [json](results/claude_skill_v0.json) |

**Ranking rule:** generalizing estimators are ranked by MAE; the stub is listed **unranked** as a
reference floor because it looks its answers up from a table keyed to these exact seed foods, so
its score does not generalize to unseen labels. The rubric is therefore #1 — the estimator a real
contribution must beat.

> **The `claude_skill` row is one run of a non-deterministic estimator.** Three identical runs of
> the same model on the same 18 cases scored MAE **24.3 / 33.7 / 34.6** (within-band 33–44%). That
> run-to-run spread is reliability **gap #4**, quantified — see
> [`docs/RELIABILITY.md`](../docs/RELIABILITY.md). The gap between the live Skill and the
> deterministic rubric (12.76) is the measured optimization target; closing it — without adding
> confidence/band chatter — is squarely AI-developer work.

> **How the three estimators differ (why MAE alone is misleading here):**
>
> - The **stub** memorizes: it looks phe up from a built-in table keyed to these exact seed
>   foods, so only its crude equal-weight recipe factor is ever tested. It is the floor.
> - The **deterministic rubric** (`rubric_estimator`) is the reproducible encoding of the
>   [SKILL.md](../phe-estimator/SKILL.md) rubric — phe from label protein × a cited
>   phe-per-g-protein class table, or the food-list phe-per-100g on the whole-food path. It
>   generalizes to unseen labels, which is why it is the one to beat.
> - The **Claude Skill** is the *live model* applying that same rubric. Its worst miss (the c16
>   rice+carrot bowl) is the recipe-factor weight-share problem (gap #3) that the food-list and
>   scale work exist to narrow.

## How to appear here

1. Implement the estimator interface (see [BENCHMARK.md](BENCHMARK.md)).
2. Run `python run_benchmark.py --estimator <you> --out results/<you>.json`.
3. Open a PR adding your `results/*.json` and a row above. CI re-runs to verify.

## Developer-participation metrics (KPI #2)

Tracked alongside performance for the hackathon:

| Metric | Value |
|---|---|
| Estimators scored | 3 (stub, deterministic rubric, Claude Skill) |
| Copy-me estimator template | ✅ `estimators/template_estimator.py` |
| External contributors | 0 |
| Test-set cases (with citations) | 18 |
| Food-list rows (cited, Layer-1 validated) | 11 |
| Contributor on-ramp | ✅ [CONTRIBUTING.md](../CONTRIBUTING.md) + CI gate ([benchmark.yml](../.github/workflows/benchmark.yml)) |
| Reliability gaps named + measured | 4 ([RELIABILITY.md](../docs/RELIABILITY.md)) |

*Update these counts as contributions arrive. Consider auto-generating this section from the
`results/` directory and merged PRs.*
