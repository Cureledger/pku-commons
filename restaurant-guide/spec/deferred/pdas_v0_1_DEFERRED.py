"""PDAS v0.1 reference implementation — Phebe Dining Access Scale.

Standard library only, Python 3.8+, matching PKU Commons convention.
Spec of record: spec/pdas-v0.1.md. If code and spec disagree, the spec wins
and this file is the bug.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional

SPEC_VERSION = "pdas-v0.1"

# ---------------------------------------------------------------- profiles
# Meal budgets in mg phe. A vector, never a scalar. See spec section 3.
PROFILES: Dict[str, Dict] = {
    "TIGHT": {"daily_mg": (200, 300),   "meal_mg": 60},
    "MID":   {"daily_mg": (400, 600),   "meal_mg": 120},
    "WIDE":  {"daily_mg": (1000, 2000), "meal_mg": 350},
}
DEFAULT_PROFILE = "MID"

ALLOWED_MODS = {
    "omit_cheese", "omit_nuts_seeds", "omit_meat_fish",
    "sauce_on_side", "sub_anchor_starch", "halve_component",
}
MAX_MODS = 2

FORMATS = ("a_la_carte", "partial_fixed", "tasting_only")
TASTING_ONLY_M_CAP = 2

SOURCE_RANK = {
    "restaurant_confirmed": 3,
    "structured_platform": 2,
    "human_transcription": 2,
    "pdf_or_vision": 1,
    "social_post": 0,
}

A_VERIFICATION_TTL_DAYS = 180


# ---------------------------------------------------------------- dish
@dataclass
class Dish:
    """One menu item with a phe estimate INTERVAL. Never a point estimate."""
    dish_id: str
    name: str
    phe_mg_low: float
    phe_mg_median: float
    phe_mg_high: float
    is_anchor_candidate: bool = False   # can this be a plate base at all?
    anchor_uncertain: bool = False      # e.g. fries: dusting unknown from text
    mods_required: List[str] = field(default_factory=list)
    is_vegetable_entree: bool = False
    course: Optional[str] = None

    def __post_init__(self):
        if not (self.phe_mg_low <= self.phe_mg_median <= self.phe_mg_high):
            raise ValueError(
                f"{self.dish_id}: interval must be ordered low<=median<=high, "
                f"got {self.phe_mg_low}/{self.phe_mg_median}/{self.phe_mg_high}"
            )
        bad = set(self.mods_required) - ALLOWED_MODS
        if bad:
            raise ValueError(f"{self.dish_id}: mods not in closed list: {sorted(bad)}")

    def clears(self, meal_mg: float) -> bool:
        """Spec 4.1: median within budget AND upper bound within 1.5x budget.
        The second condition is what stops a wide, badly-constrained estimate
        from being counted as safe."""
        return self.phe_mg_median <= meal_mg and self.phe_mg_high <= 1.5 * meal_mg

    def is_anchor(self, meal_mg: float) -> bool:
        """Anchor = plate base, <=1 modification, median <=25% of meal budget."""
        return (
            self.is_anchor_candidate
            and len(self.mods_required) <= 1
            and self.phe_mg_median <= 0.25 * meal_mg
        )


# ---------------------------------------------------------------- axis M
def score_M(dishes: List[Dish], menu_format: str, profile: str = DEFAULT_PROFILE) -> Dict:
    if menu_format not in FORMATS:
        raise ValueError(f"menu_format must be one of {FORMATS}, got {menu_format!r}")
    if profile not in PROFILES:
        raise ValueError(f"unknown profile {profile!r}")
    meal_mg = PROFILES[profile]["meal_mg"]

    as_served = [d for d in dishes if not d.mods_required and d.clears(meal_mg)]
    with_mods = [d for d in dishes
                 if d.mods_required and len(d.mods_required) <= MAX_MODS and d.clears(meal_mg)]
    anchors = [d for d in dishes if d.is_anchor(meal_mg)]
    certain_anchors = [d for d in anchors if not d.anchor_uncertain]
    veg_entree = any(d.is_vegetable_entree and d.clears(meal_mg) for d in dishes)

    n_as, n_mod = len(as_served), len(with_mods)
    n_anchor = len(certain_anchors)
    has_anchor = n_anchor > 0

    if not has_anchor and n_as == 0 and n_mod == 0:
        M = 0
    elif not has_anchor:
        M = 1
    elif n_as >= 3 and n_mod >= 3:
        M = 4 if (menu_format == "a_la_carte" and n_anchor >= 2 and veg_entree) else 3
    elif n_as >= 1:
        M = 2
    else:
        M = 1

    capped = False
    if menu_format == "tasting_only" and M > TASTING_ONLY_M_CAP:
        M, capped = TASTING_ONLY_M_CAP, True

    return {
        "M": M, "profile": profile, "meal_budget_mg": meal_mg,
        "inputs": {
            "anchor": has_anchor,
            "n_distinct_anchors": n_anchor,
            "n_anchor_uncertain": len(anchors) - n_anchor,
            "n_safe_as_served": n_as,
            "n_safe_with_mods": n_mod,
            "plausible_vegetable_entree": veg_entree,
            "format": menu_format,
        },
        "tasting_cap_applied": capped,
        "driving_dishes": {
            "anchors": [d.dish_id for d in certain_anchors],
            "safe_as_served": [d.dish_id for d in as_served],
            "safe_with_mods": [d.dish_id for d in with_mods],
        },
        "spec_version": SPEC_VERSION,
    }


def score_M_all_profiles(dishes: List[Dish], menu_format: str) -> Dict[str, Dict]:
    """M is a vector over profiles. A page showing one M is out of spec."""
    return {p: score_M(dishes, menu_format, p) for p in PROFILES}


# ---------------------------------------------------------------- axis A
def score_A(verification: Optional[Dict], today: Optional[str] = None) -> Dict:
    """A is set ONLY from contact with the restaurant. None -> unverified.
    unverified is NOT zero: A=0 is a finding and needs a source."""
    if not verification:
        return {"A": None, "A_status": "unverified", "spec_version": SPEC_VERSION,
                "note": "A is never inferred from menu text, cuisine, or reviews."}
    for k in ("A", "verified_by", "verified_utc", "method", "evidence"):
        if k not in verification:
            raise ValueError(f"A verification missing required field {k!r}")
    if verification["A"] not in (0, 1, 2, 3, 4):
        raise ValueError("A must be 0-4")

    import datetime as _dt
    v = _dt.date.fromisoformat(verification["verified_utc"][:10])
    exp = v + _dt.timedelta(days=A_VERIFICATION_TTL_DAYS)
    now = _dt.date.fromisoformat(today) if today else _dt.date.today()
    if now > exp:
        return {"A": None, "A_status": "expired", "expired_utc": exp.isoformat(),
                "prior_A": verification["A"], "spec_version": SPEC_VERSION,
                "note": "Verification older than 180 days. Badge dark until re-confirmed."}
    out = dict(verification)
    out.update({"A_status": "verified", "expires_utc": exp.isoformat(),
                "spec_version": SPEC_VERSION})
    return out


# ---------------------------------------------------------------- axis C
def score_C(source_type: str, snapshot_age_days: int) -> Dict:
    if source_type not in SOURCE_RANK:
        raise ValueError(f"unknown source_type {source_type!r}")
    rank = SOURCE_RANK[source_type]
    if snapshot_age_days > 180:
        C, pen = 0, "hard_zero"
    else:
        pen = 0 if snapshot_age_days <= 30 else (1 if snapshot_age_days <= 90 else 2)
        C = max(0, min(3, rank - pen))
    display = {0: "do_not_show_M", 1: "show_M_greyed",
               2: "show_M_with_date", 3: "show_M_with_badge"}[C]
    return {"C": C, "source_rank": rank, "age_penalty": pen,
            "snapshot_age_days": snapshot_age_days, "display_rule": display,
            "spec_version": SPEC_VERSION}


# ---------------------------------------------------------------- rollup
def pdas(dishes: List[Dish], menu_format: str, source_type: str,
         snapshot_age_days: int, verification: Optional[Dict] = None,
         today: Optional[str] = None) -> Dict:
    m_all = score_M_all_profiles(dishes, menu_format)
    a = score_A(verification, today=today)
    c = score_C(source_type, snapshot_age_days)

    m_default = m_all[DEFAULT_PROFILE]["M"]
    if a["A"] is not None:
        tier, flag = min(m_default, a["A"]), None
    else:
        tier, flag = m_default, "kitchen_unverified"

    return {
        "M": m_all, "M_display_profile": DEFAULT_PROFILE, "A": a, "C": c,
        "tier": tier, "tier_flag": flag,
        "tier_rule": "min(M,A) when A verified else M; never shown without the flag",
        "display_M": c["C"] > 0,
        "spec_version": SPEC_VERSION,
    }
