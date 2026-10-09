#!/usr/bin/env python3
"""Screen HA / ESI / HA-ESI tables of contents against the frozen name lists in search_plan.json.

Input: a cache folder with series_items.json (parsed item pages of publications.iaa.org.il) and
ha138/iss1.html (the HA-ESI 138 issue listing). Output: toc_items.csv (every table-of-contents item)
and toc_candidates.csv (items whose normalised title matches a place group or region name).

Run: python3 -I screen_toc.py <cache_dir> <out_dir>
Standard library only. Deterministic.
"""
import csv
import html
import json
import re
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
PLAN = HERE.parent / "search_plan.json"

DROP_CHARS = "ʿʾ‘’'`´׳"
SPACE_CHARS = "-–—,.;:()[]/\"״"


def norm(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower()
    for c in DROP_CHARS:
        s = s.replace(c, "")
    for c in SPACE_CHARS:
        s = s.replace(c, " ")
    return " " + " ".join(s.split()) + " "


def split_toc(desc):
    """Split a bepress description into (title_with_authors, pages) items."""
    out = []
    for m in re.finditer(r"(.+?)\[\s*([0-9]+(?:\s*[–-]\s*[0-9]+)?)\s*\]", desc):
        t = m.group(1).strip(" ,")
        out.append((t, m.group(2).replace(" ", "")))
    return out


def load_patterns(plan):
    groups = {}
    for gid, g in plan["places"]["names"].items():
        if gid == "R_JD_CLIFFS":
            continue
        pats = [norm(p).strip() for p in g.get("en", []) + g.get("he", [])]
        groups[gid] = sorted(set(p for p in pats if p))
    jd = plan["places"]["names"]["R_JD_CLIFFS"]
    jd_any = sorted(set(norm(p).strip() for p in jd["en_any"] + jd["he_any"]))
    jd_with = sorted(set(norm(p).strip() for p in jd["en_with_cave_or_survey"] + jd["he_with_cave_or_survey"]))
    jd_terms = sorted(set(norm(p).strip() for p in jd["cave_or_survey_terms"]["en"] + jd["cave_or_survey_terms"]["he"]))
    qelt = sorted(set(norm(p).strip() for p in plan["regions"]["R_WADI_QELT"]["names"]))
    return groups, jd_any, jd_with, jd_terms, qelt


HEB = re.compile(r"[א-ת]")
PREFIX = "בהולמכש"
S2 = False  # post-freeze supplementary screen (deviation D2): allow Hebrew prefix letters


def hits(ntitle, pats):
    out = []
    for p in pats:
        if (" " + p + " ") in ntitle:
            out.append(p)
        elif S2 and HEB.match(p) and re.search(" [" + PREFIX + "]{1,2}" + re.escape(p) + " ", ntitle):
            out.append(p)
    return out


def items_from_cache(cache):
    items = []
    meta = json.loads((cache / "series_items.json").read_text(encoding="utf-8"))
    for o in meta:
        f = o["file"].replace(".html", "")
        series, num = f.rsplit("_", 1)
        for i, (t, pages) in enumerate(split_toc(o.get("desc", ""))):
            items.append(dict(item_key=f"{f}#{i + 1:03d}", series=series, item_no=num, volume_title=o["title"],
                              year=o["date"], pdf_url=o["pdf"] or "", toc_text=t, pages=pages))
    page = (cache / "ha138" / "iss1.html").read_text(encoding="utf-8")
    for m in re.finditer(r'<p><a href="(https://publications\.iaa\.org\.il/ha-esi/vol138/iss1/([0-9]+))" >(.*?)</a>'
                         r'<br><span class="auth">(.*?)</span>', page):
        t = html.unescape(re.sub(r"<[^>]+>", "", m.group(3))).strip()
        a = html.unescape(m.group(4)).strip()
        items.append(dict(item_key=f"ha-esi_138_{int(m.group(2)):03d}", series="ha-esi", item_no="138",
                          volume_title="HA-ESI 138", year="2026", pdf_url=m.group(1), toc_text=f"{t} , {a}",
                          pages=m.group(2)))
    items.sort(key=lambda r: r["item_key"])
    return items


def main(cache, out):
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    groups, jd_any, jd_with, jd_terms, qelt = load_patterns(plan)
    items = items_from_cache(Path(cache))
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    cand = []
    for r in items:
        nt = norm(r["toc_text"])
        matched = {}
        for gid, pats in groups.items():
            h = hits(nt, pats)
            if h:
                matched[gid] = h
        h = hits(nt, jd_any)
        if h:
            matched["R_JD_CLIFFS"] = h
        h = hits(nt, jd_with)
        if h and hits(nt, jd_terms):
            matched.setdefault("R_JD_CLIFFS", []).extend(h)
        h = hits(nt, qelt)
        if h:
            matched["R_WADI_QELT"] = h
        r["groups"] = ";".join(sorted(matched))
        r["matched_terms"] = ";".join(sorted({t for v in matched.values() for t in v}))
        if matched:
            cand.append(r)
    fields = ["item_key", "series", "item_no", "volume_title", "year", "pages", "pdf_url", "toc_text", "groups", "matched_terms"]
    for name, rows in (("toc_items.csv", items), ("toc_candidates.csv", cand)):
        with open(out / name, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
            w.writeheader()
            w.writerows(rows)
    print(f"{len(items)} table-of-contents items; {len(cand)} candidates")


if __name__ == "__main__":
    if "--s2" in sys.argv:
        S2 = True
        sys.argv.remove("--s2")
    main(sys.argv[1], sys.argv[2])
