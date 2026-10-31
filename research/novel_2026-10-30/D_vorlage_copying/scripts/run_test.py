"""Confirmatory run of the frozen Vorlage-emendation test (see ../PROTOCOL_FROZEN.md). Run ONCE.
usage: python3 -I run_test.py REPO OUTDIR            (confirmatory)
       python3 -I run_test.py REPO OUTDIR --smoke    (code check on PLACED names jericho/doq only; writes smoke_* files)
"""
import sys, os, csv, json, random, math, collections
REPO, OUT = sys.argv[1], sys.argv[2]
SMOKE = '--smoke' in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__))
DD = os.path.join(os.path.dirname(HERE), 'data')
T01 = os.path.join(REPO, 'research/agent_review_2026-10-07/wave1/T01_place_names')
# ---- Palmer: T01 scorer and chance pool, imported unchanged -------------------------------------------------------
sys.argv = [sys.argv[0], T01]
sys.path.insert(0, os.path.join(T01, 'scripts'))
import chance as T01C                                # executes T01 load_pool() on import (tess, priority sheets)
from toponym import heb_tokens, palmer_variants, score, heb_str
sys.path.insert(0, HERE)
from askel import heb_skeletons, ar_tokens, ar_skeletons, lat_tokens, lat_skeletons, forms_from_tokens, FIN
NRAND_NEW = 200; ALPHA = 0.05; LEAD_C1 = 0.10; NPERM = 10000; NUNI = 10000
# Palmer records with metadata, same filter as T01 chance.load_pool (checked equal below)
P_RECS = []
for r in csv.DictReader(open(os.path.join(T01, 'data/palmer_names.csv'), encoding='utf-8')):
    if r['source'] != 'tess' or r['sheet'] not in T01C.PRIORITY or not r['name_raw'] or len(r['name_raw']) > 80: continue
    V, _ = palmer_variants(r['name_raw'], r['gloss'], 'tess')
    if V: P_RECS.append((r, [A for _, A in V]))
assert len(P_RECS) == len(T01C.REC_IDX), (len(P_RECS), len(T01C.REC_IDX))
RAND = {k: [x[0] for x in v] for k, v in json.load(open(os.path.join(T01, 'data/chance_random_by_pattern.json'))).items()}
def pattern(H): return tuple(("S", "strong") if k == "strong" else (t, k) for t, k in H)
def palmer_pool_freq():
    pool = collections.Counter()
    for ne in json.load(open(os.path.join(T01, 'data/scroll_names.json'), encoding='utf-8')):
        for v in ne['variants']:
            for t, k in heb_tokens(v['core']):
                if k == 'strong': pool[t] += 1
    for pc in json.load(open(os.path.join(T01, 'data/positive_controls.json'), encoding='utf-8')):
        for t, k in heb_tokens(pc['core']):
            if k == 'strong': pool[t] += 1
    for l in [l for l in sorted(set(T01C.HEB_MAP.values())) if l not in ("'", "h", "w", "y")]: pool.setdefault(l, 0)
    return dict(pool)
def ensure_random(patterns):
    missing = sorted({json.dumps(p) for p in patterns} - set(RAND))
    pf = palmer_pool_freq()
    for j, pk in enumerate(missing):
        p = tuple(tuple(x) for x in json.loads(pk))
        RAND[pk] = [T01C.rand_job((p, 7_000_000 + 1000 * j + t, pf))[0] for t in range(NRAND_NEW)]
    return missing
def p_tail(rh, obs): return (1 + sum(1 for x in rh if x >= obs)) / (len(rh) + 1)
def palmer_eval(s):
    H = heb_tokens(s)
    sk = [score(H, list(A))[0] for A in T01C.UNIQ]
    best_per_rec = [max(sk[i] for i in ri) for ri in T01C.REC_IDX]
    hits = [i for i, b in enumerate(best_per_rec) if b >= T01C.THRESH]
    return H, hits, best_per_rec, (max(sk) if sk else 0)
# ---- Mandate (S2+S4) and ASI: run 19 matcher logic -----------------------------------------------------------------
def load_gaz(files):
    rows = []
    for fn in files: rows += list(csv.DictReader(open(fn, encoding='utf-8')))
    for r in rows:
        if r['script'] == 'ar': toks = ar_tokens(r['name']); fn_ = ar_skeletons
        else: mode = r['mode']; toks = lat_tokens(r['name']); fn_ = (lambda t, m=mode: lat_skeletons(t, m))
        r['_fn'] = forms_from_tokens(toks, fn_, include_heads=False)
    ex = collections.defaultdict(set); wild = collections.defaultdict(set); dele = collections.defaultdict(set)
    for i, r in enumerate(rows):
        for g in r['_fn']:
            ex[g].add((i, g))
            if len(g) >= 4:
                for k in range(len(g)):
                    wild[g[:k] + '*' + g[k + 1:]].add((i, g)); dele[g[:k] + g[k + 1:]].add((i, g))
    return rows, (ex, wild, dele)
def lookup(s, idx):
    ex, wild, dele = idx; out = {}
    for i, g in ex.get(s, ()): out[i] = (g, 'identical')
    if len(s) >= 4:
        cand = set()
        for k in range(len(s)):
            cand |= wild.get(s[:k] + '*' + s[k + 1:], set())
            d = s[:k] + s[k + 1:]
            if len(d) >= 4: cand |= {(i, g) for i, g in ex.get(d, ()) if len(g) >= 4}
        cand |= dele.get(s, set())
        for i, g in cand:
            if i not in out and g != s: out[i] = (g, 'ed1')
    return out
def find(variants, idx):
    hits = {}
    for v in variants:
        for s in sorted(heb_skeletons(v)):
            for i, (g, kind) in lookup(s, idx).items():
                if i not in hits or (kind == 'identical' and hits[i][3] != 'identical'): hits[i] = (v, s, g, kind)
    return hits
GAZ = {'Mandate': [os.path.join(DD, 'gaz_S2.csv'), os.path.join(os.path.dirname(DD), 'inputs', 'gaz_S4.csv')],
       'ASI': [os.path.join(DD, 'gaz_ASI.csv')]}
G = {g: load_gaz(f) for g, f in GAZ.items()}
FAM = ['Palmer', 'Mandate', 'ASI']
def pb_tail(ps, k):
    dist = [1.0]
    for p in ps:
        new = [0.0] * (len(dist) + 1)
        for i, d in enumerate(dist): new[i] += d * (1 - p); new[i + 1] += d * p
        dist = new
    return sum(dist[k:])
# ---- main -----------------------------------------------------------------------------------------------------------
def main():
    if SMOKE:
        import itertools
        LET = 'אבגדהוזחטיכלמנסעפצקרשת'
        neigh = []
        for nid, core in (('jericho', 'ירחו'), ('doq', 'דוק')):
            for i, x in enumerate(core):
                for y in LET[:6]:
                    if y != x: neigh.append(dict(name_id=nid, emendation=core[:i] + y + core[i + 1:], in_V_topK='1', in_E_topK='0', w_vorlage='0', w_edition='0', rank_V='1', rank_E='1', pair='', written=x, emended_to=y, variant=core))
        pref = 'smoke_'
    else:
        neigh = list(csv.DictReader(open(os.path.join(DD, 'neighbourhood.csv'), encoding='utf-8')))
        pref = ''
    strings = sorted({r['emendation'] for r in neigh})
    VE = sorted({r['emendation'] for r in neigh if r['in_V_topK'] == '1' or r['in_E_topK'] == '1'})
    # originals (descriptive): variant cores of the unplaced names
    orig = sorted({r['variant'].translate(FIN) for r in neigh})
    res = {}
    print('Palmer scoring', len(strings) + len(orig), 'strings', flush=True)
    for s in sorted(set(strings) | set(orig)):
        H, hits, bpr, best = palmer_eval(s)
        res[s] = dict(H=H, pat=json.dumps(pattern(H)), p_hits=hits, p_bpr=bpr if s in VE or s in orig else None, p_best=best)
    missing = ensure_random([pattern(res[s]['H']) for s in res])
    for s, d in res.items():
        rh = RAND[d['pat']]; obs = len(d['p_hits'])
        d['p_obs'] = obs; d['p_p'] = p_tail(rh, obs)
        d['m_Palmer'] = int(d['p_p'] <= ALPHA)
        d['c_Palmer'] = sum(1 for r in rh if p_tail(rh, r) <= ALPHA) / len(rh)
        d['p_rand_mean'] = sum(rh) / len(rh)
        for g in ('Mandate', 'ASI'):
            h = find([s], G[g][1]); d[f'h_{g}'] = h; d[f'm_{g}'] = int(bool(h))
    rng = random.Random(20261030)
    for s in sorted(set(VE) | set(orig)):
        for g in ('Mandate', 'ASI'):
            c = 0
            for _ in range(100):
                L = list(s.translate(FIN)); rng.shuffle(L); c += bool(find([''.join(L)], G[g][1]))
            res[s][f'c_{g}'] = c / 100
    m = lambda s: sum(res[s][f'm_{g}'] for g in FAM)
    # frozen sets
    byname = collections.defaultdict(list)
    for r in neigh: byname[r['name_id']].append(r['emendation'])
    Vset = {(r['name_id'], r['emendation']) for r in neigh if r['in_V_topK'] == '1'}
    Eset = {(r['name_id'], r['emendation']) for r in neigh if r['in_E_topK'] == '1'}
    def M(S): return sum(m(s) for _, s in S)
    def C(S): return sum(res[s][f'c_{g}'] for _, s in S for g in FAM)
    MV, ME = M(Vset), M(Eset)
    pV = pb_tail([res[s][f'c_{g}'] for _, s in Vset for g in FAM], MV)
    pE = pb_tail([res[s][f'c_{g}'] for _, s in Eset for g in FAM], ME)
    # (ii-a) per-name permutation of V-only vs E-only strings
    rngp = random.Random(20261031)
    A = {n: sorted(s for (nn, s) in Vset - Eset if nn == n) for n in byname}; B = {n: sorted(s for (nn, s) in Eset - Vset if nn == n) for n in byname}
    Dobs = sum(m(s) for n in byname for s in A[n]) - sum(m(s) for n in byname for s in B[n])
    ge = 0
    for _ in range(NPERM):
        d = 0
        for n in byname:
            pool = A[n] + B[n]; rngp.shuffle(pool); k = len(A[n])
            d += sum(m(s) for s in pool[:k]) - sum(m(s) for s in pool[k:])
        ge += d >= Dobs
    p_perm = (1 + ge) / (NPERM + 1)
    # (ii-b) uniform control: K strings per name uniformly from the neighbourhood
    rngu = random.Random(20261032); K = 10; ge = 0; MU = []
    uniq_by = {n: sorted(set(v)) for n, v in byname.items()}
    for _ in range(NUNI):
        tot = 0
        for n, lst in uniq_by.items(): tot += sum(m(s) for s in rngu.sample(lst, min(K, len(lst))))
        MU.append(tot); ge += tot >= MV
    p_uni = (1 + ge) / (NUNI + 1)
    fam_counts = {S_: {g: sum(res[s][f'm_{g}'] for _, s in SS) for g in FAM} for S_, SS in (('V', Vset), ('E', Eset))}
    passed = dict(i=pV <= ALPHA and MV > C(Vset), ii_a=p_perm <= ALPHA, ii_b=p_uni <= ALPHA)
    verdict = 'obtained' if all(passed.values()) else ('partly' if passed['i'] and (passed['ii_a'] or passed['ii_b']) else 'not obtained')
    stats = dict(smoke=SMOKE, n_names=len(byname), K=K, n_V=len(Vset), n_E=len(Eset), overlap=len(Vset & Eset), neighbourhood_strings=len(strings),
                 M_V=MV, chance_expected_V=round(C(Vset), 3), p_i_poisson_binomial_V=round(pV, 5),
                 M_E=ME, chance_expected_E=round(C(Eset), 3), p_poisson_binomial_E=round(pE, 5),
                 family_matches=fam_counts, D_obs_Vonly_minus_Eonly=Dobs, n_Vonly=len(Vset - Eset), p_ii_a_permutation=round(p_perm, 5),
                 uniform_mean=round(sum(MU) / len(MU), 3), uniform_p95=sorted(MU)[int(0.95 * (len(MU) - 1))], p_ii_b_uniform=round(p_uni, 5),
                 passed=passed, verdict=verdict, palmer_new_patterns=len(missing),
                 originals=dict(n=len(orig), matches={g: sum(res[s][f'm_{g}'] for s in orig) for g in FAM},
                                chance_expected=round(sum(res[s][f'c_{g}'] for s in orig for g in FAM), 3)))
    json.dump(stats, open(os.path.join(OUT, pref + 'test_result.json'), 'w'), indent=1, ensure_ascii=False)
    # per-string table and gazetteer hits for V u E
    nrow = {}
    for r in neigh: nrow.setdefault(r['emendation'], []).append(r)
    hits = []; cand = []
    for s in VE:
        d = res[s]; rs = nrow[s]
        sets = '+'.join(x for x, S in (('V', Vset), ('E', Eset)) if any((r['name_id'], s) in S for r in rs))
        base = dict(emendation=s, name_ids=';'.join(sorted({r['name_id'] for r in rs})), from_variant=';'.join(sorted({r['variant'] for r in rs})),
                    pair=';'.join(sorted({r['pair'] for r in rs})), sets=sets)
        for i in d['p_hits']:
            rec = P_RECS[i][0]
            hits.append(dict(base, gazetteer='Palmer', record=rec['name_raw'], gaz_skeleton='', kind=f"score {d['p_bpr'][i]:.3f}", sheet=rec['sheet'], page=rec['page'], grid=rec['grid'],
                             lat='', lon='', family_match=d['m_Palmer'], family_chance=round(d['c_Palmer'], 3), palmer_hits=d['p_obs'], palmer_p=round(d['p_p'], 3), note=rec['gloss'][:120].replace('\n', ' ')))
        for g in ('Mandate', 'ASI'):
            rows_ = G[g][0]
            for i, (v, sk, gs, kind) in sorted(d[f'h_{g}'].items()):
                r = rows_[i]
                hits.append(dict(base, gazetteer=f"{g}:{r['src']}", record=r['name'], gaz_skeleton=gs, kind=kind, sheet='', page='', grid='', lat=r['lat'], lon=r['lon'],
                                 family_match=1, family_chance=d[f'c_{g}'], palmer_hits='', palmer_p='', note=r['note'][:120]))
        # candidate rule (frozen): V-set string; Mandate/ASI match with C1 <= 0.10, or Palmer match (p<=0.05) with best record score >= 0.9
        if 'V' in sets:
            why = []
            for g in ('Mandate', 'ASI'):
                if d[f'm_{g}'] and d[f'c_{g}'] <= LEAD_C1: why.append(f"{g} C1={d[f'c_{g}']:.2f}: " + '; '.join(sorted({G[g][0][i]['name'] for i in d[f'h_{g}']}))[:200])
            if d['m_Palmer'] and d['p_best'] >= 0.9:
                top = sorted(((d['p_bpr'][i], P_RECS[i][0]['name_raw'], P_RECS[i][0]['sheet'], P_RECS[i][0]['grid']) for i in d['p_hits']), reverse=True)[:3]
                why.append(f"Palmer hits={d['p_obs']} p={d['p_p']:.3f}: " + '; '.join(f'{n} ({sh} {gr}, {sc:.2f})' for sc, n, sh, gr in top))
            if why:
                cand.append(dict(base, rank_V=min(int(r['rank_V']) for r in rs), reasons=' | '.join(why)))
    cols = ['emendation', 'name_ids', 'from_variant', 'pair', 'sets', 'gazetteer', 'record', 'gaz_skeleton', 'kind', 'sheet', 'page', 'grid', 'lat', 'lon',
            'family_match', 'family_chance', 'palmer_hits', 'palmer_p', 'note']
    with open(os.path.join(OUT, pref + 'gazetteer_hits.csv'), 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(hits)
    with open(os.path.join(OUT, pref + 'per_string.csv'), 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh); w.writerow(['string', 'role', 'heb_skeleton', 'palmer_hits', 'palmer_random_mean', 'palmer_p', 'm_Palmer', 'c_Palmer', 'm_Mandate', 'c_Mandate', 'm_ASI', 'c_ASI'])
        for s in sorted(set(VE) | set(orig)):
            d = res[s]
            w.writerow([s, 'original' if s in orig else 'emendation', heb_str(d['H']), d['p_obs'], round(d['p_rand_mean'], 2), round(d['p_p'], 3), d['m_Palmer'], round(d['c_Palmer'], 3),
                        d['m_Mandate'], d.get('c_Mandate', ''), d['m_ASI'], d.get('c_ASI', '')])
    with open(os.path.join(OUT, pref + 'candidates.csv'), 'w', newline='', encoding='utf-8') as fh:
        if cand:
            w = csv.DictWriter(fh, fieldnames=list(cand[0])); w.writeheader(); w.writerows(cand)
        else: fh.write('(none)\n')
    print(json.dumps(stats, ensure_ascii=False, indent=1))
main()
