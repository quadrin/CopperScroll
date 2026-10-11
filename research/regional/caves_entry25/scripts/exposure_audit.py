#!/usr/bin/env python3
"""Exposure audit (PLAN.md section 8): which Atiqot 41 cave numbers appear in the repository outside this lane.

Run from anywhere:  python3 -I -B research/regional/caves_entry25/scripts/exposure_audit.py
Greps the git-tracked text files of the repository (excluding this lane's folder and built atlas assets) for
Atiqot 41 cave numbers written either way round ('IV/17' or '17/IV'), and compares each A41 row's coded exposure.
A number found in the repository for a row coded 'unexposed-at-freeze' is listed as 'check' (a token can also occur
in an unrelated context, so a hit is a prompt to check, not proof of exposure). Writes exposure_audit.csv.
"""
import csv
import re
import subprocess
from collections import defaultdict
from pathlib import Path

LANE = Path(__file__).resolve().parents[1]
REPO = LANE.parents[2]
ROMAN = r"(?:XV|XIV|XIII|XII|XI|X|IX|VIII|VII|VI|V|IV|III|II|I)"
TOKEN = re.compile(rf"(?<![A-Za-z0-9/])(?:({ROMAN})/(\d{{1,2}})(?:\s?[-–]\s?(\d{{1,2}}))?|(\d{{1,2}})/({ROMAN}))(?![A-Za-z0-9/])")
SKIP = ("research/regional/caves_entry25/", "atlas-site/", "atlas/app/")


RANGE_ONLY = "reviewed: the number occurs only inside a range or coverage statement (e.g. 'caves XI/1-22'), not record content"
REVIEWED = {
    "A41:VII/2": RANGE_ONLY, "A41:XI/6": RANGE_ONLY, "A41:XI/7": RANGE_ONLY, "A41:XI/9": RANGE_ONLY, "A41:XI/10": RANGE_ONLY,
    "A41:XI/11": RANGE_ONLY, "A41:XI/13": RANGE_ONLY, "A41:XI/14": RANGE_ONLY, "A41:XI/15": RANGE_ONLY, "A41:XI/16": RANGE_ONLY,
    "A41:XIV/4-south": "reviewed: the hit is XIV/4 (a separate, exposed row); the five unnumbered caves south of it are on p. 242, not opened before",
    "A41:X/42": "reviewed: unrelated token in a Zertal page index", "A41:X/43": "reviewed: unrelated token in a Zertal page index",
}


def tracked_text_files():
    out = subprocess.run(["git", "ls-files", "-z"], cwd=REPO, capture_output=True, check=True).stdout.decode().split("\0")
    for p in out:
        if not p or p.startswith(SKIP) or not p.endswith((".md", ".csv", ".json", ".py", ".txt", ".ts", ".yaml", ".yml")):
            continue
        yield p


def main():
    hits = defaultdict(set)
    for p in tracked_text_files():
        try:
            text = (REPO / p).read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for m in TOKEN.finditer(text):
            if m.group(1):
                region, lo = m.group(1), int(m.group(2))
                hi = int(m.group(3)) if m.group(3) and int(m.group(3)) > lo else lo  # ranges such as 'XII/52–53'
            else:
                region, lo = m.group(5), int(m.group(4))
                hi = lo
            for num in range(lo, min(hi, lo + 30) + 1):
                hits[f"{region}/{num}"].add(p)
    rows = list(csv.DictReader(open(LANE / "caves.csv", encoding="utf-8")))
    out = []
    for r in rows:
        if not r["cave_id"].startswith("A41:"):
            continue
        m = re.match(r"A41:([IVX]+)/(\d+)", r["cave_id"])
        if not m:
            continue
        key = f"{m.group(1)}/{int(m.group(2))}"
        files = sorted(hits.get(key, ()))
        status = "consistent"
        if files and r["exposure"] == "unexposed-at-freeze":
            status = REVIEWED.get(r["cave_id"], "check")
        if not files and r["exposure"] == "exposed-repo":
            status = "exposed via notes without the number (by name) or via merged records"
        out.append(dict(cave_id=r["cave_id"], coded_exposure=r["exposure"], repo_files=len(files),
                        examples="; ".join(files[:3]), status=status))
    with open(LANE / "exposure_audit.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(out)
    n_check = sum(1 for o in out if o["status"] == "check")
    print(f"exposure_audit.csv: {len(out)} A41 rows; {n_check} to check")


if __name__ == "__main__":
    main()
