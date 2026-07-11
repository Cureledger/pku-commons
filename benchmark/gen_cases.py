#!/usr/bin/env python3
"""Generate benchmark test cases from declared recipes + a food reference.

Ground truth is computed, never guessed: for each ingredient we pull phe_mg_per_100g
and the fdcId straight from testset/food_reference.json (already FDC-verified), then
    phe_mg = phe_mg_per_100g * grams / 100
    expected_phe_mg = sum(components)
So every generated case carries real provenance and passes validate_cases.py by
construction. When the reference list grows, add recipes and re-run — cases expand
automatically.

A recipe is: id, name, list of (reference_key, grams), optional serving_size_g
(defaults to sum of grams), optional protein_g_per_serving (None => whole-food path).
Ingredient TEXT is emitted in the recipe's declared order, so you control whether a
case is a weight-share trap (declare a phe-dense item first but light).

Usage:
    python gen_cases.py --recipes /tmp/pkuwork/recipes.json \
        --reference testset/food_reference.json --out /tmp/pkuwork/generated.jsonl
"""
import argparse, json, sys

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--recipes",required=True)
    ap.add_argument("--reference",default="testset/food_reference.json")
    ap.add_argument("--out",required=True)
    a=ap.parse_args()
    ref=json.load(open(a.reference))["foods"]
    recipes=json.load(open(a.recipes))
    lines=[]; missing=set()
    for r in recipes:
        comps=[]; total=0.0; texts=[]
        ok=True
        for key,grams in r["ingredients"]:
            if key not in ref:
                missing.add(key); ok=False; continue
            row=ref[key]
            phe100=row["phe_mg_per_100g"]
            phe=round(phe100*grams/100.0,2)
            total+=phe
            comps.append({"food":key,"fdcId":int(row["fdcId"]),"grams":grams,
                          "phe_mg_per_100g":phe100,"phe_mg":phe})
            texts.append(row.get("description",key).split(",")[0])
        if not ok: continue
        serving=r.get("serving_size_g",sum(g for _,g in r["ingredients"]))
        case={"id":r["id"],"name":r["name"],
              "label":{"serving_size_g":serving,
                       "protein_g_per_serving":r.get("protein_g_per_serving"),
                       "ingredients":", ".join(texts)},
              "expected_phe_mg":round(total,1),
              "ground_truth":{"method":"sum(FDC phe_mg_per_100g * grams/100) per component",
                              "source":"USDA FoodData Central (SR Legacy), nutrient 508 Phenylalanine",
                              "components":comps},
              "notes":r.get("notes","")}
        lines.append(json.dumps(case))
    open(a.out,"w").write("\n".join(lines)+("\n" if lines else ""))
    print(f"generated {len(lines)} cases -> {a.out}")
    if missing: print(f"skipped: keys not in reference: {sorted(missing)}")

if __name__=="__main__": main()
