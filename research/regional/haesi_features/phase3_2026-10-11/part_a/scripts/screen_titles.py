#!/usr/bin/env python3
"""Gazetteer screen of the part-A portal table-of-contents titles (HA Hebrew series 1961-1979).

Applies the phase-2 frozen gazetteer (../../../phase2_2026-10-10/PLAN.md, JSON block) with the phase-2
normalisation (common.norm, amendment A1). Two match levels are recorded:
  strict  - the frozen rule: the normalised term with a word boundary on both sides;
  prefix  - the phase-1 D2/S2 rule for Hebrew: one or two prefix letters (ב ה ו ל מ כ ש) before the term.
Output (stdout or --out): CSV with one row per TOC item and its hits. Standard library only (no pyproj needed).

Run from the repository root:
  python3 -I research/regional/haesi_features/phase3_2026-10-11/part_a/scripts/screen_titles.py [--out FILE]
"""
import csv
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PART = HERE.parent
P2 = PART.parent.parent / "phase2_2026-10-10"
sys.path.insert(0, str(P2 / "scripts"))
import common  # noqa: E402  (phase-2 plan parameters and normalisation)

HEB = re.compile(r"[֐-׿]")


def patterns(params):
    out = []
    for z, g in params["gazetteer"].items():
        for t in g["en"] + g["he"]:
            out.append((z, common.norm(t).strip()))
    rw = params["region_wide_terms"]
    for t in rw["en"] + rw["he"]:
        out.append(("REGION_WIDE", common.norm(t).strip()))
    return sorted(set(out))


def hits(title, pats):
    nt = common.norm(title)
    strict, prefix = [], []
    for z, p in pats:
        if (" " + p + " ") in nt:
            strict.append((z, p))
        elif HEB.search(p) and re.search(r"(?<= )[בהולמכש]{1,2}" + re.escape(p) + r"(?= )", nt):
            prefix.append((z, p))
    return strict, prefix


def main(out=None):
    params = common.plan_params()
    pats = patterns(params)
    rows = []
    with open(PART / "data" / "portal_toc_items.csv", newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            s, p = hits(r["title"], pats)
            r = dict(r)
            r["strict_hits"] = ";".join("%s:%s" % x for x in s)
            r["prefix_hits"] = ";".join("%s:%s" % x for x in p)
            rows.append(r)
    fields = list(rows[0].keys())
    fo = open(out, "w", newline="", encoding="utf-8") if out else sys.stdout
    w = csv.DictWriter(fo, fieldnames=fields, lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
    if out:
        fo.close()
    return rows


if __name__ == "__main__":
    main(sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else None)
