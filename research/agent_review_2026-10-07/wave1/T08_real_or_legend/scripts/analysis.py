"""Real-or-legend statistics for the Copper Scroll: compare amounts and formula features with
genuine administrative lists and legendary treasure lists. Reads data/*.csv made by the other scripts.
Writes data/amount_features.csv, data/document_features.csv, data/formula_features.csv, data/leading_digits.csv,
data/block_tests.json, data/unit_totals.csv and prints a summary.
Run: python3 -I scripts/analysis.py
"""
import csv, json, math, os, random, statistics as st
from collections import Counter, defaultdict
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(HERE, '..', 'data')
rd = lambda f: list(csv.DictReader(open(os.path.join(D, f), encoding='utf-8')))
random.seed(20261006)

# ------------------------------------------------------------------ amount sets
def mk(value, lead, sub, group, doc, unit=''):
    return dict(value=float(value), lead=float(lead), sub=bool(sub), group=group, doc=doc, unit=unit)

sets = defaultdict(list)
S = rd('scroll_amounts.csv')
for a in S:
    if a['status'] == 'doubtful': continue
    v = float(a['value']); lead = math.floor(v) if a['entry'] == '59' else v
    sub = a['has_subunit'] == 'True'
    r = mk(v, lead, sub, 'SCROLL', 'Copper Scroll', a['unit'])
    r.update(entry=a['entry'], block=a['block'], notation=a['notation'], weight=a['weight_unit'] == 'True', status=a['status'],
             variants=json.loads(a['variants']))
    sets['SCROLL_all'].append(r)
    if r['weight']: sets['SCROLL_weight'].append(r)

for g in rd('greek_amounts.csv'):
    if g['duplicate'] == 'True' or g['partial'] == 'True': continue
    lead = float(g['lead_value'])
    if lead == 0: continue
    sets[g['corpus']].append(mk(g['value_dr'], lead, g['has_subunit'] == 'True', g['corpus'], g['source'].split(',')[0], g['lead_unit']))

for h in rd('handcoded_amounts.csv'):
    sets[h['corpus']].append(mk(h['value'], h['value'], h['has_subunit'] == 'True', h['corpus'], h['ref'], h['unit']))

STRICT = ('dinar', 'mithqal', 'qantar', 'quint', 'quilital', 'lingot', 'ardeb', 'drachme', 'dirham', 'pièce')
for k in rd('kanz_amounts.csv'):
    v = float(k['value'])
    if k['kind'] == 'treasure' and (k['unit'].startswith(STRICT) or v >= 2):
        sets['L_kanz'].append(mk(v, v, v != int(v), 'L_kanz', 'Kanz §' + k['n'], k['unit']))
    if k['kind'] == 'depth':
        sets['L_kanz_depths'].append(mk(v, v, False, 'L_kanz_depths', 'Kanz §' + k['n'], k['unit']))

for e in rd('scroll_entries.csv'):
    if e['depth_cubits']:
        v = float(e['depth_cubits']); sets['SCROLL_depths'].append(mk(v, v, v != int(v), 'SCROLL_depths', e['entry'], 'cubit'))

# ------------------------------------------------------------------ features
BENF = [math.log10(1 + 1 / d) for d in range(1, 10)]
def first_digit(x):
    x = abs(x)
    while x >= 10: x /= 10
    while 0 < x < 1: x *= 10
    return int(x)
def sigdigits(n):
    n = int(round(n)); s = str(n).rstrip('0'); return len(s)

def feats(rows):
    n = len(rows); lead = [r['lead'] for r in rows]
    ge10 = [x for x in lead if x >= 10 and x == int(x)]
    ge100 = [x for x in lead if x >= 100 and x == int(x)]
    f = dict(n=n, n_ge10=len(ge10),
        m10=sum(x % 10 == 0 for x in ge10) / len(ge10) if ge10 else None,
        m5=sum(x % 5 == 0 for x in ge10) / len(ge10) if ge10 else None,
        sig1=sum(sigdigits(x) == 1 for x in ge10) / len(ge10) if ge10 else None,
        n_ge100=len(ge100), m100=sum(x % 100 == 0 for x in ge100) / len(ge100) if ge100 else None,
        subunit=sum(r['sub'] for r in rows) / n if n else None,
        myriad=sum(x >= 10000 for x in lead) / n if n else None)
    vals = [r['value'] for r in rows if r['value'] > 0]
    if len(vals) > 2:
        lv = [math.log10(v) for v in vals]
        f['log10_sd'] = st.pstdev(lv); f['log10_range'] = max(lv) - min(lv)
        f['max_over_median'] = max(vals) / st.median(vals)
        s = sorted(vals); tot = sum(s); k = max(1, round(0.1 * len(s)))
        f['top10pct_share'] = sum(s[-k:]) / tot
        f['gini'] = sum((2 * (i + 1) - len(s) - 1) * x for i, x in enumerate(s)) / (len(s) * tot)
    fd = Counter(first_digit(x) for x in lead if x > 0)
    m = sum(fd.values())
    f['benford_mad'] = sum(abs(fd.get(d, 0) / m - BENF[d - 1]) for d in range(1, 10)) / 9 if m else None
    f['distinct_ratio'] = len(set(lead)) / n if n else None
    c = Counter(lead).most_common(1)[0] if n else (None, 0)
    f['modal_value'] = c[0]; f['modal_share'] = c[1] / n if n else None
    return f

def boot_ci(rows, key, B=4000):
    out = []
    for _ in range(B):
        smp = [random.choice(rows) for _ in rows]
        v = feats(smp)[key]
        if v is not None: out.append(v)
    out.sort()
    return (out[int(0.025 * len(out))], out[int(0.975 * len(out)) - 1]) if out else (None, None)

ORDER = ['SCROLL_weight', 'SCROLL_all', 'G_inventory', 'G_accounts', 'G_tribute', 'G_eleph', 'B_admin', 'L_bibchr', 'L_kelim', 'L_kanz',
         'SCROLL_depths', 'L_kanz_depths']
LABEL = {'SCROLL_weight': 'Copper Scroll, talent/karsh amounts', 'SCROLL_all': 'Copper Scroll, all amounts',
         'G_inventory': 'Genuine: Athenian sacred inventories (weights)', 'G_accounts': 'Genuine: Athenian treasury payments/loans',
         'G_tribute': 'Genuine: Athenian tribute quota lists (derived 1/60)', 'G_eleph': 'Genuine: Elephantine collection account (totals)',
         'B_admin': 'Reference: biblical lists in administrative style', 'L_bibchr': 'Literary: idealised biblical treasure figures',
         'L_kelim': 'Legendary: Treatise of the Vessels (Massekhet Kelim)', 'L_kanz': 'Legendary: Kitab al-Durr al-Maknuz (treasure counts)',
         'SCROLL_depths': 'Copper Scroll, dig depths (cubits)', 'L_kanz_depths': 'Kitab al-Durr al-Maknuz, dig depths'}
KEYS = ['n','n_ge10','m10','m5','sig1','n_ge100','m100','subunit','myriad','log10_sd','log10_range','max_over_median','top10pct_share','gini','benford_mad','distinct_ratio','modal_value','modal_share']
amount_rows = []
for k in ORDER:
    if not sets[k]: continue
    f = feats(sets[k]); f['set'] = k; f['label'] = LABEL[k]
    for key in ('m10', 'sig1', 'subunit'):
        lo, hi = boot_ci(sets[k], key, B=2000)
        f[key + '_ci'] = f'{lo:.2f}-{hi:.2f}' if lo is not None else ''
    amount_rows.append(f)
with open(os.path.join(D, 'amount_features.csv'), 'w', newline='', encoding='utf-8') as fh:
    cols = ['set','label'] + KEYS + ['m10_ci','sig1_ci','subunit_ci']
    w = csv.DictWriter(fh, fieldnames=cols); w.writeheader()
    for r in amount_rows: w.writerow({c: (round(r[c], 3) if isinstance(r.get(c), float) else r.get(c, '')) for c in cols})

# per-document features (genuine Greek documents, plus each legendary text as one document)
doc_rows = []
by_doc = defaultdict(list)
for k in ['G_inventory', 'G_accounts', 'G_tribute', 'L_kelim', 'L_bibchr', 'B_admin', 'L_kanz']:
    for r in sets[k]:
        d = r['doc'] if k.startswith('G_') else k
        by_doc[(k, d)].append(r)
by_doc[('SCROLL_weight', 'Copper Scroll')] = sets['SCROLL_weight']
for (k, d), rows in by_doc.items():
    f = feats(rows); f['set'] = k; f['doc'] = d; doc_rows.append(f)
with open(os.path.join(D, 'document_features.csv'), 'w', newline='', encoding='utf-8') as fh:
    cols = ['set','doc','n','n_ge10','m10','sig1','m100','subunit','myriad','log10_sd','max_over_median','benford_mad','modal_share']
    w = csv.DictWriter(fh, fieldnames=cols); w.writeheader()
    for r in doc_rows: w.writerow({c: (round(r[c], 3) if isinstance(r.get(c), float) else r.get(c, '')) for c in cols})

# leading digits
with open(os.path.join(D, 'leading_digits.csv'), 'w', newline='', encoding='utf-8') as fh:
    w = csv.writer(fh); w.writerow(['set', 'n'] + [f'd{d}' for d in range(1, 10)])
    w.writerow(['Benford', ''] + [round(b, 3) for b in BENF])
    for k in ORDER:
        if not sets[k]: continue
        fd = Counter(first_digit(r['lead']) for r in sets[k] if r['lead'] > 0); m = sum(fd.values())
        w.writerow([k, m] + [round(fd.get(d, 0) / m, 3) for d in range(1, 10)])

# ------------------------------------------------------------------ blocks inside the scroll
def fisher_two_sided(a, b, c, d):
    # 2x2 [[a,b],[c,d]]; exact hypergeometric two-sided p
    from math import comb
    r1, r2, c1 = a + b, c + d, a + c; n = r1 + r2
    def p(x): return comb(r1, x) * comb(r2, c1 - x) / comb(n, c1)
    p0 = p(a); lo, hi = max(0, c1 - r2), min(r1, c1)
    return sum(p(x) for x in range(lo, hi + 1) if p(x) <= p0 + 1e-12)

def strat_perm(rows, B=20000):
    """Exact-style permutation test of block A vs 20-56 on 'multiple of ten', shuffling block labels
    within notation strata (word vs sign). Statistic: count of round amounts in block A."""
    obs = sum(r['A'] and r['round'] for r in rows)
    strata = defaultdict(list)
    for r in rows: strata[r['notation']].append(r)
    hits = 0
    for _ in range(B):
        s = 0
        for rr in strata.values():
            labs = [r['A'] for r in rr]; random.shuffle(labs)
            s += sum(l and r['round'] for l, r in zip(labs, rr))
        hits += s >= obs
    return obs, hits / B

bt = {}
W = [r for r in sets['SCROLL_weight'] if r['lead'] >= 10]
def blocklab(r):
    n = int(''.join(ch for ch in r['entry'] if ch.isdigit()))
    return 'A' if n <= 19 else 'BC' if n <= 56 else 'D'
rowsAB = [dict(A=blocklab(r) == 'A', round=r['lead'] % 10 == 0, notation=r['notation'], v=r['lead'], e=r['entry'])
          for r in W if blocklab(r) in ('A', 'BC')]
a = sum(r['A'] and r['round'] for r in rowsAB); b = sum(r['A'] and not r['round'] for r in rowsAB)
c = sum((not r['A']) and r['round'] for r in rowsAB); d = sum((not r['A']) and not r['round'] for r in rowsAB)
bt['amount_level_m10_A_vs_20_56'] = dict(A_round=a, A_n=a + b, BC_round=c, BC_n=c + d, fisher_p=fisher_two_sided(a, b, c, d))
for nt in ('word', 'sign'):
    rr = [r for r in rowsAB if r['notation'] == nt]
    a1 = sum(r['A'] and r['round'] for r in rr); b1 = sum(r['A'] and not r['round'] for r in rr)
    c1 = sum((not r['A']) and r['round'] for r in rr); d1 = sum((not r['A']) and not r['round'] for r in rr)
    bt[f'within_{nt}'] = dict(A_round=a1, A_n=a1 + b1, BC_round=c1, BC_n=c1 + d1, fisher_p=fisher_two_sided(a1, b1, c1, d1))
obs, p = strat_perm(rowsAB)
bt['stratified_by_notation_perm_p_one_sided'] = p
# notation vs roundness overall (all weight amounts >=10)
a2 = sum(r['notation'] == 'word' and r['lead'] % 10 == 0 for r in W); b2 = sum(r['notation'] == 'word' and r['lead'] % 10 != 0 for r in W)
c2 = sum(r['notation'] == 'sign' and r['lead'] % 10 == 0 for r in W); d2 = sum(r['notation'] == 'sign' and r['lead'] % 10 != 0 for r in W)
bt['word_vs_sign_m10'] = dict(word_round=a2, word_n=a2 + b2, sign_round=c2, sign_n=c2 + d2, fisher_p=fisher_two_sided(a2, b2, c2, d2))
aw = sum(r['A'] and r['notation'] == 'word' for r in rowsAB); an = sum(r['A'] for r in rowsAB)
bw = sum((not r['A']) and r['notation'] == 'word' for r in rowsAB); bn = sum(not r['A'] for r in rowsAB)
bt['word_share_A_vs_20_56'] = dict(A_word=aw, A_n=an, BC_word=bw, BC_n=bn, fisher_p=fisher_two_sided(aw, an - aw, bw, bn - bw))
# sensitivity: Puech figures where they differ (6: 42, 14: 14, 15: >=54 -> treat as 54+, 28: 62 or 82, 32: 80, 35: 7, 36: 66, 39: 23.5)
PUECH = {'6': 42, '14': 14, '28': 62, '32': 80, '36': 66}
MILIK = {'6': 42, '32': 60, '35': 4, '36': 66}
LEF = {'6': 42, '32': 60, '36': 67}
for name, alt in (('Puech', PUECH), ('Milik', MILIK), ('Lefkovits', LEF)):
    rr = []
    for r in sets['SCROLL_weight']:
        v = alt.get(r['entry'], r['lead']) if not (r['entry'] == '32' and r['unit'] == 'kkryn') else r['lead']
        if v >= 10 and blocklab(r) in ('A', 'BC'): rr.append((blocklab(r) == 'A', v % 10 == 0))
    a3 = sum(x and y for x, y in rr); b3 = sum(x and not y for x, y in rr); c3 = sum((not x) and y for x, y in rr); d3 = sum((not x) and not y for x, y in rr)
    bt[f'sensitivity_{name}'] = dict(A_round=a3, A_n=a3 + b3, BC_round=c3, BC_n=c3 + d3, fisher_p=fisher_two_sided(a3, b3, c3, d3))
# block-level feature table on all amounts
blk = {}
for B_ in ('A', 'BC', 'D'):
    rows = [r for r in sets['SCROLL_weight'] if blocklab(r) == B_]
    if rows: blk[B_] = {k: v for k, v in feats(rows).items() if k in ('n', 'n_ge10', 'm10', 'sig1', 'm100', 'subunit', 'log10_sd', 'max_over_median', 'benford_mad')}
bt['block_features_weight_amounts'] = blk
json.dump(bt, open(os.path.join(D, 'block_tests.json'), 'w'), indent=1, default=str)

# ------------------------------------------------------------------ formula features per entry
E = rd('scroll_entries.csv'); KZ = rd('kanz_paragraphs.csv')
def rate(rows, f): return sum(f(r) for r in rows) / len(rows) if rows else None
def wilson(k, n, z=1.96):
    if n == 0: return ('', '')
    p = k / n; den = 1 + z * z / n; c = p + z * z / (2 * n); h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (round((c - h) / den, 2), round((c + h) / den, 2))
T = lambda x: x == 'True'
# Massekhet Kelim, coded by hand per mishnah (12 units; see REPORT for the coding)
KEL = [  # (m, number, dig, depth, distance, direction, container, named_place, supernatural, writing)
 (1,0,0,0,0,0,0,0,0,0),(2,0,0,0,0,0,0,0,0,1),(3,1,0,0,0,0,0,0,0,1),(4,1,0,0,0,0,0,1,0,0),(5,1,0,0,0,0,0,0,1,0),(6,1,0,0,0,0,0,0,0,0),
 (7,1,0,0,0,0,0,1,1,0),(8,1,0,0,0,0,0,0,0,0),(9,1,0,0,0,0,0,1,1,0),(10,1,0,0,0,0,0,1,1,0),(11,1,0,0,0,0,0,1,0,0),(12,1,0,0,0,0,0,0,1,0)]
FEATS = [
 ('explicit numeric amount', lambda r: T(r['has_number_amount']), lambda r: T(r['treasure_numbered']), lambda k: k[1]),
 ('dig instruction', lambda r: T(r['dig']), lambda r: T(r['dig']), lambda k: k[2]),
 ('depth stated', lambda r: r['depth_cubits'] != '', lambda r: T(r['depth_stated']), lambda k: k[3]),
 ('depth in cubits', lambda r: r['depth_cubits'] != '', lambda r: T(r['depth_cubit']), lambda k: k[3]),
 ('distance/measure stated', lambda r: r['distance_cubits'] != '' or r['height_cubits'] != '', lambda r: T(r['distance_stated']), lambda k: k[4]),
 ('direction word', lambda r: r['directions'] != '', lambda r: T(r['direction']), lambda k: k[5]),
 ('container named', lambda r: r['container'] != '', lambda r: T(r['container']), lambda k: k[6]),
 ('magic / supernatural element', lambda r: False, lambda r: T(r['magic']), lambda k: k[8]),
]
form = []
KZc = [r for r in KZ if r['clean'] == 'True']
for name, fs, fk, fl in FEATS:
    row = dict(feature=name)
    for lab, rows, f in (('scroll_all', E, fs), ('scroll_1_19', [r for r in E if r['block'] == 'A'], fs),
                         ('scroll_20_56', [r for r in E if r['block'] in ('B', 'C')], fs),
                         ('kanz_clean', KZc, fk), ('kanz_all_segments', KZ, fk)):
        k = sum(f(r) for r in rows); n = len(rows)
        row[lab] = f'{k}/{n} ({k/n:.2f}; {wilson(k,n)[0]}-{wilson(k,n)[1]})'
    k = sum(fl(x) for x in KEL); row['kelim'] = f'{k}/12 ({k/12:.2f})'
    form.append(row)
with open(os.path.join(D, 'formula_features.csv'), 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, fieldnames=list(form[0].keys())); w.writeheader(); w.writerows(form)

# ------------------------------------------------------------------ totals under unit readings
TAL_KG = {'Lefkovits 2000 p.473 regular talent (via repo)': 21.3, 'Attic talent (Wikipedia)': 26.0, 'heavy common talent, Second Temple (Wikipedia)': 58.9}
def tot(alt=None, karsh_kk=False):
    t = 0.0; kk_part = 0.0
    for r in sets['SCROLL_weight']:
        v = (alt or {}).get(r['entry'], r['value']) if r['unit'] == 'kk' else r['value']
        if r['entry'] == '15' and alt is PUECH: v = 54
        if r['unit'] == 'kk':
            kk_part += v
            t += v / 300 if karsh_kk else v
        else:
            t += v
    return t, kk_part
ut = []
for lab, alt in (('displayed text', None), ('Puech figures', PUECH), ('Milik figures', MILIK), ('Lefkovits figures', LEF)):
    for reading, kar in (('all ככ/ככרין = talents', False), ('ככ = karsh (1/300 talent), ככרין = talents', True)):
        t, kkp = tot(alt, kar)
        row = dict(figures=lab, unit_reading=reading, talents=round(t, 2), kk_sum_as_written=round(kkp, 1))
        for kl, kg in TAL_KG.items(): row[f'tonnes @ {kg} kg'] = round(t * kg / 1000, 2)
        ut.append(row)
gold_ingots = sum(r['value'] for r in sets['SCROLL_all'] if r['unit'] == 'ingots')
with open(os.path.join(D, 'unit_totals.csv'), 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, fieldnames=list(ut[0].keys())); w.writeheader(); w.writerows(ut)

# ------------------------------------------------------------------ print
print('AMOUNT FEATURES')
for r in amount_rows:
    print(f"{r['set']:14s} n={r['n']:4d} ge10={r['n_ge10']:4d} m10={r['m10'] if r['m10'] is None else round(r['m10'],2)} [{r['m10_ci']}] "
          f"sig1={None if r['sig1'] is None else round(r['sig1'],2)} m100={None if r['m100'] is None else round(r['m100'],2)} (n{r['n_ge100']}) "
          f"sub={round(r['subunit'],2)} [{r['subunit_ci']}] myr={round(r['myriad'],2)} lsd={round(r.get('log10_sd',0),2)} "
          f"max/med={round(r.get('max_over_median',0),1)} gini={round(r.get('gini',0),2)} MAD={round(r['benford_mad'],3)} modal={r['modal_value']}({round(r['modal_share'],2)})")
print('\nDOCS'); [print(f"  {r['set']:12s} {r['doc'][:38]:38s} n={r['n']:4d} ge10={r['n_ge10']:3d} m10={r['m10'] if r['m10'] is None else round(r['m10'],2)} sig1={None if r['sig1'] is None else round(r['sig1'],2)} sub={round(r['subunit'],2)}") for r in doc_rows]
print('\nBLOCK TESTS'); print(json.dumps(bt, indent=1, default=str))
print('\nFORMULA'); [print(r) for r in form]
print('\nTOTALS'); [print(r) for r in ut]; print('gold ingots (count):', gold_ingots)

# ------------------------------------------------------------------ extra checks
extra = {}
# (1) reproduce the repo's 7/13 vs 4/26 (per-entry talent sums from deep_analysis/features.py, all sums incl. <10)
TAL = {'1':17,'3':900,'5':40,'6':41,'8':70,'9':10,'11':22,'12a':40,'14':13,'15':14,'16':55,'18':200,'19':70,'20':12,'21':7,
       '23':23,'24':32,'25':42,'26':21,'27':27,'28':22,'29':400,'31':22,'32':82,'34':17,'35':7,'36':65,'37':70,'39':23.5,
       '40':22,'42':9,'44':9,'45':11,'46':62,'47':300,'48':80,'49':17,'53':41,'56':107}
def blk_of(e):
    n = int(''.join(ch for ch in e if ch.isdigit())); return 'A' if n <= 19 else 'BC' if n <= 56 else 'D'
def m10_tab(pairs):
    a = sum(b == 'A' and v % 10 == 0 for b, v in pairs); n1 = sum(b == 'A' for b, v in pairs)
    c = sum(b == 'BC' and v % 10 == 0 for b, v in pairs); n2 = sum(b == 'BC' for b, v in pairs)
    return dict(A=f'{a}/{n1}', BC=f'{c}/{n2}', fisher_p=round(fisher_two_sided(a, n1 - a, c, n2 - c), 4))
extra['repo_version_entry_sums_all'] = m10_tab([(blk_of(e), v) for e, v in TAL.items()])
extra['entry_sums_ge10_only'] = m10_tab([(blk_of(e), v) for e, v in TAL.items() if v >= 10])
amt = [(blk_of(r['entry']), r['lead']) for r in sets['SCROLL_weight']]
extra['amounts_all_incl_lt10'] = m10_tab(amt)
extra['amounts_ge10_only'] = m10_tab([(b, v) for b, v in amt if v >= 10])
# (2) leading digit 1 in the scroll vs Benford (binomial, one-sided low)
from math import comb
n1 = sum(first_digit(r['lead']) == 1 for r in sets['SCROLL_weight']); nn = len(sets['SCROLL_weight'])
extra['scroll_d1'] = dict(observed=n1, n=nn, p_low_vs_benford=round(sum(comb(nn, k) * 0.301**k * 0.699**(nn - k) for k in range(n1 + 1)), 4))
# (3) toy nearest-centroid on standardised per-document features (genuine Greek documents vs legendary texts)
FE = ['m10', 'subunit', 'myriad']
docs = [r for r in doc_rows if r['set'].startswith(('G_', 'L_'))]
def z(rows):
    mu = {f: st.mean(r[f] for r in rows) for f in FE}; sd = {f: st.pstdev([r[f] for r in rows]) or 1 for f in FE}
    return mu, sd
def classify(target, train):
    mu, sd = z(train)
    cen = {}
    for cls in ('G', 'L'):
        rr = [r for r in train if r['set'].startswith(cls)]
        cen[cls] = {f: st.mean((r[f] - mu[f]) / sd[f] for r in rr) for f in FE}
    t = {f: (target[f] - mu[f]) / sd[f] for f in FE}
    dist = {c: math.sqrt(sum((t[f] - cen[c][f]) ** 2 for f in FE)) for c in cen}
    return min(dist, key=dist.get), dist
loo = []
for i, r in enumerate(docs):
    pred, _ = classify(r, docs[:i] + docs[i + 1:]); loo.append((r['doc'], r['set'][0], pred))
extra['nearest_centroid_LOO'] = dict(correct=sum(a == b for _, a, b in loo), n=len(loo), misclassified=[d for d, a, b in loo if a != b])
sc = [r for r in doc_rows if r['set'] == 'SCROLL_weight'][0]
pred, dist = classify(sc, docs)
extra['nearest_centroid_scroll'] = dict(pred=pred, dist={k: round(v, 2) for k, v in dist.items()}, features=FE)
for B_ in ('A', 'BC'):
    rr = [r for r in sets['SCROLL_weight'] if blk_of(r['entry']) == B_]
    p_, d_ = classify(feats(rr), docs); extra[f'nearest_centroid_block_{B_}'] = dict(pred=p_, dist={k: round(v, 2) for k, v in d_.items()})
# (4) bootstrap CI of m10 for blocks A and BC
for B_ in ('A', 'BC'):
    rr = [r for r in sets['SCROLL_weight'] if blk_of(r['entry']) == B_]
    lo, hi = boot_ci(rr, 'm10', B=3000); extra[f'm10_ci_block_{B_}'] = (round(feats(rr)['m10'], 2), round(lo, 2), round(hi, 2))
# (5) scroll value frequencies
extra['scroll_value_counts'] = Counter(r['lead'] for r in sets['SCROLL_weight']).most_common(10)
json.dump(extra, open(os.path.join(D, 'extra_checks.json'), 'w'), indent=1, default=str)
print('\nEXTRA'); print(json.dumps(extra, indent=1, default=str))
