"""B3 new calibration lines, their truth sets and decoy sets (rule fixed before any new line is scored).

Text: round-1 etcbc_lines.json (verbatim copy). The line string is formed exactly as round 1 forms it
(' '.join of the ETCBC word texts, stripped), so an empty ETCBC word leaves a double space, as in round 1.

Scope (round 1): columns I-X; cuts and orientation search as round-1 abs_score.COL_CUTS (all these cuts have
registered preview stacks; column I uses cuts 2-4 because cut 1 has no lit frame, as in round 1).

Undisputed word (word-level rule, after B2 items2.py): ETCBC word with no flag, not Greek, at least 2 letters,
and no row of research/text/edition_confusions/variants.csv on it (a word span such as "1-2" marks every word
of the span; a row with no word index marks every word of its line).

Eligible new line (all of):
  - column I-X; not a target line (I 12, VII 11, IX 10, X 15);
  - not one of round 1's 25 calibration lines (calibration_items.json);
  - not a template-source line: VII 7-11 (round-1 glyph templates were traced from these lines on strip 13);
  - not named in the first cell of any table row of research/text/plate_check.md (all "COL n" and
    "COL n-m" references in that cell; round 1 and B2 parsed only the first reference);
  - no Greek word on the line;
  - at least 6 letters, and at least 3 letters in undisputed words.

Truth set: round-1 candidates.candidates() generator, unchanged except for ONE change needed by the word
rule: the enumerated (position, partner) options are restricted to letter positions inside undisputed words.
K = 6, pairs = confusions.csv rows with count_places >= 3, weights = pair rate, draws without replacement
by numpy default_rng(20261030 + 100*col + line), final-form rule via round-1 subst().

Decoy set (mirrored; see PROTOCOL_FROZEN.md for why this refines the generator-only version):
  - decoy index j* = numpy default_rng(20261031 + 100*col + line).integers(m), m = number of variants;
    decoy D = variant j* (D differs from the truth T at one position p0);
  - decoy set = [D, T] + [D with variant j's substitution applied, for every j != j*, in generator order].
    Every member is a one-letter confusion-pair substitution of D drawn by the same generator. The set has
    the same number of variants per position as the truth set, so the exact null of 'decoy first' equals
    the exact null of 'truth first' for that line.

Wrong-column control (frozen): the truth set of line (c, l) is also scored, unchanged, by
abs_score.score_line(c', l*, ...) with c' = c + 5 for c <= 5 and c - 5 for c >= 6, l* = min(l, NLINES[c']).
Pairs I-VI, II-VII, III-VIII, IV-IX, V-X share no cut, so the scored image holds none of line (c, l), in either
orientation.
(Superseded exploratory design, kept for the record: wrong line l' = l + 5 if l + 5 <= N else l - 5 in the same
column. Because the registration also searches the 180-degree orientation, its window at l' can fall on line l
itself in the flipped strip; on round-1 line IV 5 it did, exactly. Only the exploratory run used it.)

Exact null of 'centre first' for one set: product over varied positions of 1/(a+1), a = number of variants
at that position (computed from the strings)."""
import csv, json, os, re, sys, numpy as np
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, '../../..'))
sys.path.insert(0, HERE)
import candidates as C   # round-1 generator (verbatim): pairs(), subst(), TOF, FROMF, K, ROM

R1_LINES = {(x['col'], x['line']) for x in json.load(open(f'{HERE}/calibration_items.json'))}
TARGETS = {(1, 12), (7, 11), (9, 10), (10, 15)}
TEMPLATE_SOURCE = {(7, l) for l in range(7, 12)}
COL_CUTS = {1: [2, 3, 4], 2: [5, 6], 3: [7, 8], 4: [9, 10], 5: [10, 11], 6: [11, 12], 7: [13, 14], 8: [15],
            9: [16, 17], 10: [17, 18]}   # = round-1 abs_score.COL_CUTS for I-X


def nletters(t):
    return sum(1 for ch in t if 'א' <= ch <= 'ת')


def plate_check_lines():
    out = set()
    for row in open(f'{REPO}/research/text/plate_check.md', encoding='utf-8'):
        if not row.startswith('|'): continue
        cell = row.split('|')[1]
        for col, a, b in re.findall(r'\b([IVX]+) (\d+)(?:[–-](\d+))?', cell):
            if col not in C.ROM: continue
            for l in range(int(a), int(b or a) + 1): out.add((C.ROM[col], l))
    return out


def disputed_words(L):
    out = set()
    for v in csv.DictReader(open(f'{REPO}/research/text/edition_confusions/variants.csv')):
        c, l = C.ROM[v['column']], int(v['line'])
        wi = [int(x) for x in re.findall(r'\d+', v['word_index'])]
        if not wi: wi = list(range(len(L.get(f'{c}:{l}', []))))
        elif len(wi) == 2 and '-' in v['word_index']: wi = list(range(wi[0], wi[1] + 1))
        for i in wi: out.add((c, l, i))
    return out


def line_text_mask(c, l, ws, varw):
    """round-1 text (' '.join, strip) and a per-character substitutable mask"""
    parts, mask = [], []
    for i, w in enumerate(ws):
        if i: parts.append(' '); mask.append(False)
        ok = (not w['flags']) and (not w['greek']) and (c, l, i) not in varw and nletters(w['t']) >= 2
        parts.append(w['t']); mask += [ok] * len(w['t'])
    t = ''.join(parts)
    lead = len(t) - len(t.lstrip()); t2 = t.strip()
    mask = mask[lead: lead + len(t2)]
    assert t2 == ' '.join(w['t'] for w in ws).strip() and len(mask) == len(t2)
    return t2, mask


def eligible():
    L = json.load(open(f'{HERE}/etcbc_lines.json'))
    varw = disputed_words(L); pc = plate_check_lines()
    out, excl = [], Counter()
    for k, ws in L.items():
        c, l = map(int, k.split(':'))
        if c > 10: continue
        why = ('target' if (c, l) in TARGETS else 'round1' if (c, l) in R1_LINES else
               'template_source' if (c, l) in TEMPLATE_SOURCE else 'plate_check' if (c, l) in pc else
               'greek' if any(w['greek'] for w in ws) else None)
        if why: excl[why] += 1; continue
        t, mask = line_text_mask(c, l, ws, varw)
        if nletters(t) < 6 or sum(1 for ch, ok in zip(t, mask) if ok and 'א' <= ch <= 'ת') < 3:
            excl['too_few_letters'] += 1; continue
        out.append((c, l, t, mask))
    return sorted(out, key=lambda x: (x[0], x[1])), excl


def truth_set(c, l, text, mask):
    """round-1 candidates.candidates(), options restricted to mask (the only change)"""
    P = C.pairs(); text = text.strip(); base = ''.join(C.FROMF.get(ch, ch) for ch in text)
    opts = []
    for i, ch in enumerate(base):
        if not mask[i]: continue
        for b, rate in P.get(ch, []):
            opts.append((i, b, rate))
    rng = np.random.default_rng(20261030 + 100 * c + l)
    w = np.array([o[2] for o in opts]); w = w / w.sum()
    pick = rng.choice(len(opts), size=min(C.K - 1, len(opts)), replace=False, p=w)
    cands = [text]; subs = []
    for j in sorted(pick):
        i, b, _ = opts[j]
        s = C.subst(text, i, b)
        if s not in cands: cands.append(s); subs.append((i, b))
    return cands, subs


def diffpos(a, b):
    d = [i for i, (x, y) in enumerate(zip(a, b)) if x != y]
    assert len(a) == len(b) and len(d) == 1, (a, b)
    return d[0]


def decoy_set(c, l, cands):
    """mirrored decoy set from a truth set [T, V1..Vm] (strings only)"""
    T, V = cands[0], cands[1:]
    js = int(np.random.default_rng(20261031 + 100 * c + l).integers(len(V)))
    D = V[js]
    out = [D, T]
    for j, v in enumerate(V):
        if j == js: continue
        i = diffpos(T, v)
        s = C.subst(D, i, v[i]) if i != diffpos(T, D) else v
        assert s not in out
        out.append(s)
    return js, out


NLINES = {1: 15, 2: 15, 3: 13, 4: 14, 5: 14, 6: 14, 7: 16, 8: 16, 9: 17, 10: 17}   # = round-1 abs_score.NLINES


def wrong_line(c, l):
    """superseded exploratory design (same column)"""
    return l + 5 if l + 5 <= NLINES[c] else l - 5


def wrong_col(c, l):
    c2 = c + 5 if c <= 5 else c - 5
    assert not set(COL_CUTS[c]) & set(COL_CUTS[c2])
    return c2, min(l, NLINES[c2])


def null_p(cands):
    """exact chance that the centre (cands[0]) ranks strictly first, under exchangeable letters per position"""
    pos = Counter(diffpos(cands[0], v) for v in cands[1:])
    p = 1.0
    for a in pos.values(): p *= 1.0 / (a + 1)
    return p, sorted(pos.values())


def build(lines, tag):
    rows = []
    for c, l, t, mask in lines:
        cs, _ = truth_set(c, l, t, mask)
        js, ds = decoy_set(c, l, cs)
        pt, at = null_p(cs); pd, ad = null_p(ds)
        assert at == ad
        rows.append(dict(col=c, line=l, set=tag, cuts=COL_CUTS[c], truth=t,
                         mask=''.join('1' if x else '0' for x in mask), candidates=cs, decoy_index=js,
                         decoy=ds[0], decoy_candidates=ds, wrong_line=wrong_line(c, l),
                         wrong_col=wrong_col(c, l)[0], wrong_col_line=wrong_col(c, l)[1], a_profile=at,
                         p_null=round(pt, 6)))
    return rows


def build_r1():
    """decoy sets for round 1's 25 exposed lines (their round-1 candidate sets, unchanged) - EXPLORATORY"""
    rows = []
    for x in json.load(open(f'{HERE}/calibration_items.json')):
        c, l, cs = x['col'], x['line'], x['candidates']
        js, ds = decoy_set(c, l, cs)
        pt, at = null_p(cs); pd, ad = null_p(ds)
        assert at == ad
        rows.append(dict(col=c, line=l, set='r1_' + x['split'], cuts=COL_CUTS[c], truth=cs[0], candidates=cs,
                         decoy_index=js, decoy=ds[0], decoy_candidates=ds, wrong_line=wrong_line(c, l),
                         wrong_col=wrong_col(c, l)[0], wrong_col_line=wrong_col(c, l)[1], a_profile=at,
                         p_null=round(pt, 6)))
    return rows


if __name__ == '__main__':
    if sys.argv[1:2] == ['r1']:
        rows = build_r1()
        json.dump(rows, open(f'{HERE}/items_r1_decoy.json', 'w'), ensure_ascii=False, indent=1)
        print(len(rows), 'round-1 lines; sum p_null', round(sum(r['p_null'] for r in rows), 3))
    else:
        Ls, excl = eligible()
        rows = build(Ls, 'new_heldout')
        json.dump(rows, open(f'{HERE}/items_b3.json', 'w'), ensure_ascii=False, indent=1)
        print(len(rows), 'new lines; excluded', dict(excl))
        print(Counter(r['col'] for r in rows))
        print(Counter(len(r['candidates']) for r in rows), 'sum p_null', round(sum(r['p_null'] for r in rows), 3))
