#!/usr/bin/env python3
"""W2-D Part B: how name-like are the seven Copper Scroll Greek groups as openings of
Jewish personal names (Ilan, Lexicon I, Palestine 330 BCE-200 CE), frequency-weighted?

usage: python3 -I ilan_initials.py ilan_counts.csv ilan_xlsx OUTDIR [--het-chi]
"""
import csv, sys, json, random, unicodedata, itertools, collections, re
import openpyxl

counts_csv, xlsx, outdir = sys.argv[1:4]
HET_CHI = "--het-chi" in sys.argv
random.seed(20261007)

GREEK = "ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ"
TARGETS = ["ΚΕΝ", "ΧΑΓ", "ΗΝ", "ΘΕ", "ΔΙ", "ΤΡ", "ΣΚ"]
SENS = {"ΘΕ": ["ΞΕ"], "ΤΡ": ["ΤΡΙ"], "ΣΚ": ["ΙΣΚ", "ΧΚ", "ΞΚ"]}
LENGTHS = [len(t) for t in TARGETS]

# Ilan Tables 5, 7, 8 (printed pp. 56-57) override parsed counts
TABLE = {"Simon": 257, "Joseph": 231, "Judah": 179, "Eleazar": 177, "Yohanan": 128, "Joshua": 103,
         "Hananiah": 85, "Jonathan": 75, "Mattathias": 63, "Menahem": 46, "Jacob": 45, "Hanan": 39,
         "Alexander": 31, "Dositheus": 31, "Zachariah": 31, "Ishmael": 31, "Levi": 29, "Saul": 29,
         "Onias": 27, "Samuel": 26, "Ezekiah": 26, "Mariam": 80, "Salome": 63, "Shelamzion": 25,
         "Martha": 20, "Joanna": 12, "Shiphra": 12, "Berenice": 10, "Sarah": 9, "Imma": 7, "Mara": 7}
# hand-verified counts for names relevant to the target checks (filled after reading the entries; see report)
HAND = {}
EXTRA = {}
HANDMODE = "--hand" in sys.argv
if HANDMODE:
    HAND = json.load(open(outdir + "/hand_counts.json"))
    EXTRA = json.load(open(outdir + "/extra_attested.json"))


def gnorm(s):
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.upper().replace("ς", "Σ").replace("Ϲ", "Σ").replace("ϲ", "Σ")
    return "".join(c for c in s if c in GREEK)

# ---------- transliteration to Greek opening alternatives ----------
LAT_DI = [("th", ["Θ"]), ("ch", ["Χ"]), ("ph", ["Φ"]), ("ps", ["Ψ"]), ("rh", ["Ρ"]), ("ae", ["ΑΙ"]),
          ("oe", ["ΟΙ"]), ("eu", ["ΕΥ"]), ("au", ["ΑΥ"]), ("ou", ["ΟΥ"]), ("ei", ["ΕΙ"]), ("qu", ["ΚΟΥ", "ΚΥ"]),
          ("kh", ["Χ"])]
LAT_1 = {"a": ["Α"], "b": ["Β"], "c": ["Κ"], "d": ["Δ"], "e": ["Ε", "Η"], "f": ["Φ"], "g": ["Γ"], "h": [""],
         "i": ["Ι"], "j": ["Ι"], "k": ["Κ"], "l": ["Λ"], "m": ["Μ"], "n": ["Ν"], "o": ["Ο", "Ω"], "p": ["Π"],
         "q": ["Κ"], "r": ["Ρ"], "s": ["Σ"], "t": ["Τ"], "u": ["Υ", "ΟΥ"], "v": ["ΟΥ", "Β"], "w": ["ΟΥ"],
         "x": ["Ξ"], "y": ["Υ"], "z": ["Ζ"]}
HEB_DI = [("yeho", ["ΙΩ", "ΙΗ", "ΙΕ", "ΙΟ"]), ("sh", ["Σ"]), ("ts", ["Σ", "Τ"]), ("tz", ["Σ", "Τ"]),
          ("kh", ["Χ", "Κ"]), ("ch", ["Χ", "Κ"]), ("ph", ["Φ"]), ("th", ["Θ", "Τ"])]
HEB_1 = {"a": ["Α"], "b": ["Β"], "c": ["Κ", "Χ"], "d": ["Δ"], "e": ["Ε", "Η"], "f": ["Φ"], "g": ["Γ"],
         "h": [""], "i": ["Ι"], "j": ["Ι"], "k": ["Χ", "Κ"], "l": ["Λ"], "m": ["Μ"], "n": ["Ν"],
         "o": ["Ο", "Ω"], "p": ["Π", "Φ"], "q": ["Κ"], "r": ["Ρ"], "s": ["Σ"], "t": ["Τ", "Θ"],
         "u": ["ΟΥ", "Υ"], "v": ["Β", "ΟΥ"], "w": ["ΟΥ"], "x": ["Ξ"], "y": ["Ι"], "z": ["Ζ"], "'": [""],
         "’": [""]}


def openings(name, tag, het_chi=False, maxlen=3):
    s = name.lower().replace("-", "").replace(" ", "")
    heb = tag.startswith("B") or tag.startswith("S-H") or tag.startswith("S/H")
    di, one = (HEB_DI, HEB_1) if heb else (LAT_DI, LAT_1)
    out = {""}
    i = 0
    first = True
    while i < len(s) and min(len(o) for o in out) < maxlen:
        alts = None
        for d, a in di:
            if s.startswith(d, i):
                alts = a; i += len(d); break
        if alts is None:
            ch = s[i]; i += 1
            alts = one.get(ch, [""])
            if heb and ch == "h" and first and het_chi:
                alts = ["", "Χ"]
        first = False
        out = {(o + a) for o in out for a in alts}
    return {o[:maxlen] for o in out if o}


def canonical(name, tag):
    s = name.lower().replace("-", "").replace(" ", "")
    heb = tag.startswith("B") or tag.startswith("S-H") or tag.startswith("S/H")
    di, one = (HEB_DI, HEB_1) if heb else (LAT_DI, LAT_1)
    out = ""; i = 0
    while i < len(s):
        a = None
        for d, al in di:
            if s.startswith(d, i):
                a = al[0]; i += len(d); break
        if a is None:
            a = one.get(s[i], [""])[0]; i += 1
        out += a
    return out

# ---------- load Ilan names + weights ----------
names = []
for r in csv.DictReader(open(counts_csv, encoding="utf-8")):
    n = r["name"]; tag = r["tag"]; b = int(r["bearers_parsed"] or 0)
    src = "parsed"
    if n in TABLE:
        b = TABLE[n]; src = "table"
    if n in HAND:
        b = HAND[n]; src = "hand"
    if b <= 0:
        b = 1; src = "min1"
    names.append({"name": n, "tag": tag, "w": b, "src": src, "pages": r["pages"]})

# ---------- xlsx attested Greek variants ----------
wb = openpyxl.load_workbook(xlsx, read_only=True)
ws = wb["Master list"]
rows = list(ws.iter_rows(values_only=True))
xv = {}
for r in rows[3:]:
    if not r or not r[0]:
        continue
    vs = str(r[3] or "")
    good = []
    for v in [x.strip() for x in vs.split(",")]:
        if not v:
            continue
        if not ("Ͱ" <= v[0] <= "Ͽ" or "ἀ" <= v[0] <= "῿"):
            continue
        base = unicodedata.normalize("NFD", v)[0]
        if not base.isupper():
            continue  # fragment / lower-case start
        g = gnorm(v)
        if len(g) >= 2:
            good.append(g)
    if good:
        xv.setdefault(str(r[0]).strip(), []).extend(good)

GREEKTAG = ("G", "S-G")
for d in names:
    rule = openings(d["name"], d["tag"], het_chi=HET_CHI)
    att = {g[:3] for g in xv.get(d["name"], [])} | {gnorm(x)[:3] for x in EXTRA.get(d["name"], [])}
    d["att"] = sorted(att)
    if d["tag"].split("/")[0] in GREEKTAG:
        att_u2 = att | {canonical(d["name"], d["tag"])[:3]}
    else:
        att_u2 = att
    d["u1"] = rule | att
    d["u2"] = att_u2
    d["canon"] = (xv[d["name"]][0] if d["name"] in xv else canonical(d["name"], d["tag"]))


def prefix_table(key):
    tot = 0; tab = collections.Counter(); ntab = collections.Counter(); nn = 0
    for d in names:
        ops = d[key]
        if not ops:
            continue
        tot += d["w"]; nn += 1
        prefs = set()
        for o in ops:
            for L in (1, 2, 3):
                if len(o) >= L:
                    prefs.add(o[:L])
        for p in prefs:
            tab[p] += d["w"]; ntab[p] += 1
    return tab, ntab, tot, nn

res = {"het_chi_sensitivity": HET_CHI}
tabs = {}
for key in ("u1", "u2"):
    tab, ntab, tot, nn = prefix_table(key)
    tabs[key] = (tab, tot)
    res[key] = {"total_weight": tot, "n_names": nn, "groups": {}}
    for g in TARGETS + sum(SENS.values(), []):
        matches = [(d["name"], d["tag"], d["w"], d["src"], d["pages"]) for d in names
                   if any(o.startswith(g) for o in d[key])]
        res[key]["groups"][g] = {"weighted_bearers": tab.get(g, 0), "p_name": tab.get(g, 0) / tot,
                                 "p_name_vs_3595": tab.get(g, 0) / 3595, "n_names": ntab.get(g, 0),
                                 "share_names": ntab.get(g, 0) / nn, "matches": matches}

# ---------- letter-frequency nulls ----------
uni = collections.Counter(); first = collections.Counter()
for d in names:
    c = d["canon"]
    for ch in c:
        if ch in GREEK:
            uni[ch] += d["w"]
    if c and c[0] in GREEK:
        first[c[0]] += d["w"]
U = sum(uni.values()); F = sum(first.values())
f1 = {L: uni[L] / U for L in GREEK}
fF = {L: first[L] / F for L in GREEK}
res["letter_freq_N1"] = f1
res["first_letter_freq_N2"] = fF


def pnull(g, model):
    p = 1.0
    for i, ch in enumerate(g):
        if model == "uniform":
            p *= 1 / 24
        elif model == "N1":
            p *= f1[ch]
        elif model == "N2":
            p *= (fF[ch] if i == 0 else f1[ch])
    return p

for key in ("u1", "u2"):
    for g, v in res[key]["groups"].items():
        for m in ("N1", "N2", "uniform"):
            pn = pnull(g, m)
            v["p_null_" + m] = pn
            v["ratio_" + m] = (v["p_name"] / pn) if pn > 0 else None


def draw(model, L):
    letters = list(GREEK)
    out = ""
    for i in range(L):
        if model == "uniform":
            out += random.choice(letters)
        else:
            wts = [fF[c] if (model == "N2" and i == 0) else f1[c] for c in letters]
            out += random.choices(letters, weights=wts)[0]
    return out

NSIM = 100000
for key in ("u1", "u2"):
    tab, tot = tabs[key]
    obsK = sum(1 for g in TARGETS if tab.get(g, 0) > 0)
    obsW = sum(tab.get(g, 0) / tot for g in TARGETS)
    res[key]["observed_K"] = obsK; res[key]["observed_W"] = obsW
    for model in ("N1", "N2", "uniform"):
        Ks = []; Ws = []
        # speed: pre-draw
        for _ in range(NSIM):
            gs = [draw(model, L) for L in LENGTHS]
            Ks.append(sum(1 for g in gs if tab.get(g, 0) > 0))
            Ws.append(sum(tab.get(g, 0) / tot for g in gs))
        Ws_sorted = sorted(Ws)
        res[key]["mc_" + model] = {
            "p_K_ge_obs": sum(1 for k in Ks if k >= obsK) / NSIM,
            "p_W_ge_obs": sum(1 for w in Ws if w >= obsW) / NSIM,
            "K_mean": sum(Ks) / NSIM, "W_mean": sum(Ws) / NSIM,
            "W_median": Ws_sorted[NSIM // 2], "K_dist": dict(collections.Counter(Ks))}
        # per-group percentile: P(random group of same length has p_name >= observed)
        pg = {}
        for g in TARGETS:
            L = len(g)
            sims = [tab.get(draw(model, L), 0) for _ in range(20000)]
            pg[g] = sum(1 for s in sims if s >= tab.get(g, 0)) / 20000
        res[key]["mc_" + model]["per_group_p_ge"] = pg

suffix = ("_hetchi" if HET_CHI else "") + ("_hand" if HANDMODE else "")
json.dump(res, open(outdir + f"/initials_results{suffix}.json", "w"), ensure_ascii=False, indent=1)
with open(outdir + f"/initials_names{suffix}.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["name", "tag", "weight", "weight_source", "pages", "u1_openings", "u2_openings", "xlsx_attested", "canonical"])
    for d in names:
        w.writerow([d["name"], d["tag"], d["w"], d["src"], d["pages"], " ".join(sorted(d["u1"])), " ".join(sorted(d["u2"])),
                    " ".join(d["att"]), d["canon"]])
# console summary
for key in ("u1", "u2"):
    r = res[key]
    print(f"== {key}: total weight {r['total_weight']}, names {r['n_names']}, K={r['observed_K']}, W={r['observed_W']:.4f}")
    for g in TARGETS + sum(SENS.values(), []):
        v = r["groups"][g]
        print(f"  {g:4s} wb={v['weighted_bearers']:5d} p={v['p_name']:.4f} names={v['n_names']:3d}  r_N1={v['ratio_N1'] if v['ratio_N1'] is None else round(v['ratio_N1'],2)}  matches={[m[0]+':'+str(m[2]) for m in v['matches']][:12]}")
    for m in ("N1", "N2", "uniform"):
        mc = r["mc_" + m]
        print(f"  MC {m}: P(K>=obs)={mc['p_K_ge_obs']:.4f} K_mean={mc['K_mean']:.2f}  P(W>=obs)={mc['p_W_ge_obs']:.4f} W_mean={mc['W_mean']:.4f} W_med={mc['W_median']:.4f}  per-group={mc['per_group_p_ge']}")
