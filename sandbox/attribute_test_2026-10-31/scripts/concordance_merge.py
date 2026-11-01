"""Merge the two concordance readings (RULE step 1) into keyed/concordance.csv.

A row is kept when both readers give the same describer (ba72, ben93, djd3), the same 1993 keys and the same
cited site or cave number (the first number after 'Cave', 'No.' or 'site' in describer_ref). The merged row
carries that number as describer_ref, ref_type = cave_number, and copied = yes if either reader said yes.
Rows of other describers, and page or name citations, cannot define a truth set (bench28.py) and are not kept.
usage: python3 concordance_merge.py
"""
import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from bench28 import DESCRIBERS, norm_atq  # noqa: E402
from model28 import RUN, read_csv  # noqa: E402


def number(ref):
    m = re.search(r"(?:Cave|No\.|[Ss]ite)\s*(\d+[A-Za-z]?)", ref or "")
    return m.group(1) if m else None


def keyset(r):
    return tuple(sorted(norm_atq(k) for k in r["atq41_keys"].split(";") if k.strip()))


def entries(R):
    out = {}
    for r in read_csv(RUN / f"keyed/concordance_{R}.csv"):
        n = number(r["describer_ref"])
        if r["describer"].strip() in DESCRIBERS and n:
            out.setdefault((r["describer"].strip(), keyset(r), n), []).append(r)
    return out


A, B = entries("A"), entries("B")
agreed = sorted(set(A) & set(B))
rows = [{"atq41_keys": ";".join(k), "describer": d, "describer_ref": n, "ref_type": "cave_number",
         "copied": "yes" if any(x["copied"].strip().lower() == "yes" for x in A[(d, k, n)] + B[(d, k, n)]) else "no",
         "confidence": "/".join(sorted({x["confidence"] for x in A[(d, k, n)] + B[(d, k, n)]})),
         "quote_A": A[(d, k, n)][0]["quote"], "quote_B": B[(d, k, n)][0]["quote"]} for d, k, n in agreed]
with open(RUN / "keyed/concordance.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)
print("agreed:", [(d, k, n) for d, k, n in agreed])
print("A only:", sorted(set(A) - set(B)))
print("B only:", sorted(set(B) - set(A)))
