"""B4 calibration lines, train/held-out split and candidate sets (rule fixed before any score).

Text: ETCBC dss 2.0.1 lines (etcbc_lines.json, same file as round 1 and B2).
Undisputed word (B2 rule): no ETCBC flag, not Greek, no row of research/text/edition_confusions/variants.csv on the
word (a word span such as "1-2" marks every word in it), at least 2 letters.
Eligible line (all of):
  - column has an A2-accepted cut/column pair (I, II, III, V, IX, X, XII);
  - no Greek on the line; not in research/text/plate_check.md; not a target line (I 12, VII 11, IX 10, X 15, XII 10);
  - at least 6 letters and at least 3 letters in undisputed words (B2 rule);
  - at least MIN_POS "placeable positions": letters inside undisputed words that have a W2F verified box placed on an
    accepted pair (b4lib.place_letters).
Split (new for B4): eligible lines sorted by (col, line), permuted by numpy default_rng(SPLIT_SEED); the first half
(floor) TRAIN, the rest HELD-OUT. No line is forced into TRAIN.
Training letters: every placed W2F letter that is not on a HELD-OUT line and not on a target line.
Template availability: a letter form (final forms separate) is "modelled" if it has >= MIN_TRAIN training letters.
Candidates per line: the ETCBC truth + up to 5 single-letter substitutions at placeable positions whose truth form is
modelled; partners from edition_confusions/confusions.csv rows with count_places >= 3 (B2 rule) whose substituted form
(final form at word end) is modelled. All (position, partner) options in reading order; up to 5 drawn without
replacement with weights equal to the pair rate, rng default_rng(CAND_SEED + 100*col + line).
Lines with no option are dropped after the split (recorded).
"""
import csv, json, os, re, collections
import numpy as np
import b4lib as B

TARGETS = {(1, 12), (7, 11), (9, 10), (10, 15), (12, 10)}
MIN_POS = 2
MIN_TRAIN = 4
SPLIT_SEED = 4310_2026
CAND_SEED = 35102026
K = 6


def nletters(t):
    return sum(1 for ch in t if "א" <= ch <= "ת")


def disputed_words():
    out = set()
    for v in csv.DictReader(open(f"{B.REPO}/research/text/edition_confusions/variants.csv", encoding="utf-8")):
        c, l = B.ROM[v["column"]], int(v["line"])
        wi = [int(x) for x in re.findall(r"\d+", v["word_index"])]
        if len(wi) == 2 and "-" in v["word_index"]:
            wi = list(range(wi[0], wi[1] + 1))
        for i in wi:
            out.add((c, l, i))
    return out


def plate_check_lines():
    t = open(f"{B.REPO}/research/text/plate_check.md", encoding="utf-8").read()
    return {(B.ROM[a], int(b)) for a, b in re.findall(r"^\| *([IVX]+) (\d+)", t, re.M)}


def pairs():
    P = {}
    for r in csv.DictReader(open(f"{B.REPO}/research/text/edition_confusions/confusions.csv", encoding="utf-8")):
        if int(r["count_places"]) >= 3:
            a, b, rate = r["letter_1"], r["letter_2"], float(r["rate"])
            P.setdefault(a, []).append((b, rate)); P.setdefault(b, []).append((a, rate))
    return P


def line_text(ws, c, l, varw):
    """B2-style line string; per character: (word index, char index, undisputed flag) or None for spaces."""
    parts, meta = [], []
    for i, w in enumerate(ws):
        if not w["t"]:
            continue
        ok = (not w["flags"]) and (c, l, i) not in varw and nletters(w["t"]) >= 2
        if parts:
            parts.append(" "); meta.append(None)
        parts.append(w["t"]); meta += [(i, j, ok) for j in range(len(w["t"]))]
    return "".join(parts), meta


def subst(text, i, b):
    end = (i == len(text) - 1) or text[i + 1] == " "
    b = B.FROMF.get(b, b)
    if end and b in B.TOF:
        b = B.TOF[b]
    return text[:i] + b + text[i + 1:]


def build(placed_letters):
    """placed_letters: output of b4lib.place_letters (all W2F letters, with 'placed')."""
    L = B.etcbc_lines()
    varw = disputed_words(); pc = plate_check_lines()
    cols = {B.ROM[col] for (_, col) in B.a2_accepted()}
    pos = {(r["col"], r["line"], r["wi"], r["ci"]): r for r in placed_letters if r["placed"]}
    lines = []
    for k, ws in L.items():
        c, l = map(int, k.split(":"))
        if c not in cols or (c, l) in TARGETS or (c, l) in pc or any(w["greek"] for w in ws):
            continue
        t, meta = line_text(ws, c, l, varw)
        und = [m is not None and m[2] for m in meta]
        if nletters(t) < 6 or sum(und) < 3:
            continue
        pp = [j for j, m in enumerate(meta) if m is not None and m[2] and (c, l, m[0], m[1]) in pos]
        if len(pp) < MIN_POS:
            continue
        lines.append(dict(col=c, line=l, text=t, meta=meta, ppos=pp))
    lines.sort(key=lambda d: (d["col"], d["line"]))
    perm = np.random.default_rng(SPLIT_SEED).permutation(len(lines))
    ntr = len(lines) // 2
    for j, i in enumerate(perm):
        lines[i]["split"] = "train" if j < ntr else "heldout"
    held = {(d["col"], d["line"]) for d in lines if d["split"] == "heldout"}
    train_letters = [r for r in placed_letters if r["placed"] and (r["col"], r["line"]) not in held
                     and (r["col"], r["line"]) not in TARGETS]
    cnt = collections.Counter(r["letter"] for r in train_letters)
    modelled = {ch for ch, n in cnt.items() if n >= MIN_TRAIN}
    P = pairs()
    items, dropped = [], []
    for d in lines:
        c, l, t = d["col"], d["line"], d["text"]
        opts = []
        for j in d["ppos"]:
            if t[j] not in modelled:
                continue
            base = B.FROMF.get(t[j], t[j])
            for b, rate in P.get(base, []):
                s = subst(t, j, b)
                if s[j] in modelled:
                    opts.append((j, s[j], rate))
        if not opts:
            dropped.append((c, l, d["split"], "no modelled option")); continue
        rng = np.random.default_rng(CAND_SEED + 100 * c + l)
        w = np.array([o[2] for o in opts]); w = w / w.sum()
        pick = rng.choice(len(opts), size=min(K - 1, len(opts)), replace=False, p=w)
        comps = []
        for q in sorted(pick):
            j, b, _ = opts[q]
            m = d["meta"][j]
            comps.append(dict(pos=j, wi=m[0], ci=m[1], truth=t[j], alt=b, text=subst(t, j, b)))
        items.append(dict(col=c, line=l, split=d["split"], truth=t, n_placeable=len(d["ppos"]),
                          n_options=len(opts), competitors=comps))
    return items, dropped, sorted(modelled), dict(cnt), train_letters


if __name__ == "__main__":
    acc = B.a2_accepted()
    rows, _ = B.w2f_letters()
    pl = B.place_letters(rows, acc)
    items, dropped, modelled, cnt, tr = build(pl)
    print("items", collections.Counter(i["split"] for i in items), "dropped", dropped)
    print("modelled", "".join(modelled), "train letters", len(tr))
    print(sorted(cnt.items(), key=lambda kv: -kv[1]))
    for i in items:
        if i["split"] == "train":
            print(i["col"], i["line"], i["n_placeable"], i["n_options"], [(c["truth"], c["alt"]) for c in i["competitors"]])
    print("heldout lines", [(i["col"], i["line"], len(i["competitors"]), len({c["pos"] for c in i["competitors"]}))
                            for i in items if i["split"] == "heldout"])
