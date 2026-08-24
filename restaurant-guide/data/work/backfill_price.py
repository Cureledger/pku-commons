"""Copy Michelin Price ($–$$$$) onto restaurant records. No invented tiers."""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
from registry import slugify  # noqa: E402

CSV_PATH = ROOT / "data" / "work" / "michelin_my_maps.csv"
TARGETS = [
    ROOT / "data" / "restaurants.json",
    ROOT / "copenhagen-working" / "restaurants.json",
    ROOT / "dublin-working" / "restaurants.json",
    ROOT / "orlando-working" / "restaurants.json",
]


def normalize_url(url: str) -> str:
    return url.strip().rstrip("/")


def compact(s: str) -> str:
    return slugify(s).replace("-", "")


def is_tier(value: str) -> bool:
    if not value or value.lower() == "none":
        return False
    return all(ch in "$€¥฿£" for ch in value)


def load_prices() -> tuple[dict[str, str], list[tuple[str, str, str]]]:
    by_url: dict[str, str] = {}
    rows: list[tuple[str, str, str]] = []
    with CSV_PATH.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            price = (row.get("Price") or "").strip()
            if not is_tier(price):
                continue
            url = normalize_url(row.get("Url") or "")
            name = (row.get("Name") or "").strip()
            if url:
                by_url[url] = price
            if name:
                rows.append((name, compact(name), price))
    return by_url, rows


def restaurant_urls(restaurant: dict) -> list[str]:
    urls = [normalize_url(c) for c in restaurant.get("provenance", {}).get("citations", [])]
    for award in restaurant.get("awards") or []:
        cite = normalize_url(award.get("citation") or "")
        if cite:
            urls.append(cite)
    return [u for u in urls if u]


def price_for(restaurant: dict, by_url: dict[str, str], rows: list[tuple[str, str, str]]) -> str | None:
    for url in restaurant_urls(restaurant):
        if url in by_url:
            return by_url[url]
    has_michelin = any(
        (award.get("program") or "") == "MICHELIN Guide"
        for award in restaurant.get("awards") or []
    )
    if not has_michelin:
        return None
    name = restaurant["name"].strip().casefold()
    exact = [price for csv_name, _key, price in rows if csv_name.casefold() == name]
    if len(set(exact)) == 1:
        return exact[0]
    keys = {compact(restaurant["slug"]), compact(restaurant["name"])}
    keys.update(compact(alias) for alias in restaurant.get("aliases") or [])
    hits = [
        price
        for _name, key, price in rows
        if key in keys or any(len(k) >= 5 and key.startswith(k) for k in keys)
    ]
    if len(set(hits)) == 1:
        return hits[0]
    return None


def backfill(path: Path, by_url: dict[str, str], rows: list[tuple[str, str, str]]) -> tuple[int, int]:
    payload = json.loads(path.read_text())
    restaurants = payload["restaurants"]
    filled = already = 0
    for restaurant in restaurants:
        if restaurant.get("price_tier"):
            already += 1
            continue
        price = price_for(restaurant, by_url, rows)
        if price:
            restaurant["price_tier"] = price
            filled += 1
    path.write_text(json.dumps(payload, indent=1, ensure_ascii=False) + "\n")
    return filled, already


def main() -> None:
    if not CSV_PATH.exists():
        sys.exit(f"missing {CSV_PATH}")
    by_url, rows = load_prices()
    for path in TARGETS:
        if not path.exists():
            continue
        filled, already = backfill(path, by_url, rows)
        print(f"{path.relative_to(ROOT)}: +{filled} already {already}")


if __name__ == "__main__":
    main()
