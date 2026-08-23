"""Add restaurants to the registry. One at a time, or a whole list at once.

    # one
    python3 src/add.py --name "Sunny Point Cafe" --city Asheville --region NC \
        --website https://sunnypointcafe.com --source community --by nina

    # a list: one restaurant per line, "Name | website | address"
    python3 src/add.py --batch mylist.txt --city Asheville --region NC \
        --source local_list --by nina --citation "Best of WNC 2025, Best Brunch"

No award is required. No approval step. The only requirement is that you say
where the record came from, so a later reader can judge it.
"""
from __future__ import annotations
import argparse, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from registry import (load, save, add, make_record, SOURCES, REGISTRY)


def parse_batch(path: str):
    """One restaurant per line. 'Name' or 'Name | website' or 'Name | website | address'.
    Blank lines and lines starting with # are skipped."""
    out = []
    with open(path, encoding="utf-8") as fh:
        for ln in fh:
            ln = ln.strip()
            if not ln or ln.startswith("#"):
                continue
            parts = [p.strip() for p in ln.split("|")]
            out.append({"name": parts[0],
                        "website": parts[1] if len(parts) > 1 else "",
                        "address": parts[2] if len(parts) > 2 else ""})
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description="Add restaurants to the registry.")
    ap.add_argument("--name")
    ap.add_argument("--batch", help="file with one restaurant per line")
    ap.add_argument("--city", required=True)
    ap.add_argument("--region", default="", help="state/province, e.g. NC")
    ap.add_argument("--country", default="us")
    ap.add_argument("--website", default="")
    ap.add_argument("--address", default="")
    ap.add_argument("--source", default="community", choices=SOURCES)
    ap.add_argument("--by", required=True, help="who added this")
    ap.add_argument("--citation", default="", help="where you found it")
    ap.add_argument("--award-program", default="")
    ap.add_argument("--award-tier", default="", help="verbatim tier label")
    ap.add_argument("--award-year", default="")
    ap.add_argument("--registry", default=REGISTRY)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)

    if not a.name and not a.batch:
        ap.error("give --name or --batch")

    award = None
    if a.award_program:
        award = {"program": a.award_program, "tier": a.award_tier,
                 "year": a.award_year, "citation": a.citation}

    rows = (parse_batch(a.batch) if a.batch
            else [{"name": a.name, "website": a.website, "address": a.address}])

    reg = load(a.registry)
    tally = {"added": 0, "merged": 0, "duplicate": 0}
    for row in rows:
        rec = make_record(name=row["name"], city=a.city, region=a.region,
                          country=a.country, website=row["website"],
                          address=row["address"], source=a.source,
                          added_by=a.by, citation=a.citation, award=award)
        r = add(reg, rec)
        tally[r] += 1
        print(f"  {r:9s} {rec['restaurant_id']}")

    if a.dry_run:
        print("\ndry run, nothing written")
    else:
        save(reg, a.registry)
        print(f"\n{tally['added']} added, {tally['merged']} merged into existing, "
              f"{len(reg['restaurants'])} in registry")
    return 0


if __name__ == "__main__":
    sys.exit(main())
