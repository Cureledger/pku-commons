# TruPKU pain points → suggested community hacks

**Source of record for the "Devs: we challenge you to solve these" block on the landing page.**

These are patient/caregiver friction points drawn from NPKUA's *TruPKU / Voice of the Patient*
(Externally-Led Patient-Focused Drug Development) effort and the project's main README, reframed as
concrete build targets for the PKU Commons community. Each is a place to point AI + devops at real
daily burden.

> Report landing page: <https://www.npkua.org/truepku/>
> Public VOP report (PDF): <https://www.npkua.org/wp-content/uploads/2025/12/TruePKU-VOP-Report-WEB-VERSION93.pdf>
>
> **Note:** the pain-point *themes* below are summarized in our own words from the public report
> and the project README. This file is a working editorial list for the site — not a quotation of
> the report. When a clinician/RD or NPKUA reviewer verifies wording against the source document,
> record the reviewer and date in the table at the bottom (legal-layer audit trail).

| # | Pain point (theme) | Suggested hack |
|---|--------------------|----------------|
| 1 | **The daily counting grind** — every food weighed, calculated, logged by hand; families burn out and stop logging, so the clinic loses data. | Cut estimation-to-log to one tap: label parse + scale weight + auto-log, benchmark-verified so the shortcut is trusted. |
| 2 | **Slow blood-phe feedback** — results return 5–14 days later by mail; no timely link between food, symptoms, and measured level. | Build the food ↔ symptom ↔ level data nexus: structured logs ready to correlate the moment faster home testing arrives. |
| 3 | **Labels don't speak PKU** — USDA protein grams are too coarse; phe-per-gram varies by source; families reverse-engineer every label. | Improve the ingredient→phe classifier and grow the living food list so very-low-protein staples are covered and cited. |
| 4 | **Tools that fade away** — apps from one parent or small shop go unmaintained and disappear, stranding reliant families. | Ship on shared, benchmark-gated infrastructure so an app keeps working — and stays trustworthy — after its author steps away. |
| 5 | **Real-world conditions break tools** — estimation happens in a grocery aisle, one-handed, on weak Wi-Fi, under time pressure. | Design for the aisle: offline-tolerant, low-bandwidth, deterministic behavior with graceful degradation. |
| 6 | **New drugs raise the stakes** — powerful new therapies can over-correct into hypophenylalaninemia, needing a fast dietary response the slow data loop can't support. | Make dietary phe data fast and shareable enough to support quick, safe adjustments alongside modern treatment. |

## Review / verification log (legal-layer audit trail)

| Item(s) | Wording verified against source? | Reviewer of record | Date | Notes |
|---------|----------------------------------|--------------------|------|-------|
| 1–6 | Pending | _(unassigned)_ | — | Themes summarized from public report + README; awaiting NPKUA/clinician wording check. |
