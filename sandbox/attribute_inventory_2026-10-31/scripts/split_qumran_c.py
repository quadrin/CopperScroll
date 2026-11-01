"""Split the Qumran third reading (keyed/qumran_C_adjudication.csv, with a `source` column) into
keyed/<src>_C_adjudication.csv (key, field, C_value, ...) for consolidate.py. A source with no
third-reading rows gets a header-only file. Written 31 Oct, before the third reading was delivered.

usage: python3 split_qumran_c.py
"""
import csv
from pathlib import Path

RUN = Path(__file__).resolve().parents[1]
SOURCES = ["qum3a", "mp18", "hir04", "bad77", "esh02", "qum4a"]

rows = list(csv.DictReader(open(RUN / "keyed/qumran_C_adjudication.csv", encoding="utf-8")))
cols = [c for c in rows[0].keys() if c != "source"] if rows else ["key", "field", "C_value"]
for src in SOURCES:
    sub = [{c: r.get(c, "") for c in cols} for r in rows if r.get("source", "").strip() == src]
    with open(RUN / f"keyed/{src}_C_adjudication.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(sub)
    print(src, len(sub))
other = sorted({r.get("source", "") for r in rows} - set(SOURCES))
if other:
    print("rows with an unknown source:", other)
