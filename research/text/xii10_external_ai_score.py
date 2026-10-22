"""Score the external AI transcription against the ETCBC base text (rules fixed in a0245b3).

Controls: letters of columns XI and XII, excluding XII 8-12, with candidate_undisputed true.
Each model line is aligned (local alignment) to the reference line it fits best.
"""
import csv, re, sys, json, collections

FIN = str.maketrans("ךםןףץ", "כמנפצ")
REF = sys.argv[1]
OUT = sys.argv[2]

rows = list(csv.DictReader(open(REF, encoding="utf-8")))
ref = collections.OrderedDict()
for r in rows:
    col, ln = r["ref"].split()
    if col not in ("XI", "XII"):
        continue
    key = f"{col} {int(ln)}"
    ref.setdefault(key, []).append((int(r["word_index"]), int(r["char_index"]),
                                    r["letter"].translate(FIN),
                                    r["candidate_undisputed"].strip().lower() in ("true", "1")))
for k in ref:
    ref[k].sort()
    ref[k] = [(c, u) for _, _, c, u in ref[k]]
EXCL = {f"XII {i}" for i in range(8, 13)}


def parse(s):
    s = s.replace("(", "").replace(")", "")
    toks, i = [], 0
    while i < len(s):
        ch = s[i]
        if ch == "[":
            j = s.index("]", i)
            inner = s[i + 1:j]
            toks.append(None if inner.strip() == "?" else frozenset(x.translate(FIN) for x in inner.split("/") if x))
            i = j + 1
        elif "א" <= ch <= "ת":
            toks.append(frozenset(ch.translate(FIN)))
            i += 1
        else:
            i += 1
    return toks


def align(a, b):
    """Smith-Waterman; a = model tokens, b = reference letters. Returns score, pairs [(i,j)]."""
    n, m = len(a), len(b)
    H = [[0] * (m + 1) for _ in range(n + 1)]
    P = [[None] * (m + 1) for _ in range(n + 1)]
    best = (0, 0, 0)
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            t = a[i - 1]
            if t is None:
                s = 0
            elif b[j - 1][0] in t:
                s = 2 if len(t) == 1 else 1
            else:
                s = -1
            opts = [(0, None), (H[i - 1][j - 1] + s, "d"), (H[i - 1][j] - 2, "u"), (H[i][j - 1] - 2, "l")]
            H[i][j], P[i][j] = max(opts, key=lambda x: x[0])
            if H[i][j] > best[0]:
                best = (H[i][j], i, j)
    sc, i, j = best
    pairs = []
    while i > 0 and j > 0 and P[i][j]:
        if P[i][j] == "d":
            pairs.append((i - 1, j - 1)); i -= 1; j -= 1
        elif P[i][j] == "u":
            i -= 1
        else:
            j -= 1
    return sc, pairs[::-1]


text = open(sys.argv[3], encoding="utf-8").read()
lines = []
img = None
for raw in text.splitlines():
    m = re.match(r"^(img_\d\d)\s*$", raw.strip())
    if m:
        img = m.group(1); continue
    m = re.match(r"^L(\d+):\s*(.*?)\s*\((high|medium|low)\)\s*$", raw.strip())
    if m and img:
        lines.append((img, int(m.group(1)), m.group(2), m.group(3)))

uniq = collections.OrderedDict()
for img, n, s, conf in lines:
    uniq.setdefault(s, []).append((img, n, conf))

res = {"lines_total": len(lines), "lines_distinct": len(uniq), "aligned": [], "unaligned": [], "xii8_12": []}
tot = collections.Counter()
hi_wrong = []
for s, where in uniq.items():
    toks = parse(s)
    best = None
    for k, b in ref.items():
        sc, pairs = align(toks, b)
        if best is None or sc > best[0]:
            best = (sc, k, pairs)
    sc, k, pairs = best
    singles = sum(1 for i, j in pairs if toks[i] and len(toks[i]) == 1 and ref[k][j][0] in toks[i])
    confs = sorted({c for _, _, c in where})
    entry = {"text": s, "where": [f"{a} L{b}" for a, b, _ in where], "conf": confs, "ref": k, "score": sc}
    if sc < 6 or singles < 3:
        res["unaligned"].append(entry); continue
    if k in EXCL:
        res["xii8_12"].append(entry); continue
    c = collections.Counter()
    for i, j in pairs:
        t = toks[i]; letter, ctrl = ref[k][j]
        if t is None or not ctrl:
            continue
        c["attempted"] += 1
        if len(t) == 1 and letter in t:
            c["exact"] += 1
        elif letter in t:
            c["in_set"] += 1
        else:
            c["wrong"] += 1
            if "high" in confs:
                hi_wrong.append(f"{k}: reference {letter}, model {'/'.join(sorted(t))} in '{s}'")
    entry["counts"] = dict(c)
    tot.update(c)
    res["aligned"].append(entry)

res["totals_controls"] = dict(tot)
res["high_conf_wrong"] = hi_wrong
json.dump(res, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: res[k] for k in ("lines_total", "lines_distinct", "totals_controls")}, ensure_ascii=False))
print("aligned:", len(res["aligned"]), "unaligned:", len(res["unaligned"]), "to XII 8-12:", len(res["xii8_12"]))
