"""Attach menu_urls found by find_menus.py onto the live registry."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REG = ROOT / "data" / "restaurants.json"
RESULTS = ROOT / "data" / "work" / "menu-find" / "results.jsonl"


def main() -> None:
    found = {}
    for line in RESULTS.read_text().splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if row.get("menu_url"):
            found[row["slug"]] = row["menu_url"]
    reg = json.loads(REG.read_text())
    attached = 0
    for restaurant in reg["restaurants"]:
        url = found.get(restaurant["slug"])
        if not url:
            continue
        restaurant.setdefault("menu_urls", [])
        if url not in restaurant["menu_urls"]:
            restaurant["menu_urls"].append(url)
            attached += 1
    REG.write_text(json.dumps(reg, indent=1, ensure_ascii=False) + "\n")
    print(f"attached {attached} menu urls, {len(found)} found rows")


if __name__ == "__main__":
    main()
