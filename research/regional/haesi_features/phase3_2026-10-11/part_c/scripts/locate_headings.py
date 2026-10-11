#!/usr/bin/env python3
"""HA-ESI phase 3, part C: locate every report heading of one volume in its reading-order text and screen it.

Runs where the text is (after screen_volume.py); standard library only.

Heading sources
  --mode toc   rows of <vol>.toc.csv (table of contents: title, authors, printed page), located in the body in
               contents order: the first line after the previous heading that begins with the title (first four
               words) and is followed within four lines by the first author's surname; failing that, a line that
               begins with the title. A file <vol>.toc_fix.csv (same columns), if present, replaces toc.csv.
  --mode caps  ESI 1 and 4 style: every all-capitals line of the English body is a report heading.

Screen rule (phase-2 plan §3.3 and §4; amendment A3)
  1. A heading's map references are those in its span (heading line to the line before the next heading).
     Its zone is the zone of its first map reference; 'zones_in_span' lists any reference in a zone.
  2. Without a map reference, the title is matched to the frozen gazetteer (plus the A3 variants).
  3. Otherwise the heading is outside the region by name.

Output: <vol>.screen.csv (one row per heading) and <vol>.orphans.csv (map references in no located span).
"""
import argparse
import bisect
import csv
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path

DROP_CHARS = "ʿʾ‘’'`´׳ʽʻ’"
SPACE_CHARS = "-–—,.;:()[]/\"״“”"
A3_VARIANTS = {"Z2_JORDAN_VALLEY": ["hagedud"], "Z4_JERUSALEM_HILLS": ["anathoth", "land of benjamin", "kh el burj", "khirbet el burj"]}
ZONES = ["Z1_GERIZIM", "Z2_JORDAN_VALLEY", "Z3_JUDEAN_DESERT", "Z4_JERUSALEM_HILLS"]


def norm(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower()
    for c in DROP_CHARS:
        s = s.replace(c, "")
    for c in SPACE_CHARS:
        s = s.replace(c, " ")
    return " " + " ".join(s.split()) + " "


def gaz_patterns(params):
    pats = {}
    for z, g in params["gazetteer"].items():
        pats[z] = sorted(set(norm(p).strip() for p in g["en"] + g["he"] if norm(p).strip()))
    for z, v in A3_VARIANTS.items():
        pats[z] = sorted(set(pats[z]) | set(v))
    rw = params["region_wide_terms"]
    pats["REGION_WIDE"] = sorted(set(norm(p).strip() for p in rw["en"] + rw["he"]))
    return pats


def title_hits(title, pats):
    nt = norm(title)
    out = {}
    for z, ps in pats.items():
        h = [p for p in ps if (" " + p + " ") in nt]
        if h:
            out[z] = h
    return out


def clean_title(t):
    t = re.sub(r"\((?:[A-Za-z0-9]{1,2}-|[0O]\.-)[^)]*\)?", " ", t)  # permit / licence numbers
    t = re.sub(r"[*•■]", " ", t)
    return " ".join(t.split())


def words(s):
    return norm(s).split()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vol", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--params", required=True)
    ap.add_argument("--mode", choices=["toc", "caps"], required=True)
    ap.add_argument("--lang", default="en")
    a = ap.parse_args()
    w = Path(a.work)
    params = json.loads(Path(a.params).read_text(encoding="utf-8"))
    pats = gaz_patterns(params)
    lines = (w / (a.vol + ".ordered.txt")).read_text(encoding="utf-8").split("\n")
    pages = list(csv.DictReader(open(w / (a.vol + ".pages.csv"), encoding="utf-8")))
    pfirst = [int(p["first_line"]) for p in pages]
    plang = {int(p["ordered_page"]): p["lang"] for p in pages}

    def page_of(line):
        return bisect.bisect_right(pfirst, line)

    en_lines = [i for i in range(1, len(lines) + 1) if plang.get(page_of(i)) == a.lang]
    body_start = 1
    maprefs = list(csv.DictReader(open(w / (a.vol + ".mapref.csv"), encoding="utf-8")))
    heads = []
    if a.mode == "caps":
        for i in en_lines:
            s = lines[i - 1].strip()
            al = [c for c in s if c.isalpha()]
            if len(al) < 4 or len(s) > 90 or s[0].isdigit():
                continue
            if sum(c.isupper() for c in al) / len(al) >= 0.85 and not re.match(r"^(FIG|PLATE|TABLE|MAP)\b", s):
                heads.append(dict(line=i, title=s, authors="", toc_page="", how="caps line"))
    else:
        fix = w / (a.vol + ".toc_fix.csv")
        toc = list(csv.DictReader(open(fix if fix.exists() else w / (a.vol + ".toc.csv"), encoding="utf-8")))
        # body starts after the contents pages
        toc_pages = [int(r["ordered_page"]) for r in toc if r.get("ordered_page")]
        if toc_pages:
            last_toc = max(toc_pages)
            body_start = pfirst[last_toc] if last_toc < len(pfirst) else 1
        en_body = [i for i in en_lines if i >= body_start]
        def title_ok(lw, tw):
            key = tw[:min(4, len(tw))]
            full = lw[:len(tw)] == tw and len(" ".join(tw)) >= 4  # run-in heading (news in brief)
            if len(lw) > len(tw) + 6 and not full:
                return False
            return full or lw[:len(key)] == key or (len(lw) >= 2 and tw[:len(lw)] == lw and len(" ".join(lw)) >= 8)

        # pass 1: title + first author's surname within four lines, in contents order (monotone)
        found = [None] * len(toc)
        tws = [words(clean_title(r["title"])) for r in toc]
        pos = 0
        for k, r in enumerate(toc):
            tw = tws[k]
            if not tw:
                continue
            sur = words(r.get("authors", "").split(",")[0].split(" and ")[0])[-1:] if r.get("authors") else []
            if not sur:
                continue
            for jj in range(pos, min(len(en_body), pos + 4000)):
                lw = words(lines[en_body[jj] - 1])
                if lw and title_ok(lw, tw):
                    nxt = " ".join(" ".join(words(x)) for x in lines[en_body[jj]:en_body[jj] + 4]).split()
                    if sur[0] in nxt:
                        found[k] = (jj, "toc title + author line")
                        pos = jj + 1
                        break
        # pass 2: title line only, strictly between the neighbouring headings found in pass 1
        for k, r in enumerate(toc):
            if found[k] or not tws[k]:
                continue
            lo = max([found[q][0] for q in range(k) if found[q]] or [-1]) + 1
            hi = min([found[q][0] for q in range(k + 1, len(toc)) if found[q]] or [len(en_body)])
            for jj in range(lo, min(hi, lo + 3000)):
                lw = words(lines[en_body[jj] - 1])
                if lw and title_ok(lw, tws[k]):
                    found[k] = (jj, "toc title line")
                    break
        for k, r in enumerate(toc):
            f = found[k]
            heads.append(dict(line=en_body[f[0]] if f else "", title=r["title"], authors=r.get("authors", ""),
                              toc_page=r["printed_page"], how=f[1] if f else "NOT LOCATED"))
    located = sorted([h for h in heads if h["line"] != ""], key=lambda h: h["line"])
    starts = [h["line"] for h in located]
    lang_end = en_lines[-1] if en_lines else len(lines)
    for j, h in enumerate(located):
        h["end"] = (starts[j + 1] - 1) if j + 1 < len(starts) else lang_end
    rows = []
    assigned = set()
    for h in heads:
        refs = []
        if h["line"] != "":
            for m in maprefs:
                if h["line"] <= int(m["line"]) <= h["end"] and m["lang"] == a.lang:
                    refs.append(m)
                    assigned.add((m["line"], m["ref"]))
        hits = title_hits(clean_title(h["title"]), pats)
        zfirst = refs[0]["zone"] if refs else ""
        zany = sorted(set(m["zone"] for m in refs if m["zone"] in ZONES))
        if refs and zfirst in ZONES:
            dec = "in region (map ref, %s)" % zfirst
        elif refs and zany:
            dec = "part in region (first map ref %s; other refs %s)" % (zfirst or "unconverted", ",".join(zany))
        elif refs and zfirst == "outside":
            dec = "outside region (map ref)"
        elif refs:
            dec = "map ref not converted; name screen: " + (",".join(sorted(hits)) or "no match")
        elif hits:
            dec = "no map ref; name match " + ",".join(sorted(hits))
        else:
            dec = "no map ref; title names no region place"
        if h["how"] == "NOT LOCATED":
            dec = "heading not located in body; name screen: " + (",".join(sorted(hits)) or "no match")
        pg = page_of(h["line"]) if h["line"] != "" else None
        rows.append(dict(vol=a.vol, heading_line=h["line"], span_end=h.get("end", ""), ordered_page=pg or "",
                         toc_page=h["toc_page"], title=h["title"], authors=h["authors"], located=h["how"],
                         n_maprefs=len(refs), first_mapref=refs[0]["ref"] if refs else "", first_zone=zfirst,
                         first_latlon=("%s,%s" % (refs[0]["lat"], refs[0]["lon"])) if refs and refs[0]["lat"] else "",
                         zones_in_span=";".join(zany), title_hits=json.dumps(hits, ensure_ascii=False) if hits else "",
                         decision=dec))
    with open(w / (a.vol + ".screen.csv"), "w", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        wr.writeheader()
        wr.writerows(rows)
    orph = [m for m in maprefs if m["lang"] == a.lang and int(m["line"]) >= body_start and (m["line"], m["ref"]) not in assigned]
    with open(w / (a.vol + ".orphans.csv"), "w", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, fieldnames=list(maprefs[0]) if maprefs else ["line"], lineterminator="\n")
        wr.writeheader()
        wr.writerows(orph)
    c = Counter(r["decision"].split(" (")[0].split(";")[0] for r in rows)
    print(a.vol, "headings", len(rows), "not located", sum(1 for r in rows if r["located"] == "NOT LOCATED"),
          "orphan refs", len(orph), "in region", sum(1 for m in orph if m["zone"] in ZONES), dict(c))


if __name__ == "__main__":
    main()
