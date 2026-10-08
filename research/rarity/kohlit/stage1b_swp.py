"""Koḥlit rarity count, Stage 1b: the SWP Memoirs screen for pool words.

Source 3 of the pre-registration. The Memoirs locate a place only to a lettered map
square (about 7.3 × 8.8 km), so a Memoir entry is linked to a WBADB unit by NAME,
within a distance that allows for the square's size and the calibration error. The unit's
WBADB Other_Names are used as well, so the frozen WBADB file is an input again.
A unit's Stage 1 status becomes "to Stage 2" if Stage 1a or 1b finds a pool word,
otherwise "not recorded" (C1 UNKNOWN). Rules are fixed in this file and words.json.

Usage:
    python3 -I stage1b_swp.py SWP_II.txt SWP_III.txt stage1a/stage1a_units.csv WBADB_data1.xlsx OUT_DIR

Inputs are archive.org's OCR text of Conder & Kitchener, Memoirs II and III
(surveyofwesternp02conduoft, surveyofwesternp03conduoft); hashes are checked.
"""
from __future__ import annotations

import csv
import difflib
import hashlib
import json
import math
import re
import sys
import unicodedata
from pathlib import Path

from pyproj import Transformer

HERE = Path(__file__).resolve().parent
W = json.loads((HERE / "words.json").read_text(encoding="utf-8"))

SWP_FILES = {
    "II": ("https://archive.org/download/surveyofwesternp02conduoft/surveyofwesternp02conduoft_djvu.txt",
           "e09da5efc8485d2904bafb8bf9a58ff65bdb1c4688fd6a41b43efd8a855da5b2"),
    "III": ("https://archive.org/download/surveyofwesternp03conduoft/surveyofwesternp03conduoft_djvu.txt",
            "102742aa163821beffab1bd4d8cb1f9b0da5755bce1bbee7b8f402c3534db6a4"),
}
# SWP square -> lat/lon, frozen from research/agent_review_2026-10-07/wave1/T01_place_names/data/grid_calibration.json
CAL_LON = (34.274747261904764, 0.07710166666666633)
CAL_LAT = (33.355886289808915, -0.07969863057324816)
MAX_DIST_M = 9_000      # square half-diagonal (~5.7 km) + calibration residual (~3 km)
MIN_SIMILARITY = 0.85   # difflib ratio between consonant skeletons of 3 or more letters
SHORT_SKELETON = 2      # a 2-letter skeleton must match exactly; shorter names are not matched

# Feature-type words: dropped, because one source may write "Kh. X" where the other writes "X".
TYPE_WORDS = {
    "kh", "kh.", "khirbet", "khirbat", "khurbet", "khurbat", "khirbe", "khurbeh", "khirbeh", "tell", "tel",
    "tall", "tulul", "ain", "ein", "ayn", "aiyun", "wadi", "wady", "nahal", "bir", "biar", "birket", "birkat",
    "birkeh", "mughr", "mugharet", "mughara", "khallet", "rujm", "iraq", "qasr", "kasr", "kusr",
}
# Words that are often part of a proper name (Beit Ur, Deir Dibwan). A name is keyed both with
# and without them, and either key may match.
NAME_PART_WORDS = {
    "deir", "dayr", "jebel", "jabal", "ras", "beit", "bet", "beth", "kefr", "kafr", "neby", "nabi",
    "sheikh", "sh.", "umm", "abu",
}
# OCR forms of Khurbet/Khirbet not listed above (khiirbet, khurhet, and Kh glued to the name)
KHIRBET_RE = re.compile(r"^k[hl]?[il]{0,2}[iuün]{1,2}r[bh][ae][tl]h?")
ARTICLES = {"el", "al", "ed", "es", "en", "er", "esh", "et", "ez", "ej", "eth", "ash", "ad", "an", "ar", "as",
            "at", "az", "edh", "ul", "il", "ibn", "ben", "bint", "of", "the", "and", "or"}
GLUED_ARTICLE = re.compile(r"(?<![A-Za-z])(El|Es|Esh|Et|Ed|Er|En|Ez|Ej|Eth|el|es|esh|et|ed|er|en|ez|ej|eth)(?=[A-Z'])")


def sha256(path):
    h = hashlib.sha256()
    h.update(Path(path).read_bytes())
    return h.hexdigest()


def strip_marks(s):
    s = unicodedata.normalize("NFKD", s)
    return "".join(ch for ch in s if not unicodedata.combining(ch))


def collapse_spaced(raw):
    """Repair OCR of letter-spaced type, using the raw spacing.

    'K  h  u  r  b  e  t        R  a  s  e  i  s  e  h' -> 'Khurbet Raseiseh'. Gaps of three or
    more spaces separate words; inside a word, a run of three or more tokens of one or two
    characters is joined; a lone capital joins the lower-case token after it ('J  elameh').
    """
    words = []
    for chunk in re.split(r"\s{3,}", raw.strip()):
        toks = chunk.replace("\u2018", "'").split()
        i, out = 0, []
        while i < len(toks):
            j = i
            while j < len(toks) and len(toks[j].strip("'")) <= 2:
                j += 1
            if j - i >= 3:
                out.append("".join(toks[i:j]))
                i = j
            else:
                out.append(toks[i])
                i += 1
        k, merged = 0, []
        while k < len(out):
            if (len(out[k]) == 1 and out[k].isupper() and k + 1 < len(out) and out[k + 1][:1].islower()):
                merged.append(out[k] + out[k + 1])
                k += 2
            else:
                merged.append(out[k])
                k += 1
        words.extend(merged)
    return " ".join(words)


def tokens(name):
    s = GLUED_ARTICLE.sub(r"\1 ", strip_marks(name))       # 'ElHammam' -> 'El Hammam'
    s = s.lower()
    s = re.sub(r"[ʿʾ'`‘’\"]", "", s)
    s = re.sub(r"[-_/,;:()\[\]]", " ", s)
    s = re.sub(r"\.(?=\S)", ". ", s)
    return [t for t in s.split() if t]


def distinctive(name, keep_name_parts=True):
    out = []
    for t in tokens(name):
        if t in ARTICLES or t in TYPE_WORDS or t.rstrip(".") in TYPE_WORDS:
            continue
        if not keep_name_parts and (t in NAME_PART_WORDS or t.rstrip(".") in NAME_PART_WORDS):
            continue
        m = KHIRBET_RE.match(t)
        if m and m.end() == len(t):
            continue
        if m and len(t) - m.end() >= 3:   # 'khurbetraseiseh' -> 'raseiseh'
            t = t[m.end():]
        out.append(t)
    return out


def skeleton(words):
    s = "".join(words)
    s = s.replace("kh", "h").replace("gh", "g").replace("sh", "s").replace("th", "t").replace("dh", "d")
    s = s.replace("ph", "f").replace("q", "k").replace("c", "k")
    s = re.sub(r"[^a-z0-9]", "", s)
    s = re.sub(r"(?<=[aeiou])h$", "", s)    # final -eh, -ah
    s = re.sub(r"(.)\1+", r"\1", s)        # doubled letters, before the vowels go (Yanun keeps y-n-n)
    s = re.sub(r"[aeiou]", "", s)           # y is kept as a consonant (Yanun, Yazur)
    return s


def name_keys(name):
    """Skeleton keys for a name and for each alternative inside it ('X, or Y', 'X (Y)')."""
    keys = set()
    for alt in [name] + re.split(r",?\s+or\s+|[()]", name):
        for keep in (True, False):
            k = skeleton(distinctive(alt, keep))
            if len(k) >= SHORT_SKELETON:
                keys.add(k)
    return keys


def name_match(keys_a, keys_b):
    """Best similarity between two key sets; 2-letter keys count only when equal."""
    best = 0.0
    for a in keys_a:
        for b in keys_b:
            if min(len(a), len(b)) <= SHORT_SKELETON:
                r = 1.0 if a == b else 0.0
            else:
                r = difflib.SequenceMatcher(None, a, b).ratio()
            best = max(best, r)
    return best


def square_latlon(sq):
    c, r = ord(sq[0]) - ord("A"), ord(sq[1]) - ord("a")
    return CAL_LAT[0] + CAL_LAT[1] * (r + 0.5), CAL_LON[0] + CAL_LON[1] * (c + 0.5)


# A Memoir entry opens a line: optional list number ('14.', '(16.)'), the name (which may hold
# a short note in brackets, '(or Abu Ghosh)', '(Northern)'), the map square '(L s)', then a dash. A square line with the name on the line
# before is joined to it in parse().
HEADER = re.compile(r"^\s*(?:\(?\d{1,3}[.,]*\)?[.,]?\s+)?([A-Z'‘ʿ](?:[^\n().—]|\([A-Za-z' ,]{1,40}\)){1,90}?)"
                    r"\(\s*([A-Z])\s*([a-z])\s*\)\s*\.?\s*[—–-]")
SQUARE_ONLY = re.compile(r"^\s*\(\s*[A-Z]\s*[a-z]\s*\)\s*\.?\s*[—–-]")
PAGE_EVEN = re.compile(r"^\s*(\d{1,3})\s+THE\s+SURVEY\s+OF\s+WESTERN", re.M)
PAGE_ODD = re.compile(r"^\s*[A-Z][A-Z .,'-]{3,40}\.\s+(\d{1,3})\s*$", re.M)
POOL_RE = re.compile(r"(?<![a-z])(" + "|".join(sorted((re.escape(w) for w in W["pool_words"]), key=len, reverse=True))
                     + r")(?:e?s)?(?![a-z])", re.IGNORECASE)


def parse(vol, text):
    """Return Memoir entries: dict(vol, page, name, square, text). Line-based: a new entry starts
    at every line that opens with a header, so entries not separated by a blank line are split."""
    page_marks = sorted([(m.start(), int(m.group(1))) for m in PAGE_EVEN.finditer(text)]
                        + [(m.start(), int(m.group(1))) for m in PAGE_ODD.finditer(text)])
    entries, cur, off, prev = [], None, 0, ""
    for line in text.split("\n"):
        start = off
        off += len(line) + 1
        probe = line
        if SQUARE_ONLY.match(line) and prev.strip() and len(prev.strip()) < 60 and not prev.rstrip().endswith((".", ",", ";")):
            probe = prev.strip() + "  " + line.strip()
            if cur and cur["text"].endswith(prev):
                cur["text"] = cur["text"][: -len(prev)].rstrip("\n")
        m = HEADER.match(probe)
        if m:
            if cur:
                entries.append(cur)
            page = None
            for o, n in page_marks:
                if o <= start:
                    page = n
                else:
                    break
            name = re.sub(r"\s+", " ", collapse_spaced(m.group(1))).strip(" .,")
            cur = dict(vol=vol, page=page, name=name, square=m.group(2) + m.group(3), text=probe)
        elif cur and len(cur["text"]) < 4000:
            cur["text"] += "\n" + line
        if line.strip():
            prev = line
    if cur:
        entries.append(cur)
    return entries


def wbadb_other_names(xlsx):
    """unit_id -> 'Other_Names' text from the frozen WBADB file (same hash as Stage 1a)."""
    import pandas as pd
    from stage1_screen import WBADB_SHA256
    if sha256(xlsx) != WBADB_SHA256:
        sys.exit("WBADB file hash does not match the frozen value")
    book = pd.ExcelFile(xlsx)
    out = {}
    for sheet, tag in (("Surveyed", "S"), ("Excavations", "E")):
        df = book.parse(sheet)
        for _, r in df.iterrows():
            v = r.get("Other_Names")
            if isinstance(v, str) and v.strip() not in ("", "-", "NDA"):
                out[f"{tag}{r['Index']}"] = v
    return out


def main(f2, f3, units_csv, xlsx, out_dir):
    for (vol, (url, digest)), path in zip(SWP_FILES.items(), (f2, f3)):
        if sha256(path) != digest:
            sys.exit(f"SWP {vol} text hash does not match the frozen value")
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    entries = parse("II", Path(f2).read_text(encoding="utf-8", errors="replace")) + \
        parse("III", Path(f3).read_text(encoding="utf-8", errors="replace"))
    to_grid = Transformer.from_crs("EPSG:4326", "EPSG:28193", always_xy=True)
    for e in entries:
        lat, lon = square_latlon(e["square"])
        gx, gy = to_grid.transform(lon, lat)
        e["gx"], e["gy"] = gx, gy - 1_000_000
        e["keys"] = name_keys(e["name"])
        e["pool_words"] = sorted({w.lower() for w in POOL_RE.findall(e["text"])})

    with open(units_csv, newline="", encoding="utf-8") as f:
        units = list(csv.DictReader(f))
    other = wbadb_other_names(xlsx)

    rows, index = [], []
    for u in units:
        ukeys = name_keys(u["name"])
        for alt in re.split(r"[;,]", other.get(u["unit_id"], "")):
            ukeys |= name_keys(alt)
        matches = []
        if ukeys:
            ux, uy = float(u["x"]), float(u["y"])
            for e in entries:
                d = math.hypot(e["gx"] - ux, e["gy"] - uy)
                if d > MAX_DIST_M or not e["keys"]:
                    continue
                sim = name_match(ukeys, e["keys"])
                if sim >= MIN_SIMILARITY:
                    matches.append((round(sim, 2), round(d), e))
        matches.sort(key=lambda m: (-m[0], m[1]))
        pool = sorted({w for _, _, e in matches for w in e["pool_words"]})
        status_1a = u["stage1a"]
        status = "to Stage 2" if (status_1a == "to Stage 2" or pool) else "not recorded (C1 UNKNOWN)"
        rows.append({
            "unit_id": u["unit_id"], "name": u["name"], "other_names": other.get(u["unit_id"], ""),
            "main_set": u["main_set"], "in_R2": u["in_R2"], "name_keys": "/".join(sorted(ukeys)),
            "stage1a": status_1a,
            "swp_matches": " | ".join(f"Mem {e['vol']} p.{e['page']} {e['name']} ({e['square']}) sim {s} ~{d} m"
                                      for s, d, e in matches[:6]),
            "swp_pool_words": "/".join(pool),
            "stage1": status,
        })
        for s, d, e in matches:
            index.append({"unit_id": u["unit_id"], "unit_name": u["name"], "vol": e["vol"], "page": e["page"],
                          "swp_name": e["name"], "square": e["square"], "similarity": s, "approx_dist_m": d,
                          "pool_words": "/".join(e["pool_words"]), "text": e["text"][:1500]})

    with open(out_dir / "stage1b_units.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    with open(out_dir / "swp_entry_index.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(index[0].keys()) if index else ["unit_id"])
        w.writeheader()
        w.writerows(index)

    def count(sel):
        sub = [r for r in rows if sel(r)]
        return {"units": len(sub),
                "to_stage2": sum(r["stage1"] == "to Stage 2" for r in sub),
                "added_by_swp": sum(r["stage1"] == "to Stage 2" and r["stage1a"] != "to Stage 2" for r in sub),
                "not_recorded": sum(r["stage1"] != "to Stage 2" for r in sub),
                "with_any_swp_match": sum(bool(r["swp_matches"]) for r in sub)}

    summary = {
        "swp_entries_parsed": len(entries),
        "swp_entries_with_pool_word": sum(bool(e["pool_words"]) for e in entries),
        "swp_entries_per_volume": {v: sum(e["vol"] == v for e in entries) for v in SWP_FILES},
        "rules": {"max_dist_m": MAX_DIST_M, "min_similarity": MIN_SIMILARITY, "short_skeleton": SHORT_SKELETON},
        "units_without_name_key": sum(not r["name_keys"] for r in rows),
        "R1_main": count(lambda r: r["main_set"] == "True"),
        "R1_pre70": count(lambda r: True),
        "R2_main": count(lambda r: r["main_set"] == "True" and r["in_R2"] == "True"),
        "R2_pre70": count(lambda r: r["in_R2"] == "True"),
    }
    (out_dir / "stage1b_summary.json").write_text(json.dumps(summary, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    sys.path.insert(0, str(HERE))
    main(*sys.argv[1:6])
