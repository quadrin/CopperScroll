#!/usr/bin/env python3
"""Shared helpers for phase 4, part E (ʿAtiqot 42-121): page parsing, unit ids, gazetteer hits.

Gazetteer and normalisation: the frozen phase-2 plan (../../../phase2_2026-10-10/PLAN.md, JSON block) through
phase-2 scripts/common.py (amendment A1 normalisation), plus the A3 name variants as used in phase 3.
Standard library only (common.py imports geo.py, which needs pyproj only when grid conversion is called).
"""
import hashlib
import re
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
PART = HERE.parent
P4 = PART.parent
LANE = P4.parent
P2 = LANE / "phase2_2026-10-10"
sys.path.insert(0, str(P2 / "scripts"))
import common  # noqa: E402  phase-2 frozen plan parameters and normalisation (A1)

# A3 name variants (phase-2 AMENDMENTS.md A3), as in phase 3 parts B and C.
A3_VARIANTS = {
    "Z2_JORDAN_VALLEY": ["hagedud", "הגדוד"],
    "Z4_JERUSALEM_HILLS": ["anathoth", "land of benjamin", "ארץ בנימין", "kh el burj", "khirbet el burj", "ח אל בורג"],
}
HE_PREFIX = "בהולמכש"  # phase-1 screen S2: one or two prefix letters before a Hebrew name

PAGES = re.compile(r"\(([^()]*\bpp?\.\s*[^()]*)\)\s*$", re.I)
FIRSTPAGE = re.compile(r"\bpp?\.\s*(\d+\*?)(?:\s*[–-]\s*(\d+\*?))?", re.I)


def split_title(title):
    """Return (title without the trailing page parenthesis, page note, first page, last page, language)."""
    m = PAGES.search(title)
    if not m:
        return title.strip(), "", "", "", ""
    note = m.group(1)
    fp = FIRSTPAGE.search(note)
    lang = "Hebrew" if re.match(r"\s*Hebrew", note, re.I) else ""
    return title[:m.start()].strip(), note, fp.group(1) if fp else "", (fp.group(2) or "") if fp else "", lang


def page_count(first, last):
    if not first:
        return None
    a, b = first.rstrip("*"), (last or first).rstrip("*")
    try:
        n = int(b) - int(a) + 1
    except ValueError:
        return None
    return n if n > 0 else None


def slug(title, words=6):
    s = unicodedata.normalize("NFKD", title)
    s = "".join(c for c in s if not unicodedata.combining(c)).lower()
    s = re.sub(r"[ʿʾ‘’'`´׳ʽʻ]", "", s)
    s = re.sub(r"[^a-z0-9]+", " ", s).split()
    stop = {"a", "an", "the", "of", "at", "in", "on", "and", "from", "to", "for", "with"}
    s = [w for w in s if w not in stop] or s
    return "-".join(s[:words]) or "untitled"


def unit_id(volume, first_page, item_no, title):
    """ATQ<vol>-<first page>-<slug>; first page zero-padded to 3 digits, a starred page gets suffix 's'.
    Without a known first page the landing item number is used: ATQ<vol>-i<item>-<slug>."""
    if first_page:
        n = first_page.rstrip("*")
        pg = "%03d" % int(n) + ("s" if first_page.endswith("*") else "")
    else:
        pg = "i%02d" % int(item_no)
    return "ATQ%s-%s-%s" % (volume, pg, slug(title))


def sha_order(uid):
    return hashlib.sha256(uid.encode("utf-8")).hexdigest()


def prenorm(s):
    return s.replace("־", " ").replace("״", " ").replace("׳", "")


def patterns(params=None):
    params = params or common.plan_params()
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


def fmt_hits(h):
    return ";".join("%s:%s" % (z, t) for z in sorted(h) for t in h[z])
