"""Model-classifies, code-computes: the phe-estimator SKILL method, split cleanly.

This is the estimator that makes the test MEANINGFUL. The SKILL asks a model to do
exactly one judgment — classify each food into a phe-source class — and then applies a
fixed coefficient (phe per g protein) by arithmetic. This estimator isolates that:

    model  -> phe_source_class  (one of 12 fixed classes; the ONLY model output)
    code   -> phe_mg = protein_g_per_serving * COEFFICIENT[class]   (pure arithmetic)

Because the model's output space is 12 labels (not a free number), the result is
bounded and reproducible: same food -> same class -> same number. The number is never
invented by the model. This is why it does not collapse to the "answer 0 for half the
foods" failure of free-form estimation.

Wire a model caller (provider-agnostic), same as claude_skill.py:
    from estimators import classify_estimator
    classify_estimator.set_model_caller(lambda system, user: my_model(system, user))
Then: python run_benchmark.py --estimator estimators.classify_estimator --model <name>

If no caller is set, estimate() raises — it never fabricates.
"""
import json, os, re

DETERMINISTIC = False  # model-backed: run_benchmark requires --model

_HERE = os.path.dirname(os.path.abspath(__file__))
_TABLE = os.path.normpath(os.path.join(_HERE, "..", "..", "phe-estimator", "phe_per_g_protein.json"))
with open(_TABLE) as fh:
    _T = json.load(fh)
COEFFICIENT = {k: v["phe_mg_per_g_protein"] for k, v in _T["classes"].items()}
CLASSES = list(COEFFICIENT.keys())

_MODEL_CALLER = None


def set_model_caller(fn):
    """Register fn(system_prompt, user_prompt) -> str (model text)."""
    global _MODEL_CALLER
    _MODEL_CALLER = fn


_SYSTEM = (
    "You classify a single food into ONE phenylalanine-source class. This is a "
    "classification task, not a numeric estimate. Choose exactly one class from this list, "
    "by the food's dominant protein source:\n"
    + "\n".join(f"  - {c}  ({COEFFICIENT[c]} mg phe per g protein)" for c in CLASSES)
    + "\n\nRules: a food that contains protein is NEVER 'none'. 'none' is only for sugars, "
    "fats/oils, water, salt, and pure refined starch. Alcohol is 'none'. When unsure, use "
    "'unknown protein' (never guess a number). Return ONLY JSON: {\"phe_source_class\": \"<one class>\"}."
)


def _label_user(case):
    l = case["label"]
    return (f"Food name: {case.get('name')}\n"
            f"ingredients: {l.get('ingredients')}\n"
            f"protein_g_per_serving: {l.get('protein_g_per_serving')}\n"
            "Classify this food into one phe_source_class.")


def _parse_class(text):
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if m:
        try:
            c = json.loads(m.group(0)).get("phe_source_class")
            if c in COEFFICIENT:
                return c
        except Exception:
            pass
    # fallback: any class name mentioned verbatim
    for c in CLASSES:
        if c in text:
            return c
    return None


def estimate(case):
    if _MODEL_CALLER is None:
        raise RuntimeError(
            "classify_estimator: no model caller set. Call "
            "classify_estimator.set_model_caller(fn) with fn(system, user)->str first."
        )
    protein = case["label"].get("protein_g_per_serving")
    if protein is None:
        raise ValueError("no protein on label (this estimator is for the protein-panel path)")
    reply = _MODEL_CALLER(_SYSTEM, _label_user(case))
    cls = _parse_class(reply)
    if cls is None:
        raise ValueError(f"model did not return a valid class: {reply[:80]!r}")
    phe = float(protein) * COEFFICIENT[cls]
    return {"phe_mg": round(phe, 1), "phe_source_class": cls,
            "protein_g_per_serving": protein, "coefficient": COEFFICIENT[cls]}
