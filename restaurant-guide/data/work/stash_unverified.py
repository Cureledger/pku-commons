"""Move restaurants without a verified menu into asheville-working."""
from __future__ import annotations

import json
from pathlib import Path

GUIDE = Path(__file__).resolve().parents[2]
DATA = GUIDE / "data"
STASH = GUIDE.parent / "asheville-working"


def main():
    pku = json.loads((DATA / "pku.json").read_text())
    reg = json.loads((DATA / "restaurants.json").read_text())

    verified_pku_slugs = {
        r["slug"] for r in pku["restaurants"] if r.get("picks")
    }
    verified_reg_slugs = set()
    for r in reg["restaurants"]:
        keys = {r["slug"], *(r.get("aliases") or [])}
        if keys & verified_pku_slugs:
            verified_reg_slugs.add(r["slug"])

    keep_reg, stash_reg = [], []
    for r in reg["restaurants"]:
        (keep_reg if r["slug"] in verified_reg_slugs else stash_reg).append(r)

    keep_pku, stash_pku = [], []
    for r in pku["restaurants"]:
        (keep_pku if r.get("picks") else stash_pku).append(r)

    STASH.mkdir(parents=True, exist_ok=True)
    (STASH / "restaurants.json").write_text(
        json.dumps(
            {
                "schema_version": "asheville-working-v1",
                "note": "Restaurants with no verified posted menu. Not shown in the app.",
                "restaurant_count": len(stash_reg),
                "restaurants": stash_reg,
            },
            indent=1,
            ensure_ascii=False,
        )
        + "\n"
    )
    (STASH / "pku.json").write_text(
        json.dumps(
            {
                "version": "working",
                "note": "Empty pick lists. No posted menu was verified.",
                "restaurants": stash_pku,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n"
    )

    reg["restaurants"] = keep_reg
    reg["restaurant_count"] = len(keep_reg)
    (DATA / "restaurants.json").write_text(
        json.dumps(reg, indent=1, ensure_ascii=False) + "\n"
    )
    pku["restaurants"] = keep_pku
    (DATA / "pku.json").write_text(
        json.dumps(pku, indent=2, ensure_ascii=False) + "\n"
    )
    print(f"live registry {len(keep_reg)}  stash {len(stash_reg)}")
    print(f"live pku {len(keep_pku)}  stash {len(stash_pku)}")


if __name__ == "__main__":
    main()
