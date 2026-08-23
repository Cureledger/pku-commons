# The app currently scores. You deferred scoring.

**Status: flagged, not deleted. This is your call, not mine.**

## What is live

`web/lib/pku.ts` computes a composite out of 7 and **sorts the homepage by it**:

```
+1  at least one pick
+1  three or more picks
+1  at least one "main"
+1  two or more "mains"
+1  substitutes == true
+1  mnt_food_check == true
+1  published menu URL verified
```

`web/components/score-lines.tsx` renders `{score.total}/{score.max}`, and `loadPkuCards()` orders every restaurant by that number.

## Why this is the thing you said not to build

Your instruction was: *"did you add in a judgment layer about the diet and percent of daily budget? do not do that yet. we need the data. I will help you come up with a strategy for assessing suitability."*

A 0–6 composite that ranks 62 restaurants is a suitability scale. Three specific problems:

1. **The weights are invented.** Why is "two mains" worth the same as "the kitchen will substitute"? Nobody decided that — it fell out of writing plausible-looking code.
2. **`data/pku.json` is hand-picked, not derived.** 52 picks across 15 restaurants, chosen by an agent reading menus, with `kind` assigned by judgment. The census counts terms and shows its work; these picks do not.
3. **`substitutes` and `mnt_food_check` are `false` for all 15** — nobody has been contacted. So the sort currently ranks on menu reading alone while displaying two fields that look verified and are simply empty. **`unverified` reading as zero is exactly the failure the accommodation axis was designed to prevent.**

## Three options

**A. Cut the composite, keep the picks.** Delete `score.total`/`max` and the sort. Show the picks as what the file already calls them — *questions for the kitchen* — plus the census counts. Ordering becomes alphabetical or by menu recency. Cheapest, and consistent with "raw data first."

**B. Keep it behind a flag.** `?scored=1` for you, off by default in public. Useful if you want to feel out whether a composite helps before committing to one.

**C. Keep it and own it.** Then it needs a spec with your name on it, the weights justified, and `substitutes`/`mnt_food_check` rendered as three states (verified yes / verified no / not asked) rather than a boolean.

I would do **A** now and **C** in a month, once there are menus for 62 restaurants instead of 10 and you have seen what the distribution actually looks like.

## Not touched

I did not delete `pku.json` or the scoring code. Deleting another agent's work on my read of an old instruction is worse than flagging it. `spec/deferred/` already holds the PDAS scale I wrote and shelved for the same reason.
