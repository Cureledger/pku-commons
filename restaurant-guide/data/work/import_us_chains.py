"""Add sit-down US national and regional chains with published menus.

Fast food is out of scope. One location per city. Slugs are city-unique
because /r/[slug] is global. Picks are copied from dishes on the operator's
posted menu; accommodation stays unset.

Official footprints:
- Cheesecake Factory: company location PDF (May 2025)
- True Food Kitchen: truefoodkitchen.com/menu location list
- North Italia: northitalia.com/locations
- Others: operator sites / well-known national sit-down footprints
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))
from registry import REGISTRY, add, load, make_record, save

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PKU = os.path.join(ROOT, "data", "pku.json")

# Destination id, display name, region. city_id becomes {id}-{region}-us.
US_CITIES = [
    ("asheville", "Asheville", "NC"),
    ("new-york", "New York", "NY"),
    ("chicago", "Chicago", "IL"),
    ("san-francisco", "San Francisco", "CA"),
    ("los-angeles", "Los Angeles", "CA"),
    ("washington", "Washington", "DC"),
    ("miami", "Miami", "FL"),
    ("atlanta", "Atlanta", "GA"),
    ("new-orleans", "New Orleans", "LA"),
    ("austin", "Austin", "TX"),
    ("houston", "Houston", "TX"),
    ("dallas", "Dallas", "TX"),
    ("san-antonio", "San Antonio", "TX"),
    ("denver", "Denver", "CO"),
    ("nashville", "Nashville", "TN"),
    ("charleston", "Charleston", "SC"),
    ("orlando", "Orlando", "FL"),
    ("san-diego", "San Diego", "CA"),
    ("boston", "Boston", "MA"),
    ("philadelphia", "Philadelphia", "PA"),
    ("phoenix", "Phoenix", "AZ"),
    ("tucson", "Tucson", "AZ"),
    ("seattle", "Seattle", "WA"),
    ("portland", "Portland", "OR"),
    ("las-vegas", "Las Vegas", "NV"),
    ("minneapolis", "Minneapolis", "MN"),
    ("detroit", "Detroit", "MI"),
    ("st-louis", "St. Louis", "MO"),
    ("kansas-city", "Kansas City", "MO"),
    ("charlotte", "Charlotte", "NC"),
    ("raleigh", "Raleigh", "NC"),
    ("tampa", "Tampa", "FL"),
    ("jacksonville", "Jacksonville", "FL"),
    ("pittsburgh", "Pittsburgh", "PA"),
    ("cleveland", "Cleveland", "OH"),
    ("cincinnati", "Cincinnati", "OH"),
    ("columbus", "Columbus", "OH"),
    ("indianapolis", "Indianapolis", "IN"),
    ("salt-lake-city", "Salt Lake City", "UT"),
    ("sacramento", "Sacramento", "CA"),
    ("baltimore", "Baltimore", "MD"),
    ("milwaukee", "Milwaukee", "WI"),
    ("memphis", "Memphis", "TN"),
    ("louisville", "Louisville", "KY"),
    ("richmond", "Richmond", "VA"),
    ("honolulu", "Honolulu", "HI"),
    ("oklahoma-city", "Oklahoma City", "OK"),
    ("albuquerque", "Albuquerque", "NM"),
]

ALL_US = [c[0] for c in US_CITIES]
WEST_COAST = {
    "san-francisco",
    "los-angeles",
    "san-diego",
    "sacramento",
    "seattle",
    "portland",
    "honolulu",
}

# Official Cheesecake Factory US metros that match this app's cities.
# Source: company-owned restaurants PDF, 13 May 2025.
CHEESECAKE = [
    "phoenix",
    "tucson",
    "los-angeles",
    "san-diego",
    "san-francisco",
    "sacramento",
    "denver",
    "washington",
    "miami",
    "jacksonville",
    "orlando",
    "tampa",
    "atlanta",
    "honolulu",
    "chicago",
    "indianapolis",
    "louisville",
    "new-orleans",
    "baltimore",
    "boston",
    "detroit",
    "minneapolis",
    "kansas-city",
    "st-louis",
    "las-vegas",
    "new-york",
    "charlotte",
    "raleigh",
    "cincinnati",
    "cleveland",
    "columbus",
    "oklahoma-city",
    "portland",
    "philadelphia",
    "pittsburgh",
    "nashville",
    "austin",
    "dallas",
    "houston",
    "san-antonio",
    "salt-lake-city",
    "richmond",
    "seattle",
    "milwaukee",
    "albuquerque",
]

# truefoodkitchen.com/menu — Select a Location
TRUE_FOOD = [
    "phoenix",
    "tucson",
    "los-angeles",
    "san-francisco",
    "san-diego",
    "denver",
    "jacksonville",
    "miami",
    "tampa",
    "atlanta",
    "chicago",
    "new-orleans",
    "baltimore",
    "washington",
    "kansas-city",
    "las-vegas",
    "new-york",
    "raleigh",
    "columbus",
    "philadelphia",
    "nashville",
    "austin",
    "dallas",
    "houston",
]

# northitalia.com/locations
NORTH_ITALIA = [
    "phoenix",
    "tucson",
    "los-angeles",
    "san-diego",
    "san-francisco",
    "denver",
    "washington",
    "miami",
    "orlando",
    "atlanta",
    "kansas-city",
    "las-vegas",
    "charlotte",
    "oklahoma-city",
    "philadelphia",
    "nashville",
    "austin",
    "dallas",
    "houston",
    "san-antonio",
    "salt-lake-city",
]

# Daytime café, posted menu. Strong in the South, Midwest, Texas, Arizona.
FIRST_WATCH = [
    c
    for c in ALL_US
    if c
    not in WEST_COAST
    | {"new-york", "boston", "las-vegas", "milwaukee"}
]

MAGGIANOS = [
    "chicago",
    "los-angeles",
    "washington",
    "atlanta",
    "houston",
    "dallas",
    "san-antonio",
    "denver",
    "boston",
    "philadelphia",
    "phoenix",
    "las-vegas",
    "minneapolis",
    "st-louis",
    "kansas-city",
    "indianapolis",
    "columbus",
    "tampa",
    "orlando",
    "nashville",
    "charlotte",
    "baltimore",
    "richmond",
    "new-york",
    "detroit",
    "seattle",
    "milwaukee",
]

YARD_HOUSE = [
    "orlando",
    "austin",
    "houston",
    "seattle",
    "boston",
    "san-antonio",
    "chicago",
    "kansas-city",
    "phoenix",
    "tucson",
    "los-angeles",
    "san-diego",
    "washington",
    "new-york",
    "las-vegas",
    "cincinnati",
    "raleigh",
    "indianapolis",
    "denver",
    "minneapolis",
    "detroit",
    "miami",
]

CAPITAL_GRILLE = [
    "phoenix",
    "los-angeles",
    "denver",
    "washington",
    "miami",
    "orlando",
    "tampa",
    "atlanta",
    "honolulu",
    "chicago",
    "indianapolis",
    "louisville",
    "baltimore",
    "boston",
    "detroit",
    "minneapolis",
    "kansas-city",
    "las-vegas",
    "new-york",
    "charlotte",
    "cleveland",
    "cincinnati",
    "columbus",
    "oklahoma-city",
    "philadelphia",
    "nashville",
    "austin",
    "dallas",
    "houston",
    "salt-lake-city",
    "seattle",
    "milwaukee",
]

RUTHS_CHRIS = [
    c
    for c in ALL_US
    if c not in {"asheville"}
]

COOPERS_HAWK = [
    "chicago",
    "indianapolis",
    "detroit",
    "kansas-city",
    "jacksonville",
    "baltimore",
    "washington",
    "orlando",
    "tampa",
    "atlanta",
    "nashville",
    "charlotte",
    "philadelphia",
    "pittsburgh",
    "cleveland",
    "cincinnati",
    "columbus",
    "minneapolis",
    "st-louis",
    "dallas",
    "houston",
    "austin",
    "denver",
    "louisville",
    "milwaukee",
]

CRACKER_BARREL = [
    c for c in ALL_US if c not in WEST_COAST | {"las-vegas", "albuquerque"}
]

SEASONS_52 = [
    "atlanta",
    "orlando",
    "tampa",
    "jacksonville",
    "chicago",
    "dallas",
    "houston",
    "denver",
    "washington",
    "boston",
    "philadelphia",
    "phoenix",
    "minneapolis",
    "detroit",
    "kansas-city",
    "charlotte",
    "indianapolis",
    "cincinnati",
    "columbus",
    "baltimore",
    "nashville",
    "austin",
]


def pick(name, description, course, kind, hold=None):
    row = {"name": name, "description": description, "course": course, "kind": kind}
    if hold:
        row["hold"] = hold
    return row


# Dishes taken from the operator pages fetched for this import.
# No accommodation flags.
PICKS = {
    "olive-garden": [
        pick(
            "Jumbo House Salad",
            "Our Famous Jumbo House Salad includes 12 Breadsticks",
            "starter",
            "potato_or_salad",
        ),
    ],
    "pf-changs": [
        pick("Buddha's Feast | Stir-Fried", "vegetable stir-fry", "main", "main"),
        pick("Spicy Eggplant", "posted entrée", "main", "main"),
        pick("Mongolian Tofu", "posted tofu entrée", "main", "main"),
        pick("Edamame", "posted appetizer", "starter", "beyond"),
        pick("Veggie Spring Rolls", "posted appetizer", "starter", "beyond"),
        pick("Crispy Green Beans", "posted appetizer", "starter", "beyond"),
        pick("Chili-Garlic Green Beans", "shareable side", "side", "beyond"),
        pick("Kung Pao Brussels Sprouts", "shareable side", "side", "beyond"),
        pick("Cold Cucumber Salad", "shareable side", "side", "beyond"),
        pick("House Salad", "soups & salads", "starter", "potato_or_salad"),
    ],
    "first-watch": [
        pick("Avocado Toast", "The Healthier Side", "main", "main"),
        pick("Market Veggie", "sandwich, served with greens or soup", "main", "main"),
        pick("Steel-Cut Oatmeal", "The Healthier Side", "main", "main"),
        pick("Kale & Berry Salad", "served with artisan ciabatta toast", "main", "potato_or_salad"),
        pick("Cup of Fresh, Seasonal Fruit", "side", "side", "beyond"),
        pick("Lemon-Dressed Organic Mixed Greens", "side", "side", "potato_or_salad"),
        pick("Fresh, Seasoned Potatoes", "side", "side", "potato_or_salad"),
        pick("Tomato Basil Soup", "cup or bowl", "starter", "beyond"),
    ],
    "texas-roadhouse": [
        pick(
            "Country Vegetable Plate",
            "Choose 4 side items (one salad only, please).",
            "main",
            "main",
        ),
        pick("Green Beans", "Sides & Extras", "side", "beyond"),
        pick("Steamed Vegetables", "Sides & Extras", "side", "beyond"),
        pick("Seasoned Corn", "Sides & Extras", "side", "beyond"),
        pick("Sauteed Mushrooms", "Sides & Extras", "side", "beyond"),
        pick("Sauteed Onions", "Sides & Extras", "side", "beyond"),
        pick("Applesauce", "Sides & Extras", "side", "beyond"),
        pick("House Salad", "fresh greens, cheddar cheese, tomato, eggs and croutons", "starter", "potato_or_salad", "cheddar, egg, croutons"),
        pick("Baked Potato", "Sides & Extras", "side", "potato_or_salad"),
        pick("Sweet Potato", "Sides & Extras", "side", "potato_or_salad"),
    ],
    "chilis": [
        pick("House-made Guacamole", "appetizer", "starter", "beyond"),
        pick("Chips & Salsa", "appetizer", "starter", "beyond"),
    ],
}

CHAINS = [
    {
        "id": "olive-garden",
        "name": "Olive Garden",
        "website": "https://www.olivegarden.com/",
        "menu_url": "https://www.olivegarden.com/menu",
        "cuisine": "Italian",
        "price_tier": "$$",
        "cities": ALL_US,
    },
    {
        "id": "applebees",
        "name": "Applebee's",
        "website": "https://www.applebees.com/",
        "menu_url": "https://www.applebees.com/en/menu",
        "cuisine": "American",
        "price_tier": "$$",
        "cities": ALL_US,
    },
    {
        "id": "chilis",
        "name": "Chili's",
        "website": "https://www.chilis.com/",
        "menu_url": "https://www.chilis.com/menu",
        "cuisine": "American",
        "price_tier": "$$",
        "cities": ALL_US,
    },
    {
        "id": "outback",
        "name": "Outback Steakhouse",
        "website": "https://www.outback.com/",
        "menu_url": "https://www.outback.com/menu",
        "cuisine": "Steakhouse",
        "price_tier": "$$",
        "cities": ALL_US,
    },
    {
        "id": "texas-roadhouse",
        "name": "Texas Roadhouse",
        "website": "https://www.texasroadhouse.com/",
        "menu_url": "https://www.texasroadhouse.com/global-menu",
        "cuisine": "Steakhouse",
        "price_tier": "$$",
        "cities": ALL_US,
    },
    {
        "id": "red-lobster",
        "name": "Red Lobster",
        "website": "https://www.redlobster.com/",
        "menu_url": "https://www.redlobster.com/menu",
        "cuisine": "Seafood",
        "price_tier": "$$",
        "cities": [c for c in ALL_US if c != "honolulu"],
    },
    {
        "id": "pf-changs",
        "name": "P.F. Chang's",
        "website": "https://www.pfchangs.com/",
        "menu_url": "https://www.pfchangs.com/menu",
        "cuisine": "Chinese",
        "price_tier": "$$",
        "cities": [c for c in ALL_US if c != "asheville"],
    },
    {
        "id": "cheesecake-factory",
        "name": "The Cheesecake Factory",
        "website": "https://www.thecheesecakefactory.com/",
        "menu_url": "https://menu.thecheesecakefactory.com/",
        "cuisine": "American",
        "price_tier": "$$",
        "cities": CHEESECAKE,
    },
    {
        "id": "true-food-kitchen",
        "name": "True Food Kitchen",
        "website": "https://www.truefoodkitchen.com/",
        "menu_url": "https://www.truefoodkitchen.com/menu/",
        "cuisine": "American",
        "price_tier": "$$",
        "cities": TRUE_FOOD,
    },
    {
        "id": "north-italia",
        "name": "North Italia",
        "website": "https://www.northitalia.com/",
        "menu_url": "https://www.northitalia.com/locations/",
        "cuisine": "Italian",
        "price_tier": "$$",
        "cities": NORTH_ITALIA,
    },
    {
        "id": "first-watch",
        "name": "First Watch",
        "website": "https://www.firstwatch.com/",
        "menu_url": "https://www.firstwatch.com/menu/",
        "cuisine": "American",
        "price_tier": "$$",
        "cities": FIRST_WATCH,
    },
    {
        "id": "maggianos",
        "name": "Maggiano's Little Italy",
        "website": "https://www.maggianos.com/",
        "menu_url": "https://locations.maggianos.com/menus/",
        "cuisine": "Italian",
        "price_tier": "$$",
        "cities": MAGGIANOS,
    },
    {
        "id": "yard-house",
        "name": "Yard House",
        "website": "https://www.yardhouse.com/",
        "menu_url": "https://www.yardhouse.com/menu",
        "cuisine": "American",
        "price_tier": "$$",
        "cities": YARD_HOUSE,
    },
    {
        "id": "capital-grille",
        "name": "The Capital Grille",
        "website": "https://www.thecapitalgrille.com/",
        "menu_url": "https://www.thecapitalgrille.com/menu/dinner",
        "cuisine": "Steakhouse",
        "price_tier": "$$$$",
        "cities": CAPITAL_GRILLE,
    },
    {
        "id": "ruths-chris",
        "name": "Ruth's Chris Steak House",
        "website": "https://www.ruthschris.com/",
        "menu_url": "https://www.ruthschris.com/menu",
        "cuisine": "Steakhouse",
        "price_tier": "$$$$",
        "cities": RUTHS_CHRIS,
    },
    {
        "id": "cracker-barrel",
        "name": "Cracker Barrel",
        "website": "https://www.crackerbarrel.com/",
        "menu_url": "https://www.crackerbarrel.com/menu",
        "cuisine": "American",
        "price_tier": "$$",
        "cities": CRACKER_BARREL,
    },
    {
        "id": "seasons-52",
        "name": "Seasons 52",
        "website": "https://www.seasons52.com/",
        "menu_url": "https://www.seasons52.com/menu",
        "cuisine": "American",
        "price_tier": "$$$",
        "cities": SEASONS_52,
    },
    {
        "id": "coopers-hawk",
        "name": "Cooper's Hawk",
        "website": "https://chwinery.com/",
        "menu_url": "https://chwinery.com/menu",
        "cuisine": "American",
        "price_tier": "$$$",
        "cities": COOPERS_HAWK,
    },
    {
        "id": "legal-sea-foods",
        "name": "Legal Sea Foods",
        "website": "https://www.legalseafoods.com/",
        "menu_url": "https://www.legalseafoods.com/menus/",
        "cuisine": "Seafood",
        "price_tier": "$$$",
        "cities": ["boston", "chicago", "philadelphia", "washington"],
    },
]


def city_by_id(dest_id: str):
    for row in US_CITIES:
        if row[0] == dest_id:
            return row
    raise KeyError(dest_id)


def main() -> int:
    city_lookup = {row[0]: row for row in US_CITIES}
    reg = load(REGISTRY)
    existing_slugs = {r["slug"] for r in reg["restaurants"]}
    tally = {"added": 0, "merged": 0, "duplicate": 0, "skipped": 0}
    pku_rows = []

    for chain in CHAINS:
        picks = PICKS.get(chain["id"], [])
        for dest_id in chain["cities"]:
            if dest_id not in city_lookup:
                tally["skipped"] += 1
                continue
            _id, name, region = city_lookup[dest_id]
            slug = f"{chain['id']}-{dest_id}"
            if slug in existing_slugs:
                tally["skipped"] += 1
                continue
            rec = make_record(
                name=chain["name"],
                city=name,
                region=region,
                country="us",
                website=chain["website"],
                source="operator_import",
                added_by="phebe-eats",
                citation=chain["menu_url"],
                menu_urls=[chain["menu_url"]],
            )
            rec["slug"] = slug
            rec["restaurant_id"] = f"{rec['city_id']}/{slug}"
            rec["cuisine"] = chain["cuisine"]
            rec["price_tier"] = chain["price_tier"]
            rec["chain"] = chain["id"]
            rec["notes"] = "US sit-down chain. Menu published by the operator."
            result = add(reg, rec)
            tally[result] += 1
            existing_slugs.add(slug)
            if picks:
                pku_rows.append({"slug": slug, "picks": picks})

    save(reg, REGISTRY)

    if pku_rows:
        pku = json.loads(open(PKU, encoding="utf-8").read())
        by_slug = {r["slug"]: r for r in pku["restaurants"]}
        for row in pku_rows:
            if row["slug"] not in by_slug:
                by_slug[row["slug"]] = {"slug": row["slug"], "picks": row["picks"]}
        pku["restaurants"] = list(by_slug.values())
        with open(PKU, "w", encoding="utf-8") as fh:
            json.dump(pku, fh, indent=2, ensure_ascii=False)
            fh.write("\n")

    print(
        f"{tally['added']} added, {tally['merged']} merged, "
        f"{tally['duplicate']} duplicate, {tally['skipped']} skipped, "
        f"{len(reg['restaurants'])} in registry, {len(pku_rows)} pku rows"
    )
    per_city: dict[str, int] = {}
    for rec in reg["restaurants"]:
        if rec.get("provenance", {}).get("source") == "operator_import" and rec.get(
            "notes", ""
        ).startswith("US sit-down chain"):
            per_city[rec["city_id"]] = per_city.get(rec["city_id"], 0) + 1
    for cid, n in sorted(per_city.items()):
        print(f"  {cid}: {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
