"""Add PKU picks for the post-Michelin Asheville restaurants.

Picks are from official posted menus fetched 2026-08-23. Empty picks mean
no usable posted menu, or the kitchen is not serving regular dinner.
Accommodation and MNT are not set.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PKU = ROOT / "pku.json"
REG = ROOT / "restaurants.json"


def pick(name, description, course, kind, hold=None, note=None):
    row = {
        "name": name,
        "description": description,
        "course": course,
        "kind": kind,
    }
    if hold:
        row["hold"] = hold
    if note:
        row["note"] = note
    return row


# Official posted menus only. Closed or no posted text => [].
NEW = {
    "plant": [
        pick("Lion Steak Tostadas", "chimichurri, queso fresco, sour cream, jalapeno-onion relish", "main", "main", "queso fresco and sour cream", "Plant cheese is usually nuts."),
        pick("Cauliflower", "tahini, chili cra’q, grilled lemon, salt & pepper breadcrumbs, parsley", "starter", "beyond", "tahini", "Tahini is sesame."),
        pick("Grilled Beets", "balsamic & herbs, horseradish mayo, onion tumbleweed", "starter", "beyond", "horseradish mayo", "Mayo is egg."),
        pick("Actually Crispy Potatoes", "italian salsa verde, shallot butter", "side", "potato_or_salad", "shallot butter"),
        pick("Gem & Carrot Salad", "baby gem lettuce, roasted carrot, cocorino cheese, creamy lemon dressing, hazelnut", "side", "potato_or_salad", "cocorino and hazelnut", "Cocorino is nut cheese."),
    ],
    "chai-pani": [
        pick("Matchstick Okra Fries", "Julienned “okra fries” tossed with salt & seasoning, served with a lime wedge.", "starter", "beyond"),
    ],
    "rhubarb": [
        pick("Grilled Jimmy Nardello Peppers", "Ricotta, BBQ Rub, Grilled Focaccia, Marcona Almonds", "starter", "beyond", "ricotta and almonds"),
        pick("Corn & Shishito Gazpacho", "Peppers, Corn, Sumac Tajin", "starter", "beyond"),
        pick("Fried Eggplant", "Rosemary honey, Pickled Peppers, Crushed Red Pepper", "starter", "beyond"),
        pick("Blistered Shishito Peppers", "Cantaloupe, XO Sauce, Shiso, Peanuts", "starter", "beyond", "XO sauce and peanuts", "XO is usually seafood."),
        pick("Butter Braised Cabbage", "Miso-Beurre Blanc, Pickled Walnuts, Crispy Cabbage, Furikake, Bonito Flake", "main", "main", "walnuts and bonito", "Bonito is fish."),
        pick("Summer Salad of Local Lettuces", "Wild East Radishes, Herbs, Pickled Turnips, Poppy Seed Granola, Dill Goat Cheese, NC Peaches, Cucumbers Buttermilk Dressing", "side", "potato_or_salad", "goat cheese and granola"),
    ],
    "jargon": [
        pick("Glazed Lion's Mane", "grilled Japanese eggplant, coconut rice noodles, do chua, basil, Aleppo oil", "main", "main"),
        pick("Grilled Local Peppers", "tamarind glaze, burnt sorghum, cilantro, sesame seeds", "starter", "beyond", "sesame"),
        pick("Grilled Carrots", "whipped labneh, ras el hanout, pistachio dukkah", "starter", "beyond", "labneh and pistachio"),
        pick("Charred Pole Beans", "black garlic bagna cauda, whipped feta, peppadew relish, lemon", "starter", "beyond", "feta", "Bagna cauda is usually anchovy."),
        pick("Smashed Fingerlings", "aioli, Spanish chorizo vinaigrette, cilantro", "side", "potato_or_salad", "aioli and chorizo vinaigrette", "Aioli is egg."),
    ],
    "posana": [
        pick("Forest-Cultivated Mushrooms", "oyster, shiitake, beech, miso emulsion, greens, crispy chickpeas", "starter", "beyond", "crispy chickpeas"),
        pick("Roasted Beets", "brown butter labneh, pistachio vinaigrette, mint, smoked salt", "starter", "beyond", "labneh and pistachio"),
        pick("Fried Green Tomatoes", "cornmeal crust, herbed yogurt, green tomato relish", "starter", "beyond", "herbed yogurt"),
        pick("Honey-Roasted Carrots", "local baby carrots, coconut carrot top basil pesto", "side", "beyond"),
        pick("Grilled Zucchini", "lemon, flake salt", "side", "beyond"),
        pick("Grilled Asparagus", "lemon, sea salt, extra virgin olive oil", "side", "beyond"),
        pick("Fingerling Pomme Frites", "truffle aioli, Parmesan", "side", "potato_or_salad", "aioli and Parmesan", "Aioli is egg."),
    ],
    "zambra-tapas-wine-bar": [
        pick("Harissa Marinated Olives", "", "starter", "beyond"),
        pick("Harissa Roasted Baby Carrots", "Whipped Goat Cheese, Roasted Pistachio, Spiced Honey", "starter", "beyond", "goat cheese and pistachio"),
        pick("Patatas Bravas", "Roasted Garlic Aioli, Salsa Brava, Chive", "side", "potato_or_salad", "aioli", "Aioli is egg."),
        pick("Fattoush", "Local Leaf Lettuce, Cucumber, Radish, Mint, Cherry Tomato, Avocado, Feta, Pita Crouton, Black Cardamom Vinaigrette, Sumac", "side", "potato_or_salad", "feta"),
    ],
    "asheville-proper": [
        pick("Local Heirloom Tomatoes", "grilled cherry tomatoes, tomato jam, tomato crumble", "side", "beyond"),
        pick("Charred Local Red Beets", "pickled blackberries, smoked goat cheese, malted mint vinaigrette", "side", "beyond", "goat cheese"),
        pick("Char-Grilled Local Zucchini", "yellow squash filling, croissant rouille, fried garlic bits", "side", "beyond", "croissant rouille", "Rouille is usually egg."),
        pick("Sautéed Local Mushroom", "peach BBQ, smoked cheeses, fried shallots", "side", "beyond", "smoked cheeses"),
        pick("Tallow Confit Potato Medley", "mimosa vinaigrette, scallion cheese, grilled maple almonds", "side", "potato_or_salad", "cheese and almonds"),
        pick("Mixed Leafy Greens", "olive caper dressing, heirloom tomato chips, smoked feta, pickled red onions, herb hazelnuts", "side", "potato_or_salad", "feta and hazelnuts"),
    ],
    "post-70-indulgence-bar": [
        pick("Warm Olives and Almonds", "Spanish and Kalamata, Garlic, Onion, Lemon, Honey, Oregano, Baguette", "starter", "beyond", "almonds"),
        pick("Roasted Broccoli", "Mornay Sauce", "side", "beyond", "Mornay", "Mornay is cheese."),
        pick("Pomme Frites", "Duck Fat, Thyme", "side", "potato_or_salad"),
        pick("Smashed Fingerlings", "Truffle Oil, Parmesan", "side", "potato_or_salad", "Parmesan"),
        pick("Spinach Salad", "Apple, Red Onion, Parmesan, Lemon, EVOO, Balsamic", "side", "potato_or_salad", "Parmesan"),
    ],
    "sovereign-remedies": [
        pick("Potato Chips", "", "side", "potato_or_salad"),
    ],
    "red-ginger": [
        pick("Yau Choy", "Season Chinese green vegetable stir fried with garlic and ginger", "main", "main"),
        pick("Stir Fried String Bean", "dry sautéed string bean with minced pickle in garlic soy sauce", "side", "beyond"),
        pick("Crispy Eggplant HK Style", "Tempura fried eggplant with mild spicy seasoning", "starter", "beyond"),
        pick("House Veggie Spring Rolls", "shredded cabbage, bok choy, carrots with chef’s seasoning", "starter", "beyond"),
        pick("Seaweed Salad", "", "side", "potato_or_salad"),
    ],
    "bargello": [
        pick("Garden Fritters", "Crispy Zucchini & Potato Cakes, Pickled Vegetables, Feta, Arugula, Spicy Yogurt, Herbs", "starter", "beyond", "feta and yogurt"),
        pick("Orecchiette", "Made Simple with Shaved Romano & Fresh Basil. Your choice of pesto, Parmesan cream, marinara, vodka sauce, olive oil or butter", "main", "main", "Romano", "Ask for olive oil or marinara."),
        pick("Grilled Broccolini", "Preserved Lemon Vinaigrette", "side", "beyond"),
        pick("Summer Squash", "Sauteed with White Wine & Butter", "side", "beyond", "butter"),
        pick("Cacio Truffle Fries", "Parmesan & Romano, Truffle Oil, Rosemary, Aleppo", "side", "potato_or_salad", "Parmesan and Romano"),
        pick("Athena’s Salad", "Spinach, Tomato, Citrus Olives, Cucumber, Red Onion, Feta, Greek Dressing", "side", "potato_or_salad", "feta"),
    ],
    "early-girl-eatery": [
        pick("Balsamic Roasted Vegetables", "Roasted Brussels sprouts and glazed sweet potatoes tossed in tangy balsamic vinaigrette. Topped with toasted pepitas.", "main", "main", "pepitas"),
        pick("Spicy Sesame Brussels", "Pan-Seared Brussels sprouts tossed in savory sesame sauce, finished with a Korean BBQ drizzle, toasted sesame seeds, and green onions.", "side", "beyond", "sesame"),
        pick("Cinnamon Apples", "Warm, tender apples simmered with sweet cinnamon spice.", "side", "beyond"),
        pick("Fresh Fruit Cup", "A refreshing mix of seasonal melon, berries, and bananas.", "starter", "beyond"),
        pick("Seasoned Home Fries", "", "side", "potato_or_salad"),
        pick("Small Salad", "Organic spring mix, bell peppers, and diced tomatoes", "side", "potato_or_salad"),
    ],
    "corner-kitchen": [
        pick("Kung Pao Cauliflower", "Bell Peppers, Onions, Tamari Ginger Glaze, Ramp Dusted Peanuts, Scallions, Sesame Seeds", "starter", "beyond", "peanuts and sesame"),
        pick("Tomato Gazpacho", "Cilantro Crème", "starter", "beyond", "cilantro crème"),
        pick("Heirloom Panzanella", "Baguette, Tomatoes, Grilled Peaches, Dare Vegan Cashew Cheese, Basil, Lemon, EVOO", "side", "potato_or_salad", "cashew cheese", "Cashew cheese is nuts."),
        pick("S.C. Strawberry & Feta Salad", "Fancy Greens, Bulgarian Feta, Hot Honey Pistachios, Pickled Red Onion, Balsamic Reduction, Lavender Honey Vinaigrette", "side", "potato_or_salad", "feta and pistachios"),
    ],
    "limones": [
        pick("Roasted Beets", "butternut squash-miso mash, pepita muhammara, braised savoy cabbage, corn relish, cashew-cilantro crema", "main", "main", "pepita muhammara and cashew crema", "Muhammara is usually nuts."),
        pick("SC Peaches", "hot honey, pistachio crumble, whipped requeson", "starter", "beyond", "pistachio and requeson", "Requeson is cheese."),
        pick("Market Salad", "watermelon, feta cheese, lemon-basil dressing, marcona almonds", "side", "potato_or_salad", "feta and almonds"),
    ],
    "nine-mile": [
        pick("Natural Mystic", "Linguine topped with house marinara sauce. (add vegetables)", "main", "main"),
        pick("More Fyah!", "Grilled jerk chicken or jerk tofu with bell peppers, fire roasted tomatoes, squash, & zucchini. Sautéed with white wine & butter. Tossed with linguine.", "main", "main", "chicken or tofu and butter"),
        pick("Lion A Roar", "Tomato mango chipotle salsa or spicy garden blend salsa with chips", "starter", "potato_or_salad"),
    ],
    "wasabi": [
        pick("Vegetable Tempura", "", "starter", "beyond"),
        pick("Asian Curry, Vegetable", "coconut milk based curry served with snow peas, sweet potatoes, onions, and shitake mushrooms", "main", "main"),
    ],
}

EMPTY = [
    "bull-beggar",
    "la-bodega-by-curate",
    "haywood-common",
    "itto-ramen-bar-tapas",
    "jerusalem-garden-cafe",
    "baba-nahm",
    "gypsy-queen-cuisine",
    "the-med",
    "biscuit-head",
    "tupelo-honey-southern-kitchen-bar",
    "green-sage-cafe",
    "liberty-house-cafe",
    "moose-cafe",
    "city-bakery",
    "flour",
    "abejas-house-cafe",
    "the-blackbird",
    "white-duck-taco-shop",
    "taco-billy",
    "mamacitas-taco-temple",
    "cantina-louie",
    "tamaleria-y-tortilleria-molina",
    "mountain-madre-mexican-kitchen-and-agave-bar",
    "salsas",
    "peace-love-tacos",
    "andale-way-mexican-grill",
    "la-rumba-restaurant-latino",
    "taqueria-munoz",
    "the-standard",
    "pie-zaa",
    "andaaz",
]

WEBSITES = {
    "plant": "https://www.plantisfood.com",
    "bull-beggar": "https://thebullandbeggar.com",
    "jargon": "https://www.jargonrestaurant.com",
    "asheville-proper": "https://www.ashevilleproper.com",
    "post-70-indulgence-bar": "https://filopost70.com",
    "sovereign-remedies": "https://www.sovereignremedies.com",
    "haywood-common": "https://haywoodcommon.com",
    "red-ginger": "http://www.redgingerasheville.com",
    "itto-ramen-bar-tapas": "https://www.ittoramen.com",
    "jerusalem-garden-cafe": "https://jerusalemgardencafe.com",
    "bargello": "https://bargelloavl.com",
    "the-med": "https://www.themedavl.com",
    "biscuit-head": "https://biscuitheads.com",
    "early-girl-eatery": "https://earlygirleatery.com",
    "tupelo-honey-southern-kitchen-bar": "https://tupelohoneycafe.com",
    "green-sage-cafe": "https://www.greensagecafe.com",
    "corner-kitchen": "https://thecornerkitchen.com",
    "white-duck-taco-shop": "https://whiteducktacoshop.com",
    "limones": "https://www.limonesavl.com",
    "wasabi": "https://wasabiavl.com",
    "nine-mile": "https://ninemileavl.com",
}

ADDRESSES = {
    "plant": "165 Merrimon Ave., Asheville, NC 28801",
    "chai-pani": "32 Banks Avenue, Asheville, NC 28801",
    "bull-beggar": "37 Paynes Way, Asheville, NC 28801",
    "jargon": "715 Haywood Rd, Asheville, NC 28806",
    "la-bodega-by-curate": "32 South Lexington Avenue, Asheville, NC 28801",
    "asheville-proper": "1 Page Ave, Asheville, NC 28801",
    "post-70-indulgence-bar": "1155 Tunnel Road, Asheville, NC 28805",
    "sovereign-remedies": "29 N Market St, Asheville, NC 28801",
}

NOTES = {
    "la-bodega-by-curate": "Regular dining ended February 2025. Event venue only. Cúrate remains open.",
    "plant": "Vegan. Posted menu is a sample; the kitchen remakes it daily. 165 Merrimon Ave.",
}


def main():
    pku = json.loads(PKU.read_text())
    by_slug = {r["slug"]: r for r in pku["restaurants"]}
    for slug, picks in NEW.items():
        by_slug[slug] = {"slug": slug, "picks": picks}
    for slug in EMPTY:
        by_slug.setdefault(slug, {"slug": slug, "picks": []})
    # Keep existing Michelin entries first, then the new slugs in harvest order.
    existing = [r for r in pku["restaurants"] if r["slug"] not in NEW and r["slug"] not in EMPTY]
    added = [by_slug[s] for s in list(NEW) + EMPTY]
    pku["restaurants"] = existing + added
    PKU.write_text(json.dumps(pku, indent=2, ensure_ascii=False) + "\n")

    reg = json.loads(REG.read_text())
    for r in reg["restaurants"]:
        slug = r["slug"]
        if slug in WEBSITES and not r.get("website"):
            r["website"] = WEBSITES[slug]
        if slug in ADDRESSES and not r.get("address"):
            r["address"] = ADDRESSES[slug]
        if slug == "chai-pani":
            r["address"] = ADDRESSES["chai-pani"]
        if slug in NOTES:
            old = (r.get("notes") or "").strip()
            if NOTES[slug] not in old:
                r["notes"] = (old + " " + NOTES[slug]).strip() if old else NOTES[slug]
    REG.write_text(json.dumps(reg, indent=1, ensure_ascii=False) + "\n")
    print("pku restaurants:", len(pku["restaurants"]))
    print("with picks:", sum(1 for r in pku["restaurants"] if r["picks"]))
    print("new with picks:", len(NEW))
    print("new empty:", len(EMPTY))


if __name__ == "__main__":
    main()
