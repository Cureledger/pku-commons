# PKU Market Atlas

Phenylketonuria as a **market**, not a biology. This is an open, cited dataset plus a browsable
dashboard ([`../market.html`](../market.html)) that surfaces the whole commercial and policy surface
of PKU so investors and innovators can see where the opportunities are. No biomedical or
mechanism-of-action science lives here by design.

## What's covered

| Dataset | File | Rows | What it maps |
|---|---|--:|---|
| US coverage | [`data/geo_us.json`](data/geo_us.json) | 51 | Every state + DC: does the law mandate insurance coverage of PKU formula and low-protein foods, or do families pay out of pocket |
| Global | [`data/geo_intl.json`](data/geo_intl.json) | 23 | Top ~20 country markets: newborn-screening reach, who pays, drug access, undiagnosed tail |
| Medical foods | [`data/medical_foods.json`](data/medical_foods.json) | 44 | Low-protein staples and specialty foods by brand, category, geography, price |
| Formulas | [`data/formulas.json`](data/formulas.json) | 46 | Amino-acid and GMP protein substitutes across life stage and format |
| Drugs & pipeline | [`data/drugs.json`](data/drugs.json) | 22 | Approved therapies, pipeline candidates, and market-relevant trials |
| Apps | [`data/apps.json`](data/apps.json) | 17 | The phe-counting and diet software, its lone-maintainer survival problem, and the AI-estimator entrants |
| Medical devices | [`data/devices.json`](data/devices.json) | 23 | The hardware layer, led by the missing home phe monitor (the biggest disruption gap in PKU) |
| Companies | [`data/manufacturers.json`](data/manufacturers.json) | 27 | Who the players are and who owns whom |
| Clinics & dietitians | [`data/clinics.json`](data/clinics.json) | 46 | The care-delivery layer and its access gaps |
| Dental | [`data/dental.json`](data/dental.json) | 17 | The diet's toll on teeth and the missing PKU-aware dental care and products |
| Mental health | [`data/mental_health.json`](data/mental_health.json) | 20 | High phe driving neuropsychiatric symptoms, and providers medicating instead of addressing diet |
| Restaurants & schools | [`data/restaurants_schools.json`](data/restaurants_schools.json) | 24 | Two near-empty consumer markets |
| Money | [`data/payers.json`](data/payers.json) | 25 | Market size, reimbursement, and the legislation that could unlock it |
| Prediction markets | [`data/markets.json`](data/markets.json) | 19 | Atlas questions written as tradeable markets, each anchored to a data point with an objective resolution source |
| Advocacy & legal | [`data/advocacy_legal.json`](data/advocacy_legal.json) | 29 | Patient organizations and the litigation shaping access |

Total: **433 records** across fifteen datasets.

## Provenance rules

Every record carries a `sources` array and a `confidence` flag:

- `sourced`: backed by a citation (a real URL in `sources`).
- `estimate`: reasoned from public inputs, not a single source (e.g. state patient counts scaled
  from national prevalence).
- `unknown`: placeholder that needs a contributor.

The envelope and per-record shape are documented in [`data/SCHEMA.md`](data/SCHEMA.md). The dashboard
reads these files directly, so a data fix shows up on the page with no code change.

## Known limits

- Coverage-mandate statutes are anchored to the 2016 Catalyst Center state survey (the most recent
  comprehensive source) cross-checked against NPKUA and National PKU News. Statutes change;
  re-confirm current text before any high-stakes use.
- Patient counts are prevalence-scaled estimates, not censuses.
- Market-size figures are analyst estimates that vary widely by methodology; the Money tab shows the
  range and its sources rather than a single number.
- Clinic and dietitian lists are representative, not a complete registry (none exists publicly).

## Contribute

Fix a row, add a source, upgrade an `estimate` to `sourced`, or extend coverage. The datasets are
plain JSON in [`data/`](data/). Open a pull request against
[Cureledger/pku-commons](https://github.com/Cureledger/pku-commons).

This atlas is a market map for research and opportunity-scouting. It is not investment, medical, or
legal advice.
