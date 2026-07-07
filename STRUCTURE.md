# PKU Commons — target monorepo layout

Built fresh for the Claude Life Sciences Hackathon (no reference-repo reads).
Drop this tree into a fresh public GitHub repo (e.g. `Cureledger/pku-commons`)
and enable GitHub Pages from the `/docs` folder on the default branch.

```
pku-commons/
├── README.md                     # main project README (from pasted stub)
├── docs/                         # GitHub Pages site  (Settings → Pages → /docs)
│   ├── index.html                # hub: intro + 3-way audience router + TruPKU hacks
│   ├── devs.html                 # developer route
│   ├── clinicians.html           # nutritionist / researcher / clinician route
│   ├── families.html             # family / patient route
│   ├── PEER-REVIEW.md            # two-layer QC governance model
│   ├── pain-points.md            # TruPKU pain points, source of record
│   └── assets/
│       └── styles.css            # shared site styling
├── benchmark/                    # the accuracy standard  (scientific spine)
│   ├── BENCHMARK.md              # how to run + reproducibility statement
│   ├── schema.json               # test-case JSON schema
│   ├── run_benchmark.py          # pluggable harness (score any estimator)
│   ├── estimators/
│   │   └── stub_estimator.py     # reference/dummy estimator for demo
│   ├── testset/
│   │   └── seed_v0.jsonl         # seed cases w/ USDA-FDC / OFF phe ground truth
│   └── leaderboard.md            # KPI #1: performance over time / across apps
├── phe-estimator/                # Claude Skill (built 7/8)
├── food-list/                    # living low-protein foods list
└── scale/                        # bluetooth scale integration
```

## Notes
- Site is dependency-free static HTML/CSS — no Jekyll build needed; Pages serves
  `/docs` as-is. `.md` files render on GitHub and are linked from the pages.
- The benchmark is the load-bearing artifact: it is the "standard" that lets
  users/clinicians/researchers judge accuracy, the CI gate that keeps apps
  trustworthy after a dev leaves, and the KPI #1 leaderboard.
