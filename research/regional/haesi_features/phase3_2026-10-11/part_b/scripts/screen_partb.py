#!/usr/bin/env python3
"""HA-ESI phase 3, part B: heading screen of the HA Hebrew volumes 73-108 (1980-1998).

Method: phase-2 plan section 3.3 (S-LOC) applied to whole volumes. Every heading of each volume's table of
contents (or, for volumes without one, the headings listed by hand in data/headings_manual.csv) is screened:
map references printed on the heading's pages are converted (Old Israel Grid EPSG:28191, New Israel Grid
EPSG:2039; phase-1 geo.py) and zoned with the frozen phase-2 boxes; the heading (English and Hebrew, with
its group heading) is matched to the frozen gazetteer plus the A3 variants. The automatic flags only decide
which headings must be opened; the decision for every flagged heading is made by reading its first lines
(data/decisions/*.csv) and the build script (build_partb.py) merges the two.

The pdftotext output is NOT in the repository. Run (from the repository root):
  python3 -I research/regional/haesi_features/phase3_2026-10-11/part_b/scripts/screen_partb.py TEXTDIR
where TEXTDIR holds IAA_HA_<key>.raw.txt and .layout.txt (pdftotext -raw and -layout of the portal PDFs).
Writes part_b/data/screen_auto.csv and part_b/data/refs_auto.csv. Deterministic.
"""
import csv
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
PARTB = HERE.parent
PHASE2 = PARTB.parent.parent / "phase2_2026-10-10"
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(PHASE2 / "scripts"))
import common  # noqa: E402  phase-2 helpers (frozen plan params, norm, zones); puts phase-1 scripts on the path
import geo  # noqa: E402
import textlib  # noqa: E402
import toc  # noqa: E402

DATA = PARTB / "data"
# A3 name variants (phase-2 AMENDMENTS.md A3), with Hebrew forms; matched like gazetteer terms.
A3_VARIANTS = {
    "Z2_JORDAN_VALLEY": ["hagedud", "הגדוד"],
    "Z4_JERUSALEM_HILLS": ["anathoth", "land of benjamin", "ארץ בנימין", "kh el burj", "ח אל בורג"],
}
HE_PREFIX = "בהולמכש"  # phase-1 screen S2: one or two prefix letters before a Hebrew name
REF = re.compile(r"(?<![\d/])(\d{3,6})\s?/\s?(\d{3,6})(?![\d/])")
NZ = re.compile(r"נ[״\"׳'.]{1,2}\s?צ")


def read_csv(p):
    with open(p, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(p, fields, rows):
    with open(p, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fields})


def prenorm(s):
    # Hebrew maqaf and geresh-like marks treated as the plan's hyphens/apostrophes
    return s.replace("־", " ").replace("״", " ").replace("׳", "")


def patterns(params):
    pats = common.gazetteer_patterns(params)
    for z, terms in A3_VARIANTS.items():
        pats[z] = sorted(set(pats[z]) | {common.norm(t).strip() for t in terms})
    return pats


def hits(title, pats):
    nt = common.norm(prenorm(title))
    out = {}
    for z, ps in pats.items():
        h = []
        for p in ps:
            if (" " + p + " ") in nt:
                h.append(p)
            elif re.search(r"[א-ת]", p) and re.search(r" [%s]{1,2}%s " % (HE_PREFIX, re.escape(p)), nt):
                h.append(p + " (prefix)")
        if h:
            out[z] = h
    return out


def printed_map(vol):
    """PDF page -> printed page number, from page-number lines; gaps filled from the nearest detected page."""
    det = {}
    for i, p in enumerate(vol.layout_pages):
        ls = [l.strip() for l in p if l.strip()]
        for l in ls[:2] + ls[-2:]:
            m = re.fullmatch(r"[-־–­\s]*(\d{1,3})[-־–­\s]*", l)
            if m:
                det[i + 1] = int(m.group(1))
                break
    # keep detections consistent with the dominant local offset
    offs = Counter(pg - n for pg, n in det.items())
    good = {pg: n for pg, n in det.items() if offs[pg - n] >= 2}
    pmap = {}
    keys = sorted(good)
    for pg in range(1, len(vol.layout_pages) + 1):
        if pg in good:
            pmap[pg] = good[pg]
            continue
        prev = [k for k in keys if k < pg]
        nxt = [k for k in keys if k > pg]
        if prev and nxt and (prev[-1] - good[prev[-1]]) == (nxt[0] - good[nxt[0]]):
            pmap[pg] = pg - (prev[-1] - good[prev[-1]])
        elif prev and not nxt:
            pmap[pg] = pg - (prev[-1] - good[prev[-1]])
        elif nxt and not prev:
            pmap[pg] = pg - (nxt[0] - good[nxt[0]])
        else:
            pmap[pg] = None
    return pmap


def pdf_of_printed(pmap, printed):
    c = [pg for pg, n in sorted(pmap.items()) if n == printed]
    return c[0] if c else None


def page_refs(vol, params, a, b):
    """All map references on PDF pages a..b (raw text), converted and zoned."""
    out = []
    for i, (ln, pg) in enumerate(zip(vol.lines, vol.line_page)):
        if pg < a or pg > b:
            continue
        for m in REF.finditer(ln):
            txt = m.group(1) + "/" + m.group(2)
            try:
                r = geo.parse_ref(txt)
            except ValueError:
                continue
            if r["grid"] == "OIG" and not (90000 <= r["e"] <= 270000 and -120000 <= r["n"] <= 300000):
                continue
            if r["grid"] == "NIG" and not (140000 <= r["e"] <= 270000 and 350000 <= r["n"] <= 800000):
                continue
            lat, lon = geo.to_wgs84(r["e"], r["n"], r["grid"])
            ctx = " ".join(vol.lines[max(0, i - 3):i + 1])
            out.append(dict(line=i + 1, page=pg, ref=txt, grid=r["grid"], lat=lat, lon=lon,
                            zone=common.zone_of(lat, lon, params) or "outside", nz=bool(NZ.search(ctx))))
    return out


def main(textdir):
    params = common.plan_params()
    pats = patterns(params)
    vols = read_csv(DATA / "volumes.csv")
    fixes = read_csv(DATA / "toc_fixes.csv") if (DATA / "toc_fixes.csv").exists() else []
    manual = read_csv(DATA / "headings_manual.csv") if (DATA / "headings_manual.csv").exists() else []
    rows, refrows = [], []
    for vrow in vols:
        key = vrow["key"]
        vol = textlib.Volume(textdir, key)
        assert vol.raw_sha256 == vrow["raw_sha256"], (key, "raw text hash differs")
        pmap = printed_map(vol)
        if vrow["toc_pages"]:
            ents = [e for e in toc.parse(vol, [int(x) for x in vrow["toc_pages"].split(";")])]
            for e in ents:
                e["source"] = "toc p%s l%s" % (e["toc_page"], e["toc_line"])
                e["key"] = "%s:%s" % (e["toc_page"], e["toc_line"])
            # manual fixes: drop, set fields, or insert
            fx = [f for f in fixes if f["key"] == key]
            for f in fx:
                tgt = [e for e in ents if e["key"] == f["toc_key"]]
                if f["action"] == "insert":
                    ents.append(dict(key=f["toc_key"], toc_page=0, toc_line=0, indent=0, group=f["group"], group_he="",
                                     en=f["en"], he=f["he"], page_tok=f["page"], page=int(f["page"]) if f["page"] else None,
                                     page_note="added by hand: " + f["note"], is_group=False, source="toc fix (insert)"))
                    continue
                assert tgt, (key, f["toc_key"])
                e = tgt[0]
                if f["action"] == "drop":
                    e["drop"] = f["note"] or "not a report heading"
                elif f["action"] == "set":
                    for k in ("en", "he", "group"):
                        if f[k]:
                            e[k] = f[k]
                    if f["page"]:
                        e["page"], e["page_note"] = int(f["page"]), "page fixed by hand: " + f["note"]
                    if f.get("is_group"):
                        e["is_group"] = f["is_group"] == "yes"
            ents = [e for e in ents if not e.get("drop")]
            # keep page order after hand insertions (an entry without a page stays after its predecessor)
            last = 0
            for i, e in enumerate(ents):
                if e["page"] is not None:
                    last = e["page"]
                e["_ord"] = (e["page"] if e["page"] is not None else last + 0.5, i if e["source"] != "toc fix (insert)" else 10 ** 5)
            ents.sort(key=lambda e: e["_ord"])
        else:
            ents = []
        for m in [m for m in manual if m["key"] == key]:
            ents.append(dict(key="manual:%s" % m["pdf_page"], toc_page=0, toc_line=0, indent=0, group=m["group"],
                             group_he="", en=m["en"], he=m["he"], page_tok="", page=int(m["printed_page"]) if m["printed_page"] else None,
                             page_note="heading listed by hand from the body (no table of contents)", is_group=False,
                             source="body heading p%s" % m["pdf_page"], pdf_page=int(m["pdf_page"])))
        # groups with children are headers, not reports
        heads = [e for e in ents if not e["is_group"]]
        has_child = {e["group"] for e in heads if e["group"]}
        for e in heads:
            if e.get("pdf_page") is None:
                e["pdf_page"] = pdf_of_printed(pmap, e["page"]) if e["page"] is not None else None
        # keep list order (tables of contents run in page order); hand-listed body headings go in by page
        toc_heads = [e for e in heads if not e["key"].startswith("manual:")]
        for m in [e for e in heads if e["key"].startswith("manual:")]:
            pos = len([e for e in toc_heads if e["pdf_page"] is not None and e["pdf_page"] <= m["pdf_page"]])
            idx = [i for i, e in enumerate(toc_heads) if e["pdf_page"] is not None]
            toc_heads.insert(idx[pos - 1] + 1 if pos else 0, m)
        heads = toc_heads
        seen_on_page = {}
        for n, e in enumerate(heads):
            a = e["pdf_page"]
            prv = [h["pdf_page"] for h in heads[:n] if h["pdf_page"] is not None]
            nxt = [h["pdf_page"] for h in heads[n + 1:] if h["pdf_page"] is not None and h["pdf_page"] >= (a or 0)]
            if a is None:
                a = prv[-1] if prv else None
                e["page_note"] += "; pages searched between the neighbouring headings"
            b = nxt[0] if nxt else a
            title = " ".join(x for x in (e.get("group", ""), e["en"], e.get("group_he", ""), e["he"]) if x)
            th = hits(title, pats)
            refs = page_refs(vol, params, a, b) if a else []
            zr = Counter(r["zone"] for r in refs)
            in_reg_refs = [r for r in refs if r["zone"] != "outside"]
            is_header_only = e["en"] in has_child and not e["group"] and e["page"] is not None and any(
                h["group"] == e["en"] for h in heads)
            if is_header_only:
                auto = "group heading (children screened)"
            elif th and "REGION_WIDE" not in th or (th and len(th) > 1):
                auto = "flag: title names a place in the region"
            elif th:
                auto = "flag: region-wide term in title"
            elif in_reg_refs:
                auto = "flag: map ref on its pages falls in the region"
            elif refs:
                auto = "outside region: map refs on its pages all outside the region"
            elif a is None:
                auto = "flag: page not located"
            else:
                auto = "outside region: no map ref on its pages; title not in gazetteer"
            pkey = ("%03d" % e["page"]) if e["page"] is not None else "p%03d" % (a or 0)
            seen_on_page[pkey] = seen_on_page.get(pkey, 0) + 1
            sid = "HA%s-%s-%d" % (vrow["vol_id"], pkey, seen_on_page[pkey])
            rows.append(dict(screen_id=sid, volume=vrow["label"], year=vrow["year"], source=e["source"],
                             group=e.get("group", ""), title_en=e["en"], title_he=e["he"], printed_page=e["page"] if e["page"] is not None else "",
                             page_note=e["page_note"], pdf_pages="%s-%s" % (a, b) if a else "",
                             title_hits=";".join("%s:%s" % (z, ",".join(h)) for z, h in sorted(th.items())),
                             zone_by_title=";".join(sorted(z for z in th if z != "REGION_WIDE")),
                             refs_on_pages=len(refs), refs_in_region=";".join(sorted("%s(%s)" % (r["ref"], r["zone"][:2]) for r in in_reg_refs)),
                             ref_zones=";".join("%s:%d" % kv for kv in sorted(zr.items())), auto_decision=auto))
            for r in refs:
                refrows.append(dict(screen_id=sid, line=r["line"], pdf_page=r["page"], ref=r["ref"], grid=r["grid"],
                                    lat="%.5f" % r["lat"], lon="%.5f" % r["lon"], zone=r["zone"], after_nz="yes" if r["nz"] else "no"))
    fields = ["screen_id", "volume", "year", "source", "group", "title_en", "title_he", "printed_page", "page_note", "pdf_pages",
              "title_hits", "zone_by_title", "refs_on_pages", "refs_in_region", "ref_zones", "auto_decision"]
    write_csv(DATA / "screen_auto.csv", fields, rows)
    write_csv(DATA / "refs_auto.csv", ["screen_id", "line", "pdf_page", "ref", "grid", "lat", "lon", "zone", "after_nz"], refrows)
    c = Counter(r["auto_decision"] for r in rows)
    print(len(rows), "headings;", dict(c))


if __name__ == "__main__":
    main(sys.argv[1])
