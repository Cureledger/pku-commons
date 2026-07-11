"""Score an agent-filled worksheet against USDA ground truth.

The phe-estimator method (phe-estimator/SKILL.md) asks a model to do ONE judgment:
classify each food into a phe-source class. Code then applies the fixed coefficient
(phe per g protein) and multiplies by label protein. This scorer runs that split so the
test measures the model's real skill (classification) — not an invented number.

Answer files are JSONL. Each line is either:
  {"id": "...", "phe_source_class": "cereal protein"}   <- preferred: the class you chose
  {"id": "...", "phe_mg": 90.0}                          <- or a direct number
Pass 2+ answer files to also measure reproducibility (same food, same answer every run).
A food left blank counts as a FAILURE (denominator is always the full testset).

    python score_worksheet.py --answers run1.jsonl run2.jsonl run3.jsonl \
        --testset low_protein_usda.jsonl --model <name> --out results/<name>.json

--model is required so the result records which model produced it. Std-lib only.
"""
import argparse, json, os, sys, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import run_benchmark as rb

# the embedded coefficient table (same source the SKILL cites)
_T = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "..", "phe-estimator", "phe_per_g_protein.json")))
COEFFICIENT = {k: v["phe_mg_per_g_protein"] for k, v in _T["classes"].items()}


def load_answers(path):
    """Return {id: phe_mg}. Classes are converted to a number via protein*coefficient
    at scoring time (we need the case protein), so store the raw answer here."""
    ans = {}
    with open(path) as f:
        for ln in f:
            ln = ln.strip()
            if not ln:
                continue
            o = json.loads(ln)
            if "id" not in o:
                continue
            if o.get("phe_source_class") in COEFFICIENT:
                ans[o["id"]] = ("class", o["phe_source_class"])
            elif o.get("phe_mg") is not None:
                ans[o["id"]] = ("mg", round(float(o["phe_mg"]), 1))
    return ans


def resolve(ans_entry, case):
    """Turn a raw answer (class or number) into phe_mg for this case."""
    kind, val = ans_entry
    if kind == "mg":
        return val
    protein = case["label"].get("protein_g_per_serving")
    if protein is None:
        raise ValueError("class answer but no protein on label")
    return round(float(protein) * COEFFICIENT[val], 1)


def score_run(ans, cases, abs_tol, rel_tol):
    def estimate(case):
        cid = case["id"]
        if cid not in ans:
            raise ValueError(f"no answer for {cid}")   # -> failure, never dropped
        return resolve(ans[cid], case)
    return rb.score(estimate, cases, abs_tol, rel_tol)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--answers", nargs="+", required=True)
    ap.add_argument("--testset", default="low_protein_usda.jsonl")
    ap.add_argument("--model", required=True)
    ap.add_argument("--runner", default=os.environ.get("PKU_BENCH_RUNNER"))
    ap.add_argument("--abs-tol-mg", type=float, default=rb.ABS_TOL_MG_DEFAULT)
    ap.add_argument("--rel-tol", type=float, default=rb.REL_TOL_DEFAULT)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    cases = rb.load_testset(a.testset)
    ids = [c["id"] for c in cases]
    case_by_id = {c["id"]: c for c in cases}
    runs = [load_answers(p) for p in a.answers]

    per_run = [score_run(r, cases, a.abs_tol_mg, a.rel_tol)[0] for r in runs]
    maes = [m["mae_mg"] for m in per_run if m["mae_mg"] is not None]
    wbs = [m["within_band_pct"] for m in per_run]

    # reproducibility: per food, resolve each run's answer to a number, all-equal?
    identical = answered_all = 0
    for cid in ids:
        nums = []
        for r in runs:
            if cid in r:
                try:
                    nums.append(resolve(r[cid], case_by_id[cid]))
                except Exception:
                    nums.append(None)
            else:
                nums.append(None)
        got = [n for n in nums if n is not None]
        if len(got) == len(runs) and len(runs) >= 2:
            answered_all += 1
            if len(set(got)) == 1:
                identical += 1

    result = {
        "test": "single-ingredient (classify -> coefficient -> multiply)",
        "model": a.model, "runner": a.runner,
        "n_cases": len(ids), "n_runs": len(runs),
        "accuracy": {
            "mae_mg": per_run[0]["mae_mg"],
            "within_band_pct": per_run[0]["within_band_pct"],
            "bias_mg": per_run[0]["bias_mg"], "rmse_mg": per_run[0]["rmse_mg"],
            "n_answered": per_run[0]["n_scored"],
            "n_unanswered": per_run[0]["n"] - per_run[0]["n_scored"],
            "tolerance_band": per_run[0]["tolerance_band"],
        },
        "reproducibility": None if len(runs) < 2 else {
            "identical_pct": round(100.0 * identical / answered_all, 1) if answered_all else None,
            "identical": identical, "answered_all_runs": answered_all,
            "mae_range": round(max(maes) - min(maes), 2) if maes else None,
        },
        "run_utc": datetime.datetime.utcnow().isoformat() + "Z",
    }

    ac = result["accuracy"]
    print(f"model: {a.model}   runs: {len(runs)}")
    print("ACCURACY (vs USDA truth):")
    print(f"  answered      {ac['n_answered']}/{result['n_cases']} (blank = failure)")
    print(f"  MAE           {ac['mae_mg']} mg")
    print(f"  within-band   {ac['within_band_pct']} %")
    print(f"  bias {ac['bias_mg']} mg   RMSE {ac['rmse_mg']} mg")
    if result["reproducibility"]:
        rp = result["reproducibility"]
        print("REPRODUCIBILITY (same food, same answer across runs):")
        print(f"  identical     {rp['identical']}/{rp['answered_all_runs']} = {rp['identical_pct']} %")
    if a.out:
        d = os.path.dirname(a.out)
        if d:
            os.makedirs(d, exist_ok=True)
        json.dump(result, open(a.out, "w"), indent=2)
        print(f"wrote {a.out}")


if __name__ == "__main__":
    main()
