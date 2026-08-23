# Copenhagen for ESPKU, October 2026

**Written 2026-08-23. Roughly two months of lead time.**

This is a scope note, not a method change. The Copenhagen method in `METHODOLOGY.md` stands and
starts where every city starts — with the Michelin layer if the city has one, which Copenhagen
emphatically does. What changes is *which subset gets done first*, because there is a date.

## What two months does not buy

- A Danish lexicon reviewed by a native reader. The seed term list in `city.json` is mine and will
  contain errors. Reviewing it properly is not a two-month-and-also-everything-else task.
- Verified accommodation for 21 restaurants. Chef-tier verification is one conversation per
  kitchen, and a conversation in Danish about a diet the chef has never heard of is not a
  five-minute call.
- A capture pipeline for Danish menu platforms. Danish restaurants do not cluster onto Toast and
  Square the way American ones do; the platform map is unknown.

Attempting all three and finishing none is the predictable failure. Pick the subset that survives
being late.

## What two months does buy, in priority order

**1. Proximity, not coverage.** The filter is walking distance from the conference venue and the
delegate hotels. A rough record for a restaurant next door beats a perfect record across the city,
because a delegate with a talk at 14:00 is not taking a train to lunch.

Order the Copenhagen Michelin list *by distance from the venue*, then work down it. Same list, same
method, different sort key.

**2. Menus captured by any means.** Hand transcription counts. A photo counts. Asking at the door
counts. The capture harness already records `human_transcription` as a first-class extraction
method with a source, a timestamp and a hash — it was built for exactly this. The extractor
pipeline is the scalable path; it is not the October path.

**3. The request card, in Danish, translated by a person.** This is the highest-value deliverable
per hour in the entire October scope.

Reasoning: the card works without any of the infrastructure. It works at a restaurant nobody has
censused, in a city with no lexicon, for a delegate who has never used the app. It converts a
difficult conversation into handing over a piece of paper. And a conference is the one setting
where a hundred families are all having that same conversation in the same week, in a language
none of them speak.

Do not machine-translate it. A card that misstates the diet is worse than no card, and "low
protein" translated carelessly can read as a preference rather than a medical requirement.

**4. Nothing else.** Explicitly: no scoring, no Danish lexicon rollout, no accommodation
verification campaign, no app feature. Those are the November-onward Copenhagen project.

## Michelin first, still

To be direct about the ordering question: yes, Copenhagen starts with its Michelin recommendations,
same as Asheville. It has a large starred set and Bib Gourmands, they are citable, and they bound a
starting list. The award layer is the cheapest way to get a defensible first list in any city that
has one.

Two Copenhagen-specific notes on using it:

- **The starred count is unresolved** (sources give 15 to 21 for 2026 — see `METHODOLOGY.md`).
  Irrelevant for October. What matters is which specific restaurants are near the venue, and that
  is a per-record question no tally answers.
- **Bib Gourmand matters more than stars here.** A Bib is Michelin's good-value tier, which
  correlates with à la carte service and a printed menu — both better for a delegate than a prepaid
  tasting menu. The starred set is the more prestigious list and the less useful one for this trip.

## Registered expectation

The tasting-menu prediction in `PRIORS.md` says starred Copenhagen restaurants should show low menu
fit and high accommodation. ESPKU is an opportunity to test it with a sample size no amount of
scraping produces: a few hundred PKU families eating in one city in one week.

**A structured visit report from ESPKU delegates would be the single largest accommodation dataset
this project has ever had.** Worth designing the form before October, even if nothing else ships.

## What this scope note hides

1. **Proximity-first capture produces a geographically biased corpus.** A Copenhagen registry built
   around the conference district describes a conference district. It should say so on its face and
   not be presented as a picture of Copenhagen.
2. **The card is a workaround for missing infrastructure**, and shipping it may reduce the pressure
   to build the infrastructure. Worth it here; worth noticing.
3. **No Danish PKU family or clinician has reviewed any of this.** ESPKU is where to fix that, and
   it is a reason to arrive with questions rather than conclusions.
