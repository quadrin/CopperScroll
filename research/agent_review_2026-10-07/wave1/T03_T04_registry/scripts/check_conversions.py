# -*- coding: utf-8 -*-
"""Check that hand-written metre windows in confirm/miss/location texts match the computed cubit conversions.
Run: python3 -I check_conversions.py <registry.json>"""
import json, re, sys
from decimal import Decimal, ROUND_HALF_UP
d = json.load(open(sys.argv[1], encoding="utf-8"))
q = lambda c, x: float((Decimal(str(c)) * Decimal(str(x))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
pat = re.compile(r"(\d+(?:\.\d+)?)\s*[–-]\s*(\d+(?:\.\d+)?)\s*m\s*\((\d+)\s*c\.")
bad = 0; n = 0
for r in d["records"]:
    for field in ("confirm", "miss", "location_constraint", "inconclusive"):
        for m in pat.finditer(r[field] or ""):
            lo, hi, c = float(m.group(1)), float(m.group(2)), int(m.group(3))
            n += 1
            exp_lo, exp_hi = q(c, 0.445), q(c, 0.525)
            # allow 1-decimal hand rounding outward or to nearest
            if not (abs(lo - exp_lo) <= 0.051 and abs(hi - exp_hi) <= 0.051):
                bad += 1
                print("MISMATCH", r["id"], field, m.group(0), "expected", exp_lo, exp_hi)
print(n, "windows checked;", bad, "mismatches")

# Broader check: every "X–Y m" range in a record's texts should match one of that record's measure conversions.
pat2 = re.compile(r"(\d+(?:\.\d+)?)\s*[–-]\s*(\d+(?:\.\d+)?)\s*m\b")
unmatched = []
for r in d["records"]:
    convs = [tuple(m["metres_primary_0.445_0.525"]) for m in r["measures"] if m.get("metres_primary_0.445_0.525")]
    for field in ("confirm", "miss", "location_constraint", "inconclusive", "feature_detail"):
        for m in pat2.finditer(r[field] or ""):
            lo, hi = float(m.group(1)), float(m.group(2))
            if not any(abs(lo - a) <= 0.051 and abs(hi - b) <= 0.051 for a, b in convs):
                unmatched.append((r["id"], field, m.group(0)))
print(len(unmatched), "ranges not matching a record measure (review manually):")
for u in unmatched: print("  ", u)
