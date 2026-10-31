"""B2 calibration lines, candidate sets and the train/held-out split (rule fixed before any scoring).

Text: ETCBC dss 2.0.1 lines (etcbc_lines.json, same file and sha256 as round 1).
Column -> cuts used for scoring (cuts present in the bucket only; Puech 2006 radiograph captions via
research/text/letter_controls/controls_manifest.csv for I-X; cuts 19-23 = columns XI-XII per
research/text/plate_check.md, XII 10 at the 21/22 cut):
  I: 2 3 4 (cut 1 absent) | II: 5 6 | III: 7 8 | IV: 10 (9 absent) | V: 10 11 | VI: 11 (12 absent)
  VII, VIII: none (13-15 absent) | IX: 16 17 | X: 17 18 | XI: 19 20 21 | XII: 21 22 23
Undisputed word: no ETCBC flag, not Greek, and no row of research/text/edition_confusions/variants.csv
on that word (rows with a word span such as "1-2" mark every word of the span), at least 2 letters.
(Round 1 required a whole line without any variants.csv row; that leaves 15 lines of >= 6 letters in
the columns with cuts present, too few. readings.json citations are not used as a filter: its letter
disputes are in variants.csv.)
Eligible calibration line (all of):
  - column has at least one cut present;
  - no Greek on the line; not in research/text/plate_check.md (line-level, visually disputed lines);
  - not a target line (I 12, VII 11, IX 10, X 15, XII 10);
  - at least 6 letters, and at least 3 letters in undisputed words.
Words that are not undisputed keep their ETCBC text in every candidate (shared context).
Split:
  - the 25 round-1 calibration lines are exposed: TRAIN, whatever their column;
  - lines of columns with a missing cut (I, IV, VI) are TRAIN only (part of each line is unobservable);
  - the remaining eligible lines (columns II, III, V, IX, X, XI, XII) are sorted by (col, line) and
    permuted by numpy default_rng(20261031); the first half (floor) is TRAIN, the rest HELD-OUT.
Candidates per line (K = 6): the ETCBC truth + 5 single-letter substitutions, at letter positions inside
undisputed words only. Substitutable pairs are the rows of edition_confusions/confusions.csv with
count_places >= 3; all (position, partner) options are enumerated in reading order and 5 are drawn without replacement with weights equal to the pair rate,
rng default_rng(31102026 + 100*col + line). A substituted word-final letter takes its final form.
"""
import csv, json, os, re, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, '../../..'))
ROM = {'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5, 'VI': 6, 'VII': 7, 'VIII': 8, 'IX': 9, 'X': 10, 'XI': 11, 'XII': 12}
TOF = dict(zip('כמנפצ', 'ךםןףץ')); FROMF = {v: k for k, v in TOF.items()}
TARGETS = {(1, 12), (7, 11), (9, 10), (10, 15), (12, 10)}
COLCUTS = {1: [2, 3, 4], 2: [5, 6], 3: [7, 8], 4: [10], 5: [10, 11], 6: [11], 9: [16, 17], 10: [17, 18],
           11: [19, 20, 21], 12: [21, 22, 23]}
PARTIAL = {1, 4, 6}
K = 6
R1 = {(1, 8), (2, 15), (3, 3), (3, 6), (3, 10), (4, 5), (5, 10), (5, 11), (6, 5), (6, 6), (6, 9), (6, 10), (6, 12),
      (6, 13), (7, 7), (7, 13), (8, 7), (8, 11), (8, 16), (9, 9), (9, 13), (9, 16), (10, 2), (10, 4), (10, 14)}


def nletters(t):
    return sum(1 for ch in t if 'א' <= ch <= 'ת')


def disputed_words():
    V = list(csv.DictReader(open(f'{REPO}/research/text/edition_confusions/variants.csv')))
    out = set()
    for v in V:
        c, l = ROM[v['column']], int(v['line'])
        wi = [int(x) for x in re.findall(r'\d+', v['word_index'])]
        if len(wi) == 2 and '-' in v['word_index']: wi = list(range(wi[0], wi[1] + 1))
        for i in wi: out.add((c, l, i))
    return out


def eligible():
    """returns (col, line, text, mask) with mask[j] = True where character j may be substituted"""
    L = json.load(open(f'{HERE}/etcbc_lines.json'))
    varw = disputed_words()
    pc = {(ROM[a], int(b)) for a, b in re.findall(r'^\| *([IVX]+) (\d+)', open(f'{REPO}/research/text/plate_check.md').read(), re.M)}
    out = []
    for k, ws in L.items():
        c, l = map(int, k.split(':'))
        if c not in COLCUTS or (c, l) in TARGETS or (c, l) in pc: continue
        if any(w['greek'] for w in ws): continue
        parts, mask = [], []
        for i, w in enumerate(ws):
            if not w['t']: continue
            ok = (not w['flags']) and (c, l, i) not in varw and nletters(w['t']) >= 2
            if parts: parts.append(' '); mask.append(False)
            parts.append(w['t']); mask += [ok] * len(w['t'])
        t = ''.join(parts)
        if nletters(t) < 6 or sum(mask) < 3: continue
        out.append((c, l, t, mask))
    return sorted(out, key=lambda x: (x[0], x[1]))


def pairs():
    P = {}
    for r in csv.DictReader(open(f'{REPO}/research/text/edition_confusions/confusions.csv')):
        if int(r['count_places']) >= 3:
            a, b, rate = r['letter_1'], r['letter_2'], float(r['rate'])
            P.setdefault(a, []).append((b, rate)); P.setdefault(b, []).append((a, rate))
    return P


def subst(text, i, b):
    end = (i == len(text) - 1) or text[i + 1] == ' '
    b = FROMF.get(b, b)
    if end and b in TOF: b = TOF[b]
    return text[:i] + b + text[i + 1:]


def candidates(c, l, text, mask):
    P = pairs(); base = ''.join(FROMF.get(ch, ch) for ch in text)
    opts = [(i, b, rate) for i, ch in enumerate(base) if mask[i] for b, rate in P.get(ch, [])]
    rng = np.random.default_rng(31102026 + 100 * c + l)
    w = np.array([o[2] for o in opts]); w = w / w.sum()
    pick = rng.choice(len(opts), size=min(K - 1, len(opts)), replace=False, p=w)
    cands = [text]
    for j in sorted(pick):
        i, b, _ = opts[j]
        s = subst(text, i, b)
        if s not in cands: cands.append(s)
    return cands


def split(lines):
    fixed = {}
    pool = []
    for c, l, t, _ in lines:
        if (c, l) in R1: fixed[(c, l)] = 'train_r1'
        elif c in PARTIAL: fixed[(c, l)] = 'train_partial'
        else: pool.append((c, l))
    rng = np.random.default_rng(20261031); perm = rng.permutation(len(pool))
    ntr = len(pool) // 2
    for j, i in enumerate(perm):
        fixed[pool[i]] = 'train' if j < ntr else 'heldout'
    return fixed


if __name__ == '__main__':
    Ls = eligible(); sp = split(Ls)
    rows = []
    for c, l, t, m in Ls:
        cs = candidates(c, l, t, m)
        rows.append(dict(col=c, line=l, split=sp[(c, l)], cuts=COLCUTS[c], truth=cs[0], candidates=cs))
    json.dump(rows, open(f'{HERE}/calibration_items2.json', 'w'), ensure_ascii=False, indent=1)
    from collections import Counter
    print(Counter(r['split'] for r in rows))
    print('heldout', [(r['col'], r['line'], len(r['candidates'])) for r in rows if r['split'] == 'heldout'])
