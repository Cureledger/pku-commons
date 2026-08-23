# Orlando, Florida — city method

**city_id `orlando-fl-us` · v0.1 · 2026-08-23 · no menus captured yet**

Orlando is not a bigger Asheville. It is a different problem, and the difference is worth more to
this project than the Asheville corpus is.

---

## Why Orlando earns priority over any other US city

Two structures exist here that exist nowhere in Asheville:

**1. Chain density → legally mandated protein numbers.** FDA's menu labeling rule covers chains of
20+ locations and requires written nutrition information including protein, on request. Orlando's
tourist corridor is one of the densest concentrations of qualifying chains in the United States.
That means dish-level protein in grams, which the phe estimator can convert directly. Asheville is
independents and gives us none of this.

**2. Theme-park operators → published accommodation policy naming PKU.** Walt Disney World's
Special Dietary Requests page directs guests on a "medically-restrictive diet (such as very low
protein)" to contact the Special Diets team for a request form, no sooner than 14 days before
arrival, after which the team helps navigate dining and may give restaurants advance notice.
Third-party coverage of the program lists PKU by name among requests requiring advance contact.
Victoria & Albert's is handled by a separate dedicated line.

Both structures are *readable*. No phone calls, no chef relationships, no waiting on goodwill.

---

## Award layer

MICHELIN Guide Florida, 2026 edition. Orlando's tally as published by the destination marketing
organization: **7 Stars, 14 Bib Gourmands, 41 Recommended** — 62 venues, up from 59 in 2025 with
six added for 2026.

Provenance caveat: that breakdown comes from the destination marketing organization and 2025-2026
press, not from guide.michelin.com, which returns 403 to non-browser clients. The internal
arithmetic is consistent (7+14+41=62) and the 59-in-2025 figure corroborates the direction, but the
62 is **one source's tally, not a verified count**. Reconcile against the guide before publishing
it.

Known and unresolved, do not paper over:
- **"7 Stars" is stars, not restaurants.** Sorekara holds two, so the starred restaurant count is
  lower than seven. Resolve per restaurant before publishing a count.
- Michelin's current word for the non-starred, non-Bib tier is **Selected**. Florida coverage and
  the DMO both still write "Recommended." Store the verbatim label per record and do not
  normalize press usage into the registry.

Named and citable from coverage of the 2025 and 2026 selections: Sorekara (two stars, chef William
Shen; GM Austin Joseph took the 2025 Service Award), ÔMO by Jônt (one star, chef Ryan Ratino;
sommelier Juan Valencia took the 2026 Sommelier Award), Victoria & Albert's (one star, at Disney's
Grand Floridian), Soseki (one star), Kaya (Recommended, **Green Star** three years running
2024–2026, chef Lordfer Lalicon), and Bib Gourmands including Domu, The Ravenous Pig, Otto's High
Dive, Z Asian, Bánh Mì Boy, Bombay Street Kitchen, Coro, Isan Zaap, Norigami, Smokemade Meats +
Eats, The Strand, Sushi Saint, Taste of Chengdu, UniGirl, Zaru.

**Victoria & Albert's is the structural curiosity of this city**: a Michelin-starred restaurant
*inside* a theme-park resort. The award layer and the operator layer overlap on one record, which
is precisely why the registry needs `operator` as a separate field rather than folding it into
notes.

---

## What is new in the schema

`operator` — a corporate dining program that a restaurant belongs to. Needed because Tier 2
accommodation attaches to the operator and inherits down to every venue it runs. Without it, a
single published Disney policy would have to be copy-pasted onto dozens of rows and would go stale
in dozens of places at once.

`disclosure_regime` — `us_independent` | `us_chain_20plus` | `eu_allergen` | `unknown`. Decides
which extractor runs and how a blank cell should be read. See `../METHODOLOGY.md` Determination 2.

---

## Capture order

1. **Chain nutrition sheets first.** Highest data quality in the whole project and no relationship
   required. Pull the published protein-per-item tables for qualifying chains in the tourist
   corridor. This is the only Orlando work that produces numbers rather than counts.
2. **Operator policies second.** Disney, Universal, and the large resort groups. One capture per
   operator, cited by URL, inherited by every venue. Cheapest accommodation coverage available
   anywhere in this project.
3. **Michelin 62 third**, as the Asheville method: census on menu prose, Regime A rules, no
   inference from silence.
4. **Local lists fourth**, using the category-harvest map. Orlando's own reader polls and food
   press replace Asheville's Best of WNC.

That order is deliberately the inverse of Asheville's. In Asheville the award list was the only
tractable starting point. Here it is the *least* informative of the four.

---

## Camouflage note

Orlando's dominant service format is counter service at scale — theme-park quick service, food
halls, resort marketplaces. On the camouflage axis that is close to ideal: ordering a plain baked
potato at a counter draws no attention whatever, and nobody at a quick-service window is watching
what anyone else ordered. The city that looks least like fine dining may be the easiest place in
the world to eat quietly on a low-protein diet.

Untested. Registered here as an expectation, not a finding.

---

## What this simplifies, and what that hides

1. **Chain coverage inside Regime B is unmeasured.** "Available on request" is a legal obligation
   to hold the data, not a promise it is on a website. Some chains publish full tables; some make
   you ask in the store. I do not yet know the split.
2. **Theme-park pricing and gating are not modeled.** A published accommodation policy inside a
   park requires park admission to use. An A4 you must buy a ticket to reach is not the same good
   as an A4 down the street, and the registry currently has no way to say so.
3. **The 62 count comes from the destination marketing organization**, not from Michelin's own
   site, because guide.michelin.com returns 403 to non-browser clients. It is corroborated by
   press but should be reconciled against the guide itself by someone with a browser.
4. **Orlando is a tourist city and the corpus will reflect that.** Menus in the tourist corridor
   are not the menus residents eat from. A census weighted to International Drive would describe a
   place no local recognizes.
5. **Operator policies are written for allergy, and PKU is not an allergy.** Disney's program is
   unusual in naming low-protein diets at all. Most operator allergy programs will be irrelevant
   to us while looking relevant, and the "gluten-free is not low-protein" trap applies with full
   force to every one of them.
