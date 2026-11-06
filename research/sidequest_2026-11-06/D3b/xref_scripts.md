# D3b scripts (6 Nov 2026)

Input: `txt/<KEY>.json` = `{"slug":..., "pages": hexview.pdf_pages_text(slug)}` saved from the bucket `pdf/<slug>/pages.jsonl`. Run `python3 -I xref.py KEY` then `python3 -I subject.py KEY`. Keys used: MAG2018, MAR4, LEI2018, RS2021 (also run on ROS07, HCM2016, HG2003, JSP19, JSP8, DJD3, HF2019; see FINDS.md dead ends).

## xref.py
```python
"""Figure/plate/plan/table cross-reference extractor for page-split text layers.
usage: python3 -I xref.py KEY   (reads txt/KEY.json, writes refs_KEY.json)
"""
import json, re, sys, collections

KEY = sys.argv[1]
d = json.load(open(f'/home/claude/swarm/scratch/D3b/txt/{KEY}.json'))
pages = d['pages']

KIND = {'fig': 'Fig', 'figs': 'Fig', 'figure': 'Fig', 'figures': 'Fig',
        'pl': 'Pl', 'pls': 'Pl', 'plate': 'Pl', 'plates': 'Pl',
        'plan': 'Plan', 'plans': 'Plan', 'table': 'Table', 'tables': 'Table'}
NUM = r'\d+(?:\.\d+){0,2}[a-z]?'
CAP_RE = re.compile(r'^\s*(Fig\.|Figure\.?|Pl\.|Plate|Plan|Table)\s*(' + NUM + r')\s*[.:\t  ]', re.I)
REF_RE = re.compile(r'\b(Figs?\.|Figures?|Pls?\.|Plates?|Plans?|Tables?)\s*(' + NUM + r'(?:\s*(?:[–\-,]|and|&)\s*' + NUM + r')*)')
EXT_RE = re.compile(r'(\b1[6-9]\d\d|\b20[0-2]\d)[a-z]?\s*[:,]\s*(?:p+\.\s*[\d–\-]+\s*[,;]\s*)?(?:[^\s]+\s*){0,3}$')


def kind(w):
    return KIND[w.lower().rstrip('.').rstrip()]


def expand(kd, s):
    """'2.19–2.21' -> list; '1.2, 1.4' -> list; '5–7' -> list"""
    out = []
    parts = re.split(r'\s*(?:,|and|&)\s*', s)
    for part in parts:
        m = re.match(r'(' + NUM + r')\s*[–\-]\s*(' + NUM + r')$', part)
        if m:
            a, b = m.group(1), m.group(2)
            pa, pb = a.split('.'), b.split('.')
            try:
                if len(pa) == len(pb) and pa[:-1] == pb[:-1]:
                    lo, hi = int(re.sub(r'\D', '', pa[-1])), int(re.sub(r'\D', '', pb[-1]))
                    if 0 < hi - lo < 60:
                        out += ['.'.join(pa[:-1] + [str(i)]) for i in range(lo, hi + 1)]
                        continue
                if len(pa) == 2 and len(pb) == 1:  # 2.19–21
                    lo, hi = int(re.sub(r'\D', '', pa[1])), int(re.sub(r'\D', '', pb[0]))
                    if 0 < hi - lo < 60:
                        out += [f'{pa[0]}.{i}' for i in range(lo, hi + 1)]
                        continue
            except ValueError:
                pass
            out += [a, b]
        elif re.match(NUM + '$', part):
            out.append(part)
    return out


caps = collections.defaultdict(list)
refs = []
for p in pages:
    lines = p['text'].split('\n')
    for i, line in enumerate(lines):
        m = CAP_RE.match(line)
        if m:
            k = kind(m.group(1))
            num = m.group(2).rstrip('.')
            text = ' '.join((line + ' ' + ' '.join(lines[i + 1:i + 3]))[:260].split())
            caps[(k, num)].append({'page': p['page'], 'caption': text})
    txt = p['text']
    for m in REF_RE.finditer(txt):
        ls = txt.rfind('\n', 0, m.start()) + 1
        if CAP_RE.match(txt[ls:m.end() + 3]) and ls == m.start() - (len(txt[ls:m.start()]) - len(txt[ls:m.start()].lstrip())):
            continue  # caption itself
        pre = txt[max(0, m.start() - 60):m.start()]
        external = bool(EXT_RE.search(pre)) or bool(re.search(r'(DJD|SC\s*\d+|Qedem|ibid|op\. cit|vol\.|Vol\.)\s*[\d,]*\s*$', pre, re.I))
        k = kind(m.group(1))
        ctx = ' '.join(txt[max(0, m.start() - 160):m.end() + 60].split())
        for num in expand(k, m.group(2)):
            refs.append({'page': p['page'], 'kind': k, 'num': num.rstrip('.'), 'raw': m.group(0).replace('\n', ' '),
                         'external': external, 'ctx': ctx})

json.dump({'caps': {f'{k}|{n}': v for (k, n), v in caps.items()}, 'refs': refs},
          open(f'/home/claude/swarm/scratch/D3b/refs_{KEY}.json', 'w'), ensure_ascii=False)
internal = [r for r in refs if not r['external']]
miss = [r for r in internal if (r['kind'], r['num']) not in caps]
print(KEY, 'captions', len(caps), 'refs', len(refs), 'internal', len(internal), 'unresolved', len(miss))
c = collections.Counter((r['kind'], r['num']) for r in miss)
print(' unresolved targets (top):', c.most_common(60))

```

## subject.py
```python
"""Subject match: tokens (locus, wall, unit, room, area, square, SC, cave, tomb) in the citing clause vs the caption.
usage: python3 -I subject.py KEY  -> prints candidate mismatches, writes subj_KEY.json
"""
import json, re, sys
KEY = sys.argv[1]
r = json.load(open(f'/home/claude/swarm/scratch/D3b/refs_{KEY}.json'))
caps = r['caps']
TOK = [
    ('L', re.compile(r'\bL(?:oci?|ocus)?\.?\s?(\d[\dA-Z]*\d|\d+[A-Z]?\d*|[1-9][A-Z]\d{3})\b')),
    ('W', re.compile(r'\bW(?:alls?)?\.?\s?(\d{2,4}[A-Z]?)\b')),
    ('Unit', re.compile(r'\bUnits?\s([A-Z]\d+)\b')),
    ('Room', re.compile(r'\bRooms?\s(\d+[a-z]?)\b')),
    ('Area', re.compile(r'\bAreas?\s([A-Z]\d?)\b')),
    ('SC', re.compile(r'\b(?:SC|Subterranean Complex)\s(\d+)\b')),
    ('Cave', re.compile(r'\bCave\s(\d+)\b')),
    ('Tomb', re.compile(r'\bTomb\s(\d+)\b')),
    ('Sq', re.compile(r'\bSquares?\s([A-Z]?\d+)\b')),
]


def toks(s):
    out = {}
    for name, rx in TOK:
        v = set(rx.findall(s))
        if v:
            out[name] = v
    return out


def cap(kind, num):
    for k in (f'{kind}|{num}', f'{kind}|' + '.'.join(num.split('.')[:2])):
        if k in caps:
            return caps[k]
    return None


out = []
for x in r['refs']:
    if x['external']:
        continue
    c = cap(x['kind'], x['num'])
    if not c:
        continue
    ctx = x['ctx']
    j = ctx.find(x['raw'][:8])
    pre = ctx[:j] if j > 0 else ctx[:160]
    # citing clause: from last sentence break
    k = max(pre.rfind('. '), pre.rfind('; '))
    clause = pre[k + 1:] if k >= 0 and len(pre) - k > 25 else pre[-140:]
    tc = toks(clause)
    tk = {}
    for cc in c:
        for a, b in toks(cc['caption'][:200]).items():
            tk.setdefault(a, set()).update(b)
    shared = [t for t in tc if t in tk]
    if shared and all(not (tc[t] & tk[t]) for t in shared):
        out.append({'page': x['page'], 'ref': x['raw'], 'num': x['num'], 'kind': x['kind'], 'clause': clause[-160:],
                    'ctx_tokens': {t: sorted(tc[t]) for t in shared}, 'cap_tokens': {t: sorted(tk[t]) for t in shared},
                    'caption': c[0]['caption'][:160], 'cap_page': c[0]['page']})
json.dump(out, open(f'/home/claude/swarm/scratch/D3b/subj_{KEY}.json', 'w'), ensure_ascii=False, indent=0)
print(KEY, len(out), 'candidates')
for o in out:
    print(o['page'], o['ref'], o['ctx_tokens'], 'vs', o['cap_tokens'], '|', o['clause'][-100:], '=>', o['caption'][:100])

```
