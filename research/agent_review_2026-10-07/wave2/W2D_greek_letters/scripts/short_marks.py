#!/usr/bin/env python3
"""From records.py output, list records whose diplomatic Greek consists only of short groups
(each group <=3 letters, at most 4 groups, at least one 2-3 letter group) = candidate 'short marks'.
usage: short_marks.py records.tsv OUT.tsv"""
import csv, re, sys
inp, outp = sys.argv[1:3]
rows = list(csv.DictReader(open(inp, encoding="utf-8"), delimiter="\t"))
out = []
for r in rows:
    caps = r["caps_lines"]
    if not caps.strip():
        continue
    lines = [l.strip() for l in caps.split(" || ") if l.strip()]
    # only consider the first block of caps lines (diplomatic text) up to 4 lines
    lines = lines[:4]
    groups = []
    ok = True
    for l in lines:
        # remove editorial brackets, dots, plus signs, dashes
        l2 = re.sub(r"[\[\]\(\)\-–\.\+·|/⟦⟧{}<>?,;:'’ʹ]", " ", l)
        toks = l2.split()
        for t in toks:
            if re.fullmatch(r"[Α-ΩϹЄ]+", t):
                groups.append(t)
            elif re.fullmatch(r"[A-Za-z]+", t) and len(t) <= 4 and t.isupper():
                groups.append(t)  # latin lookalike capitals
            elif re.search(r"[a-z]{3,}", t):
                ok = False
    if not ok or not groups:
        continue
    if all(len(g) <= 3 for g in groups) and len(groups) <= 4 and any(len(g) >= 2 for g in groups):
        out.append((r["label"], r["no"], r["pdf_page"], r["title"], " ".join(groups)))
with open(outp, "w", encoding="utf-8") as f:
    f.write("label\tno\tpdf_page\ttitle\tgroups\n")
    for o in out:
        f.write("\t".join(o) + "\n")
print(len(out))
