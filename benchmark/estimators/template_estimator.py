"""COPY-ME starter estimator. Duplicate this file, rename it, and fill in `estimate`.

    cp estimators/template_estimator.py estimators/my_estimator.py
    # edit my_estimator.py
    python run_benchmark.py --estimator estimators.my_estimator --baseline results/baseline_v0.json

Your job: implement `estimate(case) -> float | dict`. You receive the *label* (serving size,
protein per serving, ingredient text) and return the estimated phe in **milligrams** for the
serving. You must NOT read `case["expected_phe_mg"]` or `case["ground_truth"]` — those are the
answer key, and `label_view()` below hands you only what you're allowed to see.

Pick a reliability gap to attack (see docs/RELIABILITY.md):
  - Gap 1/2: use the shared food list to look phe up instead of inferring it from the label.
  - Gap 3: write a better recipe-factor / weight-share model (the biggest error source).
  - Gap 4: if you wrap an LLM, make its output reproducible run-to-run.
"""
import os, sys
from .base import label_view

# The shared, cited food list is available to every estimator. Use it for phe-per-100g lookups.
_FOODLIST_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "food-list"))
if _FOODLIST_DIR not in sys.path:
    sys.path.insert(0, _FOODLIST_DIR)
import foodlist  # foodlist.load(), .lookup_phe_100g(name), FoodList.phe_100g(name)

_FOOD_LIST = foodlist.load()


def estimate(case: dict):
    view = label_view(case)          # {"id", "name", "label"} — the ONLY thing you may read
    label = view["label"]
    serving_g = float(label.get("serving_size_g") or 0)
    protein_g = label.get("protein_g_per_serving")   # may be None (whole-food, no panel)
    ingredients = label.get("ingredients") or ""

    # -------------------------------------------------------------------------------------
    # TODO: replace this trivial body with your method.
    # Example of using the shared food list for a single named food:
    #     phe_per_100g = _FOOD_LIST.phe_100g(ingredients)
    #     if phe_per_100g is not None:
    #         return {"phe_mg": round(phe_per_100g * serving_g / 100.0, 1),
    #                 "meta": {"path": "food-list lookup"}}
    # -------------------------------------------------------------------------------------
    phe_mg = 0.0

    return {"phe_mg": round(phe_mg, 1), "meta": {"note": "template — replace estimate() body"}}
