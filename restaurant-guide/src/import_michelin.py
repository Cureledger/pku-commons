"""Import Michelin restaurants for Phebe map cities from the public dataset.

Source: https://github.com/ngshiheng/michelin-my-maps (MIT)
Citation per row is the restaurant's guide.michelin.com URL.

Does not scrape guide.michelin.com. Does not invent menus or accommodation.
"""
from __future__ import annotations

import csv
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from registry import REGISTRY, add, load, make_record, save

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEST = os.path.join(ROOT, "data", "work", "destinations.json")
CSV_PATH = os.path.join(ROOT, "data", "work", "michelin_my_maps.csv")
CITATION_DATASET = "https://github.com/ngshiheng/michelin-my-maps"

TIER = {
    "3 Stars": "Three Stars",
    "2 Stars": "Two Stars",
    "1 Star": "One Star",
    "Bib Gourmand": "Bib Gourmand",
    "Selected Restaurants": "Selected",
}


def city_id_for(dest: dict) -> str:
    parts = [dest["id"]]
    if dest.get("region"):
        parts.append(dest["region"])
    parts.append(dest["country"])
    return "-".join(parts)


def index_destinations(dests: list[dict]) -> dict[str, dict]:
    by_location: dict[str, dict] = {}
    for dest in dests:
        for loc in dest.get("locations", []):
            by_location[loc] = dest
    return by_location


def main() -> int:
    dests = json.loads(open(DEST, encoding="utf-8").read())
    by_location = index_destinations(dests)
    if not os.path.exists(CSV_PATH):
        sys.exit(f"missing {CSV_PATH}")

    reg = load(REGISTRY)
    tally = {"added": 0, "merged": 0, "duplicate": 0, "skipped": 0}
    per_city: dict[str, int] = {}

    with open(CSV_PATH, encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            dest = by_location.get(row["Location"])
            if not dest:
                tally["skipped"] += 1
                continue
            name = (row.get("Name") or "").strip()
            if not name:
                tally["skipped"] += 1
                continue
            tier = TIER.get((row.get("Award") or "").strip())
            if not tier:
                tally["skipped"] += 1
                continue
            cid = city_id_for(dest)
            url = (row.get("Url") or "").strip()
            website = (row.get("WebsiteUrl") or "").strip()
            address = (row.get("Address") or "").strip()
            cuisine = (row.get("Cuisine") or "").strip()
            citations = [c for c in (url, CITATION_DATASET) if c]
            rec = make_record(
                name=name,
                city=dest["name"],
                region=dest.get("region", ""),
                country=dest["country"],
                website=website,
                address=address,
                source="award",
                added_by="nina",
                citation=citations[0] if citations else CITATION_DATASET,
            )
            rec["city_id"] = cid
            rec["restaurant_id"] = f"{cid}/{rec['slug']}"
            rec["awards"] = [
                {
                    "program": "MICHELIN Guide",
                    "tier": tier,
                    "citation": url or CITATION_DATASET,
                }
            ]
            if str(row.get("GreenStar") or "") in {"1", "true", "True"}:
                rec["awards"].append(
                    {
                        "program": "MICHELIN Guide",
                        "tier": "Green Star",
                        "citation": url or CITATION_DATASET,
                    }
                )
            if cuisine:
                rec["cuisine"] = cuisine
            price = (row.get("Price") or "").strip()
            if price and price.lower() != "none" and all(ch in "$€¥฿£" for ch in price):
                rec["price_tier"] = price
            for extra in citations[1:]:
                rec["provenance"]["citations"].append(extra)
            result = add(reg, rec)
            tally[result] += 1
            per_city[dest["id"]] = per_city.get(dest["id"], 0) + 1

    save(reg, REGISTRY)
    print(
        f"{tally['added']} added, {tally['merged']} merged, "
        f"{tally['skipped']} skipped, {len(reg['restaurants'])} in registry"
    )
    for slug, n in sorted(per_city.items(), key=lambda kv: (-kv[1], kv[0])):
        print(f"  {n:4} {slug}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
