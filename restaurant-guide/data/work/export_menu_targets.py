"""Write per-city menu-target lists for remaining Michelin kitchens."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REG = ROOT / "data" / "restaurants.json"
DEST = ROOT / "data" / "work" / "destinations.json"
OUT = ROOT / "data" / "work" / "menu-targets"
DONE = {"asheville-nc-us", "copenhagen-dk", "dublin-ie", "orlando-fl-us"}


def city_id_for(dest: dict) -> str:
    parts = [dest["id"]]
    if dest.get("region"):
        parts.append(dest["region"])
    parts.append(dest["country"])
    return "-".join(parts)


def main() -> None:
    dests = json.loads(DEST.read_text())
    id_by_cid = {city_id_for(d): d["id"] for d in dests}
    reg = json.loads(REG.read_text())
    by: dict[str, list] = {}
    for restaurant in reg["restaurants"]:
        cid = restaurant["city_id"]
        if cid in DONE:
            continue
        slug = id_by_cid.get(cid)
        if not slug:
            continue
        by.setdefault(slug, []).append(
            {
                "name": restaurant["name"],
                "slug": restaurant["slug"],
                "city_id": cid,
                "website": restaurant.get("website") or "",
                "menu_urls": restaurant.get("menu_urls") or [],
                "awards": [a.get("tier") for a in restaurant.get("awards") or []],
                "address": restaurant.get("address") or "",
                "price_tier": restaurant.get("price_tier") or "",
            }
        )
    OUT.mkdir(parents=True, exist_ok=True)
    for slug, rows in sorted(by.items()):
        (OUT / f"{slug}.json").write_text(
            json.dumps(rows, indent=2, ensure_ascii=False) + "\n"
        )
        print(f"{slug:20} {len(rows)}")


if __name__ == "__main__":
    main()
