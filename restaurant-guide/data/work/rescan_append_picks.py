"""Append rescanned PKU dishes after existing picks. Stash Sovereign Remedies."""
from __future__ import annotations

import json
from pathlib import Path

GUIDE = Path(__file__).resolve().parents[2]
DATA = GUIDE / "data"
STASH = GUIDE.parent / "asheville-working"


def pick(name, description, course, kind, hold=None, note=None):
    row = {
        "name": name,
        "description": description,
        "course": course,
        "kind": kind,
        "update": True,
    }
    if hold:
        row["hold"] = hold
    if note:
        row["note"] = note
    return row


UPDATES = {
    "luminosa": [
        pick("Tomato", "blackberry, grebenes, marigold", "starter", "beyond", "grebenes", "Grebenes is pork crackling."),
        pick("Weeds salad", "pickled red onion, ricotta salata, sunflower seeds, peach vinaigrette", "side", "potato_or_salad", "ricotta and sunflower"),
        pick("Grilled little gem", "ramp green goddess, breadcrumb, scallion", "side", "potato_or_salad", "green goddess", "Ask what is in the green goddess."),
        pick("Figs", "sheeps milk yogurt, mint, habanada, sunflower seeds", "starter", "beyond", "yogurt and sunflower"),
        pick("Panzanella", "peach, corn, mozzarella, sherry, herbs", "side", "potato_or_salad", "mozzarella"),
    ],
    "all-day-darling": [
        pick("French Fries", "", "side", "potato_or_salad"),
        pick("Montford", "Lettuces, avocado, gruyere, veggies with champagne vinaigrette", "side", "potato_or_salad", "gruyere"),
    ],
    "curate": [
        pick("ENSALADA", "lettuce blend, pistachio vinaigrette, citrus, olives, idiazabal cheese", "side", "potato_or_salad", "pistachio and cheese"),
        pick("Salteado 'A La Catalana'", "sautéed seasonal greens, pistachio, sweet onions, pickled blueberries", "side", "beyond", "pistachio"),
    ],
    "table": [
        pick("Früts & Rüts", "feta, pistachio, papalo", "starter", "beyond", "feta and pistachio"),
        pick("Lettuces & Vinaigrette", "hazelnuts & herbs", "side", "potato_or_salad", "hazelnuts"),
        pick("Sweet Peppers", "focaccia, walnuts, goat cheese", "starter", "beyond", "walnuts and goat cheese"),
        pick("Rigatoni", "eggplant & mushroom ragout", "main", "main"),
    ],
    "soprana": [
        pick("Caesar Salad", "Baby Gem Lettuce, Pecorino Romano, Garlic Herb Croutons", "side", "potato_or_salad", "Pecorino and croutons", "Ask about the dressing. Caesar is usually egg and anchovy."),
    ],
    "good-hot-fish": [
        pick("Sweet Potato Cabbage Pancake", "Roasted sweet potatoes, cap’n crik, honey hot sauce, pickled collard stems & furikate", "main", "main", "cap’n crik and furikake", "Ask what is in them. Furikake is often fish."),
        pick("Ranchovy Iceburg", "Zesty ranch meets Caesar dressing over iceberg lettuce with pickled red onions, crispy shallots", "side", "potato_or_salad", "ranch and Caesar", "Ranch and Caesar are usually egg. Caesar is often anchovy."),
        pick("Hushpuppies", "", "side", "beyond"),
    ],
    "leos-house-of-thirst": [
        pick("Caesar", "Local greens, urfa biber, boquerones, breadcrumb, benne seed", "side", "potato_or_salad", "boquerones and benne", "Boquerones are anchovy. Benne is sesame."),
        pick("Potato Salad", "Smoked trout gribiche, lovage, radish", "side", "potato_or_salad", "trout gribiche", "Gribiche is usually egg. Trout is fish."),
    ],
    "tall-johns": [
        pick("Classic Caesar Salad", "", "side", "potato_or_salad", "dressing and cheese", "Ask about the dressing. Caesar is usually egg and anchovy."),
    ],
    "ukiah": [
        pick("Heirloom Tomato Salad", "charred tofu, green chilies + shiso", "side", "potato_or_salad", "tofu"),
        pick("Avocado Salad", "house feta, baby herbs, crispy leeks +lemon ginger dressing", "side", "potato_or_salad", "feta"),
        pick("Vegetable Gyoza", "edamame + shitake, vegan herb ponzu", "starter", "beyond"),
        pick("Crispy Mushroom Bao", "Black garlic aioli + yuzu pickle", "starter", "beyond", "aioli", "Ask what is in the aioli."),
        pick("Grilled Maitake Mushrooms", "peas, mint, wasabi, brown butter + ponzu", "side", "beyond", "brown butter"),
        pick("Tokyo Street Corn", "kewpie mayo, togarashi, itto nori, miso butter + bonito", "side", "beyond", "mayo, nori, and bonito", "Kewpie is egg. Bonito is fish."),
    ],
    "plant": [
        pick("Flatbread + Spread", "roasted red pepper dip, za’atar flatbread, date sausage, preserved lemon", "starter", "beyond", "date sausage", "Ask whether the sausage is plant."),
    ],
    "rhubarb": [
        pick("Beets and Berries", "Blackberries, Hazelnuts, Dill, Horseradish Creme Fraiche, Pickled Beets, Honey", "starter", "beyond", "hazelnuts and crème fraîche"),
        pick("Tomato Caesar", "Romas, Basil Caesar, Tomato Leaf Oil, Croutons, Pickled Peppers", "side", "potato_or_salad", "Caesar and croutons", "Ask about the dressing. Caesar is usually egg and anchovy."),
    ],
    "jargon": [
        pick("Local Greens", "grilled corn, parmigiano, Marcona almonds, cherry tomatoes, preserved lemon vinaigrette", "side", "potato_or_salad", "parmigiano and almonds"),
        pick("Heirloom Tomato Salad", "shishito peppers, cashew tzatziki, shawarma vinaigrette, crunchy alliums", "side", "potato_or_salad", "cashew tzatziki", "Cashew is nuts."),
    ],
    "posana": [
        pick("Little Gem Caesar", "black garlic Caesar dressing, shaved Parmesan, heirloom cherry tomatoes, butter herb croutons", "side", "potato_or_salad", "Parmesan and croutons", "Ask about the dressing. Caesar is usually egg and anchovy."),
        pick("Kale Salad", "Three Graces Dairy Manchego-style cheese, pumpkin seeds, currants, lemon, olive oil", "side", "potato_or_salad", "cheese and pumpkin seeds"),
        pick("Broccolini", "saffron Béarnaise", "side", "beyond", "Béarnaise", "Béarnaise is usually egg and butter."),
        pick("Haricot Verts", "fleur de sel, cracked pepper", "side", "beyond"),
    ],
    "zambra-tapas-wine-bar": [
        pick("Muhammara", "Roasted Red Pepper and Walnut Spread. Sumac, Pomegranate Molasses, Za'atar Garlic Pita.", "starter", "beyond", "walnut", "Muhammara is nuts."),
    ],
    "asheville-proper": [
        pick("Grilled Frisée & Arugula", "smoked blue cheese dressing, fresh blackberries, squash noodles, pickled corn, fried crunchies", "side", "potato_or_salad", "blue cheese"),
        pick("Grilled Skillet Corn Brûlée", "mixed cheese crisps, bourbon bacon, sumac compressed shallots", "side", "beyond", "cheese and bacon"),
    ],
    "red-ginger": [
        pick("Scallion Pan Cake", "", "starter", "beyond"),
        pick("Mushroom Dumpling", "steamed with assorted mushrooms & veggies", "starter", "beyond"),
        pick("Pan Fried Veggie Dumpling", "cabbage, celery, carrots and rice noodle with chef’s seasoning", "starter", "beyond"),
        pick("Mango Lover Roll", "vegetarian sushi roll with fresh mango, avocado and cucumber in chef's citrus mango sauce", "starter", "beyond"),
        pick("Vegetable Fired Rice or Lo mein", "", "main", "main"),
        pick("Vegetable Chow Fun", "Wok fried wide rice noodle with onion, scallion, bean sprout, egg, mushroom and Yau Choy", "main", "main", "egg"),
        pick("Cool Breeze Noodles", "Chilled thin noodles tossed with scallion and crisp radish seed in a light sweet vinegar dressing", "side", "beyond"),
    ],
    "bargello": [
        pick("Avocado Toast", "Two Slices of Homemade Rustic Toast, Whipped Avocado, Radish, Feta, Aleppo", "main", "main", "feta"),
        pick("Fresh Fruit", "", "starter", "beyond"),
        pick("Breakfast Potatoes", "", "side", "potato_or_salad"),
        pick("Caesar Salad", "Romaine, Aged Parmesan, Focaccia Croutons, Creamy Anchovy & Cacio Dressing", "side", "potato_or_salad", "Parmesan and dressing", "Caesar is egg and anchovy."),
    ],
    "early-girl-eatery": [
        pick("Ginger & Dill Coleslaw", "Creamy, crunchy scratch-made slaw with a hint of ginger.", "side", "beyond"),
        pick("French Fries", "", "side", "potato_or_salad"),
        pick("Apple & Berry Salad", "Organic spring mix, seasonal apple and berries, spicy candied pecans, herbed goat cheese.", "side", "potato_or_salad", "pecans and goat cheese"),
        pick("Roasted Brussel Sprout Salad", "Roasted Brussel sprouts, organic spring mix, herbed goat cheese, roasted sweet potatoes, pepitas.", "side", "potato_or_salad", "goat cheese and pepitas"),
    ],
    "corner-kitchen": [
        pick("Pesto Artichoke Tartine", "Grilled Artichokes, Fontina Cheese, Caper Tapenade, Roasted Red Peppers, Baby Arugula, Local Focaccia", "main", "main", "Fontina"),
        pick("Seasoned Fries", "", "side", "potato_or_salad"),
        pick("Fruit Salad", "", "side", "beyond"),
        pick("Side Salad", "", "side", "potato_or_salad"),
    ],
    "addissae": [
        pick("Salad", "", "side", "potato_or_salad"),
    ],
    "nine-mile": [
        pick("The Groundation", "Mixed greens, feta cheese, cherry tomatoes, carrots, kalamata olives & chickpeas. Served with sesame garlic tahini dressing.", "side", "potato_or_salad", "feta, chickpeas, and tahini", "Tahini is sesame."),
    ],
}


def nameset(picks):
    return {p["name"].strip().lower() for p in picks}


def main():
    pku = json.loads((DATA / "pku.json").read_text())
    reg = json.loads((DATA / "restaurants.json").read_text())
    stash_reg = json.loads((STASH / "restaurants.json").read_text())
    stash_pku = json.loads((STASH / "pku.json").read_text())

    sov_reg = next(r for r in reg["restaurants"] if r["slug"] == "sovereign-remedies")
    sov_pku = next(r for r in pku["restaurants"] if r["slug"] == "sovereign-remedies")
    if not any(r["slug"] == "sovereign-remedies" for r in stash_reg["restaurants"]):
        stash_reg["restaurants"].append(sov_reg)
    if not any(r["slug"] == "sovereign-remedies" for r in stash_pku["restaurants"]):
        stash_pku["restaurants"].append(sov_pku)
    stash_reg["restaurant_count"] = len(stash_reg["restaurants"])

    reg["restaurants"] = [r for r in reg["restaurants"] if r["slug"] != "sovereign-remedies"]
    reg["restaurant_count"] = len(reg["restaurants"])
    pku["restaurants"] = [r for r in pku["restaurants"] if r["slug"] != "sovereign-remedies"]

    added = 0
    for entry in pku["restaurants"]:
        extras = UPDATES.get(entry["slug"], [])
        have = nameset(entry["picks"])
        for p in extras:
            if p["name"].strip().lower() in have:
                continue
            entry["picks"].append(p)
            have.add(p["name"].strip().lower())
            added += 1

    pku["note"] = (
        "Picks are dishes from a posted menu that may work for a low-protein / low-phe plate. "
        "They are questions for the kitchen, not a safety claim. Every pick counts on mains or plates, "
        "including potato and salad. Accommodation, off-menu, and Phebe-verified are set only after contact or a visit."
    )
    pku["flag"] = (
        "Scale is seven independent dots named 2026-08-23: published menu, a main, plates beyond potato and salad, "
        "accommodation, cook off-menu, third-party award, Phebe-verified. See web/SCORING-FLAG.md."
    )

    (STASH / "restaurants.json").write_text(
        json.dumps(stash_reg, indent=1, ensure_ascii=False) + "\n"
    )
    (STASH / "pku.json").write_text(
        json.dumps(stash_pku, indent=2, ensure_ascii=False) + "\n"
    )
    (DATA / "restaurants.json").write_text(
        json.dumps(reg, indent=1, ensure_ascii=False) + "\n"
    )
    (DATA / "pku.json").write_text(
        json.dumps(pku, indent=2, ensure_ascii=False) + "\n"
    )

    print(f"live restaurants {reg['restaurant_count']}")
    print(f"stash restaurants {stash_reg['restaurant_count']}")
    print(f"appended picks {added}")
    for entry in pku["restaurants"]:
        mains = sum(1 for p in entry["picks"] if p["kind"] == "main")
        plates = sum(1 for p in entry["picks"] if p["kind"] != "main")
        extras_n = sum(1 for p in entry["picks"] if p.get("update"))
        print(f"  {entry['slug']}: {mains} mains, {plates} plates, +{extras_n} updates")


if __name__ == "__main__":
    main()
