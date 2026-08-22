import json

WORKSHEET = "worksheet.jsonl"
OUT = "run2.jsonl"

VALID_CLASSES = {
    "none", "cereal protein", "vegetable protein", "fruit protein",
    "tuber/root starch", "refined starch", "dairy protein", "legume protein",
    "egg protein", "nut/seed protein", "gelatin/collagen", "unknown protein",
}

# Base mapping keyed by the normalized "ingredients" field. This reflects a
# considered decision made per food-identity group while reading the full
# worksheet (see accompanying classification notes).
BASE_MAP = {
    "agave": "none",
    "alcoholic beverage": "none",
    "applebee's": "vegetable protein",  # coleslaw = cabbage-based
    "apples": "fruit protein",
    "applesauce": "fruit protein",
    "apricots": "fruit protein",
    "arrowroot flour": "refined starch",
    "asparagus": "vegetable protein",
    "avocados": "vegetable protein",
    "bagels": "cereal protein",
    "bamboo shoots": "vegetable protein",
    "bananas": "fruit protein",
    "beets": "vegetable protein",
    "blueberries": "fruit protein",
    "breadfruit": "fruit protein",
    "burdock root": "vegetable protein",
    "butter oil": "none",
    "butter": "dairy protein",
    "cabbage": "vegetable protein",
    "campbell's": "dairy protein",  # cream of mushroom soup, milk-dominant
    "carambola": "fruit protein",
    "carbonated beverage": "none",
    "carrots": "vegetable protein",
    "cassava": "tuber/root starch",
    "catsup": "vegetable protein",
    "cauliflower": "vegetable protein",
    "celery": "vegetable protein",
    "celtuce": "vegetable protein",
    "cereals": "cereal protein",
    "chard": "vegetable protein",
    "chayote": "vegetable protein",
    "cherimoya": "fruit protein",
    "cherries": "fruit protein",
    "chicory greens": "vegetable protein",
    "chicory": "vegetable protein",
    "corn": "cereal protein",
    "cornsalad": "vegetable protein",
    "cornstarch": "refined starch",
    "crabapples": "fruit protein",
    "cracker barrel": "vegetable protein",
    "cranberries": "fruit protein",
    "cranberry juice cocktail": "fruit protein",
    "cucumber": "vegetable protein",
    "dates": "fruit protein",
    "denny's": "vegetable protein",
    "dessert topping": "dairy protein",
    "dock": "vegetable protein",
    "eggplant": "vegetable protein",
    "elderberries": "fruit protein",
    "endive": "vegetable protein",
    "escarole": "vegetable protein",
    "fat": "none",
    "feijoa": "fruit protein",
    "figs": "fruit protein",
    "frostings": "dairy protein",
    "fruit syrup": "none",
    "gelatin desserts": "gelatin/collagen",
    "ginger root": "vegetable protein",
    "gourd": "vegetable protein",
    "grape juice": "fruit protein",
    "grapefruit": "fruit protein",
    "grapes": "fruit protein",
    "guava sauce": "fruit protein",
    "guavas": "fruit protein",
    "hominy": "cereal protein",
    "honey": "none",
    "jackfruit": "fruit protein",
    "jams and preserves": "none",
    "kfc": "vegetable protein",
    "kiwifruit": "fruit protein",
    "kohlrabi": "vegetable protein",
    "lard": "none",
    "leeks": "vegetable protein",
    "lettuce": "vegetable protein",
    "lime juice": "fruit protein",
    "longans": "fruit protein",
    "loquats": "fruit protein",
    "lotus root": "tuber/root starch",
    "mangos": "fruit protein",
    "margarine": "none",
    "marmalade": "none",
    "melons": "fruit protein",
    "milk substitutes": "unknown protein",
    "milk": "dairy protein",
    "mountain yam": "tuber/root starch",
    "mung beans": "legume protein",
    "mushrooms": "vegetable protein",
    "nectarines": "fruit protein",
    "noodles": "refined starch",  # chinese cellophane / mung bean starch noodles
    "nopales": "vegetable protein",
    "nuts": "nut/seed protein",  # chestnuts + coconut (per ruling)
    "oil": "none",
    "okra": "vegetable protein",
    "olives": "fruit protein",
    "onions": "vegetable protein",
    "orange juice": "fruit protein",
    "oranges": "fruit protein",
    "papayas": "fruit protein",
    "peaches": "fruit protein",
    "pears": "fruit protein",
    "peppers": "vegetable protein",
    "persimmons": "fruit protein",
    "pickle relish": "vegetable protein",
    "pickles": "vegetable protein",
    "pie fillings": "fruit protein",
    "pie": "fruit protein",  # overridden per-id for lemon meringue
    "pimento": "vegetable protein",
    "pineapple": "fruit protein",
    "plantains": "fruit protein",
    "plums": "fruit protein",
    "popeyes": "vegetable protein",
    "potato puffs": "tuber/root starch",
    "potatoes": "tuber/root starch",
    "puddings": "refined starch",  # all rows are dry mixes, not milk-prepared
    "pumpkin pie mix": "vegetable protein",
    "pumpkin": "vegetable protein",
    "purslane": "vegetable protein",
    "radicchio": "vegetable protein",
    "radishes": "vegetable protein",
    "rice noodles": "cereal protein",
    "rice": "cereal protein",
    "salt": "none",
    "sandwich spread": "egg protein",  # mayo+pickle relish spread
    "sapodilla": "fruit protein",
    "sapote": "fruit protein",
    "sauce": "vegetable protein",  # pepper/hot sauce (tabasco)
    "sauerkraut": "vegetable protein",
    "seaweed": "vegetable protein",
    "sesbania flower": "vegetable protein",
    "squash": "vegetable protein",
    "strawberries": "fruit protein",
    "sweet potato": "tuber/root starch",
    "syrup": "none",
    "tangerine juice": "fruit protein",
    "tangerines": "fruit protein",
    "tapioca": "refined starch",
    "taro": "tuber/root starch",
    "tomato juice": "vegetable protein",
    "tomato products": "vegetable protein",
    "tomato sauce": "vegetable protein",
    "tomatoes": "vegetable protein",
    "toppings": "dairy protein",  # butterscotch/caramel (butter+cream based)
    "turnip greens": "vegetable protein",
    "turnips": "vegetable protein",
    "vegetable juice cocktail": "vegetable protein",
    "vegetable oil": "none",
    "vegetables": "vegetable protein",
    "vinegar": "none",
    "vinespinach": "vegetable protein",
    "watermelon": "fruit protein",
    "whey": "dairy protein",
    "yam": "tuber/root starch",
    "yambean (jicama)": "vegetable protein",
}

# Explicit per-id overrides for foods whose "ingredients" field is too
# generic (babyfood, beverages, soup, salad dressing, cream substitute,
# candies) or where one specific item within a shared ingredients-group
# differs from the rest (pie: lemon meringue).
ID_OVERRIDES = {
    # Babyfood (ids 48-78)
    "usda-170999": "fruit protein",   # banana with mixed berries, strained
    "usda-173519": "fruit protein",   # beverage, GERBER FRUIT SPLASHERS
    "usda-170967": "cereal protein",  # cereal, mixed, with applesauce and bananas, junior
    "usda-170966": "cereal protein",  # cereal, mixed, with applesauce and bananas, strained
    "usda-171363": "cereal protein",  # cereal, oatmeal, with applesauce and bananas, junior
    "usda-171362": "cereal protein",  # cereal, oatmeal, with applesauce and bananas, strained
    "usda-170970": "cereal protein",  # cereal, rice, with applesauce and bananas, strained
    "usda-171364": "egg protein",     # cereal, with egg yolks, junior
    "usda-170971": "egg protein",     # cereal, with egg yolks, strained
    "usda-172317": "cereal protein",  # corn and sweet potatoes, strained (corn dominant)
    "usda-171379": "egg protein",     # dessert, custard pudding, vanilla, strained
    "usda-170977": "fruit protein",   # dessert, dutch apple, junior
    "usda-171374": "fruit protein",   # dessert, fruit pudding, orange, strained
    "usda-170998": "fruit protein",   # fruit, banana and strawberry, junior
    "usda-173487": "vegetable protein",  # GERBER 2nd Foods, apple, carrot and squash
    "usda-168144": "fruit protein",   # grape juice, no sugar, canned
    "usda-173478": "fruit protein",   # juice treats, fruit medley, toddler
    "usda-170989": "dairy protein",   # mashed cheddar potatoes and broccoli, toddlers
    "usda-173485": "fruit protein",   # snack, GERBER GRADUATE FRUIT STRIPS
    "usda-172255": "fruit protein",   # tropical fruit medley
    "usda-173505": "vegetable protein",  # vegetables, beets, strained
    "usda-173507": "vegetable protein",  # vegetables, carrots, junior
    "usda-173506": "vegetable protein",  # vegetables, carrots, strained
    "usda-171334": "cereal protein",  # vegetables, corn, creamed, junior
    "usda-172280": "cereal protein",  # vegetables, corn, creamed, strained
    "usda-172272": "vegetable protein",  # vegetables, green beans, junior
    "usda-172271": "vegetable protein",  # vegetables, green beans, strained
    "usda-172283": "vegetable protein",  # vegetables, mix vegetables, junior
    "usda-173515": "vegetable protein",  # vegetables, mix vegetables, strained
    "usda-172276": "tuber/root starch",  # vegetables, sweet potatoes, strained
    "usda-172277": "tuber/root starch",  # vegetables, sweet potatoes, junior

    # Beverages (ids 117-131)
    "usda-174820": "nut/seed protein",  # almond milk, chocolate
    "usda-174842": "none",   # club soda
    "usda-173203": "none",   # grape soda
    "usda-174854": "none",   # carbonated, orange
    "usda-173209": "none",   # carbonated, pepper-type
    "usda-171869": "none",   # tonic water
    "usda-171890": "none",   # coffee, brewed, tap water
    "usda-171889": "none",   # coffee, brewed, tap water, decaffeinated
    "usda-175100": "fruit protein",  # Orange drink, breakfast type, with juice/pulp
    "usda-174155": "none",   # tea, black, brewed, distilled water
    "usda-173227": "none",   # tea, black, brewed, tap water
    "usda-174871": "none",   # tea, black, brewed, decaffeinated
    "usda-171918": "none",   # tea, instant, lemon
    "usda-173233": "none",   # water, bottled, PERRIER
    "usda-173234": "none",   # water, bottled, POLAND SPRING

    # Candies (ids 160-161)
    "usda-167995": "gelatin/collagen",  # marshmallows (gelatin-based)
    "usda-167971": "dairy protein",     # TOOTSIE ROLL (milk solids/cocoa)

    # Cream substitute (ids 227-230)
    "usda-173453": "dairy protein",  # flavored, liquid
    "usda-172214": "dairy protein",  # flavored, powdered
    "usda-171261": "legume protein", # with hydrogenated vegetable oil and soy protein
    "usda-171262": "dairy protein",  # with lauric acid oil and sodium caseinate

    # Salad dressing (ids 555-568)
    "usda-171404": "none",           # french dressing, reduced fat
    "usda-171416": "none",           # french, home recipe
    "usda-171417": "none",           # home recipe, vinegar and oil
    "usda-171405": "none",           # italian, commercial, reduced fat
    "usda-171019": "none",           # italian, commercial, regular
    "usda-171403": "egg protein",    # mayonnaise type, regular, with salt
    "usda-171406": "legume protein", # mayonnaise, imitation, soybean
    "usda-171408": "legume protein", # mayonnaise, imitation, soybean, no cholesterol
    "usda-173594": "egg protein",    # mayonnaise, light
    "usda-171009": "egg protein",    # mayonnaise, regular
    "usda-171010": "egg protein",    # mayonnaise, soybean and safflower oil, with salt
    "usda-171007": "egg protein",    # russian dressing, low calorie
    "usda-171008": "egg protein",    # thousand island dressing, reduced fat
    "usda-171402": "egg protein",    # thousand island, commercial, regular

    # Soup (ids 595-606)
    "usda-171537": "dairy protein",   # cream of asparagus, condensed
    "usda-174549": "dairy protein",   # cream of asparagus, prepared with water
    "usda-171540": "dairy protein",   # cream of celery, condensed
    "usda-172907": "dairy protein",   # cream of celery, prepared with water
    "usda-171155": "dairy protein",   # cream of mushroom, condensed
    "usda-171158": "dairy protein",   # cream of potato, condensed
    "usda-172917": "dairy protein",   # cream of potato, prepared with water
    "usda-174807": "egg protein",     # egg drop, Chinese restaurant
    "usda-172913": "unknown protein", # minestrone (mixed veg/bean/pasta, no clear dominant)
    "usda-172881": "dairy protein",   # tomato bisque, condensed
    "usda-171574": "dairy protein",   # tomato bisque, prepared with water
    "usda-171161": "vegetable protein",  # vegetarian vegetable, condensed

    # Pie (ids 487-492) - lemon meringue is egg-dominant, rest default to fruit protein
    "usda-172785": "egg protein",     # Pie, lemon meringue, commercially prepared
}


def classify(row):
    food_id = row["id"]
    if food_id in ID_OVERRIDES:
        return ID_OVERRIDES[food_id]

    name = row["name"].lower()
    ingredients = row["label"]["ingredients"].lower()

    if ingredients == "beans":
        if "snap" in name:
            return "vegetable protein"
        if "mature seeds" in name:
            return "legume protein"
        return "unknown protein"

    if ingredients.startswith("shortening"):
        return "none"

    if ingredients in BASE_MAP:
        return BASE_MAP[ingredients]

    return "unknown protein"


def main():
    rows = []
    with open(WORKSHEET, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))

    print(f"Loaded {len(rows)} worksheet rows")

    results = []
    unknown_fallbacks = []
    for row in rows:
        cls = classify(row)
        if cls not in VALID_CLASSES:
            raise ValueError(f"Invalid class {cls!r} for {row['id']}")
        results.append({"id": row["id"], "phe_source_class": cls})
        if cls == "unknown protein":
            unknown_fallbacks.append((row["id"], row["name"]))

    with open(OUT, "w") as f:
        for r in results:
            f.write(json.dumps(r) + "\n")

    print(f"Wrote {len(results)} lines to {OUT}")

    # Histogram
    hist = {}
    for r in results:
        hist[r["phe_source_class"]] = hist.get(r["phe_source_class"], 0) + 1
    print("\nHistogram:")
    for k, v in sorted(hist.items(), key=lambda kv: -kv[1]):
        print(f"  {k}: {v}")

    print(f"\n'unknown protein' assignments ({len(unknown_fallbacks)}):")
    for fid, fname in unknown_fallbacks:
        print(f"  {fid}: {fname}")

    # Verify id coverage
    worksheet_ids = {row["id"] for row in rows}
    result_ids = [r["id"] for r in results]
    result_id_set = set(result_ids)
    assert len(result_ids) == len(rows), "line count mismatch"
    assert len(result_id_set) == len(result_ids), "duplicate ids in output"
    assert worksheet_ids == result_id_set, "id set mismatch between worksheet and run2"
    print("\nVerification passed: run2.jsonl has exactly", len(results),
          "lines, ids match worksheet exactly (no dupes, none missing).")


if __name__ == "__main__":
    main()
