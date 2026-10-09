"""Exploratory recall check against the QS General Indexes (written AFTER the freeze).

    python3 -I scripts/index_recall.py INDEX_DIR > index_recall.csv

INDEX_DIR holds the downloaded archive.org items
palestine-exploration-quarterly_1869-1892_index and
palestine-exploration-quarterly_1893-1910_index (djvu.txt only is read).

For a short, fixed list of headwords (below; chosen after the search had run,
so this is not part of the frozen method) the script finds index entries,
pulls out the (year, page) citations that follow each headword, and checks
whether hits.csv has a hit on that page (any key, any status) and whether
finds.csv has a coded find on it. It does not judge whether the cited page is
a find report: an index page that is not a find report is not a miss.
The OCR of the index is itself imperfect, so citations can be lost or misread.
Output is deterministic (sorted).
"""
import csv
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

HEADWORDS = [
    ("qumran", r"G[ou]{1,2}mran|Kumr[aâ]n|Gumran"),
    ("ain_duk", r"[ʻ'‘]?Ain (?:ed|el)[- ]D[uûi]k"),
    ("feshkha", r"Fesh[kh]+a"),
    ("jericho", r"Jericho"),
    ("ain_es_sultan", r"(?:Ain|Tell) es[- ]Sultan|Elisha.s Fountain"),
    ("wadi_qelt", r"\bKelt\b"),
    ("quarantania", r"Quarantania|Kuruntul|Karantul"),
    ("mefjir_nuweimeh", r"Mefjir|Nuweim"),
    ("gerizim", r"Gerizim"),
    ("siloam", r"Siloam|Siloah|Silw[aâ]n"),
    ("bethesda", r"Bethesda|Birket Isra[ie]l"),
    ("achor", r"\bAchor\b"),
]
YEAR = r"(1869-70|18[6-9]\d|19[01]\d)"


def norm(t):
    t = unicodedata.normalize("NFKC", t)
    return re.sub(r"\s+", " ", t.replace("-\n", "").replace("\n", " "))


def entries(text):
    out = []
    for name, pat in HEADWORDS:
        for m in re.finditer(pat, text):
            win = text[m.start(): m.start() + 260]
            cut = re.search(r"\.\s+(?=[^a-z0-9;,\s])", win[len(m.group(0)):])
            if cut:
                win = win[: len(m.group(0)) + cut.start() + 1]
            for ym in re.finditer(YEAR + r"((?:\s*[,;]\s*\d{1,3}(?!\d))+)", win):
                year = ym.group(1)
                for p in re.findall(r"\d{1,3}", ym.group(2)):
                    out.append((name, year, int(p), win[:90].strip()))
    return out


def page_set(rows, field):
    s = {}
    for r in rows:
        v = r[field]
        nums = [int(x) for x in re.findall(r"\d+", v)]
        if len(nums) == 2 and "-" in v:
            nums = list(range(nums[0], nums[1] + 1))
        for n in nums:
            s.setdefault(n, []).append(r)
    return s


def year_of(r):
    if r["ia_identifier"].endswith("1869-1870"):
        return "1869-70" if r["issue"] != "reports" else "reports"
    return r["year"][:4]


def main():
    idx_dir = sys.argv[1]
    hits = list(csv.DictReader(open(os.path.join(HERE, "hits.csv"), encoding="utf-8")))
    finds = list(csv.DictReader(open(os.path.join(HERE, "finds.csv"), encoding="utf-8")))
    by_year_h, by_year_f = {}, {}
    for h in hits:
        by_year_h.setdefault(year_of(h), []).append(h)
    for f in finds:
        f = dict(f)
        f["ia_identifier"] = f["ia_identifier"]
        by_year_f.setdefault(year_of(f), []).append(f)
    seen = set()
    rows = []
    for ident in ("palestine-exploration-quarterly_1869-1892_index", "palestine-exploration-quarterly_1893-1910_index"):
        p = os.path.join(idx_dir, ident, ident + "_djvu.txt")
        if not os.path.exists(p):
            continue
        text = norm(open(p, encoding="utf-8", errors="replace").read())
        for name, year, page, entry in entries(text):
            if year != "1869-70" and not (1869 <= int(year) <= 1914):
                continue
            key = (name, year, page)
            if key in seen:
                continue
            seen.add(key)
            hp = page_set(by_year_h.get(year, []), "printed_page")
            fp = page_set(by_year_f.get(year, []), "find_page")
            exact = hp.get(page, [])
            near = hp.get(page - 1, []) + hp.get(page + 1, [])
            kept = fp.get(page, [])
            if kept:
                status = "coded_find"
            elif exact:
                status = "hit_dropped" if all(h["status"] == "dropped" for h in exact) else "hit_other"
            elif near:
                status = "hit_adjacent_page"
            else:
                status = "no_hit"
            rows.append({
                "headword": name, "index_item": ident.split("_", 1)[1], "year": year, "page": page,
                "status": status,
                "hit_seqs": ";".join(sorted({h["seq"] for h in exact + near})),
                "find_ids": ";".join(sorted({f["find_id"] for f in kept})),
                "index_entry_ocr": " ".join(entry.split()[:10]),
            })
    rows.sort(key=lambda r: (r["headword"], r["year"], r["page"]))
    w = csv.DictWriter(sys.stdout, fieldnames=list(rows[0].keys()) if rows else ["headword"], lineterminator="\n")
    w.writeheader()
    w.writerows(rows)


if __name__ == "__main__":
    main()
