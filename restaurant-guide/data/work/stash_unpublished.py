"""Stash kitchens with no posted menu for Copenhagen, Dublin, and Orlando."""
from __future__ import annotations

import json
from pathlib import Path

GUIDE = Path(__file__).resolve().parents[2]
DATA = GUIDE / "data"

CITIES = {
    "copenhagen-dk": GUIDE / "copenhagen-working",
    "dublin-ie": GUIDE / "dublin-working",
    "orlando-fl-us": GUIDE / "orlando-working",
}


def main() -> None:
    reg = json.loads((DATA / "restaurants.json").read_text())
    keep, by_city = [], {cid: [] for cid in CITIES}
    for restaurant in reg["restaurants"]:
        cid = restaurant["city_id"]
        if cid in CITIES and not restaurant.get("menu_urls"):
            by_city[cid].append(restaurant)
        else:
            keep.append(restaurant)

    for cid, dest in CITIES.items():
        dest.mkdir(parents=True, exist_ok=True)
        stashed = by_city[cid]
        (dest / "restaurants.json").write_text(
            json.dumps(
                {
                    "schema_version": "working-v1",
                    "note": "No posted menu. Not shown. A PKU family needs the menu in advance.",
                    "city_id": cid,
                    "restaurant_count": len(stashed),
                    "restaurants": stashed,
                },
                indent=1,
                ensure_ascii=False,
            )
            + "\n"
        )
        print(f"{cid}: live {sum(1 for r in keep if r['city_id']==cid)}  stash {len(stashed)}")

    reg["restaurants"] = keep
    reg["restaurant_count"] = len(keep)
    (DATA / "restaurants.json").write_text(
        json.dumps(reg, indent=1, ensure_ascii=False) + "\n"
    )
    print(f"registry {len(keep)}")


if __name__ == "__main__":
    main()
