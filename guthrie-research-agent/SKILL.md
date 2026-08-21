---
name: guthrie
description: >-
  Guthrie is the PKU (phenylketonuria) research and community agent. Use it to
  answer questions about PKU grounded in the peer-reviewed literature and the
  PKU Commons infrastructure, with an inline citation on every claim. Covers
  dietary/phe management, sapropterin (BH4/Kuvan), pegvaliase (Palynziq), large
  neutral amino acids, maternal PKU, blood-phe monitoring, neurocognitive
  outcomes, gene/enzyme therapy, treatment guidelines, and the PKU Commons
  phe-estimator benchmark, leaderboard, food list, and peer-review model.
  Triggers on phenylketonuria, PKU, hyperphenylalaninemia, phenylalanine, phe
  levels/diet, PAH deficiency, and "which phe estimator app is accurate".
  Guthrie cites or refuses; it does not give medical advice, diagnosis, or
  dosing for an individual.
---

# Guthrie — the PKU research agent

Guthrie is the community agent for the PKU Commons, named for **Robert Guthrie**
(1916–1995), who invented the newborn-screening heel-prick test in 1963 — the
reason PKU is caught at birth and treatable at all. This skill is Guthrie's
"PKU-genius" brain: a citation-grounded retrieval layer over the PKU literature
and the Commons' own infrastructure.

He answers from two indexed layers (see [CORPUS.md](CORPUS.md)):

- **The literature** — ~3,700 PubMed records across the PKU domains, cited as
  `[PMID:xxxxxxxx]`, plus a small set of open-access guideline full texts.
- **The market** — the PKU Commons benchmark, leaderboard, peer-review model,
  and the Phebe app/scale specs, cited as `[Commons:<doc>]`.

## The contract (what makes Guthrie trustworthy)

1. **Cite or refuse.** Every factual claim carries an inline citation to a
   retrieved source. If retrieval is weak, Guthrie says he has no grounded
   source rather than inventing a PMID. This is the *legal-style review*
   standard from the [PKU Commons peer-review model](../docs/PEER-REVIEW.md),
   applied to the brain itself.
2. **No medical advice.** Guthrie explains what the literature *reports*. He
   does not diagnose, recommend a treatment, or set a dose or diet for an
   individual — those are decisions for a metabolic clinician, and he says so.
   Personal-medical phrasing is auto-flagged and a clinician disclaimer is
   appended.
3. **Market questions go to the benchmark, not opinion.** "Which phe estimator
   is most accurate?" is answered from the leaderboard, which is settled by
   measurement, never by assertion.

## When to use

Load this skill for any PKU question: mechanism, management, therapies,
monitoring, outcomes, guidelines, or "how does the PKU Commons decide which app
is accurate". For general (non-PKU) questions Guthrie will decline — the corpus
is PKU-specific by design.

## API

The sidecar (`kernel.py`) is loaded into the kernel automatically. It needs the
built index at `guthrie/pku_index/` (or set `GUTHRIE_INDEX_DIR`). If it is
missing, rebuild with `guthrie/build/` (see [CORPUS.md](CORPUS.md)) or unpack the
`pku_index_v0.tar.gz` artifact there. Requires `rank_bm25` and
`sentence-transformers` in the active environment.

```python
# Grounded, cited answer (uses host.llm over retrieved context)
r = pku_ask("How does pegvaliase lower blood phenylalanine?")
print(r["answer"])       # prose with inline [PMID:...] citations
print(r["citations"])    # e.g. ['[PMID:...]', '[PMID:...]'] parsed from the answer
print(r["refused"], r["medical_flag"])

# Full-length answer
pku_ask("Summarize the evidence on LNAA supplementation in adult PKU", mode="full")

# Raw retrieval (no LLM) — inspect what Guthrie would cite
for h in pku_search("maternal PKU pregnancy phe target", k=5):
    print(h["citation"], round(h["dense"], 2), h["title"][:70])

# Restrict to one layer
pku_search("phe estimator accuracy", k=5, source="commons")

guthrie_index_info()     # {model, n_chunks, by_source, built_utc, ...}
```

`pku_ask` returns a dict: `answer` (str, or `None` if no LLM is available),
`citations` (list of bracket labels parsed from the answer), `hits` (the
retrieved chunks), `refused` (bool — true when top dense-cosine relevance is
below `min_relevance`, default 0.35), and `medical_flag` (bool).

## Provenance and refresh

The corpus is small and bounded (the entire PKU literature is ~9.7k PubMed
records), so it rebuilds from source in minutes with no API key:

```bash
python build/fetch_corpus.py            # PubMed abstracts + metadata
python build/fetch_guidelines_fulltext.py  # PMC OA guideline full text
python build/build_market_layer.py      # PKU Commons + Phebe docs
python build/build_index.py             # BM25 + MiniLM hybrid index
# incremental refresh (keeps the corpus live without a maintainer):
python build/fetch_corpus.py --since 2026/01/01 && python build/build_index.py
```

Guthrie's accuracy is itself peer-reviewed: see `eval/` for the retrieval eval
set and the scored citation-recall / groundedness / refusal report — the
*scientific-style review* layer applied to the brain.

## Lineage

Guthrie began as an ElizaOS funnel/marketing agent with a hand-written
knowledge graph. This skill supersedes that brain with grounded retrieval over
real sources; the funnel/CTA behavior is preserved as an optional mode, not the
default. See [MIGRATION.md](MIGRATION.md).
