#!/usr/bin/env python3
"""PKU Commons — phe-estimation benchmark harness.

Scores any estimator that implements `estimate(case) -> float | {"phe_mg": float, ...}`
against the public seed test set, using ground truth computed from USDA FoodData Central.

Usage:
    python run_benchmark.py --estimator estimators.stub_estimator
    python run_benchmark.py --estimator estimators.stub_estimator --baseline results/prev.json
    python run_benchmark.py --estimator mypkg.mymod --testset testset/seed_v0.jsonl --out results/run.json

Metrics reported per run:
    n                 number of cases scored
    mae_mg            mean absolute error (mg phe)
    medae_mg          median absolute error (mg phe)
    rmse_mg           root-mean-square error (mg phe)
    within_band_pct   % of cases whose |error| falls inside the tolerance band
    bias_mg           mean signed error (estimate - truth); + = over-estimation

Tolerance band (clinically-motivated, tunable): an estimate "passes" a case if it is
within max(ABS_TOL_MG, REL_TOL * truth) of ground truth. Defaults: 15 mg OR 15%,
whichever is larger — small absolute floor so near-zero foods aren't judged on relative
error alone.

Exit code is non-zero if --baseline is given and this run REGRESSES (mae up or
within_band_pct down beyond --tolerance). That makes the harness usable as a CI merge gate.
"""
import argparse, importlib, json, math, os, sys, datetime

ABS_TOL_MG_DEFAULT = 15.0
REL_TOL_DEFAULT = 0.15


def load_testset(path):
    cases = []
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if line:
                cases.append(json.loads(line))
    return cases


def load_estimator(dotted):
    """Import estimators.foo (relative to this dir) or a fully-qualified module."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    mod = importlib.import_module(dotted)
    if not hasattr(mod, "estimate"):
        raise SystemExit(f"Estimator module '{dotted}' has no `estimate(case)` function.")
    return mod.estimate


def coerce(result):
    if isinstance(result, dict):
        return float(result.get("phe_mg", 0.0)), result.get("meta")
    return float(result), None


def in_band(err_abs, truth, abs_tol, rel_tol):
    return err_abs <= max(abs_tol, rel_tol * truth)


def score(estimate_fn, cases, abs_tol, rel_tol):
    per_case = []
    for c in cases:
        truth = float(c["expected_phe_mg"])
        try:
            est, meta = coerce(estimate_fn(c))
            err = None
        except Exception as e:  # a crash is a failed case, not a crashed run
            est, meta, err = None, None, f"{type(e).__name__}: {e}"
        if err is None:
            signed = est - truth
            abs_err = abs(signed)
            passed = in_band(abs_err, truth, abs_tol, rel_tol)
        else:
            signed = abs_err = None
            passed = False
        per_case.append({
            "id": c["id"], "name": c.get("name"),
            "truth_mg": truth, "estimate_mg": est,
            "signed_err_mg": None if signed is None else round(signed, 1),
            "abs_err_mg": None if abs_err is None else round(abs_err, 1),
            "passed": passed, "error": err, "meta": meta,
        })
    scored = [p for p in per_case if p["abs_err_mg"] is not None]
    n = len(per_case)
    if scored:
        errs = [p["abs_err_mg"] for p in scored]
        signs = [p["signed_err_mg"] for p in scored]
        mae = sum(errs) / len(errs)
        rmse = math.sqrt(sum(e * e for e in errs) / len(errs))
        srt = sorted(errs)
        medae = srt[len(srt) // 2] if len(srt) % 2 else (srt[len(srt)//2 - 1] + srt[len(srt)//2]) / 2
        bias = sum(signs) / len(signs)
    else:
        mae = rmse = medae = bias = None
    within = 100.0 * sum(1 for p in per_case if p["passed"]) / n if n else 0.0
    metrics = {
        "n": n, "n_scored": len(scored), "n_crashed": n - len(scored),
        "mae_mg": None if mae is None else round(mae, 2),
        "medae_mg": None if medae is None else round(medae, 2),
        "rmse_mg": None if rmse is None else round(rmse, 2),
        "bias_mg": None if bias is None else round(bias, 2),
        "within_band_pct": round(within, 1),
        "tolerance_band": {"abs_tol_mg": abs_tol, "rel_tol": rel_tol},
    }
    return metrics, per_case


def render_report(run):
    m = run["metrics"]
    lines = []
    lines.append(f"# Benchmark report — `{run['estimator']}`\n")
    lines.append(f"- **Run:** {run['run_utc']}")
    lines.append(f"- **Test set:** `{run['testset']}` ({m['n']} cases)")
    lines.append(f"- **Tolerance band:** ±max({m['tolerance_band']['abs_tol_mg']} mg, "
                 f"{int(m['tolerance_band']['rel_tol']*100)}% of truth)\n")
    lines.append("## Metrics\n")
    lines.append("| metric | value |")
    lines.append("|---|---|")
    lines.append(f"| MAE (mg) | {m['mae_mg']} |")
    lines.append(f"| Median AE (mg) | {m['medae_mg']} |")
    lines.append(f"| RMSE (mg) | {m['rmse_mg']} |")
    lines.append(f"| Bias (mg, +over) | {m['bias_mg']} |")
    lines.append(f"| Within band | {m['within_band_pct']}% |")
    lines.append(f"| Crashed cases | {m['n_crashed']} |\n")
    lines.append("## Per-case\n")
    lines.append("| id | case | truth mg | est mg | err mg | pass |")
    lines.append("|---|---|--:|--:|--:|:--:|")
    for p in run["per_case"]:
        est = "—" if p["estimate_mg"] is None else p["estimate_mg"]
        err = "—" if p["abs_err_mg"] is None else p["abs_err_mg"]
        chk = "✅" if p["passed"] else "❌"
        nm = (p["name"] or "")[:40]
        lines.append(f"| {p['id']} | {nm} | {p['truth_mg']} | {est} | {err} | {chk} |")
    return "\n".join(lines) + "\n"


def check_regression(cur, base, tol):
    """Return (regressed: bool, notes: list)."""
    notes = []
    regressed = False
    if base is None:
        return False, ["no baseline provided"]
    bm, cm = base["metrics"], cur["metrics"]
    if bm.get("mae_mg") is not None and cm.get("mae_mg") is not None:
        if cm["mae_mg"] > bm["mae_mg"] * (1 + tol):
            regressed = True
            notes.append(f"MAE regressed: {bm['mae_mg']} -> {cm['mae_mg']} mg")
        else:
            notes.append(f"MAE ok: {bm['mae_mg']} -> {cm['mae_mg']} mg")
    if cm["within_band_pct"] < bm["within_band_pct"] * (1 - tol):
        regressed = True
        notes.append(f"within-band regressed: {bm['within_band_pct']}% -> {cm['within_band_pct']}%")
    else:
        notes.append(f"within-band ok: {bm['within_band_pct']}% -> {cm['within_band_pct']}%")
    return regressed, notes


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser(description="PKU Commons phe-estimation benchmark")
    ap.add_argument("--estimator", required=True, help="dotted module exposing estimate(case)")
    ap.add_argument("--testset", default=os.path.join(here, "testset", "seed_v0.jsonl"))
    ap.add_argument("--out", default=None, help="write run JSON here")
    ap.add_argument("--report", default=None, help="write markdown report here")
    ap.add_argument("--baseline", default=None, help="prior run JSON to check regression against")
    ap.add_argument("--abs-tol-mg", type=float, default=ABS_TOL_MG_DEFAULT)
    ap.add_argument("--rel-tol", type=float, default=REL_TOL_DEFAULT)
    ap.add_argument("--tolerance", type=float, default=0.0,
                    help="fractional slack allowed before a metric counts as a regression")
    args = ap.parse_args()

    cases = load_testset(args.testset)
    estimate_fn = load_estimator(args.estimator)
    metrics, per_case = score(estimate_fn, cases, args.abs_tol_mg, args.rel_tol)

    run = {
        "estimator": args.estimator,
        "testset": os.path.relpath(args.testset, here),
        "run_utc": datetime.datetime.utcnow().isoformat() + "Z",
        "metrics": metrics,
        "per_case": per_case,
    }

    base = json.load(open(args.baseline)) if args.baseline else None
    regressed, notes = check_regression(run, base, args.tolerance)
    run["regression"] = {"regressed": regressed, "notes": notes}

    if args.out:
        os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
        json.dump(run, open(args.out, "w"), indent=2)
    report_md = render_report(run)
    if args.report:
        os.makedirs(os.path.dirname(args.report) or ".", exist_ok=True)
        open(args.report, "w").write(report_md)

    print(report_md)
    print("Regression check:", "; ".join(notes))
    if regressed:
        print("REGRESSION DETECTED — failing.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
