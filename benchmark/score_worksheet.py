"""Score an agent-filled worksheet against USDA ground truth.

Reuses run_benchmark.score() so accuracy is defined identically to the harness:
MAE, within-band %, bias, RMSE against expected_phe_mg (USDA nutrient 508), with
the same tolerance band. A food the agent left blank or could not answer counts
as a failure (not dropped) — the denominator is always the full testset.

    python score_worksheet.py --answers answers.jsonl \
        --testset low_protein_usda.jsonl --model <name-you-ran> \
        --out results/accuracy_<model>_<handle>.json

--model is required: the result records WHICH model produced these answers, so a
PR is attributable. No dependencies. Standard-library Python 3.8+.
"""
import argparse, json, os, sys, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import run_benchmark as rb


def load_answers(path):
    ans = {}
    with open(path) as f:
        for ln in f:
            ln = ln.strip()
            if not ln:
                continue
            o = json.loads(ln)
            if "id" in o and o.get("phe_mg") is not None:
                ans[o["id"]] = float(o["phe_mg"])
    return ans


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--answers", required=True)
    ap.add_argument("--testset", default="low_protein_usda.jsonl")
    ap.add_argument("--model", required=True, help="model that produced the answers (attribution)")
    ap.add_argument("--runner", default=os.environ.get("PKU_BENCH_RUNNER"))
    ap.add_argument("--abs-tol-mg", type=float, default=rb.ABS_TOL_MG_DEFAULT)
    ap.add_argument("--rel-tol", type=float, default=rb.REL_TOL_DEFAULT)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    cases = rb.load_testset(a.testset)
    ans = load_answers(a.answers)

    # an agent estimator that just returns its filled-in number; a blank answer
    # raises -> scored as a failed case (never silently dropped)
    def estimate(case):
        cid = case["id"]
        if cid not in ans:
            raise ValueError(f"no answer provided for {cid}")
        return ans[cid]

    metrics, per_case = rb.score(estimate, cases, a.abs_tol_mg, a.rel_tol)
    answered = metrics["n_scored"]
    result = {
        "test": "accuracy",
        "model": a.model,
        "runner": a.runner,
        "n_cases": metrics["n"],
        "n_answered": answered,
        "n_unanswered": metrics["n"] - answered,
        "mae_mg": metrics["mae_mg"],
        "medae_mg": metrics["medae_mg"],
        "rmse_mg": metrics["rmse_mg"],
        "bias_mg": metrics["bias_mg"],
        "within_band_pct": metrics["within_band_pct"],
        "tolerance_band": metrics["tolerance_band"],
        "run_utc": datetime.datetime.utcnow().isoformat() + "Z",
    }
    print(f"model: {a.model}")
    print(f"answered {answered}/{metrics['n']} foods "
          f"(unanswered counted as failures)")
    print(f"  MAE           {metrics['mae_mg']} mg")
    print(f"  within-band   {metrics['within_band_pct']} %")
    print(f"  bias          {metrics['bias_mg']} mg   RMSE {metrics['rmse_mg']} mg")
    if a.out:
        os.makedirs(os.path.dirname(a.out), exist_ok=True) if os.path.dirname(a.out) else None
        json.dump(result, open(a.out, "w"), indent=2)
        print(f"wrote {a.out}")


if __name__ == "__main__":
    main()
