"""Attach one national pick list to every city location of a US chain.

Restaurant records get restaurant["chain"] = chain_id.
pku.json keeps ONE row per chain_id. Per-city copies are removed.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REG = ROOT / "data" / "restaurants.json"
PKU = ROOT / "data" / "pku.json"
CHAINS = ROOT / "data" / "work" / "chain-picks.json"


def main() -> None:
    catalog = json.loads(CHAINS.read_text())
    by_id = {c["id"]: c for c in catalog["chains"]}
    reg = json.loads(REG.read_text())
    tagged = 0
    for restaurant in reg["restaurants"]:
        notes = restaurant.get("notes") or ""
        if not notes.startswith("US sit-down chain"):
            continue
        slug = restaurant["slug"]
        for chain_id in by_id:
            if slug == chain_id or slug.startswith(f"{chain_id}-"):
                restaurant["chain"] = chain_id
                tagged += 1
                break
    REG.write_text(json.dumps(reg, indent=1, ensure_ascii=False) + "\n")

    pku = json.loads(PKU.read_text())
    per_city_prefixes = tuple(f"{chain_id}-" for chain_id in by_id)
    kept = [
        row
        for row in pku["restaurants"]
        if not (row["slug"] in by_id or row["slug"].startswith(per_city_prefixes))
    ]
    for chain in catalog["chains"]:
        if chain.get("verdict") == "blocked":
            continue
        picks = chain.get("picks") or []
        if not picks:
            continue
        kept.append({"slug": chain["id"], "picks": picks})
    pku["restaurants"] = kept
    PKU.write_text(json.dumps(pku, indent=2, ensure_ascii=False) + "\n")

    with_picks = sum(1 for c in catalog["chains"] if c.get("picks"))
    blocked = [c["id"] for c in catalog["chains"] if c.get("verdict") == "blocked"]
    empty = [
        c["id"]
        for c in catalog["chains"]
        if c.get("verdict") == "no_pku" or (not c.get("picks") and c.get("verdict") != "blocked")
    ]
    print(f"tagged {tagged} locations, {with_picks} chain pick lists")
    if blocked:
        print("blocked:", ", ".join(blocked))
    if empty:
        print("no_pku:", ", ".join(empty))


if __name__ == "__main__":
    main()
