"""Tests for PDAS v0.1. The four archetypes are the acceptance criteria:
they encode WHY the single ladder was wrong, so a regression here means
the model has collapsed back into one dimension.
Run: python3 tests/test_pdas.py
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from pdas import Dish, score_M, score_M_all_profiles, score_A, score_C, pdas

FAILS = []
def check(cond, label):
    if cond: print(f"  pass  {label}")
    else:
        print(f"  FAIL  {label}"); FAILS.append(label)

def d(i, med, low=None, high=None, **kw):
    low = med * 0.7 if low is None else low
    high = med * 1.4 if high is None else high
    return Dish(dish_id=i, name=i, phe_mg_low=low, phe_mg_median=med,
                phe_mg_high=high, **kw)

# ---- 9.1 barbecue: M1 on the menu, A4 in the kitchen ----------------
print("\n[9.1] barbecue / charcuterie")
bbq = [
    d("brisket", 1900, 1500, 2400), d("ribs", 1700, 1300, 2200),
    d("sausage", 1200, 900, 1600), d("mac_cheese", 420, 320, 560),
    d("baked_beans", 380, 280, 500),
    d("fries", 95, 60, 190, is_anchor_candidate=True, anchor_uncertain=True),
    d("hush_puppies", 150, 100, 230),
    d("collards", 45, 25, 80),
    d("slaw", 55, 35, 95, mods_required=["sauce_on_side"]),
]
m = score_M(bbq, "a_la_carte", "MID")
check(m["M"] == 1, f"M(MID) == 1, got {m['M']}")
check(m["inputs"]["n_distinct_anchors"] == 0, "fries excluded as certain anchor (dusting unknown)")
check(m["inputs"]["n_anchor_uncertain"] == 1, "fries counted as uncertain anchor")
full = pdas(bbq, "a_la_carte", "structured_platform", 10,
            verification={"A": 4, "verified_by": "test", "verified_utc": "2026-08-01",
                          "method": "phone", "evidence": "will boil guest-supplied low-pro pasta"},
            today="2026-08-23")
check(full["tier"] == 1, f"tier = min(1,4) = 1, got {full['tier']}")
check(full["A"]["A"] == 4, "A4 recorded and visible despite M1 -- the case the ladder loses")

# ---- 9.2 steakhouse: thin but real -----------------------------------
print("\n[9.2] old-style steakhouse")
steak = [
    d("ribeye", 1800, 1400, 2300), d("filet", 1500, 1200, 1900),
    d("creamed_spinach", 340, 250, 450),
    d("baked_potato", 24, 16, 38, is_anchor_candidate=True),
    d("onion_rings", 210, 150, 300),
    d("mushrooms", 62, 40, 95),
    d("wedge", 88, 60, 130, mods_required=["omit_cheese", "omit_meat_fish"]),
]
allp = score_M_all_profiles(steak, "a_la_carte")
check(allp["MID"]["M"] == 2, f"M(MID) == 2, got {allp['MID']['M']}")
check(allp["TIGHT"]["M"] >= 1, f"TIGHT still scoreable, got {allp['TIGHT']['M']}")
check(allp["TIGHT"]["M"] <= allp["WIDE"]["M"], "M monotone in budget")
check(steak[3].is_anchor(120), "baked potato is an anchor at MID")

# ---- 9.3 tapas: M4, the reference case -------------------------------
print("\n[9.3] Spanish tapas")
tapas = [
    d("patatas_bravas", 58, 40, 85, is_anchor_candidate=True),
    d("tortilla_espanola", 95, 70, 135, is_anchor_candidate=True),
    d("pan_con_tomate", 105, 75, 150),
    d("escalivada", 42, 28, 65, is_vegetable_entree=True),
    d("pimientos_piquillo", 66, 45, 98),
    d("espinacas_pasas", 78, 55, 112, is_vegetable_entree=True),
    d("croquetas", 290, 210, 390),
    d("jamon", 1400, 1100, 1800),
    d("gambas", 780, 600, 1000, mods_required=["halve_component"]),
]
m3 = score_M(tapas, "a_la_carte", "MID")
check(m3["M"] == 4, f"M(MID) == 4, got {m3['M']}")
check(m3["inputs"]["n_distinct_anchors"] >= 2, "two distinct anchors (M4 gate)")
check(m3["inputs"]["plausible_vegetable_entree"], "vegetable entree present (M4 gate)")
m3b = score_M(tapas, "partial_fixed", "MID")
check(m3b["M"] == 3, f"same dishes, non-a-la-carte format -> M3, got {m3b['M']}")

# ---- 9.4 the tasting-menu trap: ladder says 3, truth is 0 -----------
print("\n[9.4] tasting menu trap")
tasting = [
    d("veg_course_1", 40, 28, 60, is_anchor_candidate=True),
    d("veg_course_2", 52, 36, 75, is_vegetable_entree=True),
    d("veg_course_3", 48, 32, 70, is_anchor_candidate=True),
    d("veg_course_4", 61, 42, 88),
    d("veg_course_5", 58, 40, 84, mods_required=["omit_cheese"]),
    d("veg_course_6", 44, 30, 64, mods_required=["omit_nuts_seeds"]),
    d("veg_course_7", 70, 50, 100, mods_required=["sauce_on_side"]),
]
mx = score_M(tasting, "tasting_only", "MID")
check(mx["M"] == 2 and mx["tasting_cap_applied"], f"tasting cap applied, M={mx['M']}")
X = pdas(tasting, "tasting_only", "structured_platform", 5,
         verification={"A": 0, "verified_by": "test", "verified_utc": "2026-08-01",
                       "method": "email", "evidence": "no substitutions to the progression"},
         today="2026-08-23")
check(X["tier"] == 0, f"Restaurant X tier == 0 (ladder would say 3), got {X['tier']}")
Y = pdas(tasting, "a_la_carte", "structured_platform", 5,
         verification={"A": 4, "verified_by": "test", "verified_utc": "2026-08-01",
                       "method": "in_person", "evidence": "swaps courses, cooks supplied low-pro pasta"},
         today="2026-08-23")
check(Y["tier"] > X["tier"], f"Restaurant Y ({Y['tier']}) > X ({X['tier']}) on the same menu")

# ---- axis A discipline ----------------------------------------------
print("\n[A axis] verification discipline")
u = score_A(None)
check(u["A"] is None and u["A_status"] == "unverified", "no contact -> None, not 0")
zero = score_A({"A": 0, "verified_by": "t", "verified_utc": "2026-08-01",
                "method": "phone", "evidence": "declined"})
check(zero["A"] == 0 and zero["A_status"] == "verified", "A=0 is a sourced finding, distinct from unverified")
exp = score_A({"A": 4, "verified_by": "t", "verified_utc": "2025-01-01",
               "method": "phone", "evidence": "old"}, today="2026-08-23")
check(exp["A"] is None and exp["A_status"] == "expired", "verification older than 180d expires")
check(exp["prior_A"] == 4, "expired verification retains prior value for audit")
try:
    score_A({"A": 3, "verified_by": "t"}); check(False, "missing fields must raise")
except ValueError: check(True, "incomplete verification rejected")

# ---- axis C ---------------------------------------------------------
print("\n[C axis] confidence and display gating")
check(score_C("structured_platform", 10)["C"] == 2, "fresh structured -> C2")
check(score_C("restaurant_confirmed", 10)["C"] == 3, "fresh confirmed -> C3")
check(score_C("pdf_or_vision", 100)["C"] == 0, "old PDF -> C0")
check(score_C("restaurant_confirmed", 200)["C"] == 0, "over 180d -> C0 regardless of source")
check(score_C("social_post", 1)["C"] == 0, "social post never above C0")
check(score_C("pdf_or_vision", 100)["display_rule"] == "do_not_show_M", "C0 suppresses M display")
g = pdas(tapas, "a_la_carte", "pdf_or_vision", 200)
check(g["display_M"] is False, "stale menu -> M not displayed even though M was computed")

# ---- interval discipline --------------------------------------------
print("\n[intervals] guardrails")
try:
    Dish("bad", "bad", 100, 50, 200); check(False, "unordered interval must raise")
except ValueError: check(True, "unordered interval rejected")
try:
    Dish("bad2", "bad2", 1, 2, 3, mods_required=["make_it_nice"]); check(False, "bad mod must raise")
except ValueError: check(True, "mod outside closed list rejected")
wide = [d("wide_anchor", 100, 20, 400, is_anchor_candidate=True)]
check(len([x for x in wide if x.clears(120)]) == 0, "median within budget but high tail -> not safe")

print("\n" + "="*60)
print(f"{'ALL PASS' if not FAILS else 'FAILURES: ' + str(FAILS)}")
print("="*60)
sys.exit(1 if FAILS else 0)
