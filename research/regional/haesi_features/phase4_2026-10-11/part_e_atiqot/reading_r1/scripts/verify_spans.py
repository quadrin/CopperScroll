#!/usr/bin/env python3
"""Phase 4, part E, reader r1: hash the text span read for every unit and check every quote against it.

Runs where the extracted texts are (the owner's Mac, $HOME/p4text/r1/); standard library only.
  python3 -I verify_spans.py --input spans_input.jsonl --work DIR --out spans.csv

spans_input.jsonl (written by export_spans_input.py) has one object per unit:
  {"report_id": ..., "text_file": "raw" | "plain", "text_lines": "a-b;c-d", "quotes": [...]}
The text file is DIR/<report_id>.<text_file>.txt (pdftotext -raw, or pdftotext default order for Hebrew).
The lines given are joined, whitespace is collapsed to single spaces and SHA-256 (UTF-8) is computed.
Each quote must have at most 12 words and be a substring of the collapsed span; for Hebrew text the
bidirectional control characters that pdftotext writes are removed before matching (the hash is always
of the unaltered collapsed text). Ligatures (U+FB00-FB06) are also folded before matching only.
"""
import argparse
import csv
import hashlib
import json
import re
import unicodedata
from pathlib import Path

BIDI = re.compile("[‎‏‪-‮⁦-⁩]")


def fold(s):
    s = BIDI.sub("", s)
    s = "".join(unicodedata.normalize("NFKC", c) if "ﬀ" <= c <= "ﬆ" else c for c in s)
    return " ".join(s.split())


def span_text(lines, spec):
    parts = []
    for rng in spec.split(";"):
        a, b = rng.split("-")
        parts.extend(lines[int(a) - 1:int(b)])
    return " ".join(" ".join(parts).split())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    rows = []
    for line in Path(a.input).read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        path = Path(a.work) / ("%s.%s.txt" % (rec["report_id"], rec["text_file"]))
        lines = path.read_text(encoding="utf-8", errors="replace").split("\n")
        t = span_text(lines, rec["text_lines"])
        tf = fold(t)
        bad = [q for q in rec["quotes"] if fold(q) not in tf or len(q.split()) > 12]
        rows.append(dict(report_id=rec["report_id"], text_file=path.name, text_lines=rec["text_lines"],
                         n_lines_total=len(lines), text_sha256=hashlib.sha256(t.encode("utf-8")).hexdigest(),
                         n_quotes=len(rec["quotes"]), quotes_not_found=" || ".join(bad)))
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
