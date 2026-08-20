"""Governor — enforces the operator's policy in code.

Nothing the model decides reaches the outside world without passing every check
here. The governor is deliberately dumb and strict: it does not reason, it gates.

Checks:
  * kill switch (HALT file) -> halt before any action
  * geo / sanctions screen  -> block banned or unknown jurisdictions
  * budget                  -> lifetime ceiling, per-action cap, rolling weekly cap
  * dry-run                 -> in dry_run mode, spends are logged, never executed

Every decision (allow / block / would-spend) is appended to ledger.jsonl with
the rationale, so the whole autonomous history is auditable after the fact.
"""
import json
import os
import time


class GovernorError(Exception):
    """Raised when an action is blocked. The loop catches and records it."""


class Governor:
    def __init__(self, policy, root="."):
        self.p = policy
        self.root = root
        self.ledger_path = os.path.join(root, "ledger.jsonl")

    # ---- ledger -------------------------------------------------------------
    def record(self, kind, **fields):
        row = {"ts": int(time.time()), "kind": kind, **fields}
        with open(self.ledger_path, "a") as f:
            f.write(json.dumps(row) + "\n")
        return row

    def _spend_rows(self):
        if not os.path.exists(self.ledger_path):
            return []
        out = []
        for line in open(self.ledger_path):
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            if r.get("kind") in ("spend", "would_spend") and "amount" in r:
                out.append(r)
        return out

    def spent_total(self):
        # only realized spend counts against the lifetime ceiling
        return sum(r["amount"] for r in self._spend_rows() if r["kind"] == "spend")

    def spent_last_week(self):
        cutoff = time.time() - 7 * 86400
        return sum(r["amount"] for r in self._spend_rows()
                   if r["kind"] == "spend" and r["ts"] >= cutoff)

    # ---- gates --------------------------------------------------------------
    def check_kill_switch(self):
        halt = os.path.join(self.root, self.p["kill_switch"]["halt_file"])
        if os.path.exists(halt):
            raise GovernorError("HALT file present — operator stopped by kill switch")

    def check_geo(self, jurisdiction):
        if not self.p["limits"].get("require_geo_check", True):
            return  # only reachable if no network is enabled
        banned = set(self.p["geo"]["banned_jurisdictions"])
        j = (jurisdiction or "").upper().strip()
        if not j:
            if self.p["geo"].get("block_on_unknown", True):
                raise GovernorError("geo blocked: unknown/missing jurisdiction")
            return
        # match country and any subdivision prefix (e.g. UA-43 under RU-flagged set)
        if j in banned or any(j.startswith(b) or b.startswith(j) for b in banned):
            raise GovernorError(f"geo blocked: jurisdiction {j} is banned")

    def check_and_reserve_spend(self, amount, rationale, counterparty=None,
                                jurisdiction=None):
        """The money gate. Returns 'executed' | 'would_spend' | raises."""
        self.check_kill_switch()
        b = self.p["budget"]
        if amount < 0:
            raise GovernorError("negative spend")
        if amount > b["per_action_max"]:
            raise GovernorError(
                f"per-action cap: {amount} > {b['per_action_max']}")
        if self.spent_last_week() + amount > b["per_week_max"]:
            raise GovernorError(
                f"weekly cap: {self.spent_last_week()}+{amount} > {b['per_week_max']}")
        if self.spent_total() + amount > b["ceiling_total"]:
            raise GovernorError(
                f"lifetime ceiling: {self.spent_total()}+{amount} > {b['ceiling_total']}")
        if jurisdiction is not None:
            self.check_geo(jurisdiction)
        # passed all caps. dry_run logs intent; live records realized spend.
        if self.p["mode"]["execution"] == "dry_run":
            self.record("would_spend", amount=amount, currency=b["currency"],
                        counterparty=counterparty, jurisdiction=jurisdiction,
                        rationale=rationale)
            return "would_spend"
        self.record("spend", amount=amount, currency=b["currency"],
                    counterparty=counterparty, jurisdiction=jurisdiction,
                    rationale=rationale)
        return "executed"

    def enabled_networks(self):
        return [n for n in self.p.get("networks", []) if n.get("enabled")]

    def budget_snapshot(self):
        b = self.p["budget"]
        return {"spent_total": self.spent_total(),
                "spent_last_week": self.spent_last_week(),
                "ceiling_total": b["ceiling_total"],
                "per_action_max": b["per_action_max"],
                "per_week_max": b["per_week_max"],
                "remaining": b["ceiling_total"] - self.spent_total()}
