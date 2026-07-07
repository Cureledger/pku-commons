# PKU Commons — TODO

Running list of outstanding work. Contributions welcome — see the audience pages and
[PEER-REVIEW.md](docs/PEER-REVIEW.md).

## Site

- [ ] **No-login feedback form.** Feedback currently routes through pre-filled GitHub Issues
  (works today, but requires a free GitHub account — friction for families/clinicians).
  Replace with a real no-login web form once a form service is chosen and verified to embed
  on GitHub Pages. Decision deferred: don't wire an endpoint that hasn't been integration-tested,
  since a mis-wired form silently drops submissions. Affects the feedback section on
  `docs/families.html`, `docs/clinicians.html`, `docs/devs.html`.
- [ ] Fill real form endpoint once chosen (see above).

## Benchmark / data

- [ ] Expand seed test set beyond the 18 v0 cases using the full USDA FDC dataset
  (already downloaded separately) — more composites and branded/packaged labels.
- [ ] Add the Claude Skill adapter (`benchmark/estimators/claude_skill.py`) and score it
  against the test set; post its row on the leaderboard.
- [ ] Clinician-defined tolerance bands per phe range.
- [ ] GitHub Actions workflow to run the benchmark on every PR and post deltas.

## Governance

- [ ] Generate the peer-review matrix once the Skill is ready to test.
- [ ] Clinician / RD reviewer roster and sign-off log.
