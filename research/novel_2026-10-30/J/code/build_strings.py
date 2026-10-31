"""Lane J: build the list of distinct period strings to be coded blind.
Reads only the period text columns. No dates are interpreted here."""
import hashlib, json, sys
from pathlib import Path
import pandas as pd

REPO = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parents[1] / "period_coding"
SRC = {
    "HAESI": ("research/regional/haesi_features/merged_2026-10-12/features_all.csv", "period_as_given"),
    "ASI": ("research/regional/asi_jerusalem/features.csv", "period_as_given"),
    "CAVES": ("research/regional/caves_entry25/caves.csv", "period_stated"),
    "COLUMB": ("research/regional/columbaria/columbaria.csv", "date_text"),
}

def norm(s):
    return " ".join(str(s).split())

def main():
    seen = {}
    for lin, (path, col) in SRC.items():
        d = pd.read_csv(REPO / path, dtype=str)
        for v in d[col].dropna():
            k = norm(v)
            if k and k not in seen:
                seen[k] = lin
    rows = sorted(seen)  # sorted text order: no information about source or date
    out = pd.DataFrame({"sid": ["P%04d" % (i + 1) for i in range(len(rows))], "text": rows})
    out.to_csv(OUT / "strings.csv", index=False)
    print(len(out))

if __name__ == "__main__":
    main()
