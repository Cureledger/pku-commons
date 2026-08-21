#!/usr/bin/env python3
"""Guthrie corpus — the 'market' layer.

Chunks the PKU Commons + Phebe documents (see CORPUS.md Layer 2) into
section-level records with a [Commons:<doc>] citation id each. Output:
build/raw/market.jsonl
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
# repo root = .../pku-commons ; phebe is a sibling under cureledger
COMMONS = os.path.abspath(os.path.join(HERE, "..", ".."))
CURELEDGER = os.path.abspath(os.path.join(COMMONS, ".."))

# (citation_id, absolute path, human title, url-or-path for provenance)
SOURCES = [
    ("benchmark",    os.path.join(COMMONS, "benchmark/BENCHMARK.md"),  "PKU Commons Benchmark", "pku-commons/benchmark/BENCHMARK.md"),
    ("leaderboard",  os.path.join(COMMONS, "benchmark/leaderboard.md"),"PKU Commons Leaderboard", "pku-commons/benchmark/leaderboard.md"),
    ("peer-review",  os.path.join(COMMONS, "docs/PEER-REVIEW.md"),     "PKU Commons Peer-Review Model", "pku-commons/docs/PEER-REVIEW.md"),
    ("pain-points",  os.path.join(COMMONS, "docs/pain-points.md"),     "TruPKU Pain Points", "pku-commons/docs/pain-points.md"),
    ("readme",       os.path.join(COMMONS, "README.md"),               "PKU Commons README", "pku-commons/README.md"),
    ("phebe-spec",   os.path.join(CURELEDGER, "phebe/APP-SPEC.md"),    "Phebe App Spec", "phebe/APP-SPEC.md"),
    ("phebe-thesis", os.path.join(CURELEDGER, "phebe/Phebe_Strategic_Thesis.md"), "Phebe Strategic Thesis", "phebe/Phebe_Strategic_Thesis.md"),
    ("scale-spec",   os.path.join(CURELEDGER, "phebe/PROMO-SCALE-SPEC.md"), "Phebe Scale Spec", "phebe/PROMO-SCALE-SPEC.md"),
    ("scale-handoff",os.path.join(CURELEDGER, "phebe/BODY-SCALE-HANDOFF.md"), "Phebe Body-Scale Handoff", "phebe/BODY-SCALE-HANDOFF.md"),
]

def chunk_markdown(text, min_chars=200):
    """Split on markdown headings into (heading, body) chunks."""
    lines = text.splitlines()
    chunks, cur_head, cur = [], None, []
    def flush():
        body = "\n".join(cur).strip()
        if body and len(body) >= min_chars:
            chunks.append((cur_head, body))
        elif body and chunks:  # merge tiny tail into previous
            h, b = chunks[-1]
            chunks[-1] = (h, b + "\n\n" + (f"{cur_head}\n" if cur_head else "") + body)
    for ln in lines:
        if re.match(r"^#{1,4}\s", ln):
            flush()
            cur_head = ln.lstrip("#").strip()
            cur = []
        else:
            cur.append(ln)
    flush()
    return chunks

def main():
    os.makedirs(RAW, exist_ok=True)
    n = 0
    with open(os.path.join(RAW, "market.jsonl"), "w") as f:
        for cid, path, title, prov in SOURCES:
            if not os.path.exists(path):
                print(f"  MISSING: {path}")
                continue
            text = open(path, encoding="utf-8").read()
            chunks = chunk_markdown(text)
            for i, (head, body) in enumerate(chunks):
                rec = {
                    "source": "commons",
                    "citation_id": cid,
                    "doc_title": title,
                    "provenance": prov,
                    "heading": head,
                    "text": (f"{head}\n\n{body}" if head else body),
                    "chunk_ix": i,
                }
                f.write(json.dumps(rec) + "\n")
                n += 1
            print(f"  {cid}: {len(chunks)} chunks  ({title})")
    print(f"DONE: wrote {n} market chunks")

if __name__ == "__main__":
    main()
