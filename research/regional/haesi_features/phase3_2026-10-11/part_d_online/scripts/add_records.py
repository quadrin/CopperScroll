#!/usr/bin/env python3
"""Append hand-coded T3 records to data/coding_online_t3.json (phase-2 coding_online.json format).

Usage (from anywhere):
  python3 -I add_records.py records.json            # a JSON list (or one object) of coding records (or stdin)
  python3 -I add_records.py --status ID STATUS NOTE  # a non-coded status row (opened outside region, held, error)

A record with an existing report_id replaces the old one. The file keeps one record per line, sorted by the
T3 order position, so that diffs stay readable. Standard library only.
"""
import csv
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PART = HERE.parent
DATA = PART / "data"
CODING = DATA / "coding_online_t3.json"
STATUS = DATA / "online_status_t3.csv"
SCREEN = PART.parent.parent / "phase2_2026-10-10" / "online_screen.csv"

CLASSES = {"cistern", "pool_reservoir", "channel_aqueduct", "dam", "ritual_bath", "cave_with_finds",
           "tomb_burial_cave", "columbarium_dovecote", "rockcut_installation", "hoard_cache"}
REQUIRED = ["report_id", "series", "volume", "year", "pages", "title", "author", "permit", "map_ref",
            "excavated_or_surveyed", "text_sha256", "text_chars", "report_type", "online_date", "features"]


def t3_positions():
    with open(SCREEN, newline="", encoding="utf-8") as f:
        return {r["report_id"]: int(r["order_position_in_tier"]) for r in csv.DictReader(f) if r["tier"] == "T3"}


def load():
    if not CODING.exists():
        return []
    return json.loads(CODING.read_text(encoding="utf-8"))


def save(recs, pos):
    recs.sort(key=lambda r: pos[r["report_id"].split("-", 1)[1]])
    body = ",\n".join(json.dumps(r, ensure_ascii=False) for r in recs)
    CODING.write_text("[\n" + body + "\n]\n", encoding="utf-8")


def check(r, pos):
    for k in REQUIRED:
        assert k in r, (r.get("report_id"), "missing " + k)
    hid = r["report_id"].split("-", 1)[1]
    assert r["report_id"].startswith("HAESI-") and hid in pos, r["report_id"]
    assert 81 <= pos[hid] <= 662, (r["report_id"], pos[hid])
    assert len(r["text_sha256"]) == 64 and all(c in "0123456789abcdef" for c in r["text_sha256"]), r["report_id"]
    for f in r["features"]:
        assert f["type"] in CLASSES, (r["report_id"], f["type"])
        assert f["window"] in ("yes", "no", "unknown"), (r["report_id"], f["window"])
        assert len(f["quote"].split()) <= 12, (r["report_id"], f["quote"])
        for k in ("subtype", "n", "period", "quote"):
            assert k in f, (r["report_id"], k)


def main():
    pos = t3_positions()
    if len(sys.argv) > 1 and sys.argv[1] == "--status":
        hid, status, note = sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else ""
        assert hid in pos
        rows = []
        if STATUS.exists():
            with open(STATUS, newline="", encoding="utf-8") as f:
                rows = [r for r in csv.DictReader(f) if r["report_id"] != hid]
        rows.append(dict(report_id=hid, status=status, note=note))
        rows.sort(key=lambda r: pos[r["report_id"]])
        with open(STATUS, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["report_id", "status", "note"], lineterminator="\n")
            w.writeheader()
            w.writerows(rows)
        print("status", hid, status)
        return
    src = Path(sys.argv[1]).read_text(encoding="utf-8") if len(sys.argv) > 1 else sys.stdin.read()
    new = json.loads(src)
    if isinstance(new, dict):
        new = [new]
    recs = {r["report_id"]: r for r in load()}
    for r in new:
        chk = r.pop("_chk", None)
        if chk is not None:
            # transcription check: first 8 hex of sha256(text_sha256 as typed), computed in the browser too
            assert hashlib.sha256(r["text_sha256"].encode()).hexdigest()[:8] == chk, (r["report_id"], "hash typo")
        check(r, pos)
        recs[r["report_id"]] = r
    save(list(recs.values()), pos)
    done = sorted(pos[r.split("-", 1)[1]] for r in recs)
    print("records %d; last positions %s" % (len(recs), done[-5:]))


if __name__ == "__main__":
    main()
