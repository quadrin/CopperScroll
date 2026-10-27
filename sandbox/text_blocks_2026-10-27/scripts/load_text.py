"""Load the ETCBC 3Q15 display text and split it into Puech's 61 entries (tables/entry_concordance.csv).
I 6 is split after word index 1 (numeral 1+100): entry 2 = I5 + I6[0:2], entry 3 = I6[2:] + I7-8 (Puech p. 179, as in
deep_analysis/features.py and T08 scroll_amounts.py)."""
import json, csv, re
REPO = '/home/claude/copperscroll'
ROMAN = ['I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII']

def load_columns():
    s = open(f'{REPO}/data/scroll-text.js', encoding='utf-8').read()
    d = json.loads(s[s.index('{'):s.rstrip().rstrip(';').rindex('}') + 1])
    return d

def rn(r): return ROMAN.index(r) + 1

def parse_range(cl):
    a, b = cl.split('–') if '–' in cl else (cl, cl)
    ca, la = a.split(':'); cb, lb = b.split(':')
    return (rn(ca), int(la)), (rn(cb), int(lb))

def entries():
    d = load_columns()
    lines = {}
    for c in d['columns']:
        for L in c['lines']:
            lines[(c['c'], L['l'])] = L['w']
    conc = list(csv.DictReader(open(f'{REPO}/tables/entry_concordance.csv', encoding='utf-8-sig')))
    out = []
    for r in conc:
        (c0, l0), (c1, l1) = parse_range(r['col_line'])
        keys = sorted(k for k in lines if (c0, l0) <= k <= (c1, l1))
        words = []
        for k in keys:
            ws = lines[k]
            for i, w in enumerate(ws):
                if k == (1, 6):
                    if r['entry_puech'] == '2' and i >= 2: continue
                    if r['entry_puech'] == '3' and i < 2: continue
                words.append(dict(w, line=f'{ROMAN[k[0]-1]} {k[1]}', idx=i))
        out.append(dict(entry=r['entry_puech'], col_line=r['col_line'], words=words))
    return out

def surface(w):
    return ''.join(p[0] for p in w['h'])

def flags(w):
    return set(f for p in w['h'] for f in p[1] if f)

if __name__ == '__main__':
    for e in entries():
        print(e['entry'], e['col_line'], ' '.join(
            (f"<{w['ns']}>" if 'n' in w else surface(w) + ('{' + ''.join(sorted(flags(w))) + '}' if flags(w) else ''))
            for w in e['words']))
