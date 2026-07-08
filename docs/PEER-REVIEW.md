# The PKU Commons Peer-Review Model

*A two-layer quality-control system for scientific infrastructure the community can trust.*

PKU Commons has to satisfy two audiences with two different definitions of "good." Clinicians and
researchers ask *"is this defensible?"* Engineers and families ask *"does it actually work, measurably?"*
Those map onto two long-established review traditions — **legal review** and **scientific review** — and
we use **both**, applied to different objects.

This document is the governance spine of the project. Every contribution is reviewed under one (or both)
of the layers below.

---

## Why two layers

| | **Legal-style review** | **Scientific-style review** |
|---|---|---|
| **Validates** | Reasoning & authority | Reproducibility & empirics |
| **Truth is established by** | Documented justification, sourced to controlling authority, adversarially tested and auditable | Independent re-measurement against evidence; beating the prior baseline without regression |
| **Failure looks like** | An unsourced claim, an unrecorded decision, a broken chain of authority | A number that went up with no reproducible measurement behind it |
| **We apply it to** | The **method** and the **food list** (the *knowledge*) | The **estimator's outputs** (the *performance*) |

Neither layer alone is enough. You cannot *argue* an estimate into being accurate — that requires
measurement. And you cannot *measure* your way to a trustworthy food-list row — that requires a citation
to authority. So we run them in parallel.

---

## Layer 1 — Legal-style review: method & data

**Applies to:** the phe-estimation methodology, every rule it encodes, and every row of the living food list.

**Standard:** *nothing enters the knowledge base without a citation to authority, a version, and a reviewer
of record.*

Every rule and every food-list entry must carry:

1. **Citation to authority** — one of:
   - a **USDA FoodData Central** record id, or
   - an **Open Food Facts** product code, or
   - a **named clinician / registered dietitian sign-off** (a professional endorsement is a citable
     source in this system).
2. **Version** — the version of the rule/row, so history is reconstructable.
3. **Reviewer of record** — who accepted it, and when.

**Process (the adversarial, auditable part):**

- A proposed rule or row is a **pull request** with its citations attached.
- A **challenge** to an existing rule or row is a **GitHub issue** — the equivalent of a filed objection.
- **Resolution** is recorded: the decision, the reasoning, and the authority relied on become part of the
  permanent record. The issue → resolution trail *is* the audit trail.

This is deliberately the model a lawyer trusts: the record shows not just *what* is in the knowledge base,
but *why*, *on whose authority*, and *who can be asked about it*.

---

## Layer 2 — Scientific-style review: estimator outputs

**Applies to:** the Claude phe-estimator Skill, and any app or model that implements the estimator interface.

**Standard:** *accuracy claims are settled by measurement against a public, reproducible benchmark — never
by assertion.*

- Ground truth for each benchmark case is **computed from documented public sources** (USDA FDC / Open Food
  Facts), so any reviewer can re-derive it. Reproducibility is the whole point.
- Every estimator is scored identically: **mean absolute error**, **per-case error**, and **% of estimates
  within a clinically-relevant tolerance band**.
- Contributions are merged only when they **improve the score without regressing** other cases —
  enforced in **CI**, not by reviewer goodwill.
- Results are posted to a **public leaderboard** and tracked over time.

See [`benchmark/BENCHMARK.md`](../benchmark/BENCHMARK.md) for the full method, tolerance bands, and how to
run it.

---

## How the layers combine on a typical change

| Change | Layer 1 (legal) | Layer 2 (scientific) |
|--------|-----------------|----------------------|
| Add a food-list row | ✅ citation + reviewer of record | — (unless it changes estimates → then also benchmarked) |
| Change a phe-per-gram rule | ✅ citation to authority + audit trail | ✅ must not regress the benchmark |
| Improve the Skill's prompt/logic | — | ✅ benchmark must improve or hold, no regressions |
| Clinician disputes an estimate | ✅ challenge filed as issue, resolution recorded | ✅ becomes a new benchmark case if reproducible |

---

## Why this makes apps *sustainable*

The central sustainability problem in PKU tooling is that apps die when their author moves on. This model
addresses it directly:

- **Quality is guaranteed by the eval, not the author.** Because every version is scored against the public
  benchmark, an app can change maintainers — or lose its original developer entirely — and families still
  know it meets the bar.
- **The knowledge is portable and cited.** The method and food list stand on documented authority, not on
  one person's expertise, so anyone can pick them up and keep them current.
- **Everything is reconstructable.** Versions, reviewers, and audit trails mean the project's decisions
  survive turnover in contributors.

---

## Roles

| Role | Reviews | Layer |
|------|---------|-------|
| **Parents / patients** | Real-world testing of estimator outputs; lived-experience method review | Both (evidence + method) |
| **Dietitians / clinicians** | Methodology soundness; sign-off as citable authority; tolerance-band definition | Layer 1 (authority) + Layer 2 (defines the bar) |
| **AI / app developers** | Estimator reliability; benchmark performance; regression prevention | Layer 2 |
| **Maintainers** | Merge gate: confirm citations (L1) and CI benchmark pass (L2) | Both |

---

## Status

- [x] Two-layer model defined
- [x] Benchmark harness scaffold + seed test set (see `benchmark/`)
- [x] Peer-review **matrix** — [`phe-estimator/PEER-REVIEW-MATRIX.md`](../phe-estimator/PEER-REVIEW-MATRIX.md); reliability gaps in [`RELIABILITY.md`](RELIABILITY.md)
- [x] Food-list Layer-1 contract enforced in code — [`food-list/foodlist.py`](../food-list/foodlist.py) `validate()` (every row cited/versioned/reviewed)
- [x] CI wiring of the benchmark as a merge gate — [`.github/workflows/benchmark.yml`](../.github/workflows/benchmark.yml)
- [ ] Clinician / RD reviewer roster and sign-off log

*This document is itself reviewed under the same model: it lives in the repo and changes by pull request.*
