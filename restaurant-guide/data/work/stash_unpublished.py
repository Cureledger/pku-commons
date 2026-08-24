"""Stash kitchens with no posted menu. A PKU family needs the menu in advance."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

GUIDE = Path(__file__).resolve().parents[2]
DATA = GUIDE / "data"
DEST = DATA / "work" / "destinations.json"
KEEP_LIVE = {"asheville-nc-us", "copenhagen-dk", "dublin-ie", "orlando-fl-us"}


def city_id_for(dest: dict) -> str:
    parts = [dest["id"]]
    if dest.get("region"):
        parts.append(dest["region"])
    parts.append(dest["country"])
    return "-".join(parts)


def folder_for(dest: dict) -> Path:
    return GUIDE / f"{dest['id']}-working"


def should_stash(restaurant: dict, mode: str) -> bool:
    if restaurant.get("menu_urls"):
        return False
    website = (restaurant.get("website") or "").strip()
    if mode == "no-website":
        return not website
    return True


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--mode",
        choices=("no-website", "no-menu"),
        default="no-menu",
        help="no-website: stash only kitchens with no site. no-menu: stash any kitchen without menu_urls.",
    )
    args = ap.parse_args()
    dests = {city_id_for(d): d for d in json.loads(DEST.read_text())}
    reg = json.loads((DATA / "restaurants.json").read_text())
    keep: list = []
    by_city: dict[str, list] = {}
    for restaurant in reg["restaurants"]:
        cid = restaurant["city_id"]
        if cid in KEEP_LIVE or cid not in dests:
            keep.append(restaurant)
            continue
        if should_stash(restaurant, args.mode):
            by_city.setdefault(cid, []).append(restaurant)
        else:
            keep.append(restaurant)

    for cid, stashed in sorted(by_city.items()):
        dest = dests[cid]
        folder = folder_for(dest)
        folder.mkdir(parents=True, exist_ok=True)
        existing: list = []
        prior = folder / "restaurants.json"
        if prior.exists():
            existing = json.loads(prior.read_text()).get("restaurants") or []
        have = {r["slug"] for r in existing}
        merged = existing + [r for r in stashed if r["slug"] not in have]
        (folder / "restaurants.json").write_text(
            json.dumps(
                {
                    "schema_version": "working-v1",
                    "note": "No posted menu. Not shown. A PKU family needs the menu in advance.",
                    "city_id": cid,
                    "restaurant_count": len(merged),
                    "restaurants": merged,
                },
                indent=1,
                ensure_ascii=False,
            )
            + "\n"
        )
        live_n = sum(1 for r in keep if r["city_id"] == cid)
        print(f"{cid}: live {live_n}  stash +{len(stashed)} total {len(merged)}")

    reg["restaurants"] = keep
    reg["restaurant_count"] = len(keep)
    (DATA / "restaurants.json").write_text(
        json.dumps(reg, indent=1, ensure_ascii=False) + "\n"
    )
    print(f"registry {len(keep)}")


if __name__ == "__main__":
    main()
