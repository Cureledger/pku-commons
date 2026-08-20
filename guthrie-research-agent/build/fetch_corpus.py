#!/usr/bin/env python3
"""Guthrie corpus fetch — PKU literature from NCBI E-utilities.

Reproducible, key-free pull of the PKU literature slice defined in
guthrie/CORPUS.md. Writes JSONL to build/raw/. One command rebuilds; --since
does an incremental refresh so the corpus stays live without a maintainer.

    python fetch_corpus.py                 # full pull (cap = --max, default 4000)
    python fetch_corpus.py --since 2026/01/01   # only records added since a date
    python fetch_corpus.py --max 500       # small pull for testing

No API key required. A contact email is attached when the host provides one.
"""
import argparse, json, os, sys, time, urllib.parse, urllib.request
import xml.etree.ElementTree as ET

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")

# Frozen retrieval universe (see CORPUS.md). Prioritized by pub type + recency.
CORE_QUERY = ('phenylketonuria OR phenylketonurias OR hyperphenylalaninemia '
              'OR "phenylalanine hydroxylase deficiency"')

# optional contact email (services work fine without it)
def _email():
    try:
        import builtins
        h = getattr(builtins, "host", None)
        if h is not None:
            return h.get_user_email()
    except Exception:
        pass
    return os.environ.get("NCBI_CONTACT_EMAIL")

def _params(extra):
    p = {"db": "pubmed", "tool": "guthrie-corpus", **extra}
    em = _email()
    if em:
        p["email"] = em
    return p

def _get(endpoint, extra, retries=4):
    url = f"{EUTILS}/{endpoint}?" + urllib.parse.urlencode(_params(extra))
    last = None
    for i in range(retries):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return r.read()
        except Exception as e:
            last = e
            time.sleep(1.5 * (i + 1))
    raise last

def esearch(query, since=None, retmax=100000):
    extra = {"term": query, "retmode": "json", "retmax": retmax,
             "sort": "pub+date", "usehistory": "y"}
    if since:
        extra["mindate"] = since
        extra["maxdate"] = "3000"
        extra["datetype"] = "edat"
    data = json.loads(_get("esearch.fcgi", extra))["esearchresult"]
    return data.get("idlist", []), int(data.get("count", 0))

def _text(el, path):
    node = el.find(path)
    return node.text.strip() if node is not None and node.text else None

def _parse_article(art):
    medline = art.find("MedlineCitation")
    if medline is None:
        return None
    pmid = _text(medline, "PMID")
    art_el = medline.find("Article")
    if art_el is None:
        return None
    title = _text(art_el, "ArticleTitle") or ""
    # abstract may have multiple labeled sections
    abs_parts = []
    for ab in art_el.findall("Abstract/AbstractText"):
        label = ab.get("Label")
        txt = "".join(ab.itertext()).strip()
        if txt:
            abs_parts.append(f"{label}: {txt}" if label else txt)
    abstract = "\n".join(abs_parts)
    journal = _text(art_el, "Journal/Title")
    year = (_text(art_el, "Journal/JournalIssue/PubDate/Year")
            or _text(art_el, "Journal/JournalIssue/PubDate/MedlineDate"))
    authors = []
    for a in art_el.findall("AuthorList/Author"):
        ln, fn = _text(a, "LastName"), _text(a, "Initials")
        if ln:
            authors.append(f"{ln} {fn}" if fn else ln)
    pub_types = [pt.text for pt in art_el.findall("PublicationTypeList/PublicationType") if pt.text]
    mesh = [m.text for m in medline.findall("MeshHeadingList/MeshHeading/DescriptorName") if m.text]
    doi = pmcid = None
    for aid in art.findall("PubmedData/ArticleIdList/ArticleId"):
        if aid.get("IdType") == "doi":
            doi = aid.text
        elif aid.get("IdType") == "pmc":
            pmcid = aid.text
    return {"pmid": pmid, "title": title, "abstract": abstract, "journal": journal,
            "year": year, "authors": authors, "pub_types": pub_types, "mesh": mesh,
            "doi": doi, "pmcid": pmcid}

def efetch_batch(pmids):
    xml = _get("efetch.fcgi", {"id": ",".join(pmids), "retmode": "xml"})
    root = ET.fromstring(xml)
    out = []
    for art in root.findall("PubmedArticle"):
        rec = _parse_article(art)
        if rec and rec.get("abstract"):  # keep only records with an abstract
            out.append(rec)
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max", type=int, default=4000, help="cap on records (recency-sorted)")
    ap.add_argument("--since", default=None, help="entrez date YYYY/MM/DD for incremental refresh")
    ap.add_argument("--batch", type=int, default=200)
    ap.add_argument("--out", default=os.path.join(RAW, "literature.jsonl"))
    args = ap.parse_args()
    os.makedirs(RAW, exist_ok=True)

    ids, total = esearch(CORE_QUERY, since=args.since, retmax=max(args.max, 100000))
    ids = ids[:args.max]
    print(f"esearch: {total:,} match the universe; fetching {len(ids):,} (cap={args.max}, since={args.since})")

    seen = 0
    with open(args.out, "w") as f:
        for i in range(0, len(ids), args.batch):
            chunk = ids[i:i + args.batch]
            recs = efetch_batch(chunk)
            for r in recs:
                f.write(json.dumps(r) + "\n")
            seen += len(recs)
            print(f"  {i+len(chunk):>5}/{len(ids)} ids -> {seen:,} records with abstracts", flush=True)
            time.sleep(0.34)  # NCBI ~3 req/s without key
    print(f"DONE: wrote {seen:,} records to {args.out}")

if __name__ == "__main__":
    main()
