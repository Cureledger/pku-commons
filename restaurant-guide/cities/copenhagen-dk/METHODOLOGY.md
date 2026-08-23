# Copenhagen, Denmark — city method

**city_id `copenhagen-dk` · v0.1 · 2026-08-23 · no menus captured yet**

Copenhagen is the first non-US city and the first jurisdiction where the law tells you what a menu
must disclose. It is also the city that tests whether the two-axis model was right.

---

## Why Copenhagen is the right second city

**1. It is the strongest test of the M/A split.** Copenhagen is tasting-menu-dominant at the top
end. That is the format the deferred scale capped for menu fit, and the format the two-axis model
predicts should score *high* on accommodation. If both axes move the same direction here, the
model is wrong. See `PRIORS.md` — the prediction is registered before capture.

**2. Regime C changes what a blank cell means.** EU Regulation 1169/2011 requires the 14 major
allergens to be declared for non-prepacked food, restaurant meals included. Nine of the fourteen
are protein sources that matter for phe: cereals containing gluten, milk, eggs, soybeans, nuts,
peanuts, fish, crustaceans, molluscs. In Asheville a silent menu meant nothing at all. Here, for
those nine categories, a restaurant is *legally obliged* to declare. Silence becomes weak evidence
rather than no evidence.

This is the single most important methodological consequence of leaving the US, and it is recorded
as Determination 2 in `../METHODOLOGY.md`.

**3. The PKU care context is different.** Denmark has national newborn screening and a
concentrated metabolic care system. A city guide here is talking to a population with different
baseline expectations of what a restaurant will do. Not modeled yet, and it should be before any
outreach copy is written.

---

## Award layer

MICHELIN Guide Nordic Countries. **The starred count is unresolved and should not be published
until it is.** What the sources say:

| source | year | stars | restaurants |
|---|---|---|---|
| Copenhagen tourism list | 2026 | 31 | 21 |
| travel guide, published April 2026 | 2026 | — | 15 |
| Wonderful Copenhagen | 2025 | 30 | 18 |
| other Nordic coverage | 2025 | 30 | 19 |

A 15-versus-21 gap for the same year is not a rounding difference. The likely cause is scope —
city limits versus greater Copenhagen, or a curated "best of" subset versus the full starred list —
and I have not resolved which. The 18-versus-19 gap for 2025 is the star-versus-restaurant error
from Determination 5.

Do not smooth these. Record all four, mark unresolved, resolve per restaurant against the guide
itself. **For ESPKU purposes the count does not matter at all** — what matters is which specific
restaurants are near the venue, and that is a per-record question the award tally cannot answer.

Named and citable: Geranium (three stars, chef Rasmus Kofoed, also holds a Green Star), Alchemist
(three stars, chef Rasmus Munk), Jordnær (three stars, chef Eric Vildgaard — promoted in the 2025
Nordic guide), Noma (two stars plus a Green Star, chef René Redzepi), Kadeau (two stars), AOC (two
stars), Alouette (one star), Kong Hans Kælder, Marchal, formel B, Kiin Kiin, Restaurant Silo,
Restaurant Domestic, Iluka, Sushi Anaba, Koan (two stars, chef Kristian Baumann).

Notable structurally: **Copenhagen is dense with Green Stars.** Geranium and Noma both hold one.
A Green Star is awarded for sustainability, and vegetable-forward cooking correlates with it —
which is a camouflage signal, not a dietary-fit signal, and must not be read as the latter.

**The Noma question.** Noma has announced a transition away from ordinary restaurant service. Its
status will change during this project's lifetime. Any Copenhagen registry that hardcodes today's
Noma will be wrong within a year, which is a useful argument for why `awards` carries an edition
and a date on every entry.

---

## Language and the lexicon

The lexicon is English-first with Spanish, Italian and Amharic patches added after Asheville
validation. Danish is entirely absent. Terms that will match nothing today:

`torsk` (cod), `svinekød` (pork), `oksekød` (beef), `kylling` (chicken), `æg` (egg), `mælk`
(milk), `ost` (cheese), `smør` (butter), `rugbrød` (rye bread), `kartofler` (potatoes), `ærter`
(peas), `bønner` (beans), `laks` (salmon), `sild` (herring), `rejer` (shrimp), `hvede` (wheat),
`fløde` (cream), `flæsk` (pork belly), `frikadelle` (meatball), `smørrebrød` (open sandwich).

Two hard problems the Asheville patches did not have:

**Compound nouns.** Danish compounds aggressively — `svinekødsfrikadeller` is one word containing
pork and meatball. Asheville's `compound_substring_terms` pass was built for `shrimpburger` and
will need real work here.

**Non-ASCII characters.** `æ ø å` will break naive matching. The slugifier already folds them
(`slugify` normalizes to ASCII), but the lexicon matcher does not, and that is a bug waiting to
happen.

**Do not capture a Danish menu until the lexicon has a Danish category set.** A 0% match rate
would be recorded as "no protein sources named," which is the worst possible failure of the one
inference rule. This is a hard gate, not a preference.

---

## Regime C — how to use it, and how not to

**Use it for:** the nine allergen categories that are also phe-relevant. A Danish menu or its
allergen sheet that omits milk is meaningfully more likely to be milk-free than an Asheville menu
that omits milk.

**Do not use it for:** quantity. Allergen law says *whether*, never *how much*. Regime C improves
the presence/absence layer and does exactly nothing for the magnitude question that PKU actually
turns on.

**Do not use it for:** the five non-protein allergens (sesame, celery, mustard, lupin, sulphites)
or as a proxy for accommodation. A kitchen that declares allergens correctly may still refuse to
cook anything differently — declaration is a legal duty, accommodation is a choice.

**Confidence still degrades with age.** An allergen declaration is a statement about a menu on a
date. Regime C does not exempt a snapshot from the source-recency rules.

---

## What this simplifies, and what that hides

1. **I have not read Annex II of 1169/2011 directly**, only its widely-reported content. Before
   any Copenhagen row is scored on Regime C reasoning, someone should read the regulation text.
   Denmark may also have national implementing rules I have not checked.
2. **Legal obligation is not compliance.** The rule creates a duty to declare. It does not
   guarantee every restaurant does, or does so accurately. Treating Regime C silence as strong
   evidence would be the same overreach as treating Asheville silence as evidence — just in the
   opposite direction.
3. **The tasting-menu prediction may be confounded by price.** Copenhagen's starred restaurants
   are expensive, and expensive restaurants may accommodate better for reasons unrelated to
   format. Any positive accommodation finding needs a price-matched à la carte comparison before
   it is attributed to the tasting format.
4. **The Danish term list above is mine, not a native speaker's.** It is a starting point that
   will contain errors and will miss the compounds that matter most. It needs review by someone
   who reads Danish menus before it is trusted.
5. **A guide covering only starred Copenhagen restaurants describes a city almost nobody eats in.**
   The award layer here is even less representative than Asheville's, because the price floor is
   higher. The local-list and community layers matter more in this city, not less.
6. **No Danish PKU community input has been sought.** The whole premise is that this serves
   families, and I have written a method for a country whose PKU families have not been consulted.
