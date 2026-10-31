#!/usr/bin/env python3
"""Lane I2: parse the fiscal-unit gazetteer of Huetteroth & Abdulfattah 1977 (ch. VI, 'Summarized statistics of
fiscal units') from the PDF text layer. Regular table; no free text is read here.
Usage: python3 -I parse_hutteroth.py TEXT_JSONL_DIR OUT_CSV
Selected PDF pages (book page = PDF page - 8): liwa' Quds 120-132, liwa' Nablus 133-149, liwa' 'Ajlun 170-182.
Not selected: Gazza 150-164, Lajjun 165-169, Safad 183-202, Hawran 203-228 (outside the five project regions).
Per entry, fields as coded by the authors (p. 229): 1) unit number (P/M/Z/MZ), 2) unit type (Q village, N town,
J tribe, other types written out), 3) name (DMG transliteration), 4) name in Arabic letters, 5) Palestine grid E/N (km).
Only facts are written: unit id, type code, name (field 3), grid E/N, PDF page, book page, liwa'. No running text.
Grid parsing (fixed rule): '5)' or '5(' followed by optional 'L', then E/N (if that marker is garbled: the first
NNN/NNN pair before field 6); E and N must be 3-digit, 90<=E<=290,
40<=N<=300; a 4-digit E with a leading OCR noise digit ('4' or '1' from the bracket) keeps its last 3 digits.
Otherwise grid = '' (unplaced). The 'L' (Levant grid) flag is recorded; Levant-grid entries are left unplaced.
"""
import sys, os, json, glob, re, csv
D, OUT = sys.argv[1:3]
P = {}
for f in sorted(glob.glob(os.path.join(D, "Erlanger*__text_p*.jsonl"))):
    for l in open(f, encoding="utf-8"):
        d = json.loads(l)
        P[d["page"]] = d["text"]
LIWA = [("Quds", 120, 132), ("Nablus", 133, 149), ("Ajlun", 170, 182)]
# entry start: field-2 type code preceded by a field-1 token; we split on ' 2)' / ' 2(' markers
E2 = re.compile(r"(?:^|\s)(\S{1,9})\s+2[\)\(]\s*(\S{1,6})\s+3[\)\(]?\s*")
rows = []
for liwa, a, b in LIWA:
    nahiya = ""
    for p in range(a, b + 1):
        t = " ".join(P[p].split())
        ms = list(E2.finditer(t))
        for k, m in enumerate(ms):
            # nahiya heading between previous entry and this one
            pre = t[(ms[k - 1].end() if k else 0):m.start()]
            mh = re.search(r"N.{0,2}h.{0,2}ya[ _]+([^\s:]+(?:[ _](?!P[aä]di|Mir|Za)[^\s:]+)?)", pre)
            if mh:
                nahiya = mh.group(1).replace("_", " ")
            end = ms[k + 1].start() if k + 1 < len(ms) else len(t)
            body = t[m.end():end]
            name = re.split(r"\s(?:[4A][\)\(]|\d[\)\(])|[؀-ۿ]", " " + body, maxsplit=1)[0].strip()
            g = re.search(r"5[\)\(]\s*(L?)\s*(\d{3,4})\s*/\s*(\d{3})\b", body)
            if not g:  # field-5 marker garbled by OCR: first E/N pair before field 6 ('Pal.100'/'6)')
                head = re.split(r"6[\)\(]|Pal|P\.E\.F|G\.T|Jor|Lev|8[\)\(]", body, maxsplit=1)[0]
                g = re.search(r"()(?<![\d/])(\d{3,4})\s*/\s*(\d{3})\b", head)
            E = N = ""; lev = ""
            if g:
                lev = g.group(1); e = g.group(2); n = int(g.group(3))
                if len(e) == 4 and e[0] in "41":
                    e = e[1:]
                e = int(e)
                if len(str(e)) == 3 and 90 <= e <= 290 and 40 <= n <= 300 and not lev:
                    E, N = e, n
            unit = m.group(1)
            typ = m.group(2).strip("_")
            mz = "mazra" in body.lower()[:60]
            rows.append(dict(liwa=liwa, nahiya=nahiya, pdf_page=p, book_page=p - 8, unit_raw=unit, type_raw=typ,
                             name=name, grid_e=E, grid_n=N, levant=lev, mazraa_word=mz))
with open(OUT, "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
import collections
print(len(rows), "entries;", sum(1 for r in rows if r["grid_e"] != ""), "with grid")
print(collections.Counter((r["liwa"], r["nahiya"]) for r in rows))
print(collections.Counter(r["type_raw"] for r in rows).most_common(12))
