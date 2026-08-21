# Guthrie HTTP service — put him on the website

A small FastAPI wrapper around the `guthrie` skill's retrieval brain
(`../kernel.py`) so the cureledger / pku-commons site can call Guthrie directly.
Same cite-or-refuse contract, same code path the eval scored.

## Run locally

```bash
cd guthrie
python -m venv .venv && ./.venv/bin/pip install -r serve/requirements.txt
export ANTHROPIC_API_KEY=sk-...
export GUTHRIE_INDEX_DIR=$PWD/pku_index      # or unpack pku_index_v0.tar.gz here
./.venv/bin/uvicorn serve:app --app-dir serve --port 8000

curl localhost:8000/health
curl -s localhost:8000/api/ask -H 'content-type: application/json' \
  -d '{"question":"How does pegvaliase lower blood phe?"}' | jq .answer
```

## Deploy (Railway / Fly — same as the old ElizaOS agent)

The `Dockerfile` bakes `kernel.py`, the index, and the MiniLM weights into the
image, so the container is self-contained and starts offline.

```bash
docker build -f serve/Dockerfile -t guthrie-svc .      # run from guthrie/
# Railway: push the image, set ONE secret -> ANTHROPIC_API_KEY
# Fly:     fly launch --dockerfile serve/Dockerfile ; fly secrets set ANTHROPIC_API_KEY=sk-...
```

Set `GUTHRIE_CORS_ORIGINS` to your site's origins (default already allows
cureledger.com + localhost:3000).

## Endpoints

| method | path | body | returns |
|---|---|---|---|
| GET | `/health` | — | `{status, n_chunks, index_version, answer_model}` |
| POST | `/api/ask` | `{question, k?, mode?}` | `{answer, citations, hits, refused, medical_flag}` |
| POST | `/api/search` | `{query, k?, source?}` | `[{citation, title, url, source, year, score}]` |

`mode`: `"brief"` (2-4 sentences) or `"full"`. `source` filter: `literature` /
`guideline_fulltext` / `commons`.

## Wiring it into the site (replaces the ElizaOS upstream)

The current `cureledger-site/app/api/chat/route.ts` polls `ELIZAOS_API_URL`
sessions. Point it at this service instead — one `fetch`, no polling:

```ts
// route.ts (Next.js) — set GUTHRIE_API_URL to the deployed service
export async function POST(req: Request) {
  const { message } = await req.json();
  const r = await fetch(`${process.env.GUTHRIE_API_URL}/api/ask`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ question: message, mode: "brief" }),
  });
  const data = await r.json(); // {answer, citations, hits, refused, medical_flag}
  return Response.json(data);
}
```

Render `answer` as the reply, and turn `hits` into clickable source chips
(each has a PubMed/Commons `url`). `refused` and `medical_flag` let the UI show
the right affordance (a "rephrase" hint, or a "talk to your clinic" note).

Because the persona, refusals, and citations all live in `kernel.py` now, there
is no character file and no agent server to keep alive — just this one stateless
container.
