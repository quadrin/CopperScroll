"""Exploratory: token content of unidentified/documentary sigla (PAM, Pam, XQ, X, KhQ, 4Q340-361, 6Q26, Mas, Mur, Hev)."""
import sys, json, re, collections, importlib.util
spec_ = importlib.util.spec_from_file_location('s', sys.argv[4] + '/search.py')
S = importlib.util.module_from_spec(spec_)
sys.argv = ['x', sys.argv[1], sys.argv[2], sys.argv[3], '/dev/null']
spec_.loader.exec_module(S)
v = dict(classes=S.spec['classes'])
pat = re.compile(r'^(PAM|Pam|XQ|X\d|KhQ|Mas|Mur|5/6hev|Xhev|34Se|Sdeir|Arug|Xjud|Xjos|4Q3[4-6]\d|6Q26|4Q46\d|4Q47\d|4Q48\d|4Q49\d|4Q5[0-9]\d)')
agg = collections.defaultdict(lambda: dict(words=0, units=0, classes=collections.Counter(), mnum=0))
for u in S.DSS:
    if not pat.match(u['scroll']): continue
    grp = re.match(r'^(PAM|Pam|XQ|X\d|KhQ|Mas|Mur|5/6hev|Xhev|34Se|Sdeir|Arug|Xjud|Xjos|4Q3[4-6]|6Q26|4Q4[6-9]|4Q5)', u['scroll']).group(1)
    ws = S.clean(u['words']); cl, mn = S.annotate(ws, v)
    a = agg[grp]; a['words'] += len(ws); a['units'] += 1; a['mnum'] += sum(mn)
    found = collections.Counter(k for c in cl for k in c)
    a['classes'].update(found)
    if len(set(found) - {'NUM'}) >= 2 or sum(mn):
        print(' ', u['scroll'], u['fragment'], dict(found), 'mnum', sum(mn))
for g, a in sorted(agg.items()):
    print(g, a['units'], 'units', a['words'], 'words', dict(a['classes']), 'meas+num', a['mnum'])
