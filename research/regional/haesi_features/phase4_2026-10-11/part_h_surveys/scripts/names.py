#!/usr/bin/env python3
"""Name cleaning for OCR'd SWP and Guérin headings, gazetteer matching with the frozen phase-2 gazetteer,
and the SWP spelling variants recorded in data/name_variants.csv (exploratory, see NOTES.md)."""
import csv
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PART = HERE.parent
PHASE2 = PART.parents[1] / "phase2_2026-10-10"
sys.path.insert(0, str(PHASE2 / "scripts"))
import common  # noqa: E402

VARIANTS = PART / "data" / "name_variants.csv"
HEADWORDS = ["Khurbet", "'Ain", "Ain", "Tell", "Beit", "Deir", "Wady", "Bir", "Birket", "Jebel", "Kusr", "Mugharet",
             "Neby", "Rujm", "Umm", "Ras", "Kubbet", "Kabr", "Tellul", "Tuleil", "Merj", "Abu", "Khan", "Sheikh", "Jisr", "Tahunet", "Burj"]
ARTICLES = {"el", "es", "ed", "er", "en", "et", "ez", "esh", "edh", "eth", "ej", "ec", "em"}
OCR_FIX = [(r"\bK\s*h\s*[iü!:\^1lI\]\[]*[^\w\s]*\s*[uiaüfAt]*\s*r\s*b\s*[ec]\s*t\b", "Khurbet"),
           (r"\bKh[iüuaf\^\']+r[bh]\s*[ec]\s*t\b", "Khurbet"), (r"\bKbnrbet\b", "Khurbet"),
           (r"\bKhiirb\.et\b", "Khurbet"), (r"\bKhfirbet\b", "Khurbet"), (r"\bKhtirbet\b", "Khurbet"),
           (r"\bKh[^\s]{1,4}rbet\b", "Khurbet"), (r"\bKhurbct\b", "Khurbet"), (r"\bKhrirbet\b", "Khurbet")]


def collapse_spaced(s):
    """'K h u r b e t  el  K u m r a n' -> 'Khurbet el Kumran' (OCR letter-spacing)."""
    toks = s.split()
    out, run = [], []

    def flush():
        if run:
            out.append("".join(run))
            run.clear()
    for t in toks:
        if t == "1" and run:
            t = "l"  # OCR digit one for letter l inside a spaced name
        if len(t) == 2 and t[0] in "'‘’`" and t[1].isalpha():
            flush()
            run.extend([t[0], t[1]])
            continue
        if run == ["'", "A"] and t.isalpha() and t.islower():
            run.append(t)
            continue
        if len(t) == 1 and (t.isalpha() or t in "'‘’`"):
            if run and t.isupper() and not (len(run) == 1 and run[0] in "'‘’`"):
                flush()
            run.append(t)
        else:
            flush()
            out.append(t)
    flush()
    # split glued articles: 'edDuk' already split by uppercase; 'Khurbetes' -> 'Khurbet es'
    res = []
    for w in out:
        m = re.match(r"^(%s)(%s)$" % ("|".join(HEADWORDS), "|".join(sorted(ARTICLES, key=len, reverse=True))), w)
        if m:
            res.extend([m.group(1), m.group(2)])
        else:
            res.append(w)
    return " ".join(res)


def clean_name(raw):
    s = re.sub(r"\s+", " ", raw).strip(" .,;:—-")
    s = re.sub(r"^K\s*h\s*\S{0,3}\s*r\s*b\s*[ec]\s*t\b", "Khurbet", s)
    s = re.sub(r"^K\s*h\s*\S{0,3}\s*r\s*b\s*[ec]\s*t(?=\s|[A-Z])", "Khurbet ", s)
    s = re.sub(r"I\\I|\]\\I|!\\I|INI|IVI|\^I|\bIM(?=\s*[a-z])", "M", s)
    s = re.sub(r"\bK\s*(?:ii|li|fi|ti|i\^i|ti|u|i)\s*s\s*r\b", "Kusr", s)
    s = re.sub(r"\b(?:Mii|Mti|ISIii|Mi\^i)gharet\b", "Mugharet", s)
    s = collapse_spaced(s)
    for pat, rep in OCR_FIX:
        s = re.sub(pat, rep, s)
    s = re.sub(r"\s+", " ", s).strip(" .,;:")
    return s


def slug(s, n=40):
    s = common.norm(s).strip()
    s = re.sub(r"[^a-z0-9 ]", "", s)
    return re.sub(r"\s+", "-", s)[:n].strip("-")


def load_variants(path=VARIANTS):
    if not Path(path).exists():
        return []
    with open(path, newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f)]


def gaz_hits(name, pats=None, variants=None):
    """Zones whose gazetteer term matches the name (plan section 4 normalisation), after
    replacing 'Khurbet' by 'kh' and applying the recorded SWP spelling variants."""
    pats = pats or common.gazetteer_patterns()
    variants = load_variants() if variants is None else variants
    n = common.norm(name)
    n = re.sub(r" (khurbet|khirbet|khirbat|khurbat) ", " kh ", n)
    alts = [n]
    for v in variants:
        f = " " + common.norm(v["source_form"]).strip() + " "
        if f in n:
            alts.append(n.replace(f, " " + common.norm(v["gazetteer_term"]).strip() + " "))
    hits = {}
    for a in alts:
        for z, h in common.title_hits(a, pats).items():
            hits.setdefault(z, set()).update(h)
    return {z: sorted(h) for z, h in hits.items()}
