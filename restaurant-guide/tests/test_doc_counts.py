"""Guard: assertion counts cited in documentation must match reality.

This file exists because the counts in README.md, HANDOFF.md and the specs
were wrong twice -- hand-counted `ck(` call sites miss loop-generated
assertions, so a suite with 30 call sites reports 37 passes. A cited number
that nobody re-checks is how a document quietly stops being true.

Run: python3 tests/test_doc_counts.py
"""
import os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUITES = ("test_census", "test_signals", "test_registry")
# Including this file in the roster would recurse, so a child run sets
# the sentinel and skips the roster section.
SELF_RUN = os.environ.get("PKU_DOC_COUNT_CHILD") == "1"
F = []


def ck(c, label):
    print(("  pass  " if c else "  FAIL  ") + label)
    if not c:
        F.append(label)


def live_count(suite):
    """Runtime pass count -- the only trustworthy number."""
    env = dict(os.environ, PKU_DOC_COUNT_CHILD="1")
    r = subprocess.run([sys.executable, os.path.join(ROOT, "tests", suite + ".py")],
                       capture_output=True, text=True, env=env)
    return len(re.findall(r"(?m)^  pass  ", r.stdout)), r.returncode


print("\n[live assertion counts]")
live = {}
for s in SUITES:
    n, rc = live_count(s)
    live[s] = n
    ck(rc == 0, f"{s}.py exits 0")
    ck(n > 0, f"{s}.py reports {n} assertions")

print("\n[documented counts match live counts]")
# Any "<n> assertion", "<n>/<n> passing", or "<n> passing test" claim in a doc
# must equal that suite's live count.
# A doc may cite several suites (README cites both), so a claim is valid if it
# matches ANY live suite count. That is weaker than pinning claim->suite, but
# it catches the real failure mode -- a number that matches nothing -- without
# needing the doc to declare which suite each sentence is about.
DOCS = ("README.md", "HANDOFF.md",
        "spec/signal-taxonomy-v0.1.md", "spec/menu-census-v0.1.md")
PAT = re.compile(r"(\d+)\s*(?:assertion|passing test)|(\d+)\s*/\s*(\d+)\s*passing")
valid = set(live.values())
for doc in DOCS:
    path = os.path.join(ROOT, doc)
    if not os.path.exists(path):
        continue
    text = open(path, encoding="utf-8").read()
    claims = []
    for m in PAT.finditer(text):
        claims.extend(int(g) for g in m.groups() if g)
    bad = [c for c in claims if c not in valid]
    ck(not bad, f"{doc}: cited counts {claims or '[]'} all match a live suite "
                f"{sorted(valid)}" + (f" -- MISMATCH {bad}" if bad else ""))

print("\n[no hand-counted ck() call sites masquerading as assertion counts]")
for s in SUITES:
    src = open(os.path.join(ROOT, "tests", s + ".py"), encoding="utf-8").read()
    sites = len(re.findall(r"(?m)^ck\(", src))
    ck(sites <= live[s], f"{s}: {sites} call sites <= {live[s]} runtime assertions "
                         "(loops expand; never cite call sites)")

if not SELF_RUN:
    # Copy these numbers into prose and docs. Do not hand-count a test file:
    # loops expand, so call sites are always an undercount.
    me, _ = live_count("test_doc_counts")
    print("\n[live roster -- cite these, never a hand count]")
    for k, v in sorted(list(live.items()) + [("test_doc_counts", me)]):
        print(f"  {k}: {v}")

print("\n" + "=" * 58)
print("ALL PASS" if not F else "FAILURES: " + str(F))
print("=" * 58)
sys.exit(1 if F else 0)
