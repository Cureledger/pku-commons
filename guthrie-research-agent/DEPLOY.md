# Deploying the Guthrie research agent

The FastAPI service (`serve/serve.py`) answers PKU questions with cite-or-refuse
grounding over a hybrid BM25 + MiniLM index. It lives here in **pku-commons** and
is deployed on **Railway** (Docker). The website at pku-commons.org calls its
`/api/ask` from the browser (CORS-allowed); there is no site-side proxy.

## The index is built in CI, not committed

The ~40MB index (`chunks.sqlite`, `embeddings.npy`, `bm25.pkl`) is git-ignored.
It is rebuilt from public sources (PubMed E-utilities — no API key) by
**`.github/workflows/build-index.yml`** and published as the **`index-latest`**
GitHub Release asset. `serve/Dockerfile` downloads that asset at build time.

This keeps git clean, keeps deploys fast and reproducible, and lets the corpus
refresh on a schedule (weekly + on-demand) with no maintainer.

## First-time deploy (do these in order)

1. **Build the index once.** GitHub → Actions → *Build PKU index* → *Run
   workflow*. It fetches the corpus, builds the index, and creates the
   `index-latest` prerelease with `pku_index.tar.gz`. (Until this exists, the
   Docker build's download step 404s by design.)

2. **Create the Railway service** from this repo:
   - Root Directory: `guthrie-research-agent`
   - Builder: Dockerfile (`railway.toml` sets `dockerfilePath = serve/Dockerfile`)
   - Variable: `ANTHROPIC_API_KEY` = a funded key on a workspace with model
     access. (A key authenticates to its owning workspace — check the
     `anthropic-workspace-id` response header if calls 401/403.)

3. **Deploy.** Railway builds the image (pulling `index-latest`), runs the
   `startCommand`, and health-checks `GET /health`.

4. **Verify:** `GET https://<service>.up.railway.app/health` →
   `{status, n_chunks, model}`, then `POST /api/ask {"question": "..."}`.

## Environment variables

| Variable | Default | Purpose |
|---|---|---|
| `ANTHROPIC_API_KEY` | — (required) | Grounding LLM |
| `GUTHRIE_ANSWER_MODEL` | `claude-haiku-4-5-20251001` | Answer model (use a **live** id; dated snapshots get retired → 404) |
| `GUTHRIE_CORS_ORIGINS` | pku-commons.org + www + cureledger.com + localhost | Browser origins allowed to call `/api/*` |
| `GUTHRIE_API_TOKEN` | unset (open) | If set, `/api/*` requires `Authorization: Bearer <token>`. Not usable from the public widget — reserve for server-to-server callers |
| `GUTHRIE_RATE_LIMIT_PER_MIN` | `20` | Per-IP sliding-window cap (denial-of-wallet guard) |
| `TURNSTILE_SECRET_KEY` | unset (off) | If set, `/api/ask` requires a valid Cloudflare Turnstile token and verifies it server-side. See below |

## Bot protection (Cloudflare Turnstile)

The browser-friendly abuse guard for the public widget (a bearer token can't be
used from a public page). It ships **dormant** and turns on only when both keys
are set — activate it alongside the other apps:

1. In Cloudflare Turnstile, create a widget for `pku-commons.org` — use a
   **Non-Interactive** or **Invisible** type so it needs no visible UI. You get a
   **site key** (public) and a **secret key**.
2. **Secret** → set `TURNSTILE_SECRET_KEY` in the Railway service Variables (same
   value type as the other apps' `TURNSTILE_SECRET_KEY`).
3. **Site key** (public) → give it to the widget via **one** of:
   `window.GUTHRIE_TURNSTILE_SITEKEY`, a `data-turnstile-sitekey` attr on the
   widget `<script>`, or `DEFAULT_TURNSTILE_SITEKEY` in `docs/assets/guthrie-widget.js`.
   This is the same value as the other apps' `NEXT_PUBLIC_TURNSTILE_SITE_KEY`.

With the secret set but no site key wired, `/api/ask` will 403 the widget (fail
closed) — set both together, or neither. The widget sends the token in the
`cf-turnstile-response` header; the server verifies it via Cloudflare siteverify.

## Growing / refreshing the corpus

The corpus **accumulates** across runs — it does not re-snapshot the most-recent
N. Each *Build PKU index* run:

1. downloads the corpus grown so far (`literature.jsonl.gz` + `fetched_ids.txt`
   from the `index-latest` release),
2. fetches up to **`max_records`** *new* PubMed records not yet attempted
   (deduped by PMID; `fetched_ids.txt` tracks every attempted id so abstract-less
   records don't stall progress),
3. rebuilds the index and republishes both the index and the grown corpus.

So to **grow it in chunks**, just re-run the workflow — each run adds another
`max_records` and prints `remaining` until the universe (~9.7k records) is
covered. Set **`max_records = 0`** to fetch everything remaining in one run. The
weekly schedule keeps adding/refreshing on its own. After any run, redeploy on
Railway so the image pulls the new `index-latest` asset.
