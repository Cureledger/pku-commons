# The PKU Commons Peer-Review Model

A two-layer quality-control system for scientific infrastructure the community can trust.

PKU Commons has to satisfy two audiences with two different definitions of "good." Clinicians and
researchers ask whether it is defensible. Engineers and families ask whether it actually works, and
whether that can be measured. Those questions map onto two long-established review traditions, legal
review and scientific review, and we use both, applied to different objects.

This document is the governance spine of the project. Every contribution is reviewed under one or both
of the layers below.

## Why two layers

| | Legal-style review | Scientific-style review |
|---|---|---|
| Validates | Reasoning and authority | Reproducibility and empirics |
| Truth is established by | Documented justification, sourced to controlling authority, adversarially tested and auditable | Independent re-measurement against evidence, beating the prior baseline without regression |
| Failure looks like | An unsourced claim, an unrecorded decision, a broken chain of authority | A number that went up with no reproducible measurement behind it |
| We apply it to | The method and the food list (the knowledge) | The estimator's outputs (the performance) |

An estimate becomes accurate through measurement, not argument. A food-list row becomes trustworthy
through a citation to authority, not through re-measurement. Both layers run in parallel because each
covers what the other cannot.

---

## Layer 1, legal-style review: method and data

Applies to the phe-estimation methodology, every rule it encodes, and every row of the living food list.

The standard: nothing enters the knowledge base without a citation to authority, a version, and a
reviewer of record.

Every rule and every food-list entry must carry:

1. A citation to authority, being one of a USDA FoodData Central record id, an Open Food Facts product
   code, or a named clinician or registered dietitian sign-off (a professional endorsement is a citable
   source in this system).
2. A version, the version of the rule or row, so history is reconstructable.
3. A reviewer of record: who accepted it, and when.

The process is the adversarial, auditable part:

- A proposed rule or row is a pull request with its citations attached.
- A challenge to an existing rule or row is a GitHub issue, the equivalent of a filed objection.
- The resolution is recorded. The decision, the reasoning, and the authority relied on become part of
  the permanent record. The trail from issue to resolution is the audit trail.

This is the model a lawyer trusts. The record shows what is in the knowledge base, why, on whose
authority, and who can be asked about it.

---

## Layer 2, scientific-style review: estimator outputs

Applies to the Claude phe-estimator Skill, and any app or model that implements the estimator interface.

The standard: accuracy claims are settled by measurement against a public, reproducible benchmark, never
by assertion.

- Ground truth for each benchmark case is computed from documented public sources (USDA FDC and Open Food
  Facts), so any reviewer can re-derive it. Reproducibility is the point.
- Every estimator is scored identically, on mean absolute error, per-case error, and the share of
  estimates within a clinically relevant tolerance band.
- Contributions are merged only when they improve the score without regressing other cases, enforced in
  CI, not by reviewer goodwill.
- Results are posted to a public leaderboard and tracked over time.

See [`benchmark/BENCHMARK.md`](../benchmark/BENCHMARK.md) for the full method, tolerance bands, and how to
run it.

---

## How the layers combine on a typical change

| Change | Layer 1 (legal) | Layer 2 (scientific) |
|--------|-----------------|----------------------|
| Add a food-list row | Yes: citation and reviewer of record | Only if it changes estimates, then also benchmarked |
| Change a phe-per-gram rule | Yes: citation to authority and audit trail | Yes: must not regress the benchmark |
| Improve the Skill's prompt or logic | Not required | Yes: benchmark must improve or hold, with no regressions |
| Clinician disputes an estimate | Yes: challenge filed as issue, resolution recorded | Yes: becomes a new benchmark case if reproducible |

---

## Why this makes apps sustainable

The central sustainability problem in PKU tooling is that apps die when their author moves on. This model
addresses that directly.

- Quality is guaranteed by the evaluation, not the author. Every version is scored against the public
  benchmark, so an app can change maintainers, or lose its original developer entirely, and families
  still know it meets the bar.
- The knowledge is portable and cited. The method and food list stand on documented authority, not on
  one person's expertise, so anyone can pick them up and keep them current.
- Everything is reconstructable. Versions, reviewers, and audit trails mean the project's decisions
  survive turnover in contributors.

---

## Roles

| Role | Reviews | Layer |
|------|---------|-------|
| Parents and patients | Real-world testing of estimator outputs; lived-experience method review | Both (evidence and method) |
| Dietitians and clinicians | Methodology soundness; sign-off as citable authority; tolerance-band definition | Layer 1 (authority) and Layer 2 (defines the bar) |
| AI and app developers | Estimator reliability; benchmark performance; regression prevention | Layer 2 |
| Maintainers | Merge gate: confirm citations (L1) and CI benchmark pass (L2) | Both |

---

## Status

- [x] Two-layer model defined
- [x] Benchmark harness scaffold + seed test set (see `benchmark/`)
- [x] Peer-review matrix, [`phe-estimator/PEER-REVIEW-MATRIX.md`](../phe-estimator/PEER-REVIEW-MATRIX.md); reliability gaps in [`RELIABILITY.md`](RELIABILITY.md)
- [x] Food-list Layer-1 contract enforced in code, [`food-list/foodlist.py`](../food-list/foodlist.py) `validate()` (every row cited, versioned, and reviewed)
- [x] CI wiring of the benchmark as a merge gate, [`.github/workflows/benchmark.yml`](../.github/workflows/benchmark.yml)
- [ ] Clinician / RD reviewer roster and sign-off log

*This document is itself reviewed under the same model: it lives in the repo and changes by pull request.*
