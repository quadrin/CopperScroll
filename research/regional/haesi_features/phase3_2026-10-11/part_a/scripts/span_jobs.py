#!/usr/bin/env python3
"""Write the ASCII job list for mac/batch_spans.py: report id, raw-text base name, raw line range, and for each
coded quote its token count and the first 16 hex of the SHA-256 of its normalised tokens. No text leaves the repo side.

usage (from the repository root):
  python3 -I research/regional/haesi_features/phase3_2026-10-11/part_a/scripts/span_jobs.py PART_A_DIR OUT_TSV
The Mac output (report id, lines, span SHA-256, PDF pages, quote status) is joined back by prep_data.py.
"""
import csv
import glob
import hashlib
import json
import re
import sys

BIDI = dict.fromkeys(map(ord, "‪‫‬‭‮‎‏⁦⁧⁨⁩"), None)
PUN = re.compile(r"[\s\.,;:!?\(\)\[\]\"'״׳`´‘’“”\-–—־_■□•*]+")


def ntok(s):
    return [t for t in PUN.split(s.translate(BIDI)) if t]


def qh(q):
    t = ntok(q)
    return "%d:%s" % (len(t), hashlib.sha256(" ".join(t).encode("utf-8")).hexdigest()[:16])


def main(part, out_path):
    vols = list(csv.DictReader(open(part + "/data/volumes.csv", encoding="utf-8")))
    names = [v["local_file"][len("IAA_"):-4] for v in vols]

    def raw_for(tf):
        v = tf[2:]
        if v == "28-29":
            return "HA_029-028_1969"
        key = "HA_" + "-".join(str(int(x)) for x in v.split("-")) + "_"
        m = [n for n in names if n.startswith(key)]
        assert len(m) == 1, (tf, m)
        return m[0]

    reps = []
    for p in sorted(glob.glob(part + "/data/coding_*.json")):
        reps += json.load(open(p, encoding="utf-8"))
    with open(out_path, "w", encoding="ascii") as out:
        for r in sorted(reps, key=lambda r: r["report_id"]):
            out.write("\t".join([r["report_id"], raw_for(r["text_file_id"]), r["text_lines"],
                                 ",".join(qh(f["quote"]) for f in r["features"])]) + "\n")
    print(len(reps))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
