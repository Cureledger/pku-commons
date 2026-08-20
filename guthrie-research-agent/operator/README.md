# Guthrie Operator — the autonomous mission agent

Guthrie stops being a chatbot and becomes an *operator*: an always-on worker
whose job is advancing one mission — "make a home phe monitor real" — using
agents and agent networks wherever possible, and routing physical/clinical work
to humans for you to approve.

It is **its own boss so long as it lives with the mission and stays inside the
policy.** The mission is the boss; the policy is the law; the loop just executes.

## The pieces

| File | Role |
|---|---|
| `mission.yaml` | **The boss.** Objectives + scope. The operator reads it every tick. Edit this to steer it. |
| `policy.yaml` | **The law.** Budget caps, geo/sanctions screen, dry-run flag, kill switch, which networks are on. |
| `governor.py` | **The enforcer.** Every external action + every spend passes through it. Enforced in code, not by the model's goodwill. |
| `loop.py` | **The heartbeat.** One API call per tick: read mission -> pick ONE action -> execute through the governor -> log. |
| `adapters/` | The only code that touches an external network. Inert until you enable + fund one. Wallet keys live here, never in the loop. |
| `ledger.jsonl` | Append-only audit trail: every tick, decision, rationale, and (would-)spend. |

## What it does each tick

Reads the mission + budget state + recent history, then chooses one of:
`research` / `draft_document` (work Guthrie does himself, grounded + cited via
the skill's brain), `post_bounty` (spend- and geo-gated), `route_to_human`
(queues an RFP/outreach for you), or `wait`.

## Safety — why you can leave it running

All verified in testing:

- **Dry-run by default.** `policy.mode.execution: dry_run` -> it runs the full
  loop and logs every spend it WOULD make (`would_spend` in the ledger), moves
  nothing. Realized spend stays $0 until you set `live`.
- **Budget enforced in code.** Lifetime ceiling, per-action cap, rolling weekly
  cap. Tested: $40 ok, $60 rejected, 4th weekly $50 rejected at the $150 cap.
- **Geo / sanctions screen.** Every counterparty + network jurisdiction is
  checked before engagement; banned or unknown -> blocked. Tested: US/DE allowed;
  Iran, Russia, N.Korea, and empty all blocked, including inside a spend.
- **Kill switch.** Drop a `HALT` file in the operator dir; the loop stops before
  its next action.
- **One action per tick.** For auditability. Cadence set by `tick_seconds`.

## Run it

```bash
cd guthrie/operator
pip install pyyaml anthropic            # plus the skill's rank_bm25 + sentence-transformers
export ANTHROPIC_API_KEY=sk-...
export GUTHRIE_INDEX_DIR=$PWD/../pku_index

python loop.py --once                   # single dry-run tick, prints decision + result
python loop.py --daemon                 # heartbeat loop (dry-run until you go live)
```

Deploy it the same way as `serve/` (Railway/Fly, one `ANTHROPIC_API_KEY`
secret). It is a worker, not a web service — no port, just the loop. Persist the
operator dir (mission/policy/ledger) on a volume so history survives restarts.

## Going live (the founder's checklist — nothing here happens without you)

1. Review a week of dry-run ledger. Confirm its judgment.
2. Implement + review one adapter in `adapters/` against the network's CURRENT
   live docs (the notes in there are placeholders, not verified fact).
3. Fund a dedicated wallet with a fixed float. Put its keys in the adapter's own
   env — never in `loop.py`, never in the ledger.
4. Set that network `enabled: true` in `policy.yaml`.
5. Set `policy.mode.execution: live`. Keep the caps low at first.
6. Watch the ledger. `HALT` any time.

The operator can propose and decide freely in dry-run today. Real money moves
only after step 5 — your flag, your wallet, your caps.
