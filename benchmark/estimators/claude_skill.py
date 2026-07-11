"""Harness adapter for the Claude phe-estimator Skill.

This is the single integration point between the Skill (phe-estimator/SKILL.md) and the
benchmark. It sends the Skill instructions + a case's label to a model, parses the JSON the
Skill is contracted to return, and hands the harness one `phe_mg` number.

The model caller is injected so this is provider-agnostic. YOU supply a function
    fn(system_prompt, user_prompt) -> str
that returns the model's text reply. The number path never leaves this file, so any
model works. Pick the wiring that matches how you (the tester) run:

--- 1. You ARE a coding agent (Claude Code, Cursor, etc.) — the decentralized path ---
No API key. You answer the cases yourself, in your own session. In a Python REPL
started from this repo, define a caller that returns what YOU (the agent) reply with
when handed the system + user prompt, then run the cases:

    from estimators import claude_skill, base
    import run_benchmark as rb, variance as var
    # `agent_reply` is however your harness lets you produce a completion for a
    # (system, user) pair — e.g. your own tool call, or reading your response back.
    claude_skill.set_model_caller(lambda system, user: agent_reply(system, user))
    var.run_variance(claude_skill.estimate, var.load_cases("low_protein_usda.jsonl"), runs=5)

--- 2. You have an Anthropic API key ---
    import os, anthropic
    _c = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    def call(system, user):
        m = _c.messages.create(model="claude-sonnet-4-5", max_tokens=1024,
                               temperature=0,           # temperature 0 = reproducible
                               system=system, messages=[{"role":"user","content":user}])
        return m.content[0].text
    claude_skill.set_model_caller(call)
    # then: python run_benchmark.py --estimator estimators.claude_skill \
    #           --testset low_protein_usda.jsonl --model claude-sonnet-4-5

--- 3. Any other provider (OpenAI, local model, ...) ---
Wire the same fn(system, user) -> str against your client. Set temperature 0.

Always pass --model (or PKU_BENCH_MODEL) so your result says which model ran it.
If no caller is set, estimate() raises — it never silently fabricates a number.
"""
import json, os, re

_HERE = os.path.dirname(os.path.abspath(__file__))
_SKILL_PATH = os.path.normpath(os.path.join(_HERE, "..", "..", "phe-estimator", "SKILL.md"))

_MODEL_CALLER = None


def set_model_caller(fn):
    """Register a callable fn(system_prompt: str, user_prompt: str) -> str (model text)."""
    global _MODEL_CALLER
    _MODEL_CALLER = fn


def _load_skill_instructions() -> str:
    with open(_SKILL_PATH) as fh:
        md = fh.read()
    # Drop the YAML front-matter; keep the instruction body as the system prompt.
    if md.startswith("---"):
        md = md.split("---", 2)[-1]
    return md.strip()


def _extract_json(text: str) -> dict:
    """Pull the first JSON object out of the model's reply."""
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if not m:
        raise ValueError(f"no JSON object in model reply: {text[:200]!r}")
    return json.loads(m.group(0))


def estimate(case: dict) -> dict:
    if _MODEL_CALLER is None:
        raise RuntimeError(
            "claude_skill.estimate: no model caller set. Call "
            "claude_skill.set_model_caller(fn) with fn(system, user)->str first "
            "(e.g. wrapping host.llm)."
        )
    label = case["label"]
    system = _load_skill_instructions()
    user = (
        "Estimate the phe for this food. Return ONLY the JSON object from your contract.\n\n"
        f"serving_size_g: {label.get('serving_size_g')}\n"
        f"protein_g_per_serving: {label.get('protein_g_per_serving')}\n"
        f"ingredients: {label.get('ingredients')}\n"
        f"portion: 1 serving\n"
    )
    reply = _MODEL_CALLER(system, user)
    obj = _extract_json(reply)
    if "error" in obj and "phe_mg" not in obj:
        # Skill refused to parse the label — surface as a crash-free miss with no number.
        raise ValueError(f"Skill returned error: {obj['error']}")
    return {"phe_mg": float(obj["phe_mg"]), "meta": obj}
