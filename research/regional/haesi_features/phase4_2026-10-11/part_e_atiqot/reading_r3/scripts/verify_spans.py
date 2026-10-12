#!/usr/bin/env python3
"""Phase 4, part E, reader r3: span hashes and quote checks (run on the owner's Mac, next to the text files).

Input: spec.json = [[unit_id, text_lines, [quotes...]], ...] (built from data/units/*.json).
Text: <unit_id>.raw.txt made with `pdftotext -raw` from the downloaded PDF (outside the repository).
text_lines: ';'-separated 'a-b' line ranges (1-based, inclusive) of the raw text; 'all' = the whole file;
            'grep:all' marks keyword searches over the whole file and is not hashed.
Hash: SHA-256 of the UTF-8 text of the listed ranges joined by '\n', whitespace collapsed to single spaces.
Quote check (NFKC, whitespace collapsed): 'exact' = substring of the whole text; 'dehyph' = substring after
removing line-break hyphens; 'tokens' = every token present (used for Hebrew, whose word order pdftotext
reverses within lines). Prints one JSON object per unit. Standard library only.
"""
import hashlib
import json
import re
import sys
import unicodedata


def norm(s):
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("‏", "").replace("‎", "").replace("‫", "").replace("‬", "")
    return re.sub(r"\s+", " ", s).strip()


def span_text(lines, spec):
    if spec.strip() == "all":
        return "\n".join(lines)
    out = []
    for part in spec.split(";"):
        part = part.strip()
        if not part or part.startswith("grep:"):
            continue
        a, b = (int(x) for x in part.split("-"))
        out.extend(lines[a - 1:b])
    return "\n".join(out)


def check_quote(q, full):
    nq, nf = norm(q), norm(full)
    if nq in nf:
        return "exact"
    dh = re.sub(r"(\w)- (\w)", r"\1\2", nf)
    if nq in dh or re.sub(r"(\w)- (\w)", r"\1\2", nq) in dh:
        return "dehyph"
    nospace = nf.replace(" ", "")
    if nq.replace(" ", "") in nospace:
        return "nospace"
    toks = [t.strip(".,;:()\"'") for t in nq.split()]
    toks = [t for t in toks if t]
    def present(t):
        # Hebrew hyphenated words come out of pdftotext with their parts in reverse order
        return t in nf or ("-" in t and "-".join(reversed(t.split("-"))) in nf)

    if all(present(t) for t in toks):
        return "tokens"
    return "NOT FOUND: " + " | ".join(t for t in toks if not present(t))


def main(spec_path, text_dir):
    spec = json.load(open(spec_path, encoding="utf-8"))
    for unit, tl, quotes in spec:
        lines = open("%s/%s.raw.txt" % (text_dir, unit), encoding="utf-8", errors="replace").read().split("\n")
        full = "\n".join(lines)
        span = span_text(lines, tl)
        h = hashlib.sha256(norm(span).encode("utf-8")).hexdigest()
        res = [check_quote(q, full) for q in quotes]
        print(json.dumps({"unit": unit, "n_lines": len(lines), "span_chars": len(norm(span)), "sha256": h,
                          "quotes": res}, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
