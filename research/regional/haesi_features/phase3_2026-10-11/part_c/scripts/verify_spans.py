#!/usr/bin/env python3
"""HA-ESI phase 3, part C: hash the text span of every coded report and check every quote against it.

Runs where the reading-order texts are (the owner's computer); standard library only.
  python3 verify_spans.py --coding DIR_WITH_coding_*.json --work DIR_WITH_<VOL>.ordered.txt --out spans.csv

For each record: the lines given in `text_lines` ("a-b", or several ranges "a-b;c-d") of <VOL>.ordered.txt are
joined, whitespace is collapsed to single spaces, and SHA-256 (UTF-8) is computed. Each feature quote must be a
substring of that collapsed text and have at most 12 words. The volume is the coding file's name (coding_<VOL>.json).
Hebrew quotes (HA-ESI, where the English text is missing) are matched after removing the bidirectional control
characters that pdftotext writes around Hebrew words; the hash is always of the unaltered collapsed text.
"""
import argparse
import csv
import hashlib
import json
import re
from pathlib import Path

BIDI = re.compile("[‎‏‪-‮⁦-⁩]")


def span_text(lines, spec):
    parts = []
    for rng in spec.split(";"):
        a, b = rng.split("-")
        parts.extend(lines[int(a) - 1:int(b)])
    return " ".join(" ".join(parts).split())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--coding", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    rows = []
    cache = {}
    for p in sorted(Path(a.coding).glob("coding_*.json")):
        vol = p.stem.split("_", 1)[1]
        if vol not in cache:
            cache[vol] = (Path(a.work) / (vol + ".ordered.txt")).read_text(encoding="utf-8").split("\n")
        lines = cache[vol]
        for rec in json.loads(p.read_text(encoding="utf-8")):
            t = span_text(lines, rec["text_lines"])
            tb = " ".join(BIDI.sub("", t).split())
            qs = [f["quote"] for f in rec["features"] if f.get("quote")]
            bad = [q for q in qs if (" ".join(q.split()) not in t and " ".join(BIDI.sub("", q).split()) not in tb)
                   or len(q.split()) > 12]
            rows.append(dict(report_id=rec["report_id"], text_file=vol, text_lines=rec["text_lines"],
                             text_sha256=hashlib.sha256(t.encode("utf-8")).hexdigest(), n_quotes=len(qs),
                             quotes_not_found=" || ".join(bad)))
    with open(a.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    nb = sum(1 for r in rows if r["quotes_not_found"])
    print("records", len(rows), "with quote problems", nb)
    for r in rows:
        if r["quotes_not_found"]:
            print(r["report_id"], "|", r["quotes_not_found"][:300])


if __name__ == "__main__":
    main()
