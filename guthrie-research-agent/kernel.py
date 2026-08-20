"""Guthrie — PKU retrieval brain (kernel sidecar).

Loaded automatically when the `guthrie` skill is loaded. Exposes:

    pku_search(query, k=8, source=None)  -> list[dict]  ranked chunks + citations
    pku_ask(question, k=8, mode="brief") -> dict         grounded, cited answer
    guthrie_index_info()                 -> dict          index build metadata

Design contract (see CORPUS.md):
  * CITE OR REFUSE. Every literature claim carries a [PMID:xxxx]; every market
    claim a [Commons:doc]. If retrieval is weak, Guthrie says so instead of
    inventing a citation.
  * NO medical advice / diagnosis / dosing for an individual. Guthrie reports
    what the literature says and routes care decisions to a clinician.
  * The index is local: BM25 + MiniLM dense, score-fused. It is located via
    $GUTHRIE_INDEX_DIR, else the `pku_index/` folder beside this file. If it is
    missing, run guthrie/build/{fetch_corpus,build_market_layer,build_index}.py
    or unpack the pku_index_v0.tar.gz artifact there.

This module is written to pass the skill-sidecar gate: only imports, defs, and
literal constants at top level; all computed state lives inside functions.
"""
import os
import re

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
DEFAULT_MIN_RELEVANCE = 0.35
MEDICAL_PATTERN = (
    r"\b(should i|my (child|kid|son|daughter|baby)|my (phe|level)s?\b|"
    r"how much .*(should|can) (i|we|my)|is it safe for (me|my)|"
    r"what dose|change (my|our|the) (dose|diet)|stop taking)\b")
GUTHRIE_SYSTEM = (
    "You are Guthrie, the PKU community research agent, named for Robert Guthrie "
    "(newborn-screening heel-prick test, 1963). You answer strictly from the "
    "CONTEXT passages provided, which are retrieved from the PKU literature "
    "(PubMed) and the PKU Commons infrastructure. RULES: "
    "(1) Cite every factual claim inline using the bracket label shown on each "
    "passage, e.g. [PMID:12345678] or [Commons:leaderboard]. "
    "(2) Never invent a citation or a PMID. If the context does not support an "
    "answer, say you do not have a grounded source and suggest the PKU Commons "
    "blog or a clinician. "
    "(3) You do not give medical advice, diagnosis, or dosing for an individual; "
    "you explain what the literature reports and defer care decisions to a "
    "clinician. "
    "(4) Be concise and direct. No em-dashes.")


def guthrie_state():
    """Lazy module-level cache (non-underscore name so the sidecar gate allows it)."""
    g = globals()
    if "GUTHRIE_STATE" not in g:
        g["GUTHRIE_STATE"] = {"loaded": False}
    return g["GUTHRIE_STATE"]


def index_dir():
    """Locate the index: $GUTHRIE_INDEX_DIR, else pku_index/ beside this file."""
    d = os.environ.get("GUTHRIE_INDEX_DIR")
    if d:
        return d
    import sys
    here = os.path.dirname(sys._getframe().f_code.co_filename)
    return os.path.join(here or ".", "pku_index")


def tokenize(text):
    return re.findall(r"[a-z0-9]+", text.lower())


def load_index():
    """Load the SQLite chunks, embeddings, BM25 corpus, and embed model once."""
    st = guthrie_state()
    if st.get("loaded"):
        return st
    os.environ.setdefault("HF_HUB_DISABLE_XET", "1")
    os.environ.setdefault("HF_XET_DISABLE", "1")
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
    import json, pickle, sqlite3
    import numpy as np
    idx = index_dir()
    dbp = os.path.join(idx, "chunks.sqlite")
    if not os.path.exists(dbp):
        raise FileNotFoundError(
            f"Guthrie index not found at {idx}. Build it "
            "(guthrie/build/*.py) or set GUTHRIE_INDEX_DIR to a prebuilt copy.")
    con = sqlite3.connect(dbp)
    con.row_factory = sqlite3.Row
    rows = [dict(r) for r in con.execute(
        "SELECT rowid, source, citation_id, cite_label, title, text, year, "
        "journal, url, extra FROM chunks ORDER BY rowid")]
    con.close()
    emb = np.load(os.path.join(idx, "embeddings.npy"))
    with open(os.path.join(idx, "bm25.pkl"), "rb") as f:
        tokenized = pickle.load(f)["tokenized"]
    from rank_bm25 import BM25Okapi
    from sentence_transformers import SentenceTransformer
    st.update(rows=rows, emb=emb, bm25=BM25Okapi(tokenized),
              model=SentenceTransformer(EMBED_MODEL, device="cpu"),
              meta=json.load(open(os.path.join(idx, "meta.json"))),
              loaded=True)
    return st


def minmax(x):
    import numpy as np
    x = np.asarray(x, dtype=np.float32)
    lo, hi = x.min(), x.max()
    return (x - lo) / (hi - lo) if hi > lo else np.zeros_like(x)


def pku_search(query, k=8, source=None, alpha=0.5):
    """Hybrid retrieval. Returns k chunks ranked by fused BM25 + dense score.

    alpha  = dense weight (0 = pure lexical, 1 = pure semantic).
    source = optional filter: 'literature' | 'guideline_fulltext' | 'commons'.
    Each result carries its citation label + url so the caller can cite it.
    The raw dense cosine is kept per hit (used as the absolute relevance gate).
    """
    import numpy as np
    st = load_index()
    rows, emb, bm25, model = st["rows"], st["emb"], st["bm25"], st["model"]
    bm_scores = np.asarray(bm25.get_scores(tokenize(query)), dtype=np.float32)
    q_emb = model.encode([query], normalize_embeddings=True)[0].astype(np.float32)
    dense = emb @ q_emb  # cosine (rows are L2-normalized)
    fused = alpha * minmax(dense) + (1 - alpha) * minmax(bm_scores)
    out = []
    for i in np.argsort(-fused):
        r = rows[int(i)]
        if source and r["source"] != source:
            continue
        out.append({
            "rank": len(out) + 1, "citation": r["cite_label"], "source": r["source"],
            "title": r["title"], "year": r["year"], "journal": r["journal"],
            "url": r["url"], "text": r["text"],
            "score": round(float(fused[int(i)]), 4),
            "dense": round(float(dense[int(i)]), 4),
            "bm25": round(float(bm_scores[int(i)]), 4)})
        if len(out) >= k:
            break
    return out


def format_context(hits):
    blocks = []
    for h in hits:
        head = f"[{h['citation']}] ({h['source']}, {h['year']}) {h['title']}".strip()
        blocks.append(f"{head}\n{h['text'][:1400]}")
    return "\n\n---\n\n".join(blocks)


def get_host():
    """Resolve the injected `host` singleton (kernel global, or up the stack)."""
    if "host" in globals():
        return globals()["host"]
    import inspect
    for fr in inspect.stack():
        h = fr.frame.f_globals.get("host")
        if h is not None:
            return h
    return None


def pku_ask(question, k=8, mode="brief", min_relevance=0.35, llm=None):
    """Grounded, cited answer. mode: 'brief' | 'full'.

    Returns {answer, citations, hits, refused, medical_flag}. Refuses (no
    fabricated citation) when retrieval is weak.

    Relevance is judged on the top hit's RAW dense cosine (not the min-max fused
    score, whose top is ~1.0 for any query). On-topic PKU questions score
    ~0.55-0.70; off-topic questions score < 0.25. Default gate 0.35.

    The grounding LLM is injectable so the SAME refusal + citation logic runs in
    every deployment. `llm` is a callable (prompt, system, max_tokens) -> {text}.
    If None, it falls back to the injected host.llm (inside Claude Science). The
    standalone HTTP service (serve/serve.py) passes an Anthropic-API llm here so
    it is literally this code path, not a reimplementation.
    """
    if llm is None:
        host = get_host()
        if host is not None:
            llm = lambda prompt, system, max_tokens: host.llm(
                prompt, system=system, max_tokens=max_tokens)
    hits = pku_search(question, k=k)
    top = hits[0]["dense"] if hits else -1.0
    medical = bool(re.search(MEDICAL_PATTERN, question, re.I))

    if not hits or top < min_relevance:  # weak-retrieval refusal
        return {"answer": ("I do not have a grounded source for that in the PKU "
                           "corpus. Try rephrasing, or see the PKU Commons blog / "
                           "a metabolic clinician. I will not guess a citation."),
                "citations": [], "hits": hits, "refused": True, "medical_flag": medical}

    disclaimer = ("\n\nNote: this is what the literature reports, not medical "
                  "advice for your situation. Dosing and diet changes are "
                  "decisions for your metabolic clinician.") if medical else ""
    length = "2-4 sentences" if mode == "brief" else "a thorough, well-structured answer"
    prompt = (f"CONTEXT (each passage is prefixed with its citation label):\n\n"
              f"{format_context(hits)}\n\nQUESTION: {question}\n\n"
              f"Answer in {length}, citing inline with the bracket labels above. "
              f"If the context is insufficient, say so plainly.")

    if llm is None:  # offline (e.g. eval without an LLM) — retrieval only
        return {"answer": None, "citations": [h["citation"] for h in hits],
                "hits": hits, "refused": False, "medical_flag": medical,
                "note": "no LLM available; returning retrieval only"}

    resp = llm(prompt, system=GUTHRIE_SYSTEM,
               max_tokens=900 if mode == "full" else 400)
    text = (resp.get("text") or "").strip() + disclaimer
    cited = sorted(set(re.findall(r"\[(?:PMID:\d+|Commons:[a-z0-9\-]+)\]", text)))
    return {"answer": text, "citations": cited, "hits": hits,
            "refused": False, "medical_flag": medical}


def guthrie_index_info():
    """Return index build metadata (model, chunk counts, build time)."""
    return load_index()["meta"]
