# PKU Commons: open infrastructure for reliable dietary phenylalanine estimation

*Claude Life Sciences Hackathon. Built by and for the PKU community.*

Website: enable GitHub Pages from `/docs` for the landing hub and its audience routes for
[developers](docs/devs.html), [clinicians and researchers](docs/clinicians.html), and
[families](docs/families.html).

PKU (phenylketonuria) requires a very-low-protein diet for life, managed by counting
phenylalanine (phe) at the gram level. AI phe-estimator apps are arriving fast. There is no
standard for judging how accurate any of them is, and PKU apps tend to die when a solo
developer moves on. PKU Commons is the shared, open, peer-reviewed spine that keeps reliable
phe-estimation tools reliable after any one developer leaves.

## What's here

| Path | What it is |
|---|---|
| [`docs/`](docs/) | GitHub Pages site: hub and 3 audience routes, [peer-review model](docs/PEER-REVIEW.md), [TruPKU pain-points](docs/pain-points.md) |
| [`docs/RELIABILITY.md`](docs/RELIABILITY.md) | The reliability map. Phe-estimator reliability broken into four named, benchmark-measured gaps, each with a concrete task for the Claude Community to pick up. |
| [`benchmark/`](benchmark/) | The accuracy standard: [BENCHMARK.md](benchmark/BENCHMARK.md), pluggable harness, seed test set with USDA-FDC ground truth, [leaderboard](benchmark/leaderboard.md) |
| [`phe-estimator/`](phe-estimator/) | The Claude phe-estimator Skill. Uses a "think like a PKU parent" method, scored live against the benchmark |
| [`food-list/`](food-list/) | The living low-protein foods list. Cited, schema'd, one shared loader ([`foodlist.py`](food-list/foodlist.py)) |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | How to contribute: pick a reliability gap, improve it, prove it on the benchmark |
| [`scale/`](scale/) | Bluetooth kitchen-scale integration (Etekcity ESN00 + FFF0 series) _(in progress)_ |

## The two-layer quality system

The method and the food list get a legal-style review. Every rule and every row carries a
citation to authority (a USDA FDC id, an Open Food Facts code, or a clinician sign-off), a
version, and a reviewer of record. A challenge opens an issue, the issue produces a recorded
resolution, and the resolutions form an audit trail.

Estimator outputs get a scientific-style review. Accuracy is settled by measurement against a
public, reproducible [benchmark](benchmark/BENCHMARK.md), with a regression gate in CI.

The evaluation guarantees quality, so an app stays trustworthy after its developer leaves. See
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
friction of living with PKU. If you build, several of those problems are yours to take. The
suggested hacks are on the [landing page](docs/index.html) and in
[`docs/pain-points.md`](docs/pain-points.md).
