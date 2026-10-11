"""Step 1 of 3 for coded/a41_index_crosswalk.csv.

Input (not committed): `pdftotext -layout -f 2 -l 19 "24 - Index.pdf"` (Atiqot 41 Part 1, file 24; hash in
../../intake/atiqot41_intake.json). Run with `python3 -I`. Step 2 parses rows; step 3 cleans and applies the
hand fixes listed in it. First read of the Index: 2026-10-11T04:49:15Z (after the plan freeze).
"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
skip = re.compile(r"Index|Nickname|Publication|Permit No|column: Exc|כינויה|הרשאת חפירה|No\. in this|^\s*[0-9]+\s*$")
out = []
for line in open(src, encoding="utf-8"):
    if not line.strip() or skip.search(line):
        continue
    line = re.sub(r"[‎‏‪-‮]", "", line.rstrip())
    out.append(re.sub(r"  +", " | ", line.strip()))
open(dst, "w", encoding="utf-8").write("\n".join(out) + "\n")
print(len(out))
