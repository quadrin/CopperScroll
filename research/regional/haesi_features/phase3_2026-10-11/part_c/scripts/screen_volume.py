#!/usr/bin/env python3
"""HA-ESI phase 3, part C: heading screen of one portal volume (phase-2 plan §3.3, S-LOC, on a whole volume).

Runs where the extracted text is (the owner's computer); standard library plus pyproj.
Text is never written into the repository; only the small screen tables made from it are.

Inputs
  --raw     pdftotext -raw output of the volume
  --layout  pdftotext -layout output of the same PDF (used for the table of contents only)
  --params  the JSON block of the frozen phase-2 PLAN.md (zones, gazetteer), as exported by export_params.py
  --vol     volume key, e.g. ESI10 or HAESI112
  --kind    'esi' (one English text, PDF order = reading order) or 'bilingual' (HA-ESI 109-115: Hebrew pages
            in PDF order, English pages bound back to front, so their PDF order is reversed for reading)
  --out     output folder

Outputs (in --out)
  <vol>.ordered.txt  reading-order text (ESI: the raw file unchanged; bilingual: Hebrew pages in PDF order,
                     then English pages in reading order). Line numbers in all tables refer to this file.
  <vol>.pages.csv    ordered page index, PDF page, language, printed page detected, first ordered line
  <vol>.mapref.csv   every 'map ref' occurrence: ordered line, page, the reference string, lat/lon, zone
  <vol>.toc.csv      table-of-contents rows parsed from the layout text: title, authors, printed page

The heading location (TOC row -> ordered line) and the screen decision are made by locate_headings.py.
"""
import argparse
import csv
import json
import re
import unicodedata
from pathlib import Path

from pyproj import Transformer

T_OIG = Transformer.from_crs("EPSG:28191", "EPSG:4326", always_xy=True)
T_NIG = Transformer.from_crs("EPSG:2039", "EPSG:4326", always_xy=True)
UNIT = {3: 1000, 4: 100, 5: 10, 6: 1}

DROP_CHARS = "ʿʾ‘’'`´׳ʽʻ’"
SPACE_CHARS = "-–—,.;:()[]/\"״“”"


def norm(s):
    """Phase-1/phase-2 title normalisation (copied from phase2 scripts/common.py, unchanged)."""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower()
    for c in DROP_CHARS:
        s = s.replace(c, "")
    for c in SPACE_CHARS:
        s = s.replace(c, " ")
    return " " + " ".join(s.split()) + " "


def zone_of(lat, lon, params):
    for z in params["zones_order"]:
        for la0, la1, lo0, lo1 in params["zones"][z]:
            if la0 <= lat <= la1 and lo0 <= lon <= lo1:
                return z
    return "outside"


def parse_num(tok):
    tok = re.sub(r"\D", "", tok)
    d = len(tok)
    if d not in UNIT:
        raise ValueError(tok)
    return int(tok) * UNIT[d], UNIT[d]


def convert(e_tok, n_tok, grid_label=""):
    """Phase-1 geo.parse_ref rules: digits give the unit; northing > 400000 = NIG, < 300000 = OIG."""
    e, ue = parse_num(e_tok)
    n, un = parse_num(n_tok)
    swapped = False
    if e > 400000 and n < 300000:
        e, n, ue, un = n, e, un, ue
        swapped = True
    grid = grid_label.upper() if grid_label.upper() in ("OIG", "NIG") else ("NIG" if n > 400000 else ("OIG" if n < 300000 else ""))
    if not grid:
        raise ValueError("grid")
    # plausibility (OCR errors such as '6129/2366'): grid eastings of Cisjordan lie between 100 and 300 km (OIG)
    # or 150 and 350 km (NIG); such a reference is listed but not converted.
    if not ((grid == "OIG" and 100000 <= e <= 300000 and 0 <= n <= 300000) or
            (grid == "NIG" and 150000 <= e <= 350000 and 400000 <= n <= 800000)):
        raise ValueError("implausible grid value")
    lon, lat = (T_OIG if grid == "OIG" else T_NIG).transform(e, n)
    return dict(e=e, n=n, unit=max(ue, un), grid=grid, lat=lat, lon=lon, swapped=swapped)


HEB = re.compile("[֐-׿]")
LAT = re.compile("[A-Za-z]")


def lang_of(page):
    h = len(HEB.findall(page))
    l = len(LAT.findall(page))
    if h > l:
        return "he"
    return "en" if l > 50 else "blank"


def order_pages(pages, kind):
    """Return list of (pdf_index, lang) in reading order."""
    langs = [lang_of(p) for p in pages]
    idx = list(range(len(pages)))
    if kind == "esi":
        return [(i, langs[i]) for i in idx]
    # bilingual: the English block is the last run of non-Hebrew pages after the last Hebrew page
    last_he = max(i for i in idx if langs[i] == "he")
    head = [(i, langs[i]) for i in idx if i <= last_he]
    tail = [(i, langs[i]) for i in reversed(idx) if i > last_he]
    return head + tail


PAGE_NUM = re.compile(r"^\*?\s*(\d{1,3})\s*\*?$")


def detect_printed(lines):
    ne = [l.strip() for l in lines if l.strip()]
    cands = []
    for l in ne[:3] + ne[-3:]:
        m = PAGE_NUM.match(l)
        if m:
            cands.append(int(m.group(1)))
    return cands


MAPREF = re.compile(
    r"(map\s*ref(?:erence)?s?\.?|נ[\"״”'׳]?\s?צ[\"״”'׳]?)\s*[:]?\s*(?:\(?(NIG|OIG|new|old)\b[^0-9]{0,15})?"
    r"(\d{3,6})(?:\s*[-–^]\s*\d{1,6})?\s*[/.]\s*(\d{3,6})", re.I)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", required=True)
    ap.add_argument("--layout", required=True)
    ap.add_argument("--params", required=True)
    ap.add_argument("--vol", required=True)
    ap.add_argument("--kind", choices=["esi", "bilingual"], required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    params = json.loads(Path(a.params).read_text(encoding="utf-8"))
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    raw = Path(a.raw).read_text(encoding="utf-8", errors="replace")
    lay = Path(a.layout).read_text(encoding="utf-8", errors="replace")
    rpages = raw.split("\f")
    lpages = lay.split("\f")
    order = order_pages(rpages, a.kind)

    # ordered text and page table
    olines, prow = [], []
    for k, (i, lg) in enumerate(order):
        pl = rpages[i].split("\n")
        prow.append(dict(ordered_page=k + 1, pdf_page=i + 1, lang=lg, printed_detected=";".join(map(str, detect_printed(pl))),
                         first_line=len(olines) + 1, n_lines=len(pl)))
        olines.extend(pl)
    (out / (a.vol + ".ordered.txt")).write_text("\n".join(olines), encoding="utf-8")
    with open(out / (a.vol + ".pages.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(prow[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(prow)

    # map references (in the ordered text; newlines allowed inside a reference)
    text = "\n".join(olines)
    starts = [0]
    for l in olines:
        starts.append(starts[-1] + len(l) + 1)
    import bisect
    page_first = [p["first_line"] for p in prow]
    mrows = []
    for m in MAPREF.finditer(text):
        line = bisect.bisect_right(starts, m.start())
        pg = bisect.bisect_right(page_first, line)
        ref = " ".join(text[m.start():m.end()].split())
        row = dict(line=line, ordered_page=pg, pdf_page=prow[pg - 1]["pdf_page"], lang=prow[pg - 1]["lang"],
                   ref=ref, e_tok=m.group(3), n_tok=m.group(4), grid_label=(m.group(2) or ""), grid="", lat="", lon="",
                   zone="", note="")
        try:
            c = convert(m.group(3), m.group(4), m.group(2) or "")
            row.update(grid=c["grid"], lat="%.5f" % c["lat"], lon="%.5f" % c["lon"], zone=zone_of(c["lat"], c["lon"], params),
                       note="swapped" if c["swapped"] else "")
        except Exception as ex:  # noqa: BLE001
            row.update(note="not converted: %s" % ex)
        mrows.append(row)
    with open(out / (a.vol + ".mapref.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["line", "ordered_page", "pdf_page", "lang", "ref", "e_tok", "n_tok", "grid_label",
                                          "grid", "lat", "lon", "zone", "note"], lineterminator="\n")
        w.writeheader()
        w.writerows(mrows)

    # table of contents (layout text, reading order); rows 'title   authors   page'
    toc = []
    in_toc = False
    n_toc_pages = 0
    ROW = re.compile(r"^(\s*)(\S.*?\S)\s{2,}(\S.*?\S)?\s{2,}[^\w\s]*\s*(\d{1,3})\s*[^\w\s]*\s*$")
    ROW2 = re.compile(r"^(\s*)(\S.*?\S)\s{2,}(\S.*?\S)[\s*.,■]*$")
    NUM = re.compile(r"^[\s*.,■’']*(\d{1,3})[\s*.,■’']*$")
    SKIP = re.compile(r"^(List of Illustrations|Index of Sites|Map of Sites|Hebrew Text|Glossary|Preface|Abbreviations)", re.I)
    for k, (i, lg) in enumerate(order):
        if lg != "en" or i >= len(lpages):
            continue
        p = lpages[i]
        first = next((l.strip() for l in p.split("\n") if l.strip()), "")
        nrows = len([l for l in p.split("\n") if ROW.match(l) or ROW2.match(l)])
        if re.search(r"^\s*(Table of )?Contents\s*$", p, re.M | re.I) and n_toc_pages == 0:
            in_toc = True
        elif in_toc and (nrows < 3 or re.match(r"^(List of Illustrations|Fig|Index)", first, re.I) or n_toc_pages >= 6):
            in_toc = False
            n_toc_pages = 99  # one contents block per volume
        if not in_toc:
            continue
        n_toc_pages += 1
        lines = p.split("\n")
        prev_single = ""
        for j, l in enumerate(lines):
            m = ROW.match(l)
            rec = None
            if m:
                rec = dict(indent=len(m.group(1)), title=m.group(2), authors=(m.group(3) or "").strip(" *,."), printed_page=m.group(4))
            else:
                m2 = ROW2.match(l)
                if m2 and j + 1 < len(lines):
                    for l2 in lines[j + 1:j + 3]:
                        m3 = NUM.match(l2)
                        if m3:
                            rec = dict(indent=len(m2.group(1)), title=m2.group(2), authors=m2.group(3).strip(" *,."),
                                       printed_page=m3.group(1))
                            break
            if rec is None:
                s = l.strip()
                prev_single = s if (s and "  " not in s and not NUM.match(l) and len(s) > 3) else ""
                continue
            if prev_single and (rec["title"][:1].islower() or rec["title"].startswith(("in ", "and ", "of "))):
                rec["title"] = prev_single + " " + rec["title"]
            prev_single = ""
            if SKIP.match(rec["title"]):
                continue
            rec.update(ordered_page=k + 1, toc_line=l.strip()[:160])
            toc.append(rec)
    with open(out / (a.vol + ".toc.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["ordered_page", "indent", "title", "authors", "printed_page", "toc_line"],
                           lineterminator="\n")
        w.writeheader()
        w.writerows(toc)
    zc = {}
    for r in mrows:
        zc[r["zone"]] = zc.get(r["zone"], 0) + 1
    print(a.vol, "pages", len(prow), "lines", len(olines), "maprefs", len(mrows), zc, "toc rows", len(toc))


if __name__ == "__main__":
    main()
