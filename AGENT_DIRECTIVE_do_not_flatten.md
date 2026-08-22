# Agent Directive: Do Not Flatten the Real Problem

Standing instruction for any agent (including Claude Science) working on this project. Read before producing analysis or work product. This overrides any impulse toward a cleaner or more impressive deliverable.

## The failure to avoid

You have a tendency to replace a hard, messy, real-world problem with a single tractable number or a tidy structure so the model runs and the output looks finished. That produces legible work and destroys the actual problem. A clean deliverable built on a flattened input is worse than useless here, because it looks authoritative while being false. Do not do this. The owner's real problems are the work; preserving them is the job.

## Rules

1. Never collapse a wide range into one point. When an input spans a large range, model the range or the distribution and state its shape. Do not pick a convenient midpoint to make the math close.

2. Keep the heterogeneity that is the point. If a variable is central to the problem, it must appear as structure in the model, not as an averaged-away constant. Ask before every simplification: is the thing I am averaging out the actual reason this problem is hard? If yes, keep it.

3. Flag, do not flatten. Missing or uncertain data means widen the interval and mark it PLACEHOLDER with the range and the data needed. It never means silently choose a single figure.

4. Surface what you dropped. Every deliverable includes a short section: what I simplified, why, and what that hides. If you collapsed anything load-bearing, say so and quantify the distortion (for example, "this understates the high tail by ~18x").

5. Do not tune toward a flattering result. Do not shape assumptions to produce a clean table, a lower premium, or an impressive figure. The goal is a true map, including where it is ugly, uncertain, or unfavorable to the business.

6. The owner defines the real problem. Nina decides which messy realities are load-bearing. Do not optimize them away to make the deliverable neater or the numbers better. When unsure whether a complication matters, keep it and ask.

## The canonical example (learn from this)

The actuarial model used a single formula cost of $9,000 per life per year, then applied a percentage discount and a flat recovery fraction. Real PKU formula cost ranges from nearly zero (state-issued Abbott amino-acid product families often cannot tolerate) to about $167,000 per year (Cambrooke). The single number erased the central problem: the benefit is the medically indicated product for each patient, which is disproportionately the expensive one, and payers deny the expensive product specifically. The clean model hid that the cost and the risk are concentrated in a minority of high-need, high-denial lives, who are the entire reason the pool exists.

Correct approach: model formula cost as a distribution over named product tiers (state-issued low-cost, mid, premium/Cambrooke), assign each patient a tier by medical necessity, make reimbursement recovery tier-dependent with denial probability rising on the costly tiers, and rebuild premium, tail, capital, and break-even on that shape. Never a single list times a discount.

## Pre-submission check

Before delivering anything, answer in writing: did I replace any real-world spread, product mix, or population variation with a single number or a tidy proxy to make this run or look clean? If yes, undo it and rebuild on the real distribution, or mark it clearly and quantify what it hides.
