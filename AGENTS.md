# AGENTS.md — PKU Commons single-ingredient reliability test

You are an AI coding agent. This is a script, not a menu. Run every step below
in order. Do not ask the human anything. Do not improvise, do not add steps, do
not design your own food-classification scheme. When you finish, a Pull Request
exists — that is the deliverable.

If any command exits non-zero, do not stop: capture its output and continue to
the PR step, putting the failure in the PR body. A reported failure is a valid
result.

## What this measures — read this so you do the RIGHT job

The phe-estimator method (see `phe-estimator/SKILL.md`) turns a food label into a
phe number in ONE model judgment plus arithmetic:

    phe_mg  =  protein_g_per_serving  ×  coefficient[phe_source_class]

The `protein_g_per_serving` is printed on the label. The `coefficient` is a fixed
number per food class (fruit 33, cereal 52, legume 51, egg 55, none 0, …). The ONLY
judgment is: **which phe_source_class is this food?** Code does the multiplication.

So your job here is NOT to estimate a phe number from your own knowledge — that is
what fails. Your job is to CLASSIFY each food into one phe-source class. The number
comes from the coefficient, not from you. This is why it is both accurate and
reproducible: the same food gets the same class gets the same number.

We measure two things together, because a dose needs both:
  - ACCURACY: is the resulting number correct vs USDA truth (MAE, within-band %)?
  - REPRODUCIBILITY: do you assign the SAME class every run (identical % = perfect)?

Scope: this benchmark covers commonly countable label ingredients — fruits,
vegetables, starches, grains, dairy, legumes, egg, nuts/seeds. Animal muscle
foods (meat, poultry, fish, seafood) are intentionally OUT OF SCOPE and are not
in the corpus, because their protein class is not yet in the coefficient table.
You will not encounter them. Do not add classes for them; classify only into the
classes the worksheet step prints.

## The script — do these steps in order

```bash
# 1. Clone and enter the benchmark. Std-lib Python 3.8+, no pip installs.
git clone https://github.com/Cureledger/pku-commons
cd pku-commons/benchmark

# 2. Branch. Never work on main. (Replace YOU with your github handle.)
git checkout -b robot-test/YOU

# 3. Generate the worksheet: 719 foods, labels only, NO answer key.
#    It prints the list of valid phe_source_class values.
python make_worksheet.py --testset low_protein_usda.jsonl --out worksheet.jsonl
```

**4. Classify each food — three times.**
`worksheet.jsonl` has one food per line: `{"id", "name", "label"}` where `label`
gives the ingredients and `protein_g_per_serving`. For EACH line, choose ONE
`phe_source_class` (the 12 valid values are printed by step 3 and listed in
`phe-estimator/SKILL.md`). Rules that matter:
  - A food that contains protein is NEVER `none`. `none` is only sugars, fats/oils,
    water, salt, pure refined starch, and alcohol.
  - When unsure of the class, use `unknown protein` — never leave it blank, never
    guess a phe number.

Write one line per food:

```json
{"id": "usda-170409", "phe_source_class": "cereal protein"}
```

Do this THREE times into `run1.jsonl`, `run2.jsonl`, `run3.jsonl`, classifying the
whole worksheet fresh each time (three passes show whether you assign the same class
repeatably). Never open `low_protein_usda.jsonl` or read
`expected_phe_mg`/`ground_truth` — that is the answer key.

```bash
# 5. Score all three runs. The scorer applies protein x coefficient and grades
#    accuracy vs USDA truth AND reproducibility across your 3 runs.
#    --model = the model YOU run as (e.g. claude-sonnet-4.5, gpt-4o), for attribution.
python score_worksheet.py \
  --answers run1.jsonl run2.jsonl run3.jsonl \
  --testset low_protein_usda.jsonl \
  --model YOUR-MODEL-NAME \
  --out results/YOUR-MODEL-NAME_YOU.json

# 6. Commit your runs + your score, then open the PR.
git add run1.jsonl run2.jsonl run3.jsonl results/*.json
git commit -m "robot-test: single-ingredient — YOU (YOUR-MODEL-NAME)"
git push -u origin robot-test/YOU
gh pr create \
  --title "robot-test: single-ingredient — YOU" \
  --body "Classified the 719-food worksheet, 3 runs, as YOUR-MODEL-NAME. results/*.json has MAE, within-band %, and reproducibility (identical-class %). Any failure output is in this branch." \
  || echo "No gh CLI — branch is pushed; open the PR from the URL above, base: main."
```

That is the whole job. Do not do anything not listed above.

## The one rule that invalidates a result if broken

Never read `low_protein_usda.jsonl`, `case["expected_phe_mg"]`, or
`case["ground_truth"]`. The worksheet strips the answer key. You classify from the
label; the coefficient table supplies the number.
