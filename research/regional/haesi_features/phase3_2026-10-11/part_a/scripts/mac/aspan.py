#!/usr/bin/env python3
"""Span of a TOC item in the raw text, from its located heading to the next located heading (or explicit anchors).
usage: aspan.py VOL N [--start PAGE "anchor"] [--end "anchor"] [--q "quote"]...
Prints: lines a-b, pages, sha256 (raw lines a..b, bidi removed, form feeds to spaces, whitespace collapsed), quote checks.
Copied from the Mac scratch copy; the bidi control characters and some punctuation are written here as \\u escapes."""
import os, sys, re, hashlib
base = os.path.expanduser("~/p3a_scratch/")
BIDI = dict.fromkeys(map(ord, "‪‫‬‭‮‎‏⁦⁧⁨⁩"), None)
PUN = re.compile(r"[\s\.,;:!?\(\)\[\]\"'״׳`´‘’“”\-–—־_■□•*]+")
def ntok(s): return [t for t in PUN.split(s.translate(BIDI)) if t]
args = sys.argv[1:]; v = "HA_" + args[0]; n = int(args[1]); rest = args[2:]
start_anchor = end_anchor = None; quotes = []
i = 0
while i < len(rest):
    if rest[i] == "--start": start_anchor = (int(rest[i + 1]), rest[i + 2]); i += 3
    elif rest[i] == "--end": end_anchor = rest[i + 1]; i += 2
    elif rest[i] == "--q": quotes.append(rest[i + 1]); i += 2
    else: i += 1
raw = open(base + "txt/%s.raw.txt" % v, encoding="utf-8").read().split("\n")
# page-token map consistent with pages.py: tokens = page.translate(BIDI).split()
toks = []  # (page, line, token)
page = 1
for li, l in enumerate(raw, 1):
    parts = l.split("\f")
    for k, part in enumerate(parts):
        if k > 0: page += 1
        for t in part.translate(BIDI).split():
            toks.append((page, li, t))
bypage = {}
for j, (p, li, t) in enumerate(toks): bypage.setdefault(p, []).append(j)
def tokidx(p, pos):
    pages = {}
    for l in open(base + "txt/%s.pages.txt" % v, encoding="utf-8"):
        pp, _, t = l.rstrip("\n").partition("\t"); pages[int(pp[1:])] = t
    k = pages[p][:pos].count(" ")
    return bypage[p][k]
rows = [l.rstrip("\n").split("\t") for l in open(base + "items.tsv", encoding="utf-8") if l.startswith(v + "\t")]
loc = sorted([(int(r[3]), int(r[4]), int(r[1])) for r in rows if r[3]])
me = [r for r in rows if int(r[1]) == n][0]
norm = [(p, li, " ".join(ntok(t))) for (p, li, t) in toks]
def find_seq(seq, j0):
    flat = []
    for j in range(j0, len(norm)):
        for w in norm[j][2].split():
            flat.append((w, j))
        if len(flat) > 200000: break
    for k in range(len(flat) - len(seq) + 1):
        if all(flat[k + m][0] == seq[m] for m in range(len(seq))): return flat[k][1], flat[k + len(seq) - 1][1]
    return None
if start_anchor:
    j0 = bypage[start_anchor[0]][0]
    r = find_seq(ntok(start_anchor[1]), j0); assert r, "start anchor not found"; ja = r[0]
else:
    ja = tokidx(int(me[3]), int(me[4]))
if end_anchor:
    r = find_seq(ntok(end_anchor), ja); assert r, "end anchor not found"; jb = r[1]
else:
    later = [x for x in loc if (x[0], x[1]) > (int(me[3]), int(me[4]))] if me[3] else []
    jb = (tokidx(later[0][0], later[0][1]) - 1) if later else len(toks) - 1
a, b = toks[ja][1], toks[jb][1]
span = "\n".join(raw[a - 1:b]).translate(BIDI).replace("\f", " ")
col = " ".join(span.split())
print("lines %d-%d pages %d-%d tokens %d sha256 %s" % (a, b, toks[ja][0], toks[jb][0], jb - ja + 1, hashlib.sha256(col.encode()).hexdigest()))
print("START: " + " ".join(t for _, _, t in toks[ja:ja + 12]))
print("END:   " + " ".join(t for _, _, t in toks[max(ja, jb - 11):jb + 1]))
J = " " + " ".join(w for (_, _, x) in norm[ja:jb + 1] for w in x.split()) + " "
lay = open(base + "txt/%s.layout.txt" % v, encoding="utf-8").read().translate(BIDI).split("\f")
L = " " + " ".join(" ".join(ntok(x)) for x in lay[toks[ja][0] - 1:toks[jb][0]]) + " "
for q in quotes:
    qq = " " + " ".join(ntok(q)) + " "
    st = "FOUND" if qq in J else ("FOUND (layout pages)" if qq in L else "NOT FOUND")
    print("quote %s (%d words): %s" % (st, len(q.split()), q))
