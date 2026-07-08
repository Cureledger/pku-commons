# PKU Commons: TODO

Running list of outstanding work. Contributions are welcome. See the audience pages and
[PEER-REVIEW.md](docs/PEER-REVIEW.md).

## Site

- [x] **No-login feedback form.** Live Tally form (`tally.so/r/EkYaAL`) embedded inline on
  `docs/families.html` and `docs/clinicians.html`. No login required. A one-line GitHub
  Issues fallback link remains under each form for anyone who wants their feedback on the
  public record. `docs/devs.html` intentionally keeps GitHub Issues as its primary channel.
  _Verify on preview that the embed renders. The GitHub fallback covers the case where the
  Tally script is blocked._

## Benchmark / data

- [ ] Expand the seed test set beyond the 18 v0 cases using the full USDA FDC dataset
  (already downloaded separately). Add more composites and branded and packaged labels.
- [x] Add the Claude Skill adapter (`benchmark/estimators/claude_skill.py`) and score it
  against the test set. Post its row on the leaderboard. _(Scored live via `host.llm`,
  `claude-opus-4-8`. Harness generated `results/claude_skill_v0.json`. On the leaderboard.)_
- [ ] Clinician-defined tolerance bands per phe range.
- [x] GitHub Actions workflow to run the benchmark on every PR and post deltas.
  _(`.github/workflows/benchmark.yml`: regression gate vs `results/baseline_v0.json` +
  food-list Layer-1 validation; report posted to job summary)_

## Governance

- [x] Generate the peer-review matrix once the Skill is ready to test.
  _(`phe-estimator/PEER-REVIEW-MATRIX.md`; reliability gaps in `docs/RELIABILITY.md`)_
- [ ] Clinician / RD reviewer roster and sign-off log.
