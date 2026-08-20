# Guthrie — Corpus Manifest

*What Guthrie's brain knows, where it comes from, and how each claim is authorized.*

Guthrie is the PKU community agent (named for Robert Guthrie, who invented the
newborn-screening heel-prick test in 1963). In his "PKU genius" form he answers
from a **hybrid retrieval index** built from two layers, and he **cites or
refuses** — he never asserts a fact he cannot ground in a retrieved source.

This manifest is the *legal-review* object for the brain: it fixes exactly what
is in scope, the exact queries that define the literature slice, and the
citation authority each source maps to. Changing the corpus means changing this
file (with a version bump and a reviewer of record), the same discipline the
[PKU Commons peer-review model](../docs/PEER-REVIEW.md) applies to the food list.

---

## Layer 1 — The PKU literature ("brains of the researchers")

**Source:** NCBI PubMed / PMC via E-utilities (`esearch` → `efetch`). No API key
required; contact email attached when available.

**Retrieval universe (frozen query).** Everything Guthrie can cite from the
literature is drawn from this one query:

```
phenylketonuria OR phenylketonurias OR hyperphenylalaninemia OR "phenylalanine hydroxylase deficiency"
```

- **Live count at freeze:** **9,659** PubMed records (see
  [`build/corpus_manifest_counts.json`](build/corpus_manifest_counts.json) for the
  timestamped pull).
- **Why this is tractable, not "big data":** the *entire* PKU literature is
  ~9.7k records. It embeds into a single local index in minutes on CPU, for
  cents. There is no knowledge-graph pipeline, no cluster, and no streaming
  ingestion — that scale does not exist for this disease. The corpus is small
  enough that one person can rebuild it from scratch with one command, which is
  the whole point for sustainability.

**Coverage domains (sub-queries).** These are not separate corpora; they are the
domains the [eval set](eval/) must exercise, with their live counts at freeze:

| Domain | Records | Query intent |
|---|---:|---|
| Dietary management | 3,181 | diet, medical food, protein substitute, phe intake |
| Blood-phe monitoring | 1,024 | blood phenylalanine, dried blood spot, monitoring |
| BH4 / sapropterin | 933 | sapropterin, tetrahydrobiopterin, Kuvan, BH4 |
| Neurocognitive outcomes | 869 | cognition, executive function, IQ, white matter |
| Guidelines / consensus | 650 | guideline, consensus, recommendation, standard of care |
| Maternal PKU | 608 | maternal phenylketonuria |
| Gene / enzyme therapy | 320 | gene therapy, mRNA, AAV, enzyme substitution |
| Pegvaliase | 200 | pegvaliase, Palynziq, phenylalanine ammonia lyase |
| Large neutral amino acids | 100 | LNAA |

Exact query strings are frozen in
[`build/corpus_manifest_counts.json`](build/corpus_manifest_counts.json).

**Ingestion policy (v0):**
- **Metadata + abstract** for the full retrieval universe (title, abstract,
  year, journal, authors, MeSH, PMID, DOI).
- **Practical cap for v0:** the most recent **N = 4,000** records by entrez
  date, prioritizing review/guideline/consensus publication types and the years
  2010–present. Rationale: abstracts older than ~15 years are dominated by
  superseded dietary thresholds; the eval measures whether this cap costs
  coverage, and the cap is a one-line change in `build/fetch_corpus.py`.
- **PMC open-access full text** for the guidelines/consensus subset only (small,
  high-value, and the documents users most need quoted accurately).

**Citation authority:** every literature chunk carries its **PMID** (and DOI/PMCID
when present). A literature claim Guthrie makes must cite `[PMID:xxxxxx]`.

---

## Layer 2 — The PKU Commons "market" ("knowledge of the market")

Guthrie also indexes the community's own infrastructure so he can answer
"which app is accurate?", "what does the food list say?", and "how is quality
guaranteed?" — routing to the real artifacts instead of improvising.

| Source doc | What it authorizes Guthrie to say |
|---|---|
| [`benchmark/BENCHMARK.md`](../benchmark/BENCHMARK.md) | the accuracy standard and how estimators are scored |
| [`benchmark/leaderboard.md`](../benchmark/leaderboard.md) | current measured estimator accuracy (the answer to "which is best") |
| [`docs/PEER-REVIEW.md`](../docs/PEER-REVIEW.md) | the two-layer (legal + scientific) governance model |
| [`docs/pain-points.md`](../docs/pain-points.md) | TruPKU / community pain points (what to build) |
| [`phebe/APP-SPEC.md`](../../phebe/APP-SPEC.md) | what the Phebe phe-estimator/logger app does |
| [`phebe/Phebe_Strategic_Thesis.md`](../../phebe/Phebe_Strategic_Thesis.md) | the market thesis |
| [`phebe/PROMO-SCALE-SPEC.md`](../../phebe/PROMO-SCALE-SPEC.md), [`phebe/BODY-SCALE-HANDOFF.md`](../../phebe/BODY-SCALE-HANDOFF.md) | the Bluetooth scale integration |
| Cambrooke low-protein foods table (`phebe/phe-estimator/cambrooke_low_protein_foods.json`) | living-food-list product data, itself sourced to a dated Cambrooke nutrition table |

**Citation authority:** market chunks cite `[Commons:<doc>]` (e.g.
`[Commons:leaderboard]`). Food/nutrition facts that trace to USDA FoodData
Central carry `[FDC:<id>]`; a clinician/RD sign-off is itself a citable
authority per the peer-review model.

---

## The contract (carried over from the ElizaOS Guthrie)

1. **Cite or refuse.** No fact without a retrieved source. If retrieval is weak,
   Guthrie says so and points to the blog / a clinician — he does not fabricate a
   PMID. (This is the *legal-review* standard applied to the brain.)
2. **No medical advice, diagnosis, or dosing** for an individual. Guthrie
   explains what the *literature* says and hands care decisions to clinicians.
3. **Market questions route to the benchmark**, not to opinion. "Which estimator
   is most accurate" is answered from the leaderboard, which is settled by
   measurement.
4. **No invented business/fundraising detail** (unchanged from the funnel agent).

---

## Reproducibility

- `build/fetch_corpus.py` — pulls Layer 1 from E-utilities into `build/raw/`.
- `build/build_index.py` — normalizes both layers into the hybrid index.
- One command rebuilds everything from source; `--since YYYY/MM/DD` does an
  incremental refresh so the corpus stays live without a dedicated maintainer.

**Version:** corpus v0 · **Reviewer of record:** Nina Kilbride · frozen at the
timestamp in `build/corpus_manifest_counts.json`.
