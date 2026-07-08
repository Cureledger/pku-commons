# PKU Commons ,  open infrastructure for reliable dietary phenylalanine estimation

*Claude Life Sciences Hackathon. Built by and for the PKU community.*

**Website:** enable GitHub Pages from `/docs` for the landing hub and audience routes for
[developers](docs/devs.html), [clinicians & researchers](docs/clinicians.html), and
[families](docs/families.html).

PKU (phenylketonuria) requires a very-low-protein "diet for life" managed by gram-level
phenylalanine (phe) counting. AI phe-estimator apps are appearing fast. No standard exists by
which users can judge their accuracy, and PKU apps tend to die when a solo developer moves on.
**PKU Commons is the shared, open, peer-reviewed spine** that keeps reliable phe-estimation
tools reliable.

## What's here

| Path | What it is |
|---|---|
| [`docs/`](docs/) | GitHub Pages site: hub and 3 audience routes, [peer-review model](docs/PEER-REVIEW.md), [TruPKU pain-points](docs/pain-points.md) |
| [**`docs/RELIABILITY.md`**](docs/RELIABILITY.md) | **The reliability map.** Phe-estimator reliability broken into four named, benchmark-measured gaps, each with a concrete ask. This is the contribution ask to the Claude Community. |
| [`benchmark/`](benchmark/) | The accuracy standard: [BENCHMARK.md](benchmark/BENCHMARK.md), pluggable harness, seed test set with USDA-FDC ground truth, [leaderboard](benchmark/leaderboard.md) |
| [`phe-estimator/`](phe-estimator/) | The Claude phe-estimator Skill. Uses a "think like a PKU parent" method, scored live against the benchmark |
| [`food-list/`](food-list/) | The living low-protein foods list. Cited, schema'd, one shared loader ([`foodlist.py`](food-list/foodlist.py)) |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | How to contribute: pick a reliability gap, improve it, prove it on the benchmark |
| [`scale/`](scale/) | Bluetooth kitchen-scale integration (Etekcity ESN00 + FFF0 series) _(in progress)_ |

## The two-layer quality system

- **Legal-style review** for the *method* and *food list*. Every rule and row carries a citation
  to authority (USDA FDC id, Open Food Facts code, or clinician sign-off), a version, and a
  reviewer of record. Challenges lead to issues lead to recorded resolutions, forming an audit
  trail.
- **Scientific-style review** for *estimator outputs*. Accuracy is settled by measurement against
  a public, reproducible [benchmark](benchmark/BENCHMARK.md), regression-gated in CI.

The eval guarantees quality, not the author. Apps stay trustworthy after a developer leaves. See
[`docs/PEER-REVIEW.md`](docs/PEER-REVIEW.md).

## Quick start (benchmark)

```bash
cd benchmark
python run_benchmark.py --estimator estimators.stub_estimator --report report.md
```

## Enabling the website

Push this repo to GitHub, then go to **Settings, Pages, Source: deploy from branch,
`/docs` folder**. The site is dependency-free static HTML/CSS with no build step.

## Further reading

NPKUA's [TruPKU / Voice of the Patient](https://www.npkua.org/truepku/) report catalogs the
friction of living with PKU. **Developers: we challenge you to solve some of these problems.**
See the suggested-hacks block on the [landing page](docs/index.html) and
[`docs/pain-points.md`](docs/pain-points.md).
