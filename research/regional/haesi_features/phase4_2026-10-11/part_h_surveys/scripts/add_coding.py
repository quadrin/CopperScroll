#!/usr/bin/env python3
"""Append hand-coded unit records (a JSON list in a batch file) to data/coding_<source>.jsonl, with checks.

Record fields: unit_id, name, pages, read_scope, text_sha256, text_chars, excavated_or_surveyed,
features (list of {type, n, period, window, quote, subtype, label, site}), notes, held_paragraphs (optional).
Usage: add_coding.py SOURCE batch.json   (SOURCE = swp3, swp2, gue_j1, ...)"""
import json
import re
import sys
from pathlib import Path

PART = Path(__file__).resolve().parent.parent
CLASSES = {"cistern", "pool_reservoir", "channel_aqueduct", "dam", "ritual_bath", "cave_with_finds",
           "tomb_burial_cave", "columbarium_dovecote", "rockcut_installation", "hoard_cache"}
LABELS = {"observed remains", "author's function label", "reconstruction", "INFERENCE", "author's report (not seen)"}


def check(r):
    assert re.match(r"^(SWP[23]|GUE-(J1|J2|J3|S1))-", r["unit_id"]), r["unit_id"]
    assert re.match(r"^[0-9a-f]{64}$", r["text_sha256"]), r["unit_id"]
    assert isinstance(r["text_chars"], int)
    assert r["excavated_or_surveyed"] in ("surveyed", "inspected"), r["unit_id"]
    for f in r["features"]:
        assert f["type"] in CLASSES, (r["unit_id"], f["type"])
        assert f["window"] in ("yes", "no", "unknown"), r["unit_id"]
        assert len(f["quote"].split()) <= 12, (r["unit_id"], f["quote"])
        assert f["period"], r["unit_id"]
        assert f["label"] in LABELS, (r["unit_id"], f["label"])


def main(source, batch):
    out = PART / "data" / ("coding_%s.jsonl" % source)
    have = set()
    if out.exists():
        for line in out.read_text(encoding="utf-8").splitlines():
            if line.strip():
                have.add(json.loads(line)["unit_id"])
    recs = json.loads(Path(batch).read_text(encoding="utf-8"))
    for r in recs:  # check the whole batch before writing anything
        check(r)
        assert r["unit_id"] not in have, "duplicate " + r["unit_id"]
        have.add(r["unit_id"])
    with open(out, "a", encoding="utf-8") as f:
        for r in recs:
            f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")
    print("added %d, total %d" % (len(recs), len(have)))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
