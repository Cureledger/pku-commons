#!/usr/bin/env python3
"""Guthrie as a standalone HTTP service.

Wraps the guthrie skill's retrieval brain (kernel.py) behind a small FastAPI app
so the cureledger / pku-commons website can call it directly. This calls
kernel.pku_ask itself (not a copy) and only injects the grounding LLM via the
Anthropic API (the skill's host.llm is not present outside Claude Science), so
the refusal gate, medical flag, and citation logic are literally the same code
the eval scored.

    ANTHROPIC_API_KEY=sk-...  GUTHRIE_INDEX_DIR=./pku_index  uvicorn serve:app

Endpoints:
    GET  /health        -> {status, n_chunks, model}
    POST /api/ask       {question, k?, mode?} -> {answer, citations, hits, refused, medical_flag}
    POST /api/search    {query, k?, source?}  -> [{citation, title, score, url, ...}]

The answer contract is identical to the skill: cite-or-refuse, medical-advice
flag + clinician deferral, off-topic refusal. This is the same code path the
eval scored, so the number on the website is the number in eval/report.md.
"""
import hmac
import os
import re
import sys
import time
from collections import deque

from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

# import the skill's retrieval brain (kernel.py sits one dir up)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import kernel  # noqa: E402

# Current, live Haiku snapshot. The dated 3.5 snapshots get retired by Anthropic
# over time (a retired id returns HTTP 404) — the same failure that took the chat
# agent down — so default to the current generation. Override per-deploy with
# GUTHRIE_ANSWER_MODEL. The scored gate (refusal, citations, medical flag) lives
# in kernel.py, not the LLM; the model only phrases the grounded answer.
ANSWER_MODEL = os.environ.get("GUTHRIE_ANSWER_MODEL", "claude-haiku-4-5-20251001")
ALLOWED_ORIGINS = [
    o.strip()
    for o in os.environ.get(
        "GUTHRIE_CORS_ORIGINS",
        "https://pku-commons.org,https://www.pku-commons.org,"
        "https://cureledger.com,https://www.cureledger.com,http://localhost:3000",
    ).split(",")
    if o.strip()
]

# This service makes metered Anthropic calls, so /api/* is protected against
# denial-of-wallet abuse two ways:
#   1. Rate limiting (always on) — per-IP sliding window. One Railway replica
#      runs this process, so an in-memory counter is effective.
#   2. Optional shared token — when GUTHRIE_API_TOKEN is set, callers must send
#      `Authorization: Bearer <token>`. Unset = open (so an existing server-side
#      caller keeps working until you configure the token). CORS only limits
#      browsers; a direct curl bypasses it, which is why these apply server-side.
API_TOKEN = os.environ.get("GUTHRIE_API_TOKEN", "").strip()
RATE_LIMIT_MAX = int(os.environ.get("GUTHRIE_RATE_LIMIT_PER_MIN", "20"))
RATE_LIMIT_WINDOW = 60.0

app = FastAPI(title="Guthrie - PKU research agent", version="0")
app.add_middleware(
    CORSMiddleware, allow_origins=ALLOWED_ORIGINS, allow_methods=["*"],
    allow_headers=["*"],
)

_rl_hits: dict[str, deque] = {}


@app.middleware("http")
async def rate_limit(request: Request, call_next):
    if request.url.path.startswith("/api/"):
        ip = (
            request.headers.get("x-forwarded-for", "").split(",")[0].strip()
            or (request.client.host if request.client else "unknown")
        )
        now = time.monotonic()
        dq = _rl_hits.setdefault(ip, deque())
        while dq and now - dq[0] > RATE_LIMIT_WINDOW:
            dq.popleft()
        if len(dq) >= RATE_LIMIT_MAX:
            return JSONResponse({"detail": "Too many requests"}, status_code=429)
        dq.append(now)
    return await call_next(request)


def require_token(authorization: str | None = Header(default=None)):
    if not API_TOKEN:
        return  # auth disabled until GUTHRIE_API_TOKEN is set
    if not authorization or not hmac.compare_digest(authorization, f"Bearer {API_TOKEN}"):
        raise HTTPException(status_code=401, detail="Unauthorized")


class AskBody(BaseModel):
    question: str = Field(min_length=1, max_length=2000)
    k: int = Field(default=8, ge=1, le=20)
    mode: str = Field(default="brief", max_length=32)
    min_relevance: float = Field(default=0.35, ge=0.0, le=1.0)


class SearchBody(BaseModel):
    query: str = Field(min_length=1, max_length=2000)
    k: int = Field(default=8, ge=1, le=20)
    source: str | None = Field(default=None, max_length=64)


def _anthropic_llm(prompt, system, max_tokens):
    """The grounding call, via the Anthropic API (stands in for host.llm)."""
    import anthropic
    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY
    msg = client.messages.create(
        model=ANSWER_MODEL, max_tokens=max_tokens, system=system,
        messages=[{"role": "user", "content": prompt}])
    return {"text": "".join(b.text for b in msg.content if b.type == "text")}


@app.get("/health")
def health():
    info = kernel.guthrie_index_info()
    return {"status": "ok", "n_chunks": info["n_chunks"],
            "index_version": info["version"], "answer_model": ANSWER_MODEL}


@app.post("/api/ask")
def ask(body: AskBody, _=Depends(require_token)):
    # SAME code path as the skill + eval: kernel.pku_ask owns the refusal gate,
    # medical flag, and citation logic. We only inject the grounding LLM.
    r = kernel.pku_ask(body.question, k=body.k, mode=body.mode,
                       min_relevance=body.min_relevance, llm=_anthropic_llm)
    # trim hit payload for the wire (drop full passage text)
    r["hits"] = [{"citation": h["citation"], "title": h["title"],
                  "url": h["url"], "source": h["source"],
                  "score": h["score"]} for h in r["hits"]]
    return r


@app.post("/api/search")
def search(body: SearchBody, _=Depends(require_token)):
    hits = kernel.pku_search(body.query, k=body.k, source=body.source)
    return [{"citation": h["citation"], "title": h["title"], "url": h["url"],
             "source": h["source"], "year": h["year"], "score": h["score"]}
            for h in hits]
