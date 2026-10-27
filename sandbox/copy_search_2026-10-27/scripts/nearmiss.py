"""Exploratory: near misses (window with measure+number and 2 classes; or >=3 classes without measure+number) and token tallies."""
import sys, json, collections
OUTNM = sys.argv[5]
sys.path.insert(0, sys.argv[4])
import importlib.util
spec_ = importlib.util.spec_from_file_location('s', sys.argv[4] + '/search.py')
S = importlib.util.module_from_spec(spec_)
saved = sys.argv
sys.argv = ['x', sys.argv[1], sys.argv[2], sys.argv[3], '/dev/null']
spec_.loader.exec_module(S)
v = dict(classes=S.spec['classes'])
tally = collections.Counter(); near = []
for u in S.DSS:
    cat = S.category(u)
    if cat == '3Q15': continue
    ws = S.clean(u['words'])
    cl, mn = S.annotate(ws, v)
    for c in cl: 
        for k in c: tally[(cat, k)] += 1
    tally[(cat,'MEAS+NUM')] += sum(mn)
    if u['scroll'] in ('11Q19','11Q20','4Q365a','4Q524'):
        for c in cl:
            for k in c: tally[(u['scroll'], k)] += 1
        tally[(u['scroll'],'MEAS+NUM')] += sum(mn)
    n = len(ws); seen = set()
    for s in range(max(1, n - S.W + 1)):
        e = min(n, s + S.W)
        c = set().union(*cl[s:e])
        m = any(mn[s:e])
        lex = c - {'NUM'}
        if (m and len(c) == 2) or (not m and len(lex) >= 3):
            key = (u['scroll'], u['fragment'])
            if key in seen: continue
            seen.add(key)
            near.append(dict(cat=cat, scroll=u['scroll'], frag=u['fragment'], kind='meas+num, 2 classes' if m else '3+ lexical classes, no meas+num',
                             classes=sorted(c), lines=sorted(set(w['line'] for w in ws[s:e])), text=' '.join(w['full'] for w in ws[s:e])))
for k in sorted(tally, key=str): print(k, tally[k])
print(len(near))
for r in near: print(r['cat'], r['scroll'], r['frag'], r['lines'], r['kind'], r['classes'], '|', r['text'])
json.dump(near, open(OUTNM, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
