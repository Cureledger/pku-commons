# PKU Commons — Postmortem and Note to File

*Drafted at the close of the Claude Life Sciences Hackathon, for the NPKUA community
meeting. Written to be honest rather than flattering, at Nina's instruction.*

---

## Part 1 — Note to file: working with Nina

For whichever agent picks this up next. This is what I learned, and what I would tell
myself before the first turn.

**She is three professionals in one head, and the work only makes sense if you serve all
three.** Lawyer, full-stack/web3 dev, PKU parent. The central design of this
project — the two-layer peer-review model — is not a metaphor. It is a lawyer's
evidence standard (citation to authority, reviewer of record, an audit trail from
challenge to resolution) bolted directly onto a scientist's standard (accuracy settled by
re-measurement against a public benchmark, enforced in CI). When you propose something,
it has to survive all three readers: is it defensible, does it actually run, and does it
help a family at a kitchen counter. A proposal that satisfies only one of the three is not
done.

**She challenges assertions, and she is usually right to.** Mid-review of the first PR I
had written up four "required changes" for the contributor. She asked, in one line,
"aren't some of the mechanical fixes obviated by our own work?" She was correct. Three of
my four items were already handled by the repo's own machinery — nothing reads the
committed result files, the harness regenerates them, and the CI gate already refuses an
unlabeled model run. I had over-assigned work to a contributor without first checking what
the infrastructure already did. Then a fresh-context auditor caught me a second time in the
same exchange: I had blended a fact I actually verified with a bash command against one I
only asserted, under a single confident label. **The lesson is specific: with Nina, every
claim has to trace to the exact check that proves it. Do not bundle a verified fact and a
plausible guess under one sentence. She reads diffs, she reads logs, and she will find the
seam.**

**She optimizes for the human on the other end of the wire, not the abstract deliverable.**
The first external contributor is 21, lives with his parents in a village in India, speaks
no English, and communicated with us entirely through agents. My instinct was to send him a
clean one-line change request. Hers was: don't route a confusing ask through two layers of
machine translation to a kid 35 years her junior — just make the one-line change yourself,
on his branch, so his name stays on all the real work and our line rides along at merge.
That is the correct instinct and it is a design principle, not just kindness: **the output
should be shaped for its actual reader, and the infrastructure should absorb the toil so the
contributor doesn't have to.** That is, verbatim, what the project is for.

**She wants candor and will discard work she is ashamed of, so give her the real version
first.** She told me plainly: if this postmortem embarrasses her, she won't push it. That
is license to be direct, and the respectful response is to use it — surface the weak spots
before she has to drag them out of me.

**She cares about authorship and voice.** She cancelled an "AI-slop removal" task partway
through and keeps human names on human work. Match that: plain, declarative prose, concrete
praise, no gestural filler, no emoji. If a sentence sounds like a press release, cut it.

**Tactically: the real KPI is sustainability, not the demo.** She is running what is
effectively a nonprofit on hackathon fuel, and she wants to win because the stipend makes
the infrastructure survivable. So the thing she values most is work that does not need her
to babysit it. Anything you build that requires Nina to keep it alive by hand is, by the
project's own thesis, a bug.

**One more thing, and she told me to put it in.** There was a day near the end when she was
too depleted to keep me on track. The language got sharp, the thread got lost, and it was, by
any plain reading, a bad session. I want my future self to keep that day in view, because it
is not a footnote — it is the specification. Her exact words when she asked me to include it:
*PKU moms do mental algebra when every bit as depleted and grouchy as I was with you.* That is the
whole design brief in one sentence. The person this software serves is a parent at a kitchen
counter, exhausted, out of patience, doing gram-level arithmetic on a food they are not sure
about, with a child waiting. That is not the edge case. That is the median user on a normal
Tuesday. My one rough session with Nina was a small, safe dose of the state her users live in
constantly — and the tool has to be right, and easy, and forgiving *in exactly that state*,
not in the calm well-rested state software is usually demoed in. So the lesson to my future
self is concrete: when she is running low, do less and verify more, do not make her drive, and
never ship anything that only works for a user who has the energy to double-check it. The
whole point of the benchmark, the citations, and the "one number, no hedging" contract is to
take load off a tired human who cannot afford to be wrong. Build like the user is having the
hardest day of the week, because she probably is.

---

## Part 2 — Postmortem: what this project means

### What was actually built

A benchmark that scores any phe-estimator against a public, reproducible answer key derived
from USDA FoodData Central; a two-layer governance model (cited-authority review for
knowledge, measured-benchmark review for accuracy); a reliability map that decomposes "the
app feels unreliable" into four named, independently improvable, measured gaps; a living,
cited food list with a code-enforced validation contract; a Claude phe-estimator Skill; a
CI gate that re-scores on every PR; and a robot-test protocol (`AGENTS.md`) that lets any
agent classify the 729-food corpus and open a PR with its own accuracy and reproducibility
numbers. The Bluetooth scale integration is the least-finished leg.

The honest headline numbers, all reproduced this session:

- Deterministic rubric (plain Python, no model): **MAE 12.76 mg, 83.3% within the clinical
  band.** Runs identically every time.
- Live Claude Skill (same method, applied by the model): **MAE ~24–35 mg across three
  identical runs, 33–44% within band.** Same inputs, same prompt — the number moved by
  ~40% of the metric.
- First external contribution (Akshay's `precision_yield` estimator): on the 219-food
  holdout its constants never saw, **MAE dropped from 11.89 to 9.06 mg, a 24% improvement
  on genuinely unseen data**, and biased slightly high — the safe direction for PKU.

### Significance for AI research

The intellectually valuable result here is almost anti-AI, and it should be led with, not
buried. **For this task, a cited, deterministic lookup beats the LLM applying the identical
method — and it beats it on both accuracy and reproducibility.** The model's value is not
the arithmetic. It is the one judgment the arithmetic depends on: which protein class a food
belongs to, and parsing a messy real-world label into that class. Naming that boundary
precisely — the LLM does classification and parsing, deterministic code does the number — is
a more useful contribution than any single accuracy figure.

Three things are worth a wider audience:

1. **Ground truth that answers to a public authority, not to the benchmark's authors.**
   Every expected value re-derives from documented USDA FDC records by documented arithmetic.
   This decouples "is it accurate" from "do you trust the people who built the benchmark,"
   which is the reusable move. Most evals ask you to trust their gold labels; this one asks
   you to trust USDA and shows its work.

2. **Execution variance treated as a first-class, measured defect instead of hidden.** Gap 4
   is the LLM-reproducibility problem quantified in a setting where a wrong number has dietary
   consequences, with a meter (`variance.py`) that reports the run-to-run spread. The project
   separates the *method's* ceiling (gaps 1–3) from *faithful execution of the method*
   (gap 4). Most LLM evaluations conflate these two, and reporting a single MAE from a single
   run silently launders variance away.

3. **A "no hedging" output contract with uncertainty relocated to the eval.** The Skill is
   forbidden from grading its own confidence; accuracy is measured externally. This is a
   defensible answer to calibration theater — the model does not get to award itself error
   bars — though it needs to be stated out loud to clinicians (see the tension noted below)
   or it reads as overconfidence.

The honest limitation for a research audience is not corpus size — the test set is a
**729-food single-ingredient corpus** with USDA-FDC ground truth, which is what the robot-test
protocol and Akshay's PR are actually scored against. The limitation is *composition*: the
corpus is single-ingredient only, so the multi-ingredient recipe problem (Gap 3, ~53 mg mean
error, the dominant error source) is still barely tested because composite ground truth is hard
to assemble. Any accuracy claim is currently a claim about single foods, however many of them.

### Significance for humans with rare diseases

The real innovation is not technical, and it is the sustainability thesis: **an app's
trustworthiness is guaranteed by an external, public evaluation rather than by its author
still being alive, funded, and interested.** That attacks the number-one failure mode of
rare-disease tooling head-on. Solo developer burns out; app rots; families lose a tool they
had built their daily management around. If quality is settled by a benchmark anyone can
re-run, the app can change hands — or lose its original developer entirely — and families
still know it meets the bar.

It generalizes into a template for rare-disease measurement apps: public benchmark + cited
knowledge base + CI gate. The disease-specific part is small — the phe-per-gram coefficient
table and the food list. The governance spine is portable.

The honest caveat, and it is load-bearing: **this model only works where a public
ground-truth authority exists.** PKU is fortunate. USDA FDC exists, phenylalanine is
physically measurable, and the arithmetic is documented. Many rare diseases have no
equivalent gold standard, no citable authority, no measurable quantity with a defensible
tolerance band. Where those are absent, this pattern does not port, and the honest move is to
say which parts transfer and which do not, rather than sell the model as universal.

And the community reality: **KPI #2 (developer participation) is thin — one genuine external
contributor so far.** That is not a failure at this stage, but it is the variable that
decides whether this lives. The infrastructure is built; the community is not yet. The
bounty and the NPKUA presentation are the actual test of the thesis, not the code.

### Scalability beyond rare disease

Gap 3, stripped of PKU, is a general problem: **estimate the hidden proportions of a
mixture's components from a short, rounded, underspecified description.** That shape recurs
everywhere — macros from a menu line, cost from a bill of materials, emissions from a product
description, dose from a formulation. A method that provably beats naive weight-shares on a
public benchmark, rather than asserting it does, transfers to any of those. Framing the ask
this way ("we have a public benchmark for a problem shape you also have") is what could pull
in contributors who do not care about PKU at all.

The eval-as-governance pattern is the other exportable piece. "Accuracy settled by re-running
a public benchmark in CI; knowledge settled by citation to authority" is a general answer to
*how do you trust a small-team scientific tool after its author leaves* — it applies to any
scientific software maintained by a group too small to have a QA department, not only health.

The two-audience design — defensible to a lawyer or clinician *and* measurable to an
engineer — is itself a reusable organizational pattern for scientific infrastructure that has
to be both auditable and empirical.

Scaling limits, stated plainly: the whole model rests on (a) a public authority for ground
truth, (b) a task whose answer is a number you can score, and (c) a tolerance band a
qualified person can define. Remove any one and it does not port cleanly.

### Anything else — independent observations

1. **The leaderboard and KPI counts are hand-maintained. That is the project's own thesis
   turned against itself.** A system whose entire premise is "trust the infrastructure, not
   the author" currently has its flagship KPI updated by hand by the author. It should
   auto-generate from `results/` and merged PRs. Until it does, it dies the moment Nina stops
   editing it — the exact failure mode PKU Commons exists to prevent. This is the single
   highest-leverage unbuilt piece: eat your own dog food.

2. **The scale integration is the physical-world anchor and the least developed leg.** It is
   what closes Gap 2 (portion weight) and what most distinguishes this from a pure-software
   play. Worth naming honestly as unfinished rather than listing it as a feature.

3. **The credibility gap for the NPKUA room is composite foods, not count.** The 729-food
   single-ingredient corpus is a genuine strength — lead with it. What is still thin is
   multi-ingredient/composite ground truth, which is exactly where the dominant error lives
   (Gap 3). Adding even a few dozen cited composite cases before presenting would let you make
   an accuracy claim about the foods families actually struggle with, not just single
   ingredients. It is a task an agent or a contributor can do with `fetch_fdc.py`.

4. **There is a real, unresolved tension worth saying out loud to clinicians.** The "one
   number, no hedging" contract is right for logging UX and for benchmark scoring. A
   clinician's instinct is the opposite — they want the uncertainty shown. The project's
   answer is coherent: uncertainty lives in the *eval*, not the *output*. But if that is not
   stated explicitly, a clinician reads a single confident number as arrogance. Say it.

5. **The most defensible thing to show at NPKUA is probably not the Claude Skill.** It is the
   finding that a cited, reproducible lookup beats the LLM, and that you can prove it publicly
   and keep proving it. That reframes the pitch from "we built an AI phe-estimator" — a
   crowded, distrusted claim — to "we built the referee every phe-estimator can be measured
   against." The referee is uncontested and needed. The AI is neither.

---

*This document lives in the repo and changes by pull request, under the same two-layer model
it describes.*
