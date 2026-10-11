#!/usr/bin/env python3
"""usage: lspan.py VOL A B [x] -> sha256 of raw lines A..B (bidi removed, form feeds to spaces, whitespace collapsed);
with a 4th argument also prints the text. Same hash rule as aspan.py and batch_spans.py."""
import os, sys, re, hashlib
base = os.path.expanduser("~/p3a_scratch/")
BIDI = dict.fromkeys(map(ord, "‪‫‬‭‮‎‏⁦⁧⁨⁩"), None)
v = "HA_" + sys.argv[1]; a = int(sys.argv[2]); b = int(sys.argv[3])
raw = open(base + "txt/%s.raw.txt" % v, encoding="utf-8").read().split("\n")
t = " ".join(raw[a-1:b]).translate(BIDI).replace("\f", " ")
t = re.sub(r"\s+", " ", t).strip()
print(a, b, hashlib.sha256(t.encode("utf-8")).hexdigest())
if len(sys.argv) > 4: print(t)
