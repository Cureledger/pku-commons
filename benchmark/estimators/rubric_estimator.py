"""Deterministic reference implementation of the phe-estimator rubric.

This is the 7-step rubric from phe-estimator/SKILL.md encoded in plain Python — no LLM, no
network — so it can be scored in CI as the reproducible baseline the Claude Skill must match
or beat. It uses the cited phe-per-g-protein table (phe-estimator/phe_per_g_protein.json).

It intentionally makes the recipe-factor judgment by a documented, deterministic heuristic
(ingredient order → weight shares), so its numbers are explainable and regression-gated.

    python run_benchmark.py --estimator estimators.rubric_estimator
"""

# Plain-Python, no model/network: identical output every run.
DETERMINISTIC = True

import json, os, re, sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_TABLE_PATH = os.path.normpath(os.path.join(_HERE, "..", "..", "phe-estimator", "phe_per_g_protein.json"))

with open(_TABLE_PATH) as fh:
    _T = json.load(fh)
PHE_PER_G = {k: v["phe_mg_per_g_protein"] for k, v in _T["classes"].items()}

# Whole-food phe-per-100g reference (the "food list" / knowledge-graph path). Used when a
# recipe has an ingredients list but NO declared protein panel (e.g. a fruit salad).
# Single source of truth: the shared food-list loader (food-list/foodlist.py), which reads
# the cited, versioned food-list/foods.json. Same stem-match logic as before, so this refactor
# is numerically identical to the previous ad-hoc read of testset/food_reference.json.
_FOODLIST_DIR = os.path.normpath(os.path.join(_HERE, "..", "..", "food-list"))
if _FOODLIST_DIR not in sys.path:
    sys.path.insert(0, _FOODLIST_DIR)
import foodlist as _foodlist

_FOOD_LIST = _foodlist.load()


def lookup_food_phe_100g(name: str):
    """phe mg per 100 g of a whole food, by name stem; None if not in the food list."""
    return _FOOD_LIST.phe_100g(name)

# Ingredient-name -> protein source class. Order matters (first match wins).
# Patterns use a leading \b but NO trailing boundary, so stems match their plurals
# ("apple" matches "apples", "carrot" matches "carrots").
_CLASS_RULES = [
    ("none",              r"\b(sugars?|sucrose|dextrose|glucose|fructose|corn syrup|water|salt|"
                          r"oils?|fats?|butter|shortening|citric acid|vinegar|baking soda|"
                          r"baking powder|colors?|flavors?|lecithin)"),
    ("refined starch",    r"\b(cornstarch|corn starch|tapioca|potato starch|modified starch|maltodextrin)"),
    # tuber/root BEFORE cereal so "potato flour" matches its own class, not the bare "flour"
    # alternative in the cereal pattern.
    ("tuber/root starch", r"\b(potato flour|potato|sweet potato|cassava)"),
    ("cereal protein",    r"\b(wheat|flour|rice|corn|maize|oat|barley|rye|semolina|bread|pasta|cereal|bran|"
                          r"cracker|noodle)"),
    ("dairy protein",     r"\b(milk|whey|casein|cheese|yogurt|cream|dairy)"),
    ("legume protein",    r"\b(soy|pea protein|peas?|lentil|beans?|chickpea|peanut)"),
    ("egg protein",       r"\b(eggs?|albumen)"),
    ("nut/seed protein",  r"\b(almond|cashew|walnut|hazelnut|seeds?|sesame|sunflower)"),
    ("gelatin/collagen",  r"\b(gelatin|collagen)"),
    ("fruit protein",     r"\b(apple|banana|strawberr|orange|grape|berry|berries|peach|pear|mango|pineapple|"
                          r"fruit|tomato)"),
    ("vegetable protein", r"\b(carrot|broccoli|cucumber|spinach|lettuce|pepper|celery|onion|zucchini|"
                          r"cauliflower|mushroom|vegetable|squash)"),
]


def classify(name: str) -> str:
    n = name.lower()
    for cls, pat in _CLASS_RULES:
        if re.search(pat, n):
            return cls
    return "unknown protein"


def split_ingredients(text: str):
    if not text:
        return []
    # split on commas / semicolons / "and"; strip parenthetical sub-lists and %.
    text = re.sub(r"\([^)]*\)", "", text)
    parts = re.split(r"[,;]|\band\b", text)
    return [p.strip(" .%0123456789").strip() for p in parts if p.strip(" .%").strip()]


def _order_shares(n: int):
    """Weight shares from ingredient ORDER (descending weight), normalized to 1.
    Ingredients are listed by descending weight, so give earlier items more mass."""
    if n <= 0:
        return []
    raw = [1.0 / (i + 1) for i in range(n)]
    s = sum(raw)
    return [w / s for w in raw]


def estimate(case: dict) -> dict:
    label = case["label"]
    serving_g = float(label.get("serving_size_g") or 0)
    protein_declared = label.get("protein_g_per_serving")
    ing_text = label.get("ingredients") or ""
    names = split_ingredients(ing_text) or ["unknown"]

    # -------- Path B: no protein panel (whole-food recipe) → food-list lookup --------
    # A fruit salad has no nutrition label. Estimate phe from each whole food's phe-per-100g
    # (the food list), apportioning the serving grams across ingredients by weight share.
    if protein_declared is None:
        shares = _order_shares(len(names))
        considered, recipe_factor = [], 0.0
        for nm, share in zip(names, shares):
            phe100 = lookup_food_phe_100g(nm)
            grams = serving_g * share
            contrib = (phe100 or 0.0) * grams / 100.0
            recipe_factor += contrib
            considered.append({"name": nm,
                               "phe_source_class": "whole food (food-list)" if phe100 else "unknown",
                               "est_share": round(share, 3)})
        return {
            "phe_mg": round(recipe_factor, 1),
            "meta": {"recipe_factor_mg_per_serving": round(recipe_factor, 1),
                     "serving_size_g": serving_g, "portion_g": serving_g,
                     "countable": None, "protein_g_per_serving": None,
                     "path": "food-list lookup (no protein panel)",
                     "ingredients_considered": considered},
        }

    # -------- Path A: protein declared on the panel → rubric via protein × class --------
    protein_g = float(protein_declared)

    # Step 1: countable?
    countable = protein_g <= 2.0

    # Step 2-3: identify + classify phe-bearing ingredients
    classes = [(nm, classify(nm)) for nm in names]
    phe_bearing = [(nm, cls) for nm, cls in classes if PHE_PER_G.get(cls, 0) > 0]

    # Step 4: recipe factor. Weight shares from ingredient ORDER (descending weight).
    # Geometric-ish decay by position, restricted to phe-bearing items, normalized to 1.
    considered = []
    shares = _order_shares(len(phe_bearing))

    recipe_factor = 0.0
    bi = 0
    for nm, cls in classes:
        ppg = PHE_PER_G.get(cls, 0.0)
        if ppg > 0 and phe_bearing:
            share = shares[bi]; bi += 1
            contrib = protein_g * share * ppg
            recipe_factor += contrib
            considered.append({"name": nm, "phe_source_class": cls, "est_share": round(share, 3)})
        else:
            considered.append({"name": nm, "phe_source_class": cls, "est_share": 0.0})

    # If nothing classified as phe-bearing but protein > 0, fall back to unknown class
    if recipe_factor == 0.0 and protein_g > 0:
        recipe_factor = protein_g * PHE_PER_G["unknown protein"]

    # Steps 5-6: scale to portion. Benchmark scores the labeled serving, so portion = serving.
    portion_g = serving_g
    phe_mg = recipe_factor * (portion_g / serving_g) if serving_g else recipe_factor

    return {
        "phe_mg": round(phe_mg, 1),
        "meta": {
            "recipe_factor_mg_per_serving": round(recipe_factor, 1),
            "serving_size_g": serving_g,
            "portion_g": portion_g,
            "countable": countable,
            "protein_g_per_serving": protein_g,
            "ingredients_considered": considered,
        },
    }
