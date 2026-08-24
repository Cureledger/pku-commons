"""Apply NYC menu-pass results: keep kitchens with picks, stash the rest."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
RESULTS = DATA / "work" / "picks" / "nyc-results"
PKU = DATA / "pku.json"
REG = DATA / "restaurants.json"
DEST = DATA / "work" / "destinations.json"
NOTE = "Not appropriate for now: posted menu has no PKU-friendly main or plate, or the dish list would not load."


def city_id_for(dest: dict) -> str:
    parts = [dest["id"]]
    if dest.get("region"):
        parts.append(dest["region"])
    parts.append(dest["country"])
    return "-".join(parts)


def main() -> None:
    files = sorted(RESULTS.glob("batch*.json"))
    if not files:
        raise SystemExit("no nyc-results/batch*.json")
    results = []
    for path in files:
        payload = json.loads(path.read_text())
        rows = payload if isinstance(payload, list) else payload.get("results") or payload.get("restaurants") or []
        results.extend(rows)

    keep_picks = [r for r in results if r.get("verdict") == "picks" and r.get("picks")]
    stash_slugs = [
        r["slug"]
        for r in results
        if r.get("verdict") in {"no_pku", "blocked"} or not r.get("picks")
    ]
    # A picks verdict with empty picks still stashes.
    stash_slugs = sorted(set(stash_slugs) - {r["slug"] for r in keep_picks})

    pku = json.loads(PKU.read_text())
    by_slug = {r["slug"]: r for r in pku["restaurants"]}
    reg = json.loads(REG.read_text())
    for row in keep_picks:
        slug = row["slug"]
        entry = by_slug.get(slug) or {"slug": slug, "picks": []}
        have = {(p["name"], p.get("description", "")) for p in entry["picks"]}
        for pick in row["picks"]:
            key = (pick["name"], pick.get("description", ""))
            if key not in have:
                entry["picks"].append(pick)
                have.add(key)
        by_slug[slug] = entry
        menu_url = row.get("menu_url")
        if menu_url:
            for restaurant in reg["restaurants"]:
                if restaurant["slug"] == slug and restaurant["city_id"] == "new-york-ny-us":
                    restaurant.setdefault("menu_urls", [])
                    if menu_url not in restaurant["menu_urls"]:
                        restaurant["menu_urls"].append(menu_url)
                    break
    pku["restaurants"] = list(by_slug.values())
    PKU.write_text(json.dumps(pku, indent=2, ensure_ascii=False) + "\n")

    dests = {city_id_for(d): d for d in json.loads(DEST.read_text())}
    want = set(stash_slugs)
    keep_reg = []
    by_city: dict[str, list] = {}
    for restaurant in reg["restaurants"]:
        if restaurant["city_id"] == "new-york-ny-us" and restaurant["slug"] in want:
            by_city.setdefault(restaurant["city_id"], []).append(restaurant)
        else:
            keep_reg.append(restaurant)
    for cid, stashed in sorted(by_city.items()):
        dest = dests.get(cid)
        folder = ROOT / f"{dest['id']}-working" if dest else ROOT / f"{cid}-working"
        folder.mkdir(parents=True, exist_ok=True)
        prior = folder / "restaurants.json"
        existing = []
        old_note = NOTE
        if prior.exists():
            payload = json.loads(prior.read_text())
            existing = payload.get("restaurants") or []
            old_note = payload.get("note") or NOTE
            if "Not appropriate" not in old_note:
                old_note = old_note.rstrip(".") + ". " + NOTE
        have = {r["slug"] for r in existing}
        merged = existing + [r for r in stashed if r["slug"] not in have]
        prior.write_text(
            json.dumps(
                {
                    "schema_version": "working-v1",
                    "note": old_note,
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
    reg["restaurants"] = keep_reg
    REG.write_text(json.dumps(reg, indent=1, ensure_ascii=False) + "\n")

    counts = {}
    for row in results:
        counts[row.get("verdict") or "unknown"] = counts.get(row.get("verdict") or "unknown", 0) + 1
    print(f"results {len(results)} {counts}")
    print(f"kept with picks {len(keep_picks)}, stashed {len(stash_slugs)}, live {len(keep_reg)}")
    blocked = [r for r in results if r.get("verdict") == "blocked"]
    if blocked:
        print("blocked:")
        for row in blocked:
            print(f"  {row['slug']}: {row.get('reason') or row.get('menu_url') or ''}")


if __name__ == "__main__":
    main()
