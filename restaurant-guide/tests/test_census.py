"""Tests for the menu census. Acceptance criteria are all OBSERVABLE:
did we correctly detect which ingredients are NAMED? No suitability
assertions appear here, by design.
Run: python3 tests/test_census.py
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from census import census_dish, census_menu, restaurant_counts, load_lexicon

LEX = load_lexicon()
F = []
def ck(c, label):
    print(("  pass  " if c else "  FAIL  ") + label)
    if not c: F.append(label)

def cd(name, desc=""):
    return census_dish("t", "r", name, desc, lex=LEX)

print("\n[longest-match-first: the classic false positives]")
ck("legume" not in cd("grilled peach salad").categories, "'peach' does not match 'pea'")
ck("legume" in cd("boiled peanuts").categories, "'peanuts' -> legume")
ck("nut_seed" not in cd("boiled peanuts").categories, "'peanut' not double-counted as nut_seed")
sp = cd("roasted sweet potato")
ck("other_starch" in sp.categories, "'sweet potato' -> other_starch")
ck("potato" not in sp.categories, "'sweet potato' does not also fire plain potato")
ck("legume" in cd("english pea puree").categories, "'pea' alone -> legume")

print("\n[multi-category and ambiguity are recorded, not resolved]")
g = cd("potato gnocchi", "brown butter, sage")
ck("potato" in g.categories and "wheat_grain" in g.categories, "gnocchi -> potato AND wheat_grain")
ck("gnocchi" in g.ambiguous_terms, "gnocchi flagged ambiguous")
ck("dairy" in g.categories, "'butter' detected as dairy")
t = cd("tortilla")
ck(set(["corn","wheat_grain","egg"]).issubset(set(t.categories)), "'tortilla' -> all three readings")
ck("tortilla" in t.ambiguous_terms, "tortilla flagged ambiguous")

print("\n[free-from markers suppress, and are recorded]")
gf = cd("gluten-free pasta", "zucchini, tomato, basil")
ck("wheat_grain" not in gf.categories, "'gluten-free' suppresses wheat_grain")
ck(len(gf.free_from_markers) > 0, "free-from marker recorded, not silently dropped")
ck("vegetable" in gf.categories, "vegetable still detected alongside suppression")

print("\n[observable predicates -- the buckets requested]")
d1 = cd("patatas bravas", "crispy potato, salsa brava, garlic")
ck(d1.no_meat_no_legume_named, "potato dish: no meat, no legume named")
ck(d1.names_potato_or_starch, "potato dish: starch named")
ck(d1.starch_categories == ["potato"], f"starch categories == ['potato'], got {d1.starch_categories}")
d2 = cd("hummus plate", "chickpea, tahini, olive oil, pita")
ck(d2.no_meat_named, "hummus: no meat named")
ck(not d2.no_meat_no_legume_named, "hummus: EXCLUDED by legume -- the distinction asked for")
ck(d2.names_nut_seed, "tahini -> nut_seed reported separately")
d3 = cd("escalivada", "roasted eggplant, pepper, onion, olive oil")
ck(d3.names_no_protein_source_at_all, "escalivada: no protein-source term named at all")
ck(d3.names_vegetable, "escalivada: vegetable named")
d4 = cd("mac and cheese")
ck(d4.no_meat_named and d4.names_dairy, "mac+cheese: no meat named, dairy named -- both true, no verdict")
ck(not d4.names_no_protein_source_at_all, "mac+cheese: dairy counts as a protein source term")
d5 = cd("brisket plate", "smoked beef brisket, white bread")
ck(d5.names_meat and not d5.no_meat_named, "brisket: meat named")
ck("wheat_grain" in d5.categories, "white bread -> wheat_grain")

print("\n[absence is never evidence]")
plain = cd("seasonal vegetables")
ck(plain.completeness == "text_only_unknown", "completeness marked text_only_unknown")
ck(cd("chef's choice").categories == [], "unparseable dish yields empty categories, not a guess")

print("\n[restaurant counts: raw, with denominator]")
menu = [
 {"name":"patatas bravas","description":"potato, salsa brava"},
 {"name":"pan con tomate","description":"grilled bread, tomato, garlic"},
 {"name":"escalivada","description":"roasted eggplant, pepper, onion"},
 {"name":"espinacas con pasas","description":"spinach, raisins, pine nuts"},
 {"name":"jamon iberico","description":"cured pork"},
 {"name":"gambas al ajillo","description":"shrimp, garlic, chile"},
 {"name":"tortilla espanola","description":"potato, egg, onion"},
 {"name":"garbanzos","description":"chickpea stew"},
]
rows = census_menu(menu, "test-restaurant", lex=LEX)
c = restaurant_counts(rows)
ck(c["n_dishes"] == 8, f"n_dishes == 8, got {c['n_dishes']}")
ck(c["n_no_meat_named"] == 6, f"no-meat-named == 6, got {c['n_no_meat_named']}")
ck(c["n_no_meat_no_legume_named"] == 5, f"no-meat-no-legume == 5, got {c['n_no_meat_no_legume_named']}")
ck(c["starch_dish_counts"]["potato"] == 2, f"2 potato dishes, got {c['starch_dish_counts']['potato']}")
ck(c["absence_is_not_evidence"] is True, "counts carry the absence caveat")
ck("score" not in json.dumps(c).lower() if (json:=__import__("json")) else True,
   "counts payload contains no 'score' field")
ck(all(k.startswith("n_") or k.endswith("counts") or k in
       ("completeness","absence_is_not_evidence","census_version")
       for k in c), "payload is counts and provenance only")

print("\n" + "="*58)
print("ALL PASS" if not F else "FAILURES: " + str(F))
print("="*58)
sys.exit(1 if F else 0)
