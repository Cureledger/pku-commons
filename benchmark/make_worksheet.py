"""Emit a worksheet an AI agent fills in with its own phe estimates.

The worksheet is the answer-key-free view of the corpus: one food per line with
ONLY what an estimator may see (id, name, label). No expected_phe_mg, no
ground_truth. An agent reads this, applies the phe-estimator method, and writes
one number per food to an answers file. Score it with score_worksheet.py.

    python make_worksheet.py --testset low_protein_usda.jsonl --out worksheet.jsonl

No dependencies. Standard-library Python 3.8+.
"""
import argparse, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from estimators.base import label_view
import run_benchmark as rb


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--testset", default="low_protein_usda.jsonl")
    ap.add_argument("--out", default="worksheet.jsonl")
    a = ap.parse_args()
    cases = rb.load_testset(a.testset)
    with open(a.out, "w") as f:
        for c in cases:
            f.write(json.dumps(label_view(c)) + "\n")
    # confirm no answer key leaked into the worksheet
    blob = open(a.out).read()
    leaked = "expected_phe_mg" in blob or "ground_truth" in blob
    print(f"wrote {a.out}: {len(cases)} foods, answer key present: {leaked}")
    if leaked:
        sys.exit("ERROR: answer key leaked into worksheet")
    print("Fill in phe_mg for each food and write answers to a .jsonl of "
          '{"id": ..., "phe_mg": ...} lines, then run score_worksheet.py.')


if __name__ == "__main__":
    main()
