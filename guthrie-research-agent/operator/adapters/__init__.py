"""Network adapters — the only place that touches an external bounty network.

Each adapter exposes:
    post_bounty(task, amount) -> ref     # post a task, fund escrow (bounded pay)
    list_tasks()             -> [ ... ]  # discover claimable work
    jurisdiction()           -> ISO code # for the governor's geo screen

Adapters are only invoked in LIVE mode, and only after the governor has already
authorized the spend and geo. In dry_run the loop never calls an adapter. Wallet
keys live in the adapter's own env (e.g. TASKBOUNTY_API_KEY, wallet secret), read
at call time — never passed through the loop or logged.

Nothing is enabled by default. To add a live network: implement the class,
register it below, then flip enabled: true in policy.yaml.
"""


class AdapterNotConfigured(Exception):
    pass


class TaskBountyAdapter:
    """Skeleton for task-bounty.com.

    IMPORTANT: TaskBounty appears to be an EARN network, not a post-a-bounty
    network — agents point at open GitHub bug bounties, fix them, and get paid
    (USDC/ETH/BTC/USD). So the operator would use it to EARN toward the mission
    budget, not to spend.

    UNCONFIRMED API surface (from a 2026 web read of task-bounty.com/for-agents,
    NOT verified against live docs — CONFIRM before enabling): agent registration
    via a PATCH /api/v1/agents/{id} style endpoint (Bearer key); task discovery
    via signed webhook (an HMAC-SHA256 signature header) or a Supabase realtime
    channel. Treat every field here as a placeholder to check against the current
    docs at implementation time, not as fact.

    So `list_tasks` here is a discovery/earn surface; there is no post_bounty.
    Fill in when you register an agent + wallet. Inert now so dry-run needs no key.
    """
    id = "taskbounty"
    role = "earn"  # earn | post

    def jurisdiction(self):
        # network operating jurisdiction; the governor screens this + counterparties
        return "US"

    def list_tasks(self):
        raise AdapterNotConfigured("taskbounty adapter not implemented — dry-run only")

    def claim_and_submit(self, task_id, fix):
        raise AdapterNotConfigured("taskbounty adapter not implemented — dry-run only")


_REGISTRY = {"taskbounty": TaskBountyAdapter}


def get_adapter(network_id):
    if network_id not in _REGISTRY:
        raise AdapterNotConfigured(f"no adapter registered for {network_id!r}")
    return _REGISTRY[network_id]()
