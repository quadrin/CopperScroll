#!/usr/bin/env python3
"""Phase 4 part I (ADAJ): hash the OCR text span read for each coded unit and check every quote in it.

The OCR text is kept outside the repository (scratch folder, one file per PDF page: <OCR_DIR>/<pdf stem>/pNNN.txt).
Each record in data/coding.json has a "span": {"pdf": <pdf_file>, "pages": "a-b", "start": <marker>, "end": <marker>}.
The span is the text of PDF pages a..b joined, cut from the first occurrence of the start marker (if given) to the
first occurrence of the end marker after it (if given, exclusive). Whitespace is collapsed to single spaces and the
SHA-256 is taken over the UTF-8 bytes. A quote is found if it occurs in the collapsed span, either as is or after
joining words hyphenated across line ends ("con- tained" -> "contained").

Writes data/spans.csv. Usage (from the repository root):
  python3 -I research/regional/haesi_features/phase4_2026-10-11/part_i_adaj/scripts/verify_spans.py OCR_DIR
"""
import csv
import hashlib
import json
import re
import sys
from pathlib import Path

PART = Path(__file__).resolve().parents[1]
DATA = PART / "data"
FIELDS = ["report_id", "pdf_file", "pdf_pages", "start_marker", "end_marker", "n_chars", "text_sha256", "n_quotes",
          "quotes_not_found"]


def collapse(s):
    return " ".join(s.split())


def span_text(ocr_dir, span):
    stem = span["pdf"][:-4] if span["pdf"].endswith(".pdf") else span["pdf"]
    a, b = (int(x) for x in (span["pages"].split("-") + [span["pages"]])[:2])
    parts = []
    for k in range(a, b + 1):
        parts.append((Path(ocr_dir) / stem / ("p%03d.txt" % k)).read_text(encoding="utf-8", errors="replace"))
    t = collapse("\n".join(parts))
    if span.get("start"):
        i = t.find(span["start"])
        if i < 0:
            raise ValueError("start marker not found: %r" % span["start"])
        t = t[i:]
    if span.get("end"):
        j = t.find(span["end"], len(span.get("start") or "") or 1)
        if j < 0:
            raise ValueError("end marker not found: %r" % span["end"])
        t = t[:j]
    return t.strip()


def dehyphen(t):
    return re.sub(r"(\w)[-‐] (\w)", r"\1\2", t)


def main(ocr_dir):
    recs = json.loads((DATA / "coding.json").read_text(encoding="utf-8"))
    out = []
    for r in sorted(recs, key=lambda x: x["report_id"]):
        sp = r["span"]
        t = span_text(ocr_dir, sp)
        th = dehyphen(t)
        quotes = [f["quote"] for f in r["features"] if f.get("quote")]
        missing = [q for q in quotes if collapse(q) not in t and collapse(q) not in th]
        out.append(dict(report_id=r["report_id"], pdf_file=sp["pdf"], pdf_pages=sp["pages"],
                        start_marker=sp.get("start", ""), end_marker=sp.get("end", ""), n_chars=len(t),
                        text_sha256=hashlib.sha256(t.encode("utf-8")).hexdigest(), n_quotes=len(quotes),
                        quotes_not_found=" | ".join(missing)))
    with open(DATA / "spans.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, lineterminator="\n")
        w.writeheader()
        w.writerows(out)
    bad = [o for o in out if o["quotes_not_found"]]
    for o in bad:
        print("QUOTE NOT FOUND", o["report_id"], o["quotes_not_found"])
    print("spans %d, with missing quotes %d" % (len(out), len(bad)))


if __name__ == "__main__":
    main(sys.argv[1])
