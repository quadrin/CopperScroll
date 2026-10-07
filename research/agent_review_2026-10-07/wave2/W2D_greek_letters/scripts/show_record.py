#!/usr/bin/env python3
"""print the CIIP record NNNN (from its header to the next header) from a pdftotext file.
usage: show_record.py TEXTFILE NUM [maxchars]"""
import re, sys
path, num = sys.argv[1], sys.argv[2]
maxc = int(sys.argv[3]) if len(sys.argv) > 3 else 5000
text = open(path, encoding="utf-8", errors="replace").read()
pages = text.split("\f")
pos = []
off = 0
for i, p in enumerate(pages, 1):
    pos.append((off, i))
    off += len(p) + 1
m = re.search(r"(?m)^\s{0,6}" + re.escape(num) + r"\.\s", text)
if not m:
    print("NOT FOUND", num); sys.exit()
start = m.start()
m2 = re.compile(r"(?m)^\s{0,6}(\d{1,4})\.\s+\S").search(text, m.end())
# skip false next headers that are the same num or line numbers (keep going until a different 3-4 digit number)
while m2 and (m2.group(1) == num or len(m2.group(1)) < len(num)):
    m2 = re.compile(r"(?m)^\s{0,6}(\d{1,4})\.\s+\S").search(text, m2.end())
end = m2.start() if m2 else len(text)
pg = max(i for o, i in pos if o <= start)
seg = text[start:end]
seg = "\n".join(l.rstrip() for l in seg.split("\n") if l.strip())
print(f"[pdf page {pg}]")
print(seg[:maxc])
