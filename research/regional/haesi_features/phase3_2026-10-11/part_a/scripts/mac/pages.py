#!/usr/bin/env python3
"""Join pdftotext -raw output into one line of text per PDF page (logical order), strip bidi controls.
usage: pages.py RAW_TXT OUT_TXT   -> OUT has lines 'P<n>\t<text>'
(Copied from the Mac scratch copy; the bidi control characters are written here as \\u escapes.)"""
import sys
BIDI = dict.fromkeys(map(ord, "‪‫‬‭‮‎‏⁦⁧⁨⁩"), None)
t = open(sys.argv[1], encoding="utf-8").read().translate(BIDI)
pages = t.split("\f")
with open(sys.argv[2], "w", encoding="utf-8") as f:
    for i, p in enumerate(pages, 1):
        s = " ".join(p.split())
        f.write("P%d\t%s\n" % (i, s))
