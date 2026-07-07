# Phe-estimator Skill

> **The most important job after the landing page.**

This Skill is intended to do the "thinking like a PKU parent" needed to parse and
estimate the phenylalanine (phe) contained in a food from its nutrition label and
ingredients list. The general method:

## Is this food potentially suitable for my diet?

For purposes of label analysis, PKU patients are often taught that foods with **2 g of
protein or less per serving** are potentially suitable for the diet. For these foods we
need to accurately calculate phe. We're less concerned about calculating phe for
higher-protein foods, in general, because they aren't usually relevant to the diet.

Accordingly, we set the Claude Skill's initial parameter for label parsing to **under 2 g
of protein** — not to make a decision about a food product's suitability for any person,
but to focus on making the Skill and label parser work well at the critical "countable"
food range.

## How do I count the phe in this food?

1. Once you determine a food is potentially suitable, read the label's ingredients list,
   searching for items that contain phe.
2. Classify each ingredient by type of protein source, for a phe-per-gram calculation for
   that ingredient.
3. Make an educated guess about recipe composition and the relative weight of phe-bearing
   ingredients in the entire label recipe, based on basic cooking science. We call this
   the **"recipe factor."**
4. Multiply the recipe factor by the portion consumed.
5. Log it.

My experiments show that many factors affect the AI's performance. So we need to **reduce
non-deterministic thinking** by the AI — so it doesn't "work" as hard and potentially
introduce errors — and create specific guidelines for optimizing performance in
foreseeable technical conditions (for example, weak grocery-store WiFi).

## Peer review requests

- **Methodology review** by parents, dietitians, and clinicians.
- **Testing of phe-reader outputs** by parents and dietitians.
- **Creating and optimizing the reliability** of the phe-estimator Skill by AI developers.

I have tested the phe-estimator function in real life, but have not yet created a working
Skill.

> **CRITICAL:** We will have Claude Science create a peer-review matrix once we feel the
> Skill is ready to test.

## How it's measured

Any estimator implementing the shared interface is scored on the public benchmark — see
[`../benchmark/`](../benchmark/) for the harness, the seed test set, and the leaderboard.
The Skill plugs in via a `benchmark/estimators/claude_skill.py` adapter so its accuracy
lands on the leaderboard next to every other estimator.
