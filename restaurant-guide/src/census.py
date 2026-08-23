"""Menu census v0.1 — OBSERVABLE menu facts. No diet judgment.

What this does: reads menu text, records which ingredient categories are
NAMED in each dish, and counts. That is all.

What this deliberately does NOT do: assign a phe budget, apply a threshold,
call a dish suitable or unsuitable, rank restaurants, or produce a score.
The suitability scale is defined by the project owner after the corpus
exists, not by this module. See spec/menu-census-v0.1.md.

The one inference rule, stated once: a term match means the ingredient is
NAMED. A non-match means NOTHING. Menu prose is marketing, not a recipe.
Every row carries completeness='text_only_unknown' to keep that visible
downstream.

Standard library only, Python 3.8+.
"""
from __future__ import annotations
import json, os, re
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Set

CENSUS_VERSION = "menu-census-v0.1"
_LEX_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "ingredient_lexicon.json")

PROTEIN_SOURCE_CATS = ("animal_muscle", "cured_meat", "dairy", "egg", "legume", "nut_seed")
STARCH_CATS = ("wheat_grain", "pseudo_grain", "potato", "rice", "corn", "other_starch")
MEAT_CATS = ("animal_muscle", "cured_meat")


def load_lexicon(path: str = _LEX_PATH) -> Dict:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _compile(lex: Dict):
    """Longest-term-first so 'sweet potato' wins over 'potato' and
    'peanut' is not read as 'pea'."""
    pairs = []
    for cat, spec in lex["categories"].items():
        for term in spec["terms"]:
            pairs.append((term.lower(), cat))
    pairs.sort(key=lambda p: -len(p[0]))
    compiled = [(re.compile(r"(?<![\w-])" + re.escape(t) + r"(?:e?s)?(?![\w-])"), t, c)
                for t, c in pairs]
    # Keep the readable label alongside the pattern. Storing p.pattern leaked
    # regex source ("(?<![\\w-])gf(?![\\w-])") into the output rows.
    free = [(re.compile(r"(?<![\w-])" + re.escape(m) + r"(?![\w-])"), m)
            for m in lex.get("free_from_markers", [])]
    # Compound-word terms: 'shrimpburger' hides 'shrimp' inside one word, so
    # word-boundary matching misses it entirely. Substring-matched, and only
    # as a fallback after boundary matching, to limit false positives.
    compound = [(re.compile(re.escape(t)), t, c)
                for t, c in sorted(lex.get("compound_substring_terms", {}).items(),
                                   key=lambda kv: -len(kv[0]))]
    return compiled, free, compound


@dataclass
class DishCensus:
    dish_id: str
    restaurant_id: str
    name: str
    description: str = ""
    menu_section: Optional[str] = None
    price_usd: Optional[float] = None
    matched_terms: Dict[str, List[str]] = field(default_factory=dict)  # cat -> terms
    categories: List[str] = field(default_factory=list)
    ambiguous_terms: List[str] = field(default_factory=list)
    free_from_markers: List[str] = field(default_factory=list)
    completeness: str = "text_only_unknown"
    census_version: str = CENSUS_VERSION

    # ---- observable predicates. Each is a statement about NAMED terms only.
    @property
    def names_meat(self) -> bool:
        return any(c in self.categories for c in MEAT_CATS)

    @property
    def names_legume(self) -> bool:
        return "legume" in self.categories

    @property
    def names_dairy(self) -> bool:
        return "dairy" in self.categories

    @property
    def names_egg(self) -> bool:
        return "egg" in self.categories

    @property
    def names_nut_seed(self) -> bool:
        return "nut_seed" in self.categories

    @property
    def names_any_protein_source(self) -> bool:
        return any(c in self.categories for c in PROTEIN_SOURCE_CATS)

    @property
    def starch_categories(self) -> List[str]:
        return [c for c in STARCH_CATS if c in self.categories]

    @property
    def names_vegetable(self) -> bool:
        return "vegetable" in self.categories

    # ---- the three buckets Nina asked for, as raw membership, not a rating
    @property
    def no_meat_named(self) -> bool:
        """'vegetarian' in the observable sense: no meat/poultry/fish term named."""
        return not self.names_meat

    @property
    def no_meat_no_legume_named(self) -> bool:
        """Multiple of these is the thing that makes a menu workable.
        Dairy, egg and nuts are reported SEPARATELY, not folded in."""
        return not self.names_meat and not self.names_legume

    @property
    def names_potato_or_starch(self) -> bool:
        return bool(self.starch_categories)

    @property
    def names_no_protein_source_at_all(self) -> bool:
        """Nothing from any protein-source category is named. The strongest
        observable statement available from menu text -- and still not proof."""
        return not self.names_any_protein_source


def census_dish(dish_id: str, restaurant_id: str, name: str, description: str = "",
                menu_section: Optional[str] = None, price_usd: Optional[float] = None,
                lex: Optional[Dict] = None) -> DishCensus:
    lex = lex or load_lexicon()
    compiled, free, compound = _compile(lex)
    amb = lex.get("ambiguous_terms", {})
    blob = f"{name} {description}".lower()

    hits_free = [label for p, label in free if p.search(blob)]
    suppress: Set[str] = set()
    for m in hits_free:
        raw = m.replace(r"(?<![\w-])", "").replace(r"(?![\w-])", "").replace("\\", "")
        if "gluten" in raw:  suppress.add("wheat_grain")
        if "dairy" in raw or "cheese" in raw: suppress.add("dairy")
        if "nut" in raw:     suppress.add("nut_seed")
        if raw in ("vegan",): suppress.update(("dairy", "egg", "animal_muscle", "cured_meat"))
        if raw in ("meatless", "plant based", "plant-based"):
            suppress.update(("animal_muscle", "cured_meat"))

    matched: Dict[str, List[str]] = {}
    found_amb: List[str] = []
    consumed: List[tuple] = []   # (start, end) of accepted matches, longest-first
    for pat, term, cat in compiled:
        for mo in pat.finditer(blob):
            s, e = mo.span()
            if any(s < ce and cs < e for cs, ce in consumed):
                continue           # overlaps a longer, already-accepted term
            consumed.append((s, e))
            cats = amb.get(term, [cat])
            if term in amb:
                found_amb.append(term)
            for c in cats:
                if c in suppress:
                    continue
                matched.setdefault(c, [])
                if term not in matched[c]:
                    matched[c].append(term)

    # fallback pass: compound words the boundary matcher could not see
    compound_hits: List[str] = []
    for pat, term, cat in compound:
        if cat in suppress or cat in matched:
            continue
        for mo in pat.finditer(blob):
            s_, e_ = mo.span()
            if any(s_ < ce and cs < e_ for cs, ce in consumed):
                continue
            consumed.append((s_, e_))
            matched.setdefault(cat, [])
            label = term + " (compound)"
            if label not in matched[cat]:
                matched[cat].append(label)
                compound_hits.append(term)
            break

    return DishCensus(
        dish_id=dish_id, restaurant_id=restaurant_id, name=name,
        description=description, menu_section=menu_section, price_usd=price_usd,
        matched_terms=matched, categories=sorted(matched),
        ambiguous_terms=sorted(set(found_amb)), free_from_markers=hits_free,
        completeness="text_only_unknown",
    )


def census_menu(dishes: List[Dict], restaurant_id: str, lex: Optional[Dict] = None
                ) -> List[DishCensus]:
    lex = lex or load_lexicon()
    return [census_dish(d.get("dish_id") or f"{restaurant_id}#{i}", restaurant_id,
                        d["name"], d.get("description", ""), d.get("menu_section"),
                        d.get("price_usd"), lex=lex)
            for i, d in enumerate(dishes)]


def restaurant_counts(rows: List[DishCensus]) -> Dict:
    """RAW COUNTS. No score, no rank, no threshold. Denominator always shown
    so a count is never read without knowing the menu size."""
    n = len(rows)
    starch_breakdown = {c: sum(1 for r in rows if c in r.categories) for c in STARCH_CATS}
    protein_breakdown = {c: sum(1 for r in rows if c in r.categories)
                         for c in PROTEIN_SOURCE_CATS}
    return {
        "n_dishes": n,
        "n_no_meat_named": sum(1 for r in rows if r.no_meat_named),
        "n_no_meat_no_legume_named": sum(1 for r in rows if r.no_meat_no_legume_named),
        "n_names_potato_or_starch": sum(1 for r in rows if r.names_potato_or_starch),
        "n_names_vegetable": sum(1 for r in rows if r.names_vegetable),
        "n_names_no_protein_source_at_all": sum(1 for r in rows
                                                if r.names_no_protein_source_at_all),
        "n_no_meat_no_legume_no_dairy_no_egg_no_nut": sum(
            1 for r in rows if r.no_meat_no_legume_named
            and not r.names_dairy and not r.names_egg and not r.names_nut_seed),
        "starch_dish_counts": starch_breakdown,
        "protein_source_dish_counts": protein_breakdown,
        "n_dishes_with_ambiguous_terms": sum(1 for r in rows if r.ambiguous_terms),
        "n_dishes_no_terms_matched": sum(1 for r in rows if not r.categories),
        "completeness": "text_only_unknown",
        "absence_is_not_evidence": True,
        "census_version": CENSUS_VERSION,
    }


def to_jsonl(rows: List[DishCensus], path: str) -> int:
    with open(path, "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(asdict(r), ensure_ascii=False) + "\n")
    return len(rows)
