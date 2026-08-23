"""Signal detection v0.1 — taggable QC facts about a restaurant.

Detects the machine-readable tags in data/signal_registry.json from a menu
snapshot plus platform metadata. Every tag is independent and carries its
own provenance and evidence. No composite score is computed, no tag is
combined with another, and nothing here says a restaurant is suitable --
the suitability scale is the project owner's to define.

Design constraint that shapes this file: a tag is only worth having if it
is (a) machine-readable, (b) free to store, and (c) uniform across
countries. That rules out crowd ratings -- Google's Places policies allow
storing only place_id indefinitely -- and rules out anything requiring a
per-restaurant phone call as the primary path.

Standard library only, Python 3.8+.
"""
from __future__ import annotations
import json, os, re
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional

SIGNALS_VERSION = "signals-v0.1"
_REG = os.path.join(os.path.dirname(__file__), "..", "data", "signal_registry.json")

# Menu-section names indicating standalone sides / vegetable plates.
SIDES_SECTIONS = ("side", "sides", "vegetable", "vegetables", "verdure", "contorni",
                  "contorno", "verduras", "guarnicion", "guarniciones", "banchan",
                  "small plates", "snacks", "for the table", "a la carte sides")

# Formats where composing your own meal from many small plates IS the house
# style, so ordering five vegetable dishes is invisible rather than notable.
COMPOSE_FORMATS = ("tapas", "mezze", "meze", "dim sum", "izakaya", "small plates",
                   "raciones", "pintxos", "banchan", "antipasti", "cicchetti",
                   "share plates", "shared plates", "family style")

TASTING_MARKERS = ("tasting menu", "chef's tasting", "chefs tasting", "prix fixe",
                   "prix-fixe", "set menu", "omakase", "menu degustation",
                   "menú degustación", "degustazione", "no substitutions",
                   "no modifications", "menu only", "coursed menu")

BUILD_YOUR_OWN = ("build your own", "build-your-own", "create your own", "your way",
                  "choose your", "pick two", "pick three", "make it a")

COUNTER_MARKERS = ("counter service", "order at the counter", "walk up", "walk-up",
                   "kiosk", "self-order", "order online", "quick service", "fast casual",
                   "no table service")

ALLERGEN_MARKERS = ("allergen", "allergens", "dietary matrix", "nutrition information",
                    "allergy information", "dietary information", "nutritional info")

DIETARY_PAGE_MARKERS = ("dietary restrictions", "dietary needs", "dietary requests",
                        "special diets", "food allergies", "accommodate",
                        "accommodations", "let us know", "dietary accommodations")


@dataclass
class Signal:
    key: str
    value: object
    family: str
    evidence: str
    source: str
    machine_readable: bool = True
    signals_version: str = SIGNALS_VERSION


@dataclass
class RestaurantSignals:
    restaurant_id: str
    snapshot_id: Optional[str] = None
    signals: Dict[str, Dict] = field(default_factory=dict)
    signals_version: str = SIGNALS_VERSION
    note: str = ("Independent tags, each with its own provenance. No composite "
                 "score. No suitability judgment. Absence of a tag is not "
                 "evidence of its opposite.")

    def add(self, s: Signal):
        self.signals[s.key] = asdict(s)

    def tags(self) -> List[str]:
        """Keys whose value is truthy -- the filterable tag list."""
        return sorted(k for k, v in self.signals.items() if v["value"])


def _blob(dishes: List[Dict]) -> str:
    return " ".join(f"{d.get('name','')} {d.get('description','')} "
                    f"{d.get('menu_section','')}" for d in dishes).lower()


def detect(restaurant_id: str, dishes: List[Dict],
           snapshot_id: Optional[str] = None,
           menu_platform: Optional[str] = None,
           site_text: str = "",
           modifier_groups: Optional[Dict[str, List[str]]] = None,
           reservation_platform: Optional[str] = None,
           census_counts: Optional[Dict] = None,
           menu_format_hint: Optional[str] = None) -> RestaurantSignals:
    out = RestaurantSignals(restaurant_id=restaurant_id, snapshot_id=snapshot_id)
    blob = _blob(dishes)
    site = (site_text or "").lower()
    n = len(dishes)

    # ---------------- structural
    out.add(Signal("menu_published", bool(dishes), "structural",
                   f"{n} dishes captured", "menu snapshot"))

    n_desc = sum(1 for d in dishes if (d.get("description") or "").strip())
    out.add(Signal("menu_has_descriptions", n_desc >= max(1, int(0.5 * n)) if n else False,
                   "structural", f"{n_desc}/{n} dishes carry a description",
                   "menu snapshot"))

    tasting_hits = [m for m in TASTING_MARKERS if m in blob or m in site]
    is_tasting = (menu_format_hint == "tasting_only") or bool(tasting_hits)
    out.add(Signal("format_a_la_carte", not is_tasting, "structural",
                   f"tasting markers: {tasting_hits}" if tasting_hits
                   else "no tasting/prix-fixe markers found", "menu structure"))

    sides = [d for d in dishes
             if any(s in (d.get("menu_section") or "").lower() for s in SIDES_SECTIONS)]
    out.add(Signal("sides_section_size", len(sides), "structural",
                   f"{len(sides)} dishes in sides/vegetable sections", "menu structure"))

    if census_counts:
        fams = [k for k, v in census_counts.get("starch_dish_counts", {}).items() if v]
        out.add(Signal("starch_family_count", len(fams), "structural",
                       f"starch families named: {fams}", "census"))

    allerg = [m for m in ALLERGEN_MARKERS if m in site]
    out.add(Signal("allergen_matrix_published", bool(allerg), "structural",
                   f"markers: {allerg}" if allerg else "none found on captured site text",
                   "restaurant site"))

    STRUCTURED = ("toast", "square", "chownow", "clover", "olo", "olo_serve",
                  "doordash", "popmenu", "bentobox")
    out.add(Signal("has_online_ordering",
                   bool(menu_platform and menu_platform.lower() in STRUCTURED),
                   "structural", f"platform={menu_platform}", "platform detection"))

    # ---------------- accommodation evidence (machine-readable subset)
    # A published modifier group is a kitchen capability the restaurant has
    # already committed to in machine-readable form. Evidence, never
    # verification: it proves the option exists, not that staff apply it.
    mg = modifier_groups or {}
    REMOVE = re.compile(r"\b(no|without|omit|remove|hold|sub|substitute|swap|"
                        r"on the side|light|extra|add)\b", re.I)
    hits = {dish: [o for o in opts if REMOVE.search(o)] for dish, opts in mg.items()}
    hits = {k: v for k, v in hits.items() if v}
    out.add(Signal("modifier_groups_present", len(hits), "accommodation_evidence",
                   f"{len(hits)} dishes expose remove/substitute modifiers"
                   + (f"; e.g. {list(hits.items())[0]}" if hits else ""),
                   "ordering platform menu JSON"))

    BOOKING = ("opentable", "resy", "tock", "sevenrooms", "yelp_reservations")
    out.add(Signal("special_request_field",
                   bool(reservation_platform and reservation_platform.lower() in BOOKING),
                   "accommodation_evidence",
                   f"reservation_platform={reservation_platform}; free-text request "
                   "field reaches the kitchen, needs no API partnership",
                   "booking platform"))

    diet = [m for m in DIETARY_PAGE_MARKERS if m in site]
    out.add(Signal("dietary_page_exists", bool(diet), "accommodation_evidence",
                   f"markers: {diet}" if diet else "none found in captured site text",
                   "restaurant site"))

    # ---------------- camouflage
    comp = [f for f in COMPOSE_FORMATS if f in blob or f in site]
    out.add(Signal("compose_your_own_format", bool(comp), "camouflage",
                   f"format markers: {comp}" if comp else "none found",
                   "menu structure"))

    counter = [m for m in COUNTER_MARKERS if m in site or m in blob]
    out.add(Signal("counter_or_kiosk_service", bool(counter), "camouflage",
                   f"markers: {counter}" if counter else "none found",
                   "restaurant site"))

    byo = [m for m in BUILD_YOUR_OWN if m in blob]
    out.add(Signal("build_your_own_item", bool(byo), "camouflage",
                   f"markers: {byo}" if byo else "none found", "menu structure"))

    if census_counts:
        veg = census_counts.get("n_names_no_protein_source_at_all", 0)
        out.add(Signal("vegetable_forward_menu", veg, "camouflage",
                       f"{veg}/{census_counts.get('n_dishes', 0)} dishes name no "
                       "protein source at all -- ordering one as a main is unremarkable. "
                       "Does NOT mean low protein.", "census"))

    kids = ("kids", "kid's", "children", "little", "menu bambini", "niños")
    out.add(Signal("kids_menu_present",
                   any(k in (d.get("menu_section") or "").lower() for d in dishes for k in kids)
                   or any(k in site for k in kids),
                   "camouflage", "kids/children menu section or site mention",
                   "menu structure"))
    return out


def load_registry(path: str = _REG) -> Dict:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)
