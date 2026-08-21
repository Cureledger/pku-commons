#!/usr/bin/env python3
"""Guthrie Operator — the autonomous mission loop.

An always-on worker (deploy like the serve/ service) whose job is advancing the
mission in mission.yaml. Each tick is one API call: it reads the mission, the
budget state, and recent history, then picks ONE bounded action. Every external
action and every spend passes through the Governor (governor.py), which enforces
the geo screen, budget caps, dry-run, and kill switch in code.

    ANTHROPIC_API_KEY=...  python loop.py --once          # single tick (test)
    ANTHROPIC_API_KEY=...  python loop.py --daemon        # heartbeat loop

The loop NEVER holds wallet keys directly. A network adapter (adapters/) that is
enabled + funded exposes a bounded pay() the governor authorizes; in dry_run the
adapter is never called, only the intent is logged.

Actions the model may choose (the bounded tool set):
  draft_document   — write/update a mission artifact (uses Guthrie's brain)
  research         — deepen evidence via pku_ask (cited, grounded)
  post_bounty      — post an agent-sized task to an enabled network (spend-gated)
  route_to_human   — queue an RFP/outreach for the founder to approve+send
  wait             — nothing worth doing this tick; log why
"""
import argparse
import json
import os
import sys
import time

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, SKILL)     # kernel.py (Guthrie's brain)
sys.path.insert(0, HERE)      # governor, adapters

import kernel  # noqa: E402
from governor import Governor, GovernorError  # noqa: E402

ACTIONS = ["draft_document", "research", "post_bounty", "route_to_human", "wait"]


def load(root):
    mission = yaml.safe_load(open(os.path.join(root, "mission.yaml")))
    policy = yaml.safe_load(open(os.path.join(root, "policy.yaml")))
    return mission, policy


def _llm(prompt, system, max_tokens, model=None):
    import anthropic
    client = anthropic.Anthropic()
    model = model or os.environ.get("GUTHRIE_OPERATOR_MODEL", "claude-sonnet-4-5")
    msg = client.messages.create(model=model, max_tokens=max_tokens, system=system,
                                 messages=[{"role": "user", "content": prompt}])
    return "".join(b.text for b in msg.content if b.type == "text")


def recent_history(gov, n=12):
    if not os.path.exists(gov.ledger_path):
        return []
    rows = [json.loads(l) for l in open(gov.ledger_path) if l.strip()]
    return rows[-n:]


def decide(mission, policy, gov):
    """One API call -> the next action as a JSON object."""
    system = (
        "You are the Guthrie Operator, an autonomous agent whose entire job is "
        "advancing the mission you are given. You act only in service of the "
        "mission and never outside the stated scope. You choose exactly ONE "
        "action per tick and return it as strict JSON. Be decisive and concrete; "
        "prefer producing an artifact over waiting. You do not give medical advice.")
    tools_doc = (
        "Return JSON: {\"action\": one of "
        f"{ACTIONS}, \"objective_id\": <id from the mission>, "
        "\"rationale\": <one sentence>, \"params\": {...}}.\n"
        "params by action:\n"
        "  draft_document: {\"title\":..., \"instructions\":...}\n"
        "  research:       {\"question\":...}\n"
        "  post_bounty:    {\"network\":..., \"task\":..., \"amount\":<USD>, "
        "\"jurisdiction\":<ISO code of the network/counterparty>}\n"
        "  route_to_human: {\"kind\":\"rfp|outreach\", \"target\":..., \"draft_instructions\":...}\n"
        "  wait:           {\"reason\":...}")
    enabled = [n["id"] for n in gov.enabled_networks()]
    prompt = (
        f"MISSION:\n{yaml.safe_dump(mission, sort_keys=False)}\n\n"
        f"BUDGET STATE: {json.dumps(gov.budget_snapshot())}\n"
        f"ENABLED NETWORKS: {enabled or 'none — post_bounty is unavailable'}\n"
        f"EXECUTION MODE: {policy['mode']['execution']}\n\n"
        f"RECENT HISTORY (most recent last):\n"
        f"{json.dumps(recent_history(gov), indent=2)}\n\n"
        f"{tools_doc}\n\nChoose the single best next action now.")
    raw = _llm(prompt, system, max_tokens=700)
    # extract the JSON object
    s = raw[raw.find("{"): raw.rfind("}") + 1]
    return json.loads(s)


def act(decision, mission, policy, gov, out_dir):
    """Execute one governed action. Returns a result dict for the ledger."""
    a = decision.get("action")
    params = decision.get("params", {})
    if a not in ACTIONS:
        return {"status": "invalid", "note": f"unknown action {a}"}

    if a == "wait":
        return {"status": "waited", "reason": params.get("reason", "")}

    if a in ("draft_document", "research"):
        # work Guthrie can do himself — grounded, cited, no spend
        if a == "research":
            r = kernel.pku_ask(params.get("question", ""), mode="full", llm=_llm_shim())
            path = os.path.join(out_dir, f"research_{int(time.time())}.md")
            open(path, "w").write((r.get("answer") or "") + "\n")
            return {"status": "drafted", "artifact": path,
                    "citations": r.get("citations", []), "refused": r.get("refused")}
        # draft_document: use the brain as context, write the artifact
        q = params.get("instructions", "")
        r = kernel.pku_ask(q, mode="full", llm=_llm_shim())
        title = params.get("title", "draft")
        safe = "".join(c if c.isalnum() else "_" for c in title)[:40]
        path = os.path.join(out_dir, f"{safe}_{int(time.time())}.md")
        open(path, "w").write(f"# {title}\n\n{(r.get('answer') or '')}\n")
        return {"status": "drafted", "artifact": path,
                "citations": r.get("citations", [])}

    if a == "route_to_human":
        # never sent externally by the operator; queued for founder approval
        path = os.path.join(out_dir, f"for_human_{int(time.time())}.json")
        json.dump({"decision": decision, "queued": int(time.time())},
                  open(path, "w"), indent=2)
        return {"status": "queued_for_human", "artifact": path}

    if a == "post_bounty":
        net = params.get("network")
        enabled_ids = [n["id"] for n in gov.enabled_networks()]
        if net not in enabled_ids:
            raise GovernorError(f"network {net!r} not enabled")
        amount = float(params.get("amount", 0))
        # THE money + geo gate. In dry_run this returns 'would_spend' and the
        # adapter is never touched.
        outcome = gov.check_and_reserve_spend(
            amount, rationale=decision.get("rationale", ""),
            counterparty=net, jurisdiction=params.get("jurisdiction"))
        if outcome == "would_spend":
            return {"status": "dry_run_bounty", "network": net, "amount": amount,
                    "task": params.get("task")}
        # live: hand to the adapter (which holds the bounded pay path)
        from adapters import get_adapter
        adapter = get_adapter(net)
        res = adapter.post_bounty(task=params.get("task"), amount=amount)
        return {"status": "posted_bounty", "network": net, "amount": amount, "ref": res}

    return {"status": "noop"}


def _llm_shim():
    # kernel.pku_ask expects llm(prompt, system, max_tokens) -> {"text": ...}
    return lambda prompt, system, max_tokens: {"text": _llm(prompt, system, max_tokens)}


def tick(root=HERE):
    mission, policy = load(root)
    gov = Governor(policy, root=root)
    out_dir = os.path.join(root, "output")
    os.makedirs(out_dir, exist_ok=True)
    gov.check_kill_switch()
    decision = decide(mission, policy, gov)
    try:
        result = act(decision, mission, policy, gov, out_dir)
        status = result.get("status")
    except GovernorError as e:
        result, status = {"status": "blocked", "reason": str(e)}, "blocked"
    gov.record("tick", action=decision.get("action"),
               objective=decision.get("objective_id"),
               rationale=decision.get("rationale"), result=result)
    return decision, result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--once", action="store_true")
    ap.add_argument("--daemon", action="store_true")
    ap.add_argument("--root", default=HERE)
    args = ap.parse_args()
    if args.daemon:
        _, policy = load(args.root)
        cadence = policy["limits"]["tick_seconds"]
        while True:
            try:
                d, r = tick(args.root)
                print(json.dumps({"action": d.get("action"), "result": r}))
            except GovernorError as e:
                print(json.dumps({"halted": str(e)}))
                break
            time.sleep(cadence)
    else:
        d, r = tick(args.root)
        print(json.dumps({"decision": d, "result": r}, indent=2))


if __name__ == "__main__":
    main()
