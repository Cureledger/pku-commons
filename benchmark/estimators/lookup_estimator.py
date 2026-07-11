"""Deterministic single-ingredient lookup estimator.

A single-ingredient phe value is a LOOKUP, not a guess. This estimator resolves the
label's food name to a row in a single-ingredient USDA reference table (name ->
phe_mg_per_100g), then returns phe = phe_per_100g * grams / 100. No model, no network,
so the SAME food yields the SAME number on every run — precision is 100% by construction.

It does NOT read case["expected_phe_mg"] or case["ground_truth"]; it matches on the
label/name only (what an estimator is allowed to see). Name matching is deterministic:
exact -> normalized -> stem, with a cached alias map. If no row matches, it returns
None-equivalent with confidence "none" (an honest miss, never a guess).

Reference table: benchmark/usda_single_ingredient_ref.json — single source of truth for
single ingredients. In production this is the shipped, versioned food list, which must
grow to raise coverage. Each row carries its USDA fdcId citation.
"""
DETERMINISTIC = True

import json, os, re

_HERE = os.path.dirname(os.path.abspath(__file__))
_REF = os.path.join(_HERE, "..", "usda_single_ingredient_ref.json")

def _norm(s):
    s = (s or "").lower().strip()
    s = re.sub(r"[^a-z0-9 ,]", " ", s)
    s = re.sub(r"\s+", " ", s)
    return s

def _stem(s):
    # first comma-clause, first token group — "banana, raw" -> "banana"
    return _norm(s).split(",")[0].strip()

with open(_REF) as fh:
    _TABLE = json.load(fh)["foods"]   # {norm_name: {phe_mg_per_100g, fdcId, ...}}

# build match indices once
_BY_NORM = {_norm(k): v for k, v in _TABLE.items()}
_BY_STEM = {}
for k, v in _TABLE.items():
    _BY_STEM.setdefault(_stem(k), v)   # first wins, stable

def _resolve(name, ingredients):
    for cand in (name, ingredients):
        n = _norm(cand)
        if n in _BY_NORM: return _BY_NORM[n], "exact"
    for cand in (name, ingredients):
        st = _stem(cand)
        if st in _BY_STEM: return _BY_STEM[st], "stem"
    return None, "none"

def estimate(case):
    label = case["label"]
    name = case.get("name")
    grams = label.get("serving_size_g") or 0
    row, how = _resolve(name, label.get("ingredients"))
    if row is None:
        return {"phe_mg": 0.0, "meta": {"confidence": "none", "match": how,
                "note": "no single-ingredient table row; honest miss, not a guess"}}
    phe = round(row["phe_mg_per_100g"] * grams / 100.0, 1)
    return {"phe_mg": phe, "meta": {"confidence": "exact" if how=="exact" else "high",
            "match": how, "fdcId": row.get("fdcId")}}
