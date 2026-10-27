"""Build graphical-word sequences per chapter from ETCBC BHSA 2021 TF.
Graphical word = BHSA words joined while trailer is empty (prefixes such as ו ב ה ל are separate BHSA words).
Usage: python -I build_bhsa.py <scriptdir> <tfdir> <out.json>
"""
import sys, json
sys.path.insert(0, sys.argv[1])
from tfmini import load_feature, load_otype, load_oslots, slot_ranges

T, OUT = sys.argv[2], sys.argv[3]
otype = load_otype(T)
types = {t: (a, b) for a, b, t in otype}
oslots = load_oslots(T)
g = load_feature(T, 'g_cons_utf8')
tr = load_feature(T, 'trailer_utf8')
ls = load_feature(T, 'ls')
sp = load_feature(T, 'sp')
book = load_feature(T, 'book')
chap = load_feature(T, 'chapter')

nw = types['word'][1]
w2ch = [0] * (nw + 1)
a, b = types['chapter']
for n in range(a, b + 1):
    for x, y in slot_ranges(oslots[n]):
        for s in range(x, y + 1):
            w2ch[s] = n
ba, bb = types['book']
ch2book = {}
for n in range(ba, bb + 1):
    for x, y in slot_ranges(oslots[n]):
        ch2book[(x, y)] = book[n]
w2b = [''] * (nw + 1)
for (x, y), bk in ch2book.items():
    for s in range(x, y + 1):
        w2b[s] = bk

units = {}
order = []
cur = None
for w in range(1, nw + 1):
    c = w2ch[w]
    if c not in units:
        units[c] = dict(scroll=f"{w2b[w]} {chap.get(c, '')}", fragment='', biblical='BHSA', words=[])
        order.append(c)
        cur = None
    part = dict(g=g.get(w, '') or '', typ='', sp=sp.get(w, ''), cl=ls.get(w, ''), ncons=0, nrec=0)
    if cur is None:
        cur = dict(parts=[], line='', ref=f"{w2b[w]} {chap.get(c,'')}")
        units[c]['words'].append(cur)
    cur['parts'].append(part)
    t = tr.get(w, '') or ''
    if t != '':
        cur = None
out = []
for c in order:
    u = units[c]
    for x in u['words']:
        x['t'] = ''.join(p['g'] for p in x['parts'])
        x['full'] = x['t']
        x['num'] = False
    out.append(u)
json.dump(out, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False)
print(len(out), 'chapters', sum(len(u['words']) for u in out), 'graphical words')
