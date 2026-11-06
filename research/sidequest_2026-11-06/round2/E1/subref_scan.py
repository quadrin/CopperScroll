#!/usr/bin/env python3
"""E1 round 2: within-report map-reference check for HA-ESI (vols 116-137).
For each English report: the map refs in the opening paragraph = the report's own general box(es);
every later map ref in the body = a sub-feature ref. Flag sub-refs lying > THRESH m outside every general box.
Then look up the same digits in the Hebrew text (source-level error vs translation error).
Usage: python3 subref_scan.py <hadtext root with en/ he/> out.csv
"""
import os, re, sys, csv, glob, math
ROOT, OUT = sys.argv[1], sys.argv[2]
THRESH = 300
BIDI = re.compile('[‎‏‪-‮⁦-⁩]')
NUM = r'(\d{3,7})(?:\s*[–\-]\s*(\d{1,7}))?'
PAT = re.compile(NUM + r'\s*/\s*' + NUM)
KEY = re.compile(r'map ref(?:erence)?s?\.?|\bNIG\b', re.I)

def expand(a, b):
    if b is None: return a, a
    if len(b) < len(a): b = a[:len(a) - len(b)] + b
    return a, b

def scale(s, n):
    return int(s) * {3: 1000, 4: 100, 5: 10, 6: 1, 7: 1}[n]

def box(m):
    e1, e2 = expand(m.group(1), m.group(2)); n1, n2 = expand(m.group(3), m.group(4))
    if len(e1) == 7 or len(n1) == 7: return None
    ne, nn = len(e1), len(n1)
    try:
        E = sorted([scale(e1, ne), scale(e2, len(e2) if len(e2)==ne else ne)])
        N = sorted([scale(n1, nn), scale(n2, len(n2) if len(n2)==nn else nn)])
    except Exception: return None
    # range widths: coarse units mean the box covers the whole last-digit cell
    cell_e = {3:1000,4:100,5:10,6:1}[ne]; cell_n = {3:1000,4:100,5:10,6:1}[nn]
    E = [E[0], E[1] + cell_e]; N = [N[0], N[1] + cell_n]
    # northing-first ordering (e.g. 626215/221800): swap if first looks like a northing
    if E[0] > 400000 and N[0] < 300000: E, N = N, E
    # OIG -> NIG
    if N[0] < 350000 and E[0] < 200000 and N[0] > 0:
        if N[0] < 300000 and E[0] < 300000:
            E = [E[0] + 50000, E[1] + 50000]; N = [N[0] + 500000, N[1] + 500000]
    if not (100000 <= E[0] <= 300000 and 350000 <= N[0] <= 820000): return None
    if E[1] - E[0] > 30000 or N[1] - N[0] > 30000: return None
    return (E[0], E[1], N[0], N[1])

def dist(b, g):
    dx = max(g[0] - b[1], b[0] - g[1], 0); dy = max(g[2] - b[3], b[2] - g[3], 0)
    return math.hypot(dx, dy)

def refs(text):
    text = BIDI.sub('', text)
    out = []
    for k in KEY.finditer(text):
        win = text[k.end():k.end() + 80]
        for p in PAT.finditer(win):
            b = box(p)
            if b: out.append((k.start() + p.start(), p.group(0).replace('\n', ' '), b))
            break
    return out

rows = []
for f in sorted(glob.glob(os.path.join(ROOT, 'en', 'vol-*', '*.txt'))):
    t = open(f, encoding='utf-8', errors='replace').read()
    rs = refs(t)
    if len(rs) < 2: continue
    # general = refs in the first 1,200 chars of text after the date line
    first = rs[0][0]
    gen = [r for r in rs if r[0] < first + 600]
    sub = [r for r in rs if r[0] >= first + 600]
    if not sub: continue
    hf = f.replace('/en/', '/he/')
    ht = BIDI.sub('', open(hf, encoding='utf-8', errors='replace').read()) if os.path.exists(hf) else ''
    for pos, s, b in sub:
        d = min(dist(b, g[2]) for g in gen)
        if d > THRESH:
            digits = re.sub(r'[^0-9]', ' ', s).split()
            in_he = all(x in ht for x in digits) if ht else None
            ctx = re.sub(r'\s+', ' ', t[max(0, pos - 160):pos + 60])
            rows.append(dict(file=f.replace(ROOT + '/', ''), general=' ; '.join(g[1] for g in gen), sub_ref=s,
                             dist_m=round(d), same_digits_in_he=in_he, context=ctx))
with open(OUT, 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print(len(rows), 'flags')
