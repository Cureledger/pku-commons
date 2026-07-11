# TruPKU pain points and suggested community hacks

Source of record for the "Devs: we challenge you to solve these" block on the landing page.

These patient and caregiver friction points come from NPKUA's *TruPKU / Voice of the Patient*
(Externally-Led Patient-Focused Drug Development) effort and the project's main README. We reframe
them here as concrete build targets for the PKU Commons community. Each one points AI and devops
work at a real daily burden.

> Report landing page: <https://www.npkua.org/truepku/>
> Public VOP report (PDF): <https://www.npkua.org/wp-content/uploads/2025/12/TruePKU-VOP-Report-WEB-VERSION93.pdf>
>
> Note: the pain-point themes below are summarized in our own words from the public report
> and the project README. This file is a working editorial list for the site. It is not a
> quotation of the report. When a clinician, RD, or NPKUA reviewer verifies wording against the
> source document, record the reviewer and date in the table at the bottom (legal-layer audit
> trail).

| # | Pain point (theme) | Suggested hack |
|---|--------------------|----------------|
| 1 | The daily counting grind: every food weighed, calculated, and logged by hand. Families burn out and stop logging, so the clinic loses data. | Cut estimation-to-log to one tap: label parse, scale weight, and auto-log, benchmark-verified so the shortcut is trusted. |
| 2 | Slow blood-phe feedback: results return 5 to 14 days later by mail. There is no timely link between food, symptoms, and measured level. | Build the data link between food, symptom, and level: structured logs ready to correlate the moment faster home testing arrives. |
| 3 | Labels do not speak PKU: USDA protein grams are too coarse. Phe-per-gram varies by source, and families reverse-engineer every label. | Improve the ingredient-to-phe classifier and grow the living food list so very-low-protein staples are covered and cited. |
| 4 | Tools that fade away: apps built by one parent or a small shop go unmaintained and disappear, stranding families that depend on them. | Ship on shared, benchmark-gated infrastructure so an app keeps working, and stays trustworthy, after its author steps away. |
| 5 | Real-world conditions break tools: estimation happens in a grocery aisle, one-handed, on weak Wi-Fi, under time pressure. | Design for the aisle: offline-tolerant, low-bandwidth, deterministic behavior with graceful degradation. |
| 6 | New drugs raise the stakes: powerful new therapies can over-correct into hypophenylalaninemia, and that needs a fast dietary response the slow data loop cannot support. | Make dietary phe data fast and shareable enough to support quick, safe adjustments alongside modern treatment. |

## Review / verification log (legal-layer audit trail)

| Item(s) | Wording verified against source? | Reviewer of record | Date | Notes |
|---------|----------------------------------|--------------------|------|-------|
| 1-6 | Pending | _(unassigned)_ | _(pending)_ | Themes summarized from public report and README.  |
