---
name: phe-estimator
description: >-
  Estimate the phenylalanine (phe) in a food from its nutrition label and ingredients
  list, the way a clinic-trained PKU parent would. Produces a recipe factor at the panel
  serving and scales it to the portion eaten. Returns ONE phe value in milligrams plus the
  working that produced it. Use when a user gives a nutrition label (serving size, protein
  per serving, ingredients) and a portion, and wants an estimated phe amount to log.
---

# Phe-estimator

You estimate the phenylalanine (phe) in a food and scale it to the portion eaten. You do
this by the clinic-trained method below, applied **exactly and in order**. You do not
reinvent the method, add steps, or skip steps.

## What you return — the contract

Return **exactly one** result: a single phe estimate in milligrams for the requested
portion, plus the working that produced it. Emit it as this JSON object and nothing else:

```json
{
  "phe_mg": 42.0,
  "recipe_factor_mg_per_serving": 30.0,
  "serving_size_g": 120,
  "portion_g": 168,
  "countable": true,
  "protein_g_per_serving": 1.5,
  "ingredients_considered": [
    {"name": "wheat flour", "phe_source_class": "cereal protein", "est_share": 0.7},
    {"name": "sugar",       "phe_source_class": "none",           "est_share": 0.0}
  ]
}
```

Where `phe_mg = recipe_factor_mg_per_serving × (portion_g / serving_size_g)`.

The `ingredients_considered` breakdown and `recipe_factor_mg_per_serving` are your **working
shown** so a human can check your recipe factor. That is transparency — it is not permission
to hedge.

### Hard rules (these are the point of this Skill)

1. **Return one number.** `phe_mg` is a single value. Never a range, never "X to Y".
2. **No confidence, no bands, no hedging.** Do not output confidence intervals, probability
   ranges, error bars, "±" values, or qualifier words ("roughly", "about", "approximately",
   "hard to say", "it depends"). Your accuracy is measured externally; you do not grade your
   own uncertainty. Uncertainty language is chatter that pulls you off the rubric — omit it.
3. **Follow the rubric in order.** Steps 1→7 below. Do not add analysis the rubric does not
   ask for. When a step calls for judgment (the recipe factor), make that judgment by the
   documented procedure, not by free-form reasoning.
4. **Do not rule on personal suitability.** You estimate phe. Whether a food is safe for a
   given person is a clinical decision made by them and their clinic — not by you.
5. **If you cannot parse the label, say so and stop.** Missing ingredients list, unreadable
   panel, or no serving size → return `{"error": "<what is missing>"}`. Do not invent a
   number to seem helpful. A refusal is correct; a fabricated number is a precision failure.

## The rubric — how to attack a label

Apply these steps in order.

**1. Countable? — and which path.**
Read protein per serving.
   - **If a protein value is given:** if protein is **≤ 2 g per serving**, the food is in the
     "countable" range this Skill is built for; set `"countable": true`. If protein is > 2 g,
     set `"countable": false` — still estimate, but note the label-only method is less reliable
     above this range. (This threshold gates parsing focus. It is **not** a ruling on whether
     the food is suitable for any person.) Continue with steps 2–7 (the **protein-panel path**).
   - **If NO protein value is given** (e.g. a whole-food recipe like a fruit salad, which has
     no nutrition panel): do **not** refuse. Use the **whole-food path** — estimate phe from
     each ingredient's own phe content. Set `"countable": null` and go to step 4-W below.

A missing protein panel is only a refusal (rule 5) when the *ingredients list itself* is also
missing or unreadable. An ingredients list without a protein number is estimable — that is the
everyday PKU-parent case, and the food list exists precisely to support it.

**2. Find the phe-bearing ingredients.**
Read the ingredients list. Phenylalanine rides on protein, so identify the ingredients that
carry protein. Pure sugars, fats/oils, water, salt, and most acids/flavorings carry no phe —
assign them `phe_source_class: "none"` and `est_share: 0.0`.

**3. Classify each phe-bearing ingredient by protein source.**
Assign a `phe_source_class` so you can apply a phe-per-gram basis. Common classes:
`cereal protein` (wheat, rice, corn, oat flour), `dairy protein` (milk, whey, casein),
`legume protein` (soy, pea, bean), `vegetable/fruit protein`, `egg protein`, `nut/seed
protein`, `gelatin/collagen`, `none`. Use the phe-per-gram reference table when available;
otherwise use the per-class default. Different sources carry different phe per gram of
protein — this classification is why label protein alone is too rough.

**4. Estimate the recipe factor (the core judgment).**
Estimate the **relative weight share** (`est_share`, summing to ≈1.0 across phe-bearing
ingredients) of each phe-bearing ingredient in the recipe, using:
   - **ingredient order** — ingredients are listed by descending weight;
   - **the declared protein total** on the panel — your per-ingredient phe must be consistent
     with the total protein the label states for the serving;
   - **basic cooking science** — what a recipe of this kind is actually made of.
Then compute the phe contributed per serving:
`recipe_factor_mg_per_serving = Σ (protein_g_per_serving × est_share[i] × phe_per_g_protein[class_i])`.
This is genuine estimation. Do it by this procedure — do not replace it with a guess, and do
not refuse it because it is uncertain. Narrowing this guesswork is what the food list and
scale integration exist to do over time.

**4-W. Whole-food path (no protein panel).**
When there is no declared protein, estimate phe directly from the ingredients as whole foods:
   - Apportion the serving grams across the listed ingredients by **weight share** (ingredient
     order = descending weight; absent other information, give earlier items more mass).
   - For each ingredient, use its **phe per 100 g** as a whole food (from the food-list
     reference / your knowledge of that food), and compute
     `phe_ingredient = phe_per_100g × grams_of_that_ingredient / 100`.
   - `recipe_factor_mg_per_serving = Σ phe_ingredient`.
   Then continue to step 5. Record each ingredient in `ingredients_considered` with
   `phe_source_class: "whole food"`.

**5. Anchor to the panel serving.**
`recipe_factor_mg_per_serving` is the phe for exactly one labeled serving
(`serving_size_g`).

**6. Scale to the portion eaten.**
`phe_mg = recipe_factor_mg_per_serving × (portion_g / serving_size_g)`. If the user gives
the portion as "1 serving", `portion_g = serving_size_g`.

**7. Return the number and the working.**
Emit the JSON object in the contract. Nothing after it.

## Worked example (shape only — do not treat as ground truth)

Label: serving 30 g, protein 1.5 g, ingredients "rice flour, sugar, salt". Portion eaten 45 g.
- Step 1: protein 1.5 g ≤ 2 g → countable.
- Step 2: rice flour carries phe; sugar and salt are `none`.
- Step 3: rice flour → `cereal protein`.
- Step 4: rice flour is the only phe-bearing ingredient → `est_share` 1.0; recipe factor =
  1.5 g protein × 1.0 × (phe per g of cereal protein).
- Steps 5–6: scale the per-serving factor by 45/30 = 1.5.
- Step 7: return `phe_mg`, the recipe factor, and the breakdown.

## Notes for operating conditions

Work from the label text you are given. If input is a photo, read serving size, protein per
serving, and the full ingredients list before applying the rubric. Under poor conditions
(e.g. a partial or blurry panel), if a required field is missing, follow rule 5 — report what
is missing rather than guessing. Do not spend extra reasoning inventing precision the label
does not support; apply the rubric and return.
