# Run 21 test: Spearman(amount, walking time from Temple Mount), 10,000 permutations of amounts, one-sided (rho <= obs).
import csv, json, sys, math, itertools, numpy as np
from scipy.stats import spearmanr, rankdata
R = '/tmp/claude-0/-home-claude/6e619308-8bee-58f1-9a7e-0bdd6ec66961/scratchpad/amount_gravity_2026-10-27'
units = list(csv.DictReader(open(f'{R}/out/units.csv', encoding='utf-8')))
walk = {g: json.load(open(f'{R}/out/walk_{g}.json'))['times'] for g in ('30m_n8', '90m_n16')}
BANDS = [(0, 1), (1, 3), (3, 6), (6, 12), (12, 99)]   # hours; descriptive only

def rho(x, y): return float(spearmanr(x, y).statistic)

def perm_test(amt, t, seed=20261027, n=10000):
    amt = np.asarray(amt, float); t = np.asarray(t, float); obs = rho(amt, t)
    rt = rankdata(t); ra = rankdata(amt)
    def r_of(rA):  # Pearson on ranks, vectorised
        a = rA - rA.mean(axis=-1, keepdims=True); b = rt - rt.mean()
        return (a * b).sum(-1) / np.sqrt((a ** 2).sum(-1) * (b ** 2).sum())
    rng = np.random.default_rng(seed)
    P = np.array([rng.permutation(len(ra)) for _ in range(n)])
    null = r_of(ra[P])
    out = dict(n=len(amt), rho=round(obs, 4), p_perm10k=float((null <= obs + 1e-12).mean()))
    if math.factorial(len(amt)) <= 4_000_000:
        E = np.array(list(itertools.permutations(range(len(ra)))))
        nullE = r_of(ra[E]); out['p_exact'] = float((nullE <= obs + 1e-12).mean()); out['n_orderings'] = len(E)
    return out

def subset(flag, need='kg_karsh', ok_only=False):
    return [u for u in units if u[flag] == '1' and u[need] != '' and (not ok_only or u['any_uncertain'] == '0')]

results = {}
for setname, flag in [('A', 'in_A'), ('D1_deviation', 'in_D1'), ('B', 'in_B')]:
    for ok_only in (False, True):
        U = subset(flag, ok_only=ok_only)
        for g in ('30m_n8', '90m_n16'):
            for metric in ('out_h', 'back_h', 'straight_km'):
                if g == '90m_n16' and metric == 'straight_km': continue
                t = [walk[g][u['place_id']][metric] for u in U]
                for reading in ('kg_karsh', 'kg_talent'):
                    key = f'{setname}|{"ok_only" if ok_only else "all_status"}|{g}|{metric}|{reading}'
                    results[key] = perm_test([float(u[reading]) for u in U], t)
                    results[key]['entries'] = [u['entry'] for u in U]

# per-unit table (primary grid, outbound)
table = []
for u in units:
    w = walk['30m_n8'][u['place_id']]; w9 = walk['90m_n16'][u['place_id']]
    table.append(dict(entry=u['entry'], place=u['place_id'], region=u['region'], A=u['in_A'], D1=u['in_D1'], B=u['in_B'],
                      sums=u['sums'], kg_karsh=u['kg_karsh'], kg_talent=u['kg_talent'], counts=u['counts'],
                      walk_out_h_30m=w['out_h'], walk_back_h_30m=w['back_h'], walk_out_h_90m=w9['out_h'], straight_km=w['straight_km']))

# counts scored separately (set A and B), descriptive
counts = {}
for setname, flag in [('A', 'in_A'), ('B', 'in_B')]:
    C = [u for u in units if u[flag] == '1' and u['counts'] and u['kg_karsh'] == '']
    rows = [(u['entry'], u['counts'], float(u['counts'].split()[0]), walk['30m_n8'][u['place_id']]['out_h']) for u in C]
    counts[setname] = dict(rows=rows)
    if len(rows) >= 3:
        counts[setname]['rho_count_vs_walk'] = round(rho([r[2] for r in rows], [r[3] for r in rows]), 4)
        counts[setname]['perm'] = perm_test([r[2] for r in rows], [r[3] for r in rows])

# totals per region and per band
def totals(flag):
    U = [u for u in units if u[flag] == '1' and u['kg_karsh'] != '']
    reg = {}; band = {}
    for u in U:
        t = walk['30m_n8'][u['place_id']]['out_h']
        b = next(f'{lo}-{hi} h' if hi < 99 else f'>={lo} h' for lo, hi in BANDS if lo <= t < hi)
        for d, k in ((reg, u['region']), (band, b)):
            x = d.setdefault(k, dict(n=0, kg_karsh=0.0, kg_talent=0.0, entries=[]))
            x['n'] += 1; x['kg_karsh'] += float(u['kg_karsh']); x['kg_talent'] += float(u['kg_talent']); x['entries'].append(u['entry'])
    for d in (reg, band):
        for x in d.values(): x['kg_karsh'] = round(x['kg_karsh'], 2); x['kg_talent'] = round(x['kg_talent'], 1)
    return dict(region=reg, band=dict(sorted(band.items(), key=lambda kv: float(kv[0].lstrip('>=').split('-')[0].split()[0]))))
tot = {s: totals(f) for s, f in [('A', 'in_A'), ('B', 'in_B')]}
json.dump(dict(results=results, table=table, counts=counts, totals=tot), open(f'{R}/out/gravity_results.json', 'w'), indent=1, ensure_ascii=False)
for k, v in results.items(): print(k, v)
print(json.dumps(counts, ensure_ascii=False, indent=0)); print(json.dumps(tot, indent=0))
