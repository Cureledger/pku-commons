#!/usr/bin/env python3
"""Reproducibility meter — run an estimator N times and report the spread of its score.

This measures reliability **gap #4** (execution variance): how much an estimator's accuracy
wobbles run-to-run on the *same* inputs. A deterministic estimator (the rubric, a plain-Python
model) scores identically every run → spread 0. A model-backed estimator (the live Claude Skill)
does not — and that spread is itself a reliability defect a family feels when the same food logs
a different number twice.

It changes nothing about any estimator. It only re-runs the existing benchmark scorer and
summarizes the resulting metrics. Use it to check whether a prompt/method change to
`phe-estimator/SKILL.md` reduced variance:

    # deterministic estimators (runs from a plain shell; spread should be 0 = reproducible)
    python variance.py --estimator estimators.rubric_estimator --runs 5

    # the live Claude Skill needs a model caller. Easiest: run inside a Claude Science kernel:
    #   import variance
    #   from estimators import claude_skill
    #   claude_skill.set_model_caller(lambda s, u: host.llm(u, system=s)["text"])
    #   variance.run_variance(claude_skill.estimate, variance.load_cases(), runs=5)
    # or wire your own provider's client the same way, then run this script.

No third-party dependencies — standard library only, same as the harness.
"""
import argparse, json, math, os, statistics, sys, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import run_benchmark as rb


def load_cases(testset=None):
    here = os.path.dirname(os.path.abspath(__file__))
    return rb.load_testset(testset or os.path.join(here, "testset", "seed_v0.jsonl"))


def run_variance(estimate_fn, cases, runs=5, abs_tol=rb.ABS_TOL_MG_DEFAULT,
                 rel_tol=rb.REL_TOL_DEFAULT):
    """Score `estimate_fn` `runs` times over `cases`; return per-run metrics + spread summary."""
    per_run = []
    for _ in range(runs):
        metrics, _pc = rb.score(estimate_fn, cases, abs_tol, rel_tol)
        per_run.append(metrics)

    def spread(key):
        vals = [m[key] for m in per_run if m.get(key) is not None]
        if not vals:
            return None
        return {
            "runs": vals,
            "min": round(min(vals), 2), "max": round(max(vals), 2),
            "mean": round(statistics.mean(vals), 2),
            "stdev": round(statistics.pstdev(vals), 2) if len(vals) > 1 else 0.0,
            "range": round(max(vals) - min(vals), 2),
        }

    summary = {k: spread(k) for k in ("mae_mg", "within_band_pct", "bias_mg", "rmse_mg")}
    deterministic = (summary["mae_mg"] is not None and summary["mae_mg"]["range"] == 0.0)
    return {"n_runs": runs, "n_cases": len(cases), "deterministic": deterministic,
            "spread": summary, "per_run": per_run}


def render(report):
    s = report["spread"]
    L = []
    L.append(f"reproducibility over {report['n_runs']} runs on {report['n_cases']} cases "
             f"({'DETERMINISTIC' if report['deterministic'] else 'NON-deterministic'}):")
    L.append(f"  {'metric':<16} {'min':>8} {'mean':>8} {'max':>8} {'range':>8} {'stdev':>8}")
    for key, label in (("mae_mg", "MAE (mg)"), ("within_band_pct", "within-band %"),
                       ("bias_mg", "bias (mg)"), ("rmse_mg", "RMSE (mg)")):
        d = s[key]
        if d:
            L.append(f"  {label:<16} {d['min']:>8} {d['mean']:>8} {d['max']:>8} "
                     f"{d['range']:>8} {d['stdev']:>8}")
    return "\n".join(L)


def main():
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    ap = argparse.ArgumentParser(description="Reproducibility meter (reliability gap #4)")
    ap.add_argument("--estimator", required=True, help="dotted module exposing estimate(case)")
    ap.add_argument("--runs", type=int, default=5)
    ap.add_argument("--testset", default=None)
    ap.add_argument("--out", default=None, help="write the variance report JSON here")
    ap.add_argument("--abs-tol-mg", type=float, default=rb.ABS_TOL_MG_DEFAULT)
    ap.add_argument("--rel-tol", type=float, default=rb.REL_TOL_DEFAULT)
    ap.add_argument("--model", default=os.environ.get("PKU_BENCH_MODEL"),
                    help="identify the model/engine under test (e.g. 'claude-sonnet-4', "
                         "'cursor:gpt-4o'). Defaults to the PKU_BENCH_MODEL env var. This is the "
                         "precision test — the result is meaningless without knowing WHICH model "
                         "was re-run, so set this for any model-backed estimator.")
    ap.add_argument("--runner", default=os.environ.get("PKU_BENCH_RUNNER"),
                    help="who/what ran this (e.g. 'claude-code', 'cursor', a handle). "
                         "Defaults to the PKU_BENCH_RUNNER env var.")
    args = ap.parse_args()

    estimate_fn = rb.load_estimator(args.estimator)
    model_label = rb.resolve_model(estimate_fn, args.model)
    cases = load_cases(args.testset)
    report = run_variance(estimate_fn, cases, args.runs, args.abs_tol_mg, args.rel_tol)
    report["estimator"] = args.estimator
    report["model"] = model_label
    report["runner"] = args.runner
    report["run_utc"] = datetime.datetime.utcnow().isoformat() + "Z"

    print(f"model / engine: {report['model']}"
          + (f"  (runner: {report['runner']})" if report['runner'] else ""))
    print(render(report))
    if args.out:
        os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
        json.dump(report, open(args.out, "w"), indent=2)
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
