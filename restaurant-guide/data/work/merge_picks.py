"""Merge agent pick files into data/pku.json and attach menu_urls."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PKU = ROOT / "data" / "pku.json"
REG = ROOT / "data" / "restaurants.json"
PICKS_DIR = ROOT / "data" / "work" / "picks"


def main(paths: list[str]) -> None:
    files = [Path(p) for p in paths] if paths else sorted(PICKS_DIR.glob("*.json"))
    if not files:
        sys.exit("no pick files")
    pku = json.loads(PKU.read_text())
    by_slug = {r["slug"]: r for r in pku["restaurants"]}
    reg = json.loads(REG.read_text())
    added = 0
    for path in files:
        payload = json.loads(path.read_text())
        rows = payload if isinstance(payload, list) else payload.get("restaurants", [])
        for row in rows:
            slug = row["slug"]
            picks = row.get("picks") or []
            if not picks:
                continue
            entry = by_slug.get(slug) or {"slug": slug, "picks": []}
            have = {(p["name"], p.get("description", "")) for p in entry["picks"]}
            for pick in picks:
                key = (pick["name"], pick.get("description", ""))
                if key not in have:
                    entry["picks"].append(pick)
                    have.add(key)
            by_slug[slug] = entry
            added += 1
            menu_url = row.get("menu_url")
            if menu_url:
                for restaurant in reg["restaurants"]:
                    if restaurant["slug"] == slug:
                        restaurant.setdefault("menu_urls", [])
                        if menu_url not in restaurant["menu_urls"]:
                            restaurant["menu_urls"].append(menu_url)
                        break
    pku["restaurants"] = list(by_slug.values())
    PKU.write_text(json.dumps(pku, indent=2, ensure_ascii=False) + "\n")
    REG.write_text(json.dumps(reg, indent=1, ensure_ascii=False) + "\n")
    print(f"merged {added} kitchens with picks, {len(pku['restaurants'])} pku rows")


if __name__ == "__main__":
    main(sys.argv[1:])
