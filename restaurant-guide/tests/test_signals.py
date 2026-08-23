"""Tests for signal detection. Every assertion is about an OBSERVABLE tag.
No test asserts that a restaurant is suitable -- that scale does not exist.
Run: python3 tests/test_signals.py
"""
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from signals import detect, load_registry, SIGNALS_VERSION

F = []
def ck(c, label):
    print(("  pass  " if c else "  FAIL  ") + label)
    if not c: F.append(label)

TAPAS = [
 {"name":"patatas bravas","description":"potato, salsa brava","menu_section":"raciones"},
 {"name":"escalivada","description":"roasted eggplant, pepper","menu_section":"verduras"},
 {"name":"pimientos de piquillo","description":"stuffed peppers","menu_section":"verduras"},
 {"name":"jamon iberico","description":"cured pork","menu_section":"embutidos"},
]
STEAK = [
 {"name":"ribeye","description":"dry aged 45 days","menu_section":"steaks"},
 {"name":"baked potato","description":"butter, chive","menu_section":"sides"},
 {"name":"creamed spinach","description":"","menu_section":"sides"},
]

print("\n[structural]")
s = detect("r/tapas", TAPAS, menu_platform="toast", reservation_platform="resy")
ck(s.signals["menu_published"]["value"] is True, "menu_published true when dishes exist")
ck(s.signals["menu_has_descriptions"]["value"] is True, "descriptions detected (3/4)")
ck(s.signals["format_a_la_carte"]["value"] is True, "a la carte when no tasting markers")
ck(s.signals["sides_section_size"]["value"] == 2, f"2 sides/veg sections, got {s.signals['sides_section_size']['value']}")
ck(s.signals["has_online_ordering"]["value"] is True, "toast -> online ordering")

t = detect("r/tasting", [{"name":"seven course tasting menu","description":"no substitutions"}])
ck(t.signals["format_a_la_carte"]["value"] is False, "tasting markers -> not a la carte")
ck("tasting menu" in t.signals["format_a_la_carte"]["evidence"], "evidence names the marker found")

print("\n[camouflage -- the 'no big deal' axis]")
ck(s.signals["compose_your_own_format"]["value"] is True, "'raciones' -> compose-your-own format")
st = detect("r/steak", STEAK)
ck(st.signals["compose_your_own_format"]["value"] is False, "steakhouse is not compose-your-own")
ck(st.signals["sides_section_size"]["value"] == 2, "steakhouse sides still counted")
c = detect("r/counter", [{"name":"fish plate"}], site_text="Counter service. Order at the counter.")
ck(c.signals["counter_or_kiosk_service"]["value"] is True, "counter service detected")
b = detect("r/byo", [{"name":"build your own bowl","description":"choose your base"}])
ck(b.signals["build_your_own_item"]["value"] is True, "build-your-own detected")

print("\n[accommodation evidence -- machine-readable, and only evidence]")
mods = {"polenta":["no cheese","extra herbs"],
        "salad":["dressing on the side","add chicken"],
        "steak":["medium rare","medium"]}
m = detect("r/mods", STEAK, modifier_groups=mods, reservation_platform="opentable")
ck(m.signals["modifier_groups_present"]["value"] == 2,
   f"2 dishes expose remove/sub modifiers, got {m.signals['modifier_groups_present']['value']}")
ck("polenta" in m.signals["modifier_groups_present"]["evidence"], "evidence quotes a real modifier")
ck(m.signals["special_request_field"]["value"] is True, "opentable -> special-request field")
ck(m.signals["modifier_groups_present"]["family"] == "accommodation_evidence",
   "modifier groups are accommodation EVIDENCE, not verification")
none = detect("r/phone", STEAK, reservation_platform="phone")
ck(none.signals["special_request_field"]["value"] is False, "phone-only -> no request field")
d = detect("r/diet", STEAK, site_text="Please let us know about dietary restrictions.")
ck(d.signals["dietary_page_exists"]["value"] is True, "dietary statement detected")

print("\n[census-derived tags]")
counts = {"n_dishes":8,"n_names_no_protein_source_at_all":3,
          "starch_dish_counts":{"potato":2,"corn":1,"wheat_grain":0,"rice":0,
                                "pseudo_grain":0,"other_starch":0}}
cs = detect("r/c", TAPAS, census_counts=counts)
ck(cs.signals["starch_family_count"]["value"] == 2, "2 starch families named")
ck(cs.signals["vegetable_forward_menu"]["value"] == 3, "3 dishes name no protein source")
ck("Does NOT mean low protein" in cs.signals["vegetable_forward_menu"]["evidence"],
   "vegetable-forward tag carries its own anti-inference warning")

print("\n[no composite, no judgment]")
payload = json.dumps(s.signals).lower()
for banned in ("score","rating","suitab","rank","tier_total","phe_budget","threshold"):
    ck(banned not in payload, f"payload contains no '{banned}'")
ck(isinstance(s.tags(), list) and all(isinstance(x,str) for x in s.tags()),
   "tags() returns a flat filterable key list, not a number")
ck(all("provenance" not in k for k in s.signals) and
   all(v["source"] for v in s.signals.values()), "every signal carries a source")
ck(all(v["signals_version"]==SIGNALS_VERSION for v in s.signals.values()),
   "every signal carries its version")

print("\n[registry integrity]")
R = load_registry()
keys = {x["key"] for x in R["signals"]}
detected = set(s.signals) | set(cs.signals) | set(m.signals)
ck(detected <= keys, f"every detected key is registered; stray={detected-keys}")
ck(len(R["explicitly_rejected"]) >= 4, "rejected signals are documented, not silently dropped")
rej = json.dumps(R["explicitly_rejected"]).lower()
ck("place_id" in rej and "places" in rej, "Google rating rejection cites the caching policy")
ck("gluten" in rej and "higher" in rej, "gluten-free-as-proxy rejection is recorded")
ck(any(x["family"]=="camouflage" for x in R["signals"]), "camouflage family exists in registry")
ck(sum(1 for x in R["signals"] if x["machine_readable"]) >= 15,
   "at least 15 of 18 signals are machine-readable")

print("\n" + "="*58)
print("ALL PASS" if not F else "FAILURES: " + str(F))
print("="*58)
sys.exit(1 if F else 0)
