"""Stash kitchens whose posted menu has no PKU-friendly main or plate.

A PKU family cannot use a meat-only board. Those records leave the live
list and go in {city}-working/restaurants.json.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

GUIDE = Path(__file__).resolve().parents[2]
DATA = GUIDE / "data"
DEST = DATA / "work" / "destinations.json"
PKU = DATA / "pku.json"


def city_id_for(dest: dict) -> str:
    parts = [dest["id"]]
    if dest.get("region"):
        parts.append(dest["region"])
    parts.append(dest["country"])
    return "-".join(parts)


def folder_for(dest: dict) -> Path:
    return GUIDE / f"{dest['id']}-working"


def main(slugs: list[str]) -> None:
    if not slugs:
        sys.exit("pass slugs to stash")
    want = set(slugs)
    dests = {city_id_for(d): d for d in json.loads(DEST.read_text())}
    reg = json.loads((DATA / "restaurants.json").read_text())
    keep: list = []
    by_city: dict[str, list] = {}
    for restaurant in reg["restaurants"]:
        if restaurant["slug"] in want:
            by_city.setdefault(restaurant["city_id"], []).append(restaurant)
        else:
            keep.append(restaurant)

    for cid, stashed in sorted(by_city.items()):
        dest = dests.get(cid)
        folder = folder_for(dest) if dest else GUIDE / f"{cid}-working"
        folder.mkdir(parents=True, exist_ok=True)
        existing: list = []
        prior = folder / "restaurants.json"
        if prior.exists():
            existing = json.loads(prior.read_text()).get("restaurants") or []
        have = {r["slug"] for r in existing}
        merged = existing + [r for r in stashed if r["slug"] not in have]
        prior.write_text(
            json.dumps(
                {
                    "schema_version": "working-v1",
                    "note": "Posted menu has no PKU-friendly main or plate. Not shown.",
                    "city_id": cid,
                    "restaurant_count": len(merged),
                    "restaurants": merged,
                },
                indent=1,
                ensure_ascii=False,
            )
            + "\n"
        )
        print(f"stashed {len(stashed):3} {cid} -> {folder.name}")

    reg["restaurants"] = keep
    (DATA / "restaurants.json").write_text(
        json.dumps(reg, indent=1, ensure_ascii=False) + "\n"
    )
    if PKU.exists():
        pku = json.loads(PKU.read_text())
        pku["restaurants"] = [r for r in pku["restaurants"] if r["slug"] not in want]
        PKU.write_text(json.dumps(pku, indent=2, ensure_ascii=False) + "\n")
    print(f"{len(keep)} remain live")


if __name__ == "__main__":
    main(sys.argv[1:])
