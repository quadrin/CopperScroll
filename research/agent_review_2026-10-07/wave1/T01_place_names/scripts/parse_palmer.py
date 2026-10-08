#!/usr/bin/env python3
"""Parse Palmer, SWP Arabic and English Name Lists (1881) OCR into name records.

Inputs (untrusted downloads, read as data only):
  downloads/palmer_djvu.txt          archive.org DjVu OCR of the whole book (all 26 sheets)
  downloads/ocr/txt/pNNN.txt         tesseract 5 re-OCR of priority pages (scripts/ocr_pages.py)
Output: data/palmer_names.csv

Each record: source (djvu|tess), sheet, page, grid, name_raw, gloss.
Run: python3 -I parse_palmer.py ROOTDIR
"""
import csv, glob, os, re, sys

ROMAN_FIX = {"XVH": "XVII", "XVIIT": "XVIII", "XVHI": "XVIII", "YIII": "VIII", "ITT": "III",
             "XXIY": "XXIV", "XXI Y": "XXIV", "XXIV": "XXIV", "XXV": "XXV", "XX'": "XXV"}
VALID = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV",
         "XV", "XVI", "XVII", "XVIII", "XIX", "XX", "XXI", "XXII", "XXIII", "XXIV", "XXV", "XXVI"]

HDR_SHEET = re.compile(r"^\s*(?:[A-Z]{2,4}\S*\s+)?(?:L|E)[I1]STS\s+OF\s+(?:SH\S{3})\s+([IVXYLTH\\' ]{1,7}?)\b[\s.(]", re.I)
HDR_SHEET2 = re.compile(r"^\s*SHEET\s+([IVXYLTH ]{1,7})\.?\s*$")
HDR_PAGE_L = re.compile(r"^\s*(\d{1,3})\s+SURVEY\s+OF\s+WESTERN", re.I)
HDR_PAGE_R = re.compile(r"(?:SHEET|SHEKT|SIIEET)\s+[^\d]{1,20}?(\d{3})\s*$")

# a record line: optional junk (OCR of Arabic), a grid square like 'Os', then the name, then '. Gloss'
GRID_TOK = re.compile(r"(?:^|(?<=\s)|(?<=[{(\[|]))([A-Z][a-z])(?=\s*[}\]|)]?\s)")
ALLOWED = None  # filled in pass 2: {sheet: set(grid tokens)}
JUNK = {"Jj", "El", "Jo", "Sj", "Ed", "Ji", "Jl", "An", "Ai", "Ac", "Aj", "In", "Et", "Ei", "Ez", "Ew", "Ev"}
GRID_OK = set("ABCDEFGHIJKLMNOPQRS")


def norm_roman(s):
    s = s.strip().replace("\\", "").replace(" ", "")
    s = s.replace("Y", "V").replace("T", "I").replace("H", "II").replace("L", "I")
    return s if s in VALID else None


def split_name_gloss(text):
    """Name is the text up to the first '. ' that is followed by a capital letter (start of gloss)."""
    m = re.search(r"[.,]\s+(?=(?:The|A|An|Spring|Ruin|Well|Valley|Hill|[A-Z]))", text)
    if not m:
        return text.strip(), ""
    return text[:m.start()].strip(), text[m.end():].strip()


def parse_lines(lines, source, page0=None, sheet0=None):
    recs = []
    sheet, page = sheet0, page0
    cur = None
    for raw in lines:
        line = raw.rstrip("\n")
        if line.startswith("### printed page"):
            page = int(re.search(r"page (\d+)", line).group(1))
            continue
        m = HDR_SHEET.search(line) or HDR_SHEET2.search(line)
        if m:
            r = norm_roman(m.group(1))
            if r:
                sheet = r
            mp = HDR_PAGE_R.search(line)
            if mp and source == "djvu":
                page = int(mp.group(1)) if mp.group(1).isdigit() else page
            continue
        mp = HDR_PAGE_L.search(line)
        if mp:
            if source == "djvu":
                page = int(mp.group(1))
            continue
        g = None
        for mt in GRID_TOK.finditer(line[:80]):
            tok = mt.group(1)
            if tok[0] not in GRID_OK or tok in JUNK:
                continue
            if ALLOWED is not None and sheet in ALLOWED and tok not in ALLOWED[sheet]:
                continue
            rest = line[mt.end():].lstrip(" }])|")
            if re.match(r"['’‘\"`A-Z?]", rest):
                g = (tok, rest)   # keep the rightmost acceptable grid token
        if g and len(line.strip()) > 6:
            if cur:
                recs.append(cur)
            name, gloss = split_name_gloss(g[1])
            cur = dict(source=source, sheet=sheet, page=page, grid=g[0], name_raw=name,
                       gloss=gloss, line=line.strip()[:200])
        elif cur and line.strip():
            if len(cur["gloss"]) < 400:
                cur["gloss"] = (cur["gloss"] + " " + line.strip()).strip()
        elif not line.strip() and cur and cur["gloss"]:
            recs.append(cur)
            cur = None
    if cur:
        recs.append(cur)
    return recs


def main():
    root = sys.argv[1]
    dl = os.path.join(root, "downloads")
    global ALLOWED
    from collections import Counter
    with open(os.path.join(dl, "palmer_djvu.txt"), encoding="utf-8", errors="replace") as fh:
        lines = fh.readlines()
    # pass 1: learn the grid squares actually used on each sheet (count >= 4)
    c = Counter((r["sheet"], r["grid"]) for r in parse_lines(lines, "djvu"))
    ALLOWED = {}
    for (sh, g), n in c.items():
        if n >= 4 and g not in JUNK:
            ALLOWED.setdefault(sh, set()).add(g)
    recs = parse_lines(lines, "djvu")
    # tesseract pages: sheet carried across pages in order
    sheet = None
    for f in sorted(glob.glob(os.path.join(dl, "ocr", "txt", "p*.txt"))):
        with open(f, encoding="utf-8", errors="replace") as fh:
            lines = fh.readlines()
        page = int(re.search(r"p(\d+)\.txt", f).group(1))
        # infer sheet from page ranges (checked against headers in the djvu text)
        ranges = [(221, 250, "XIV"), (251, 264, "XV"), (265, 278, "XVI"), (279, 338, "XVII"),
                  (339, 358, "XVIII"), (385, 415, "XXI"), (416, 420, "XXII"), (421, 426, "XXIV")]
        sh = None
        for a, b, s in ranges:
            if a <= page <= b:
                sh = s
        rs = parse_lines(lines, "tess", page0=page, sheet0=sh)
        for r in rs:
            r["sheet"] = r["sheet"] or sh
        recs += rs
    out = os.path.join(root, "data", "palmer_names.csv")
    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["source", "sheet", "page", "grid", "name_raw", "gloss", "line"])
        w.writeheader()
        for r in recs:
            w.writerow(r)
    from collections import Counter
    print(len(recs), Counter((r["source"], r["sheet"]) for r in recs).most_common(60))


if __name__ == "__main__":
    main()
