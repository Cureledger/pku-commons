# Signal Taxonomy v0.1 — what makes a restaurant taggable

Status: draft, unreviewed. Version `v0.1`. Reviewer of record: PLACEHOLDER — unassigned.
Cite as: PKU Commons, *Signal Taxonomy v0.1*, `restaurant-guide/spec/signal-taxonomy-v0.1.md`.
Machine-readable registry: `data/signal_registry.json` · Detector: `src/signals.py` · Tests: `tests/test_signals.py` (37 assertions)

## 1. The question this answers

How do you screen restaurants for a low-protein diet, worldwide, without a research trip per restaurant and without making a scene at the table?

Awards were the obvious first answer and they are a weak one. They bound a starting list, which is genuinely useful — a closed, externally-defined, citable set is a good way to begin a city. But an award says a kitchen is *good*, and good is not the question. Michelin's selection skews toward expensive, protein-centred, tasting-format restaurants, which are among the hardest cases in this domain. **Award recognition has no established relationship to dietary accommodation, and the guide must never imply that it does.**

So awards are one inclusion criterion among several, stored as citable provenance rather than as the organizing idea.

## 2. Four families

**Curatorial** — third-party recognition. Bootstraps a list, indicates kitchen competence, predicts nothing about accommodation. Coverage is uneven by construction: Michelin covers ~40 destinations, weighted to Europe, Japan and the US coasts. Useless for horizontal coverage of anywhere else.

**Structural** — facts about how the menu and service are *organized*. Is a menu published at all. Do dishes carry ingredient descriptions. À la carte or fixed. How many standalone sides. How many distinct starch families. These are machine-readable, uniform across countries, free to store, and they are the workhorse family.

**Camouflage** — whether ordering the way you need to order looks like how everyone else orders. This is the axis nobody builds and it is often the one that decides whether a meal out is worth attempting.

**Accommodation evidence** — what the kitchen will actually do. Historically this required a phone call, which is why it never scales. Two members of this family turn out to be machine-readable, which is the most useful finding in this document.

## 3. Camouflage: the axis nobody builds

Allergy apps optimize for safety, so they push you toward *announcing* your requirements: tell the server, ask about the fryer, confirm with the kitchen. For PKU that is both unnecessary and counterproductive. Cross-contamination is irrelevant — a trace of parmesan does not matter, only milligrams do — so there is no safety reason to announce anything. What is left is pure social cost, and social cost is why people skip going out.

Signals that lower it, all machine-readable from menu structure:

**Composing your own meal is the house format.** Tapas, mezze, dim sum, izakaya, banchan, small plates. When everyone at the table orders five dishes and shares, ordering five vegetable dishes is invisible. This is the strongest camouflage signal available and it explains something the census will keep showing: the tapas bar is a better restaurant for this than the vegetable-forward tasting menu, despite the tasting menu looking better on paper.

**Counter, kiosk or app ordering.** No server conversation at all. You tap what you want and nobody asks why. Note the trade-off: counter service usually means fewer modifications are possible, so camouflage and flexibility pull against each other here.

**Build-your-own items.** Per-component choice is already a published, priced option, so specifying components is ordinary rather than a special request.

**Vegetables as centre-of-plate dishes.** Removes the "is that all you're having?" moment. Carries a mandatory warning: vegetable-forward does **not** mean low protein. Legume, cheese and nut-heavy vegetarian dishes are frequently the highest-phe items on a menu.

**Kids menu.** Institutionalised plain food, small portions already priced. Weak signal — kids menus are usually breaded and cheese-heavy — but nearly free to collect.

## 4. The finding worth acting on: modifier groups

Accommodation was assumed to require contact. One form of it does not.

Online ordering platforms — Toast, Square, ChowNow, Clover — publish **modifier groups** as structured data: *no cheese*, *dressing on the side*, *substitute a side*, *hold the nuts*. A modifier group is not marketing copy. It is a kitchen capability the restaurant has committed to in machine-readable form. If Toast lets a stranger uncheck cheese at 11pm on a Tuesday, the line cook has a process for a plate without cheese.

That makes it the first accommodation signal that scales without a phone call, and it is uniform across every restaurant on a given platform in any country.

Boundaries, because this is evidence and not proof: it shows the modifier *exists*, not that staff apply it correctly; it covers only dishes sold online, which is often a subset of the dinner menu; and it says nothing about a request the platform has no checkbox for. So a modifier group can raise a restaurant to **evidenced**, never to **verified**. Verification still means someone asked and someone answered on the record, and it still expires after 180 days.

## 5. Structured visit reports: the scaling engine

This is the TripAdvisor analogue, and the unit matters more than the mechanism.

A star rating is worthless here. "4.5 stars" tells a PKU family nothing, because the crowd was answering a different question. What travels is a **structured report**: *asked for the polenta without the cheese, they did it without comment, server brought the gram weight when asked.* That is reusable by the next person and it is checkable.

Properties that make this the engine rather than a nice-to-have: coverage is unbounded and grows with the community rather than with a publisher's travel budget; there is no third-party IP surface, no attribution burden, no takedown exposure, because the data is ours; and it is the only way to populate the accommodation axis faster than the team can make phone calls.

Limits, stated up front: self-selected sample, single-night observation, and staff turnover ages it. So a visit report expires like any other verification, and several agreeing reports are worth more than one.

## 6. What we deliberately do not use

**Crowd star ratings — Google, TripAdvisor, Yelp.** Rejected for two independent reasons, either of which would be sufficient.

The legal one: Google's Places API policies prohibit pre-fetching, caching or storing Places content beyond narrow exceptions. Only `place_id` may be stored indefinitely; coordinates may be cached up to 30 days. Names, ratings and reviews must be requested live. A warehoused rating is a terms violation, and because you cannot amortize a result you are not allowed to keep, every render is another billable call.

The substantive one, which matters more: a crowd rating measures whether a restaurant is *good*. A 4.8-star steakhouse can be unusable; a 3.9-star tapas bar can be excellent. Building on crowd ratings would import a judgment about the wrong question.

What we do keep is `place_id` — storable indefinitely, non-editorial, and it functions as a stable global join key that makes every other data source line up across cities. Keep the identifier, drop the opinion.

**"Gluten-free available" as a proxy for low protein.** The most common and most dangerous wrong inference in this domain. GF baking substitutes almond, chickpea and soy flour, frequently *higher* phe than wheat. An allergen matrix is kept only as evidence that the kitchen tracks ingredients per dish, never as a dietary signal.

**"Vegan" or "vegetarian" as a proxy.** Same error. A vegan restaurant can be the worst option in a city.

**Price tier.** Expensive restaurants are protein-cut-focused, cheap ones starch-heavy. If anything the correlation runs against intuition, and it is too weak either way to be worth a tag.

## 7. No composite

Every signal is an independent, filterable tag carrying its own provenance and its own failure mode. Nothing is summed, weighted, or averaged into an overall number.

Combining them would *be* the suitability scale, and that is deferred by design — see `menu-census-v0.1.md` §1. A weighting invented before the corpus exists would quietly decide what the corpus appears to say.

`signals.tags()` returns a flat list of keys. The app filters on tags. It does not rank.

## 8. Trademark and citation discipline

For any award tag, store and display: program name, tier label **verbatim from the program**, edition or year, and a source URL. Never store or display the program's descriptive prose about a restaurant — the fact of inclusion is not protectable, their review copy is.

Michelin's current term for the non-starred, non-Bib tier is **Selected**. "Recommended" appears in press coverage and in some legislative citations, but it is legacy usage; store the program's own current word. A restaurant holding both a Green Star and a Bib Gourmand holds both — never flatten multiple recognitions into one label.

Referential use only: word mark in plain text, grammatically modifying the restaurant and never naming a Phebe feature; no logos, roundels, plaques or star glyphs; an affiliation disclaimer on every surface where the mark appears; and never in an app name, store listing, ASO keyword field, domain or paid-search bid.

## 9. What v0.1 simplifies, and what that hides

Required by `AGENT_DIRECTIVE_do_not_flatten.md`.

1. **Coverage is a three-level ordinal** (uneven / broad / universal) standing in for a per-country reality. "Broad" hides that online-ordering penetration varies enormously between the US and, say, Italy. This will overstate scalability in low-platform-density markets.
2. **Every tag is boolean or a raw count, with no quality dimension.** `dietary_page_exists` is true for a serious allergen policy and for one line of marketing. Mitigated by storing the matched evidence string, not just the bit.
3. **`sides_section_size` counts dishes, not portions or calories.** Four sides may still not be dinner. The census's starch-family breakdown partly compensates; nothing fully does without portion data.
4. **Camouflage is inferred from menu structure, not observed.** A tapas bar with a hostile server is still tagged as camouflage-friendly. Only visit reports can correct this, which is another reason they matter.
5. **Modifier-group detection is regex over option labels.** It will miss modifiers phrased unusually and will fire on "add chicken" as readily as "no cheese" — the count is *modification capability*, not *useful-to-us modification capability*. Refining that needs real platform data.
6. **The award list is Western-weighted.** Michelin, James Beard, World's 50 Best, Gault&Millau and La Liste between them barely touch Africa, South Asia and most of Latin America. Community nomination is the only tag with genuinely unbounded reach, which is a statement about the others' limits.

## 10. Interfaces

- Structural and camouflage tags are computed from a menu snapshot plus platform metadata; several derive directly from census counts (`src/census.py`).
- Accommodation evidence tags feed the same `accommodation` field defined in the restaurant schema, but at a lower evidence level: `evidenced` from machine-readable signals, `verified` only from direct contact, expiring after 180 days.
- Visit reports are Layer 1 knowledge under `../docs/PEER-REVIEW.md`: each needs a submitter of record, a date, and a structured body. They are not free-text reviews.
