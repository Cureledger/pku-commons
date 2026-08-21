#!/usr/bin/env python3
"""Guthrie corpus fetch — PKU literature from NCBI E-utilities.

Reproducible, key-free pull of the PKU literature universe defined in
guthrie/CORPUS.md. Writes JSONL to build/raw/. The corpus ACCUMULATES: each run
merges up to --max NEW records (deduped by PMID) into the existing
literature.jsonl and logs every attempted id in fetched_ids.txt, so repeated
runs grow it in chunks toward the whole universe instead of re-snapshotting the
most-recent N.

    python fetch_corpus.py                 # add up to 4000 more (default chunk)
    python fetch_corpus.py --max 0         # fetch ALL remaining in one run
    python fetch_corpus.py --max 500       # small pull for testing
    python fetch_corpus.py --reset         # discard prior state, start fresh

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

def _load_corpus(path):
    """Existing records keyed by pmid, so a run MERGES instead of overwriting."""
    have = {}
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    r = json.loads(line)
                except json.JSONDecodeError:
                    continue
                pmid = str(r.get("pmid") or "").strip()
                if pmid:
                    have[pmid] = r
    return have

def _load_ids(path):
    ids = set()
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            for line in f:
                t = line.strip()
                if t:
                    ids.add(t)
    return ids

def _sort_key(pmid):
    # numeric PMIDs ascending; anything odd sorts last, deterministically
    return (0, int(pmid)) if pmid.isdigit() else (1, 0)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max", type=int, default=4000,
                    help="max NEW records to fetch THIS run (0 = all remaining). The "
                         "corpus accumulates across runs, so this grows it in chunks.")
    ap.add_argument("--since", default=None,
                    help="entrez date YYYY/MM/DD to restrict the universe (optional; "
                         "leave unset so growth walks the whole universe)")
    ap.add_argument("--batch", type=int, default=200)
    ap.add_argument("--out", default=os.path.join(RAW, "literature.jsonl"))
    ap.add_argument("--reset", action="store_true",
                    help="ignore the existing corpus + attempted-id log; start fresh")
    args = ap.parse_args()
    out_dir = os.path.dirname(args.out) or "."
    os.makedirs(out_dir, exist_ok=True)
    ids_path = os.path.join(out_dir, "fetched_ids.txt")

    # Prior state (persisted between runs). `attempted` tracks every id we have
    # efetch'd, INCLUDING abstract-less ones that never enter `have` — otherwise
    # they'd be retried forever and block the chunk from advancing.
    have = {} if args.reset else _load_corpus(args.out)
    attempted = set() if args.reset else _load_ids(ids_path)

    universe, total = esearch(CORE_QUERY, since=args.since, retmax=100000)
    universe = [str(x) for x in universe]
    todo = [i for i in universe if i not in attempted]
    if args.max and args.max > 0:
        todo = todo[:args.max]

    print(f"universe: {total:,} match | have: {len(have):,} records | "
          f"attempted: {len(attempted):,} | this run: {len(todo):,} "
          f"(cap={args.max or 'ALL'}, since={args.since})", flush=True)

    added = 0
    for i in range(0, len(todo), args.batch):
        chunk = todo[i:i + args.batch]
        for r in efetch_batch(chunk):
            pmid = str(r.get("pmid") or "").strip()
            if pmid:
                have[pmid] = r
                added += 1
        attempted.update(chunk)
        print(f"  {min(i + args.batch, len(todo)):>6}/{len(todo)} ids -> "
              f"+{added:,} new (corpus {len(have):,})", flush=True)
        time.sleep(0.34)  # NCBI ~3 req/s without a key

    with open(args.out, "w") as f:
        for pmid in sorted(have, key=_sort_key):
            f.write(json.dumps(have[pmid]) + "\n")
    with open(ids_path, "w") as f:
        for pmid in sorted(attempted, key=_sort_key):
            f.write(pmid + "\n")

    remaining = sum(1 for i in universe if i not in attempted)
    tail = (" Corpus is COMPLETE for this universe."
            if remaining == 0 else
            f" Re-run to fetch the next {min(args.max or remaining, remaining):,}.")
    print(f"DONE: corpus {len(have):,} records (+{added:,} this run); "
          f"universe {total:,}, attempted {len(attempted):,}, remaining {remaining:,}.{tail}")

if __name__ == "__main__":
    main()
