"""PKU Commons — phe-estimator interface.

Any estimator (the Claude Skill, an app backend, a heuristic, a model) is scored by
implementing ONE function:

    def estimate(case: dict) -> float | dict

`case` is a test case (see benchmark/schema.json). The estimator receives the *label*
(serving size, ingredient text, protein/serving) and must NOT read `case["expected_phe_mg"]`
or `case["ground_truth"]` — those are the answer key.

Return either:
  * a float — the estimated phe in **mg** for the serving, or
  * a dict {"phe_mg": float, "meta": {...}} to attach diagnostic info.

Register your estimator by exposing a module-level `estimate` callable, then run:

    python run_benchmark.py --estimator estimators.my_estimator
"""
from typing import Union

Label = dict
Result = Union[float, dict]


def label_view(case: dict) -> dict:
    """Return ONLY what an estimator is allowed to see (guards against peeking)."""
    return {
        "id": case["id"],
        "name": case.get("name"),
        "label": case["label"],
    }
