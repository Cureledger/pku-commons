# City roadmap

**v0.2 · 2026-08-23**

Cities are chosen by where PKU families travel — conferences, camps, family trips. **Disclosure
regime is a method note, not a sequencing input**: it tells you which extractor to run once a city
is on the list. It does not reorder the list.

Every city starts the same way Asheville did: award layer first if one exists, then local lists,
then community submissions.

> v0.1 of this file reordered these cities by regime and pushed Brisbane early because it has no
> award program. That inverted the geography for the agent's convenience. Corrected.

## Live

| city | id | award layer | status |
|---|---|---|---|
| Asheville, NC | `asheville-nc-us` | MICHELIN American South, 15 venues | **299 dishes / 10 restaurants captured**; 62 in registry |
| Orlando, FL | `orlando-fl-us` | MICHELIN Florida 2026, ~62 venues (one source) | method written, no capture |
| Copenhagen | `copenhagen-dk` | MICHELIN Nordic, starred count unresolved (15–21) | method written, **ESPKU October 2026** |

## Event anchors — these set the dates

**ESPKU, Copenhagen, October 2026.** Roughly two months out. That is the nearest hard date in the
project and it changes Copenhagen from a research city into a deadline. Two months is not enough to
build a Danish lexicon, capture 21 restaurants, and verify accommodation with kitchens.

What a delegate can actually use in October, in priority order:

1. **Restaurants walkable from the conference venue and the delegate hotels.** Proximity is the
   whole filter. A perfect record for a restaurant across the city is worth less than a rough one
   next door.
2. **Menus captured however possible** — by hand, by photo, by asking. The extractor pipeline is
   the scalable path; it is not the October path.
3. **The request card in Danish.** One printed card that explains a low-protein diet and asks a
   specific question. This is the highest-value October deliverable per hour spent, and it needs a
   native-speaker translation, not a machine one.

Michelin still comes first in Copenhagen, exactly as in Asheville. But the ordering *within* the
Copenhagen list should be by distance from the venue, not by star count.

**MDDA annual meeting, Gold Coast, Queensland.** Dates not yet confirmed.

Gold Coast is **not** Brisbane — it is a separate city roughly 70 km south, with its own
restaurants. A Brisbane registry would not serve an MDDA delegate. Added as its own `city_id`;
Brisbane stays on the list separately.

## Roadmap, in Nina's order

| city | id | award layer | blocking gate |
|---|---|---|---|
| Brisbane | `brisbane-au` | none — no Michelin presence in Australia | map the AU disclosure regime |
| Gold Coast | `gold-coast-au` | none | confirm MDDA dates and venue |
| Dublin | `dublin-ie` | MICHELIN Ireland | none — English-language, EU allergen regime |
| Paris | `paris-fr` | MICHELIN France | French lexicon set |
| London | `london-gb` | MICHELIN Great Britain & Ireland | verify post-Brexit UK regime |

The two Australian cities have no award layer to start from. That is not a reason to move them —
it just means they start at the local-list and community layers, which is what the open registry
was built for.

## Per-city gate, before any capture

1. **Award layer identified** if the city has one, with counts as published — stars separate from
   restaurants, verbatim tier labels, conflicts recorded rather than averaged.
2. **Disclosure regime recorded** in `city.json`. Determines which extractor runs and how to read a
   blank cell. Not assumed from the country.
3. **Lexicon covers the menu language**, native-reader reviewed. Hard gate — a 0% match rate
   recorded as "no protein sources named" is a tooling gap masquerading as a finding about food.
4. **Priors written and dated before the first capture.**
5. **Operator entities identified** where corporate dining programs exist.

## What this simplifies, and what that hides

1. **Regime grouping still saves engineering** — Dublin, Paris and London share one extractor
   design. That is a reason to *build* in that order, not to *visit* in that order.
2. **Cities track conference and camp locations in wealthy countries.** The places where a
   low-protein diet is hardest to eat are not on this list. A guide that serves the trips families
   actually take beats a globally balanced one nobody uses.
3. **Only Asheville was chosen by a PKU family who lives there.** Every other city is somewhere
   this community visits, which is a different and shallower kind of knowledge.
4. **Conference-adjacent capture is geographically biased on purpose.** A Copenhagen registry built
   around the ESPKU venue describes a conference district, not a city, and should say so.
