# PKU Commons — TODO

Running list of outstanding work. Contributions welcome — see the audience pages and
[PEER-REVIEW.md](docs/PEER-REVIEW.md).

## Site

- [x] **No-login feedback form.** Live Tally form (`tally.so/r/EkYaAL`) embedded inline on
  `docs/families.html` and `docs/clinicians.html` — no login required. A one-line GitHub
  Issues fallback link remains under each form for anyone who wants their feedback on the
  public record. `docs/devs.html` intentionally keeps GitHub Issues as its primary channel.
  _Verify on preview that the embed renders; the GitHub fallback covers the case where the
  Tally script is blocked._

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
