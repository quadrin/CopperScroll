#!/usr/bin/env python3
"""W2-D CIIP / CPJ search for the seven Copper Scroll Greek letter groups.

Usage: python3 -I ciip_search.py TEXTFILE LABEL OUT.tsv [--tokens OUT_tokens.tsv]

Input: pdftotext -layout output (pages separated by \f).
For every Greek "token" (letters + editorial brackets) the script computes the
INSCRIBED letters before the first "(" (abbreviation expansion) and decides:
  - EXACT: the token's inscribed letters equal a target and nothing written follows
           (standalone mark, or abbreviation like Θε(όδωρος)), or
  - PREFIX_FULLWORD: the token begins with the target but continues with written letters
           (a fully written word) -> counted only, never a hit.
Also searches Latin look-alike all-caps tokens (OCR/transliteration variants).
Outputs one row per EXACT candidate (and look-alikes) with page, current inscription
number (last 'NNNN.' header seen), and a context window, for manual classification.
"""
import re, sys, unicodedata, collections

TARGETS = ["ΚΕΝ", "ΧΑΓ", "ΗΝ", "ΘΕ", "ΔΙ", "ΤΡ", "ΣΚ"]
SENS = ["ΞΕ", "ΤΡΙ", "ΙΣΚ", "ΧΚ", "ΞΚ"]
ALL = TARGETS + SENS

LOOK = str.maketrans({"K": "Κ", "E": "Ε", "N": "Ν", "X": "Χ", "A": "Α", "H": "Η", "T": "Τ",
                      "P": "Ρ", "I": "Ι", "O": "Ο", "C": "Σ", "M": "Μ", "B": "Β", "Z": "Ζ",
                      "Y": "Υ", "Ϲ": "Σ", "ϲ": "Σ", "Є": "Ε", "є": "Ε"})

GREEK_RE = re.compile(r"[Ͱ-Ͽἀ-῿̀-ͯ\[\]\(\)⟦⟧⟨⟩\{\}<>·ʹ'’`ϹϲЄє]+")
LATCAP_RE = re.compile(r"(?<![A-Za-zͰ-Ͽ])([A-Z]{2,3})(?![A-Za-zͰ-Ͽ])")
HEAD_RE = re.compile(r"^\s{0,6}(\d{1,4})\.\s+\S")


def norm_letters(s):
    """strip diacritics, uppercase, unify sigma/epsilon forms; keep brackets"""
    s = s.replace("Ϲ", "Σ").replace("ϲ", "Σ").replace("Є", "Ε").replace("є", "Ε")
    s = unicodedata.normalize("NFD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    s = s.upper().replace("ς", "Σ")
    return s


def inscribed_prefix(tok):
    """letters actually written before the first '(' ; restored letters in [] are marked with '_'"""
    out = []
    inbr = False
    for ch in tok:
        if ch == "(":
            break
        if ch in "[⟦":
            inbr = True
            continue
        if ch in "]⟧":
            inbr = False
            continue
        if ch in "⟨⟩{}<>·ʹ'’`":
            continue
        if "Α" <= ch <= "Ω":
            out.append("_" if inbr else ch)
    return "".join(out)


def main():
    path, label, outp = sys.argv[1], sys.argv[2], sys.argv[3]
    text = open(path, encoding="utf-8", errors="replace").read()
    pages = text.split("\f")
    rows = []
    prefix_counts = collections.Counter()
    exact_counts = collections.Counter()
    token_total = 0
    cur_no = ""
    for pi, page in enumerate(pages, start=1):
        lines = page.split("\n")
        for li, line in enumerate(lines):
            # v2: join letters split by pdftotext after combining dots / precomposed dotted letters
            line = unicodedata.normalize("NFD", line)
            line = re.sub(r"\u0323\s+(?=[\u0391-\u03A9A-Z])", "\u0323", line)
            line = unicodedata.normalize("NFC", line)
            m = HEAD_RE.match(line)
            if m and int(m.group(1)) > 0:
                cur_no = m.group(1)
            ctx = " | ".join(x.strip() for x in lines[max(0, li - 2): li + 3])
            for gm in GREEK_RE.finditer(line):
                tok = gm.group(0)
                nt = norm_letters(tok)
                ins = inscribed_prefix(nt)
                if not ins:
                    continue
                token_total += 1
                has_paren = "(" in nt
                for t in ALL:
                    if ins == t:
                        kind = "EXACT_ABBR" if has_paren else "EXACT"
                        exact_counts[t] += 1
                        rows.append((label, pi, cur_no, t, kind, tok, line.strip()[:200], ctx[:600]))
                    elif ins.startswith(t):
                        prefix_counts[t] += 1
                    elif "_" in ins and ins.replace("_", "")[:len(t)] == t and len(ins) == len(t):
                        rows.append((label, pi, cur_no, t, "EXACT_WITH_RESTORED", tok, line.strip()[:200], ctx[:600]))
            # Latin look-alike all-caps 2-3 letter tokens
            for lm in LATCAP_RE.finditer(line):
                tok = lm.group(1)
                g = tok.translate(LOOK)
                if g in ALL:
                    rows.append((label, pi, cur_no, g, "LATIN_LOOKALIKE", tok, line.strip()[:200], ctx[:600]))
            # mixed Greek/Latin tokens e.g. 'ΘE', 'XAΓ'
            for mm in re.finditer(r"(?<![A-Za-zͰ-Ͽ])([A-ZΑ-ΩϹЄ]{2,3})(?![A-Za-zͰ-Ͽ])", line):
                tok = mm.group(1)
                if re.search(r"[A-Z]", tok) and re.search(r"[Α-ΩϹЄ]", tok):
                    g = tok.translate(LOOK)
                    if g in ALL:
                        rows.append((label, pi, cur_no, g, "MIXED_LOOKALIKE", tok, line.strip()[:200], ctx[:600]))
    with open(outp, "w", encoding="utf-8") as f:
        f.write("source\tpdf_page\tlast_header_no\ttarget\tkind\ttoken\tline\tcontext\n")
        for r in rows:
            f.write("\t".join(str(x).replace("\t", " ") for x in r) + "\n")
    summ = {"source": label, "pages": len(pages), "greek_tokens": token_total,
            "exact_or_abbr": dict(exact_counts), "prefix_fullword": dict(prefix_counts),
            "candidate_rows": len(rows)}
    print(summ)


if __name__ == "__main__":
    main()
