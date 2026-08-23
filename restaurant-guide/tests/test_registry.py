"""Tests for the open registry. The point being tested: an award is optional
metadata, never a gate on membership.

Run: python3 tests/test_registry.py
"""
import sys, os, json, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from registry import (make_record, add, load, save, find, slugify, city_id, SOURCES,
                      add_alias)

F = []
def ck(c, label):
    print(("  pass  " if c else "  FAIL  ") + label)
    if not c: F.append(label)

print("\n[membership needs no award]")
r = make_record("Some Diner", "Asheville", "NC", source="community", added_by="nina")
ck(r["awards"] == [], "a record with no award is valid")
ck(r["provenance"]["source"] == "community", "source recorded")
ck(r["provenance"]["added_by"] == "nina", "who added it is recorded")
ck(r["census"]["status"] == "no_menu_captured", "census starts empty")
ck(r["accommodation"]["status"] == "unverified", "accommodation starts unverified")
ck("not zero" in r["accommodation"]["note"], "'unverified is not zero' travels with the record")
reg = {"schema_version":"registry-v1","restaurants":[]}
ck(add(reg, r) == "added", "added to an empty registry")
ck(len(reg["restaurants"]) == 1, "registry has 1")

print("\n[awards are optional decoration]")
a = make_record("Star Place", "Asheville", "NC", source="award", added_by="nina",
                citation="press", award={"program":"MICHELIN Guide","tier":"Selected","year":"2025"})
add(reg, a)
ck(len(a["awards"]) == 1, "award attached when supplied")
ck(a["awards"][0]["tier"] == "Selected", "tier stored verbatim, not normalised")
ck(isinstance(a["awards"], list), "awards is a LIST -- a restaurant can hold several")

print("\n[the fix: a Michelin negative control can still be in the registry]")
# Chai Pani is NOT in the Michelin selection. That makes it a negative control
# for the Michelin AWARD, and says nothing about whether it belongs in the guide.
nc = make_record("Chai Pani", "Asheville", "NC", source="local_list", added_by="nina",
                 citation="Best of WNC")
ck(add(reg, nc) == "added", "a Michelin non-member is added without objection")
ck(nc["awards"] == [], "and carries no Michelin award")
ncf = os.path.join(os.path.dirname(__file__), "..", "data", "negative_controls.json")
if os.path.exists(ncf):
    n = json.load(open(ncf, encoding="utf-8"))
    names = {e["name"] for e in n["not_in_selection"]}
    ck("Chai Pani" in names, "still a negative control for the Michelin claim specifically")
    ck("award" in n["rule"].lower() or "michelin" in n["rule"].lower(),
       "the rule is scoped to award membership, not registry membership")

print("\n[reaching the same restaurant twice keeps both routes]")
again = make_record("Chai Pani", "Asheville", "NC", source="award", added_by="nina",
                    citation="JBF 2022", award={"program":"James Beard Foundation","tier":"Winner"})
ck(add(reg, again) == "merged", "second sighting merges, does not duplicate")
got = find(reg, "asheville-nc-us/chai-pani")
ck(len(got["awards"]) == 1, "the award from the second route is kept")
ck(len(got["provenance"]["citations"]) == 2, "both citations kept")
ck(got["provenance"]["also_found_via"] == ["award"], "second route recorded, first not overwritten")
ck(len([x for x in reg["restaurants"] if x["slug"]=="chai-pani"]) == 1, "no duplicate row")

print("\n[ids are stable and portable]")
ck(slugify("Cúrate Bar de Tapas") == "curate-bar-de-tapas", "accents folded")
ck(slugify("Leo's House of Thirst") == "leos-house-of-thirst", "apostrophes dropped")
ck(slugify("Bull & Beggar") == "bull-beggar", "ampersand handled")
ck(city_id("Asheville","NC","us") == "asheville-nc-us", "city id from city/region/country")
ck(city_id("Seville","","es") == "seville-es", "region optional -- works outside the US")
ck(city_id("Ho Chi Minh City","","vn") == "ho-chi-minh-city-vn", "multi-word city")
ck(make_record("X","Melbourne","VIC","au")["restaurant_id"] == "melbourne-vic-au/x",
   "any city, no code change")

print("\n[guardrails]")
try:
    make_record("Y","Asheville","NC",source="because_i_like_it"); ck(False,"bad source rejected")
except ValueError: ck(True, "an unrecognised source is rejected")
try:
    make_record("  ","Asheville","NC"); ck(False,"blank name rejected")
except ValueError: ck(True, "a blank name is rejected")
ck(add(reg, make_record("Some Diner","Asheville","NC",added_by="x"), merge=False) == "duplicate",
   "merge=False reports a duplicate instead of writing one")
ck("community" in SOURCES and "self_submitted" in SOURCES,
   "community and self-submission are first-class sources")

print("\n[no judgment in the schema]")
blob = json.dumps(r).lower()
for banned in ("score","rating","rank","suitab","tier_total","phe_budget","threshold"):
    ck(banned not in blob, f"record contains no '{banned}'")

print("\n[round-trips to disk]")
with tempfile.TemporaryDirectory() as d:
    p = os.path.join(d, "reg.json")
    save(reg, p)
    back = load(p)
    ck(back["restaurant_count"] == len(reg["restaurants"]), "count written on save")
    ck("updated_utc" in back, "timestamp written on save")
    ck(find(back, "asheville-nc-us/chai-pani") is not None, "records survive the round trip")
    ck(load(os.path.join(d,"missing.json"))["restaurants"] == [],
       "a missing registry loads as empty, not an error")

print("\n[tier labels are verbatim, never internal slugs]")
# The seed migration once copied slugs ('recommended') into the tier field,
# which contradicted the contributor guide telling everyone to write
# 'Selected'. Two label buckets for one tier is a silent query bug.
import re as _re
_p = os.path.join(os.path.dirname(__file__), "..", "data", "restaurants.json")
if os.path.exists(_p):
    live = json.load(open(_p, encoding="utf-8"))
    tiers = [a.get("tier", "") for r in live["restaurants"] for a in r.get("awards", [])]
    ck(tiers, f"live registry has {len(tiers)} award entries to check")
    slugs = [t for t in tiers if _re.search(r"[_+]|^[a-z]", t)]
    ck(not slugs, f"no snake_case or lowercase slugs in tier labels; found {slugs[:4]}")
    ck("Selected" in tiers and "recommended" not in tiers,
       "the non-starred Michelin tier is stored as 'Selected', not 'recommended'")
    ck(not [t for t in tiers if "+" in t],
       "no compound tier -- two recognitions are two entries, never one flattened label")
    lum = [r for r in live["restaurants"] if r["slug"] == "luminosa"]
    if lum:
        mich = [a["tier"] for a in lum[0]["awards"] if a.get("program") == "MICHELIN Guide"]
        ck(sorted(mich) == ["Bib Gourmand", "Green Star"],
           f"Luminosa holds both recognitions as separate entries, got {mich}")
    adding = os.path.join(os.path.dirname(__file__), "..", "ADDING.md")
    if os.path.exists(adding):
        doc = open(adding, encoding="utf-8").read()
        ck("Selected" in doc, "ADDING.md names the same label the data uses")

print("\n[a rename must not orphan captured menus]")
# The seed migration renamed 'curate' to 'curate-bar-de-tapas' by slugifying the
# full name, orphaning 84 captured dishes. Aliases make the old id resolvable.
_reg = {"schema_version":"registry-v1","restaurants":[]}
add(_reg, make_record("Curate Bar de Tapas","Asheville","NC",added_by="x",source="award"))
ck(find(_reg,"asheville-nc-us/curate") is None, "before the alias, the old id does not resolve")
ck(add_alias(_reg,"asheville-nc-us/curate-bar-de-tapas","curate"), "alias recorded")
ck(find(_reg,"asheville-nc-us/curate") is not None, "old id resolves after the alias")
ck(find(_reg,"curate") is not None, "a bare slug resolves via alias too")
ck(find(_reg,"asheville-nc-us/curate-bar-de-tapas") is not None, "live id still resolves")
add(_reg, make_record("Curate","Asheville","NC",added_by="x",source="community"))
ck(not add_alias(_reg,"asheville-nc-us/curate-bar-de-tapas","curate"),
   "an alias that collides with a different restaurant's live slug is refused")
_live = os.path.join(os.path.dirname(__file__), "..", "data", "restaurants.json")
if os.path.exists(_live):
    _mdir = os.path.join(os.path.dirname(__file__), "..", "data", "menus")
    if os.path.isdir(_mdir):
        _rl = json.load(open(_live, encoding="utf-8"))
        _dirs = [d for d in os.listdir(_mdir) if os.path.isdir(os.path.join(_mdir, d))]
        _orphans = [d for d in _dirs if find(_rl, "asheville-nc-us/" + d) is None]
        ck(not _orphans, f"every captured menu dir resolves to a record; orphans={_orphans}")

print("\n" + "="*58)
print("ALL PASS" if not F else "FAILURES: " + str(F))
print("="*58)
sys.exit(1 if F else 0)
