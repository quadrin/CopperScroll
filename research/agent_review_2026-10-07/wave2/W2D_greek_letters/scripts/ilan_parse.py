#!/usr/bin/env python3
"""Parse Ilan, Lexicon of Jewish Names I (OCR text, pdftotext -layout) into
(1) the English name index (name, category tag, page range) and
(2) bearer counts per headword from the lexicon body (max entry number per section).
usage: ilan_parse.py ilan1.txt OUTDIR
Writes ilan_index.csv and ilan_counts.csv and prints validation against Ilan's Tables 5,7,8.
"""
import re, sys, csv, collections

txt_path, outdir = sys.argv[1], sys.argv[2]
text = open(txt_path, encoding="utf-8", errors="replace").read()
pages = text.split("\f")


def collapse(s):
    s = s.strip()
    # 'D u s h a i' -> 'Dushai' ; 'Van i ah' -> 'Vaniah'
    if re.fullmatch(r"(?:[A-Za-z'’]\s+)+[A-Za-z'’]+", s) or re.fullmatch(r"[A-Za-z]+(?:\s[a-z]{1,3})+", s):
        s = s.replace(" ", "")
    return s

# ---------------- (1) English index ----------------
idx_start = text.find("Index of the Names in English")
idx_end = text.find("Texts and Studies in Ancient Judaism", idx_start)
idx = text[idx_start:idx_end]
# split two columns: split each line at a gap of >=3 spaces after col 30
entries = []
pat = re.compile(r"^\s*([A-Z][A-Za-z'’ \-]*?)\s*(?:-\s*(.*?))?\s*\(\s*([A-Z](?:\s*[-/]\s*[A-Z])?)\s*[/]?\s*([MF])\s*\)\s*([0-9 ,\-–_]*(?:,?\s*addendum)?)\s*$")
for line in idx.split("\n"):
    if "Index of the Names" in line:
        continue
    parts = re.split(r"\s{3,}(?=[A-Z])", line.strip())
    for p in parts:
        m = pat.match(p)
        if m:
            name = collapse(m.group(1))
            tag = re.sub(r"\s", "", m.group(3)).replace("/", "-") + "/" + m.group(4)
            pg = re.sub(r"\s", "", m.group(5))
            entries.append((name, tag, pg))
# lines broken over two lines (e.g. 'Aristobulus - ... (G/' + 'M) 266-7') are handled loosely below
seen = {}
for n, t, p in entries:
    seen.setdefault(n, (t, p))
with open(outdir + "/ilan_index.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["name", "tag", "pages"])
    for n, (t, p) in sorted(seen.items()):
        w.writerow([n, t, p])
print("index names parsed:", len(seen))
names = set(seen) | {"Onias", "Ezekiah", "Mara", "Berenice"}
for extra, tg in [("Onias", "B/M"), ("Ezekiah", "B/M"), ("Mara", "S-H/F"), ("Berenice", "G/F")]:
    seen.setdefault(extra, (tg, ""))

# ---------------- (2) body bearer counts ----------------
ENTRY = re.compile(r"^\s*([0-9Il]{1,3})\s*\.\s*[O0Q]\s*[:;]")
HEAD = re.compile(r"-\s*([A-Z][A-Za-z'’]+(?:\s?[A-Za-z'’]+){0,3})\s*$")


def split_cols(page):
    lines = page.split("\n")
    # estimate boundary: positions where a segment starts after >=3 spaces, in 38..75
    hist = collections.Counter()
    for l in lines:
        for m in re.finditer(r"\s{3,}(\S)", l):
            pos = m.start(1)
            if 38 <= pos <= 75:
                hist[pos // 2 * 2] += 1
    if not hist:
        return lines, []
    B = hist.most_common(1)[0][0]
    left, right = [], []
    for l in lines:
        if not l.strip():
            continue
        first = len(l) - len(l.lstrip())
        if first >= B - 6:
            right.append(l.strip()); continue
        # find a gap of >=2 spaces whose end is within B-8..B+10
        cut = None
        for m in re.finditer(r"\s{2,}", l):
            if B - 10 <= m.end() <= B + 12:
                cut = m; break
        if cut:
            left.append(l[:cut.start()].strip()); right.append(l[cut.end():].strip())
        else:
            left.append(l.strip())
    return left, right


counts = collections.Counter()
sections = collections.Counter()
section_log = []
body_pages = range(80, 485)  # pdf pages of lexicon body (approx; index excluded)
cur = None; curmax = 0
def close():
    global cur, curmax
    if cur is not None:
        counts[cur] += curmax; sections[cur] += 1
        section_log.append((cur, curmax))
    cur = None; curmax = 0

for pi in body_pages:
    if pi - 1 >= len(pages):
        break
    pg = pages[pi - 1]
    if "Index of the Names in English" in pg or "Orthographical" in pg:
        break
    L, R = split_cols(pg)
    stream = L[2:] + R if len(L) > 2 else L + R  # drop running head lines (first 2 of left col)
    for line in stream:
        mh = HEAD.search(line)
        if mh:
            cand = collapse(mh.group(1))
            if cand in names and len(line) < 70:
                if cand != cur:
                    close(); cur = cand
                continue
        me = ENTRY.match(line)
        if me and cur is not None:
            s = me.group(1).replace("I", "1").replace("l", "1")
            try:
                n = int(s)
            except ValueError:
                continue
            if n <= curmax + 40 and n < 300:
                curmax = max(curmax, n)
close()
with open(outdir + "/ilan_counts.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["name", "tag", "pages", "bearers_parsed", "sections"])
    for n in sorted(names):
        t, p = seen[n]
        w.writerow([n, t, p, counts.get(n, 0), sections.get(n, 0)])
tot = sum(counts.values())
print("names with >=1 parsed bearer:", sum(1 for n in names if counts.get(n, 0) > 0), "total parsed bearers:", tot)
ref = {"Simon": 257, "Joseph": 231, "Judah": 179, "Eleazar": 177, "Yohanan": 128, "Joshua": 103, "Hananiah": 85,
       "Jonathan": 75, "Mattathias": 63, "Menahem": 46, "Jacob": 45, "Hanan": 39, "Alexander": 31, "Dositheus": 31,
       "Zachariah": 31, "Ishmael": 31, "Levi": 29, "Saul": 29, "Onias": 27, "Samuel": 26, "Ezekiah": 26,
       "Mariam": 80, "Salome": 63, "Shelamzion": 25, "Martha": 20, "Joanna": 12, "Shiphra": 12, "Berenice": 10,
       "Sarah": 9, "Imma": 7, "Mara": 7}
for k, v in ref.items():
    print(f"  {k:12s} table={v:4d} parsed={counts.get(k, 0):4d} in_index={k in names}")
