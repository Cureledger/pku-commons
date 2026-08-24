"""Load the 2026 Copenhagen Michelin seed into the open registry."""
from __future__ import annotations
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from registry import REGISTRY, add, load, make_record, save

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEED = os.path.join(ROOT, "data", "copenhagen_michelin_2026.json")


def main() -> int:
    seed = json.loads(open(SEED, encoding="utf-8").read())
    edition = seed["edition"]
    year = seed["year"]
    citation = seed["citation"]
    program = seed["program"]

    reg = load(REGISTRY)
    tally = {"added": 0, "merged": 0, "duplicate": 0}
    for row in seed["restaurants"]:
        awards = [
            {
                "program": program,
                "tier": row["tier"],
                "edition": edition,
                "year": year,
                "citation": citation,
            }
        ]
        if row.get("green_star"):
            awards.append(
                {
                    "program": program,
                    "tier": "Green Star",
                    "edition": edition,
                    "year": year,
                    "citation": citation,
                }
            )
        rec = make_record(
            name=row["name"],
            city="Copenhagen",
            country="dk",
            website=row.get("website", ""),
            address=row.get("address", ""),
            source="award",
            added_by="nina",
            citation=citation,
        )
        rec["awards"] = awards
        if row.get("blurb"):
            rec["blurb"] = row["blurb"]
        tally[add(reg, rec)] += 1

    save(reg, REGISTRY)
    print(
        f"{tally['added']} added, {tally['merged']} merged, "
        f"{len(reg['restaurants'])} in registry"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
