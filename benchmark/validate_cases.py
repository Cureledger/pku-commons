#!/usr/bin/env python3
"""Validate phe-benchmark test cases for self-consistency.

Every case an agent contributes must pass this before it can be trusted as
ground truth. Checks, per case:
  1. schema: required fields present, types correct
  2. arithmetic: sum(components.phe_mg) == expected_phe_mg (within tol)
  3. per-component: phe_mg == phe_mg_per_100g * grams / 100 (within tol)
  4. provenance: every component carries an integer fdcId
  5. id uniqueness across the file
  6. weight-order: for multi-ingredient labels, ingredient text is ordered
     by descending component grams (the property the estimator assumes)

Dependency-free. Usage:
    python validate_cases.py testset/seed_v0.jsonl
Exit code 1 if any case fails.
"""
import json, sys, re

ARITH_TOL_MG = 0.6      # rounding slack on summed ground truth
COMP_TOL_MG  = 0.6      # slack on per-component recompute

def load(path):
    out=[]
    with open(path) as fh:
        for i,line in enumerate(fh,1):
            line=line.strip()
            if not line: continue
            try: out.append((i,json.loads(line)))
            except json.JSONDecodeError as e:
                out.append((i,{"__parse_error__":str(e)}))
    return out

def check_case(c):
    errs=[]
    for f in ("id","name","label","expected_phe_mg","ground_truth"):
        if f not in c: errs.append(f"missing top-level field '{f}'")
    if errs: return errs
    lab=c["label"]
    for f in ("serving_size_g","ingredients"):
        if f not in lab: errs.append(f"label missing '{f}'")
    gt=c["ground_truth"]
    comps=gt.get("components")
    if not isinstance(comps,list) or not comps:
        errs.append("ground_truth.components missing/empty"); return errs
    total=0.0
    for j,comp in enumerate(comps):
        for f in ("food","fdcId","grams","phe_mg_per_100g","phe_mg"):
            if f not in comp: errs.append(f"component[{j}] missing '{f}'")
        if "fdcId" in comp and not isinstance(comp["fdcId"],int):
            errs.append(f"component[{j}] fdcId not integer (provenance): {comp.get('fdcId')!r}")
        if all(k in comp for k in ("phe_mg_per_100g","grams","phe_mg")):
            recomputed=comp["phe_mg_per_100g"]*comp["grams"]/100.0
            if abs(recomputed-comp["phe_mg"])>COMP_TOL_MG:
                errs.append(f"component[{j}] '{comp.get('food')}' phe_mg={comp['phe_mg']} "
                            f"!= {comp['phe_mg_per_100g']}*{comp['grams']}/100={recomputed:.2f}")
            total+=comp["phe_mg"]
    if abs(total-c["expected_phe_mg"])>ARITH_TOL_MG:
        errs.append(f"sum(components)={total:.2f} != expected_phe_mg={c['expected_phe_mg']}")
    # weight-order: ingredient text order vs descending component grams.
    # A mismatch is NOT an error — it is a *wanted* weight-share trap case
    # (order lies about weight), the exact failure the estimator must handle.
    warns=[]
    ing=lab.get("ingredients","")
    tokens=[t.strip().lower() for t in re.split(r"[,;]| and ",ing) if t.strip()]
    if len(comps)>1 and len(tokens)==len(comps):
        grams=[comp["grams"] for comp in comps]
        if grams!=sorted(grams,reverse=True):
            warns.append(f"weight-share trap: ingredient order {tokens} vs grams {grams} "
                         f"(order != weight) — valuable case, kept")
    return errs,warns

def main():
    if len(sys.argv)<2:
        print("usage: validate_cases.py <cases.jsonl> [more.jsonl ...]"); sys.exit(2)
    seen={}; nfail=0; ntot=0; ntrap=0
    for path in sys.argv[1:]:
        for lineno,c in load(path):
            ntot+=1
            if "__parse_error__" in c:
                print(f"[FAIL] {path}:{lineno} JSON parse: {c['__parse_error__']}"); nfail+=1; continue
            cid=c.get("id","<no-id>")
            if cid in seen:
                print(f"[FAIL] {path}:{lineno} duplicate id '{cid}' (also {seen[cid]})"); nfail+=1
            seen[cid]=f"{path}:{lineno}"
            errs,warns=check_case(c)
            if errs:
                nfail+=1
                print(f"[FAIL] {cid} ({c.get('name','?')[:40]}):")
                for e in errs: print(f"        - {e}")
            for w in warns:
                ntrap+=1
                print(f"[trap] {cid}: {w}")
    ok=ntot-nfail
    print(f"\n{ok}/{ntot} cases valid; {nfail} failed; {ntrap} weight-share trap cases (wanted).")
    sys.exit(1 if nfail else 0)

if __name__=="__main__": main()
