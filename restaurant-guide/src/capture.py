"""Menu capture harness. Records a menu snapshot with provenance, then runs
the census over it.

Capture is deliberately separate from census: a snapshot is a citable
Layer-1 artifact (source URL, timestamp, content hash, capturer) and the
census is a reproducible derivation from it. Re-running the census with a
newer lexicon must not silently rewrite history, so the snapshot is stored
verbatim and never edited.

Usage:
  python3 src/capture.py --restaurant good-hot-fish \\
      --source-url https://example.com/menu \\
      --menu-label dinner \\
      --method human_transcription \\
      --capturer nina \\
      --dishes-json /tmp/dishes.json

  dishes.json: [{"name": "...", "description": "...", "menu_section": "...",
                 "price_usd": 12.0}, ...]
  Transcribe VERBATIM. Do not translate, normalize, or supply a missing
  description from knowledge -- an empty description is data.
"""
from __future__ import annotations
import argparse, hashlib, json, os, sys, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from census import census_menu, restaurant_counts, load_lexicon, to_jsonl, CENSUS_VERSION

METHODS = ("structured_platform", "pdf_text", "vision_ocr",
           "human_transcription", "restaurant_submitted")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Capture a menu snapshot and run the census.")
    ap.add_argument("--restaurant", required=True, help="slug, e.g. good-hot-fish")
    ap.add_argument("--source-url", required=True)
    ap.add_argument("--menu-label", required=True,
                    help="dinner | brunch | bar | lunch | sample_undated -- one menu per snapshot")
    ap.add_argument("--method", required=True, choices=METHODS)
    ap.add_argument("--capturer", required=True)
    ap.add_argument("--dishes-json", required=True)
    ap.add_argument("--city", default="asheville-nc-us")
    a = ap.parse_args(argv)

    with open(a.dishes_json, encoding="utf-8") as fh:
        dishes = json.load(fh)
    if not isinstance(dishes, list) or not dishes:
        sys.exit("dishes-json must be a non-empty JSON list")
    for d in dishes:
        if "name" not in d:
            sys.exit(f"every dish needs a 'name': {d}")

    payload = json.dumps(dishes, ensure_ascii=False, sort_keys=True).encode()
    sha = hashlib.sha256(payload).hexdigest()
    now = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat()
    day = now[:10]
    rid = f"{a.city}/{a.restaurant}"
    snap_id = f"{a.restaurant}:{a.menu_label}:{day}"

    outdir = os.path.join(ROOT, "data", "menus", a.restaurant)
    os.makedirs(outdir, exist_ok=True)
    raw_path = os.path.join(outdir, f"{day}.{a.menu_label}.json")
    with open(raw_path, "w", encoding="utf-8") as fh:
        json.dump({"snapshot_id": snap_id, "restaurant_id": rid,
                   "source_url": a.source_url, "fetched_utc": now,
                   "content_sha256": sha, "extraction_method": a.method,
                   "menu_label": a.menu_label, "capturer": a.capturer,
                   "dishes": dishes}, fh, indent=1, ensure_ascii=False)

    lex = load_lexicon()
    rows = census_menu(dishes, rid, lex=lex)
    counts = restaurant_counts(rows)
    counts.update({"snapshot_id": snap_id, "menu_label": a.menu_label,
                   "lexicon_version": lex["lexicon_version"]})
    to_jsonl(rows, os.path.join(outdir, f"{day}.{a.menu_label}.census.jsonl"))

    with open(os.path.join(ROOT, "data", "snapshots.jsonl"), "a", encoding="utf-8") as fh:
        fh.write(json.dumps({"snapshot_id": snap_id, "restaurant_id": rid,
                             "source_url": a.source_url, "fetched_utc": now,
                             "content_sha256": sha, "extraction_method": a.method,
                             "menu_label": a.menu_label,
                             "n_dishes_extracted": len(dishes), "capturer": a.capturer,
                             "completeness": "text_only_unknown",
                             "lexicon_version": lex["lexicon_version"],
                             "census_version": CENSUS_VERSION,
                             "raw_path": os.path.relpath(raw_path, ROOT)},
                            ensure_ascii=False) + "\n")

    n = counts["n_dishes"]
    print(f"snapshot {snap_id}  sha256 {sha[:12]}  dishes {n}")
    print(f"  no meat named:                       {counts['n_no_meat_named']:3d} / {n}")
    print(f"  no meat and no legume named:         {counts['n_no_meat_no_legume_named']:3d} / {n}")
    print(f"  names a potato or other starch:      {counts['n_names_potato_or_starch']:3d} / {n}")
    print(f"  names a vegetable:                   {counts['n_names_vegetable']:3d} / {n}")
    print(f"  names NO protein source at all:      {counts['n_names_no_protein_source_at_all']:3d} / {n}")
    print(f"  starch families: " + ", ".join(f"{k}={v}" for k, v in
          counts["starch_dish_counts"].items() if v))
    print(f"  quality: {counts['n_dishes_no_terms_matched']} dishes matched no term, "
          f"{counts['n_dishes_with_ambiguous_terms']} have ambiguous terms")
    print("  NOTE: a non-match means NOT NAMED, never absent. No suitability implied.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
