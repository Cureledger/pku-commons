# PDAS v0.1 — Phebe Dining Access Scale

Status: draft, unreviewed. Version `v0.1`. Reviewer of record: PLACEHOLDER — unassigned.
Cite as: PKU Commons, *Phebe Dining Access Scale v0.1*, `restaurant-guide/spec/pdas-v0.1.md`.

## 1. What this scores, and what it refuses to score

PDAS scores **a restaurant's legibility and flexibility for a diner on a phenylalanine-restricted diet**. It does not score food quality, and it is not a safety certification. It answers one question: *can this person compose a meal here, and what do they have to ask for?*

PKU is quantitative, not binary. This is the single most important design fact and it separates PDAS from every allergy-rating scheme:

- Cross-contamination is **irrelevant**. A shared fryer, a shared grill, a trace of parmesan on the pass — none of it matters. There is no immune reaction. There is only a milligram count.
- What matters is **milligrams of phenylalanine, per portion, as actually served**.
- Therefore the atomic unit of this system is a **dish-level phe estimate with an uncertainty interval**, and a restaurant score is a *rollup* of those estimates. PDAS never emits a "contains protein: yes/no" flag, and any implementation that does has misunderstood the problem.

A corollary that is easy to miss: a restaurant can be excellent for PKU and terrible for a peanut allergy, and vice versa. Do not import allergy heuristics.

## 2. Why three axes and not one ladder

The originating intuition was a single four-rung ladder: barbecue and charcuterie at the bottom, then steakhouses, then naturally-accommodating menus, then kitchens that will make a low-protein substitution on request. That ladder is correct about the world. It is wrong as a *model*, because it multiplies two independent variables into one number, and the two failure modes it produces are the two you hit most often:

- A barbecue joint whose pitmaster will cheerfully boil the low-pro pasta you hand him. Bottom rung. Actually a good dinner.
- A tasting-menu restaurant with a gorgeous vegetable-forward menu and a no-substitutions policy. Third rung. A disaster.

The two variables are: **what is printed on the menu**, and **what the kitchen will do**. They are close to orthogonal, they come from different sources, they update on different clocks, and only one of them is computable at scale. So PDAS separates them.

- **M — Menu Fit (0–4).** Derived from menu text by machine. Updates when the menu changes.
- **A — Accommodation (0–4).** Derived *only* from contact with the restaurant. Never inferred. Updates when someone asks, and expires.
- **C — Confidence (0–3).** How much either of the above should be believed, given menu age, source type, and verification state.

The original four archetypes are the **diagonal** of the M×A grid. That is why they felt like one ladder. Splitting the axes buys three things: M is computable from scraped menus, A is the axis that outreach can actually *move*, and the high-A/low-M restaurants — the pitmaster with the pasta pot — become findable instead of invisible.

## 3. The phe budget is a distribution, not a number

A "safe dish" is meaningless without a budget, and there is no single PKU budget. Daily tolerance across the treated population spans roughly an order of magnitude, and it moves with age, genotype, sapropterin response, and pegvaliase status. Collapsing that into one threshold would erase the population the tool serves.

So M is computed **once per diner profile** and stored as a vector. Three named profiles, v0.1:

| Profile | Daily phe budget | Single restaurant meal budget | Typical population |
|---|---|---|---|
| `TIGHT` | 200–300 mg | **60 mg** | classic PKU, young child, strict management |
| `MID` | 400–600 mg | **120 mg** | classic PKU, older child/adult, good control |
| `WIDE` | 1000+ mg | **350 mg** | sapropterin-responsive, pegvaliase-treated, mild HPA |

Meal budget assumes the restaurant meal is the largest of three daily eating occasions and takes ~40–50% of the day's allowance, leaving room for formula and home food. It is a planning number, not a prescription.

`M_display` defaults to `MID`. The other two are always computed and always available. A restaurant page that shows only one M is out of spec.

Profile boundaries are a v0.1 placeholder awaiting clinician review. They need a dietitian of record before this is presented as guidance. The *shape* — a vector, not a scalar — is not a placeholder and should not be collapsed in later versions.

## 4. Axis M — Menu Fit (0–4)

Machine-derivable from menu text plus the dish-level phe estimates. Computed per profile.

### 4.1 Computed inputs

**`anchor`** — does a low-phe calorie anchor exist? This is the load-bearing input, because a PKU meal out is built around a starch or fat base that carries the calories. An anchor is a dish or side, available as served or with at most one named modification, whose median estimated phe is ≤ 25% of the profile's meal budget, and which can function as a plate base.

Preparation decides this, not the ingredient name. Concretely:
- plain boiled, roasted, mashed (water/oil) or baked potato — anchor
- fries — anchor **only if** not beer-battered, not breaded, not flour-dusted. Many kitchen fries are dusted; this is unknowable from menu text and must be marked `anchor_uncertain`.
- rice, grits, polenta, masa/arepa, corn tortilla — anchor if not cheese-finished, or if cheese can be plated on the side
- mashed potato made with milk and butter — anchor, but the dairy must be counted, not ignored
- bread, pasta, couscous, farro, quinoa — **not** an anchor as served (wheat and quinoa are meaningful phe)
- salad — never an anchor. It is not calories.

**`n_safe_as_served`** — count of dishes whose median estimate ≤ meal budget **and** whose upper interval bound ≤ 1.5 × meal budget. The second condition is what keeps a wide, badly-constrained estimate from being counted as safe.

**`n_safe_with_mods`** — count of dishes that clear the same test after at most **two** named modifications, drawn from a closed list: omit cheese; omit nuts/seeds; omit meat/fish; sauce or dressing on the side; substitute a known anchor for the dish's starch; halve the portion of one named component.

**`n_distinct_anchors`** — count of distinct anchor dishes. Two matters more than one: one anchor is a single point of failure on a night when it is off the menu.

**`plausible_vegetable_entree`** — is there at least one vegetable-forward dish substantial enough to be the centre of a plate, rather than a garnish? This is what separates "I ordered dinner" from "I ordered four sides."

**`format`** — `a_la_carte` | `partial_fixed` | `tasting_only`. Tasting-menu-only **caps M at 2**, regardless of how the individual courses score, because the diner cannot choose. The cap is lifted only by a verified A ≥ 2, and lifting it changes A, never M.

### 4.2 Rubric

| M | Name | Condition |
|---|---|---|
| **0** | Cannot eat | no anchor, `n_safe_as_served` = 0, `n_safe_with_mods` = 0 |
| **1** | Snack, not a meal | ≥1 item clears with mods, but no anchor, or the only anchor is a side and no composable meal exists |
| **2** | Thin meal | anchor present, ≥1 safe as served, a composable meal exists but is ≤2 items or repetitive |
| **3** | Real meal | anchor present, `n_safe_as_served` ≥ 3, `n_safe_with_mods` ≥ 3, multi-course meal composable from the printed menu |
| **4** | Order like everyone else | M3 conditions, plus `format = a_la_carte`, plus `n_distinct_anchors` ≥ 2, plus `plausible_vegetable_entree` |

M4 is deliberately hard. It means the diner reads the same menu as the table and orders off it without a conversation.

## 5. Axis A — Accommodation (0–4)

**A may only be set from contact with the restaurant.** Not from menu text, not from cuisine type, not from a review, not from the presence of an allergen matrix, not from a model's opinion. An unverified restaurant has `A = null` and `A_status = "unverified"`. `null` is not `0`; `A = 0` is a finding, and it requires a source like every other finding.

| A | Name | What the restaurant has agreed to |
|---|---|---|
| **0** | Fixed | Will not alter dishes and cannot reliably itemise ingredients. A real, recorded answer. |
| **1** | Transparent | Will answer ingredient questions accurately, including on request to the kitchen. No changes to dishes. |
| **2** | Flexible | Will make omissions and substitutions from existing mise en place: cheese off, sauce on the side, swap the starch. |
| **3** | Composing | Will plate a composed off-menu vegetable-and-starch entrée; scratch kitchen; will report component **gram weights** on request. |
| **4** | Partner | Will cook guest-supplied or house-stocked low-protein product (pasta, bread, baking mix) to a documented procedure, **and** holds a standing accommodation note so no future diner has to re-explain. |

A4 is the target of the whole outreach programme. Note what it requires and what it does not: it does **not** require the restaurant to source anything. Pre-positioning a case of low-pro pasta with a kitchen converts an A0 restaurant to A4 without asking the chef to solve a procurement problem. That is the cheapest tier jump available and it is a logistics move, not a persuasion move.

Every A value carries: `verified_by`, `verified_utc`, `method` (`email` | `phone` | `in_person` | `restaurant_submitted`), `evidence` (quote or note), and `expires_utc` = `verified_utc` + 180 days. On expiry, A reverts to `unverified` and the badge goes dark. Expiring badges are the forcing function that keeps this alive after the initial push — the same mechanism the living food list uses.

## 6. Axis C — Confidence (0–3)

C governs whether M should be shown at all.

`source_rank`: `restaurant_confirmed` 3 · `structured_platform` 2 · `human_transcription` 2 · `pdf_or_vision` 1 · `social_post` 0

`age_penalty` on menu snapshot age: ≤30 d → 0 · 31–90 d → −1 · 91–180 d → −2 · >180 d → **C = 0 regardless**

`C = clamp(source_rank − age_penalty, 0, 3)`

| C | Meaning | Display rule |
|---|---|---|
| 0 | Stale or unsourced | **Do not show M.** Show "menu too old to score" and the capture date. |
| 1 | Low | Show M greyed, with the snapshot date adjacent. |
| 2 | Good | Show M normally with the snapshot date. |
| 3 | Restaurant-confirmed, recent | Show M with the verified badge. |

**M is never displayed without C.** A score without provenance is precisely the failure the Commons exists to correct; the restaurant guide does not get to reintroduce it.

## 7. The never-infer list

These may **not** be concluded from menu text. Each is a real error a language model will make unprompted.

1. That a kitchen will substitute anything. That is axis A.
2. That "vegetarian" implies low phe. Legumes, tofu, seitan, cheese and nuts are among the highest-phe foods on any menu. Vegetarian dishes are frequently *worse* than a plain potato side.
3. That "gluten-free" implies low protein. GF baking leans on almond, chickpea and soy flour — often **higher** phe than wheat. This inference is actively dangerous and it is the most common one.
4. That "vegan" implies low phe. See 2 and 3.
5. That an ingredient absent from the menu description is absent from the dish. Menu prose is marketing, not a recipe. Butter, stock, cheese finishes and flour thickeners are routinely unlisted.
6. That fries are not flour-dusted or batter-coated.
7. Portion size. Unless a weight is printed, portion is an assumption and must enter the estimate as an interval, not a point.
8. That a dish is unchanged from a previously captured menu with the same name. Recipes drift seasonally; the name is not the dish.

Anything on this list that a pipeline needs must become a **question to the restaurant**, which is why the chef card exists and why outreach is not optional.

## 8. Composite: no single number

PDAS does not multiply M, A and C into one score. The triple is the score. For sorting and filtering only, a derived ordinal is permitted:

```
if A verified:  tier = min(M, A)          # you can only do what BOTH allow
else:           tier = M, flagged "kitchen unverified"
```

`min` is the correct operator: a menu you cannot get modified is bounded by the menu, and a willing kitchen with nothing to work from is bounded by the pantry. `tier` never appears without the flag, and the underlying triple is always one click away.

## 9. Worked examples

Constructed to exercise the rubric, including the two cases the single-ladder model gets wrong. Numbers are illustrative pending the real corpus.

### 9.1 Barbecue / charcuterie — the archetype the ladder ranks last
Menu: smoked meats by the pound, sausage, brisket, ribs; sides of mac and cheese, baked beans, coleslaw, hush puppies, fries, collards.
- anchor: fries — `anchor_uncertain` (dusting unknown); collards greens, low phe but not calories; hush puppies are corn but bound with egg and milk
- `n_safe_as_served` (MID): 2 (collards, plain slaw dressing-on-side)
- `n_safe_with_mods`: 3 · `n_distinct_anchors`: 0–1 · vegetable entrée: no · format: à la carte
- **M(MID) = 1.** Snack, not a meal. Matches the intuition.
- **But:** a pitmaster with a pot of water and your box of low-pro pasta is **A4**. `tier = min(1, 4) = 1` on the printed menu — and the restaurant page shows "M1/A4: bring your own pasta, they will cook it." **That is a good dinner, and the single ladder cannot express it.**

### 9.2 Old-style steakhouse — the ladder's second rung
Menu: dry-aged cuts, creamed spinach, baked potato, onion rings, wedge salad, sautéed mushrooms.
- anchor: baked potato — clean, unambiguous, and the plate can be built on it
- `n_safe_as_served` (MID): 3 (baked potato, mushrooms, wedge without blue cheese and bacon → with mods)
- `n_distinct_anchors`: 1 · vegetable entrée: no · format: à la carte
- **M(MID) = 2.** M(TIGHT) = 2 (the potato still clears 60 mg); M(WIDE) = 3.
- The ladder's instinct — "you're stuck with sides" — is exactly right, and the vector shows it is a *thin* meal rather than an impossible one.

### 9.3 Naturally accommodating — Spanish tapas
Menu: patatas bravas, pan con tomate, escalivada, pimientos de piquillo, espinacas con pasas, croquetas, jamón, tortilla española.
- anchor: patatas (potato), plus a second in the potato of the tortilla → `n_distinct_anchors` = 2
- `n_safe_as_served` (MID): 5+ · `n_safe_with_mods`: 7 · vegetable entrée: yes (escalivada, espinacas) · format: à la carte by design
- **M(MID) = 4.** No modification, no conversation, no special request. The diner orders like everyone else.
- This is why à la carte format is an M4 gate: the format itself is the accommodation.

### 9.4 Low-protein on request — and the tasting-menu trap
Restaurant X: seven-course tasting menu, vegetable-forward, no substitutions.
- Every course individually vegetable-heavy, several would clear the budget
- format: `tasting_only` → **M capped at 2**
- A: contacted, will not alter the progression → **A = 0** (recorded, not inferred)
- `tier = min(2, 0) = 0`. **The ladder scores this a 3. It is a 0.**

Restaurant Y: same menu, but the chef will swap two courses and cook supplied low-pro pasta.
- **A = 4** → cap lifted, `tier = min(3, 4) = 3`.
- Same printed menu, opposite outcome. The A axis is the entire difference, and it is invisible to any scraper.

## 10. What v0.1 simplifies, and what that hides

Required by `AGENT_DIRECTIVE_do_not_flatten.md`.

1. **Three profiles stand in for a continuous tolerance distribution.** Real tolerance is continuous and individual. Three buckets under-serve diners at the edges — particularly a very young child below `TIGHT`. Mitigation: profiles are a display convenience over per-dish mg estimates, which are stored raw. A future version should accept a user's own mg budget and recompute. The dish estimates do not need to change for that to work.
2. **Modification count (≤2) is a proxy for social cost.** Two modifications at a counter-service window and two at a tasting menu are not the same ask. Not modelled in v0.1.
3. **Portion uncertainty is per-dish, not per-restaurant.** Real portion variance is partly a house trait — some kitchens plate heavy. Currently absorbed into the dish interval, which understates correlated error when a diner orders several dishes at the same restaurant. This inflates apparent confidence in a multi-dish meal. Flagged, not fixed.
4. **`n_safe_*` counts weight all dishes equally.** A safe dessert and a safe entrée both count 1. This flatters dessert-heavy menus. Mitigated in part by the `plausible_vegetable_entree` gate on M4.
5. **A is a single ordinal over a set of distinct capabilities.** "Will report gram weights" and "will cook supplied pasta" are different things and A3/A4 orders them by assumption. If outreach shows kitchens commonly do one without the other, A must become a capability set rather than a ladder. Watch for this in the first ten verifications.
6. **C does not model source disagreement.** Two sources with different menus for one restaurant is currently unrepresented; the newer wins. It should widen the interval instead.

## 11. Interfaces

- Dish estimates come from the existing PKU Commons phe-estimator (`../phe-estimator/SKILL.md`) and the living food list (`../food-list/`). PDAS **does not** contain an estimator. Any implementation that grows a second parallel estimator has created exactly the divergence the Commons exists to prevent.
- Restaurant dishes are the hardest case in phe estimation: composite, unweighed, unlabelled. That makes them excellent benchmark material. When a chef supplies a real recipe with gram weights, that is **ground truth for a hard case** and it belongs in `../benchmark/testset/`. Outreach feeds the benchmark; this is the flywheel, not a side effect.
- Review follows `../docs/PEER-REVIEW.md`. An M value is Layer 2 (an estimate — prove it with a number). An A value is Layer 1 (knowledge — cite an authority, name a reviewer of record, version it).
