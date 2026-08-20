#!/usr/bin/env python3
"""Guthrie — build the hybrid retrieval index.

Reads the raw corpus (build/raw/*.jsonl), normalizes every document into
provenance-carrying chunks, and builds a portable hybrid index:

  * dense:  sentence-transformers all-MiniLM-L6-v2 embeddings (CPU, no API key)
  * lexical: BM25 (rank_bm25) over tokenized chunk text

Persisted to guthrie/pku_index/ :
  chunks.sqlite   — one row per chunk (text + full provenance + citation id)
  embeddings.npy  — float32 [n_chunks, 384], row order == sqlite rowid-1
  bm25.pkl        — tokenized corpus for BM25
  meta.json       — build stats, model name, version

One command rebuilds from source. Everything downstream (kernel.py) only reads
this directory, so the brain is fully reproducible from the fetch scripts.
"""
import os
# Force plain-HTTPS weight downloads. HuggingFace's newer Xet transfer client
# uses a protocol that is not reachable from the sandbox; plain HTTPS is.
os.environ.setdefault("HF_HUB_DISABLE_XET", "1")
os.environ.setdefault("HF_XET_DISABLE", "1")
os.environ.setdefault("HF_HUB_ENABLE_HF_TRANSFER", "0")

import json, pickle, re, sqlite3, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
OUT = os.path.abspath(os.path.join(HERE, "..", "pku_index"))
MODEL = "sentence-transformers/all-MiniLM-L6-v2"

_word = re.compile(r"[a-z0-9]+")
def tokenize(text):
    return _word.findall(text.lower())

def literature_chunks(path):
    """One chunk per abstract (abstracts are already ~paragraph sized)."""
    for line in open(path, encoding="utf-8"):
        r = json.loads(line)
        text = f"{r['title']}\n\n{r['abstract']}"
        yield {
            "source": "literature",
            "citation_id": f"PMID:{r['pmid']}",
            "cite_label": f"PMID:{r['pmid']}",
            "title": r["title"],
            "text": text,
            "year": str(r.get("year") or "")[:4],
            "journal": r.get("journal") or "",
            "url": f"https://pubmed.ncbi.nlm.nih.gov/{r['pmid']}/",
            "extra": json.dumps({"doi": r.get("doi"), "pmcid": r.get("pmcid"),
                                 "pub_types": r.get("pub_types", [])[:4]}),
        }

def guideline_chunks(path):
    """Section-level chunks from PMC full-text guidelines."""
    if not os.path.exists(path):
        return
    for line in open(path, encoding="utf-8"):
        r = json.loads(line)
        for sec in r["sections"]:
            body = sec["text"]
            if len(body) < 200:
                continue
            head = sec.get("heading") or ""
            yield {
                "source": "guideline_fulltext",
                "citation_id": f"PMID:{r['pmid']}",
                "cite_label": f"PMID:{r['pmid']}",
                "title": f"{r['title']} — {head}" if head else r["title"],
                "text": (f"{head}\n\n{body}" if head else body),
                "year": "",
                "journal": "",
                "url": f"https://www.ncbi.nlm.nih.gov/pmc/articles/{r['pmcid']}/",
                "extra": json.dumps({"pmcid": r["pmcid"], "heading": head}),
            }

def market_chunks(path):
    for line in open(path, encoding="utf-8"):
        r = json.loads(line)
        yield {
            "source": "commons",
            "citation_id": f"Commons:{r['citation_id']}",
            "cite_label": f"Commons:{r['citation_id']}",
            "title": r["doc_title"] + (f" — {r['heading']}" if r.get("heading") else ""),
            "text": r["text"],
            "year": "",
            "journal": "",
            "url": r["provenance"],
            "extra": json.dumps({"provenance": r["provenance"], "heading": r.get("heading")}),
        }

def collect():
    chunks = []
    chunks += list(literature_chunks(os.path.join(RAW, "literature.jsonl")))
    chunks += list(guideline_chunks(os.path.join(RAW, "guidelines_fulltext.jsonl")))
    chunks += list(market_chunks(os.path.join(RAW, "market.jsonl")))
    return chunks

def main():
    os.makedirs(OUT, exist_ok=True)
    t0 = time.time()
    chunks = collect()
    n = len(chunks)
    by_src = {}
    for c in chunks:
        by_src[c["source"]] = by_src.get(c["source"], 0) + 1
    print(f"collected {n} chunks: {by_src}")

    # --- SQLite: chunk text + provenance ---
    db = os.path.join(OUT, "chunks.sqlite")
    if os.path.exists(db):
        os.remove(db)
    con = sqlite3.connect(db)
    con.execute("""CREATE TABLE chunks(
        rowid INTEGER PRIMARY KEY, source TEXT, citation_id TEXT, cite_label TEXT,
        title TEXT, text TEXT, year TEXT, journal TEXT, url TEXT, extra TEXT)""")
    con.executemany(
        "INSERT INTO chunks VALUES(?,?,?,?,?,?,?,?,?,?)",
        [(i + 1, c["source"], c["citation_id"], c["cite_label"], c["title"],
          c["text"], c["year"], c["journal"], c["url"], c["extra"])
         for i, c in enumerate(chunks)])
    con.commit(); con.close()

    # --- BM25 lexical ---
    from rank_bm25 import BM25Okapi
    tokenized = [tokenize(c["text"]) for c in chunks]
    bm25 = BM25Okapi(tokenized)
    with open(os.path.join(OUT, "bm25.pkl"), "wb") as f:
        pickle.dump({"tokenized": tokenized}, f)
    print(f"BM25 built over {n} docs")

    # --- Dense embeddings ---
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(MODEL, device="cpu")
    emb = model.encode([c["text"] for c in chunks], batch_size=64,
                       show_progress_bar=True, normalize_embeddings=True)
    emb = np.asarray(emb, dtype=np.float32)
    np.save(os.path.join(OUT, "embeddings.npy"), emb)
    print(f"embeddings: {emb.shape}")

    meta = {"version": "v0", "model": MODEL, "n_chunks": n, "by_source": by_src,
            "embedding_dim": int(emb.shape[1]),
            "built_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "build_seconds": round(time.time() - t0, 1)}
    json.dump(meta, open(os.path.join(OUT, "meta.json"), "w"), indent=2)
    print(f"DONE in {meta['build_seconds']}s -> {OUT}")
    print(json.dumps(meta, indent=2))

if __name__ == "__main__":
    main()
