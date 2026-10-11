#!/usr/bin/env python3
"""Print a TOC item's text: it.py VOL N [maxchars] [skipchars]  (VOL like 27_1968). Uses items.tsv located starts.
Copied from the Mac scratch copy."""
import os, sys, collections
base = os.path.expanduser("~/p3a_scratch/")
v = "HA_" + sys.argv[1]; n = int(sys.argv[2]); mx = int(sys.argv[3]) if len(sys.argv) > 3 else 4000; sk = int(sys.argv[4]) if len(sys.argv) > 4 else 0
rows = [l.rstrip("\n").split("\t") for l in open(base + "items.tsv", encoding="utf-8") if l.startswith(v + "\t")]
pages = {}
for l in open(base + "txt/%s.pages.txt" % v, encoding="utf-8"):
    p, _, t = l.rstrip("\n").partition("\t"); pages[int(p[1:])] = t
loc = sorted([(int(r[3]), int(r[4]), int(r[1])) for r in rows if r[3]])
me = [r for r in rows if int(r[1]) == n][0]
if me[3]:
    p0, s0 = int(me[3]), int(me[4])
    later = [x for x in loc if (x[0], x[1]) > (p0, s0)]
    p1, s1 = (later[0][0], later[0][1]) if later else (max(pages), len(pages[max(pages)]))
    nxt = [r for r in rows if later and int(r[1]) == later[0][2]]
else:
    a = int(me[2].replace("–", "-").split("-")[0]); p0, s0, p1, s1 = a, 0, a + 3, 0; nxt = []
txt = ""
for p in range(p0, p1 + 1):
    t = pages.get(p, ""); a = s0 if p == p0 else 0; b = s1 if p == p1 else len(t)
    txt += " [P%d] " % p + t[a:b]
print("## %s n=%d [%s] %s | how=%s | next=%s" % (v, n, me[2], me[6], me[5], (nxt[0][6] if nxt else "")))
print(txt[sk:sk + mx])
if len(txt) > sk + mx: print("...[%d more chars]" % (len(txt) - sk - mx))
