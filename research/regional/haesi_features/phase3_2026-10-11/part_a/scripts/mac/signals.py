#!/usr/bin/env python3
"""Per TOC item: its text (located start to next located start), map refs and gazetteer hits within it.
Writes signals.tsv: vol n printed pdfpage how title refs hits nchars.
gaz.json holds the phase-2 frozen gazetteer and region-wide terms (PLAN.md JSON block). NOISE terms are common Hebrew
words dropped from the BODY-text count only; titles were screened with the full gazetteer (../screen_titles.py).
Copied from the Mac scratch copy."""
import os, re, json, collections, unicodedata, sys
base = os.path.expanduser("~/p3a_scratch/")
DROP = "ʿʾ‘’'`´׳ʽʻ’"; SPACE = "-–—,.;:()[]/\"״“”־"
def norm(s):
    s = unicodedata.normalize("NFKD", s); s = "".join(c for c in s if not unicodedata.combining(c)).lower()
    for c in DROP: s = s.replace(c, "")
    for c in SPACE: s = s.replace(c, " ")
    return " ".join(s.split())
g = json.load(open(base + "bin/gaz.json", encoding="utf-8"))
NOISE = {"גילה", "ביתר", "דרגה", "קדר", "תומר", "נעמה", "מוצא", "פסגות", "מנחת", "רימונים", "סככה", "עוגה", "רמות", "גבע", "מלחה"}
pats = []
for z, d in list(g["gazetteer"].items()) + [("RW", g["region_wide_terms"])]:
    for t in d["en"] + d["he"]:
        tn = norm(t); he = bool(re.search(r"[֐-׿]", tn))
        if tn in NOISE: continue
        pats.append((z.split("_")[0], tn, re.compile(r"(?:(?<=\s)|^)" + ("[בהולמכש]{0,2}" if he else "") + re.escape(tn) + r"(?=\s|$)")))
REF1 = re.compile(r"נ[\.״\"]?\s?צ[\.׳']?\s*[\(\)]?\s*(\d{3,6})\s*[/\-\s\.]\s*(\d{3,6})")
REF2 = re.compile(r"(?<![\d/])(\d{4,6})\s*/\s*(\d{4,6})(?![\d/])")
items = collections.defaultdict(list)
for l in open(base + "items.tsv", encoding="utf-8"):
    f = l.rstrip("\n").split("\t")
    items[f[0]].append(f)
out = open(base + "signals.tsv", "w", encoding="utf-8")
for v in sorted(items):
    pages = {}
    for l in open(base + "txt/%s.pages.txt" % v, encoding="utf-8"):
        p, _, t = l.rstrip("\n").partition("\t"); pages[int(p[1:])] = t
    loc = sorted([(int(f[3]), int(f[4]), int(f[1])) for f in items[v] if f[3]])
    nxt = {}
    for i, (p, pos, n) in enumerate(loc):
        nxt[n] = loc[i + 1][:2] if i + 1 < len(loc) else (max(pages), len(pages[max(pages)]))
    for f in items[v]:
        n = int(f[1])
        if f[3]:
            p0, s0 = int(f[3]), int(f[4]); p1, s1 = nxt[n]
            txt = ""
            for p in range(p0, p1 + 1):
                t = pages.get(p, "")
                a = s0 if p == p0 else 0; b = s1 if p == p1 else len(t)
                txt += " " + t[a:b]
        else:
            a = int(re.split("[–-]", f[2])[0]); b = int(re.split("[–-]", f[2])[-1])
            txt = " ".join(pages.get(p, "") for p in range(a, b + 3))
        refs = []
        for rx in (REF1, REF2):
            for m in rx.finditer(txt):
                s = "%s/%s" % m.groups()
                if s not in refs: refs.append(s)
        nt = norm(txt); hits = collections.Counter()
        for z, t, rx in pats:
            c = len(rx.findall(nt))
            if c: hits["%s:%s" % (z, t)] += c
        out.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%d\n" % (v, f[1], f[2], f[3], f[5][:12], f[6], ";".join(refs), " ".join("%s=%d" % kv for kv in sorted(hits.items())), len(txt)))
