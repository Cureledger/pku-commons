# Plan: model the process before the next line of code

*What I forgot, why it matters, and what to do about it. Next output before shipping more code.*

## What I forgot

I built a governance model — the two-layer peer review — and applied it rigorously to the
project's *knowledge* (cited food list) and its *outputs* (benchmarked estimates). I never
applied it to the *process itself*. There is no business process model of the estimator: the
actors, the artifacts, the decision points, and the review gates, drawn as one diagram before
code. I wore the lawyer hat for the data and the dev hat for the build, and forgot the
legal-engineering hat that models the workflow first.

## Why it matters

**The estimator is a chain of subprocesses, and only one of them is the hard part.** In shorthand:

    parse label → classify protein source → apply coefficient → (recipe weight-share) → scale to portion → score against benchmark

Without a process model, those steps stayed fused. We treated "the estimator" as one thing and
measured it end to end. The single most consequential fact in the whole project — that the LLM's
job is **classification and parsing**, and deterministic code does the arithmetic — was not
named up front. It surfaced late, empirically, from Akshay's PR: his zero-leakage math made it
visible that *classification* is the subprocess to test today, not the arithmetic.

A process model would have made me **decompose the estimator into named subprocesses on day one**,
each with its own inputs, its own failure mode, and its own place on the benchmark. Then each
subprocess is independently attackable — we test classification accuracy as its own experiment,
recipe weight-share as another, portion scaling as another — instead of waiting for a
contributor's good work to reveal which box in the pipeline was the bottleneck. This is the
scientific method the project already preaches, applied one layer earlier: to the *design of the
work*, not just the outputs of it. (The reliability map's four gaps are the same idea discovered
the slow way — a process model would have produced that decomposition before any measurement,
not after.)

**Second-order cost: collaboration friction.** With no shared process artifact, every working
session re-derived intent from memory, and the boundaries between subprocesses had to be
rediscovered each time. A one-page model an agent loads at the start of every session is a
contract: it removes the class of error where work gets mis-assigned to a step the infrastructure
already handles, and it lets session ten start where session nine ended.

## What this is *not*

Not a claim the project would have been finished. The Bluetooth scale would still be unfinished —
a diagram does not fold firmware. And some of this was genuine discovery: the classify-vs-compute
boundary was partly unknowable before measurement. But modeling under uncertainty is the lawyer's
job — a v0 model, amended with a reviewer of record as we learned, is the two-layer method applied
to the process. The honest claim: the parts that did ship would have arrived faster, with less
thrash, and testable in pieces.

## The action

1. Draw the process model in bpmn.io; export `process-model.bpmn` (XML) into this repo.
2. Model the estimator as named subprocesses (parse, classify, coefficient, recipe-factor,
   portion-scale, score), each with inputs, failure mode, and the benchmark signal that measures it.
3. Mark the review gates: which subprocess changes are Layer 1 (cited) vs Layer 2 (measured).
4. Reconcile against `docs/RELIABILITY.md` — every named subprocess should map to a gap or expose
   a gap the map is missing.
5. Land it before the next line of estimator code. This is the next deliverable.

## Why it belongs in the deliverables, not a footnote

For the mom&pop dev shops this project exists to sustain, the transferable lesson is one sentence:
**model the process in a shared artifact your agent reads, before you write code.** That is legal
engineering handed to non-lawyers as a gift. It is also the same defect the postmortem already
names one layer up — the hand-maintained leaderboard, the thesis turned against itself — showing
up at the process level. The fix for the omission and the fix for the collaboration are the same
object: a process model that becomes loaded context.
