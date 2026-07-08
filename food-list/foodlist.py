"""PKU Commons — the single source of truth for the living food list.

Both the estimator (phe-per-100g whole-food lookup) and the benchmark (ground-truth
provenance) import THIS module, so there is one place a food row is defined, cited, and
versioned. Dependency-free (standard library only).

The canonical data file is ``food-list/foods.json`` (schema: ``food-list/foods.schema.json``).
Every row is a Layer-1 (legal-style review) artifact and MUST carry a citation to authority,
a version, and a reviewer of record — see ``docs/PEER-REVIEW.md``. ``validate()`` enforces
that; CI can call it to reject an uncited row.

Typical use:

    from foodlist import load, lookup_phe_100g
    fl = load()
    phe = lookup_phe_100g("banana", fl)        # -> 49.0  (mg phe per 100 g)
"""
import json, os, re

_HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_PATH = os.path.join(_HERE, "foods.json")

# Layer-1 fields every row must carry (docs/PEER-REVIEW.md).
REQUIRED_ROW_FIELDS = ("key", "description", "phe_mg_per_100g", "citation", "version",
                       "reviewer_of_record")
VALID_AUTHORITIES = ("USDA_FDC", "OpenFoodFacts", "clinician_signoff")


class FoodList:
    """Loaded food list with lookup helpers. Keeps the raw rows and derived indexes."""

    def __init__(self, doc):
        self.meta = doc.get("_meta", {})
        self.rows = doc.get("foods", [])
        # exact-key index
        self._by_key = {r["key"].lower(): r for r in self.rows}
        # stem index for fuzzy ingredient matching: first word of the key, singularized
        self._by_stem = {}
        for r in self.rows:
            stem = re.split(r"[ _]", r["key"])[0].lower().rstrip("s")
            self._by_stem.setdefault(stem, r)

    def __len__(self):
        return len(self.rows)

    def get(self, key):
        """Exact (case-insensitive) key lookup; None if absent."""
        return self._by_key.get((key or "").lower())

    def match(self, ingredient_name):
        """Fuzzy lookup by ingredient name: return the row whose key-stem the name contains.

        Mirrors the estimator's historical behavior (6-char stem prefix match) so the
        food-list refactor is numerically identical to the previous ad-hoc lookup.
        """
        n = (ingredient_name or "").lower()
        for stem, row in self._by_stem.items():
            if stem and stem[:6] in n:
                return row
        return None

    def phe_100g(self, ingredient_name):
        """phe mg per 100 g for an ingredient name, or None if not in the list."""
        row = self.match(ingredient_name)
        return None if row is None else row.get("phe_mg_per_100g")


def load(path=None):
    """Load the canonical food list. Returns a FoodList."""
    with open(path or DEFAULT_PATH) as fh:
        return FoodList(json.load(fh))


def lookup_phe_100g(ingredient_name, food_list=None):
    """Convenience: phe mg per 100 g for an ingredient name (loads default list if needed)."""
    fl = food_list or load()
    return fl.phe_100g(ingredient_name)


def validate(path=None):
    """Enforce the Layer-1 contract on every row. Returns (ok: bool, errors: list[str]).

    CI-callable: a row missing a citation / version / reviewer of record, or citing an
    unknown authority, is a Layer-1 violation and fails validation.
    """
    fl = load(path)
    errors = []
    seen_keys = set()
    for i, r in enumerate(fl.rows):
        tag = r.get("key", f"row[{i}]")
        for f in REQUIRED_ROW_FIELDS:
            if f not in r or r[f] in (None, "", {}):
                errors.append(f"{tag}: missing required field '{f}'")
        cit = r.get("citation", {})
        auth = cit.get("authority")
        if auth not in VALID_AUTHORITIES:
            errors.append(f"{tag}: citation.authority '{auth}' not in {VALID_AUTHORITIES}")
        else:
            # authority-specific evidence must be present
            if auth == "USDA_FDC" and not cit.get("fdcId"):
                errors.append(f"{tag}: USDA_FDC citation missing fdcId")
            if auth == "OpenFoodFacts" and not cit.get("off_code"):
                errors.append(f"{tag}: OpenFoodFacts citation missing off_code")
            if auth == "clinician_signoff" and not cit.get("signoff_by"):
                errors.append(f"{tag}: clinician_signoff citation missing signoff_by")
        if r.get("key") in seen_keys:
            errors.append(f"{tag}: duplicate key")
        seen_keys.add(r.get("key"))
    return (len(errors) == 0), errors


if __name__ == "__main__":
    import sys
    ok, errs = validate()
    fl = load()
    print(f"food list: {len(fl)} rows from {DEFAULT_PATH}")
    if ok:
        print("Layer-1 validation: PASS (every row carries citation + version + reviewer of record)")
    else:
        print(f"Layer-1 validation: FAIL ({len(errs)} problems)")
        for e in errs:
            print("  -", e)
        sys.exit(1)
