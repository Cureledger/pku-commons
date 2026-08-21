#!/usr/bin/env python3
"""Guthrie corpus — PMC open-access full text for the guidelines/consensus subset.

Small, high-value pull: the documents users most need quoted accurately. Finds
PKU guideline/consensus records that have a PMC id, fetches the OA full text,
and writes section-level records to build/raw/guidelines_fulltext.jsonl.
"""
import json, os, time, urllib.parse, urllib.request
import xml.etree.ElementTree as ET

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")

# Note: PMC availability is resolved via elink (pubmed->pmc) below, not a PubMed
# filter string, so we do NOT use an "open access"[filter] clause (which matches 0).
GUIDELINE_QUERY = ('phenylketonuria AND (guideline[ptyp] OR consensus OR '
                   'recommendation OR "standard of care" OR "practice guideline")')

def _get(endpoint, extra, db="pubmed", retries=4):
    p = {"db": db, "tool": "guthrie-corpus", **extra}
    url = f"{EUTILS}/{endpoint}?" + urllib.parse.urlencode(p)
    last = None
    for i in range(retries):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return r.read()
        except Exception as e:
            last = e; time.sleep(1.5 * (i + 1))
    raise last

def esearch_ids(query, retmax=200):
    extra = {"term": query, "retmode": "json", "retmax": retmax, "sort": "pub+date"}
    return json.loads(_get("esearch.fcgi", extra))["esearchresult"].get("idlist", [])

def pmid_to_pmcid(pmids):
    """Use elink to map PMIDs -> PMC ids."""
    out = {}
    for i in range(0, len(pmids), 100):
        chunk = pmids[i:i+100]
        xml = _get("elink.fcgi", {"dbfrom": "pubmed", "db": "pmc",
                   "id": ",".join(chunk), "retmode": "xml"})
        root = ET.fromstring(xml)
        for ls in root.findall("LinkSet"):
            src = ls.find("IdList/Id")
            link = ls.find("LinkSetDb/Link/Id")
            if src is not None and link is not None:
                out[src.text] = "PMC" + link.text
        time.sleep(0.34)
    return out

def fetch_pmc_fulltext(pmcid):
    xml = _get("efetch.fcgi", {"id": pmcid, "retmode": "xml"}, db="pmc")
    root = ET.fromstring(xml)
    art = root.find(".//article")
    if art is None:
        return None
    def _txt(el):
        return " ".join("".join(el.itertext()).split()) if el is not None else ""
    title = _txt(art.find(".//article-meta/title-group/article-title"))
    sections = []
    body = art.find(".//body")
    if body is None:
        return {"title": title, "sections": []}
    for sec in body.findall(".//sec"):
        st = _txt(sec.find("title"))
        paras = [_txt(p) for p in sec.findall("p")]
        text = "\n".join([p for p in paras if p])
        if text:
            sections.append({"heading": st, "text": text})
    return {"title": title, "sections": sections}

def main():
    os.makedirs(RAW, exist_ok=True)
    pmids = esearch_ids(GUIDELINE_QUERY, retmax=200)
    print(f"guideline/consensus OA candidates: {len(pmids)}")
    mapping = pmid_to_pmcid(pmids)
    print(f"with PMC full text: {len(mapping)}")
    n = 0
    with open(os.path.join(RAW, "guidelines_fulltext.jsonl"), "w") as f:
        for pmid, pmcid in mapping.items():
            try:
                doc = fetch_pmc_fulltext(pmcid)
            except Exception as e:
                print(f"  skip {pmcid}: {e}"); continue
            if doc and doc["sections"]:
                rec = {"pmid": pmid, "pmcid": pmcid, "title": doc["title"],
                       "sections": doc["sections"]}
                f.write(json.dumps(rec) + "\n")
                n += 1
                print(f"  {pmcid}: {len(doc['sections'])} sections", flush=True)
            time.sleep(0.34)
    print(f"DONE: wrote {n} full-text guideline docs")

if __name__ == "__main__":
    main()
