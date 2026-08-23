# Cross-city methodology

**Version 0.1 · 2026-08-23 · applies to every city fork**

Asheville produced a working method. Extending it to Orlando and Copenhagen exposed that three
things I had treated as fixed properties of the problem are actually properties *of Asheville*.
This document records what generalizes and what does not, so a city fork starts from the right
frame instead of copying Asheville's.

---

## Determination 1 — "the Michelin N" is not a unit of work

| city | award-recognized venues | note |
|---|---|---|
| Asheville | 15 | inaugural American South edition, no stars |
| Orlando | ~62 | 7 stars, 14 Bib Gourmand, 41 Recommended (2026 guide) |
| Copenhagen | 15-21 starred | sources conflict; see below. Plus Bibs |

Asheville's 15 was small enough that "do the Michelin list" was a coherent sprint. Orlando's is
four times that and Copenhagen's starred set alone rivals Asheville's entire selection. **A city
plan denominated in "the Michelin list" silently means a different amount of work in every city.**

Corollary: award coverage does not scale with city size, it scales with Michelin's own market
entry. Orlando has a guide because Florida got an edition in 2022 and expanded since; Brisbane has
no Michelin presence at all. A method that requires an award to bootstrap cannot enter those
cities. The open registry already fixed this — recording it here so no fork re-derives it.

**Do not report "N of N confirmed" across cities as if N were comparable.** Report the count and
the edition, per city, with the star/restaurant distinction preserved (see Determination 5).

---

## Determination 2 — the disclosure regime, not the cuisine, decides the method

This is the load-bearing finding of this document. What a menu legally must tell you varies by
jurisdiction, and it changes which layer of the pipeline does the work.

**Regime A — US independent restaurant. Nothing mandated.**
No nutrition disclosure, no allergen disclosure. All you have is marketing prose. This is what
the census was built for: count what the menu *names*, and never infer from silence. Asheville is
almost entirely Regime A.

**Regime B — US chain, 20+ locations. Quantitative protein, on request.**
FDA's menu labeling rule (21 CFR 101.11, compliance date 2018-05-07) applies to chains of 20 or
more locations doing business under the same name with substantially the same menu. Calories go
on the menu board. And critically: <span>businesses must also provide, upon request, written
nutrition information including total carbohydrates, sugars, fiber, and **protein**</span>.

Protein in grams, per standard menu item, legally required to exist in writing. That is not a
census — it is a number. Feed protein grams into the phe estimator's existing
`phe_mg = protein_g × coefficient[phe_source_class]` path and you get a dish-level phe estimate
with the same provenance quality as a packaged food. **Regime B is the highest-value data in this
entire project and it does not exist in Asheville**, because Asheville's restaurants are
independents. Orlando is dense with chains.

**Regime C — EU / UK. Named allergens, mandated, no quantity.**
EU Regulation 1169/2011 requires the 14 major allergens to be declared for non-prepacked food,
including meals sold in restaurants. Cereals containing gluten, milk, eggs, soybeans, nuts,
peanuts, fish, crustaceans, molluscs, sesame, celery, mustard, lupin, sulphites.

Nine of those fourteen are protein sources that matter for phe. This converts the census's
weakest assumption — *a non-match means not named, never absent* — into something much stronger
for those nine categories, because a Danish restaurant is **legally obliged** to declare milk,
egg, gluten, soy, nuts and fish. Silence in Regime C is closer to evidence of absence than
silence in Regime A. Not proof: the obligation is to declare, and compliance varies. But the
epistemic status of a blank cell genuinely differs by jurisdiction, and the census spec must say
so instead of applying one rule everywhere.

No quantity, though. Allergen law tells you *whether* milk is present, never how much. So Regime
C improves the presence/absence layer and does nothing for the magnitude question.

**Consequence for the roadmap.** Group cities by regime, not by continent. Dublin, Paris and
London are all Regime C and share one extractor design. Brisbane is a fourth regime (Australian
allergen declaration under the Food Standards Code) that needs its own check before work starts.

---

## Determination 3 — accommodation has three grantor tiers, not one

The Asheville model assumed one grantor: a chef, reachable by phone, whose answer expires in 180
days because chefs move. That assumption breaks in Orlando.

**Tier 1 — chef.** One kitchen, one conversation. Evidence is a person's word. 180-day TTL,
because staff turnover is the failure mode. This is all of Asheville.

**Tier 2 — operator.** A corporate dining program covering many venues, with a *published
policy*. Walt Disney World's Special Dietary Requests page instructs guests on a
"medically-restrictive diet (such as very low protein)" to email the Special Diets team in
advance for a Special Diets Request Form, and asks that contact come no sooner than 14 days
before arrival; the team then assists with the dining process, which may include giving the
restaurants advance notice. Third-party coverage of the same program lists **PKU by name** among
the requests that require contacting Disney in advance.

Read what that means for this project. A single published corporate policy, citable by URL,
naming our exact condition, covering dozens of restaurants, verifiable without a phone call. That
is an A4 (Partner) on the accommodation axis — reached by *reading*, not by asking. Nothing in
Asheville can be scored that way.

Tier 2 needs its own TTL. A corporate policy does not turn over when a line cook quits; annual
re-check is right, not 180 days. And Tier 2 verification attaches to the **operator**, then
inherits down to every venue that operator runs — the registry needs an operator entity to hang
it on.

**Tier 3 — regulator.** Regime C above. Doesn't expire, isn't revocable by the restaurant, and
tells you about allergens rather than accommodation. Not a substitute for either other tier: a
kitchen that correctly declares milk may still refuse to cook anything differently.

**The rule that survives from Asheville:** none of these three tiers may be inferred from menu
text, cuisine, price, or reviews. What changes is that Tiers 2 and 3 can be established from
*published documents*, which the Asheville method had no category for because Asheville has none.

---

## Determination 4 — a testable prediction about tasting menus

Copenhagen is tasting-menu-dominant. The deferred scale capped menu fit for fixed-format
restaurants, on the reasoning that you cannot compose a plate from a menu with no choices. That
reasoning is still right about *menu fit*.

But the M/A decoupling predicts something counterintuitive, and Copenhagen is the city that tests
it. A prepaid ticketed tasting menu booked weeks ahead means: the kitchen knows exactly who is
coming, how many, and when; the menu is planned rather than reactive; and there is a booking
record with a contact field. Those are the conditions under which a kitchen can *most* easily
prepare something different — the opposite of a walk-in at a busy à la carte restaurant.

**Registered prediction, before any Copenhagen menu is captured:** starred tasting-menu
restaurants in Copenhagen will show low menu fit and *high* accommodation, and the correlation
between the two axes will be negative or absent — not positive. If it comes out positive, the
two-axis model is wrong and should be collapsed.

This is recorded in `cities/copenhagen-dk/PRIORS.md` before capture. A prior written afterward is
not a prior.

---

## Determination 5 — count stars and restaurants separately, always

Sources conflict on Copenhagen in *both* years. For 2025: one gives 30 stars across 18
restaurants, another 30 across 19. For 2026 the spread is wider — a tourism source reports 31 stars
across 21 restaurants while a travel guide published in April 2026 titles its list "15 Amazing
Michelin Star Restaurants in Copenhagen (2026)". A 15-versus-21 gap is not a rounding difference;
it is likely a scope difference (city limits versus greater Copenhagen, or stars-only versus
including Bibs), and I have not resolved which. Orlando's 2026 tally is published as "seven total
Stars" — which is not seven restaurants, because one of them (Sorekara) holds two.

Stars are not restaurants. A three-star restaurant is one row in a registry and three stars in a
press release. Collapsing them produces a count that is wrong in a way nobody notices, and it is
the same error class as flattening Luminosa's Green Star and Bib Gourmand into one label.

Registry rule, already enforced by `test_registry.py`: one row per restaurant, `awards` is a
list, tier labels verbatim. Add: never derive a restaurant count from a star count, and where
sources disagree, record both and mark it unresolved.

---

## What this document simplifies, and what that hides

1. **Three regimes is a coarse cut.** US states add their own labeling rules; the UK diverged
   from the EU after Brexit and added Natasha's Law for prepacked-for-direct-sale food. Treat
   Regime C as "check the specific jurisdiction," not as a settled fact about a country.
2. **The Regime B protein number is total protein, not phenylalanine.** The conversion still runs
   through a phe_source_class coefficient, and that classification step carries all the
   uncertainty it always did. Regime B improves the input, not the model.
3. **"On request" is not "published."** FDA requires the information to exist in writing at the
   establishment. Many chains post it online; some do not. Coverage inside Regime B is unmeasured
   and I should not assume it is complete.
4. **Tier 2 accommodation is a policy, and a policy is not a plate.** Disney's own page says
   restaurants take reasonable efforts and cannot guarantee all requests can be met. A published
   program is strong evidence about *process*, and no evidence at all about what arrives at the
   table on a given night.
5. **Operator-tier verification could concentrate risk.** If one operator covers thirty venues
   and the policy changes, thirty rows go stale simultaneously. Per-chef verification fails
   independently; per-operator verification fails in blocks.
6. **I have not verified the EU allergen obligation against the regulation text**, only against
   its widely-reported content. Before any Copenhagen row is scored on Regime C reasoning,
   someone should read Annex II of 1169/2011 directly.

---

## Interfaces

- Census engine and the one inference rule: `../spec/menu-census-v0.1.md`
- Screening signals, four families: `../spec/signal-taxonomy-v0.1.md`
- Adding restaurants, any city: `../ADDING.md`
- Deferred suitability scale: `../spec/deferred/`
- Per-city method and priors: `orlando-fl-us/`, `copenhagen-dk/`
- Roadmap and regime grouping: `ROADMAP.md`
