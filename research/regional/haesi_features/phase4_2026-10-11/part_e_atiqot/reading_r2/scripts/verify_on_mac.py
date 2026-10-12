#!/usr/bin/env python3
"""Run on the owner's Mac (in $HOME/p4text/r2, outside the repository) against the extracted text.

For every unit: PDF page count, SHA-256 of the article text (raw text of PDF pages 2..N, i.e. without the
portal cover page, whitespace collapsed to single spaces, UTF-8), and the printed page numbers seen on each
PDF page. For every coded quote: whether it occurs verbatim (after normalising quote marks, dashes and
whitespace) on a PDF page, which page, and the printed numbers seen on that page. Hebrew quotes (logical order,
while pdftotext gives visual order) are checked as a set of words on one page.

Usage: python3 verify_on_mac.py quotes.json > verify.json
Standard library only. Prints JSON; no text from the PDFs is printed beyond page numbers.
"""
import hashlib
import json
import re
import sys
import unicodedata

HEB = re.compile("[א-ת]")


def variants(s):
    """Two readings of line-end hyphens: kept (pre-existing) and dropped (re-joined word)."""
    a = re.sub("([-–—])[ \t]*\n\\s*", r"\1", s)
    c = re.sub(r"(\w)-[ \t]*\n\s*(\w)", r"\1\2", s)
    c = re.sub("([–—])[ \t]*\n\\s*", r"\1", c)
    return [norm(a), norm(c)]


def norm(s):
    s = unicodedata.normalize("NFKC", s)
    for a, b in (("‘", "'"), ("’", "'"), ("ʼ", "'"), ("ʻ", "'"), ("ʽ", "'"), ("“", '"'),
                 ("”", '"'), ("–", "-"), ("—", "-"), ("×", "x"), ("­", ""), ("׳", "'"),
                 ("״", '"'), ("‎", ""), ("‏", ""), ("‪", ""), ("‫", ""), ("‬", "")):
        s = s.replace(a, b)
    return " ".join(s.split())


def heb_words(s):
    s = norm(s)
    return [w for w in re.split(r"[\s,.;:()\[\]!?\"'/]+", s) if w]


def page_numbers(page):
    nums = []
    for line in page.split("\n"):
        t = line.strip()
        m = re.fullmatch(r"\*?(\d{1,3})(\*?)", t) or re.search(r"[A-Za-z’,)א-ת] (\d{1,3})(\*?)$", t) \
            or re.match(r"^(\d{1,3})(\*?) [A-Zא-ת]", t) or re.search(r"(\d{1,3}) of \d{1,3}$", t)
        if m:
            nums.append(m.group(1) + (m.group(2) if m.lastindex and m.lastindex >= 2 and m.group(2) else ""))
    return nums


def main():
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    out = {"units": {}, "quotes": []}
    pages = {}
    global layout_pages
    layout_pages = {}
    for u in spec["units"]:
        try:
            layout_pages[u] = open(u + ".layout.txt", encoding="utf-8", errors="replace").read().split("\f")
        except OSError:
            layout_pages[u] = []
        raw = open(u + ".raw.txt", encoding="utf-8", errors="replace").read()
        pg = raw.split("\f")
        if pg and not pg[-1].strip():
            pg = pg[:-1]
        pages[u] = pg
        body = " ".join(" ".join(p.split()) for p in pg[1:])
        out["units"][u] = dict(pdf_pages=len(pg), text_sha256=hashlib.sha256(" ".join(body.split()).encode("utf-8")).hexdigest(),
                               chars=len(body), printed=[page_numbers(p)[:4] for p in pg])
    for q in spec["quotes"]:
        pg = pages[q["unit"]]
        hit, how = None, ""
        if HEB.search(q["quote"]):
            words = set(heb_words(q["quote"]))
            for i, p in enumerate(pg):
                pw = set(heb_words(p))
                if words <= pw:
                    hit, how = i, "hebrew word set"
                    break
            if hit is None:
                best = max(range(len(pg)), key=lambda i: len(words & set(heb_words(pg[i]))))
                miss = sorted(words - set(heb_words(pg[best])))
                how = "hebrew: best page %d missing %s" % (best + 1, miss)
        else:
            nq = norm(q["quote"])
            for i, p in enumerate(pg):
                if any(nq in v for v in variants(p)):
                    hit, how = i, "verbatim"
                    break
            if hit is None:
                for i in range(len(pg) - 1):
                    if any(nq in v for v in variants(pg[i] + "\n" + pg[i + 1])):
                        hit, how = i, "verbatim across page break"
                        break
            if hit is None:
                lay = layout_pages.get(q["unit"], [])
                for i, p in enumerate(lay):
                    if any(nq in v for v in variants(p)):
                        hit, how = i, "verbatim in layout text"
                        break
            if hit is None:
                nqs = nq.replace(" ", "").lower()
                for i, p in enumerate(pg):
                    if any(nqs in v.replace(" ", "").lower() for v in variants(p)):
                        hit, how = i, "space-insensitive only (extraction lost spaces)"
                        break
        out["quotes"].append(dict(unit=q["unit"], i=q["i"], found=hit is not None, how=how,
                                  pdf_page=(hit + 1) if hit is not None else None,
                                  printed_on_page=page_numbers(pg[hit]) if hit is not None else [], claimed=q["page"]))
    json.dump(out, sys.stdout, ensure_ascii=False, indent=0)


if __name__ == "__main__":
    main()
