# Phebe Restaurant Guide — restaurant menu transparency for the low-protein diet

Part of [PKU Commons](../README.md). Starting city: **Asheville, NC**, seeded from the 15 restaurants recognized in the inaugural MICHELIN Guide American South (ceremony 2025-11-03).

## What this is

A repeatable **census of what restaurant menus actually say**, so that eating out on a phenylalanine-restricted diet stops being a research project performed from scratch by every family, at every restaurant, every time.

## What this is NOT, yet

**There is no suitability score, rating, or ranking in this repository.** No phe budget, no threshold, no percent-of-daily-allowance, no ranked tier.

That is deliberate. The census comes first and the scale comes second, because a threshold chosen before the corpus exists quietly decides what the corpus appears to say — pick one number and tapas looks workable, pick another and the same menu looks impossible. The suitability scale is defined by the project owner, argued from the real corpus.

An earlier draft did impose a scale. It sits unused and uncited in [`spec/deferred/`](spec/deferred/), kept only because one structural argument inside it survives review and should inform whatever replaces it: **what a kitchen will do is a separate axis from what its menu says, and it is knowable only by asking.**

## The one rule

> **A term match means the ingredient is NAMED on the menu. A non-match means nothing at all.**

Menu prose is marketing copy, not a recipe. Butter, stock, cream finishes, cheese garnishes, flour thickeners, egg washes and flour-dusted fries go unwritten constantly. Every row carries `completeness: "text_only_unknown"`; every rollup carries `absence_is_not_evidence: true`. Those fields exist so the caveat travels with the data instead of living in a footnote that gets dropped on the second copy-paste.

This is also why restaurant outreach is not optional: the census's job is to generate the **questions**, and only the kitchen can answer them.

## Layout

```
restaurant-guide/
├── spec/
│   ├── menu-census-v0.1.md          # the live spec: observable counts, no judgment
│   └── deferred/                    # the scoring layer, deliberately not in use
├── data/
│   ├── cities/asheville.json        # city registry
│   ├── restaurants.seed.json        # the 15 (all confirmed by name)
│   ├── negative_controls.json       # names that are NOT in the selection (regression test)
│   ├── ingredient_lexicon.json      # 17 categories, 947 terms, versioned
│   ├── lexicon_validation_press.json# 25 press-cited dishes, used to debug the lexicon
│   ├── prior_expectations.json      # pre-registered guesses, NOT app data, not displayed
│   ├── capture_manifest.json        # the work order for menu collection
│   └── snapshots.jsonl              # menu snapshot index (empty until capture)
├── src/census.py                    # census engine, stdlib only
├── tests/test_census.py             # 35 assertions, all observable
├── web/                             # Next.js directory of the 15, no scores
└── figures/
```

## Status

| Step | State |
|---|---|
| City + restaurant registry | **15 of 15** confirmed by name |
| Ingredient lexicon | v0.2, 947 terms, validated against 25 real dishes |
| Census engine + tests | working, 35/35 passing |
| Census spec | v0.1 draft, unreviewed |
| **Menu corpus** | **empty — this is the next job** |
| Suitability scale | deliberately not started |
| Accommodation data | none; requires restaurant contact |
| Next.js app | `web/` — directory of the 15, no scores |

## Two blockers for whoever picks this up

**1. Identity of the 15 is resolved.** Michelin recognized 15: 3 Bib Gourmand (Luminosa, Little Chango, Mother — Luminosa also holds a Green Star) plus 12 Recommended: Addissae, All Day Darling, Cúrate, Golden Hour, Good Hot Fish, Leo's House of Thirst, Soprana, Sunny Point Café, Table, Tall John's, **The Admiral**, **Ukiah Japanese Smokehouse**. The Admiral is a different restaurant from Leo's House of Thirst (shared ownership historically; different kitchen, menu, and address).

**2. No menus have been captured.** `data/capture_manifest.json` is the work order: 15 rows needing capture.

## Run it

```bash
python3 tests/test_census.py                 # 35 assertions
python3 tests/test_signals.py                # 37 assertions
python3 tests/test_doc_counts.py             # guards the two counts above
python3 src/capture.py --help                # capture harness

cd web && npm install && npm run dev         # directory of the 15, http://localhost:3000
```

The census engine is standard-library Python 3.8+. The directory app in `web/` is Next.js.

## Contributing

Layer 1 (knowledge — cite it, version it, name a reviewer): lexicon terms, restaurant records, menu snapshots, accommodation verifications.
Layer 2 (estimates — prove it with a number): anything derived.
See [`../docs/PEER-REVIEW.md`](../docs/PEER-REVIEW.md) and [`../CONTRIBUTING.md`](../CONTRIBUTING.md).

The lexicon's known weak spot is non-English menus — Amharic worst, then Spanish and Italian. That systematically undercounts exactly the restaurants with the least English-legible menus, which is the opposite of what this guide should do. Lexicon PRs are the highest-value contribution right now.
