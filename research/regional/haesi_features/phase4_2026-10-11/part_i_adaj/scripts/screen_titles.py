#!/usr/bin/env python3
"""Phase 4 part I (ADAJ): gazetteer hits for every title or heading in data/portal_toc.csv and data/early_headings.csv.

Uses the frozen phase-2 gazetteer and normalisation (phase-2 scripts/common.py, amendment A1) plus the A3 variants.
Prints one JSON line per title with its hits; the screen decisions themselves are in data/screen_decisions.csv
(hand decisions with reasons) and are joined by build_part_i.py.

Run from the repository root:
  python3 -I research/regional/haesi_features/phase4_2026-10-11/part_i_adaj/scripts/screen_titles.py
"""
import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PART = HERE.parent
LANE = PART.parent.parent
sys.path.insert(0, str(LANE / "phase2_2026-10-10" / "scripts"))
import common  # noqa: E402

# Amendment A3 name variants (phase-2 AMENDMENTS.md), with the zone they point to.
A3_VARIANTS = {"hagedud": "Z2_JORDAN_VALLEY", "anathoth": "Z4_JERUSALEM_HILLS",
               "land of benjamin": "Z4_JERUSALEM_HILLS", "kh el burj": "Z4_JERUSALEM_HILLS"}


def patterns():
    pats = common.gazetteer_patterns()
    for v, z in A3_VARIANTS.items():
        pats.setdefault(z, [])
        pats[z] = sorted(set(pats[z]) | {common.norm(v).strip()})
    return pats


def hits_for(title, pats):
    return common.title_hits(title, pats)


def main():
    pats = patterns()
    for name in ("portal_toc.csv", "early_headings.csv"):
        p = PART / "data" / name
        if not p.exists():
            continue
        with open(p, newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                h = hits_for(r["title"], pats)
                if h:
                    print(json.dumps(dict(source=name, key=r.get("heading_id") or r.get("chapter_id"),
                                          volume=r["volume"], title=r["title"], hits=h), ensure_ascii=False))


if __name__ == "__main__":
    main()
