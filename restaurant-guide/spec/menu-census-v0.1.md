# Menu Census v0.1

Status: draft, unreviewed. Version `v0.1`. Reviewer of record: PLACEHOLDER — unassigned.
Cite as: PKU Commons, *Menu Census v0.1*, `restaurant-guide/spec/menu-census-v0.1.md`.

## 1. What this is, and the line it does not cross

The census records **which ingredient categories are named in each dish on a menu, and counts them.** That is the whole scope.

It does not score. It does not rate. It does not apply a phenylalanine budget, a threshold, a percentage of a daily allowance, or a suitability judgment. It does not rank restaurants against each other, and it does not say a dish is safe, unsafe, good or bad.

That line is deliberate and it is the main design decision in this document. The suitability scale is defined by the project owner **after** this corpus exists. A threshold invented before the data would silently decide what the data appears to say: pick 120 mg and tapas looks workable, pick 60 mg and the same menu looks impossible. The scale has to be argued from the corpus, not imposed on it.

An earlier draft did impose one. It is preserved, unused and uncited, in `deferred/` — kept only because the structural argument inside it (what the kitchen *will do* is a separate axis from what the menu *says*, and it is only knowable by asking) survives and should inform whatever scale replaces this.

## 2. What the census is for

Two uses, both served by raw counts and neither needing a score.

**Evidence of the customer problem.** The counts are the argument. "This menu has 34 dishes; 6 name no meat; 3 name no meat and no legume; 2 name a potato or starch; 1 names no protein source of any kind" is a far stronger statement to a chef, a conference room, or a journalist than any rating, because the chef can check every number against their own menu in about a minute. A rating invites a dispute about the rating. A count invites a look at the menu.

**A baseline that can be re-measured.** The census is repeatable, so the same menu measured in August 2026 and June 2027 produces a comparable pair of numbers. That is what makes an accommodation campaign measurable rather than anecdotal.

## 3. The one inference rule

**A term match means the ingredient is NAMED on the menu. A non-match means nothing at all.**

Menu prose is marketing copy, not a recipe. Butter, stock, cream finishes, cheese garnishes, flour thickeners, egg washes and flour-dusted fries are routinely unwritten. A dish whose description names no protein source is a dish whose description names no protein source — not a dish without protein.

Every row carries `completeness: "text_only_unknown"` and every restaurant rollup carries `absence_is_not_evidence: true`. These fields exist so the caveat travels with the data into the app, the CSV, and any figure, instead of living in a footnote that gets dropped on the second copy-paste.

Consequence: the census generates **questions for the restaurant**, and the unwritten-ingredient problem is most of why outreach is not optional.

## 4. Categories

17 categories over 947 terms (`data/ingredient_lexicon.json`, lexicon v0.2), grouped by role:

**Protein sources** — `animal_muscle`, `cured_meat`, `dairy`, `egg`, `legume`, `nut_seed`

**Starches** — `wheat_grain`, `pseudo_grain`, `potato`, `rice`, `corn`, `other_starch`

**Other** — `vegetable`, `fruit`, `fat_oil`, `sugar_sweet`, `herb_spice_acid`

Two things to note about the grouping.

`legume` is separated from `vegetable`, and both are separated from `dairy`, `egg` and `nut_seed`. This is the distinction that matters and that generic "vegetarian" filters destroy: a chickpea stew and a plate of roasted eggplant are both vegetarian and they are not remotely the same thing. The census reports them separately and folds nothing.

Starches are split six ways rather than lumped. Potato, rice, corn and cassava behave very differently from wheat and quinoa, and a menu with three wheat starches and no others is a different situation from one with two potato preparations. The rollup reports the breakdown, not just a total.

## 5. Per-dish output

Each dish yields: the matched terms per category, the category list, any ambiguous terms hit, any free-from markers found, and the completeness flag. Plus observable predicates, each a statement about named terms and nothing more:

| Predicate | Reads as |
|---|---|
| `names_meat` | a meat, poultry, fish, shellfish or cured-meat term appears |
| `no_meat_named` | no such term appears |
| `no_meat_no_legume_named` | no meat term and no legume term appears |
| `names_dairy` / `names_egg` / `names_nut_seed` | reported **separately**, never folded into the above |
| `names_no_protein_source_at_all` | no term from any of the six protein-source categories appears — the strongest statement the text supports, and still not proof |
| `starch_categories` | which of the six starch families are named |
| `names_vegetable` | a vegetable term appears |

## 6. Per-restaurant rollup

Counts only, always with `n_dishes` as the denominator so a count is never read without the menu size:

`n_dishes` · `n_no_meat_named` · `n_no_meat_no_legume_named` · `n_names_potato_or_starch` · `n_names_vegetable` · `n_names_no_protein_source_at_all` · `n_no_meat_no_legume_no_dairy_no_egg_no_nut` · `starch_dish_counts` (per family) · `protein_source_dish_counts` (per family) · `n_dishes_with_ambiguous_terms` · `n_dishes_no_terms_matched`

The last two are quality metrics on the census itself. A restaurant with 12 unparseable dishes has a capture problem, and that must be visible rather than reported as a low count of anything.

There is no total, no index, and no composite. Adding one would be a scale, and the scale is not mine to write.

## 7. Known limitations

1. **Absence is not evidence.** Section 3. The largest limitation and unfixable by text analysis; only the restaurant can close it.
2. **No portion or quantity.** The census counts named ingredients, never amounts. "Cheese" is recorded identically whether it is a dusting or a half-pound.
3. **Ambiguous terms are recorded, not resolved.** `tortilla` reads as corn, wheat or egg-and-potato depending on cuisine; `chips` as fries or crisps; `gnocchi` is genuinely both potato and wheat. Multi-category assignment plus an `ambiguous_terms` flag is the intended behaviour. Resolving them needs the restaurant or a human reviewer.
4. **Free-from suppression is shallow.** "Gluten-free" suppresses `wheat_grain`, "vegan" suppresses animal categories. Real menus phrase this many more ways than the marker list covers, and a GF dish frequently substitutes almond or chickpea flour — which the census will record only if named. Suppression is recorded in `free_from_markers` so it can be audited.
5. **English-centric with partial Spanish, Italian and Amharic coverage.** Addissae and Cúrate will expose gaps. Fixing them is a lexicon PR, which is the intended contribution path.
6. **Multi-category by design.** `gnocchi` firing both potato and wheat is correct; deduplicating it would lose information.
7. **`n_dishes_no_terms_matched` conflates two causes** — a dish the lexicon cannot parse, and a dish genuinely described without ingredients ("chef's choice"). Not currently separated.

## 8. What v0.1 simplifies, and what that hides

Required by `AGENT_DIRECTIVE_do_not_flatten.md`.

1. **Presence/absence stands in for quantity.** This is the deliberate simplification of the whole census, and it hides the entire magnitude question — which is the question PKU actually turns on. It is acceptable *only* because the census does not claim to assess suitability. The moment a threshold is attached to these counts, this simplification becomes a falsification. That is the strongest reason the scale waits for the corpus.
2. **Binary predicates over a graded reality.** `names_dairy` is true for a butter-basted dish and for a fondue. Reported as one bit. Mitigated by keeping `matched_terms` verbatim so a reviewer can see which term fired.
3. **Dishes are weighted equally in the counts.** A safe dessert and a safe entrée each count 1. A dessert-heavy menu therefore looks better than it eats. No course weighting exists in v0.1 because weighting is a judgment call.
4. **Menu snapshots are point-in-time.** A dish name is not a dish; recipes drift seasonally. Every count is only as current as its snapshot date, which is why the snapshot index and the freshness pipeline are part of the system rather than a nicety.
5. **The lexicon is a fixed list, so coverage is uneven across cuisines.** Spanish and Italian terms are better covered than Amharic. This *systematically undercounts* at the restaurants with the least English-legible menus — the opposite of what the guide should do. Named as a bug, not a footnote.

## 9. Interfaces

- Dish-level phenylalanine estimation, when it happens, goes through the existing PKU Commons phe-estimator (`../phe-estimator/SKILL.md`) and the living food list (`../food-list/`). The census contains no phe values and will not grow an estimator.
- A chef-supplied recipe with gram weights is ground truth for a genuinely hard estimation case, and belongs in `../benchmark/testset/`. Restaurant outreach feeds the benchmark; that is the flywheel.
- Review follows `../docs/PEER-REVIEW.md`. A lexicon term is Layer 1 knowledge: cite it, version it, name a reviewer. A census count is derived and reproducible from the snapshot plus the lexicon version.
