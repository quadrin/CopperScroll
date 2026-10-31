"""Merge blind coder outputs into coded_intervals.csv and validate sid coverage."""
import csv, io
from pathlib import Path
import pandas as pd
D = Path(__file__).resolve().parents[1] / "period_coding"
s = pd.read_csv(D / "strings.csv", dtype=str)
rows = []
for f in sorted((D / "raw").glob("coded_batch_*.csv")):
    for r in csv.reader(io.StringIO(f.read_text(encoding="utf-8"))):
        if not r or not r[0].startswith("P"):
            continue
        r = (r + [""] * 7)[:7]
        rows.append(dict(zip(["sid", "start", "end", "start_event", "end_event", "kind", "confidence"], r), batch=f.name))
c = pd.DataFrame(rows)
assert c.sid.is_unique, c[c.sid.duplicated()]
m = s.merge(c, on="sid", how="left", validate="1:1")
miss = m[m.batch.isna()]
print("strings", len(s), "coded", len(c), "missing", len(miss))
for col in ("start", "end"):
    m[col] = pd.to_numeric(m[col], errors="coerce")
bad = m[(m.start.notna()) & (m.end.notna()) & (m.start > m.end)]
print("start>end", len(bad))
print(m.kind.value_counts(dropna=False).to_dict()); print(m.confidence.value_counts(dropna=False).to_dict())
m.to_csv(D / "coded_intervals.csv", index=False)
