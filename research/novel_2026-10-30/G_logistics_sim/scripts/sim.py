# Direction G: trip-level Monte Carlo logistics model of the Copper Scroll concealment.
# Frozen with PROTOCOL_FROZEN.md. usage:
#   python3 -I sim.py <repo_root> <walk_times_90m.json> <out_dir> [--smoke]
# --smoke replaces every sum with 1 unit of value 1 (synthetic) to test the code path only.
import sys, csv, json, math, os
import numpy as np

REPO, WALK, OUT = sys.argv[1:4]
SMOKE = '--smoke' in sys.argv
SEED = 20261030
NDRAW = 300 if SMOKE else 4000
SOBOL_N = 2 ** 7 if SMOKE else 2 ** 12
os.makedirs(OUT, exist_ok=True)

SUMS = f'{REPO}/research/first_tests_2026-10-24/method10_hoards/scroll_sums.json'
POST = f'{REPO}/research/agent_review_2026-10-07/wave2/W2B_model_v1/outputs_v3/posteriors_v2_v3.csv'
PLACES = f'{REPO}/research/agent_review_2026-10-07/wave2/W2B_model_v1/inputs_v3/places_v3.csv'

# ---------------- frozen scenario lists ----------------
READINGS = ['talent', 'karsh', 'all_small']          # all_small = hypothetical lower bound, not source-attested
ORIGINS = {'temple': 'JER', 'qumran': 'QUMRAN', 'jericho': 'JERICHO'}
SPREADS = ['map', 'posterior', 'uniform', 'local']
MODES = ['porter', 'donkey', 'mule']
WINDOWS = {  # name: (max nights, corridor rule)
    'W1_open_66_68': (575, 'open'),            # 8 Dius 66 (BJ II 19.9) -> 3 Desius 68 (BJ IV 8.1)
    'W2_encircled_68_70': (665, 'origin_region'),  # 3 Desius 68 -> 14 Xanthicus 70 (BJ IV 9.1; BJ V 13.7)
    'W3_sealed_70': (115, 'intramural'),       # 14 Xanthicus 70 (BJ V 13.7) -> 10 Lous 70 (BJ VI 4.5); wall BJ V 12.2
}
CREWS = [3, 10, 20, 50, 100, 300]
N_SECRET = 10        # Mishnah Shekalim 5:2: no fewer than 7 amarkalin and 3 gizbarim
INTRAMURAL_H = 0.35  # W3 proxy: JER-region destinations within 0.35 h walk of the Temple

# continuous parameter priors (uniform unless stated) -- all ranges frozen
PRI = dict(
    talent_kg=(20.4, 42.6),       # light 21.3 (Lefkovits 2000 p.473, via method 10 registration) .. heavy 42.6
    load_porter=(20.0, 60.0),     # kg; Roman soldier 20-45 kg, Marian legionary ~55 kg (Luc 2018 via imperiumromanum.pl)
    load_donkey=(50.0, 100.0),    # kg; Cotterell & Kaminga 1990 p.194 donkey 80-100 kg (via Adams 2007); 50 kg welfare floor
    load_mule=(90.0, 200.0),      # kg; US Army 20% body mass ~91 kg; Indian 1965 rule cap 200 kg (via Wikipedia 'Pack animal')
    k_animals=(1, 4),             # animals per handler, integer, ASSUMPTION
    f_load=(0.6, 1.0),            # loaded / unloaded Tobler speed; porters 3-4 km/h (Bastien et al. 2016) vs Tobler ~5 km/h flat
    f_night=(0.5, 0.9),           # night-walking speed factor, ASSUMPTION
    hours=(6.0, 10.0),            # usable walking hours per night (computed night length 9.8-13.9 h at 31.78 N minus overhead)
    duty=(0.5, 1.0),              # fraction of nights worked, ASSUMPTION
    overhead=(1.0, 10.0),         # concealment person-nights per weighed entry, ASSUMPTION
    T_op=(7.0, 575.0),            # Sobol Y2 only: operation length, nights, log-uniform, ASSUMPTION
)
HANDLING_H = 0.5  # loading/unloading per round trip, hours (fixed)

# ---------------- inputs ----------------
sums = json.load(open(SUMS))
assert len(sums) == 45
if SMOKE:
    sums = [dict(s, value=1.0) for s in sums]
walk = json.load(open(WALK))
places = list(csv.DictReader(open(PLACES, encoding='utf-8')))
region_of = {p['place_id']: p['model_region'] for p in places}
mix = {}
for p in places:
    if p['mixture_of'].strip():
        mix[p['place_id']] = p['mixture_of'].split('|')
    elif p['components'].strip():
        mix[p['place_id']] = [f"{p['place_id']}#{i}" for i in range(len(p['components'].split('|')))]
for r in set(region_of.values()):
    region_of['U_' + r] = r

def times(origin, state):
    """(out_h, back_h) for state, averaging mixture members (MAP/uniform) -- members list returned for sampling."""
    mem = mix.get(state, [state])
    o = [walk['out_h'][origin][m] for m in mem]; b = [walk['back_h'][origin][m] for m in mem]
    return o, b

post = {}
for r in csv.DictReader(open(POST, encoding='utf-8')):
    post.setdefault(r['entry'], []).append((r['state'], float(r['P_v3'])))
entries = sorted({s['entry'] for s in sums}, key=lambda e: (int(''.join(c for c in e if c.isdigit())), e))
listed_states = [p['place_id'] for p in places]

unit_ix = {'kk': 0, 'kkryn': 1, 'kkr': 1}
s_entry = np.array([entries.index(s['entry']) for s in sums])
s_val = np.array([s['value'] for s in sums])
s_unit = np.array([unit_ix[s['unit']] for s in sums])
NE = len(entries)

def unit_factor(reading):
    # mass multiplier per talent_kg for (kk, kkryn/kkr)
    return {'talent': (1.0, 1.0), 'karsh': (1 / 300, 1.0), 'all_small': (1 / 300, 1 / 300)}[reading]

def entry_mass(reading, talent_kg):
    """returns (draws, NE) masses in kg"""
    fk, fr = unit_factor(reading)
    per = s_val * np.where(s_unit == 0, fk, fr)               # in talents
    m = np.zeros(NE); np.add.at(m, s_entry, per)
    return np.outer(talent_kg, m)

def placements(spread, origin, rng, n):
    """returns out_h, back_h arrays (n, NE) and region labels (n, NE) object"""
    O = np.zeros((n, NE)); B = np.zeros((n, NE)); R = np.empty((n, NE), dtype=object)
    for j, e in enumerate(entries):
        if spread == 'local':
            st = ['U_' + ORIGINS[origin]] * n
        elif spread == 'map':
            st = [max(post[e], key=lambda x: x[1])[0]] * n
        elif spread == 'posterior':
            S = [x[0] for x in post[e]]; P = np.array([x[1] for x in post[e]]); P = P / P.sum()
            st = list(rng.choice(S, size=n, p=P))
        elif spread == 'uniform':
            st = list(rng.choice(listed_states, size=n))
        for i, s in enumerate(st):
            o, b = times(origin, s)
            if spread in ('posterior', 'uniform') and len(o) > 1:
                k = rng.integers(len(o)); O[i, j] = o[k]; B[i, j] = b[k]
            else:
                O[i, j] = float(np.mean(o)); B[i, j] = float(np.mean(b))
            R[i, j] = region_of[s]
    return O, B, R

def reachable(R, O, origin, window):
    rule = WINDOWS[window][1]
    if rule == 'open':
        return np.ones(R.shape, bool)
    if origin != 'temple':
        return np.zeros(R.shape, bool)   # Jericho garrisoned / Jordan valley occupied from June 68 (BJ IV 9.1)
    ok = (R == 'JER')
    if rule == 'intramural':
        ok &= (O <= INTRAMURAL_H)
    return ok

def person_nights(M, O, B, mode, p):
    """M,O,B: (n,NE); p: dict of (n,) arrays. returns P (n,), loads (n,NE), nights_per_load (n,NE)"""
    L = {'porter': p['load_porter'], 'donkey': p['load_donkey'], 'mule': p['load_mule']}[mode][:, None]
    loads = np.ceil(M / L - 1e-12)
    v = p['f_night'][:, None]
    rt = O / (v * p['f_load'][:, None]) + B / v + HANDLING_H
    H = p['hours'][:, None]
    trips_per_night = np.floor(H / rt)
    npl = np.where(trips_per_night >= 1, 1.0 / np.maximum(trips_per_night, 1), np.ceil(rt / H))
    carrier_nights = loads * npl
    people = carrier_nights if mode == 'porter' else carrier_nights / p['k_animals'][:, None]
    weighed = (M > 0)
    P = people.sum(1) + p['overhead'] * weighed.sum(1)
    return P, loads, npl

def draw_params(rng, n):
    p = {}
    for k, (a, b) in PRI.items():
        if k == 'k_animals':
            p[k] = rng.integers(a, b + 1, size=n).astype(float)
        elif k == 'T_op':
            p[k] = np.exp(rng.uniform(math.log(a), math.log(b), n))
        else:
            p[k] = rng.uniform(a, b, n)
    return p

# ---------------- envelope ----------------
rng = np.random.default_rng(SEED)
par = draw_params(rng, NDRAW)            # common random numbers across all cells
kk_entries = np.zeros(NE, bool)
for s in sums:
    if s['unit'] == 'kk': kk_entries[entries.index(s['entry'])] = True
env = []; paired = []
for origin in ORIGINS:
    for spread in SPREADS:
        prng = np.random.default_rng(SEED + 100 * list(ORIGINS).index(origin) + SPREADS.index(spread))
        O, B, R = placements(spread, origin, prng, NDRAW)
        for mode in MODES:
            Pr = {}
            for reading in READINGS:
                M = entry_mass(reading, par['talent_kg'])
                P, loads, npl = person_nights(M, O, B, mode, par)
                Pr[reading] = P
                cap_people = {'porter': 1.0, 'donkey': par['k_animals'], 'mule': par['k_animals']}[mode]
                for window, (Tmax, _) in WINDOWS.items():
                    ok_route = reachable(R, O, origin, window)
                    route_all = ok_route.all(1)
                    Nreq = P / (Tmax * par['duty'])
                    for N in CREWS:
                        feas = route_all & (Nreq <= N)
                        # per-entry single night-trip with crew N: all loads carried at once and round trip fits one night
                        cap = N * (cap_people if np.ndim(cap_people) == 0 else cap_people[:, None])
                        single = (loads <= cap) & (npl <= 1.0)
                        env.append(dict(reading=reading, origin=origin, spread=spread, mode=mode, window=window,
                                        T_max_nights=Tmax, crew_N=N,
                                        F_feasible=round(float(feas.mean()), 4),
                                        F_route_all=round(float(route_all.mean()), 4),
                                        frac_entries_reachable=round(float(ok_route.mean()), 4),
                                        P_person_nights_p05=round(float(np.percentile(P, 5)), 1),
                                        P_person_nights_p50=round(float(np.percentile(P, 50)), 1),
                                        P_person_nights_p95=round(float(np.percentile(P, 95)), 1),
                                        N_req_p50=round(float(np.percentile(Nreq, 50)), 2),
                                        N_req_p95=round(float(np.percentile(Nreq, 95)), 2),
                                        total_tonnes_p50=round(float(np.percentile(M.sum(1), 50)) / 1000, 3),
                                        single_trip_frac_kk_entries=round(float(single[:, kk_entries].mean()), 4),
                                        single_trip_frac_all_weighed=round(float(single.mean()), 4)))
            r = Pr['talent'] / Pr['karsh']
            paired.append(dict(origin=origin, spread=spread, mode=mode,
                               ratio_talent_karsh_p05=round(float(np.percentile(r, 5)), 3),
                               ratio_talent_karsh_p50=round(float(np.percentile(r, 50)), 3),
                               ratio_talent_karsh_p95=round(float(np.percentile(r, 95)), 3)))

def wcsv(name, rows):
    with open(f'{OUT}/{name}', 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); [w.writerow(x) for x in rows]
wcsv('feasibility_envelope.csv', env)
wcsv('paired_ratio_talent_karsh.csv', paired)

# ---------------- verdict (frozen rule) ----------------
def F(reading, origin, spread, mode, window='W1_open_66_68', N=N_SECRET):
    for x in env:
        if (x['reading'], x['origin'], x['spread'], x['mode'], x['window'], x['crew_N']) == (reading, origin, spread, mode, window, N):
            return x['F_feasible']
cells = []
for origin in ORIGINS:
    for spread in ('map', 'posterior'):
        for mode in MODES:
            ft, fk = F('talent', origin, spread, mode), F('karsh', origin, spread, mode)
            if ft < 0.05 and fk >= 0.50: c = 'excluded'
            elif fk - ft >= 0.25: c = 'constrained'
            elif abs(fk - ft) < 0.25: c = 'unaffected'
            else: c = 'other'
            cells.append(dict(origin=origin, spread=spread, mode=mode, F_talent=ft, F_karsh=fk,
                              F_all_small=F('all_small', origin, spread, mode), cls=c))
n_exc = sum(c['cls'] == 'excluded' for c in cells); n_con = sum(c['cls'] == 'constrained' for c in cells)
n_un = sum(c['cls'] == 'unaffected' for c in cells)
if n_exc >= 12: overall = 'excluded'
elif n_exc + n_con >= 9: overall = 'constrained'
elif n_un >= 10: overall = 'unaffected'
else: overall = 'mixed'

# ---------------- Sobol (Saltelli / Jansen via SALib) ----------------
from SALib.sample import sobol as sobol_sample
from SALib.analyze import sobol as sobol_analyze
NPLACE = 2048
place_rng = np.random.default_rng(SEED + 1)
PL = {o: placements('posterior', o, place_rng, NPLACE)[:2] for o in ORIGINS}

def sobol_run(readings, label):
    names = ['reading', 'talent_kg', 'mode', 'load_porter', 'load_donkey', 'load_mule', 'k_animals', 'f_load',
             'f_night', 'hours', 'overhead', 'origin', 'placement', 'duty', 'T_op']
    prob = dict(num_vars=len(names), names=names, bounds=[[0, 1]] * len(names))
    X = sobol_sample.sample(prob, SOBOL_N, calc_second_order=False, seed=SEED)
    n = X.shape[0]
    def lin(u, a, b): return a + u * (b - a)
    rd = np.minimum((X[:, 0] * len(readings)).astype(int), len(readings) - 1)
    md = np.minimum((X[:, 2] * 3).astype(int), 2)
    og = np.minimum((X[:, 11] * 3).astype(int), 2)
    pi = np.minimum((X[:, 12] * NPLACE).astype(int), NPLACE - 1)
    p = dict(talent_kg=lin(X[:, 1], *PRI['talent_kg']), load_porter=lin(X[:, 3], *PRI['load_porter']),
             load_donkey=lin(X[:, 4], *PRI['load_donkey']), load_mule=lin(X[:, 5], *PRI['load_mule']),
             k_animals=np.minimum(np.floor(lin(X[:, 6], 1, 5)), 4), f_load=lin(X[:, 7], *PRI['f_load']),
             f_night=lin(X[:, 8], *PRI['f_night']), hours=lin(X[:, 9], *PRI['hours']),
             overhead=lin(X[:, 10], *PRI['overhead']), duty=lin(X[:, 13], *PRI['duty']),
             T_op=np.exp(lin(X[:, 14], math.log(PRI['T_op'][0]), math.log(PRI['T_op'][1]))))
    Y1 = np.zeros(n)
    olist = list(ORIGINS)
    for ri, reading in enumerate(readings):
        for mi, mode in enumerate(MODES):
            for oi, o in enumerate(olist):
                sel = (rd == ri) & (md == mi) & (og == oi)
                if not sel.any(): continue
                ps = {k: v[sel] for k, v in p.items()}
                M = entry_mass(reading, ps['talent_kg'])
                O = PL[o][0][pi[sel]]; B = PL[o][1][pi[sel]]
                P, _, _ = person_nights(M, O, B, mode, ps)
                Y1[sel] = np.log10(P)
    Y2 = Y1 - np.log10(p['T_op'] * p['duty'])
    rows = []
    for yname, Y in (('Y1_log10_person_nights', Y1), ('Y2_log10_crew_required', Y2)):
        Si = sobol_analyze.analyze(prob, Y, calc_second_order=False, seed=SEED, print_to_console=False)
        for k, nm in enumerate(names):
            rows.append(dict(setting=label, output=yname, factor=nm, factor_class=CLASS[nm],
                             S1=round(float(Si['S1'][k]), 4), S1_conf=round(float(Si['S1_conf'][k]), 4),
                             ST=round(float(Si['ST'][k]), 4), ST_conf=round(float(Si['ST_conf'][k]), 4)))
    return rows, n
CLASS = dict(reading='scenario', mode='scenario', origin='scenario', placement='scenario',
             talent_kg='sourced', load_porter='sourced', load_donkey='sourced', load_mule='sourced',
             f_load='sourced', hours='sourced',
             k_animals='unconstrained', f_night='unconstrained', overhead='unconstrained',
             duty='unconstrained', T_op='unconstrained')
rowsA, nA = sobol_run(['talent', 'karsh'], 'A_talent_vs_karsh')
rowsB, nB = sobol_run(['talent', 'karsh', 'all_small'], 'B_three_readings')
wcsv('sensitivity_indices.csv', rowsA + rowsB)

def st(rows, out, f): return next(r['ST'] for r in rows if r['output'] == out and r['factor'] == f)
Y1 = 'Y1_log10_person_nights'
st_read = st(rowsA, Y1, 'reading')
st_unc_max = max(st(rowsA, Y1, f) for f in ('k_animals', 'f_night', 'overhead'))
F1 = overall == 'unaffected'
F2 = (st_read < 0.05) or (st_read < st_unc_max)
summary = dict(smoke=SMOKE, ndraw=NDRAW, sobol_base_N=SOBOL_N, sobol_evals=[nA, nB], n_sums=len(sums),
               n_weighed_entries=NE, main_cells=cells, counts=dict(excluded=n_exc, constrained=n_con, unaffected=n_un),
               overall_talent_verdict=overall,
               sobolA_Y1_ST_reading=st_read, sobolA_Y1_ST_max_unconstrained=st_unc_max,
               F1_no_discrimination=F1, F2_unconstrained_dominates_or_reading_insensitive=F2)
json.dump(summary, open(f'{OUT}/summary.json', 'w'), indent=1)
print(json.dumps({k: v for k, v in summary.items() if k != 'main_cells'}, indent=1))
