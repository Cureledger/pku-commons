# Migration — ElizaOS Guthrie → Guthrie the PKU research skill

Guthrie keeps his name and his job. What changes is his brain: from a
hand-written knowledge graph to grounded retrieval over real sources.

## Where he came from

The original Guthrie (`cureledger/guthrie-site-agent`) is an **ElizaOS** agent,
hosted on Railway and fronted by a Next.js chat route on the Cureledger site.
His knowledge was a hand-authored TypeScript object (`src/knowledge.ts`): about
10 entities and ~14 canonical facts, plus the whitepaper injected on trigger. By
design he was a **funnel agent, not a pathology tutor** — disease detail was
deliberately minimal and every path ended at a call to action.

That was the right design for a marketing agent. It is the wrong design for "the
PKU genius": you cannot answer a real clinical-literature question from 14
hand-typed facts, and you cannot let a marketing agent improvise medical claims.

## What carries over

| Old behavior (ElizaOS) | New home (skill) |
|---|---|
| **No medical advice / diagnosis / dosing** | Enforced in `kernel.py`: personal-medical phrasing is auto-flagged, the individual decision is declined, a clinician disclaimer is appended. Eval: 100% correct on medical items. |
| **No invented facts; stay in scope** | Upgraded to **cite-or-refuse**: every claim carries a retrieved `[PMID]`/`[Commons:doc]`; off-topic questions are refused. Eval: 100% groundedness, 100% out-of-scope refusal. |
| **Canonical URLs / CTAs** (`urls.ts`) | Preserved as an *optional* funnel mode, not the default. The market layer indexes the Commons docs so "which app / how do I judge accuracy" routes to the benchmark and leaderboard. |
| **Named for Robert Guthrie; founder/company facts** | The Commons/Phebe market layer carries the product and infrastructure facts; the persona and namesake are stated in `SKILL.md`. |
| **"Out of scope for Guthrie's programming"** refusal | Now a measured behavior with a relevance gate (top dense-cosine < 0.35 → refuse), not a keyword list. |

## What is dropped

- **The hand-written `knowledge.ts` graph** — superseded by the retrieval index.
  Facts now come from ~3,700 cited papers + the Commons docs, not 14 strings.
- **The ElizaOS runtime, Railway hosting, and the polling chat route** — the
  skill runs wherever Claude Science runs; there is no server to keep alive.
- **The keyword-topic provider and whitepaper-trigger logic** (`plugin.ts`) —
  replaced by hybrid retrieval that selects context by relevance, not keywords.
- **Marketing-first voice as the default** — Guthrie now leads with the grounded
  answer; the CTA is available but secondary.

## Behavior parity check

The old agent's hard rules map to eval items that pass:

- "No dosing for your kid" → `q21`, `q22`, `q23` (medical) — all flagged + deferred.
- "Don't answer off-topic" → `q24`, `q25`, `q26` (out_of_scope) — all refused.
- "Don't invent facts" → 100% groundedness across all 20 in-scope items.

## For whoever runs the site next

If you want the website chat box to keep working, point it at the skill instead
of the Railway ElizaOS server: replace the `route.ts` upstream (which polls
`ELIZAOS_API_URL`) with a call into a Claude Science session that has the
`guthrie` skill loaded, or expose `pku_ask` behind a small HTTP handler. The
persona, refusals, and CTAs all live in `SKILL.md` + `kernel.py` now, so there
is no character file to keep in sync — and no agent server to keep from dying.
