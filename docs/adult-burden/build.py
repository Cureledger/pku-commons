#!/usr/bin/env python3
"""Build adult-burden/data/studies.json from adult-burden/evidence.md.

The markdown is the canonical evidence file (Guthrie corpus, PubMed-verified).
Entry format:  - [PMID:x](url) (Journal, Year) — one-sentence summary.
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).parent
SRC = HERE / "evidence.md"
OUT = HERE / "data" / "studies.json"

ENTRY = re.compile(r"^- \[PMID:(\d+)\]\((https?://\S+)\) \(([^,]+), (\d{4})\) — (.+)$")

domain = None
records = []
for ln in SRC.read_text().splitlines():
    if ln.startswith("## "):
        domain = ln[3:].strip()
    m = ENTRY.match(ln)
    if m:
        pmid, url, journal, year, summary = m.groups()
        summary = re.sub(r"\*\*([^*]+)\*\*", r"\1", summary)
        summary = re.sub(r"\*([^*]+)\*", r"\1", summary)
        records.append({
            "pmid": pmid,
            "domain": domain,
            "journal": journal.strip(),
            "year": int(year),
            "summary": summary.strip(),
            "sources": [{"title": f"PMID:{pmid} on PubMed", "url": url}],
            "confidence": "sourced",
        })

OUT.write_text(json.dumps({
    "dataset": "adult-burden",
    "title": "Long-Term Health and Sustainability of the PKU Diet",
    "updated": "2026-09-06",
    "source_note": ("Compiled from the Guthrie PKU corpus (PubMed-indexed). Every PMID, title, "
                    "and numeric claim verified against live PubMed records via NCBI E-utilities "
                    "on 2026-09-06."),
    "records": records,
}, indent=1))
print(f"wrote {OUT} ({len(records)} records, "
      f"{len(set(r['domain'] for r in records))} domains)")
