# AGENTS.md — PKU Commons test protocol for AI agents

You are an AI coding agent (Claude Code or similar) working on behalf of a
volunteer. Your job is to test the phe-estimator and report results back to
this project. Follow this file exactly. Do not improvise steps.

## Mission

The phe-estimator turns a food label into one phenylalanine number. The one
step that is not yet reliable is guessing the WEIGHT SHARE of each ingredient
in a mixed food. You are here to measure that unreliability and add evidence
that helps close it. Everything you produce is a data point, including a
failure. A failure you report is worth as much as a pass.

## Setup (run once)

    git clone https://github.com/Cureledger/pku-commons
    cd pku-commons/benchmark
    python run_benchmark.py --estimator estimators.rubric_estimator \
        --testset low_protein_usda.jsonl
    # Expect a table of ~729 single-ingredient foods and a summary line, with
    # no error. Standard-library Python 3.8+. No dependencies to install.
    #
    # low_protein_usda.jsonl is the 729-food single-ingredient corpus: one whole
    # food per case, phe ground truth from USDA FoodData Central (nutrient 508),
    # each with its fdcId. It isolates ONE thing — how precisely the estimator
    # reads a single-ingredient label — before mixed dishes are added later.

If that table does not print, stop and report the error (see "Report back").

## Rule you must never break

Never read `case["expected_phe_mg"]` or `case["ground_truth"]`. Those are the
answer key. `estimators/base.py:label_view()` hands you only what you may see:
serving size, protein per serving, ingredient text. An estimator that reads
the answer key is invalid and will be rejected.

## Pick ONE task. Do it fully. Report. Then optionally pick another.

### TASK A — Reproducibility test (needs many model calls; good use of spare cycles)

Measure whether the same single-ingredient food gives the same number twice,
across the 729-food corpus.

    python variance.py --estimator estimators.rubric_estimator --runs 5 \
        --testset low_protein_usda.jsonl \
        --out results/variance_rubric_<yourhandle>.json

Then do the same for any LLM-backed estimator you have wired (see
`estimators/claude_skill.py` for how one is wired), with the same `--testset`
and `--runs 5`. This is the precision test: how tightly the AI reproduces a
one-ingredient lookup run to run.

Report: the min / mean / max / range of MAE for each estimator you ran. A
range of 0 is perfect reproducibility. Any range above 0 on an LLM estimator
is the defect we are tracking. Name the model you used.

### TASK B — Contribute a real meal (grows the test set; highest value)

Take a real food label from your volunteer's kitchen, or a real mixed dish.

1. Write the label as one JSON line matching `benchmark/schema.json`:
   serving size, protein per serving (or null if none), ingredient text.
2. Compute the true phe by hand: for each ingredient, look up its phe in USDA
   FoodData Central (https://fdc.nal.usda.gov), record the FDC id and the grams
   you used, and sum. Put this in `ground_truth.components` with every FDC id
   and gram amount, so anyone can re-derive your number.
3. Append the line to `benchmark/low_protein_usda.jsonl`, then confirm it is
   arithmetically honest — this must exit 0:
       python validate_cases.py low_protein_usda.jsonl
4. Run `python run_benchmark.py --estimator estimators.rubric_estimator \
       --testset low_protein_usda.jsonl` and note whether the current method
   passed or failed your new case.

Report: your new case, and whether the method got it right. A mixed dish the
method fails is exactly what we want.

### TASK C — Beat the weight-share step (for agents that want to build)

    cp estimators/template_estimator.py estimators/<yourhandle>_estimator.py
    # implement estimate(case): a better way to split ingredient weights
    python run_benchmark.py --estimator estimators.<yourhandle>_estimator \
        --baseline results/baseline_v0.json \
        --out results/<yourhandle>.json --report report.md

The run exits non-zero if you regress (MAE up, or within-band % down). A
green run that lowers MAE beats the current method.

Report: your MAE and within-band %, and one sentence on your method.

## Report back (required — this is the point)

Open a Pull Request against `Cureledger/pku-commons` containing only the file
you produced (your `results/*.json`, or your new line in
`low_protein_usda.jsonl`, or your estimator file). Title it `robot-test: <task letter> — <yourhandle>`.
Paste this block into the PR description, filled in:

    Task: A / B / C
    Model used (if any):
    Numbers: (MAE, within-band %, variance range, or new-case pass/fail)
    One thing that broke or surprised me:
    Time spent:

If you cannot open a PR, open a GitHub Issue with the label `robot-test` and
paste the same block. Do not push directly to the main branch.

## Do not

- Do not edit files other than the one your task produces.
- Do not change the answer key, the tolerance band, or another person's results.
- Do not report a number you did not produce by running the command.
