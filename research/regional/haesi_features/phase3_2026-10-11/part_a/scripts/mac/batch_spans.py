#!/usr/bin/env python3
"""Batch span hashes and quote checks (run on the Mac against the extracted text, which stays outside the repository).
usage: batch_spans.py jobs.tsv out.tsv
jobs: rid, raw base, a-b, quote hashes "len:sha16,..." (ntok-normalised quote, sha256 first 16 hex; ../span_jobs.py)
out:  rid, raw base, a-b, span sha256, pages, n_quotes, per-quote status (R raw span / L layout pages / N not found)
Only quote hashes travel to the Mac and only span hashes come back, so no text crosses between the machines."""
import os, sys, re, hashlib
base = os.path.expanduser("~/p3a_scratch/")
BIDI = dict.fromkeys(map(ord, "‪‫‬‭‮‎‏⁦⁧⁨⁩"), None)
PUN = re.compile(r"[\s\.,;:!?\(\)\[\]\"'״׳`´‘’“”\-–—־_■□•*]+")
def ntok(s): return [t for t in PUN.split(s.translate(BIDI)) if t]
def grams(tokens, n):
    return {hashlib.sha256(" ".join(tokens[k:k + n]).encode("utf-8")).hexdigest()[:16] for k in range(len(tokens) - n + 1)}
cache = {}
def vol(v):
    if v not in cache:
        raw = open(base + "txt/%s.raw.txt" % v, encoding="utf-8").read().split("\n")
        lay = open(base + "txt/%s.layout.txt" % v, encoding="utf-8").read().translate(BIDI).split("\f")
        pg = []; p = 1
        for l in raw:
            pg.append(p); p += l.count("\f")
        cache[v] = (raw, lay, pg)
    return cache[v]
out = open(sys.argv[2], "w", encoding="utf-8")
for line in open(sys.argv[1], encoding="ascii"):
    rid, v, lines, qs = (line.rstrip("\n").split("\t") + [""])[:4]
    raw, lay, pg = vol(v)
    a, b = map(int, lines.split("-"))
    span = "\n".join(raw[a - 1:b]).translate(BIDI).replace("\f", " ")
    col = " ".join(span.split())
    sha = hashlib.sha256(col.encode("utf-8")).hexdigest()
    p0, p1 = pg[a - 1], pg[b - 1] + raw[b - 1].count("\f")
    T = ntok(span)
    L = [t for x in lay[p0 - 1:p1] for t in ntok(x)]
    st = []
    for q in [x for x in qs.split(",") if x]:
        n, h = q.split(":"); n = int(n)
        st.append("R" if h in grams(T, n) else ("L" if h in grams(L, n) else "N"))
    out.write("\t".join([rid, v, lines, sha, "%d-%d" % (p0, p1), str(len(st)), "".join(st)]) + "\n")
out.close()
