#!/usr/bin/env python3
"""Export the coded quotes (unit, feature index, quote, claimed page) as JSON for verify_on_mac.py.

Run: python3 -I research/regional/haesi_features/phase4_2026-10-11/part_e_atiqot/reading_r2/scripts/export_quotes.py > quotes.json
Standard library only.
"""
import json
import sys
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"


def load():
    out = []
    for p in sorted(DATA.glob("coding_*.jsonl")):
        for line in p.read_text(encoding="utf-8").splitlines():
            if line.strip():
                out.append(json.loads(line))
    return out


if __name__ == "__main__":
    rows = []
    for u in load():
        for i, f in enumerate(u["features"]):
            rows.append(dict(unit=u["unit_id"], i=i, quote=f["quote"], page=f.get("page", "")))
    json.dump(dict(units=[u["unit_id"] for u in load()], quotes=rows), sys.stdout, ensure_ascii=False)
