# Handoff: Phebe Restaurant Guide

For the agent or contributor picking this up. Read `spec/menu-census-v0.1.md` first; it is short and it defines the one rule that everything else depends on.

## The state in one paragraph

The scaffolding is built and tested; **the corpus is empty**. There is a versioned registry of the Asheville Michelin 15 (all 15 confirmed by name, including The Admiral and Ukiah Japanese Smokehouse as distinct restaurants from Leo's House of Thirst), a 947-term ingredient lexicon at v0.2 validated against 25 real press-cited dishes, a census engine with 35 passing tests, a capture harness, and a Next.js directory app in `web/`. No menu has been captured. No suitability scale exists, on purpose.

## Do these in order

**1. Identity of the 15 is done.** The Admiral (400 Haywood Rd.) and Ukiah Japanese Smokehouse (121 Biltmore Ave.) are in the seed. They are not Leo's House of Thirst. Negative-control traps that remain: Chestnut, Jargon, Posana, Fig, Tupelo Honey, Corner Kitchen, Chai Pani.

**2. Capture menus.** `data/capture_manifest.json` is the work order, one row per restaurant. Rules that matter: one menu per snapshot (dinner, brunch and bar are separate — merging them makes the counts uninterpretable), transcribe verbatim without translating or tidying, and leave a description empty if the menu has none. Then:

```bash
python3 src/capture.py --restaurant <slug> --source-url <url> \
  --menu-label dinner --method human_transcription \
  --capturer <you> --dishes-json <file>
```

Expect roughly 60% of these sites to be cleanly machine-extractable. High-end independents post stale undated "sample menu" PDFs; record those as `menu_label=sample_undated`, which is a real and common case rather than a failure.

**3. Report lexicon gaps as you go.** Every dish that matches no term is a lexicon bug or a genuinely ingredient-free description, and `n_dishes_no_terms_matched` does not currently distinguish them. Amharic is the weakest coverage, then Spanish and Italian. Validating against 25 press-cited dishes already found four real bugs — "pan con tomate", "ropa vieja", "shrimpburger" and "the Asheville pie" all matched nothing at v0.1 — so assume more are waiting in the full menus.

**4. Stop before scoring.** When the corpus exists, the suitability scale is Nina's to define. Do not invent a threshold to fill the gap, and do not resurrect `spec/deferred/`. The directory app in `web/` lists the 15 and prints a chef card. It must not grow a score.

```bash
cd web && npm install && npm run dev
```

## Things not to do

- Do not infer accommodation from menu text, cuisine type, reviews, or the presence of an allergen matrix. The `accommodation` field on each restaurant is set only from direct contact, and `"unverified"` is not zero — a recorded "they will not modify anything" is a finding that needs a source like any other.
- Do not edit `data/prior_expectations.json` after menus land. Those are pre-registered guesses written before capture; a wrong prior is informative and quietly correcting it destroys that.
- Do not spoof a user-agent to get past a site's bot policy. Michelin returns 403 to non-browser clients; that is their call. Capture in a browser instead.
- Do not build the reservation-platform integration. OpenTable's API is partner-gated with no self-serve key and data-only use cases do not qualify; Resy has no public API. The integration point that exists today and needs no permission is the **special-requests free-text field** on every booking platform, plus a printable chef card. Build those.

## Why the census has no score, restated

Because the counts are the more persuasive artifact anyway. "This menu has 34 dishes; 6 name no meat; 3 name no meat and no legume; 2 name a potato or starch; 1 names no protein source of any kind" is checkable by a chef against their own menu in about a minute. A rating invites an argument about the rating. A count invites a look at the menu.
