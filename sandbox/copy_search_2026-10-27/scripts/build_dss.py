"""Build graphical-word sequences per (scroll, fragment) from ETCBC dss TF 2.0.2.
Output JSON: list of units {scroll, fragment, biblical, words:[{t, line, full, num, sp:[...], lex:[...] }]}
A graphical word = consecutive word nodes joined while `after` is empty (Abegg connection 'B').
Usage: python -I build_dss.py <scriptdir> <tfdir> <out.json>
"""
import sys, json
sys.path.insert(0, sys.argv[1])
from tfmini import load_feature, load_otype, load_oslots, slot_ranges

T, OUT = sys.argv[2], sys.argv[3]
otype = load_otype(T)
types = {t: (a, b) for a, b, t in otype}
oslots = load_oslots(T)
F = {n: load_feature(T, n) for n in ['rec', 'glyph', 'full', 'after', 'type', 'sp', 'cl', 'lex', 'scroll', 'fragment', 'line', 'biblical', 'lang', 'book', 'chapter', 'verse']}

nsign = types['sign'][1]
sign_scroll = [0] * (nsign + 1)
sign_frag = [0] * (nsign + 1)
sign_line = [0] * (nsign + 1)
for kind, arr in (('scroll', sign_scroll), ('fragment', sign_frag), ('line', sign_line)):
    a, b = types[kind]
    for n in range(a, b + 1):
        for x, y in slot_ranges(oslots[n]):
            for s in range(x, y + 1):
                arr[s] = n

wa, wb = types['word']
words = []
for w in range(wa, wb + 1):
    sl = slot_ranges(oslots[w])
    s0 = sl[0][0]
    words.append((s0, w))
words.sort()

units = {}
order = []
cur = None  # current graphical word
for s0, w in words:
    sc, fr, ln = sign_scroll[s0], sign_frag[s0], sign_line[s0]
    key = (sc, fr)
    if key not in units:
        units[key] = dict(scroll=F['scroll'].get(sc, ''), fragment=F['fragment'].get(fr, ''),
                          biblical=F['biblical'].get(fr, ''), words=[])
        order.append(key)
        cur = None
    u = units[key]
    g = F['glyph'].get(w, '') or ''
    typ = F['type'].get(w, '')
    ncons = nrec = 0
    sl = slot_ranges(oslots[w])
    for x, y in sl:
        for s in range(x, y + 1):
            if F['type'].get(s) == 'cons':
                ncons += 1
                if F['rec'].get(s):
                    nrec += 1
    part = dict(ncons=ncons, nrec=nrec, g=g, full=F['full'].get(w, '') or '', typ=typ, sp=F['sp'].get(w, ''), cl=F['cl'].get(w, ''),
                lex=F['lex'].get(w, ''), lang=F['lang'].get(w, ''), bib=F['biblical'].get(w, ''))
    if cur is None or cur['_key'] != key or cur['_ln'] != ln:
        cur = dict(_key=key, _ln=ln, parts=[], line=F['line'].get(ln, ''), ref='')
        u['words'].append(cur)
    cur['parts'].append(part)
    if F['book'].get(w):
        cur['ref'] = f"{F['book'].get(w,'')} {F['chapter'].get(w,'')}:{F['verse'].get(w,'')}"
    if F['after'].get(w, '') != '':
        cur = None

out = []
for key in order:
    u = units[key]
    ws = []
    for c in u['words']:
        ps = c['parts']
        t = ''.join(p['g'] for p in ps)
        ws.append(dict(parts=[dict(g=p['g'], typ=p['typ'], sp=p['sp'], cl=p['cl'], ncons=p['ncons'], nrec=p['nrec']) for p in ps], t=t, full=''.join(p['full'] for p in ps), line=c['line'], ref=c['ref'],
                       num=any(p['typ'] == 'numr' for p in ps),
                       sp=[p['sp'] for p in ps], cl=[p['cl'] for p in ps], lex=[p['lex'] for p in ps],
                       lang=[p['lang'] for p in ps], bib=[p['bib'] for p in ps]))
    u['words'] = ws
    out.append(u)
json.dump(out, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False)
print(len(out), 'units', sum(len(u['words']) for u in out), 'graphical words')
