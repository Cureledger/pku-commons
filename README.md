# PKU Commons — open infrastructure for reliable dietary phenylalanine estimation

*Claude Life Sciences Hackathon · built by and for the PKU community.*

**Website:** enable GitHub Pages from `/docs` → landing hub + audience routes for
[developers](docs/devs.html), [clinicians & researchers](docs/clinicians.html), and
[families](docs/families.html).

PKU (phenylketonuria) requires a very-low-protein "diet for life" managed by gram-level
phenylalanine (phe) counting. AI phe-estimator apps are appearing fast — but there is no
standard by which users can judge their accuracy, and PKU apps tend to die when a solo
developer moves on. **PKU Commons is the shared, open, peer-reviewed spine** so that reliable
phe-estimation tools exist and stay reliable.

## What's here

| Path | What it is |
|---|---|
| [`docs/`](docs/) | GitHub Pages site: hub + 3 audience routes, [peer-review model](docs/PEER-REVIEW.md), [TruPKU pain-points](docs/pain-points.md) |
| [`benchmark/`](benchmark/) | The accuracy standard: [BENCHMARK.md](benchmark/BENCHMARK.md), pluggable harness, seed test set with USDA-FDC ground truth, [leaderboard](benchmark/leaderboard.md) |
| [`phe-estimator/`](phe-estimator/) | The Claude phe-estimator Skill — "think like a PKU parent" method _(in progress)_ |
| [`food-list/`](food-list/) | The living low-protein foods list — USDA / Open Food Facts knowledge graph _(in progress)_ |
| [`scale/`](scale/) | Bluetooth kitchen-scale integration (Etekcity ESN00 + FFF0 series) _(in progress)_ |

## The two-layer quality system

- **Legal-style review** for the *method* and *food list*: every rule/row carries a citation to
  authority (USDA FDC id / Open Food Facts code / clinician sign-off), a version, and a reviewer
  of record. Challenges → issues → recorded resolutions = an audit trail.
- **Scientific-style review** for *estimator outputs*: accuracy is settled by measurement against
  a public, reproducible [benchmark](benchmark/BENCHMARK.md), regression-gated in CI.

Quality is guaranteed by the eval, not the author — so apps stay trustworthy even after a
developer leaves. See [`docs/PEER-REVIEW.md`](docs/PEER-REVIEW.md).

## Quick start (benchmark)

```bash
cd benchmark
python run_benchmark.py --estimator estimators.stub_estimator --report report.md
```

## Enabling the website

Push this repo to GitHub, then **Settings → Pages → Source: deploy from branch →
`/docs` folder**. The site is dependency-free static HTML/CSS; no build step.

## Further reading

NPKUA's [TruPKU / Voice of the Patient](https://www.npkua.org/truepku/) report catalogs the
friction of living with PKU. **Devs: we challenge you to solve some of these** — see the
suggested-hacks block on the [landing page](docs/index.html) and [`docs/pain-points.md`](docs/pain-points.md).
