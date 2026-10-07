#!/usr/bin/env python3
"""Split a CIIP pdftotext file into records; list mark-like records.
usage: records.py TEXTFILE LABEL OUT.tsv
Output columns: label, no, pdf_page, title, n_greek_cap_lines, short_greek_tokens (<=3 letters, standalone
in diplomatic capitals lines), keyword_flags
"""
import re, sys, unicodedata

HEAD = re.compile(r"(?m)^\s{0,6}(\d{3,4}[A-Za-z]?)\.\s+(\S.*)$")
KEYS = ["mason", "mark", "jar", "amphora", "ossuar", "monogram", "abbreviat", "weight", "label",
        "dipint", "graffit", "initial", "letters", "stamp", "seal", "token", "measure", "numeral", "sign"]


def strip(s):
    s = unicodedata.normalize("NFD", s)
    return "".join(c for c in s if not unicodedata.combining(c))


def main():
    path, label, outp = sys.argv[1:4]
    text = open(path, encoding="utf-8", errors="replace").read()
    # page offsets
    offs = []
    o = 0
    for i, p in enumerate(text.split("\f"), 1):
        offs.append((o, i)); o += len(p) + 1
    heads = list(HEAD.finditer(text))
    rows = []
    last_no = 0
    for k, m in enumerate(heads):
        no = m.group(1)
        try:
            n_int = int(re.match(r"\d+", no).group(0))
        except Exception:
            continue
        start = m.start(); end = heads[k + 1].start() if k + 1 < len(heads) else len(text)
        seg = text[start:end]
        title_lines = [m.group(2)]
        # titles are sometimes split 'G\n       reek ...'
        nxt = seg.split("\n")[1:3]
        title = m.group(2).strip()
        if len(title) <= 2 and nxt:
            title = title + nxt[0].strip()
        page = max(i for oo, i in offs if oo <= start)
        caps_lines = []
        for line in seg.split("\n")[1:]:
            s = strip(line).strip()
            if not s:
                continue
            # a diplomatic line: mostly Greek capitals/brackets, few Latin lowercase letters
            g = sum(1 for c in s if "Α" <= c <= "Ω" or c in "ϹЄ")
            lat = sum(1 for c in s if c.isalpha() and c.isascii() and c.islower())
            if g >= 1 and lat <= 3 and g >= 0.5 * sum(1 for c in s if c.isalpha()):
                caps_lines.append(s[:80])
        short = []
        for cl in caps_lines:
            for t in re.findall(r"(?<![Α-ΩϹЄA-Z])([Α-ΩϹЄ]{1,3})(?![Α-ΩϹЄA-Z])", cl):
                short.append(t)
        flags = [kk for kk in KEYS if kk in title.lower()]
        rows.append((label, no, page, title[:120], len(caps_lines), " ".join(short[:40]), ",".join(flags),
                     " || ".join(caps_lines[:8])))
    with open(outp, "w", encoding="utf-8") as f:
        f.write("label\tno\tpdf_page\ttitle\tn_caps_lines\tshort_tokens\tflags\tcaps_lines\n")
        for r in rows:
            f.write("\t".join(str(x).replace("\t", " ") for x in r) + "\n")
    print(label, "records:", len(rows))


if __name__ == "__main__":
    main()
