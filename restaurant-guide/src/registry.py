"""Open restaurant registry. Anyone can be added; awards are optional metadata.

The Michelin 15 was a way to bound a starting list, not a membership rule.
A restaurant is in the registry because someone added it and said where it
came from. That is the only gate.

Standard library only, Python 3.8+.
"""
from __future__ import annotations
import json, os, re, unicodedata, datetime
from typing import Dict, List, Optional

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTRY = os.path.join(ROOT, "data", "restaurants.json")
SCHEMA_VERSION = "registry-v1"

# How a record got here. Not a quality ranking -- a provenance label.
SOURCES = ("award", "local_list", "community", "self_submitted",
           "association", "operator_import", "visit")


def slugify(name: str) -> str:
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    s = re.sub(r"[''`]", "", s.lower())
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return re.sub(r"-+", "-", s)


def city_id(city: str, region: str = "", country: str = "us") -> str:
    parts = [slugify(city)]
    if region:
        parts.append(slugify(region))
    parts.append(slugify(country))
    return "-".join(parts)


def _now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat()


def load(path: str = REGISTRY) -> Dict:
    if not os.path.exists(path):
        return {"schema_version": SCHEMA_VERSION, "restaurants": [],
                "note": ("Open registry. Membership requires only that someone added the "
                         "record and recorded where it came from. Awards are optional "
                         "metadata, never a gate. No suitability score lives here.")}
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def save(reg: Dict, path: str = REGISTRY) -> None:
    reg["restaurant_count"] = len(reg["restaurants"])
    reg["updated_utc"] = _now()
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(reg, fh, indent=1, ensure_ascii=False)


def find_exact(reg: Dict, rid: str) -> Optional[Dict]:
    """Exact restaurant_id match only. Used by add(), because resolving an
    alias there would silently merge two genuinely different restaurants --
    'Curate' and 'La Bodega by Curate' are not the same kitchen."""
    return next((r for r in reg["restaurants"] if r["restaurant_id"] == rid), None)


def find(reg: Dict, rid: str) -> Optional[Dict]:
    """Look up by restaurant_id, then by any alias it has been known by.
    For reads and menu resolution -- never for deciding whether to insert."""
    hit = find_exact(reg, rid)
    if hit is not None:
        return hit
    slug = rid.rsplit("/", 1)[-1]
    return next((r for r in reg["restaurants"]
                 if slug in r.get("aliases", [])
                 or rid in [f"{r['city_id']}/{a}" for a in r.get("aliases", [])]), None)


def add_alias(reg: Dict, rid: str, alias: str) -> bool:
    """Record a prior slug. Returns False if the alias would collide with a
    different restaurant's live slug."""
    rec = find(reg, rid)
    if rec is None:
        raise KeyError(rid)
    clash = next((r for r in reg["restaurants"]
                  if r["slug"] == alias and r["restaurant_id"] != rec["restaurant_id"]), None)
    if clash is not None:
        return False
    rec.setdefault("aliases", [])
    if alias not in rec["aliases"] and alias != rec["slug"]:
        rec["aliases"].append(alias)
    return True


def make_record(name: str, city: str, region: str = "", country: str = "us",
                website: str = "", source: str = "community",
                added_by: str = "unknown", citation: str = "",
                award: Optional[Dict] = None, address: str = "",
                menu_urls: Optional[List[str]] = None,
                reservation_platform: str = "", notes: str = "",
                harvest_categories: Optional[List[str]] = None) -> Dict:
    if source not in SOURCES:
        raise ValueError(f"source must be one of {SOURCES}, got {source!r}")
    if not name.strip():
        raise ValueError("name is required")
    cid = city_id(city, region, country)
    slug = slugify(name)
    return {
        "restaurant_id": f"{cid}/{slug}",
        "city_id": cid, "slug": slug, "name": name.strip(),
        "website": website, "address": address,
        "menu_urls": menu_urls or [],
        "reservation_platform": reservation_platform,
        # Awards are a LIST of optional decorations. Empty is normal and fine.
        "awards": [award] if award else [],
        "provenance": {"source": source, "added_by": added_by,
                       "added_utc": _now(),
                       "citations": [citation] if citation else []},
        "census": {"status": "no_menu_captured"},
        "accommodation": {"status": "unverified",
                          "note": "'unverified' is not zero. Set only by direct contact."},
        "signals": {},
        # Prior slugs this restaurant has been known by. A rename must never
        # orphan captured menus filed under the old id.
        "aliases": [],
        # Which local-list category this restaurant was found under. A tag,
        # not a rating -- "Best Tapas" says the FORMAT is compose-your-own,
        # which is a structural fact, not a claim about the food.
        "harvest_categories": harvest_categories or [],
        "notes": notes,
    }


def add(reg: Dict, rec: Dict, merge: bool = True) -> str:
    """Add a record. Returns 'added', 'merged', or 'duplicate'."""
    existing = find_exact(reg, rec["restaurant_id"])
    if existing is None:
        reg["restaurants"].append(rec)
        return "added"
    if not merge:
        return "duplicate"
    # Same restaurant reached by a second route: keep both awards and both
    # citations rather than letting one source overwrite the other.
    for a in rec["awards"]:
        if a not in existing["awards"]:
            existing["awards"].append(a)
    for c in rec["provenance"]["citations"]:
        if c not in existing["provenance"]["citations"]:
            existing["provenance"]["citations"].append(c)
    existing["provenance"].setdefault("also_found_via", [])
    src = rec["provenance"]["source"]
    if src != existing["provenance"]["source"] and src not in existing["provenance"]["also_found_via"]:
        existing["provenance"]["also_found_via"].append(src)
    for k in ("website", "address", "reservation_platform"):
        if not existing.get(k) and rec.get(k):
            existing[k] = rec[k]
    for u in rec["menu_urls"]:
        if u not in existing["menu_urls"]:
            existing["menu_urls"].append(u)
    existing.setdefault("aliases", [])
    for al in rec.get("aliases", []):
        if al not in existing["aliases"] and al != existing["slug"]:
            existing["aliases"].append(al)
    existing.setdefault("harvest_categories", [])
    for c in rec.get("harvest_categories", []):
        if c not in existing["harvest_categories"]:
            existing["harvest_categories"].append(c)
    return "merged"
