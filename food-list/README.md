# Low-Protein Living PKU Foods List

## Why we need to supplement knowledge with a foods list

PKU food manufacturers and associations often maintain low-protein foods lists for the
community.

Currently, AI does not obviate the need for these lists. Reliability of label-only
ingredient analysis is hard to gauge, and harder to prove. In order to enhance the
reliability of the agent, we've created a number of food lists to serve similar to
"knowledge graphs."

This has shown, in my experiments, to improve performance for the range of foods in the
**very low protein** range — the staples of the PKU diet.

## TODO

We need to create a system for maintaining a **living foods list** that reduces the work
of the Claude Skill AI, or any agent using the service.

Analogues exist from sources like **Open Food Facts**, from whom we gratefully forked some
resources.

### Goal for the Claude Science hackathon

Get the **USDA** and **Open Food Facts** modules working well as a supplement to the label
reader, and create the technical foundation for the "low-protein living foods list."

## Relationship to the benchmark

Ground truth for the phe-estimation [`benchmark/`](../benchmark/) is computed from
documented sources (USDA FoodData Central; Open Food Facts). The living foods list feeds
the same very-low-protein staple range the benchmark seed set covers — see
`benchmark/testset/food_reference.json`.
