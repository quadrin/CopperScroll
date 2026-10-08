#!/usr/bin/env python3
"""Hebrew/Aramaic -> Arabic (Palmer SWP transliteration) toponym matching.

Documented rules (IDs used in rule paths; see REPORT.md section 3 for sources):
 Hebrew side
  H1  final aleph (Aramaic emphatic -ā) and final he (fem. -ā) are vowels: dropped.
  H2  medial waw / yod are matres lectionis or glides: weak (cheap to lose or gain).
  H3  final taw after a strong consonant may be the feminine ending -at/-it: cheap to lose.
 Arabic (Palmer) side
  A1  Palmer's printed transliteration does not distinguish s/ṣ, k/q, t/ṭ, h/ḥ, d/ḍ, z/ẓ
      (Palmer 1881 preface p. iii) -> these pairs are merged.
  A2  generic topographic words (Khŭrbet, ʿAin, Wâdy, Tell, Bîr, Jebel, Râs, Umm, Abu, Deir, ...)
      and the article (el, ed, es, esh, et, en, er, ez, edh ...) are stripped before comparison.
  A3  word-final -eh/-ah is the feminine tāʾ marbūṭa: weak.
  A4  geminates are written double in Palmer and collapsed to one consonant.
 Correspondences (cost 0 = regular; higher = less regular)
  R1  identity (letter for letter: Palmer 1881 p. iv)
  R2  šin/samekh -> s or sh (Palmer 1881 p. iv; Kampffmeyer 1892 §16, §22)
  R3  ḥet -> ḥ (regular); -> kh (PS *ḫ merged in Hebrew ḥ; Palmer p. iv k/kh); -> ʿ or lost
      (Kampffmeyer 1892 §9, pp. 24-26)
  R4  ʿayin -> ʿ (regular); -> gh (PS *ġ); -> ḥ (Palmer p. iv); -> alif/lost (Palmer p. iv, rare)
  R5  pe -> f (Arabic has no p; Kampffmeyer 1892 §18)
  R6  qof -> q/k (merged in Palmer); kaf -> k, or kh (spirantised kaf)
  R7  gimel -> j (Arabic ǧīm), e.g. Gibeah/Jebaʿ
  R8  ṣade -> ṣ (merged with s in Palmer), ḍ/ẓ (written dh in Palmer)
  R9  zayin -> z or dh; dalet -> d or dh; taw -> t or th
  R10 liquids and nasals alternate l~n~r, m~n, b~m (e.g. Jezreel/Zerʿīn, Timnah/Tibneh)
  R11 adjacent-consonant metathesis
  R12 loss of a Hebrew consonant (weak letters cheap; gutturals medium; others expensive)
  R13 insertion of an Arabic consonant (glides w/y cheap; Arabic suffix -ān/-īn/-at medium)
  R14 degemination (two identical Hebrew radicals realised as one Arabic geminate)
"""
import re
import unicodedata

HEB_MAP = {"א": "'", "ב": "b", "ג": "g", "ד": "d", "ה": "h", "ו": "w", "ז": "z", "ח": "H", "ט": "7",
           "י": "y", "כ": "k", "ך": "k", "ל": "l", "מ": "m", "ם": "m", "נ": "n", "ן": "n", "ס": "s",
           "ע": "3", "פ": "p", "ף": "p", "צ": "C", "ץ": "C", "ק": "q", "ר": "r", "ש": "$", "ת": "t"}
HEB_NAME = {"'": "ʾ", "b": "b", "g": "g", "d": "d", "h": "h", "w": "w", "z": "z", "H": "ḥ", "7": "ṭ",
            "y": "y", "k": "k", "l": "l", "m": "m", "n": "n", "s": "s", "3": "ʿ", "p": "p", "C": "ṣ",
            "q": "q", "r": "r", "$": "š", "t": "t"}
AR_NAME = {"b": "b", "j": "j", "d": "d", "D": "dh", "h": "h", "w": "w", "z": "z", "X": "kh", "t": "t",
           "y": "y", "k": "k", "l": "l", "m": "m", "n": "n", "s": "s", "S": "sh", "3": "ʿ", "G": "gh",
           "f": "f", "r": "r", "T": "th", "'": "ʾ", "E": "-eh", "g": "g"}
WEAK_H = {"'", "h", "w", "y"}

def heb_tokens(core):
    """Hebrew consonantal core -> list of (token, weak?) applying H1-H3."""
    letters = [HEB_MAP[c] for c in core if c in HEB_MAP]
    # H1: drop final aleph/he
    while len(letters) > 1 and letters[-1] in ("'", "h"):
        letters = letters[:-1]
    toks = []
    for i, c in enumerate(letters):
        weak = c in WEAK_H and not (i == 0 and c in ("w", "y"))
        if c == "t" and i == len(letters) - 1 and i >= 2:
            toks.append(("t", "fem"))  # H3
        else:
            toks.append((c, "weak" if weak else "strong"))
    return toks

# --- substitution costs Hebrew token -> Arabic token, with rule ids
SUB = {
    "'": {"'": (0, "R1"), "3": (0.5, "R4")},
    "b": {"b": (0, "R1"), "m": (0.5, "R10"), "f": (0.6, "R5"), "w": (0.6, "R10")},
    "g": {"j": (0, "R7"), "g": (0, "R7"), "G": (0.5, "R7"), "k": (0.7, "R7")},
    "d": {"d": (0, "R1"), "D": (0.3, "R9"), "t": (0.6, "R9"), "T": (0.6, "R9")},
    "h": {"h": (0.2, "R1"), "E": (0.1, "A3")},
    "w": {"w": (0, "R1"), "b": (0.6, "R10"), "y": (0.3, "H2")},
    "z": {"z": (0, "R1"), "D": (0.4, "R9"), "s": (0.6, "R9"), "S": (0.8, "R9")},
    "H": {"h": (0, "R3"), "X": (0.3, "R3"), "3": (0.5, "R3"), "G": (0.8, "R3"), "E": (0.6, "R3")},
    "7": {"t": (0, "R1"), "d": (0.5, "R9"), "T": (0.6, "R9")},
    "y": {"y": (0, "R1"), "w": (0.3, "H2")},
    "k": {"k": (0, "R6"), "X": (0.3, "R6"), "j": (0.7, "R6"), "G": (0.8, "R6")},
    "l": {"l": (0, "R1"), "n": (0.4, "R10"), "r": (0.5, "R10")},
    "m": {"m": (0, "R1"), "n": (0.4, "R10"), "b": (0.5, "R10")},
    "n": {"n": (0, "R1"), "l": (0.4, "R10"), "m": (0.4, "R10"), "r": (0.5, "R10")},
    "s": {"s": (0, "R2"), "S": (0.3, "R2"), "z": (0.6, "R2"), "T": (0.6, "R2"), "t": (0.8, "R2")},
    "3": {"3": (0, "R1"), "G": (0.3, "R4"), "h": (0.5, "R4"), "'": (0.5, "R4"), "E": (0.6, "R4")},
    "p": {"f": (0, "R5"), "b": (0.4, "R5"), "m": (0.8, "R5")},
    "C": {"s": (0, "R8"), "D": (0.3, "R8"), "z": (0.5, "R8"), "S": (0.6, "R8"), "T": (0.7, "R8"), "t": (0.8, "R8")},
    "q": {"k": (0, "R6"), "G": (0.6, "R6"), "j": (0.6, "R6"), "X": (0.7, "R6")},
    "r": {"r": (0, "R1"), "l": (0.5, "R10"), "n": (0.5, "R10")},
    "$": {"s": (0, "R2"), "S": (0, "R2"), "T": (0.4, "R2"), "z": (0.8, "R2")},
    "t": {"t": (0, "R1"), "T": (0.3, "R9"), "d": (0.6, "R9")},
}
MISMATCH = 1.0

def del_cost(tok, kind):
    if kind == "weak":
        return 0.1
    if kind == "fem":
        return 0.2
    if tok in ("3", "H"):
        return 0.5
    return 0.9

def ins_cost(a, pos, n):
    if a in ("w", "y"):
        return 0.15
    if a == "E":
        return 0.05
    if a == "'":
        return 0.2
    if a == "3":
        return 0.5
    if a == "h":
        return 0.5
    if pos == n - 1 and a in ("n", "t"):
        return 0.4   # Arabic -ān/-īn/-at suffix (R13)
    return 0.8

def align(H, A):
    """Global weighted alignment. H: list of (tok, kind); A: list of tokens.
    Returns (cost, path list of rule strings)."""
    n, m = len(H), len(A)
    INF = 1e9
    D = [[INF] * (m + 1) for _ in range(n + 1)]
    P = [[None] * (m + 1) for _ in range(n + 1)]
    D[0][0] = 0.0
    for i in range(n + 1):
        for j in range(m + 1):
            d = D[i][j]
            if d >= INF:
                continue
            if i < n:  # delete Hebrew consonant (R12) or degeminate (R14)
                h, k = H[i]
                c = del_cost(h, k)
                rule = "R12"
                if i > 0 and H[i - 1][0] == h:
                    c, rule = 0.2, "R14"
                if d + c < D[i + 1][j]:
                    D[i + 1][j] = d + c
                    P[i + 1][j] = (i, j, f"{rule}:-{HEB_NAME[h]}")
            if j < m:  # insert Arabic consonant (R13)
                c = ins_cost(A[j], j, m)
                if d + c < D[i][j + 1]:
                    D[i][j + 1] = d + c
                    P[i][j + 1] = (i, j, f"R13:+{AR_NAME.get(A[j], A[j])}")
            if i < n and j < m:  # substitute
                h, k = H[i]
                a = A[j]
                if h in SUB and a in SUB[h]:
                    c, rule = SUB[h][a]
                elif h == a:
                    c, rule = 0.0, "R1"
                else:
                    c, rule = MISMATCH, "X"
                if k == "weak" and c >= MISMATCH:
                    c = 0.6
                if d + c < D[i + 1][j + 1]:
                    D[i + 1][j + 1] = d + c
                    lab = f"{rule}:{HEB_NAME[h]}>{AR_NAME.get(a, a)}" if rule != "R1" else f"{HEB_NAME[h]}={AR_NAME.get(a, a)}"
                    P[i + 1][j + 1] = (i, j, lab)
            if i + 1 < n and j + 1 < m:  # metathesis of adjacent consonants (R11)
                h1, h2 = H[i][0], H[i + 1][0]
                a1, a2 = A[j], A[j + 1]
                c1 = SUB.get(h1, {}).get(a2, (0 if h1 == a2 else MISMATCH,))[0]
                c2 = SUB.get(h2, {}).get(a1, (0 if h2 == a1 else MISMATCH,))[0]
                if c1 < 0.5 and c2 < 0.5:
                    c = 0.6 + c1 + c2
                    if d + c < D[i + 2][j + 2]:
                        D[i + 2][j + 2] = d + c
                        P[i + 2][j + 2] = (i, j, f"R11:{HEB_NAME[h1]}{HEB_NAME[h2]}>{AR_NAME.get(a1,a1)}{AR_NAME.get(a2,a2)}")
    # backtrace
    path = []
    i, j = n, m
    while (i, j) != (0, 0):
        pi, pj, lab = P[i][j]
        path.append(lab)
        i, j = pi, pj
    return D[n][m], list(reversed(path))

def denom(H):
    return sum(1.0 if k == "strong" else (0.5 if k == "fem" else 0.3) for _, k in H)

def score(H, A):
    cost, path = align(H, A)
    s = max(0.0, 1.0 - cost / max(1.0, denom(H)))
    return s, cost, path

# ---------------- Palmer side ----------------
ARTICLES = {"'i", "'1", "el", "al", "ed", "es", "esh", "et", "eth", "en", "er", "ez", "edh", "ej", "ul", "il", "'l", "l",
            "cl", "cd", "cs", "csh", "ct", "cth", "cn", "cr", "cz", "cdh", "d", "e", "ei", "ech", "esli",
            "ctli", "ccl", "c", "ad", "as", "at", "an", "ar", "az", "ash", "'1", "1"}
GENERIC_RE = re.compile(r"^(?:k(?:h|li)[a-z]{0,3}rb[ce][tl]|r[iu]{1,3}j[imn]{1,2}|mugh[aád]r[ec]t|d(?:h|li)a?hr[ec]t|k(?:h|li)all[ec]t|k[uüi]{1,2}rn[ec]t|b[ií]rk[ec]t|s(?:h|li)eikh|sh?[aá]'?b|'?[aá]i[nmt]|'?din|'?ain|'?aiun|'?ayun|'?aiyun|b[iíîtée]r|btr|jbir|bi[aá]r|biar|"
                        r"w[aáde]{1,2}dy|wady|wadi|w[aá]dy|kh[uüiíl]{1,3}rb[ec]t|kh[uü]rbet|kliurbet|khurbct|khirbet|"
                        r"kh|tell|tel|tellul|tulul|j[ce]bel|jebel|r[aáde]s|ras|umm|um|unim|umin|unnn|abu|ab[uü]|deir|"
                        r"mugh[aá]ret|mugh[aá]ir|maghair|birket|birkct|neby|nebi|sheikh|shcikh|shiekh|ard|'?ar[aád]k|"
                        r"k[uü]rnet|rujm|r[uü]jm|khallet|kh[aá]llet|shi'?b|sha'?b|'?akabet|'?ak[aá]bet|nukb|n[uü]kb|"
                        r"kusr|k[uü]sr|kasr|merj|kefr|beit|bctt|bett|bab|b[aá]b|jisr|burj|kul'?at|kal'?at|m[uü]k[aá]m|"
                        r"mazar|maz[aá]r|kubbet|k[uü]bbet|seil|sahel|sahl|dahret|batn|tor|tubk|tubkat|jurat|jorat|"
                        r"bahr|nahr|haud|hamam|hammam|mukhad|mersa|tal'?at|'?arkub|'?arkiib|dhahr|nebk|ras|"
                        r"bir|biar|'ain|ain|tellet|tellat|kurn|rds|jcbel|wddy|wddi|ivady|ifady)$", re.I)
GLOSS_GENERIC = re.compile(r"^(the|a|an)\s+(spring|well|wells|valley|ruin|ruins|hill|mountain|cave|pool|cistern|"
                           r"top|peak|summit|cliff|shrine|tomb|ascent|pass|road|plain|mound|heap|cairn)", re.I)

def strip_diacritics(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    return s

def clean_name(raw):
    s = strip_diacritics(raw)
    # djvu OCR renders italic h as '/i' or '/?' (e.g. 'S/uiweike/i' = Shuweikeh): restore h
    s = re.sub(r"(?<=[A-Za-z])/[i1l]?", "h", s)
    s = re.sub(r"[’‘`´ʿʻ\"]", "'", s)
    s = re.sub(r"\{[^}]*\}|\([^)]*\)", " ", s)
    s = re.sub(r"[^A-Za-z' \-]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def specific_words(raw, gloss=""):
    s = clean_name(raw)
    toks = [t for t in re.split(r"[ \-]+", s) if t]
    out, generic, kept_beit = [], [], False
    for i, t in enumerate(toks):
        tl = t.lower().strip("'")
        tl2 = t.lower()
        if tl2 in ARTICLES or tl in ARTICLES:
            continue
        if GENERIC_RE.match(tl2) or GENERIC_RE.match(tl):
            generic.append(tl)
            continue
        if i == 0 and GLOSS_GENERIC.match(gloss or "") and len(toks) > 1 and len(tl) <= 6 and not out:
            # first word is very likely an OCR-garbled generic (e.g. 'Str' for Bîr, 'Sir el' ...)
            generic.append(tl + "?")
            continue
        out.append(t)
    return out, generic

def lat_tokens(word, li_fix=False, t_fix=False):
    w = strip_diacritics(word).lower()
    w = re.sub(r"[’‘`´ʿ]", "'", w)
    if li_fix:
        w = re.sub(r"li(?=[aeiou']|$)", "h", w)
        w = w.replace("kli", "kh").replace("sli", "sh").replace("tli", "th").replace("dli", "dh").replace("gli", "gh")
    w = w.replace("zv", "w").replace("v", "w")
    w = w.replace("kh", "X").replace("sh", "S").replace("th", "T").replace("dh", "D").replace("gh", "G")
    w = w.replace("q", "k").replace("p", "f").replace("x", "ks")
    toks = []
    L = len(w)
    for i, c in enumerate(w):
        if c in "aeiouc":
            toks.append("_")
        elif c == "'":
            toks.append("3")
        elif c in "bdfhjklmnrstwyzXSTDGg":
            toks.append(c)
    # A3: final -eh/-ah  -> E (tā' marbūṭa)
    if len(toks) >= 2 and toks[-1] == "h" and toks[-2] == "_":
        toks[-1] = "E"
    if t_fix:  # djvu OCR: 't' between consonants is often a misread î (e.g. 'Btr' = Bîr)
        nt = []
        for i, c in enumerate(toks):
            if c == "t" and 0 < i < len(toks) - 1 and toks[i - 1] not in ("_",) and toks[i + 1] not in ("_",):
                continue
            nt.append(c)
        toks = nt
    # A4: collapse geminates (adjacent identical consonants without vowel between)
    out = []
    for c in toks:
        if c == "_":
            out.append(c)
            continue
        if out and out[-1] == c:
            continue
        out.append(c)
    return [c for c in out if c != "_"]

def palmer_variants(raw, gloss="", source="tess"):
    """Return list of (label, arabic token list, words) to compare."""
    words, generic = specific_words(raw, gloss)
    if not words:
        return [], generic
    cand = []
    seqs = [words] + ([[w] for w in words] if len(words) > 1 else [])
    for ws in seqs:
        fixes = [(False, False)]
        if source == "djvu":
            fixes += [(True, False), (False, True), (True, True)]
        for lf, tf in fixes:
            A = []
            for w in ws:
                A += lat_tokens(w, li_fix=lf, t_fix=tf)
            if A:
                cand.append((" ".join(ws), tuple(A)))
    # dedupe
    seen, out = set(), []
    for lab, A in cand:
        if (lab, A) not in seen:
            seen.add((lab, A))
            out.append((lab, A))
    return out, generic

def ar_str(A):
    return "-".join(AR_NAME.get(a, a) for a in A)

def heb_str(H):
    return "-".join(HEB_NAME[h] for h, _ in H)
