#!/usr/bin/env python3
"""Locate each TOC item's heading in the page texts (squashed Hebrew/Latin letters), in document order.
Writes items.tsv: vol, n, printed, pdf_page, pos, how, title, context. Copied from the Mac scratch copy."""
import os, re, collections
base = os.path.expanduser("~/p3a_scratch/")
FIN = str.maketrans("ךםןףץ", "כמנפצ")
def keep(c): return ("א" <= c <= "ת") or c.isalpha() and c.isascii()
def squash(s):
    idx, out = [], []
    for i, c in enumerate(s):
        if keep(c): out.append(c.translate(FIN).lower()); idx.append(i)
    return "".join(out), idx
toc = collections.defaultdict(list)
for l in open(base + "toc.tsv", encoding="utf-8"):
    v, n, pg, ti, au = l.rstrip("\n").split("\t")
    a = int(re.split("[–-]", pg)[0]); toc[v].append((a, int(n), pg, ti))
out = open(base + "items.tsv", "w", encoding="utf-8")
for v in sorted(toc):
    pages = {}
    for l in open(base + "txt/%s.pages.txt" % v, encoding="utf-8"):
        p, _, t = l.rstrip("\n").partition("\t"); pages[int(p[1:])] = t
    sq = {p: squash(t) for p, t in pages.items()}
    last = (0, 0)
    for a, n, pg, ti in sorted(toc[v]):
        cands = []
        t2 = re.sub(r"\s*[-–]\s*\d{4}.*$", "", ti)  # drop year suffix
        parts = [t2] + ([t2.split(":", 1)[1]] if ":" in t2 else []) + [w for w in re.split(r"[\s:,\-–()\"']+", t2) if len(squash(w)[0]) >= 3]
        found = None
        for k, part in enumerate(parts):
            ps = squash(part)[0]
            if len(ps) < 3: continue
            for p in range(max(1, a - 1), a + 6):
                if p not in sq: continue
                s, idx = sq[p]
                start = 0
                if (p, 0) < (last[0], 0) : continue
                if p == last[0]: start = sum(1 for i in idx if i < last[1]) if k == 0 else 0
                j = s.find(ps, start if p == last[0] else 0)
                if p == last[0] and j >= 0 and idx[j] < last[1]:
                    j = s.find(ps, start)
                if j >= 0:
                    found = (p, idx[j], "full" if k == 0 else ("after-colon" if (":" in t2 and k == 1) else "word:" + part)); break
            if found: break
        if found:
            p, pos, how = found; last = (p, pos)
            ctx = pages[p][pos:pos + 70]
            out.write("%s\t%d\t%s\t%d\t%d\t%s\t%s\t%s\n" % (v, n, pg, p, pos, how, ti, ctx))
        else:
            out.write("%s\t%d\t%s\t\t\tNOTFOUND\t%s\t\n" % (v, n, pg, ti))
out.close()
