#!/usr/bin/env python3
"""Fetch per-food phenylalanine + protein from USDA FoodData Central.

Reads the API key via `config.py` (env var FDC_API_KEY or .env; see .env.example).
Dependency-free (stdlib urllib). Used to build / expand the benchmark ground truth.

Usage:
    # single lookups (prints phe mg/100g + FDC id for each query)
    python fetch_fdc.py "cornstarch" "banana raw" "carrots raw"

    # append matched foods to the food reference JSON
    python fetch_fdc.py --update-reference testset/food_reference.json "spinach raw" "peas green raw"

Phenylalanine is USDA nutrient 508; protein is 203. FDC returns phe in grams/100g,
which we convert to mg/100g.
"""
import argparse, json, os, sys, time, urllib.request, urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import config  # noqa: E402


def fdc_search(query, dtype="SR Legacy", n=5):
    params = urllib.parse.urlencode(
        {"query": query, "api_key": config.FDC_API_KEY, "pageSize": n, "dataType": dtype}
    )
    url = f"{config.FDC_API_BASE}/foods/search?{params}"
    with urllib.request.urlopen(url, timeout=30) as resp:
        return json.load(resp)


def extract(food):
    out = {"fdcId": food["fdcId"], "description": food["description"],
           "dataType": food.get("dataType")}
    for n in food.get("foodNutrients", []):
        nm = n.get("nutrientName", "").lower()
        if nm == "protein":
            out["protein_g_per_100g"] = n.get("value")
        if nm == "phenylalanine":
            out["phe_mg_per_100g"] = round((n.get("value") or 0) * 1000, 3)  # g -> mg
    return out


def best_with_phe(query, dtype="SR Legacy"):
    j = fdc_search(query, dtype=dtype)
    for f in j.get("foods", []):
        e = extract(f)
        if e.get("phe_mg_per_100g") is not None:
            return e
    return None


def main():
    ap = argparse.ArgumentParser(description="Fetch FDC phe/protein values")
    ap.add_argument("queries", nargs="+", help="food search terms")
    ap.add_argument("--datatype", default="SR Legacy",
                    help="FDC dataType (SR Legacy | Foundation | Branded)")
    ap.add_argument("--update-reference", metavar="PATH",
                    help="append matched foods into this food_reference.json")
    ap.add_argument("--sleep", type=float, default=2.0,
                    help="seconds between requests (raise if you hit 429)")
    args = ap.parse_args()

    if config.FDC_API_KEY == "DEMO_KEY":
        print("! Using DEMO_KEY (rate-limited). Set FDC_API_KEY in .env for full access.\n",
              file=sys.stderr)

    matched = {}
    for q in args.queries:
        try:
            e = best_with_phe(q, dtype=args.datatype)
        except Exception as ex:
            print(f"  {q!r}: ERROR {type(ex).__name__}: {str(ex)[:120]}", file=sys.stderr)
            e = None
        if e:
            matched[q] = e
            print(f"  {q!r}: fdc {e['fdcId']} | {e['phe_mg_per_100g']} mg phe/100g | "
                  f"{e.get('protein_g_per_100g')} g protein | {e['description']}")
        else:
            print(f"  {q!r}: no SR-Legacy record with a phenylalanine value")
        time.sleep(args.sleep)

    if args.update_reference and matched:
        path = args.update_reference
        ref = json.load(open(path)) if os.path.exists(path) else {"foods": {}}
        ref.setdefault("foods", {}).update(matched)
        json.dump(ref, open(path, "w"), indent=2)
        print(f"\nUpdated {path}: +{len(matched)} foods (total {len(ref['foods'])}).")


if __name__ == "__main__":
    main()
