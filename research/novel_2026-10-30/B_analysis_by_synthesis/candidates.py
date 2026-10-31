"""Calibration lines, their candidate sets, and the train/held-out split (frozen rule).
Eligible undisputed line (cols I-X only): no ETCBC flag or Greek word on the line; no row of
research/text/edition_confusions/variants.csv on the line (any class); not in research/text/plate_check.md;
not cited by any text/readings.json record; not a target line (I 12, VII 11, IX 10, X 15; XII never).
Candidates per line: the ETCBC text (truth) + K-1 = 5 single-letter substitutions. Substitutable pairs =
rows of edition_confusions/confusions.csv with count_places >= 3 (shape pairs; yod/waw kept apart there).
All (position, partner) substitutions of the line are enumerated in reading order; 5 are drawn without
replacement by numpy default_rng(20261030 + 100*col + line), weights = the pair's confusion rate. Word-final
letters take final forms (כמנפצ -> ךםןףץ) and final forms map back.
Split: lines sorted by (col,line); rng(20261030).permutation; first 12 = TRAIN, rest = HELD-OUT."""
import csv, json, os, re, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, '../../..'))
ROM = {'I':1,'II':2,'III':3,'IV':4,'V':5,'VI':6,'VII':7,'VIII':8,'IX':9,'X':10,'XI':11,'XII':12}
TOF = dict(zip('כמנפצ', 'ךםןףץ')); FROMF = {v: k for k, v in TOF.items()}
TARGETS = {(1, 12), (7, 11), (9, 10), (10, 15)}
K = 6
def eligible():
    L = json.load(open(f'{HERE}/etcbc_lines.json'))
    V = list(csv.DictReader(open(f'{REPO}/research/text/edition_confusions/variants.csv')))
    var = {(ROM[v['column']], int(v['line'])) for v in V}
    pc = {(ROM[a], int(b)) for a, b in re.findall(r'^\| *([IVX]+) (\d+)', open(f'{REPO}/research/text/plate_check.md').read(), re.M)}
    rj = set()
    for r in json.load(open(f'{REPO}/text/readings.json')):
        for x in [r] + r.get('also', []):
            mm = re.match(r'([IVX]+) (\d+)', x.get('line', '') or '')
            if mm: rj.add((ROM[mm.group(1)], int(mm.group(2))))
    out = []
    for k, ws in L.items():
        c, l = map(int, k.split(':'))
        if c > 10 or (c, l) in TARGETS: continue
        if any(w['flags'] or w['greek'] for w in ws): continue
        if (c, l) in var or (c, l) in pc or (c, l) in rj: continue
        out.append((c, l, ' '.join(w['t'] for w in ws)))
    return sorted(out)
def pairs():
    P = {}
    for r in csv.DictReader(open(f'{REPO}/research/text/edition_confusions/confusions.csv')):
        if int(r['count_places']) >= 3:
            a, b, rate = r['letter_1'], r['letter_2'], float(r['rate'])
            P.setdefault(a, []).append((b, rate)); P.setdefault(b, []).append((a, rate))
    return P
def subst(text, i, b):
    """replace letter i by b; a substituted word-final letter takes its final form if it has one,
    a substituted non-final position takes the medial form. Unsubstituted letters stay as ETCBC prints them
    (e.g. the abbreviation ככ keeps two medial kafs)."""
    end = (i == len(text) - 1) or text[i + 1] == ' '
    b = FROMF.get(b, b)
    if end and b in TOF: b = TOF[b]
    return text[:i] + b + text[i + 1:]
def candidates(c, l, text):
    P = pairs(); text = text.strip(); base = ''.join(FROMF.get(ch, ch) for ch in text)
    opts = []
    for i, ch in enumerate(base):
        for b, rate in P.get(ch, []):
            opts.append((i, b, rate))
    rng = np.random.default_rng(20261030 + 100 * c + l)
    w = np.array([o[2] for o in opts]); w = w / w.sum()
    pick = rng.choice(len(opts), size=min(K - 1, len(opts)), replace=False, p=w)
    truth = text
    cands = [truth]
    for j in sorted(pick):
        i, b, _ = opts[j]
        s = subst(text, i, b)
        if s not in cands: cands.append(s)
    return cands
def split(lines):
    rng = np.random.default_rng(20261030); perm = rng.permutation(len(lines))
    tr = {lines[i][:2] for i in perm[:12]}
    return ['train' if x[:2] in tr else 'heldout' for x in lines]
if __name__ == '__main__':
    Ls = eligible(); sp = split(Ls)
    rows = []
    for (c, l, t), s in zip(Ls, sp):
        cs = candidates(c, l, t)
        rows.append(dict(col=c, line=l, split=s, truth=cs[0], candidates=cs))
        print(c, l, s, cs)
    json.dump(rows, open(f'{HERE}/calibration_items.json', 'w'), ensure_ascii=False, indent=1)
