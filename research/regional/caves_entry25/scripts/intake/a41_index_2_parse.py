"""Parse the condensed text layer of the Atiqot 41 Part 1 Index into a crosswalk (draft; reviewed by hand)."""
import csv, re, sys

ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "XV"]
src, dst = sys.argv[1], sys.argv[2]
heb = re.compile(r"[֐-׿]")
pub_re = re.compile(r"^(\d+)/(\S+)$")
region = None
rows = []
cur = None
for raw in open(src, encoding="utf-8"):
    line = raw.rstrip("\n")
    toks = [t.strip() for t in line.split(" | ")]
    m_head = re.match(r"^Region (\S+)", toks[0])
    if m_head:
        r = m_head.group(1).upper().replace("1", "I")
        # the Hebrew side of the heading gives the region for the Region IV page mislabelled 'Region VI'
        m_he = re.search(r"\b([IVX]+)\s*אזור", line)
        if m_he:
            r = m_he.group(1)
        if r in ROMAN:
            region = r
        continue
    last = toks[-1].replace(" ", "")
    m = pub_re.match(last)
    if m:
        n, rr = m.group(1), m.group(2).upper()
        reg = rr if rr in ROMAN else region
        mid = toks[:-1]
        permit = ""
        for t in list(mid):
            if re.search(r"L-\d+", t, re.I) or "הרשאת הסקר" in t:
                permit = ("under survey permit" if "הרשאת" in t else "") or re.search(r"L-\d+", t, re.I).group(0)
                if t.startswith("L-") and "תחת" in t:
                    permit = "under " + re.search(r"L-\d+", t, re.I).group(0)
                mid.remove(t)
        cur = {"pub_id": f"A41:{reg}/{n}", "region": reg, "n": int(n), "cells": " | ".join(mid), "permit": permit, "english": ""}
        rows.append(cur)
    elif cur is not None and not heb.search(line):
        cur["english"] = (cur["english"] + " " + line.replace(" | ", " ")).strip()
    elif cur is not None:
        cur["cells"] = (cur["cells"] + " || " + line).strip()
with open(dst, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)
print(len(rows))
