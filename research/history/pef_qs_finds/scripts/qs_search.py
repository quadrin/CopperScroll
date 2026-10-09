"""Search QS OCR text for find reports near project places.

Standard library only. Run with python3 -I.

    python3 -I qs_search.py TERMS.json TEXT_DIR OUT_DIR

TEXT_DIR holds one folder per archive.org item, each with
<id>_hocr_searchtext.txt.gz, <id>_hocr_pageindex.json.gz and
<id>_page_numbers.json (see volumes.csv for URLs and SHA-256).
OUT_DIR receives:
  hits_raw.csv     one row per (item, leaf, key) hit, no OCR text
  occurrences.csv  pattern occurrences per item and key (for recall checks)
  context.jsonl    OCR context around each hit (keep OUT of the repository)
"""
import csv
import gzip
import json
import os
import re
import sys
import unicodedata

ART = "(?:(?:el|es|ed|et|en|er|ez|ej|esh|eth|al|as|ad|at|an|ar|az|ash|ul|il|e) )?"
A_ALT = "(?:a|aa|ad|dd|d|4|e)"
U_ALT = "(?:u|ii|ti|it|tr|ui|iu)"
APOS = set("'‘’‛ʼʻʿʾ`´′")
MONTHS = "JANUARY|FEBRUARY|MARCH|APRIL|MAY|JUNE|JULY|AUGUST|SEPTEMBER|OCTOBER|NOVEMBER|DECEMBER"
WINDOW = 300


def tolerant(pat):
    """Apply the frozen OCR tolerance to literal a and u outside [...] and {ART}."""
    out, i, in_class = [], 0, False
    while i < len(pat):
        if pat.startswith("{ART}", i) and not in_class:
            out.append("{ART}")
            i += 5
            continue
        c = pat[i]
        if c == "[" and not in_class:
            in_class = True
        elif c == "]" and in_class:
            in_class = False
        if not in_class and c == "a":
            out.append(A_ALT)
        elif not in_class and c == "u":
            out.append(U_ALT)
        else:
            out.append(c)
        i += 1
    return "".join(out)


def compile_pattern(pat, exact):
    body = pat if pat in exact else tolerant(pat)
    body = body.replace("{ART}", ART)
    return re.compile(r"(?<![a-z0-9])" + body + r"(?![a-z0-9])")


def compile_terms(terms):
    return [re.compile(r"(?<![a-z0-9])" + t + r"(?![a-z0-9])") for t in terms]


def normalize(raw, join_hyphens):
    """Return (normalized text, list mapping each normalized char to a raw index)."""
    out, pos = [], []
    n = len(raw)
    i = 0
    last_space = True
    while i < n:
        c = raw[i]
        if join_hyphens and c in "-­" and i > 0 and raw[i - 1].isalpha():
            j = i + 1
            saw_ws = False
            while j < n and raw[j] in " \t\r\n":
                j += 1
                saw_ws = True
            if saw_ws and j < n and raw[j].isalpha():
                i = j
                continue
        if c in APOS:
            i += 1
            continue
        lc = c.lower()
        if lc in ("œ",):
            seq = "oe"
        elif lc in ("æ",):
            seq = "ae"
        else:
            d = unicodedata.normalize("NFKD", lc)
            seq = "".join(ch for ch in d if not unicodedata.combining(ch))
        for ch in seq:
            if ("a" <= ch <= "z") or ("0" <= ch <= "9"):
                out.append(ch)
                pos.append(i)
                last_space = False
            else:
                if not last_space:
                    out.append(" ")
                    pos.append(i)
                    last_space = True
        i += 1
    return "".join(out), pos


HEAD_RE = re.compile(r"^\s*(?:\d{1,3}\s+[A-Z][A-Z .,;:'’&-]{5,}|[A-Z][A-Z .,;:'’&-]{5,}\s+\d{1,3}\.?)\s*$")


def split_djvu_by_heads(text):
    """Fallback when the page-indexed search text is unavailable: split the plain
    _djvu.txt at running-head lines (a page number beside an upper-case title)."""
    pages, cur = [], []
    for line in text.split("\n"):
        if HEAD_RE.match(line) and cur:
            pages.append("\n".join(cur))
            cur = []
        cur.append(line)
    if cur:
        pages.append("\n".join(cur))
    return pages


def load_item(dirpath, ident):
    """Return (pages, page_number_map, mode)."""
    pn_path = os.path.join(dirpath, ident + "_page_numbers.json")
    pn = {}
    try:
        for p in json.load(open(pn_path, encoding="utf-8")).get("pages", []):
            pn[p["leafNum"]] = p.get("pageNumber") or ""
    except (OSError, ValueError):
        pn = {}
    try:
        st = gzip.open(os.path.join(dirpath, ident + "_hocr_searchtext.txt.gz")).read().decode("utf-8")
        pi = json.load(gzip.open(os.path.join(dirpath, ident + "_hocr_pageindex.json.gz")))
        return [st[a:b] for a, b, *_ in pi], pn, "searchtext"
    except (OSError, ValueError, EOFError):
        text = open(os.path.join(dirpath, ident + "_djvu.txt"), encoding="utf-8").read()
        return split_djvu_by_heads(text), {}, "djvu_split"


def running_head_number(text):
    lines = [l.strip() for l in text.strip().split("\n") if l.strip()]
    if not lines:
        return ""
    for line in (lines[0], lines[-1]):
        m = re.match(r"^(\d{1,3})\b", line) or re.search(r"\b(\d{1,3})$", line)
        if m:
            return m.group(1)
    return ""


def _valid(v):
    return v.isdigit() and int(v) > 0


def printed_pages(pages, pn):
    """Printed page per leaf, with its source ('running_head',
    'page_numbers.json' or 'inferred').

    Revised after the first coding pass, when archive.org page_numbers.json
    was found to count plates in some volumes (e.g. QS 1872 April, 1885
    January, 1893, 1901, 1905), shifting whole runs of pages.
    Pass A confirms a leaf's own running head when page_numbers.json gives
    the same number, or when a running head within two leaves fits the same
    leaf-to-page offset. Pass B, for the other leaves: page_numbers.json if
    it fits the offset of a confirmed leaf within two leaves; else the offset
    best supported by confirmed leaves within four leaves (weights
    1/(1+distance), at least two leaves); else page_numbers.json; else the
    leaf's own running head if it fits between the nearest confirmed pages;
    else inference from the nearest confirmed leaf. Plates and unnumbered
    front matter get approximate 'inferred' numbers.
    """
    n = len(pages)
    rh = [running_head_number(t) for t in pages]
    js = [str(pn.get(leaf, "") or "") for leaf in range(n)]
    conf = {}
    for leaf in range(n):
        r = rh[leaf]
        if not _valid(r):
            continue
        o = int(r) - leaf
        if js[leaf] == r or any(_valid(rh[k]) and int(rh[k]) - k == o
                                for k in range(max(0, leaf - 2), min(n, leaf + 3)) if k != leaf):
            conf[leaf] = int(r)
    out = []
    for leaf in range(n):
        if leaf in conf:
            out.append([str(conf[leaf]), "running_head"])
            continue
        p = js[leaf]
        near = [k for k in conf if abs(k - leaf) <= 2]
        if _valid(p) and any(conf[k] - k == int(p) - leaf for k in near):
            out.append([p, "page_numbers.json"])
            continue
        score, count = {}, {}
        for k in conf:
            if abs(k - leaf) <= 4:
                o = conf[k] - k
                score[o] = score.get(o, 0.0) + 1.0 / (1 + abs(k - leaf))
                count[o] = count.get(o, 0) + 1
        good = [(score[o], -abs(o), o) for o in score if count[o] >= 2 and leaf + o > 0]
        if good:
            page = str(leaf + max(good)[2])
            out.append([page, "page_numbers.json" if p == page else "inferred"])
            continue
        if _valid(p):
            out.append([p, "page_numbers.json"])
            continue
        out.append(["", ""])
    known = [k for k in range(n) if out[k][0] and out[k][1] != "inferred"]
    res = [list(x) for x in out]
    for leaf in range(n):
        if out[leaf][0]:
            continue
        prev = max((k for k in known if k < leaf), default=None)
        nxt = min((k for k in known if k > leaf), default=None)
        r = rh[leaf]
        if _valid(r) and prev is not None and nxt is not None:
            pp, pq = int(out[prev][0]), int(out[nxt][0])
            if pp < int(r) < pq and int(r) - pp <= leaf - prev and pq - int(r) <= nxt - leaf:
                res[leaf] = [r, "running_head"]
                continue
        cands = []
        if nxt is not None and int(out[nxt][0]) - (nxt - leaf) > 0:
            cands.append((nxt - leaf, 0, int(out[nxt][0]) - (nxt - leaf)))
        if prev is not None:
            cands.append((leaf - prev, 1, int(out[prev][0]) + (leaf - prev)))
        if cands:
            res[leaf] = [str(min(cands)[2]), "inferred"]
    return res


def item_year_issue(ident, pages):
    tail = ident.split("_", 1)[1]
    years = []
    m = re.match(r"^(\d{4})-(\d{2})$", tail)
    if m:
        return [(tail[:4], m.group(2))] * len(pages)
    m = re.match(r"^(\d{4})_(\d)$", tail)
    if m:
        return [(tail[:4], "no" + m.group(2))] * len(pages)
    if re.match(r"^\d{4}$", tail):
        return [(tail, "")] * len(pages)
    # 1869-70 combined volume: reprinted Reports on Progress (1867-69) come first,
    # then Quarterly Statement Nos. 1-7. Nos. 1-3 are dated 1869 and Nos. 4-7 1870
    # (inference from their contents). Issue numbers are read from the issue headers.
    cur = ("1867-69", "reports")
    for text in pages:
        head = text[:300].upper()
        mm = re.search(r"S\w{3,6}EMENT[,.]?\s+NO\.\s*(\d)", head)
        if mm:
            n = int(mm.group(1))
            cur = ("1869" if n <= 3 else "1870", "no%d" % n)
        elif cur[1] == "reports" and "QUARTERLY STATEMENT OF PROGRESS" in head:
            cur = ("1869", "no1")
        years.append(cur)
    return years


def main():
    terms_path, text_dir, out_dir = sys.argv[1:4]
    T = json.load(open(terms_path, encoding="utf-8"))
    exact = set(T["exact_patterns"])
    keys = []
    for k, v in T["places"].items():
        keys.append((k, v, "place"))
    for k, v in T["groups"].items():
        keys.append((k, v, "group"))
    comp = []
    for k, v, kind in keys:
        pats = [(p, compile_pattern(p, exact)) for p in v["patterns"]]
        excl = [compile_pattern(p, exact) for p in v.get("exclude", [])]
        ctx = v.get("context_any", [])
        comp.append((k, v.get("region", ""), pats, excl, ctx))
    strong = compile_terms(T["find_terms"]["strong"])
    feature = compile_terms(T["find_terms"]["feature"])
    disc = compile_terms(T["find_terms"]["discovery"])

    idents = sorted(d for d in os.listdir(text_dir)
                    if os.path.isdir(os.path.join(text_dir, d)) and "index" not in d)
    os.makedirs(out_dir, exist_ok=True)
    hits_rows, occ_rows, ctx_out = [], [], []
    for ident in idents:
        pages, pn, mode = load_item(os.path.join(text_dir, ident), ident)
        pp = printed_pages(pages, pn)
        yi = item_year_issue(ident, pages)
        occ_count = {}
        for leaf, raw in enumerate(pages):
            if not raw.strip():
                continue
            versions = []
            for join in (False, True):
                versions.append((join,) + normalize(raw, join))
            page_norm_b = versions[0][1]
            found = {}  # key -> (version_index, start, end, raw_start, raw_end, cls, terms)
            for vi, (join, norm, pos) in enumerate(versions):
                # term positions
                def spans(regs):
                    s = []
                    for r in regs:
                        s.extend((m.start(), m.end(), m.group(0)) for m in r.finditer(norm))
                    return s
                S, F, D = spans(strong), spans(feature), spans(disc)
                allm = []
                for k, region, pats, excl, ctx in comp:
                    if ctx and not any(re.search(r"(?<![a-z0-9])" + re.escape(c) + r"(?![a-z0-9])", page_norm_b) for c in ctx):
                        continue
                    ex_spans = [(m.start(), m.end()) for e in excl for m in e.finditer(norm)]
                    for p, r in pats:
                        for m in r.finditer(norm):
                            if any(a <= m.start() and m.end() <= b for a, b in ex_spans):
                                continue
                            allm.append((m.start(), m.end(), k, region))
                # suppress matches contained in a longer match of another key
                kept = []
                for s0, e0, k0, r0 in allm:
                    inside = any(k1 != k0 and s1 <= s0 and e0 <= e1 and (e1 - s1) > (e0 - s0)
                                 for s1, e1, k1, r1 in allm)
                    if not inside:
                        kept.append((s0, e0, k0, r0))
                if vi == 0:
                    for s0, e0, k0, r0 in kept:
                        occ_count[k0] = occ_count.get(k0, 0) + 1
                for s0, e0, k0, r0 in sorted(kept):
                    lo, hi = max(0, s0 - WINDOW), e0 + WINDOW

                    def inwin(lst):
                        return sorted(set(t for a, b, t in lst
                                          if a < hi and b > lo and not (a >= s0 and b <= e0)))
                    s_in, f_in, d_in = inwin(S), inwin(F), inwin(D)
                    cls = "strong" if s_in else ("feature" if (f_in and d_in) else "")
                    if not cls:
                        continue
                    prev = found.get(k0)
                    rank = 0 if cls == "strong" else 1
                    if prev is None or (rank < prev[0]):
                        found[k0] = (rank, vi, s0, e0, pos[s0], pos[e0 - 1] + 1, cls, s_in, f_in, d_in,
                                     sum(1 for x in kept if x[2] == k0))
            for k0, (rank, vi, s0, e0, rs, re_, cls, s_in, f_in, d_in, nocc) in sorted(found.items()):
                region = next(c[1] for c in comp if c[0] == k0)
                hid = "%s:%d:%s" % (ident, leaf, k0)
                year, issue = yi[leaf]
                hits_rows.append({
                    "hit_id": hid, "ia_identifier": ident, "year": year, "issue": issue, "leaf": leaf,
                    "printed_page": pp[leaf][0], "page_source": pp[leaf][1], "key": k0, "region": region,
                    "hit_class": cls, "matched_text": re.sub(r"\s+", " ", raw[rs:re_])[:60],
                    "strong_terms": "|".join(s_in), "feature_terms": "|".join(f_in),
                    "discovery_terms": "|".join(d_in), "occurrences_on_page": nocc,
                    "text_version": ("B_space" if vi == 0 else "A_joined") + ("" if mode == "searchtext" else "/" + mode),
                })
                c0, c1 = max(0, rs - 450), min(len(raw), re_ + 450)
                head = raw.strip().split("\n")[0][:90]
                ctx_out.append({"hit_id": hid, "head": head, "match": raw[rs:re_],
                                "before": re.sub(r"\s+", " ", raw[c0:rs]),
                                "after": re.sub(r"\s+", " ", raw[re_:c1])})
        for k0 in sorted(occ_count):
            occ_rows.append({"ia_identifier": ident, "key": k0, "occurrences": occ_count[k0]})
    hf = ["hit_id", "ia_identifier", "year", "issue", "leaf", "printed_page", "page_source", "key",
          "region", "hit_class", "matched_text", "strong_terms", "feature_terms", "discovery_terms",
          "occurrences_on_page", "text_version"]
    with open(os.path.join(out_dir, "hits_raw.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=hf)
        w.writeheader()
        w.writerows(hits_rows)
    with open(os.path.join(out_dir, "occurrences.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["ia_identifier", "key", "occurrences"])
        w.writeheader()
        w.writerows(occ_rows)
    with open(os.path.join(out_dir, "context.jsonl"), "w", encoding="utf-8") as f:
        for c in ctx_out:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    print("items", len(idents), "hits", len(hits_rows))


if __name__ == "__main__":
    main()
