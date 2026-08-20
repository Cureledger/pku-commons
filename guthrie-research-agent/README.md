# Guthrie — the PKU research agent

*Part of [PKU Commons](../README.md). Named for Robert Guthrie (1916–1995), who
invented the newborn-screening heel-prick test in 1963.*

Guthrie answers PKU questions grounded in the peer-reviewed literature and the
PKU Commons infrastructure, with an inline citation on every claim. He is a
Claude Skill: a portable retrieval brain plus a persona contract. He **cites or
refuses** — he never asserts a fact he cannot ground in a retrieved source, and
he does not give medical advice, diagnosis, or dosing for an individual.

## Why this exists

PKU apps and PKU information sources tend to die when a solo developer moves on,
and there has been no standard for judging whether an AI answer about PKU is
trustworthy. Guthrie is built so that a reliable, *checkable* PKU knowledge
agent exists and stays reliable even without a dedicated maintainer:

- the corpus rebuilds from public sources with one command (no API key);
- every answer carries a citation a clinician or researcher can verify;
- Guthrie's own accuracy is peer-reviewed by a reproducible eval, not asserted.

This is the same two-layer quality model the rest of PKU Commons uses
([legal-style review of the knowledge, scientific-style review of the
outputs](../docs/PEER-REVIEW.md)) — turned on the agent itself.

## What's here

| Path | What it is |
|---|---|
| [`SKILL.md`](SKILL.md) | the skill: persona, contract, `pku_ask`/`pku_search` API |
| [`kernel.py`](kernel.py) | the retrieval brain (hybrid BM25 + dense, cite-or-refuse) |
| [`CORPUS.md`](CORPUS.md) | the corpus manifest — exactly what Guthrie knows and on whose authority |
| [`build/`](build/) | reproducible fetch + index scripts (one command rebuilds) |
| [`eval/`](eval/) | the retrieval eval set + scored report (the scientific-review layer) |
| [`MIGRATION.md`](MIGRATION.md) | how this supersedes the ElizaOS Guthrie |
| `pku_index/` | the built index (or unpack `pku_index_v0.tar.gz` here) |

## Quick start

```bash
# 1. environment
python -m venv .venv && ./.venv/bin/pip install rank_bm25 sentence-transformers numpy

# 2. build the brain from source (a few minutes, no API key)
python build/fetch_corpus.py                 # PubMed abstracts + metadata
python build/fetch_guidelines_fulltext.py    # PMC open-access guideline full text
python build/build_market_layer.py           # PKU Commons + Phebe docs
python build/build_index.py                  # BM25 + MiniLM hybrid index -> pku_index/

# 3. use it (in a Claude Science session, the skill loads kernel.py for you)
python -c "import kernel; print(kernel.pku_ask('How does pegvaliase lower blood phe?')['answer'])"
```

## The numbers

- **Corpus:** ~3,700 PubMed abstracts (1998–2026) + 26 guideline full-text
  sections + 74 PKU Commons / Phebe chunks = **3,800 indexed chunks**. The whole
  PKU literature is only ~9.7k records, so this is a complete-enough slice that
  fits in one local index (~10 MB) and builds in ~35 s on CPU.
- **Eval:** 85% citation recall (conservative), **100% groundedness — zero
  fabricated citations**, 100% correct medical + out-of-scope refusal. See
  [`eval/report.md`](eval/report.md).

## Staying live without a maintainer

```bash
# incremental refresh: pull only records added since a date, rebuild the index
python build/fetch_corpus.py --since 2026/01/01 && python build/build_index.py
python eval/run_eval.py   # confirm the score held (regression gate)
```

Because the corpus is small and the build is one command, keeping Guthrie
current is a cron job, not a project. Anyone in the community can run it.
