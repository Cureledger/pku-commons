"""Reference STUB estimator — a transparent, deterministic baseline.

This is NOT the Claude Skill. It exists so the harness has something to score out of the
box and so contributors have a worked example of the interface. It implements a crude
version of the "think like a PKU parent" method:

  1. Look up phe-bearing ingredients in a small built-in table (mg phe per 100 g food).
  2. Split the serving weight evenly across the named phe-bearing ingredients
     (a naive stand-in for the human "recipe factor").
  3. Sum the contributions.

Its errors are the point: they show what the benchmark rewards improving.
"""
import re
from .base import label_view

# Tiny built-in knowledge table (mg phe per 100 g). A real estimator would use the
# living food list. Keys are lowercase substrings matched against the ingredient text.
PHE_MG_PER_100G = {
    "cornstarch": 13, "corn starch": 13,
    "tapioca": 4,
    "potato flour": 316,
    "rice": 353,
    "apple": 7,
    "banana": 49,
    "carrot": 61,
    "cucumber": 31,
    "broccoli": 117,
    "strawberr": 19,
    "tomato": 27,
}
# Ingredients that carry no phe (so a naive equal-split doesn't wrongly divide weight into them)
ZERO_PHE = ["water", "sugar", "salt", "oil", "fat"]


def _match(ingredient_token: str):
    t = ingredient_token.lower().strip()
    for key, val in PHE_MG_PER_100G.items():
        if key in t:
            return val
    return None


def estimate(case: dict):
    view = label_view(case)
    label = view["label"]
    serving = float(label.get("serving_size_g") or 0)
    text = (label.get("ingredients") or "")
    tokens = [t for t in re.split(r"[,;]| and ", text) if t.strip()]

    phe_tokens = []
    for tok in tokens:
        if any(z in tok.lower() for z in ZERO_PHE):
            continue
        v = _match(tok)
        if v is not None:
            phe_tokens.append((tok.strip(), v))

    if not phe_tokens or serving <= 0:
        return {"phe_mg": 0.0, "meta": {"matched": [], "reason": "no phe-bearing ingredient matched"}}

    # Naive recipe factor: split serving weight evenly across phe-bearing ingredients.
    grams_each = serving / len(phe_tokens)
    total = sum(v * grams_each / 100.0 for _, v in phe_tokens)
    return {"phe_mg": round(total, 1),
            "meta": {"matched": phe_tokens, "grams_each": round(grams_each, 1)}}
