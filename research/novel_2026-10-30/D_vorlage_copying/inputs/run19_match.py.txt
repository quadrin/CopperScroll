"""Run 19 matching: scroll names + landmark words vs one gazetteer (CSV from build_gaz.py). C1 shuffles and C2 as run 6.
usage: match.py scroll_names.json c2_names.json gaz.csv[,gaz2.csv] outprefix [ext]
"""
import sys, os, csv, json, random, collections, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from askel import heb_skeletons, ar_tokens, ar_skeletons, lat_tokens, lat_skeletons, forms_from_tokens, FIN
SN, C2F, GAZ, OP = sys.argv[1:5]
EXT = len(sys.argv) > 5 and sys.argv[5] == 'ext'
LANDMARKS = [('lm_kippa', 'כפא', 'Kippa'), ('lm_yagar', 'יגר', 'yagar (heap)'), ('lm_sariah', 'צריח', 'ṣariaḥ (tower)'),
             ('lm_shit', 'שית', 'šit (drain/pit)'), ('lm_sedeq', 'סדק', 'sedeq (fissure)'), ('lm_ashiah', 'אשיח', 'ʾašiaḥ (reservoir)'),
             ('lm_nefesh', 'נפש', 'nefeš (tomb monument)')]
PLACED = {'jericho', 'achor', 'sekakah'}   # run 6's known set; plus priority 0 in scroll_names.json

rows = []
for fn in GAZ.split(','):
    rows += list(csv.DictReader(open(fn, encoding='utf-8')))
for i, r in enumerate(rows):
    if r['script'] == 'ar':
        toks = ar_tokens(r['name']); fn_ = ar_skeletons
    else:
        mode = r['mode']; toks = lat_tokens(r['name']); fn_ = (lambda t, m=mode: lat_skeletons(t, m))
    r['_fn'] = forms_from_tokens(toks, fn_, include_heads=False)
    r['_fl'] = forms_from_tokens(toks, fn_, include_heads=True)

def build_index(key):
    ex = collections.defaultdict(set); wild = collections.defaultdict(set); dele = collections.defaultdict(set)
    for i, r in enumerate(rows):
        for g in r[key]:
            ex[g].add((i, g))
            if len(g) >= 4:
                for k in range(len(g)):
                    wild[g[:k] + '*' + g[k + 1:]].add((i, g))
                    dele[g[:k] + g[k + 1:]].add((i, g))
    return ex, wild, dele
IDX = {'_fn': build_index('_fn'), '_fl': build_index('_fl')}

def lookup(s, key):
    """returns {row index: (gaz_skel, kind)} for skeleton s."""
    ex, wild, dele = IDX[key]; out = {}
    for i, g in ex.get(s, ()): out[i] = (g, 'identical')
    if len(s) >= 4:
        cand = set()
        for k in range(len(s)):
            cand |= wild.get(s[:k] + '*' + s[k + 1:], set())          # substitution (same length)
            d = s[:k] + s[k + 1:]
            if len(d) >= 4: cand |= {(i, g) for i, g in ex.get(d, ()) if len(g) >= 4}   # gaz shorter by one
        cand |= dele.get(s, set())                                       # gaz longer by one
        for i, g in cand:
            if i not in out and g != s: out[i] = (g, 'ed1')
    return out

def find(variants, key):
    hits = {}
    for v in variants:
        for s in sorted(heb_skeletons(v, EXT)):
            for i, (g, kind) in lookup(s, key).items():
                if i not in hits or (kind == 'identical' and hits[i][3] != 'identical'):
                    hits[i] = (v, s, g, kind)
    return hits

names = json.load(open(SN))
units = [dict(id=n['id'], label=n['name'], kind='name', variants=[v['core'] for v in n['variants']],
              placed=(n['priority'] == 0 or n['id'] in PLACED), entries=n.get('entries', ''), key='_fn') for n in names]
units += [dict(id=i, label=l, kind='landmark', variants=[h], placed=False, entries='', key='_fl') for i, h, l in LANDMARKS]

rng = random.Random(20261027)
allm = []; summ = []
for u in units:
    h = find(u['variants'], u['key'])
    for i, (v, s, g, kind) in sorted(h.items()):
        r = rows[i]
        allm.append(dict(unit=u['id'], unit_kind=u['kind'], status='placed/known' if u['placed'] else 'unplaced', variant=v, scroll_skel=s,
                         src=r['src'], gid=r['gid'], gaz_name=r['name'], gaz_note=r['note'], gaz_skel=g, kind=kind, cls=r['cls'], lat=r['lat'], lon=r['lon']))
    c = 0
    for k in range(100):
        sh = []
        for v in u['variants']:
            L = list(v.translate(FIN)); rng.shuffle(L); sh.append(''.join(L))
        c += bool(find(sh, u['key']))
    ident = sum(1 for x in h.values() if x[3] == 'identical')
    summ.append(dict(unit=u['id'], label=u['label'], kind=u['kind'], status='placed/known' if u['placed'] else 'unplaced', entries=u['entries'],
                     match=int(bool(h)), n_rows=len(h), n_identical=ident, n_features=len({rows[i]['src'] + rows[i]['gid'] for i in h}), c1=c / 100,
                     lead=int(bool(h) and not u['placed'] and c / 100 <= 0.10),
                     examples='; '.join(sorted({rows[i]['name'] for i in h}))[:300]))

c2 = json.load(open(C2F)); c2r = []
for c in c2:
    h = find([c['c2_hebrew']], '_fn')
    c2r.append(dict(c2=c['c2_hebrew'], ref=c['ref'], for_scroll=c['for_scroll'], match=int(bool(h)), n_rows=len(h),
                    examples='; '.join(sorted({rows[i]['name'] for i in h}))[:200]))

def pb_tail(ps, k):
    dist = [1.0]
    for p in ps:
        new = [0.0] * (len(dist) + 1)
        for i, d in enumerate(dist): new[i] += d * (1 - p); new[i + 1] += d * p
        dist = new
    return sum(dist[k:])
def fisher_two(a, b, c, d):
    n = a + b + c + d; r1 = a + b; c1 = a + c
    def pr(x): return math.comb(c1, x) * math.comb(n - c1, r1 - x) / math.comb(n, r1)
    p0 = pr(a); lo = max(0, r1 - (n - c1)); hi = min(r1, c1)
    return sum(pr(x) for x in range(lo, hi + 1) if pr(x) <= p0 + 1e-12)

def wcsv(fn, L):
    with open(fn, 'w', newline='', encoding='utf-8') as f:
        if not L: f.write('(none)\n'); return
        w = csv.DictWriter(f, fieldnames=list(L[0].keys())); w.writeheader(); [w.writerow(x) for x in L]
wcsv(OP + '_matches.csv', allm); wcsv(OP + '_per_unit.csv', summ); wcsv(OP + '_c2.csv', c2r)
nm = [s for s in summ if s['kind'] == 'name']
obs = sum(s['match'] for s in nm); ps = [s['c1'] for s in nm]; k2 = sum(x['match'] for x in c2r)
un = [s for s in nm if s['status'] == 'unplaced']; pl = [s for s in nm if s['status'] != 'unplaced']
st = dict(gazetteer=GAZ, ext=EXT, n_gaz_rows=len(rows), names_matched=obs, c1_expected=round(sum(ps), 2), c1_mean=round(sum(ps) / 40, 3),
          p_c1=round(pb_tail(ps, obs), 4), c2_matched=k2, fisher_scroll_vs_c2=round(fisher_two(obs, 40 - obs, k2, 40 - k2), 4),
          unplaced_matched=f"{sum(s['match'] for s in un)}/{len(un)}", unplaced_c1_expected=round(sum(s['c1'] for s in un), 2),
          p_c1_unplaced=round(pb_tail([s['c1'] for s in un], sum(s['match'] for s in un)), 4),
          placed_matched=f"{sum(s['match'] for s in pl)}/{len(pl)}", placed_c1_expected=round(sum(s['c1'] for s in pl), 2),
          p_c1_placed=round(pb_tail([s['c1'] for s in pl], sum(s['match'] for s in pl)), 4),
          landmarks_matched=sum(s['match'] for s in summ if s['kind'] == 'landmark'),
          landmark_c1_expected=round(sum(s['c1'] for s in summ if s['kind'] == 'landmark'), 2),
          leads=[s['unit'] for s in summ if s['lead']],
          leads_literal_priority_only=[s['unit'] for s in summ if s['match'] and s['c1'] <= 0.10 and s['unit'] in ('achor', 'sekakah')])
json.dump(st, open(OP + '_stats.json', 'w'), indent=1, ensure_ascii=False)
print(json.dumps(st, ensure_ascii=False))
for s in summ: print(f"{s['unit']:10} {s['status'][:8]:8} m={s['match']} rows={s['n_rows']:4} id={s['n_identical']:4} C1={s['c1']:.2f} lead={s['lead']} | {s['examples'][:120]}")
