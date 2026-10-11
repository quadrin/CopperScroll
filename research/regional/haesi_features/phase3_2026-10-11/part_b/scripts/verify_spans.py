#!/usr/bin/env python3
"""Hash every coded text span and check every quote against it (HA part B).

For each record in data/coding/*.json: SHA-256 of the whitespace-collapsed text of raw lines `text_lines`
(pdftotext -raw output, bidi control marks removed, UTF-8), number of quotes and quotes not found verbatim.
Writes data/spans.csv. Needs the text directory (not in the repository):
  python3 -I .../part_b/scripts/verify_spans.py TEXTDIR
"""
import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import textlib  # noqa: E402

DATA = HERE.parent / "data"


def main(textdir):
    vols = {}
    rows, bad = [], 0
    for p in sorted((DATA / "coding").glob("*.json")):
        for r in json.loads(p.read_text(encoding="utf-8")):
            key = r["text_file_id"]
            if key not in vols:
                vols[key] = textlib.Volume(textdir, key)
            v = vols[key]
            miss, n = [], 0
            spans = [s for s in r["text_lines"].split(";") if s]
            text = " ".join(v.text(*map(int, s.split("-"))) for s in spans)
            for f in r["features"]:
                if f.get("quote"):
                    n += 1
                    if " ".join(f["quote"].split()) not in text:
                        miss.append(f["quote"])
            for q in r.get("extra_quotes", []):
                n += 1
                if " ".join(q.split()) not in text:
                    miss.append(q)
            sha = v.span_sha256(*map(int, spans[0].split("-"))) if len(spans) == 1 else \
                textlib.hashlib.sha256(text.encode("utf-8")).hexdigest()
            rows.append(dict(report_id=r["report_id"], text_file=key, text_lines=r["text_lines"], text_sha256=sha,
                             n_quotes=n, quotes_not_found=" | ".join(miss)))
            if miss:
                bad += 1
                print("MISSING", r["report_id"], miss)
    with open(DATA / "spans.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["report_id", "text_file", "text_lines", "text_sha256", "n_quotes", "quotes_not_found"],
                           lineterminator="\n")
        w.writeheader()
        w.writerows(sorted(rows, key=lambda x: x["report_id"]))
    print(len(rows), "records;", bad, "with quotes not found")


if __name__ == "__main__":
    main(sys.argv[1])
