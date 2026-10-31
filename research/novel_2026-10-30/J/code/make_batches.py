"""Split strings.csv into batches of 400 lines (sid<TAB>text) for the blind coders."""
from pathlib import Path
import pandas as pd
D = Path(__file__).resolve().parents[1] / "period_coding"
s = pd.read_csv(D / "strings.csv", dtype=str)
B = 400
for i in range(0, len(s), B):
    part = s.iloc[i:i + B]
    txt = "\n".join(f"{r.sid}\t{r.text}" for r in part.itertuples()) + "\n"
    (D / "batches" / f"batch_{i // B + 1:02d}.tsv").write_text(txt, encoding="utf-8")
print((len(s) + B - 1) // B)
